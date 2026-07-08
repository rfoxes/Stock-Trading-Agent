"""Event-Driven Catalyst — entries on positive news, exits on negative news.

The only strategy in the library that reads ctx.news_brief as a signal
(every other strategy uses news at most as a filter). It's the user's
explicit "trade on news" answer in the harness.

This is intentionally simpler than the technical strategies — no EMAs, no
oscillators. News is the trigger; ATR sets the stop; the time stop forces
turnover so the strategy can't drift into long-term holds.
"""

from __future__ import annotations

import datetime as dt

from quant_trading_system import journal
from quant_trading_system._strategy_helpers import (
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


MAX_CONCURRENT_FROM_THIS_STRATEGY = 3

# How far back to scan the journal when dating a held position's entry.
# Positions should never live longer than max_hold_days, but they can drift
# if a prior run failed to enforce the stop — keep generous headroom.
_JOURNAL_LOOKBACK_DAYS = 180


def _position_age_days(strategy_id: str, symbol: str, run_date: dt.date) -> int | None:
    """Calendar days since this strategy opened the *current* lot of ``symbol``.

    The live Alpaca position object carries no entry date, so we derive it from
    the journal: the entry is the earliest ``order_submitted`` buy that follows
    the most recent ``trade_closed`` for the symbol (a re-entry resets the
    clock). Returns ``None`` if no entry can be located — in that case we do NOT
    force a time-stop, because we can't prove the position's age.
    """
    sym = symbol.upper()
    try:
        events = journal.read_events(
            days=_JOURNAL_LOOKBACK_DAYS,
            strategy_id=strategy_id,
            types=["order_submitted", "trade_closed"],
        )
    except Exception:
        return None
    entry_ts: str | None = None
    for e in events:  # oldest-first
        if str(e.get("symbol", "")).upper() != sym:
            continue
        if e.get("type") == "trade_closed":
            entry_ts = None  # position closed; clock resets for any re-entry
        elif (
            e.get("type") == "order_submitted"
            and str(e.get("side", "")).lower() == "buy"
            and e.get("result_status") == "submitted"
            and entry_ts is None
        ):
            entry_ts = e.get("timestamp")
    if not entry_ts:
        return None
    try:
        entry_date = dt.datetime.fromisoformat(entry_ts).date()
    except ValueError:
        return None
    return (run_date - entry_date).days


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    risk_pct = float(p.get("risk_pct_per_trade", 0.01))
    atr_stop_mult = float(p.get("stop_atr_multiplier", 2.0))
    atr_period = int(p.get("atr_period", 14))
    max_hold_days = int(p.get("max_hold_days", 7))
    equity = float(ctx.account.get("equity", 0.0))
    brief = ctx.news_brief
    intents: list[OrderIntent] = []

    # ---- Exits first, and always (they run before the halt-worthy entry gate
    #      so the strategy can always reduce risk). ctx.positions is already
    #      narrowed by the runtime to THIS strategy's claimed symbols, so we
    #      never touch another strategy's positions. Each held name emits at
    #      most one sell; priority: negative news > hard stop > time stop.
    #
    #      There is no resting broker stop order — the entry submits a plain
    #      market buy. THE STRATEGY IS THE STOP: the hard stop and time stop are
    #      re-derived and re-checked here every session. ----
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        qty = position_qty(ctx.positions, sym)
        if not sym or qty <= 0:
            continue

        exit_reason: str | None = None

        # (1) Negative-news exit — the catalyst turned; takes precedence.
        if brief.has_negative_signal(sym):
            exit_reason = (
                f"News exit: brief contains negative markers for {sym}. "
                f"Note: \"{brief.news_for(sym)[:200]}\""
            )

        # (2) Hard stop — current price <= entry - stop_atr_multiplier*ATR(14),
        #     ATR re-computed from current bars. Skipped (not fatal) if bars are
        #     unavailable, so a data gap never blocks the time stop below.
        if exit_reason is None:
            entry = float(pos.get("avg_entry_price", 0) or 0)
            cur = float(pos.get("current_price", 0) or 0)
            bars = ctx.get_bars(sym, "1Day", 60)
            if entry > 0 and not bars.empty and len(bars) >= atr_period + 1:
                atr = ti.compute_atr(
                    bars["High"], bars["Low"], bars["Close"], atr_period
                )
                last_atr = float(atr.iloc[-1] or 0)
                if cur <= 0:
                    cur = float(bars["Close"].iloc[-1])
                stop_level = entry - atr_stop_mult * last_atr
                if last_atr > 0 and cur > 0 and cur <= stop_level:
                    exit_reason = (
                        f"Hard stop: {sym} {cur:.2f} <= entry {entry:.2f} - "
                        f"{atr_stop_mult}x ATR({atr_period})={last_atr:.2f} "
                        f"(stop {stop_level:.2f})."
                    )

        # (3) Time stop — the catalyst edge decays fast; force turnover.
        if exit_reason is None:
            age = _position_age_days(ctx.strategy_id, sym, ctx.date)
            if age is not None and age >= max_hold_days:
                exit_reason = (
                    f"Time stop: {sym} held {age}d >= max_hold_days "
                    f"{max_hold_days}; catalyst edge decayed."
                )

        if exit_reason is not None:
            intents.append(OrderIntent(
                symbol=sym, side="sell", qty=qty, order_type="market",
                reasoning=exit_reason,
            ))

    # ---- Entries: only if the day allows it ----
    if brief.is_halt_worthy():
        ctx.log.info("skip_entries: brief is HALT-WORTHY EVENT")
        return intents

    # How many positions has this strategy already opened? We don't track
    # by strategy attribution at the broker level, so use the operator's
    # rule of thumb: never run more than N catalyst longs concurrently.
    open_long_count = sum(
        1 for pos in ctx.positions if float(pos.get("qty", 0) or 0) > 0
    )

    # Candidate universe is whatever the strategy's filtered universe says —
    # plus any held symbols that have FRESH positive news (rare; we usually
    # don't add to winners on news alone, so we just consider new entries).
    for sym in ctx.watchlist:
        if open_long_count >= MAX_CONCURRENT_FROM_THIS_STRATEGY:
            break
        if has_position(ctx.positions, sym):
            continue
        if not brief.has_positive_signal(sym):
            continue
        if brief.has_negative_signal(sym):
            # Mixed signal — pass
            continue

        # Need bars for ATR + sizing
        bars = ctx.get_bars(sym, "1Day", 60)
        if bars.empty or len(bars) < atr_period + 5:
            continue
        atr = ti.compute_atr(bars["High"], bars["Low"], bars["Close"], atr_period)
        last_atr = float(atr.iloc[-1] or 0)
        last_close = float(bars["Close"].iloc[-1])
        if last_atr <= 0 or last_close <= 0:
            continue
        stop_distance = atr_stop_mult * last_atr
        stop_pct = stop_distance / last_close
        if stop_pct <= 0:
            continue

        shares = share_count(
            equity=equity, risk_pct=risk_pct,
            entry_price=last_close, stop_distance_pct=stop_pct,
            max_position_pct=float(ctx.params.get("max_position_pct", 0.10)),
        )
        if shares <= 0:
            continue
        stop_price = round(last_close - stop_distance, 2)

        intents.append(OrderIntent(
            symbol=sym, side="buy", qty=float(shares), order_type="market",
            time_in_force="day",
            reasoning=(
                f"Catalyst entry: brief flags positive news for {sym}. "
                f"Note: \"{brief.news_for(sym)[:200]}\". "
                f"Stop @ {stop_price} ({atr_stop_mult}x ATR={last_atr:.2f}, "
                f"-{stop_pct*100:.1f}%). Risk = {risk_pct*100:.1f}% of equity. "
                f"7-day time stop applies."
            ),
            stop_loss_pct=stop_pct,
        ))
        open_long_count += 1

    return intents
