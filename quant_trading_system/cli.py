"""Command-line wrapper around the most-used agent tools.

Designed for the Cowork-mode harness: when Claude is the orchestrator (instead
of `orchestrator.py` calling Claude via API), it shells out to this CLI to do
deterministic things — read health signals, submit orders through SafetyGate,
write the journal, etc.

Every subcommand prints one JSON object to stdout (compact, one line). All
diagnostic logs go to stderr. Exit 0 on success.

Usage:
    python -m quant_trading_system.cli regime
    python -m quant_trading_system.cli health mean_reversion_bollinger
    python -m quant_trading_system.cli portfolio-health
    python -m quant_trading_system.cli account
    python -m quant_trading_system.cli positions
    python -m quant_trading_system.cli open-orders
    python -m quant_trading_system.cli bars SPY --days 60
    python -m quant_trading_system.cli indicator SPY rsi --period 14
    python -m quant_trading_system.cli quote SPY
    python -m quant_trading_system.cli recent-trades --days 30
    python -m quant_trading_system.cli kelly-size --win-rate 0.55 --avg-win 0.03 --avg-loss 0.02 --price 450
    python -m quant_trading_system.cli submit STRATEGY_ID SYMBOL SIDE QTY --reasoning "..."
    python -m quant_trading_system.cli cancel ORDER_ID
    python -m quant_trading_system.cli log-closed STRATEGY_ID SYMBOL PNL
    python -m quant_trading_system.cli set-active STRATEGY_ID --reason "..."

The CLI always uses the same ToolContext as `orchestrator.py`, so SafetyGate,
the journal, and DRY_RUN behave identically across both modes.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from typing import Any

from quant_trading_system import agent_tools
from quant_trading_system.agent_tools import ToolContext
from quant_trading_system.config import Settings


def _build_context() -> ToolContext:
    """Same setup as orchestrator._init_components — single source of truth."""
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.brokers.safety_gate import SafetyGate
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.data.regime_classifier import RegimeClassifier

    settings = Settings(_env_file=".env")
    market_data = MarketDataService(settings)
    regime = RegimeClassifier()

    alpaca = None
    if settings.ALPACA_API_KEY and not settings.DRY_RUN:
        try:
            alpaca = AlpacaClient(settings)
        except Exception as e:
            print(f"[cli] alpaca init failed: {e}", file=sys.stderr)

    safety_gate = SafetyGate(settings, alpaca)
    return ToolContext(
        settings=settings,
        market_data=market_data,
        regime_classifier=regime,
        safety_gate=safety_gate,
        alpaca_client=alpaca,
        run_id=f"cli-{uuid.uuid4().hex[:8]}",
    )


def _emit(payload: Any) -> None:
    """Print one JSON object to stdout."""
    print(json.dumps(payload, default=str))


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def cmd_regime(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.classify_regime(ctx, symbol=args.symbol))
    return 0


def cmd_health(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_strategy_health(
        ctx, strategy_id=args.strategy_id, lookback_days=args.days
    ))
    return 0


def cmd_portfolio_health(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_portfolio_health(ctx, lookback_days=args.days))
    return 0


def cmd_account(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_account(ctx))
    return 0


def cmd_positions(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_positions(ctx))
    return 0


def cmd_open_orders(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_open_orders(ctx))
    return 0


def cmd_bars(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_bars(
        ctx, symbol=args.symbol, timeframe=args.timeframe, lookback_days=args.days
    ))
    return 0


def cmd_indicator(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.compute_indicator(
        ctx, symbol=args.symbol, indicator=args.indicator, period=args.period
    ))
    return 0


def cmd_quote(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_quote(ctx, symbol=args.symbol))
    return 0


def cmd_recent_trades(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_recent_trades(
        ctx, days=args.days, strategy_id=args.strategy_id
    ))
    return 0


def cmd_market_status(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.market_status(ctx))
    return 0


def cmd_kelly_size(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.kelly_position_size(
        ctx,
        win_rate=args.win_rate,
        avg_win=args.avg_win,
        avg_loss=args.avg_loss,
        price_per_share=args.price,
        portfolio_value=args.portfolio_value,
        fraction=args.fraction,
        max_position_pct=args.max_position_pct,
    ))
    return 0


def cmd_submit(ctx: ToolContext, args: argparse.Namespace) -> int:
    if not args.reasoning:
        print(
            "[cli] --reasoning is required (must include stop/target plan)",
            file=sys.stderr,
        )
        return 2
    _emit(agent_tools.submit_order(
        ctx,
        symbol=args.symbol,
        side=args.side,
        qty=args.qty,
        order_type=args.order_type,
        strategy_id=args.strategy_id,
        time_in_force=args.tif,
        limit_price=args.limit_price,
        stop_price=args.stop_price,
        reasoning=args.reasoning,
    ))
    return 0


def cmd_cancel(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.cancel_order(ctx, order_id=args.order_id))
    return 0


def cmd_log_closed(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.log_trade_closed(
        ctx,
        strategy_id=args.strategy_id,
        symbol=args.symbol,
        pnl=args.pnl,
        pnl_pct=args.pnl_pct,
        notes=args.notes,
    ))
    return 0


def cmd_set_active(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.set_active_strategy(
        ctx, strategy_id=args.strategy_id, reason=args.reason, notes=args.notes
    ))
    return 0


def cmd_get_active(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.get_active_strategy(ctx))
    return 0


def cmd_list_strategies(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.list_strategies(
        ctx,
        status=args.status,
        type=args.type,
        include_archived=args.include_archived,
    ))
    return 0


def cmd_run_backtest(ctx: ToolContext, args: argparse.Namespace) -> int:
    _emit(agent_tools.run_backtest(
        ctx,
        strategy_id=args.strategy_id,
        symbol=args.symbol,
        start=args.start,
        end=args.end,
    ))
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="quant_trading_system.cli",
        description="CLI for the daily trading harness.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # regime
    sp = sub.add_parser("regime", help="Classify current market regime.")
    sp.add_argument("--symbol", default="SPY")
    sp.set_defaults(func=cmd_regime)

    # health
    sp = sub.add_parser("health", help="Deterministic health for one strategy.")
    sp.add_argument("strategy_id")
    sp.add_argument("--days", type=int, default=30)
    sp.set_defaults(func=cmd_health)

    # portfolio-health
    sp = sub.add_parser("portfolio-health", help="Portfolio-wide health snapshot.")
    sp.add_argument("--days", type=int, default=30)
    sp.set_defaults(func=cmd_portfolio_health)

    # account
    sp = sub.add_parser("account", help="Broker account state.")
    sp.set_defaults(func=cmd_account)

    # positions
    sp = sub.add_parser("positions", help="Current positions.")
    sp.set_defaults(func=cmd_positions)

    # open-orders
    sp = sub.add_parser("open-orders", help="Open orders on the broker.")
    sp.set_defaults(func=cmd_open_orders)

    # bars
    sp = sub.add_parser("bars", help="Recent OHLCV bars for a symbol.")
    sp.add_argument("symbol")
    sp.add_argument("--timeframe", default="1Day")
    sp.add_argument("--days", type=int, default=60)
    sp.set_defaults(func=cmd_bars)

    # indicator
    sp = sub.add_parser("indicator", help="Compute one technical indicator.")
    sp.add_argument("symbol")
    sp.add_argument("indicator", choices=["sma", "ema", "rsi", "macd", "bbands", "atr", "adx", "obv"])
    sp.add_argument("--period", type=int)
    sp.set_defaults(func=cmd_indicator)

    # quote
    sp = sub.add_parser("quote", help="Latest bid/ask.")
    sp.add_argument("symbol")
    sp.set_defaults(func=cmd_quote)

    # recent-trades
    sp = sub.add_parser("recent-trades", help="Read journal events.")
    sp.add_argument("--days", type=int, default=30)
    sp.add_argument("--strategy-id")
    sp.set_defaults(func=cmd_recent_trades)

    # market-status
    sp = sub.add_parser("market-status", help="Whether the market is open.")
    sp.set_defaults(func=cmd_market_status)

    # kelly-size
    sp = sub.add_parser("kelly-size", help="Compute Kelly-sized position.")
    sp.add_argument("--win-rate", type=float, required=True)
    sp.add_argument("--avg-win", type=float, required=True)
    sp.add_argument("--avg-loss", type=float, required=True)
    sp.add_argument("--price", type=float, required=True)
    sp.add_argument("--portfolio-value", type=float, default=None)
    sp.add_argument("--fraction", type=float, default=0.5, help="0.5 = half-Kelly (default).")
    sp.add_argument("--max-position-pct", type=float, default=None)
    sp.set_defaults(func=cmd_kelly_size)

    # submit
    sp = sub.add_parser("submit", help="Submit an order through SafetyGate.")
    sp.add_argument("strategy_id")
    sp.add_argument("symbol")
    sp.add_argument("side", choices=["buy", "sell"])
    sp.add_argument("qty", type=float)
    sp.add_argument("--reasoning", required=True, help="Required: include stop/target plan.")
    sp.add_argument("--order-type", default="market", choices=["market", "limit", "stop", "stop_limit"])
    sp.add_argument("--tif", default="day", choices=["day", "gtc", "ioc", "fok"])
    sp.add_argument("--limit-price", type=float)
    sp.add_argument("--stop-price", type=float)
    sp.set_defaults(func=cmd_submit)

    # cancel
    sp = sub.add_parser("cancel", help="Cancel an open order.")
    sp.add_argument("order_id")
    sp.set_defaults(func=cmd_cancel)

    # log-closed
    sp = sub.add_parser("log-closed", help="Log a closed-position outcome.")
    sp.add_argument("strategy_id")
    sp.add_argument("symbol")
    sp.add_argument("pnl", type=float, help="Realized return as fraction (e.g. 0.03 = +3%).")
    sp.add_argument("--pnl-pct", type=float, default=None)
    sp.add_argument("--notes", default="")
    sp.set_defaults(func=cmd_log_closed)

    # set-active
    sp = sub.add_parser("set-active", help="Switch the active strategy.")
    sp.add_argument("strategy_id")
    sp.add_argument("--reason", required=True)
    sp.add_argument("--notes", default="")
    sp.set_defaults(func=cmd_set_active)

    # get-active
    sp = sub.add_parser("get-active", help="Show current active strategy.")
    sp.set_defaults(func=cmd_get_active)

    # list-strategies
    sp = sub.add_parser("list-strategies", help="List strategies on disk.")
    sp.add_argument("--status", choices=["active", "testing", "deprecated", "proposed", "archived"])
    sp.add_argument("--type", choices=["equity", "options"])
    sp.add_argument("--include-archived", action="store_true")
    sp.set_defaults(func=cmd_list_strategies)

    # backtest
    sp = sub.add_parser("backtest", help="Run an equity backtest.")
    sp.add_argument("strategy_id")
    sp.add_argument("symbol")
    sp.add_argument("start", help="YYYY-MM-DD")
    sp.add_argument("end", help="YYYY-MM-DD")
    sp.set_defaults(func=cmd_run_backtest)

    return p


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        ctx = _build_context()
    except Exception as e:
        print(f"[cli] failed to build context: {e}", file=sys.stderr)
        return 4
    try:
        return args.func(ctx, args)
    except Exception as e:
        import traceback
        print(f"[cli] command failed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
