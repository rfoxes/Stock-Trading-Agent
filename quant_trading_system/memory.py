"""Markdown-as-source-of-truth memory layer.

The harness has no database. Everything the agent remembers between runs lives
on disk as plain markdown:

    quant_trading_system/knowledge_base/
        strategies/equity/*.md         — strategy definitions (YAML frontmatter + body)
        strategies/options/*.md
        conclusions/YYYY-MM-DD.md      — one file per run, the day's narrative
        state/active_strategy.md       — which strategy is currently in use
        state/last_handoff.md          — message from previous Claude to next Claude
        state/summary.md               — rolling long-term takeaways
    trades/YYYY-MM.jsonl               — append-only trade journal (separate module)

This module owns reading and writing those files. The orchestrator and the
agent tools both go through these helpers; nobody touches paths directly.
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


# ---------------------------------------------------------------------------
# Minimal YAML-frontmatter parser (replaces python-frontmatter dep)
# ---------------------------------------------------------------------------

_FM_DELIM = "---"


def _parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body_text) for a markdown file.

    Accepts:
        ---\\n
        key: value\\n
        ---\\n
        body...
    Files without leading frontmatter return ({}, full_text).
    """
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if not lines or lines[0].strip() != _FM_DELIM:
        return {}, text
    # Find the closing delimiter
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == _FM_DELIM:
            end = i
            break
    if end is None:
        return {}, text
    fm_text = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :])
    # Strip a single leading blank line in the body if present
    if body.startswith("\n"):
        body = body[1:]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}
    if not isinstance(fm, dict):
        fm = {}
    return fm, body

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Resolved relative to the repo root (parent of the package).
_PKG_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PKG_DIR.parent

KB_DIR = _PKG_DIR / "knowledge_base"
STRATEGIES_DIR = KB_DIR / "strategies"
EQUITY_DIR = STRATEGIES_DIR / "equity"
OPTIONS_DIR = STRATEGIES_DIR / "options"
ARCHIVED_DIR = STRATEGIES_DIR / "archived"
CONCLUSIONS_DIR = KB_DIR / "conclusions"
STATE_DIR = KB_DIR / "state"

ACTIVE_STRATEGY_FILE = STATE_DIR / "active_strategy.md"
HANDOFF_FILE = STATE_DIR / "last_handoff.md"
SUMMARY_FILE = STATE_DIR / "summary.md"

RUNS_DIR = _REPO_ROOT / "runs"
TRADES_DIR = _REPO_ROOT / "trades"
LOCK_FILE = _REPO_ROOT / ".harness.lock"


def _ensure_dirs() -> None:
    for d in (
        EQUITY_DIR,
        OPTIONS_DIR,
        ARCHIVED_DIR,
        CONCLUSIONS_DIR,
        STATE_DIR,
        RUNS_DIR,
        TRADES_DIR,
    ):
        d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Strategy I/O
# ---------------------------------------------------------------------------


_STRATEGY_TEMPLATE_PY = '''"""Strategy: {id}

This file is the executable counterpart to strategy.md. The harness calls
``evaluate(ctx)`` once per scheduled run. Return a list of OrderIntent
objects (or dicts with the same shape) describing the orders you want
submitted today. Return [] for a do-nothing day.

The agent may edit this file when the strategy's logic genuinely changes.
Trivial parameter tweaks belong in strategy.md's frontmatter, not here.
"""

from __future__ import annotations

from typing import Any

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    """Decide what to do today. Return list of OrderIntent (may be empty)."""
    ctx.log.info("evaluate called for {id} regime=%s", ctx.regime.get("regime"))
    return []
'''


@dataclass
class StrategyFile:
    """A strategy on disk = a folder containing strategy.md and (optionally) strategy.py."""

    id: str
    type: str  # "equity" | "options" | "archived"
    dir: Path
    frontmatter: dict[str, Any]
    body: str

    @property
    def md_path(self) -> Path:
        return self.dir / "strategy.md"

    @property
    def py_path(self) -> Path:
        return self.dir / "strategy.py"

    @property
    def name(self) -> str:
        return self.frontmatter.get("name", self.id)

    @property
    def status(self) -> str:
        return self.frontmatter.get("status", "active")

    @property
    def has_script(self) -> bool:
        return self.py_path.exists()

    def to_full_text(self) -> str:
        """Reassemble frontmatter + body into the on-disk strategy.md format."""
        fm_yaml = yaml.safe_dump(self.frontmatter, sort_keys=False).strip()
        return f"---\n{fm_yaml}\n---\n\n{self.body.lstrip()}"

    def summary_dict(self) -> dict[str, Any]:
        """Compact dict for listing in tool responses."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "timeframe": self.frontmatter.get("timeframe", []),
            "market_regime": self.frontmatter.get("market_regime", []),
            "indicators": self.frontmatter.get("indicators", []),
            "has_script": self.has_script,
        }


def _strategy_dir_for(strategy_id: str, type_hint: str | None = None) -> Path | None:
    """Resolve a strategy_id to its folder.

    Two-pass lookup:
      1. Direct: folder name == strategy_id.
      2. Fallback: scan folders and match the `id` in their frontmatter.

    Lets the folder name and the id diverge cleanly (e.g. folder
    `trend_following_ema_cross` holding a strategy whose id is
    `equity_trend_following_ema_cross`).
    """
    if type_hint == "equity":
        candidates = [EQUITY_DIR]
    elif type_hint == "options":
        candidates = [OPTIONS_DIR]
    elif type_hint == "archived":
        candidates = [ARCHIVED_DIR]
    else:
        candidates = [EQUITY_DIR, OPTIONS_DIR, ARCHIVED_DIR]
    # Pass 1: direct name match
    for d in candidates:
        p = d / strategy_id
        if (p / "strategy.md").exists():
            return p
    # Pass 2: scan and match by frontmatter id
    for d in candidates:
        if not d.exists():
            continue
        for sub in d.iterdir():
            md = sub / "strategy.md"
            if not md.exists():
                continue
            try:
                fm, _ = _parse_frontmatter(md)
            except Exception:
                continue
            if fm.get("id") == strategy_id:
                return sub
    return None


def _load_strategy_file(folder: Path) -> StrategyFile:
    """Parse a strategy folder from disk."""
    md = folder / "strategy.md"
    fm, body = _parse_frontmatter(md)
    sid = fm.get("id") or folder.name
    # Type from parent dir name (equity/options/archived)
    type_from_dir = folder.parent.name
    if type_from_dir not in ("equity", "options", "archived"):
        type_from_dir = fm.get("type", "equity")
    return StrategyFile(id=sid, type=type_from_dir, dir=folder, frontmatter=fm, body=body)


def list_strategies(
    status: str | None = None,
    type_filter: str | None = None,
    include_archived: bool = False,
) -> list[StrategyFile]:
    """List all strategies on disk, optionally filtered.

    Each strategy is a folder under strategies/<type>/<id>/ containing a
    strategy.md. Folders without strategy.md are skipped.
    """
    _ensure_dirs()
    dirs: list[Path] = []
    if type_filter == "equity":
        dirs = [EQUITY_DIR]
    elif type_filter == "options":
        dirs = [OPTIONS_DIR]
    else:
        dirs = [EQUITY_DIR, OPTIONS_DIR]
    if include_archived:
        dirs.append(ARCHIVED_DIR)

    out: list[StrategyFile] = []
    for d in dirs:
        if not d.exists():
            continue
        for sub in sorted(d.iterdir()):
            if not sub.is_dir():
                continue
            if not (sub / "strategy.md").exists():
                continue
            try:
                sf = _load_strategy_file(sub)
            except Exception:
                continue
            if status is not None and sf.status != status:
                continue
            out.append(sf)
    return out


def read_strategy(strategy_id: str) -> StrategyFile | None:
    """Read a single strategy by id. Returns None if not found."""
    _ensure_dirs()
    d = _strategy_dir_for(strategy_id)
    if d is None:
        return None
    return _load_strategy_file(d)


def update_strategy(
    strategy_id: str,
    frontmatter_updates: dict[str, Any] | None = None,
    body: str | None = None,
) -> StrategyFile:
    """Update an existing strategy.md in place (does not touch strategy.py)."""
    sf = read_strategy(strategy_id)
    if sf is None:
        raise FileNotFoundError(f"Strategy not found: {strategy_id}")
    if frontmatter_updates:
        sf.frontmatter.update(frontmatter_updates)
    if body is not None:
        sf.body = body
    sf.md_path.write_text(sf.to_full_text(), encoding="utf-8")
    return sf


def update_strategy_script(strategy_id: str, py_source: str) -> StrategyFile:
    """Replace a strategy's strategy.py contents.

    The agent uses this when a strategy's execution logic needs to change
    (vs. just parameter tweaks which go through `update_strategy`).
    """
    sf = read_strategy(strategy_id)
    if sf is None:
        raise FileNotFoundError(f"Strategy not found: {strategy_id}")
    sf.py_path.write_text(py_source, encoding="utf-8")
    return sf


def create_strategy(
    strategy_id: str,
    type: str,
    frontmatter_data: dict[str, Any],
    body: str,
    script: str | None = None,
) -> StrategyFile:
    """Create a new strategy folder with strategy.md (and optionally strategy.py).

    If `script` is None, a template strategy.py is written that returns no
    orders — safe default until the agent fills in the logic.
    """
    if type not in ("equity", "options"):
        raise ValueError(f"type must be 'equity' or 'options', got {type!r}")
    _ensure_dirs()
    target_dir = EQUITY_DIR if type == "equity" else OPTIONS_DIR
    folder = target_dir / strategy_id
    if folder.exists():
        raise FileExistsError(f"Strategy folder already exists: {folder}")
    folder.mkdir(parents=True)
    fm = dict(frontmatter_data)
    fm.setdefault("id", strategy_id)
    fm.setdefault("type", type)
    fm.setdefault("status", "testing")
    sf = StrategyFile(id=strategy_id, type=type, dir=folder, frontmatter=fm, body=body)
    sf.md_path.write_text(sf.to_full_text(), encoding="utf-8")
    sf.py_path.write_text(
        script if script is not None else _STRATEGY_TEMPLATE_PY.format(id=strategy_id),
        encoding="utf-8",
    )
    return sf


def archive_strategy(strategy_id: str, reason: str = "") -> StrategyFile:
    """Move a strategy folder to archived/ and set status=archived."""
    sf = read_strategy(strategy_id)
    if sf is None:
        raise FileNotFoundError(f"Strategy not found: {strategy_id}")
    if sf.type == "archived":
        return sf
    _ensure_dirs()
    sf.frontmatter["status"] = "archived"
    sf.frontmatter["archived_on"] = dt.date.today().isoformat()
    if reason:
        sf.body = sf.body.rstrip() + (
            f"\n\n## Archive note ({dt.date.today().isoformat()})\n\n{reason}\n"
        )
    new_dir = ARCHIVED_DIR / sf.dir.name
    new_dir.mkdir(parents=True, exist_ok=True)
    (new_dir / "strategy.md").write_text(sf.to_full_text(), encoding="utf-8")
    if sf.py_path.exists():
        (new_dir / "strategy.py").write_text(sf.py_path.read_text(encoding="utf-8"), encoding="utf-8")
    # Remove originals
    for f in sf.dir.iterdir():
        f.unlink()
    sf.dir.rmdir()
    sf.dir = new_dir
    sf.type = "archived"
    return sf


# ---------------------------------------------------------------------------
# Conclusions (one file per run)
# ---------------------------------------------------------------------------

_CONCLUSION_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")


def conclusion_path_for(date: dt.date | str | None = None) -> Path:
    if date is None:
        date = dt.date.today()
    if isinstance(date, str):
        date = dt.date.fromisoformat(date)
    return CONCLUSIONS_DIR / f"{date.isoformat()}.md"


def write_conclusion(content: str, date: dt.date | str | None = None) -> Path:
    """Write today's conclusion file. Overwrites if it already exists."""
    _ensure_dirs()
    path = conclusion_path_for(date)
    path.write_text(content, encoding="utf-8")
    return path


def append_conclusion(content: str, date: dt.date | str | None = None) -> Path:
    """Append to today's conclusion file (creates it if absent)."""
    _ensure_dirs()
    path = conclusion_path_for(date)
    sep = "\n\n---\n\n" if path.exists() else ""
    with path.open("a", encoding="utf-8") as f:
        f.write(sep + content)
    return path


def read_recent_conclusions(days: int = 14) -> list[dict[str, Any]]:
    """Return the last `days` conclusion files, oldest first.

    Each entry: {date, path, content}.
    """
    _ensure_dirs()
    cutoff = dt.date.today() - dt.timedelta(days=days)
    results: list[dict[str, Any]] = []
    for p in CONCLUSIONS_DIR.glob("*.md"):
        m = _CONCLUSION_FILENAME_RE.match(p.name)
        if not m:
            continue
        try:
            d = dt.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        if d < cutoff:
            continue
        results.append({"date": d.isoformat(), "path": str(p), "content": p.read_text(encoding="utf-8")})
    results.sort(key=lambda r: r["date"])
    return results


# ---------------------------------------------------------------------------
# State files (handoff, active strategy, summary)
# ---------------------------------------------------------------------------


def read_handoff() -> str:
    if not HANDOFF_FILE.exists():
        return ""
    return HANDOFF_FILE.read_text(encoding="utf-8")


def write_handoff(content: str) -> Path:
    _ensure_dirs()
    HANDOFF_FILE.write_text(content, encoding="utf-8")
    return HANDOFF_FILE


def read_active_strategy() -> dict[str, Any]:
    """Return {strategy_id, since, reason} or empty dict if not set."""
    if not ACTIVE_STRATEGY_FILE.exists():
        return {}
    fm, body = _parse_frontmatter(ACTIVE_STRATEGY_FILE)
    return {
        "strategy_id": fm.get("strategy_id", ""),
        "since": fm.get("since", ""),
        "reason": fm.get("reason", ""),
        "notes": body,
    }


def set_active_strategy(strategy_id: str, reason: str, notes: str = "") -> Path:
    _ensure_dirs()
    fm = {
        "strategy_id": strategy_id,
        "since": dt.date.today().isoformat(),
        "reason": reason,
    }
    fm_yaml = yaml.safe_dump(fm, sort_keys=False).strip()
    body = notes.lstrip() if notes else f"Active strategy as of {fm['since']}.\n"
    ACTIVE_STRATEGY_FILE.write_text(f"---\n{fm_yaml}\n---\n\n{body}", encoding="utf-8")
    return ACTIVE_STRATEGY_FILE


def read_summary() -> str:
    if not SUMMARY_FILE.exists():
        return ""
    return SUMMARY_FILE.read_text(encoding="utf-8")


def write_summary(content: str) -> Path:
    _ensure_dirs()
    SUMMARY_FILE.write_text(content, encoding="utf-8")
    return SUMMARY_FILE


# ---------------------------------------------------------------------------
# Tool-friendly view of memory (used by the orchestrator at startup)
# ---------------------------------------------------------------------------


def load_run_context(recent_conclusion_days: int = 14) -> dict[str, Any]:
    """Bundle everything the agent needs at the start of a run."""
    _ensure_dirs()
    return {
        "today": dt.date.today().isoformat(),
        "active_strategy": read_active_strategy(),
        "handoff_from_previous_run": read_handoff(),
        "summary": read_summary(),
        "recent_conclusions": read_recent_conclusions(days=recent_conclusion_days),
        "strategies_index": [s.summary_dict() for s in list_strategies()],
    }
