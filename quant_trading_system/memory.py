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

import frontmatter
import yaml

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


@dataclass
class StrategyFile:
    """A parsed strategy markdown file."""

    id: str
    type: str  # "equity" | "options" | "archived"
    path: Path
    frontmatter: dict[str, Any]
    body: str

    @property
    def name(self) -> str:
        return self.frontmatter.get("name", self.id)

    @property
    def status(self) -> str:
        return self.frontmatter.get("status", "active")

    def to_full_text(self) -> str:
        """Reassemble frontmatter + body into the on-disk format."""
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
        }


def _strategy_path_for(strategy_id: str, type_hint: str | None = None) -> Path | None:
    """Resolve a strategy_id to its file path, searching all type subdirs."""
    candidates = []
    if type_hint == "equity":
        candidates = [EQUITY_DIR]
    elif type_hint == "options":
        candidates = [OPTIONS_DIR]
    elif type_hint == "archived":
        candidates = [ARCHIVED_DIR]
    else:
        candidates = [EQUITY_DIR, OPTIONS_DIR, ARCHIVED_DIR]
    for d in candidates:
        p = d / f"{strategy_id}.md"
        if p.exists():
            return p
    return None


def _load_strategy_file(path: Path) -> StrategyFile:
    """Parse a strategy markdown file from disk."""
    post = frontmatter.load(path)
    fm = dict(post.metadata)
    body = post.content
    sid = fm.get("id") or path.stem
    # Type from parent dir name (equity/options/archived) takes precedence
    type_from_dir = path.parent.name
    if type_from_dir not in ("equity", "options", "archived"):
        type_from_dir = fm.get("type", "equity")
    return StrategyFile(id=sid, type=type_from_dir, path=path, frontmatter=fm, body=body)


def list_strategies(
    status: str | None = None,
    type_filter: str | None = None,
    include_archived: bool = False,
) -> list[StrategyFile]:
    """List all strategies on disk, optionally filtered.

    Args:
        status: filter by frontmatter `status` (active, testing, deprecated, …)
        type_filter: "equity" or "options"
        include_archived: include the archived/ subdir

    Returns:
        List of StrategyFile, sorted by id.
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
        for p in sorted(d.glob("*.md")):
            try:
                sf = _load_strategy_file(p)
            except Exception:  # malformed file — skip but don't crash the run
                continue
            if status is not None and sf.status != status:
                continue
            out.append(sf)
    return out


def read_strategy(strategy_id: str) -> StrategyFile | None:
    """Read a single strategy by id. Returns None if not found."""
    _ensure_dirs()
    p = _strategy_path_for(strategy_id)
    if p is None:
        return None
    return _load_strategy_file(p)


def update_strategy(
    strategy_id: str,
    frontmatter_updates: dict[str, Any] | None = None,
    body: str | None = None,
) -> StrategyFile:
    """Update an existing strategy file in place.

    Either field can be omitted to leave it unchanged. Frontmatter updates merge
    (top-level keys); pass `body=...` to fully replace the markdown body.
    """
    sf = read_strategy(strategy_id)
    if sf is None:
        raise FileNotFoundError(f"Strategy not found: {strategy_id}")
    if frontmatter_updates:
        sf.frontmatter.update(frontmatter_updates)
    if body is not None:
        sf.body = body
    sf.path.write_text(sf.to_full_text(), encoding="utf-8")
    return sf


def create_strategy(
    strategy_id: str,
    type: str,
    frontmatter_data: dict[str, Any],
    body: str,
) -> StrategyFile:
    """Create a new strategy file. `type` must be 'equity' or 'options'."""
    if type not in ("equity", "options"):
        raise ValueError(f"type must be 'equity' or 'options', got {type!r}")
    _ensure_dirs()
    target_dir = EQUITY_DIR if type == "equity" else OPTIONS_DIR
    path = target_dir / f"{strategy_id}.md"
    if path.exists():
        raise FileExistsError(f"Strategy already exists: {strategy_id}")
    fm = dict(frontmatter_data)
    fm.setdefault("id", strategy_id)
    fm.setdefault("type", type)
    fm.setdefault("status", "testing")
    sf = StrategyFile(id=strategy_id, type=type, path=path, frontmatter=fm, body=body)
    path.write_text(sf.to_full_text(), encoding="utf-8")
    return sf


def archive_strategy(strategy_id: str, reason: str = "") -> StrategyFile:
    """Move a strategy to the archived/ subdir and set status=archived.

    Adds a `# Archive note` section to the body with the reason and date.
    """
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
    new_path = ARCHIVED_DIR / sf.path.name
    new_path.write_text(sf.to_full_text(), encoding="utf-8")
    sf.path.unlink()
    sf.path = new_path
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
    post = frontmatter.load(ACTIVE_STRATEGY_FILE)
    fm = dict(post.metadata)
    return {
        "strategy_id": fm.get("strategy_id", ""),
        "since": fm.get("since", ""),
        "reason": fm.get("reason", ""),
        "notes": post.content,
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
