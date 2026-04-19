"""Swing Trading Agent — the first fully functional trading agent.

Operates on daily bars with 3-20 day holding periods.
Internal subgraph: MarketAnalysis → StrategySelection → RiskEvaluation → OrderExecution
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from quant_trading_system.llm_factory import create_llm
from quant_trading_system.models.state import TradingAgentState
from quant_trading_system.models.trade import OrderRequest, OrderSide, OrderType
from quant_trading_system.tools.kelly_criterion import half_kelly, position_size
from quant_trading_system.tools.technical_indicators import compute_all_indicators

if TYPE_CHECKING:
    from quant_trading_system.brokers.safety_gate import SafetyGate
    from quant_trading_system.config import Settings
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

logger = structlog.get_logger(__name__)

MARKET_ANALYSIS_PROMPT = """You are a quantitative market analyst for swing trading (3-20 day holds).

Analyze the following technical data for {symbol}:
{indicators_summary}

Market Regime: {market_regime}

Provide a concise analysis covering:
1. Current trend direction and strength
2. Key support and resistance levels
3. Momentum indicators interpretation
4. Recommended bias: BULLISH, BEARISH, or NEUTRAL

Respond in JSON format:
{{"bias": "bullish|bearish|neutral", "confidence": 0.0-1.0, "key_levels": {{"support": X, "resistance": Y}}, "reasoning": "..."}}
"""

STRATEGY_SELECTION_PROMPT = """You are a quantitative strategy selector for swing trading.

Current market analysis:
{analysis}

Available strategies:
{strategies}

Market regime: {market_regime}

Select the most appropriate strategy for the current market conditions.
Respond in JSON format:
{{"strategy_id": "...", "reasoning": "...", "expected_edge": "..."}}
"""


def create_swing_agent(
    settings: Settings,
    market_data: MarketDataService,
    knowledge_base: KnowledgeBaseClient,
    safety_gate: SafetyGate,
) -> StateGraph:
    """Create the swing trading agent subgraph."""
    from quant_trading_system.dashboard.event_bus import event_bus

    analysis_llm = create_llm(settings, model_name=settings.ANALYSIS_MODEL)
    strategy_llm = create_llm(settings, model_name=settings.ANALYSIS_MODEL)

    def market_analysis_node(state: TradingAgentState) -> dict:
        """Fetch data and compute technical indicators for the watchlist."""
        log = logger.bind(agent="swing", node="market_analysis")
        log.info("market_analysis_start")
        event_bus.publish("log", {"level": "info", "message": "Swing agent: Market analysis starting"})

        watchlist = state.get("watchlist", ["SPY", "QQQ"])
        market_data_results = {}
        analyses = []

        for symbol in watchlist[:10]:  # Limit to 10 symbols per cycle
            try:
                df = market_data.get_bars(symbol, "1Day")
                if df.empty:
                    continue

                # Compute all indicators
                df_with_indicators = compute_all_indicators(df)

                # Summarize latest indicators
                latest = df_with_indicators.iloc[-1]
                summary = {
                    "symbol": symbol,
                    "close": float(latest["Close"]),
                    "sma_20": float(latest.get("SMA_20", 0)),
                    "sma_50": float(latest.get("SMA_50", 0)),
                    "rsi_14": float(latest.get("RSI_14", 0)),
                    "macd": float(latest.get("MACD", 0)),
                    "macd_signal": float(latest.get("MACD_Signal", 0)),
                    "macd_histogram": float(latest.get("MACD_Histogram", 0)),
                    "bb_upper": float(latest.get("BB_Upper", 0)),
                    "bb_lower": float(latest.get("BB_Lower", 0)),
                    "atr_14": float(latest.get("ATR_14", 0)),
                    "adx_14": float(latest.get("ADX_14", 0)),
                }
                market_data_results[symbol] = summary

                # Get LLM analysis
                try:
                    prompt = MARKET_ANALYSIS_PROMPT.format(
                        symbol=symbol,
                        indicators_summary=str(summary),
                        market_regime=state.get("market_regime", "unknown"),
                    )
                    response = analysis_llm.invoke([
                        SystemMessage(content="You are a quantitative analyst. Respond only in valid JSON."),
                        HumanMessage(content=prompt),
                    ])
                    analyses.append({"symbol": symbol, "analysis": response.content})
                except Exception as e:
                    log.warning("llm_analysis_failed", symbol=symbol, error=str(e))
                    analyses.append({
                        "symbol": symbol,
                        "analysis": f'{{"bias": "neutral", "confidence": 0, "reasoning": "LLM error: {e}"}}',
                    })

            except Exception as e:
                log.error("market_data_error", symbol=symbol, error=str(e))

        log.info("market_analysis_complete", symbols_analyzed=len(market_data_results))
        event_bus.publish("log", {"level": "info", "message": f"Swing agent: Analyzed {len(market_data_results)} symbols"})

        return {
            "market_data": market_data_results,
            "signals": analyses,
        }

    def strategy_selection_node(state: TradingAgentState) -> dict:
        """Select the best strategy for current conditions."""
        log = logger.bind(agent="swing", node="strategy_selection")
        log.info("strategy_selection_start")
        event_bus.publish("log", {"level": "info", "message": "Swing agent: Selecting strategy"})

        if not state.get("signals"):
            log.info("no_signals_skipping")
            return {"selected_strategy": {}}

        # Query knowledge base for swing strategies
        try:
            strategies = knowledge_base.search_strategies(
                query=f"swing trading strategy for {state.get('market_regime', 'unknown')} market",
                n_results=5,
                strategy_type="equity",
            )
        except Exception as e:
            log.error("kb_search_failed", error=str(e))
            strategies = []

        if not strategies:
            log.info("no_strategies_found")
            return {"selected_strategy": {}}

        # Ask LLM to select best strategy
        try:
            strategies_summary = "\n".join(
                f"- {s['id']}: {s['content'][:200]}..." for s in strategies
            )
            analyses_summary = "\n".join(
                f"- {a['symbol']}: {a['analysis'][:200]}" for a in state["signals"][:5]
            )

            prompt = STRATEGY_SELECTION_PROMPT.format(
                analysis=analyses_summary,
                strategies=strategies_summary,
                market_regime=state.get("market_regime", "unknown"),
            )

            response = strategy_llm.invoke([
                SystemMessage(content="You are a strategy selector. Respond only in valid JSON."),
                HumanMessage(content=prompt),
            ])

            log.info("strategy_selected", response=response.content[:200])
            return {"selected_strategy": {"response": response.content, "strategies": strategies}}

        except Exception as e:
            log.error("strategy_selection_failed", error=str(e))
            return {"selected_strategy": {}}

    def risk_evaluation_node(state: TradingAgentState) -> dict:
        """Evaluate risk for proposed trades and compute position sizes."""
        log = logger.bind(agent="swing", node="risk_evaluation")
        log.info("risk_evaluation_start")

        if not state.get("selected_strategy") or not state.get("signals"):
            return {"risk_check": {"approved": False, "reason": "no strategy or signals"}}

        portfolio = state.get("portfolio_snapshot", {})
        equity = portfolio.get("equity", settings.PAPER_PORTFOLIO_SIZE)

        # Generate order requests based on signals
        order_requests = []

        for signal in state.get("signals", []):
            analysis = signal.get("analysis", "")
            symbol = signal.get("symbol", "")

            if not symbol:
                continue

            # Simple signal interpretation: look for bullish/bearish bias
            analysis_lower = analysis.lower()
            if '"bullish"' in analysis_lower or "'bullish'" in analysis_lower:
                side = OrderSide.BUY
            elif '"bearish"' in analysis_lower or "'bearish'" in analysis_lower:
                side = OrderSide.SELL
            else:
                continue  # Neutral — skip

            # Position sizing with half-Kelly (conservative)
            market_info = state.get("market_data", {}).get(symbol, {})
            price = market_info.get("close", 0)

            if price <= 0:
                continue

            # Use conservative fixed fractional sizing
            kelly_f = half_kelly(win_rate=0.55, avg_win=0.03, avg_loss=0.02)
            shares = position_size(
                kelly_f=kelly_f,
                portfolio_value=equity,
                price_per_share=price,
                max_position_pct=settings.MAX_POSITION_SIZE_PCT,
            )

            if shares <= 0:
                continue

            order = OrderRequest(
                symbol=symbol,
                side=side,
                qty=shares,
                order_type=OrderType.MARKET,
                agent_name="swing_agent",
                strategy_name=state.get("selected_strategy", {}).get("response", "unknown")[:50],
                reasoning=f"Swing signal: {analysis[:200]}",
            )
            order_requests.append(order)

        log.info("risk_evaluation_complete", orders_generated=len(order_requests))
        event_bus.publish("log", {"level": "info", "message": f"Swing agent: Risk evaluation complete, {len(order_requests)} orders approved"})

        return {
            "risk_check": {
                "approved": len(order_requests) > 0,
                "order_count": len(order_requests),
            },
            "order_requests": [o.model_dump() for o in order_requests],
        }

    def order_execution_node(state: TradingAgentState) -> dict:
        """Submit approved orders through the safety gate."""
        log = logger.bind(agent="swing", node="order_execution")
        log.info("order_execution_start")
        event_bus.publish("log", {"level": "info", "message": "Swing agent: Executing orders"})

        risk = state.get("risk_check", {})
        if not risk.get("approved", False):
            log.info("orders_not_approved")
            return {}

        order_dicts = state.get("order_requests", [])
        results = []

        for order_dict in order_dicts:
            try:
                order = OrderRequest(**order_dict)
                result = safety_gate.validate_and_submit(order)
                results.append({
                    "symbol": order.symbol,
                    "status": result.status.value,
                    "mode": result.mode.value,
                    "order_id": result.order_id,
                })
                log.info(
                    "order_result",
                    symbol=order.symbol,
                    status=result.status.value,
                    mode=result.mode.value,
                )
            except Exception as e:
                log.error("order_execution_error", error=str(e))
                results.append({"symbol": order_dict.get("symbol", ""), "error": str(e)})

        log.info("order_execution_complete", results_count=len(results))
        return {"order_requests": results}

    # Build the subgraph
    graph = StateGraph(TradingAgentState)

    graph.add_node("market_analysis", market_analysis_node)
    graph.add_node("strategy_selection", strategy_selection_node)
    graph.add_node("risk_evaluation", risk_evaluation_node)
    graph.add_node("order_execution", order_execution_node)

    graph.set_entry_point("market_analysis")
    graph.add_edge("market_analysis", "strategy_selection")
    graph.add_edge("strategy_selection", "risk_evaluation")

    # Conditional: only execute orders if risk check approves
    def should_execute(state: TradingAgentState) -> str:
        risk = state.get("risk_check", {})
        if risk.get("approved", False):
            return "order_execution"
        return "__end__"

    graph.add_conditional_edges("risk_evaluation", should_execute)
    graph.add_edge("order_execution", END)

    return graph
