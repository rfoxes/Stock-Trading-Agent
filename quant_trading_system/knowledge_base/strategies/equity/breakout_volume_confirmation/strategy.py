"""Volume-Confirmed Breakout — executable counterpart to strategy.md.

Entry: close > N-day high (excluding today), volume > vol_mult * avg, ATR-based
position sizing.

Exit: close < trailing N-bar low.
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
    lookback = int(p.get("breakout_lookback_days", 20))
    vol_mult = float(p.get("volume_multiplier", 1.5))
    vol_window = int(p.get("volume_lookback", 20))
    atr_period = int(p.get("atr_period", 14))
    atr_stop_mult = float(p.get("atr_stop_multiplier", 2.0))
    trail_low_lookback = int(p.get("trailing_low_lookback", 10))
    risk_pct = float(p.get("risk_pct", 0.015))

    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    # Exits: close below trailing low
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        if not sym:
            continue
        bars = ctx.get_bars(sym, "1Day", max(50, trail_low_lookback + 5))
        if bars.empty or len(bars) < trail_low_lookback + 2:
            continue
        trailing_low = float(bars["Low"].iloc[-(trail_low_lookback + 1):-1].min())
        close = float(bars["Close"].iloc[-1])
        qty = position_qty(ctx.positions, sym)
        if qty > 0 and close < trailing_low:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: close {close:.2f} < trailing {trail_low_lookback}d low {trailing_low:.2f}.",
            ))

    # Entries
    for sym in ctx.watchlist:
        if has_position(ctx.positions, sym):
            continue
        bars = ctx.get_bars(sym, "1Day", max(60, lookback + 5))
        if bars.empty or len(bars) < lookback + 5:
            continue
        prior_high = float(bars["High"].iloc[-(lookback + 1):-1].max())
        last_close = float(bars["Close"].iloc[-1])
        last_vol = float(bars["Volume"].iloc[-1] or 0)
        avg_vol = average_volume(bars, vol_window)
        atr = ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period)
        last_atr = float(atr.iloc[-1] or 0)
        if last_atr <= 0 or avg_vol <= 0:
            continue
        if last_close <= prior_high:
            continue
        if last_vol < vol_mult * avg_vol:
            continue
        stop_distance = atr_stop_mult * last_atr
        stop_pct = stop_distance / last_close
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
                f"Entry: close {last_close:.2f} > prior {lookback}d high {prior_high:.2f}, "
                f"vol {last_vol:.0f} > {vol_mult}x avg {avg_vol:.0f}. "
                f"ATR-based stop {atr_stop_mult}x ATR ({last_atr:.2f}) = "
                f"-{stop_pct*100:.1f}%."
            ),
            stop_loss_pct=stop_pct,
        ))

    return intents
