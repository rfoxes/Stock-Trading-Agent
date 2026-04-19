"""Master LangGraph assembly — builds the complete trading system graph."""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog
from langgraph.graph import END, StateGraph

from quant_trading_system.agents.supervisor import SupervisorAgent
from quant_trading_system.agents.swing_trading import create_swing_agent
from quant_trading_system.graph.checkpointer import create_checkpointer
from quant_trading_system.graph.routing import supervisor_router
from quant_trading_system.models.state import SupervisorState, TradingAgentState

if TYPE_CHECKING:
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.brokers.safety_gate import SafetyGate
    from quant_trading_system.config import Settings
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.data.regime_classifier import RegimeClassifier
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

logger = structlog.get_logger(__name__)


def _wrap_agent_subgraph(agent_graph: StateGraph, agent_name: str):
    """Create a wrapper function that maps SupervisorState to TradingAgentState."""
    compiled = agent_graph.compile()

    def wrapper(state: SupervisorState) -> dict:
        """Run the agent subgraph with state mapping."""
        # Map supervisor state to agent state
        agent_state: TradingAgentState = {
            "messages": [],
            "agent_name": agent_name,
            "market_data": {},
            "signals": [],
            "selected_strategy": {},
            "risk_check": {},
            "order_requests": [],
            "portfolio_snapshot": state.get("portfolio_snapshot", {}),
            "watchlist": state.get("watchlist", []),
            "market_regime": state.get("market_regime", "unknown"),
        }

        try:
            result = compiled.invoke(agent_state)

            # Map results back to supervisor state
            pending = state.get("pending_orders", [])
            if result.get("order_requests"):
                pending.extend(result["order_requests"])

            return {
                "pending_orders": pending,
                "current_agent": "",  # Reset after agent runs
            }
        except Exception as e:
            logger.error(f"{agent_name}_subgraph_error", error=str(e))
            errors = state.get("errors", [])
            errors.append({"agent": agent_name, "error": str(e)})
            return {
                "errors": errors,
                "current_agent": "",
            }

    return wrapper


def build_trading_graph(
    settings: Settings,
    safety_gate: SafetyGate,
    market_data: MarketDataService,
    regime_classifier: RegimeClassifier,
    knowledge_base: KnowledgeBaseClient,
    alpaca_client: AlpacaClient | None = None,
):
    """Build and compile the complete trading system graph.

    Returns a compiled LangGraph that can be invoked with an initial SupervisorState.
    """
    logger.info("building_trading_graph")

    # Create the supervisor
    supervisor = SupervisorAgent(
        settings=settings,
        safety_gate=safety_gate,
        market_data=market_data,
        regime_classifier=regime_classifier,
        knowledge_base=knowledge_base,
        alpaca_client=alpaca_client,
    )

    # Create agent subgraphs
    swing_graph = create_swing_agent(settings, market_data, knowledge_base, safety_gate)

    # Build the supervisor graph
    graph = StateGraph(SupervisorState)

    # Add nodes
    graph.add_node("supervisor", supervisor.supervisor_node)
    graph.add_node("swing_agent", _wrap_agent_subgraph(swing_graph, "swing_agent"))

    # Placeholder nodes for agents not yet implemented
    def placeholder_agent(name: str):
        def _placeholder(state: SupervisorState) -> dict:
            logger.info(f"{name}_placeholder", message="Agent not yet implemented")
            return {"current_agent": ""}
        return _placeholder

    graph.add_node("intraday_agent", placeholder_agent("intraday"))
    graph.add_node("position_agent", placeholder_agent("position"))

    def risk_check_node(state: SupervisorState) -> dict:
        """Portfolio-level risk check on pending orders."""
        logger.info("risk_check_node", pending_orders=len(state.get("pending_orders", [])))
        # RiskManagerAgent will be implemented in Phase 6
        # For now, pass through all orders
        return {"pending_orders": []}

    graph.add_node("risk_check", risk_check_node)

    # Set entry point
    graph.set_entry_point("supervisor")

    # Add conditional routing from supervisor
    graph.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "intraday_agent": "intraday_agent",
            "swing_agent": "swing_agent",
            "position_agent": "position_agent",
            "risk_check": "risk_check",
            "__end__": END,
        },
    )

    # After each agent, go back to supervisor for next decision
    graph.add_edge("swing_agent", "supervisor")
    graph.add_edge("intraday_agent", "supervisor")
    graph.add_edge("position_agent", "supervisor")
    graph.add_edge("risk_check", "supervisor")

    # Compile with checkpointer
    checkpointer = create_checkpointer(settings)
    compiled = graph.compile(checkpointer=checkpointer)

    logger.info("trading_graph_built")
    return compiled
