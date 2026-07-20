"""Turn-of-the-Month — executable counterpart to strategy.md.

Enter when 4 weekdays remain in the month (fill next open ≈ T-4); exit
once the new month has printed its 3rd session bar (fill ≈ T+4 open).
Both signals derive from dates/bars only, so backtests replay them
exactly.
"""

from __future__ import annotations

import datetime as dt
import math

from quant_trading_system._strategy_helpers import (
    has_position,
    position_age_days,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def _f(x) -> float | None:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def _weekdays_remaining_in_month(d: dt.date) -> int:
    """Mon-Fri days strictly after `d` within d's calendar month."""
    n = 0
    cur = d + dt.timedelta(days=1)
    while cur.month == d.month:
        if cur.weekday() < 5:
            n += 1
        cur += dt.timedelta(days=1)
    return n


def _bars_in_month(bars, year: int, month: int) -> int:
    n = 0
    for ts in bars.index[-40:]:  # a month never has more than ~23 sessions
        try:
            if ts.year == year and ts.month == month:
                n += 1
        except AttributeError:
            continue
    return n


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    entry_wd_before_eom = int(p.get("entry_weekdays_before_eom", 4))
    exit_td_of_month = int(p.get("exit_trading_day_of_month", 3))
    stop_loss_pct = float(p.get("stop_loss_pct", 3.0)) / 100.0
    max_hold_days = int(p.get("max_hold_days", 12))
    use_trend_filter = bool(p.get("use_trend_filter", False))
    trend_period = int(p.get("trend_ma_period", 200))
    trend_min_periods = int(p.get("trend_ma_min_periods", 60))
    risk_pct = float(p.get("risk_pct_per_trade", 0.01))

    equity = float(ctx.account.get("equity", 0.0))
    today: dt.date = ctx.date
    intents: list[OrderIntent] = []

    # ---- Exits first ----
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        qty = position_qty(ctx.positions, sym)
        if not sym or qty <= 0:
            continue
        bars = ctx.get_bars(sym, "1Day", 60)
        if bars.empty:
            continue
        close = _f(bars["Close"].iloc[-1])
        avg_entry = _f(pos.get("avg_entry_price")) or 0.0
        month_bars = _bars_in_month(bars, today.year, today.month)
        # Entries only happen at month END (>= entry window), so a held
        # position observed on the month's 3rd+ session bar was entered for
        # THIS turn — the window is done.
        in_entry_window = _weekdays_remaining_in_month(today) < 5

        exit_reason: str | None = None
        if month_bars >= exit_td_of_month and not in_entry_window:
            exit_reason = (
                f"Calendar exit: session bar #{month_bars} of the new month >= "
                f"{exit_td_of_month} (turn-of-month window over)."
            )
        elif avg_entry > 0 and close is not None and close <= avg_entry * (1 - stop_loss_pct):
            exit_reason = (
                f"Safety stop: close {close:.2f} <= entry {avg_entry:.2f} "
                f"- {stop_loss_pct*100:.1f}%."
            )
        else:
            age = position_age_days(ctx.strategy_id, sym, today)
            if age is not None and age >= max_hold_days:
                exit_reason = f"Failsafe time stop: held {age}d >= {max_hold_days}d."

        if exit_reason is not None:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=exit_reason,
            ))

    # ---- Entries: exactly N weekdays remain in the month ----
    if _weekdays_remaining_in_month(today) != entry_wd_before_eom:
        return intents

    for sym in ctx.watchlist:
        if has_position(ctx.positions, sym):
            continue
        bars = ctx.get_bars(sym, "1Day", 320)
        if bars.empty or len(bars) < 20:
            continue
        close = _f(bars["Close"].iloc[-1])
        if close is None or close <= 0:
            continue
        if use_trend_filter:
            sma = _f(bars["Close"].rolling(trend_period, min_periods=trend_min_periods).mean().iloc[-1])
            if sma is None or close <= sma:
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
                f"Turn-of-month entry: {entry_wd_before_eom} weekdays remain in "
                f"{today.strftime('%B')}; long through the ~{exit_td_of_month}rd "
                f"session of next month. Safety stop -{stop_loss_pct*100:.1f}%."
            ),
            stop_loss_pct=stop_loss_pct,
        ))

    return intents
