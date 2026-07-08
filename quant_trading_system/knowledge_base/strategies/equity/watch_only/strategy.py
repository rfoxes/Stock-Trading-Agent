"""Watch-only — coverage without trading.

The library's passive fallback. It NEVER submits an order: evaluate() always
returns an empty list. Its job is to give a universe symbol an honest strategy
attachment when no trading strategy has a validated edge on it yet — "keep
watch, don't trade." The news layer still covers the symbol; Saturday research
can later upgrade it to a real trading strategy via triage / head-to-head if an
edge is found.

Operator directive 2026-07-08: every symbol the news reports on enters the
universe and gets a strategy; that strategy may just be to watch.
"""

from __future__ import annotations

from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext


def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
    # Passive by design: monitor only, never trade.
    if ctx.positions:
        # Should not normally happen — watch_only is attached to symbols with
        # no validated trading edge, which we would not have opened. Surface it
        # so a mis-attachment (a held position with a non-managing owner) is
        # visible in the logs rather than silently unmanaged.
        held = [str(p.get("symbol", "")) for p in ctx.positions]
        ctx.log.warning(
            "watch_only owns held position(s) %s but never trades/exits; "
            "research should attach a managing strategy via triage/head-to-head",
            held,
        )
    return []
