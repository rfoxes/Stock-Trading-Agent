"""Long Straddle (Pre-Earnings) — SKELETON (no options or earnings data).

Buys ATM put + ATM call right before an expected vol expansion event
(earnings). Needs:
  - An earnings calendar (when does each watchlist symbol report?).
  - Options chain + per-expiration IV.
  - Historical earnings-move stats to gate entries.

None of that is wired up. Skipped.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info("skeleton_no_action: long_straddle_earnings needs earnings calendar + options chain")
    return []
