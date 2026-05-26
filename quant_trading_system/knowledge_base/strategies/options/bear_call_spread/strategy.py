"""Bear Call Credit Spread — SKELETON (no options data infrastructure).

Implementing this for real requires:
  - An options chain feed (Alpaca options API or polygon.io).
  - IV rank / implied volatility data per expiration.
  - Multi-leg order construction (sell short call, buy long call wing).
  - Delta-based strike selection.

None of that is wired up in the harness today. This script confirms the
underlying-level setup conditions (bearish or neutral regime, optionally
high IV proxy via realized vol) and returns no orders with a log line that
documents what would have happened.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    regime = (ctx.regime or {}).get("regime", "unknown")
    if regime in ("bear", "neutral", "sideways"):
        ctx.log.info(
            "setup_would_fire_but_no_options_data regime=%s; need options chain feed",
            regime,
        )
    else:
        ctx.log.info("no_setup regime=%s (need bearish/neutral)", regime)
    return []
