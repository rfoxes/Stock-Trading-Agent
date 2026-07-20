"""Bollinger Band Mean Reversion, IBS-filtered v2 — update candidate.

Byte-for-byte the incumbent `equity_mean_reversion_bollinger` logic plus:
  - entry additionally requires IBS = (close-low)/(high-low) < ibs_entry_max
  - exits additionally fire when IBS > ibs_exit_min (strength-close accel)

Keep any future incumbent rule changes mirrored here (or re-derive the v2)
so evaluate-update keeps isolating the IBS filter's effect.
"""

from __future__ import annotations

import math

from quant_trading_system._strategy_helpers import (
    average_volume,
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


def _ibs(bars) -> float | None:
    """Internal Bar Strength of the last bar; 0.5 (neutral) on a zero-range bar."""
    try:
        high = float(bars["High"].iloc[-1])
        low = float(bars["Low"].iloc[-1])
        close = float(bars["Close"].iloc[-1])
    except (TypeError, ValueError, KeyError, IndexError):
        return None
    if any(math.isnan(v) for v in (high, low, close)):
        return None
    rng = high - low
    if rng <= 0:
        return 0.5
    return max(0.0, min(1.0, (close - low) / rng))


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
    ibs_entry_max = float(p.get("ibs_entry_max", 0.2))
    ibs_exit_min = float(p.get("ibs_exit_min", 0.8))

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
        ibs_v = _ibs(bars)
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
        # v2: IBS strength-close accelerator
        if ibs_v is not None and ibs_v > ibs_exit_min and qty > 0:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=f"Exit: IBS {ibs_v:.2f} > {ibs_exit_min} (closed at top of range).",
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
        ibs_v = _ibs(bars)
        if last_lower <= 0 or last_rsi <= 0 or avg_vol <= 0:
            continue
        if last_close >= last_lower:
            continue
        if last_rsi >= rsi_oversold:
            continue
        if last_vol < vol_mult * avg_vol:
            continue
        # v2: only buy band breaks that closed weak (IBS in the bottom fifth)
        if ibs_v is None or ibs_v >= ibs_entry_max:
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
                f"vol {last_vol:.0f} > {vol_mult}x avg {avg_vol:.0f}, "
                f"IBS {ibs_v:.2f} < {ibs_entry_max} (weak close). "
                f"Hard stop {stop_loss_pct*100:.1f}% below entry, "
                f"target = mid-BB ({float(bb['Middle'].iloc[-1]):.2f})."
            ),
            stop_loss_pct=stop_loss_pct,
        ))

    return intents
