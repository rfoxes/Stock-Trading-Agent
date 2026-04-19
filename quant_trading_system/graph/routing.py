"""Routing functions for LangGraph conditional edges."""

from __future__ import annotations

from typing import Literal

from quant_trading_system.models.state import SupervisorState, TradingAgentState

# Valid agent node names
AGENT_NODES = ["intraday_agent", "swing_agent", "position_agent"]


def supervisor_router(
    state: SupervisorState,
) -> Literal["intraday_agent", "swing_agent", "position_agent", "risk_check", "__end__"]:
    """Route supervisor to the next agent or end the cycle."""
    current = state.get("current_agent", "")
    cycle_count = state.get("cycle_count", 0)

    # Max iterations safety
    if cycle_count >= 10:
        return "__end__"

    # If an agent is specified, route to it
    if current in AGENT_NODES:
        return current

    # If there are pending orders, route to risk check
    if state.get("pending_orders"):
        return "risk_check"

    return "__end__"


def agent_internal_router(
    state: TradingAgentState,
) -> Literal["strategy_selection", "risk_evaluation", "order_execution", "__end__"]:
    """Route within a trading agent subgraph."""
    # If market data is present but no strategy selected, go to strategy selection
    if state.get("market_data") and not state.get("selected_strategy"):
        return "strategy_selection"

    # If strategy selected but not risk-checked, evaluate risk
    if state.get("selected_strategy") and not state.get("risk_check"):
        return "risk_evaluation"

    # If risk check passed, execute orders
    risk = state.get("risk_check", {})
    if risk.get("approved", False) and state.get("signals"):
        return "order_execution"

    # Risk check failed or no signals
    return "__end__"
