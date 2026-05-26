"""Opening Range Breakout — SKELETON.

ORB is an intraday strategy: define the first 5/15/30 min range, then trade
breakouts of that range during the rest of the session. It does not fit a
once-per-day post-close cadence; you'd need to wake the harness intraday.

For now this script returns no orders. If you want ORB:
  - Move the trigger to a few minutes after the opening range completes
    (e.g. 9:45 ET), or
  - Submit a pair of stop orders (long at range high + 1 tick, short at
    range low - 1 tick) at the start of the session via a separate
    pre-market trigger.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: opening_range_breakout is intraday; doesn't fit post-close run")
    return []
