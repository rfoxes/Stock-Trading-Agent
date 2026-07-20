"""Double Seven — executable counterpart to strategy.md.

Buy a 7-day closing low above the 200-day SMA; sell a 7-day closing high.
ATR hard stop and a journal-dated time stop backstop the two book rules.
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
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    entry_low_period = int(p.get("entry_low_period", 7))
    exit_high_period = int(p.get("exit_high_period", 7))
    trend_period = int(p.get("trend_ma_period", 200))
    trend_min_periods = int(p.get("trend_ma_min_periods", 60))
    atr_mult = float(p.get("stop_atr_multiplier", 2.0))
    atr_period = int(p.get("atr_period", 14))
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
        if bars.empty or len(bars) < max(exit_high_period, trend_min_periods) + 5:
            continue
        close = _f(bars["Close"].iloc[-1])
        rolling_high = _f(bars["Close"].rolling(exit_high_period, min_periods=exit_high_period).max().iloc[-1])
        sma_trend = _f(_trend_sma(bars).iloc[-1])
        avg_entry = _f(pos.get("avg_entry_price")) or 0.0
        atr_v = _f(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period).iloc[-1])

        exit_reason: str | None = None
        if close is not None and rolling_high is not None and close >= rolling_high:
            exit_reason = f"Primary exit: close {close:.2f} is a {exit_high_period}-day closing high."
        elif close is not None and sma_trend is not None and close < sma_trend:
            exit_reason = f"Trend break: close {close:.2f} < SMA{trend_period} {sma_trend:.2f}."
        elif (
            avg_entry > 0 and close is not None and atr_v is not None and atr_v > 0
            and close <= avg_entry - atr_mult * atr_v
        ):
            exit_reason = (
                f"Hard stop: close {close:.2f} <= entry {avg_entry:.2f} "
                f"- {atr_mult}x ATR({atr_period})={atr_v:.2f}."
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
        if bars.empty or len(bars) < max(entry_low_period, trend_min_periods) + 5:
            continue
        close = _f(bars["Close"].iloc[-1])
        rolling_low = _f(bars["Close"].rolling(entry_low_period, min_periods=entry_low_period).min().iloc[-1])
        sma_trend = _f(_trend_sma(bars).iloc[-1])
        atr_v = _f(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period).iloc[-1])
        avg_dollar_vol = _f((bars["Close"] * bars["Volume"]).tail(20).mean())
        if close is None or rolling_low is None or sma_trend is None or atr_v is None or avg_dollar_vol is None:
            continue
        if close <= sma_trend:
            continue
        if close > rolling_low:  # must BE the N-day closing low
            continue
        if avg_dollar_vol < min_dollar_vol:
            continue
        if atr_v <= 0:
            continue

        stop_pct = (atr_mult * atr_v) / close
        if stop_pct <= 0:
            continue
        shares = share_count(
            equity=equity, risk_pct=risk_pct,
            entry_price=close, stop_distance_pct=stop_pct,
            max_position_pct=float(p.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            continue
        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Entry: close {close:.2f} is a {entry_low_period}-day closing low "
                f"above SMA{trend_period} {sma_trend:.2f}. Exit on {exit_high_period}-day "
                f"closing high; stop {atr_mult}x ATR (-{stop_pct*100:.1f}%); "
                f"{max_hold_days}d time stop."
            ),
            stop_loss_pct=stop_pct,
        ))
        open_count += 1

    return intents
