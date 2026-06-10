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

ACTIVE_STRATEGY_FILE = STATE_DIR / "active_strategy.md"            # legacy single
ACTIVE_STRATEGIES_FILE = STATE_DIR / "active_strategies.md"        # new plural
LIBRARY_GAPS_FILE = STATE_DIR / "library_gaps.md"                  # triage-marked unclaimed
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


# ---------------------------------------------------------------------------
# Active strategy SET (new, plural). Multiple strategies can be active
# simultaneously, each owning a slice of the universe.
#
# File format — `state/active_strategies.md`:
#
#     ---
#     strategies:
#       - id: equity_trend_following_ema_cross
#         symbols: [AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA]
#         since: 2026-05-27
#         reason: "Operator-assigned attribution for the inherited 8 positions."
#       - id: equity_mean_reversion_bollinger
#         symbols: [DIS, KO]
#         since: 2026-06-15
#         reason: "Head-to-head backtest 2026-06-12 beat trend on these symbols."
#     ---
#     <free-form notes>
#
# Contract:
#   - Every symbol claimed in `symbols` is owned exclusively by that
#     strategy. Two active strategies cannot claim the same symbol.
#   - Conflicts must be resolved BEFORE landing in this file, via the
#     research agent's head-to-head backtest. The trader never adjudicates
#     a runtime conflict.
#   - Strategies with an empty `symbols: []` claim no symbols — they are
#     idle but listed for visibility. `cli execute` skips them.
#   - Unclaimed symbols in the universe are surfaced as library-gap
#     diagnostics (no responder) — they are NOT auto-assigned.
# ---------------------------------------------------------------------------


@dataclass
class ActiveStrategyClaim:
    """One entry in active_strategies.md."""
    strategy_id: str
    symbols: list[str]
    since: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "symbols": list(self.symbols),
            "since": self.since,
            "reason": self.reason,
        }


def read_active_strategies() -> list[ActiveStrategyClaim]:
    """Return the plural active-strategy set, in declared order.

    Falls back to the legacy singular ``active_strategy.md`` if the plural
    file does not exist; in that case the returned list has one entry with
    an empty ``symbols`` claim (meaning "no explicit claim, run against the
    full universe like the legacy path did").
    """
    if ACTIVE_STRATEGIES_FILE.exists():
        fm, _body = _parse_frontmatter(ACTIVE_STRATEGIES_FILE)
        raw = fm.get("strategies", []) or []
        out: list[ActiveStrategyClaim] = []
        for entry in raw:
            if not isinstance(entry, dict):
                continue
            sid = str(entry.get("id", "")).strip()
            if not sid:
                continue
            syms_raw = entry.get("symbols", []) or []
            if isinstance(syms_raw, str):
                # Allow comma-separated string as a tolerance.
                syms_raw = [s.strip() for s in syms_raw.split(",") if s.strip()]
            syms = [str(s).upper() for s in syms_raw if str(s).strip()]
            out.append(ActiveStrategyClaim(
                strategy_id=sid,
                symbols=syms,
                since=str(entry.get("since", "")),
                reason=str(entry.get("reason", "")),
            ))
        return out
    # Legacy fallback.
    legacy = read_active_strategy()
    sid = legacy.get("strategy_id", "")
    if not sid:
        return []
    return [ActiveStrategyClaim(
        strategy_id=sid,
        symbols=[],                        # no explicit claim = run on full universe
        since=str(legacy.get("since", "")),
        reason=str(legacy.get("reason", "")),
    )]


def write_active_strategies(claims: Iterable[ActiveStrategyClaim], notes: str = "") -> Path:
    """Write the plural active-strategy set, enforcing the no-conflict rule.

    Raises ValueError if two claims share a symbol — every symbol must be
    owned by exactly one strategy. Use the research agent's head-to-head
    battery to break ties before calling this.
    """
    _ensure_dirs()
    claims_list = list(claims)

    # Conflict check: every symbol must be claimed at most once.
    seen: dict[str, str] = {}
    for c in claims_list:
        for sym in c.symbols:
            if sym in seen and seen[sym] != c.strategy_id:
                raise ValueError(
                    f"symbol {sym!r} is claimed by both "
                    f"{seen[sym]!r} and {c.strategy_id!r}. The harness does "
                    "not adjudicate runtime conflicts — run a head-to-head "
                    "backtest (cli head-to-head) and let only the winner "
                    "claim it."
                )
            seen[sym] = c.strategy_id

    fm = {
        "strategies": [
            {
                "id": c.strategy_id,
                "symbols": list(c.symbols),
                "since": c.since or dt.date.today().isoformat(),
                "reason": c.reason,
            }
            for c in claims_list
        ]
    }
    fm_yaml = yaml.safe_dump(fm, sort_keys=False, default_flow_style=False).strip()
    body = notes.lstrip() if notes else (
        "Active strategy set. Each entry owns its declared symbols "
        "exclusively. Conflicts are resolved by head-to-head backtest at "
        "the research layer, never at runtime.\n"
    )
    ACTIVE_STRATEGIES_FILE.write_text(
        f"---\n{fm_yaml}\n---\n\n{body}", encoding="utf-8"
    )
    return ACTIVE_STRATEGIES_FILE


def add_active_strategy(
    strategy_id: str,
    *,
    symbols: list[str],
    reason: str,
) -> ActiveStrategyClaim:
    """Add or replace a strategy in the active set.

    If the strategy is already active, its symbols are REPLACED with the
    new claim list (call with the union if you want to extend). The
    no-conflict rule is enforced against every other claim in the set.
    """
    syms = [s.upper().strip() for s in symbols if s.strip()]
    current = [c for c in read_active_strategies() if c.strategy_id != strategy_id]
    new_claim = ActiveStrategyClaim(
        strategy_id=strategy_id,
        symbols=syms,
        since=dt.date.today().isoformat(),
        reason=reason,
    )
    write_active_strategies(current + [new_claim])
    return new_claim


def remove_active_strategy(strategy_id: str, *, reason: str = "") -> bool:
    """Drop a strategy from the active set. Returns True if it was present."""
    current = read_active_strategies()
    kept = [c for c in current if c.strategy_id != strategy_id]
    if len(kept) == len(current):
        return False
    # `reason` isn't stored on the surviving claims; it belongs in
    # last_handoff.md's narrative. We just persist the new set.
    _ = reason
    write_active_strategies(kept)
    return True


def unclaimed_symbols(universe: Iterable[str]) -> list[str]:
    """Return symbols in `universe` that no active strategy claims.

    Library-gap diagnostic: these are the symbols the harness is tracking
    (positions / news / extras / strategy frontmatter) but no algorithmic
    responder owns.

    Symbols flagged in `state/library_gaps.md` (triaged → no responder
    beats baseline) are also counted as unclaimed — they ARE unclaimed.
    The library_gap registry is metadata about why, not a claim. Callers
    deciding whether to block on unclaimed symbols should filter against
    ``library_gap_symbols()`` separately.
    """
    universe_set = {str(s).upper() for s in universe}
    claimed: set[str] = set()
    for c in read_active_strategies():
        claimed.update(c.symbols)
    return sorted(universe_set - claimed)


# ---------------------------------------------------------------------------
# Library-gap registry (state/library_gaps.md)
#
# When `cli triage-symbol` runs and no library strategy clears baseline
# Sharpe for the symbol, the verdict is "true_library_gap" and the
# symbol is appended here. The unclaimed-gate in execute treats
# library-gap symbols as "tolerated unclaimed" — execute proceeds, the
# symbol simply isn't traded that day, and Saturday research uses this
# file as its top-priority queue for new-template work.
#
# File format — `state/library_gaps.md`:
#
#     ---
#     gaps:
#       - symbol: NUVL
#         gap_type: ma_arbitrage
#         triaged_at: 2026-06-10
#         reason: "no library strategy declares gap_type ma_arbitrage"
#         top_strategy: null
#         top_sharpe: null
#         baseline_sharpe: 0.5
#     ---
#     <free-form notes>
# ---------------------------------------------------------------------------


@dataclass
class LibraryGap:
    symbol: str
    gap_type: str
    triaged_at: str
    reason: str
    top_strategy: str | None = None
    top_sharpe: float | None = None
    baseline_sharpe: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "gap_type": self.gap_type,
            "triaged_at": self.triaged_at,
            "reason": self.reason,
            "top_strategy": self.top_strategy,
            "top_sharpe": self.top_sharpe,
            "baseline_sharpe": self.baseline_sharpe,
        }


def read_library_gaps() -> list[LibraryGap]:
    """Return the current list of triaged-but-unclaimed symbols."""
    if not LIBRARY_GAPS_FILE.exists():
        return []
    fm, _ = _parse_frontmatter(LIBRARY_GAPS_FILE)
    raw = fm.get("gaps", []) or []
    out: list[LibraryGap] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        sym = str(entry.get("symbol", "")).strip().upper()
        if not sym:
            continue
        out.append(LibraryGap(
            symbol=sym,
            gap_type=str(entry.get("gap_type", "") or ""),
            triaged_at=str(entry.get("triaged_at", "") or ""),
            reason=str(entry.get("reason", "") or ""),
            top_strategy=(
                str(entry["top_strategy"])
                if entry.get("top_strategy") not in (None, "")
                else None
            ),
            top_sharpe=(
                float(entry["top_sharpe"])
                if isinstance(entry.get("top_sharpe"), (int, float))
                else None
            ),
            baseline_sharpe=float(entry.get("baseline_sharpe", 0.5)),
        ))
    return out


def write_library_gaps(gaps: Iterable[LibraryGap], notes: str = "") -> Path:
    """Replace the library-gaps file. Use append_library_gap() in normal
    flow; this is for batch edits and Saturday research cleanup."""
    _ensure_dirs()
    gap_list = list(gaps)
    fm = {"gaps": [g.to_dict() for g in gap_list]}
    fm_yaml = yaml.safe_dump(fm, sort_keys=False, default_flow_style=False).strip()
    body = notes.lstrip() if notes else (
        "Symbols the harness is tracking that no library strategy can "
        "respond to. Triage marked them as true_library_gap. Saturday "
        "research is responsible for either adding a template that "
        "handles the gap_type or removing the symbol from the universe.\n"
    )
    LIBRARY_GAPS_FILE.write_text(
        f"---\n{fm_yaml}\n---\n\n{body}", encoding="utf-8"
    )
    return LIBRARY_GAPS_FILE


def append_library_gap(
    symbol: str,
    *,
    gap_type: str,
    reason: str,
    top_strategy: str | None = None,
    top_sharpe: float | None = None,
    baseline_sharpe: float = 0.5,
) -> LibraryGap:
    """Add (or refresh) a library-gap marker for `symbol`. If the symbol
    is already present, the entry is updated with today's triaged_at +
    fresh reason/top_score. Idempotent on identical re-runs.
    """
    sym = symbol.strip().upper()
    today = dt.date.today().isoformat()
    new_gap = LibraryGap(
        symbol=sym,
        gap_type=gap_type,
        triaged_at=today,
        reason=reason,
        top_strategy=top_strategy,
        top_sharpe=top_sharpe,
        baseline_sharpe=baseline_sharpe,
    )
    current = [g for g in read_library_gaps() if g.symbol != sym]
    current.append(new_gap)
    current.sort(key=lambda g: (g.gap_type, g.symbol))
    write_library_gaps(current)
    return new_gap


def clear_library_gap(symbol: str) -> bool:
    """Remove a symbol from the library-gaps registry. Saturday research
    calls this once it has added a strategy that responds and claimed
    the symbol via add_active_strategy. Returns True if removed."""
    sym = symbol.strip().upper()
    current = read_library_gaps()
    kept = [g for g in current if g.symbol != sym]
    if len(kept) == len(current):
        return False
    write_library_gaps(kept)
    return True


def library_gap_symbols() -> list[str]:
    """Convenience: just the symbols currently flagged as library gaps."""
    return sorted({g.symbol for g in read_library_gaps()})


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
