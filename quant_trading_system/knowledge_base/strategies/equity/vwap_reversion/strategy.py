"""VWAP Reversion — SKELETON.

VWAP reversion trades intraday extensions away from VWAP and back. It needs
intraday bars (1Min/5Min) plus session-anchored VWAP, neither of which is
sensible to evaluate post-close. Skipped.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: vwap_reversion is intraday; doesn't fit post-close run")
    return []
