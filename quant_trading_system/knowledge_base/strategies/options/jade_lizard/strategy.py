"""Jade Lizard — SKELETON (no options data infrastructure).

Sells an OTM put + an OTM call spread above the stock; carries no upside
risk if call spread credit > put credit width. Needs options chain. Skipped.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: jade_lizard needs options chain + IV rank")
    return []
