"""Iron Condor (High IV) — SKELETON (no options data infrastructure).

Four-leg market-neutral structure for high-IV, range-bound regimes. Needs
options chain + IV rank + delta-based strike selection. Skipped.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    regime = (ctx.regime or {}).get("regime", "unknown")
    if regime in ("sideways", "range_bound", "volatile"):
        ctx.log.info(
            "setup_would_fire_but_no_options_data regime=%s; need options chain + IV rank",
            regime,
        )
    else:
        ctx.log.info("no_setup regime=%s (need sideways or volatile)", regime)
    return []
