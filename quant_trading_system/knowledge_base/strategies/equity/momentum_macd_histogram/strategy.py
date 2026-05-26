"""MACD Histogram Momentum — executable counterpart to strategy.md.

Entry: MACD histogram crosses above zero, MACD line is above signal line,
and the histogram is rising for at least the last 2 bars. Filter by trend
(price above SMA(50)).

Exit: histogram crosses back below zero, or price < SMA(20).
"""

from __future__ import annotations

from quant_trading_system._strategy_helpers import (
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    fast = int(p.get("fast_ema", 12))
    slow = int(p.get("slow_ema", 26))
    signal = int(p.get("signal_period", 9))
    risk_pct = float(p.get("risk_pct", 0.012))
    stop_pct = float(p.get("stop_loss_pct", 3.0)) / 100.0

    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    # Exits
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        if not sym:
            continue
        bars = ctx.get_bars(sym, "1Day", 120)
        if bars.empty or len(bars) < slow + signal + 5:
            continue
        m = ti.compute_macd(bars["Close"], fast, slow, signal)
        sma20 = ti.compute_sma(bars["Close"], 20)
        close = float(bars["Close"].iloc[-1])
        hist = float(m["Histogram"].iloc[-1] or 0)
        qty = position_qty(ctx.positions, sym)
        if qty > 0 and hist < 0:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: MACD hist {hist:.4f} flipped negative.",
            ))
            continue
        if qty > 0 and close < float(sma20.iloc[-1] or 0):
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: close {close:.2f} < SMA20 {float(sma20.iloc[-1]):.2f}.",
            ))

    # Entries
    for sym in ctx.watchlist:
        if has_position(ctx.positions, sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 200)
        if bars.empty or len(bars) < slow + signal + 5:
            continue
        m = ti.compute_macd(bars["Close"], fast, slow, signal)
        sma50 = ti.compute_sma(bars["Close"], 50)
        hist = m["Histogram"].dropna()
        if len(hist) < 4:
            continue
        h2, h1, h0 = float(hist.iloc[-3]), float(hist.iloc[-2]), float(hist.iloc[-1])
        macd_v, sig_v = float(m["MACD"].iloc[-1] or 0), float(m["Signal"].iloc[-1] or 0)
        close = float(bars["Close"].iloc[-1])
        sma50_v = float(sma50.iloc[-1] or 0)

        # Conditions: histogram crosses above zero on last bar, rising for 2+ bars,
        # MACD > Signal, price > SMA(50).
        if not (h2 <= 0 < h0):
            continue
        if not (h0 > h1):
            continue
        if not (macd_v > sig_v):
            continue
        if close <= sma50_v:
            continue

        shares = share_count(
            equity=equity, risk_pct=risk_pct,
            entry_price=close, stop_distance_pct=stop_pct,
            max_position_pct=float(ctx.params.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            continue
        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Entry: MACD hist crossed above 0 ({h2:.4f} -> {h0:.4f}, rising), "
                f"MACD {macd_v:.3f} > signal {sig_v:.3f}, "
                f"close {close:.2f} > SMA50 {sma50_v:.2f}. "
                f"Stop {stop_pct*100:.1f}% below entry."
            ),
            stop_loss_pct=stop_pct,
        ))

    return intents
