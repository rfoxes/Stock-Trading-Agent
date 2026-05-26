"""Gap and Go — SKELETON.

Gap-and-go trades pre-market gaps (>3%) on news catalysts at the open. It
needs:
  - Pre-market quote data (not just regular-session bars).
  - A news/catalyst feed to filter gaps with reason from gaps without.
  - Intraday execution.

A post-close run can't act on this. Skipped.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: gap_and_go is intraday + needs pre-market + news feed")
    return []
