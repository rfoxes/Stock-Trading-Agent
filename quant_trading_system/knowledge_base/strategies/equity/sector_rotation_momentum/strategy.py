"""Sector Rotation Momentum — SKELETON.

This strategy ranks sector ETFs by 3-6 month relative strength and rotates
into the leaders. To implement properly we'd need:
  - A sector ETF universe (XLK, XLF, XLE, XLV, XLI, XLP, XLU, XLY, XLB, XLRE, XLC).
  - Each ETF's daily bars over the lookback window.
  - Rebalance logic that closes losers and buys winners.

The watchlist as currently configured is single-name stocks (SPY, QQQ, AAPL,
etc.), not sector ETFs. Rather than fake a setup, this script returns no
orders and logs why. The agent should either:
  (a) Extend the watchlist to include sector ETFs and re-implement
      this evaluate() function properly, or
  (b) Pick a different active strategy that fits the current watchlist.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    ctx.log.info(
        "skeleton_no_action: sector_rotation_momentum needs sector-ETF watchlist; "
        "current watchlist=%s",
        ",".join(ctx.watchlist),
    )
    return []
