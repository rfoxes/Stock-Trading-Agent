"""EMA Crossover Trend Following — executable counterpart to strategy.md.

Each scheduled run, this script:
  1. For every symbol on the watchlist we don't already hold, fetch daily bars.
  2. Compute EMA(fast), EMA(slow), ADX(14), SMA(200).
  3. Submit a long if: EMA fast just crossed above EMA slow, ADX > entry_threshold,
     price > SMA(200). Otherwise: nothing.
  4. For positions we already hold: check the death-cross / ADX-fade exit
     conditions and submit a sell if either triggers.

Run cadence is post-close, so all entries are queued for the next session.
"""

from __future__ import annotations

from quant_trading_system._strategy_helpers import (
    crossed_above,
    crossed_below,
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    fast_period = int(p.get("fast_ema_period", 12))
    slow_period = int(p.get("slow_ema_period", 26))
    adx_period = int(p.get("adx_period", 14))
    adx_entry = float(p.get("adx_entry_threshold", 25))
    adx_exit = float(p.get("adx_exit_threshold", 20))
    atr_period = int(p.get("atr_period", 14))
    atr_stop_mult = float(p.get("atr_stop_multiplier", 2.5))

    risk_pct_per_trade = 0.015  # 1.5% of equity per trade (per strategy.md)
    equity = float(ctx.account.get("equity", 0.0))

    intents: list[OrderIntent] = []

    # --- Exit pass: check existing positions for death-cross / ADX fade ---
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        if not sym:
            continue
        bars = ctx.get_bars(sym, "1Day", 260)
        if bars.empty or len(bars) < slow_period + 5:
            continue
        ema_fast = ti.compute_ema(bars["Close"], fast_period)
        ema_slow = ti.compute_ema(bars["Close"], slow_period)
        adx = ti.compute_adx(bars["High"], bars["Low"], bars["Close"], adx_period)
        if crossed_below(ema_fast, ema_slow):
            qty = position_qty(ctx.positions, sym)
            if qty > 0:
                intents.append(OrderIntent(
                    symbol=sym, side="sell", qty=qty, order_type="market",
                    reasoning=f"Exit: EMA{fast_period} crossed below EMA{slow_period} (death cross).",
                ))
                continue
        if not adx.empty and not adx.iloc[-1] != adx.iloc[-1]:  # not NaN
            if float(adx.iloc[-1]) < adx_exit:
                qty = position_qty(ctx.positions, sym)
                if qty > 0:
                    intents.append(OrderIntent(
                        symbol=sym, side="sell", qty=qty, order_type="market",
                        reasoning=f"Exit: ADX({adx_period})={float(adx.iloc[-1]):.1f} < exit threshold {adx_exit}.",
                    ))

    # --- Entry pass: only consider symbols we don't already hold ---
    for sym in ctx.watchlist:
        if has_position(ctx.positions, sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 260)
        if bars.empty or len(bars) < 210:
            ctx.log.info("skip %s: insufficient bars (%d)", sym, len(bars))
            continue

        ema_fast = ti.compute_ema(bars["Close"], fast_period)
        ema_slow = ti.compute_ema(bars["Close"], slow_period)
        adx = ti.compute_adx(bars["High"], bars["Low"], bars["Close"], adx_period)
        sma_200 = ti.compute_sma(bars["Close"], 200)
        atr = ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period)

        if not crossed_above(ema_fast, ema_slow, lookback=2):
            continue
        if adx.empty or float(adx.iloc[-1] or 0) < adx_entry:
            continue
        last_close = float(bars["Close"].iloc[-1])
        if last_close <= float(sma_200.iloc[-1] or 0):
            continue  # regime filter: only trade with the secular trend
        last_atr = float(atr.iloc[-1] or 0)
        if last_atr <= 0:
            continue
        stop_distance = atr_stop_mult * last_atr
        stop_distance_pct = stop_distance / last_close
        shares = share_count(
            equity=equity,
            risk_pct=risk_pct_per_trade,
            entry_price=last_close,
            stop_distance_pct=stop_distance_pct,
            max_position_pct=float(ctx.params.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            ctx.log.info("skip %s: share_count=0 (equity=%.0f, atr_stop=%.2f)",
                         sym, equity, stop_distance)
            continue
        stop_price = round(last_close - stop_distance, 2)
        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Entry: EMA{fast_period} crossed above EMA{slow_period}, "
                f"ADX={float(adx.iloc[-1]):.1f} > {adx_entry}, "
                f"price {last_close:.2f} > SMA200 {float(sma_200.iloc[-1]):.2f}. "
                f"Stop @ {stop_price} ({atr_stop_mult}x ATR={last_atr:.2f}). "
                f"Risking {risk_pct_per_trade*100:.1f}% of equity."
            ),
            stop_loss_pct=stop_distance_pct,
        ))

    return intents
