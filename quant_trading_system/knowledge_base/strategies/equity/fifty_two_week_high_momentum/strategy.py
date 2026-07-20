"""52-Week High Proximity Momentum — executable counterpart to strategy.md.

Enter when the close first crosses into the proximity band of the prior
252-bar closing high on above-average volume; exit on close < SMA20, a
2.5x ATR stop, or the 30-day time stop.
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
    high_lookback = int(p.get("high_lookback", 252))
    high_min_periods = int(p.get("high_min_periods", 126))
    proximity = float(p.get("proximity_entry_pct", 2.0)) / 100.0
    vol_mult = float(p.get("volume_mult_min", 1.5))
    vol_window = int(p.get("volume_lookback", 20))
    exit_ma_period = int(p.get("exit_ma_period", 20))
    stop_mult = float(p.get("stop_atr_multiplier", 2.5))
    atr_period = int(p.get("atr_period", 14))
    max_hold_days = int(p.get("max_hold_days", 30))
    min_dollar_vol = float(p.get("min_avg_dollar_volume", 5_000_000))
    risk_pct = float(p.get("risk_pct_per_trade", 0.01))
    max_concurrent = int(p.get("max_concurrent_positions", 4))

    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    def _prior_high(bars):
        # Rolling max of closes EXCLUDING the current bar (shift(1)).
        return bars["Close"].shift(1).rolling(high_lookback, min_periods=high_min_periods).max()

    # ---- Exits first ----
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        qty = position_qty(ctx.positions, sym)
        if not sym or qty <= 0:
            continue
        bars = ctx.get_bars(sym, "1Day", 400)
        if bars.empty or len(bars) < exit_ma_period + 5:
            continue
        close = _f(bars["Close"].iloc[-1])
        sma_exit = _f(bars["Close"].rolling(exit_ma_period, min_periods=exit_ma_period).mean().iloc[-1])
        atr_v = _f(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period).iloc[-1])
        avg_entry = _f(pos.get("avg_entry_price")) or 0.0

        exit_reason: str | None = None
        if close is not None and sma_exit is not None and close < sma_exit:
            exit_reason = f"Trend-loss exit: close {close:.2f} < SMA{exit_ma_period} {sma_exit:.2f}."
        elif (
            avg_entry > 0 and close is not None and atr_v is not None and atr_v > 0
            and close <= avg_entry - stop_mult * atr_v
        ):
            exit_reason = (
                f"Hard stop: close {close:.2f} <= entry {avg_entry:.2f} "
                f"- {stop_mult}x ATR({atr_period})={atr_v:.2f}."
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

    # ---- Entries: crossing into the proximity band ----
    open_count = sum(1 for pos in ctx.positions if float(pos.get("qty", 0) or 0) > 0)
    for sym in ctx.watchlist:
        if open_count >= max_concurrent:
            break
        if has_position(ctx.positions, sym):
            continue
        if ctx.news_brief.has_negative_signal(sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 400)
        if bars.empty or len(bars) < high_min_periods + 5:
            continue
        prior_high = _prior_high(bars)
        close = _f(bars["Close"].iloc[-1])
        prev_close = _f(bars["Close"].iloc[-2])
        thresh = _f(prior_high.iloc[-1])
        prev_thresh = _f(prior_high.iloc[-2])
        atr_v = _f(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period).iloc[-1])
        last_vol = _f(bars["Volume"].iloc[-1])
        avg_vol = _f(bars["Volume"].shift(1).rolling(vol_window, min_periods=vol_window).mean().iloc[-1])
        avg_dollar_vol = _f((bars["Close"] * bars["Volume"]).tail(20).mean())
        if None in (close, prev_close, thresh, prev_thresh, atr_v, last_vol, avg_vol, avg_dollar_vol):
            continue
        if thresh <= 0 or prev_thresh <= 0 or atr_v <= 0 or avg_vol <= 0:
            continue
        band = thresh * (1 - proximity)
        prev_band = prev_thresh * (1 - proximity)
        if close < band:
            continue
        if prev_close >= prev_band:  # already inside the band yesterday — not a crossing
            continue
        if last_vol < vol_mult * avg_vol:
            continue
        if avg_dollar_vol < min_dollar_vol:
            continue

        stop_pct = (stop_mult * atr_v) / close
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
                f"Entry: close {close:.2f} crossed into {proximity*100:.0f}% band of "
                f"prior 52wk high {thresh:.2f} on volume {last_vol:.0f} >= {vol_mult}x "
                f"avg {avg_vol:.0f} (anchoring breakout). Exit: close < SMA{exit_ma_period}, "
                f"stop {stop_mult}x ATR (-{stop_pct*100:.1f}%), {max_hold_days}d time stop."
            ),
            stop_loss_pct=stop_pct,
        ))
        open_count += 1

    return intents
