"""Pairs Trading (Cointegration) — SKELETON.

Pairs trading requires:
  - A vetted list of cointegrated pairs (would normally come from an offline
    research process running Engle-Granger or Johansen tests).
  - Per-pair state: the hedge ratio, the rolling spread mean and stdev,
    z-score thresholds, and whether the pair currently has open positions.
  - Two-leg order construction (long one symbol, short the other) and
    careful unwinding.

None of that exists yet. This script returns no orders and logs the missing
infrastructure. The agent can drive implementation by:
  1. Picking 1-2 pairs (e.g. KO/PEP, MA/V, XOM/CVX).
  2. Computing rolling hedge ratios.
  3. Re-implementing evaluate() to act on z-score thresholds.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: pairs_trading_cointegration needs pair list + state")
    return []
