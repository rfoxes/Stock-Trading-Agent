"""Bollinger Band Mean Reversion — executable counterpart to strategy.md.

Each run:
  1. For every watchlist symbol we don't already hold, fetch daily bars.
  2. Enter long if: close below lower BB, RSI < oversold, volume > vol_mult * avg.
  3. For positions we hold: exit at middle BB touch, RSI cross above exit, or
     a hard stop at -stop_loss_pct from entry. Also a time-stop at max_hold_days.
"""

from __future__ import annotations

from quant_trading_system._strategy_helpers import (
    average_volume,
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    bb_period = int(p.get("bb_period", 20))
    bb_std = float(p.get("bb_std_dev", 2.0))
    rsi_period = int(p.get("rsi_period", 14))
    rsi_oversold = float(p.get("rsi_oversold", 30))
    rsi_exit = float(p.get("rsi_exit", 50))
    vol_mult = float(p.get("volume_multiplier", 1.5))
    vol_window = int(p.get("volume_lookback", 20))
    stop_loss_pct = float(p.get("stop_loss_pct", 2.0)) / 100.0

    risk_pct_per_trade = 0.01
    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    # Exits
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        if not sym:
            continue
        bars = ctx.get_bars(sym, "1Day", 60)
        if bars.empty or len(bars) < bb_period + 5:
            continue
        bb = ti.compute_bollinger_bands(bars["Close"], bb_period, bb_std)
        rsi = ti.compute_rsi(bars["Close"], rsi_period)
        close = float(bars["Close"].iloc[-1])
        middle = float(bb["Middle"].iloc[-1])
        rsi_v = float(rsi.iloc[-1] or 0)
        qty = position_qty(ctx.positions, sym)
        avg_entry = float(pos.get("avg_entry_price", 0) or 0)
        # Primary target: touch middle band
        if close >= middle and qty > 0:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: target hit, close {close:.2f} >= mid-BB {middle:.2f}.",
            ))
            continue
        # Momentum exit
        if rsi_v >= rsi_exit and qty > 0:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: RSI {rsi_v:.1f} >= exit {rsi_exit} (mean reversion underway).",
            ))
            continue
        # Hard stop
        if avg_entry > 0 and close < avg_entry * (1 - stop_loss_pct) and qty > 0:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: hard stop, close {close:.2f} < {avg_entry*(1-stop_loss_pct):.2f}.",
            ))

    # Entries
    for sym in ctx.watchlist:
        if has_position(ctx.positions, sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 60)
        if bars.empty or len(bars) < bb_period + 5:
            continue
        bb = ti.compute_bollinger_bands(bars["Close"], bb_period, bb_std)
        rsi = ti.compute_rsi(bars["Close"], rsi_period)
        last_close = float(bars["Close"].iloc[-1])
        last_lower = float(bb["Lower"].iloc[-1] or 0)
        last_rsi = float(rsi.iloc[-1] or 0)
        last_vol = float(bars["Volume"].iloc[-1] or 0)
        avg_vol = average_volume(bars, vol_window)
        if last_lower <= 0 or last_rsi <= 0 or avg_vol <= 0:
            continue
        if last_close >= last_lower:
            continue
        if last_rsi >= rsi_oversold:
            continue
        if last_vol < vol_mult * avg_vol:
            continue
        shares = share_count(
            equity=equity,
            risk_pct=risk_pct_per_trade,
            entry_price=last_close,
            stop_distance_pct=stop_loss_pct,
            max_position_pct=float(ctx.params.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            continue
        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Entry: close {last_close:.2f} < lower-BB {last_lower:.2f}, "
                f"RSI {last_rsi:.1f} < {rsi_oversold}, "
                f"vol {last_vol:.0f} > {vol_mult}x avg {avg_vol:.0f}. "
                f"Hard stop {stop_loss_pct*100:.1f}% below entry, "
                f"target = mid-BB ({float(bb['Middle'].iloc[-1]):.2f})."
            ),
            stop_loss_pct=stop_loss_pct,
        ))

    return intents
