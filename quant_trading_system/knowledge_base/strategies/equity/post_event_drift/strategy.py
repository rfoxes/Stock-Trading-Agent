"""Post-Event Gap Drift — executable counterpart to strategy.md.

Event days are detected from bars (gap% + volume surge + strong close), so
the strategy is fully replayable by the backtester — including its time
exit, which counts sessions since the event day instead of relying on the
journal.
"""

from __future__ import annotations

import math

from quant_trading_system._strategy_helpers import (
    has_position,
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


def _event_mask(bars, *, min_gap: float, vol_mult: float, vol_window: int,
                require_upper_half: bool):
    """Boolean Series marking event days, computable bar-by-bar with no
    look-ahead: gap vs prior close, volume vs PRIOR `vol_window`-day average,
    close position within the day's range."""
    close = bars["Close"]
    gap = bars["Open"] / close.shift(1) - 1.0
    prior_vol_avg = bars["Volume"].shift(1).rolling(vol_window, min_periods=vol_window).mean()
    mask = (gap >= min_gap) & (bars["Volume"] >= vol_mult * prior_vol_avg)
    if require_upper_half:
        rng = bars["High"] - bars["Low"]
        pos_in_range = (close - bars["Low"]) / rng
        mask = mask & (rng > 0) & (pos_in_range >= 0.5)
    return mask.fillna(False)


def _last_event_pos(mask) -> int | None:
    """Positional index of the most recent True in the mask, else None."""
    vals = list(mask)
    for i in range(len(vals) - 1, -1, -1):
        if bool(vals[i]):
            return i
    return None


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    min_gap = float(p.get("gap_entry_min_pct", 4.0)) / 100.0
    vol_mult = float(p.get("volume_mult_min", 2.5))
    vol_window = int(p.get("volume_lookback", 20))
    require_upper_half = bool(p.get("require_close_upper_half", True))
    hold_max_sessions = int(p.get("hold_max_sessions", 15))
    target_mult = float(p.get("target_atr_multiplier", 2.0))
    stop_mult = float(p.get("stop_atr_multiplier", 1.5))
    atr_period = int(p.get("atr_period", 14))
    min_dollar_vol = float(p.get("min_avg_dollar_volume", 5_000_000))
    risk_pct = float(p.get("risk_pct_per_trade", 0.01))
    max_concurrent = int(p.get("max_concurrent_positions", 3))

    equity = float(ctx.account.get("equity", 0.0))
    intents: list[OrderIntent] = []

    # ---- Exits first ----
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        qty = position_qty(ctx.positions, sym)
        if not sym or qty <= 0:
            continue
        bars = ctx.get_bars(sym, "1Day", 320)
        if bars.empty or len(bars) < vol_window + 5:
            continue
        close = _f(bars["Close"].iloc[-1])
        atr_v = _f(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period).iloc[-1])
        avg_entry = _f(pos.get("avg_entry_price")) or 0.0
        mask = _event_mask(
            bars, min_gap=min_gap, vol_mult=vol_mult, vol_window=vol_window,
            require_upper_half=require_upper_half,
        )
        event_pos = _last_event_pos(mask)

        exit_reason: str | None = None
        if ctx.news_brief.has_negative_signal(sym):
            exit_reason = (
                f"News exit: brief has negative markers for {sym}. "
                f"Note: \"{ctx.news_brief.news_for(sym)[:160]}\""
            )
        elif event_pos is not None and close is not None:
            event_low = _f(bars["Low"].iloc[event_pos])
            bars_since_event = (len(bars) - 1) - event_pos
            if event_low is not None and close < event_low:
                exit_reason = (
                    f"Invalidation: close {close:.2f} < event-day low {event_low:.2f} "
                    f"(event {bars_since_event} sessions ago)."
                )
            elif bars_since_event >= hold_max_sessions:
                exit_reason = (
                    f"Time exit: {bars_since_event} sessions since event day >= "
                    f"{hold_max_sessions} (drift window over)."
                )
        if exit_reason is None and avg_entry > 0 and close is not None and atr_v is not None and atr_v > 0:
            if close >= avg_entry + target_mult * atr_v:
                exit_reason = (
                    f"Target: close {close:.2f} >= entry {avg_entry:.2f} "
                    f"+ {target_mult}x ATR={atr_v:.2f}."
                )
            elif close <= avg_entry - stop_mult * atr_v:
                exit_reason = (
                    f"Hard stop: close {close:.2f} <= entry {avg_entry:.2f} "
                    f"- {stop_mult}x ATR={atr_v:.2f}."
                )
        if exit_reason is None and event_pos is None:
            # No event visible in the lookback at all — the position has
            # outlived its rationale (or bars are truncated). Exit defensively.
            exit_reason = "Time exit: no event day visible in lookback window."

        if exit_reason is not None:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=exit_reason,
            ))

    # ---- Entries: today must BE an event day ----
    open_count = sum(1 for pos in ctx.positions if float(pos.get("qty", 0) or 0) > 0)
    for sym in ctx.watchlist:
        if open_count >= max_concurrent:
            break
        if has_position(ctx.positions, sym):
            continue
        if ctx.news_brief.has_negative_signal(sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 320)
        if bars.empty or len(bars) < vol_window + 5:
            continue
        mask = _event_mask(
            bars, min_gap=min_gap, vol_mult=vol_mult, vol_window=vol_window,
            require_upper_half=require_upper_half,
        )
        if not bool(mask.iloc[-1]):
            continue
        close = _f(bars["Close"].iloc[-1])
        atr_v = _f(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period).iloc[-1])
        avg_dollar_vol = _f((bars["Close"] * bars["Volume"]).tail(20).mean())
        prev_close = _f(bars["Close"].iloc[-2])
        if close is None or atr_v is None or avg_dollar_vol is None or prev_close is None:
            continue
        if atr_v <= 0 or prev_close <= 0:
            continue
        if avg_dollar_vol < min_dollar_vol:
            continue

        gap_pct = float(bars["Open"].iloc[-1]) / prev_close - 1.0
        stop_pct = (stop_mult * atr_v) / close
        target_pct = (target_mult * atr_v) / close
        if stop_pct <= 0 or target_pct <= 0:
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
                f"Event-day entry: gapped +{gap_pct*100:.1f}% on volume >= "
                f"{vol_mult}x 20d avg and held the gap into the close. Riding "
                f"post-event drift: target +{target_mult}x ATR (+{target_pct*100:.1f}%), "
                f"stop {stop_mult}x ATR (-{stop_pct*100:.1f}%), invalidation below "
                f"event-day low, {hold_max_sessions}-session time exit."
            ),
            stop_loss_pct=stop_pct,
            take_profit_pct=target_pct,
        ))
        open_count += 1

    return intents
