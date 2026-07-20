"""RSI(2) Pullback in Uptrend — executable counterpart to strategy.md.

Each run:
  1. Exits first: strength (close > SMA5), momentum (RSI2 > exit), trend
     break (close < SMA200), hard stop vs entry, journal-dated time stop.
  2. Entries: close > SMA200, RSI(2) < entry threshold, liquidity floor,
     no negative news markers. Market buy at next open with a stop bracket.

The 200-day SMA uses min_periods=trend_ma_min_periods so the filter is
defined early in a walk-forward window (see strategy.md).
"""

from __future__ import annotations

import math

from quant_trading_system._strategy_helpers import (
    has_position,
    position_age_days,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


def _f(x) -> float | None:
    """float() with NaN/None mapped to None so comparisons stay explicit."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    rsi_period = int(p.get("rsi_period", 2))
    rsi_entry_max = float(p.get("rsi_entry_max", 10.0))
    rsi_exit_min = float(p.get("rsi_exit_min", 70.0))
    exit_ma_period = int(p.get("exit_ma_period", 5))
    trend_period = int(p.get("trend_ma_period", 200))
    trend_min_periods = int(p.get("trend_ma_min_periods", 60))
    stop_loss_pct = float(p.get("stop_loss_pct", 4.0)) / 100.0
    max_hold_days = int(p.get("max_hold_days", 10))
    min_dollar_vol = float(p.get("min_avg_dollar_volume", 5_000_000))
    risk_pct = float(p.get("risk_pct_per_trade", 0.01))
    max_concurrent = int(p.get("max_concurrent_positions", 4))

    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    def _trend_sma(bars):
        return bars["Close"].rolling(trend_period, min_periods=trend_min_periods).mean()

    # ---- Exits first ----
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        qty = position_qty(ctx.positions, sym)
        if not sym or qty <= 0:
            continue
        bars = ctx.get_bars(sym, "1Day", 320)
        if bars.empty or len(bars) < trend_min_periods + 5:
            continue
        close = _f(bars["Close"].iloc[-1])
        sma_exit = _f(bars["Close"].rolling(exit_ma_period, min_periods=exit_ma_period).mean().iloc[-1])
        sma_trend = _f(_trend_sma(bars).iloc[-1])
        rsi_v = _f(ti.compute_rsi(bars["Close"], rsi_period).iloc[-1])
        avg_entry = _f(pos.get("avg_entry_price")) or 0.0

        exit_reason: str | None = None
        if close is not None and sma_exit is not None and close > sma_exit:
            exit_reason = f"Strength exit: close {close:.2f} > SMA{exit_ma_period} {sma_exit:.2f}."
        elif rsi_v is not None and rsi_v >= rsi_exit_min:
            exit_reason = f"Momentum exit: RSI({rsi_period}) {rsi_v:.1f} >= {rsi_exit_min}."
        elif close is not None and sma_trend is not None and close < sma_trend:
            exit_reason = f"Trend break: close {close:.2f} < SMA{trend_period} {sma_trend:.2f}."
        elif avg_entry > 0 and close is not None and close <= avg_entry * (1 - stop_loss_pct):
            exit_reason = (
                f"Hard stop: close {close:.2f} <= entry {avg_entry:.2f} "
                f"- {stop_loss_pct*100:.1f}%."
            )
        else:
            age = position_age_days(ctx.strategy_id, sym, ctx.date)
            if age is not None and age >= max_hold_days:
                exit_reason = f"Time stop: held {age}d >= max_hold_days {max_hold_days}."

        if exit_reason is not None:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=exit_reason,
            ))

    # ---- Entries ----
    open_count = sum(1 for pos in ctx.positions if float(pos.get("qty", 0) or 0) > 0)
    for sym in ctx.watchlist:
        if open_count >= max_concurrent:
            break
        if has_position(ctx.positions, sym):
            continue
        if ctx.news_brief.has_negative_signal(sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 320)
        if bars.empty or len(bars) < trend_min_periods + 5:
            continue
        close = _f(bars["Close"].iloc[-1])
        sma_trend = _f(_trend_sma(bars).iloc[-1])
        rsi_v = _f(ti.compute_rsi(bars["Close"], rsi_period).iloc[-1])
        avg_dollar_vol = _f((bars["Close"] * bars["Volume"]).tail(20).mean())
        if close is None or sma_trend is None or rsi_v is None or avg_dollar_vol is None:
            continue
        if close <= sma_trend:
            continue
        if rsi_v >= rsi_entry_max:
            continue
        if avg_dollar_vol < min_dollar_vol:
            continue

        shares = share_count(
            equity=equity, risk_pct=risk_pct,
            entry_price=close, stop_distance_pct=stop_loss_pct,
            max_position_pct=float(p.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            continue
        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Entry: RSI({rsi_period}) {rsi_v:.1f} < {rsi_entry_max} with close "
                f"{close:.2f} > SMA{trend_period} {sma_trend:.2f} (uptrend pullback). "
                f"Exit at close > SMA{exit_ma_period} or RSI > {rsi_exit_min}; "
                f"hard stop -{stop_loss_pct*100:.1f}%; {max_hold_days}d time stop."
            ),
            stop_loss_pct=stop_loss_pct,
        ))
        open_count += 1

    return intents
