"""Entry point for the Autonomous Quantitative Trading System."""

from __future__ import annotations

import argparse
import sys
import threading
import uuid

import structlog

from quant_trading_system.config import Settings
from quant_trading_system.logging_config import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Autonomous Quantitative Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run full pipeline without submitting any orders",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one cycle and exit (vs. continuous scheduler mode)",
    )
    parser.add_argument(
        "--agents",
        type=str,
        default="swing",
        help="Comma-separated list of agents to activate: intraday,swing,position (default: swing)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=None,
        help="Override log level (DEBUG, INFO, WARNING, ERROR)",
    )
    parser.add_argument(
        "--seed-kb",
        action="store_true",
        help="Seed the knowledge base with initial strategies and exit",
    )
    parser.add_argument(
        "--backtest",
        type=str,
        default=None,
        help="Run backtests: --backtest auto (agent decides) or --backtest STRATEGY:SYMBOL:START:END",
    )
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Launch web dashboard at http://localhost:8501",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Dashboard port (default: 8501)",
    )
    return parser.parse_args()


def seed_knowledge_base(settings: Settings) -> None:
    """Load strategy files into ChromaDB."""
    logger = structlog.get_logger("seed_kb")
    logger.info("seeding_knowledge_base")

    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient
    from quant_trading_system.knowledge_base.strategy_loader import StrategyLoader

    kb = KnowledgeBaseClient(settings)
    loader = StrategyLoader()
    count = loader.sync_to_chroma(kb)
    logger.info("knowledge_base_seeded", strategies_loaded=count)


def _run_single_backtest(
    settings: Settings, strategy_id: str, symbol: str, start: str, end: str
) -> dict:
    """Run one backtest and publish results to dashboard."""
    logger = structlog.get_logger("backtest")
    from quant_trading_system.dashboard.event_bus import event_bus

    from quant_trading_system.agents.backtesting_agent import BacktestingAgent
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

    event_bus.publish("log", {"level": "info", "message": f"Backtesting {strategy_id} on {symbol} ({start} to {end})"})

    market_data = MarketDataService(settings)
    kb = KnowledgeBaseClient(settings)
    agent = BacktestingAgent(settings, market_data, kb)

    result = agent.backtest_strategy(strategy_id, symbol, start, end)
    metrics = result.get("report", {}).get("metrics", {})
    promotion = result.get("promotion", {})

    event_bus.publish("backtest", {
        "strategy_id": strategy_id,
        "symbol": symbol,
        "start": start,
        "end": end,
        "metrics": {k: round(v, 4) if isinstance(v, float) else v for k, v in metrics.items()
                    if k not in ("returns_series", "equity_curve")},
        "promoted": promotion.get("promoted", False),
        "promotion_reasons": promotion.get("reasons", []),
    })

    logger.info(
        "backtest_result",
        strategy=strategy_id,
        symbol=symbol,
        sharpe=metrics.get("sharpe", 0),
        total_return=metrics.get("total_return", 0),
        max_drawdown=metrics.get("max_drawdown", 0),
        promoted=promotion.get("promoted", False),
    )
    return result


def run_backtest(settings: Settings, backtest_spec: str) -> list[dict]:
    """Run backtests. Supports 'auto' mode where the agent decides everything."""
    logger = structlog.get_logger("backtest")
    from quant_trading_system.dashboard.event_bus import event_bus

    event_bus.publish("status", {"status": "running"})

    if backtest_spec.lower() == "auto":
        return run_auto_backtest(settings)

    # Manual mode: STRATEGY_ID:SYMBOL:START:END
    parts = backtest_spec.split(":")
    if len(parts) != 4:
        logger.error("invalid_backtest_spec", expected="'auto' or STRATEGY_ID:SYMBOL:START:END")
        sys.exit(1)

    strategy_id, symbol, start, end = parts
    result = _run_single_backtest(settings, strategy_id, symbol, start, end)
    event_bus.publish("status", {"status": "idle"})
    return [result]


def run_auto_backtest(settings: Settings) -> list[dict]:
    """Agent-driven backtest: picks strategies and symbols automatically."""
    logger = structlog.get_logger("backtest")
    from quant_trading_system.dashboard.event_bus import event_bus
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.data.regime_classifier import RegimeClassifier
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient
    from quant_trading_system.llm_factory import create_llm
    from langchain_core.messages import HumanMessage, SystemMessage
    import json

    event_bus.publish("log", {"level": "info", "message": "Auto-backtest: Agent is selecting strategies and symbols..."})

    market_data = MarketDataService(settings)
    kb = KnowledgeBaseClient(settings)
    regime_classifier = RegimeClassifier()

    # 1. Classify current market regime
    try:
        spy_data = market_data.get_bars("SPY", "1Day")
        regime = regime_classifier.classify(spy_data)
        event_bus.publish("regime", regime)
    except Exception:
        regime = {"regime": "unknown", "confidence": 0}

    event_bus.publish("log", {"level": "info", "message": f"Market regime: {regime.get('regime', 'unknown')} (confidence: {regime.get('confidence', 0):.0%})"})

    # 2. Get all strategies from KB
    all_strategies = kb.get_all_strategies()
    strategy_summary = "\n".join(
        f"- {s['id']}: {s['metadata'].get('name', s['id'])} (type: {s['metadata'].get('type', '?')}, timeframes: {s['metadata'].get('timeframes', '?')})"
        for s in all_strategies
    )

    # 3. Ask the LLM to pick strategies and symbols to backtest
    llm = create_llm(settings, model_name=settings.ANALYSIS_MODEL)

    prompt = f"""You are a quantitative trading strategist. Based on the current market conditions, select strategies and symbols to backtest.

Current market regime: {regime.get('regime', 'unknown')} (confidence: {regime.get('confidence', 0):.0%})
Regime details: {regime.get('reasoning', '')}

Available strategies in the knowledge base:
{strategy_summary}

Available symbols from watchlist: {', '.join(settings.watchlist)}

Select 3-5 strategy+symbol combinations to backtest. Pick strategies that are well-suited for the current market regime. Use a 2-year backtest window ending today.

Respond ONLY with a JSON array, no other text:
[
  {{"strategy_id": "...", "symbol": "...", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}},
  ...
]"""

    try:
        response = llm.invoke([
            SystemMessage(content="You are a quantitative analyst. Respond ONLY with valid JSON, no markdown."),
            HumanMessage(content=prompt),
        ])
        raw = response.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

        selections = json.loads(raw)
        if not isinstance(selections, list):
            selections = [selections]
    except Exception as e:
        logger.warning("llm_selection_failed", error=str(e))
        event_bus.publish("log", {"level": "warning", "message": f"LLM selection failed ({e}), using defaults"})
        # Fallback: pick top 3 strategies for the watchlist
        from datetime import datetime, timedelta
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
        selections = [
            {"strategy_id": all_strategies[0]["id"], "symbol": "SPY", "start": start, "end": end},
            {"strategy_id": all_strategies[1]["id"], "symbol": "QQQ", "start": start, "end": end},
            {"strategy_id": all_strategies[2]["id"], "symbol": "AAPL", "start": start, "end": end},
        ]

    event_bus.publish("log", {"level": "info", "message": f"Agent selected {len(selections)} backtests to run"})

    # 4. Run each backtest
    results = []
    for i, sel in enumerate(selections):
        sid = sel.get("strategy_id", "")
        sym = sel.get("symbol", "SPY")
        start = sel.get("start", "2022-01-01")
        end = sel.get("end", "2024-01-01")

        event_bus.publish("log", {"level": "info", "message": f"Backtest {i+1}/{len(selections)}: {sid} on {sym}"})

        try:
            result = _run_single_backtest(settings, sid, sym, start, end)
            results.append(result)
        except Exception as e:
            logger.error("backtest_failed", strategy=sid, symbol=sym, error=str(e))
            event_bus.publish("log", {"level": "error", "message": f"Backtest failed: {sid} on {sym}: {e}"})

    event_bus.publish("log", {"level": "info", "message": f"Auto-backtest complete: {len(results)} backtests finished"})
    event_bus.publish("status", {"status": "idle"})
    return results


def _init_components(settings: Settings):
    """Initialize all shared components. Returns a dict of components."""
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.brokers.safety_gate import SafetyGate
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.data.regime_classifier import RegimeClassifier
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

    logger = structlog.get_logger("main")

    market_data = MarketDataService(settings)
    regime = RegimeClassifier()
    kb = KnowledgeBaseClient(settings)

    alpaca_client = None
    if settings.ALPACA_API_KEY and not settings.DRY_RUN:
        try:
            alpaca_client = AlpacaClient(settings)
        except Exception as e:
            logger.warning("alpaca_init_failed", error=str(e))

    safety_gate = SafetyGate(settings, alpaca_client)

    return {
        "market_data": market_data,
        "regime_classifier": regime,
        "knowledge_base": kb,
        "alpaca_client": alpaca_client,
        "safety_gate": safety_gate,
    }


def run_single_cycle(settings: Settings, components: dict | None = None) -> None:
    """Run one complete trading cycle."""
    logger = structlog.get_logger("main")
    cycle_id = str(uuid.uuid4())[:8]
    structlog.contextvars.bind_contextvars(cycle_id=cycle_id)

    logger.info("single_cycle_start", dry_run=settings.DRY_RUN)

    from quant_trading_system.dashboard.event_bus import event_bus
    from quant_trading_system.graph.trading_graph import build_trading_graph
    from quant_trading_system.models.state import SupervisorState

    if components is None:
        components = _init_components(settings)

    # Publish status to dashboard
    event_bus.publish("status", {"status": "running"})
    event_bus.publish("log", {"level": "info", "message": "Trading cycle starting", "cycle_id": cycle_id})

    # Classify regime and publish
    try:
        spy_data = components["market_data"].get_bars("SPY", "1Day")
        if not spy_data.empty:
            regime_info = components["regime_classifier"].classify(spy_data)
            event_bus.publish("regime", regime_info)
    except Exception:
        pass

    # Get portfolio and publish
    if components["alpaca_client"]:
        try:
            account = components["alpaca_client"].get_account()
            positions = components["alpaca_client"].get_positions()
            portfolio_data = {
                "equity": account.get("equity", 0),
                "cash": account.get("cash", 0),
                "buying_power": account.get("buying_power", 0),
                "positions": positions,
                "unrealized_pnl": sum(p.get("unrealized_pl", 0) for p in positions),
            }
            event_bus.publish("portfolio", portfolio_data)
        except Exception:
            pass

    # Build and run the graph
    graph = build_trading_graph(
        settings=settings,
        safety_gate=components["safety_gate"],
        market_data=components["market_data"],
        regime_classifier=components["regime_classifier"],
        knowledge_base=components["knowledge_base"],
        alpaca_client=components["alpaca_client"],
    )

    initial_state: SupervisorState = {
        "messages": [],
        "current_agent": "",
        "market_regime": "unknown",
        "portfolio_snapshot": {},
        "pending_orders": [],
        "risk_assessment": {},
        "cycle_count": 0,
        "watchlist": settings.watchlist,
        "active_strategies": [],
        "errors": [],
    }

    config = {"configurable": {"thread_id": cycle_id}}

    try:
        result = graph.invoke(initial_state, config=config)

        # Publish orders to dashboard
        for order in result.get("pending_orders", []):
            event_bus.publish("order", order)

        event_bus.publish("cycle", {"cycle_count": result.get("cycle_count", 0)})
        event_bus.publish("status", {"status": "idle"})
        event_bus.publish("log", {
            "level": "info",
            "message": f"Cycle complete. Regime: {result.get('market_regime', 'unknown')}, "
                       f"Orders: {len(result.get('pending_orders', []))}, "
                       f"Errors: {len(result.get('errors', []))}",
        })

        logger.info(
            "single_cycle_complete",
            final_regime=result.get("market_regime", "unknown"),
            cycles_run=result.get("cycle_count", 0),
            pending_orders=len(result.get("pending_orders", [])),
            errors=len(result.get("errors", [])),
        )
    except Exception as e:
        event_bus.publish("status", {"status": "error"})
        event_bus.publish("log", {"level": "error", "message": f"Cycle failed: {e}"})
        logger.error("cycle_failed", error=str(e))
        raise


def run_continuous(settings: Settings) -> None:
    """Run in continuous mode with APScheduler."""
    logger = structlog.get_logger("scheduler")
    logger.info("continuous_mode_start")

    from quant_trading_system.scheduler.market_schedule import MarketScheduler

    scheduler = MarketScheduler(settings)
    scheduler.start()

    logger.info("scheduler_running", message="Press Ctrl+C to stop")
    try:
        import time

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("scheduler_stopping")
        scheduler.stop()


def start_dashboard(settings: Settings, components: dict, port: int) -> None:
    """Start the web dashboard server."""
    import uvicorn

    from quant_trading_system.dashboard.app import create_app

    app = create_app(
        settings=settings,
        kb_client=components["knowledge_base"],
        market_data=components["market_data"],
        regime_classifier=components["regime_classifier"],
        risk_manager=None,
        safety_gate=components["safety_gate"],
        alpaca_client=components["alpaca_client"],
    )

    logger = structlog.get_logger("dashboard")
    logger.info("dashboard_starting", url=f"http://localhost:{port}")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


def main() -> None:
    args = parse_args()

    # Build settings
    settings = Settings(_env_file=".env")

    # Override from CLI
    if args.dry_run:
        settings.DRY_RUN = True
    if args.log_level:
        settings.LOG_LEVEL = args.log_level

    # Setup logging
    setup_logging(settings)
    logger = structlog.get_logger("main")

    logger.info(
        "system_starting",
        mode="dry_run" if settings.DRY_RUN else ("paper" if settings.ALPACA_PAPER else "live"),
        agents=args.agents,
        dashboard=args.dashboard,
    )

    # Handle special modes
    if args.seed_kb:
        seed_knowledge_base(settings)
        return

    # Dashboard mode
    if args.dashboard:
        components = _init_components(settings)

        # Start dashboard server in background
        dashboard_thread = threading.Thread(
            target=start_dashboard,
            args=(settings, components, args.port),
            daemon=True,
        )
        dashboard_thread.start()

        import time
        time.sleep(1)  # Let server start
        logger.info("dashboard_ready", url=f"http://localhost:{args.port}")

        # Run the requested task
        if args.backtest:
            run_backtest(settings, args.backtest)
        elif args.once:
            run_single_cycle(settings, components)

        # Keep dashboard alive for review
        logger.info(
            "dashboard_running",
            url=f"http://localhost:{args.port}",
            message="Press Ctrl+C to stop",
        )
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("shutting_down")
        return

    # No dashboard — run and exit
    if args.backtest:
        run_backtest(settings, args.backtest)
        return

    if args.once:
        run_single_cycle(settings)
    else:
        run_continuous(settings)


if __name__ == "__main__":
    main()
