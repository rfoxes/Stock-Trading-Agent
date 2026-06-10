"""Strategy template registry.

Lets the trader (and downstream tools) answer two algorithmic questions
without judgment:

1. "Given an unclaimed symbol + a gap_type (from the news brief), which
   library strategies could plausibly respond to it?"  →  registry
   lookup.
2. "Given a candidate strategy + a symbol, does it actually beat
   baseline on that symbol's history?"  →  cli triage-symbol +
   cli instantiate-template.

The taxonomy of gap_types is small and stable — each strategy declares
which of these it handles in its frontmatter `gap_types: [...]` field.
The news brief and trader use the same taxonomy when tagging events.

This module deliberately contains no judgment, scoring, or ranking.
It indexes. The CLI commands do the algorithmic work using the
existing backtester + addition battery.
"""

from quant_trading_system.templates.registry import (
    CANONICAL_GAP_TYPES,
    find_strategies_for_gap,
    gap_types_for_strategy,
    inverted_registry,
)

__all__ = [
    "CANONICAL_GAP_TYPES",
    "find_strategies_for_gap",
    "gap_types_for_strategy",
    "inverted_registry",
]
