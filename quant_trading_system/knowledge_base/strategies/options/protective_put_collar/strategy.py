"""Protective Put / Collar — SKELETON (no options data infrastructure).

Hedges an existing equity position by buying a put (and optionally selling
a call to finance it). Requires:
  - The harness to currently hold the underlying stock.
  - Options chain to select strike and expiration.
  - Delta-based strike selection.

Skipped — no options chain.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: protective_put_collar needs options chain + held equity positions")
    return []
