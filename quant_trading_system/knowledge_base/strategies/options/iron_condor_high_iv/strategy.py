"""Iron Condor (High IV) — real implementation.

End-to-end proof that the harness can actually trade options. Flow:
  1. For each symbol in our (filtered) universe with a chain available:
  2. Check IV rank >= min_iv_rank.
  3. Find expirations within DTE range (30-45 by default).
  4. For the chosen expiration: find 0.16-delta short strikes (put + call).
  5. Build the wings 5 strikes away (or $5 wide depending on price level).
  6. Construct a 4-leg OptionsIntent: short put + long put wing + short call + long call wing.
  7. Submit through SafetyGate's options validator.

This strategy is defined-risk: max loss = (wing width - net credit) * 100 per spread.

If options data is unavailable (chain returns []), the strategy logs and
returns no intents — same graceful degradation as every other strategy.
"""

from __future__ import annotations

from quant_trading_system.options import (
    expirations_in_dte_range,
    find_strike_by_delta,
    parse_occ_symbol,
)
from quant_trading_system.strategy_runtime import OptionsIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list:
    p = ctx.params
    min_iv_rank = float(p.get("min_iv_rank", 50))
    short_delta = float(p.get("short_strike_delta", 0.16))
    wing_width = float(p.get("long_wing_width", 5))
    dte_range = p.get("dte_range") or [30, 45]
    min_dte = int(dte_range[0])
    max_dte = int(dte_range[1])
    max_loss_pct = float(p.get("max_portfolio_risk_pct", 5)) / 100.0
    premium_to_width_ratio = float(p.get("premium_to_width_ratio", 0.33))

    equity = float(ctx.account.get("equity", 0.0))
    if equity <= 0:
        return []

    # HALT-WORTHY news → skip entries
    if ctx.news_brief.is_halt_worthy():
        ctx.log.info("skip: brief HALT-WORTHY EVENT")
        return []

    intents: list = []

    for sym in ctx.watchlist:
        # Negative news on the underlying → skip (don't sell vol into a story)
        if ctx.news_brief.has_negative_signal(sym):
            ctx.log.info("skip %s: negative news in brief", sym)
            continue

        iv_rank = ctx.compute_iv_rank(sym)
        if iv_rank is None or iv_rank < min_iv_rank:
            ctx.log.info(
                "skip %s: iv_rank=%s < %s", sym, iv_rank, min_iv_rank,
            )
            continue

        chain = ctx.get_options_chain(sym)
        if not chain:
            ctx.log.info("skip %s: no chain available", sym)
            continue

        # Pick first expiration in our DTE range
        exps = expirations_in_dte_range(chain, min_dte, max_dte)
        if not exps:
            ctx.log.info("skip %s: no expirations in DTE range %d-%d", sym, min_dte, max_dte)
            continue
        expiration = exps[0]

        # Short legs: 0.16-delta call + 0.16-delta put
        short_call_snap = find_strike_by_delta(
            chain, target_delta=short_delta, right="C", expiration=expiration,
        )
        short_put_snap = find_strike_by_delta(
            chain, target_delta=short_delta, right="P", expiration=expiration,
        )
        if not short_call_snap or not short_put_snap:
            ctx.log.info("skip %s: missing short strikes at delta %.2f", sym, short_delta)
            continue

        short_call = parse_occ_symbol(short_call_snap["symbol"])
        short_put = parse_occ_symbol(short_put_snap["symbol"])

        # Long wings: same expiration, strikes wing_width away
        long_call_strike = short_call.strike + wing_width
        long_put_strike = short_put.strike - wing_width
        long_call_snap = next(
            (
                s for s in chain
                if (c := _try_parse(s["symbol"])) is not None
                and c.right == "C"
                and c.expiration == expiration
                and abs(c.strike - long_call_strike) < 0.01
            ),
            None,
        )
        long_put_snap = next(
            (
                s for s in chain
                if (c := _try_parse(s["symbol"])) is not None
                and c.right == "P"
                and c.expiration == expiration
                and abs(c.strike - long_put_strike) < 0.01
            ),
            None,
        )
        if not long_call_snap or not long_put_snap:
            ctx.log.info("skip %s: missing wing strikes at +/-%s", sym, wing_width)
            continue

        # Estimate net credit from quote mids
        def _mid(snap) -> float:
            q = snap.get("latestQuote") or {}
            bid = float(q.get("bp") or q.get("bid") or 0.0)
            ask = float(q.get("ap") or q.get("ask") or 0.0)
            return (bid + ask) / 2 if bid and ask else 0.0

        net_credit = (
            _mid(short_call_snap) + _mid(short_put_snap)
            - _mid(long_call_snap) - _mid(long_put_snap)
        )
        if net_credit <= 0:
            ctx.log.info("skip %s: net credit %.2f <= 0", sym, net_credit)
            continue

        # Premium-to-width filter
        if net_credit < premium_to_width_ratio * wing_width:
            ctx.log.info(
                "skip %s: net credit %.2f < %.2f%% of width %s",
                sym, net_credit, premium_to_width_ratio * 100, wing_width,
            )
            continue

        # Max loss per spread (one contract per leg, $100 multiplier)
        max_loss_per_spread = (wing_width - net_credit) * 100.0
        # Size: how many spreads to fit our risk budget?
        budget = equity * max_loss_pct
        contracts = max(1, int(budget // max_loss_per_spread))
        declared_max_loss = max_loss_per_spread * contracts

        # Construct the 4-leg intent
        intent = OptionsIntent(
            legs=[
                {"contract_symbol": short_put.occ_symbol, "side": "sell", "ratio": 1},
                {"contract_symbol": long_put_snap["symbol"], "side": "buy", "ratio": 1},
                {"contract_symbol": short_call.occ_symbol, "side": "sell", "ratio": 1},
                {"contract_symbol": long_call_snap["symbol"], "side": "buy", "ratio": 1},
            ],
            qty=contracts,
            order_type="limit",
            limit_price=round(net_credit, 2),  # net credit limit
            time_in_force="day",
            reasoning=(
                f"Iron condor on {sym}, exp {expiration}: "
                f"-{short_put.strike}P / +{long_put_strike}P / "
                f"-{short_call.strike}C / +{long_call_strike}C. "
                f"IV rank={iv_rank:.0f}, net credit=${net_credit:.2f}, "
                f"max loss=${declared_max_loss:.0f}, "
                f"size={contracts}x. "
                f"Close at 50% profit per strategy.md."
            ),
            declared_max_loss_usd=declared_max_loss,
            allow_undefined_risk=False,
        )
        intents.append(intent)

    return intents


def _try_parse(symbol):
    try:
        return parse_occ_symbol(symbol)
    except Exception:
        return None
