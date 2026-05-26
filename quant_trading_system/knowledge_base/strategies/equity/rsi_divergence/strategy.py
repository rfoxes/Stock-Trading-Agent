"""RSI Divergence — executable counterpart to strategy.md.

Detects bullish divergence: price makes a lower low over the last `lookback`
bars while RSI makes a higher low. Enter long the next day after confirmation
(RSI > 30 close).

Exit: RSI > 70 (overbought) or price < entry * (1 - stop_pct).
"""

from __future__ import annotations

import numpy as np

from quant_trading_system._strategy_helpers import (
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    rsi_period = int(p.get("rsi_period", 14))
    lookback = int(p.get("divergence_lookback", 30))
    stop_pct = float(p.get("stop_loss_pct", 4.0)) / 100.0
    risk_pct = float(p.get("risk_pct", 0.01))
    rsi_overbought = float(p.get("rsi_exit_overbought", 70))

    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    # Exits
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        if not sym:
            continue
        bars = ctx.get_bars(sym, "1Day", 60)
        if bars.empty or len(bars) < rsi_period + 5:
            continue
        rsi = ti.compute_rsi(bars["Close"], rsi_period)
        rsi_v = float(rsi.iloc[-1] or 0)
        close = float(bars["Close"].iloc[-1])
        avg_entry = float(pos.get("avg_entry_price", 0) or 0)
        qty = position_qty(ctx.positions, sym)
        if qty > 0 and rsi_v >= rsi_overbought:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: RSI {rsi_v:.1f} >= overbought {rsi_overbought}.",
            ))
            continue
        if qty > 0 and avg_entry > 0 and close < avg_entry * (1 - stop_pct):
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: hard stop, close {close:.2f} < {avg_entry*(1-stop_pct):.2f}.",
            ))

    # Entries — bullish divergence
    for sym in ctx.watchlist:
        if has_position(ctx.positions, sym):
            continue
        bars = ctx.get_bars(sym, "1Day", lookback + 60)
        if bars.empty or len(bars) < lookback + rsi_period + 5:
            continue
        rsi = ti.compute_rsi(bars["Close"], rsi_period).dropna()
        closes = bars["Close"].iloc[-lookback:]
        rsi_window = rsi.iloc[-lookback:]
        if len(closes) < lookback or len(rsi_window) < lookback:
            continue
        # Split window in half; compare lows
        half = lookback // 2
        old_low_close = float(closes.iloc[:half].min())
        new_low_close = float(closes.iloc[half:].min())
        old_low_rsi = float(rsi_window.iloc[:half].min())
        new_low_rsi = float(rsi_window.iloc[half:].min())
        last_rsi = float(rsi_window.iloc[-1])
        last_close = float(closes.iloc[-1])

        is_divergence = (new_low_close < old_low_close) and (new_low_rsi > old_low_rsi)
        is_confirmed = last_rsi > 30 and last_close > float(closes.iloc[-2])
        if not (is_divergence and is_confirmed):
            continue

        shares = share_count(
            equity=equity, risk_pct=risk_pct,
            entry_price=last_close, stop_distance_pct=stop_pct,
            max_position_pct=float(ctx.params.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            continue
        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Entry: bullish RSI divergence over {lookback}d. "
                f"Price low {new_low_close:.2f} < prior {old_low_close:.2f}; "
                f"RSI low {new_low_rsi:.1f} > prior {old_low_rsi:.1f}. "
                f"Confirmed by RSI {last_rsi:.1f} > 30 and price recovering. "
                f"Stop {stop_pct*100:.1f}% below entry."
            ),
            stop_loss_pct=stop_pct,
        ))

    return intents
