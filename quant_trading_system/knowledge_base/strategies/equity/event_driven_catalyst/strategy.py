"""Event-Driven Catalyst — entries on positive news, exits on negative news.

The only strategy in the library that reads ctx.news_brief as a signal
(every other strategy uses news at most as a filter). It's the user's
explicit "trade on news" answer in the harness.

This is intentionally simpler than the technical strategies — no EMAs, no
oscillators. News is the trigger; ATR sets the stop; the time stop forces
turnover so the strategy can't drift into long-term holds.
"""

from __future__ import annotations

from quant_trading_system._strategy_helpers import (
    has_position,
    position_qty,
    share_count,
)
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext
from quant_trading_system.tools import technical_indicators as ti


MAX_CONCURRENT_FROM_THIS_STRATEGY = 3


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    p = ctx.params
    risk_pct = float(p.get("risk_pct_per_trade", 0.01))
    atr_stop_mult = float(p.get("stop_atr_multiplier", 2.0))
    atr_period = int(p.get("atr_period", 14))
    equity = float(ctx.account.get("equity", 0.0))
    brief = ctx.news_brief
    intents: list[OrderIntent] = []

    # ---- Exits first: negative news on any held position takes precedence ----
    for pos in ctx.positions:
        sym = str(pos.get("symbol", "")).upper()
        if not sym:
            continue
        if brief.has_negative_signal(sym):
            qty = position_qty(ctx.positions, sym)
            if qty > 0:
                intents.append(OrderIntent(
                    symbol=sym, side="sell", qty=qty, order_type="market",
                    reasoning=(
                        f"News exit: brief contains negative markers for {sym}. "
                        f"Note: \"{brief.news_for(sym)[:200]}\""
                    ),
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
