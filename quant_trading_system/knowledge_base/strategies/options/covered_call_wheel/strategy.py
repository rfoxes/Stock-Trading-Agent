"""Covered Call / Wheel — SKELETON (no options data infrastructure).

The Wheel requires:
  - Cash-secured puts on the way in, covered calls on the way out.
  - Per-expiration delta-based strike selection.
  - IV rank to gate entries.

Skipped — no options chain feed.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: covered_call_wheel needs options chain + IV rank")
    return []
