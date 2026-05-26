"""Calendar Spread — SKELETON (no options data infrastructure).

Calendar spreads exploit term-structure skew (front-month IV > back-month IV).
Needs an options chain + per-expiration IV. Not wired up. Skipped.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: calendar_spread needs options chain + IV term structure")
    return []
