"""Bull Put Credit Spread — SKELETON (no options data infrastructure).

Same data gap as the other options strategies — no options chain feed,
no per-expiration IV. Setup check on the underlying regime only.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    regime = (ctx.regime or {}).get("regime", "unknown")
    if regime in ("bull", "neutral", "sideways"):
        ctx.log.info(
            "setup_would_fire_but_no_options_data regime=%s; need options chain feed",
            regime,
        )
    else:
        ctx.log.info("no_setup regime=%s (need bullish/neutral)", regime)
    return []
