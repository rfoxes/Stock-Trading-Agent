"""Gap-type → strategy registry, indexed at read time from each strategy's
frontmatter.

Each strategy.md declares which gap categories it handles via a
``gap_types: [...]`` list in its YAML frontmatter. This module loads
that view across the whole library on demand and exposes a couple of
small lookup helpers.

Why this is not a static map: the strategy library is the source of
truth. Adding a new template strategy to the library should
automatically register it for the gap_types it declares; we don't want
to update a separate table.
"""

from __future__ import annotations

from typing import Iterable

from quant_trading_system import memory


# The canonical taxonomy of gap_types. Strategies should pick from this
# list when declaring `gap_types: [...]` in their frontmatter.
#
# Keep this list SMALL and stable. New gap_types only get added when an
# operator-flagged library gap genuinely doesn't fit any existing
# category. See state/manual.md §"Library gaps" for the inbound flow.
CANONICAL_GAP_TYPES: tuple[str, ...] = (
    "trending",             # directional trend continuation
    "breakout",             # consolidation → directional move
    "mean_reversion",       # overextended → mean
    "earnings_window",      # within ±N days of earnings print
    "event_catalyst",       # discrete non-earnings news event (M&A, FDA, etc.)
    "gap_play",             # overnight gap continuation/reversal
    "intraday_range",       # opening-range / intraday breakout
    "pairs_arbitrage",      # relative-value cointegration
    "divergence",           # price-vs-indicator divergence
    "sector_rotation",      # cross-sector rotation / cohort momentum
    "volatility_regime",    # VIX-anchored sizing / IV-rank entries
)


def _all_active_or_testing_strategies():
    """Return strategy_id, frontmatter_dict for every non-archived strategy.

    Library lookup spans `status: active` AND `status: testing` —
    candidates in testing should still be selectable by the trader for
    triage if they happen to match a fresh gap.
    """
    out = []
    for sf in memory.list_strategies():
        status = (sf.frontmatter or {}).get("status", "")
        if status == "archived":
            continue
        out.append((sf.id, sf.frontmatter or {}))
    return out


def gap_types_for_strategy(strategy_id: str) -> list[str]:
    """Return the declared gap_types for a single strategy, or []."""
    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return []
    raw = (sf.frontmatter or {}).get("gap_types", []) or []
    if isinstance(raw, str):
        raw = [s.strip() for s in raw.split(",") if s.strip()]
    return [str(s) for s in raw]


def find_strategies_for_gap(gap_type: str) -> list[str]:
    """Return the IDs of every non-archived strategy that declares it
    handles `gap_type`. Empty list = no template fits = true library
    gap, escalate to research.
    """
    gap_type = (gap_type or "").strip()
    if not gap_type:
        return []
    out: list[str] = []
    for sid, fm in _all_active_or_testing_strategies():
        declared = fm.get("gap_types", []) or []
        if isinstance(declared, str):
            declared = [s.strip() for s in declared.split(",") if s.strip()]
        if gap_type in [str(s) for s in declared]:
            out.append(sid)
    return sorted(out)


def inverted_registry() -> dict[str, list[str]]:
    """Return {gap_type: [strategy_ids...]} across every non-archived
    strategy. Includes gap_types that no strategy claims (mapped to []) so
    the operator can see coverage holes in one place.
    """
    out: dict[str, list[str]] = {gt: [] for gt in CANONICAL_GAP_TYPES}
    for sid, fm in _all_active_or_testing_strategies():
        declared = fm.get("gap_types", []) or []
        if isinstance(declared, str):
            declared = [s.strip() for s in declared.split(",") if s.strip()]
        for gt in declared:
            gt = str(gt)
            out.setdefault(gt, []).append(sid)
    for gt in out:
        out[gt] = sorted(out[gt])
    return out


def validate_gap_types(values: Iterable[str]) -> tuple[list[str], list[str]]:
    """Split `values` into (canonical, unknown). Strategy authors who
    introduce a new gap_type get a clear warning when this is run; the
    rule of thumb is that any gap_type appearing in a strategy.md
    should also be in CANONICAL_GAP_TYPES.
    """
    canon: list[str] = []
    unknown: list[str] = []
    canonical_set = set(CANONICAL_GAP_TYPES)
    for v in values:
        s = str(v).strip()
        if not s:
            continue
        if s in canonical_set:
            canon.append(s)
        else:
            unknown.append(s)
    return canon, unknown
