"""State definitions for LangGraph trading graphs."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class TradingState:
    """Top-level state for the supervisor graph.

    Uses TypedDict-style annotations for LangGraph compatibility.
    Defined as annotations dict for LangGraph StateGraph.
    """
    pass


# LangGraph requires TypedDict, so we define states as TypedDicts
from typing import TypedDict


class SupervisorState(TypedDict):
    """State for the supervisor orchestration graph."""

    messages: Annotated[list[BaseMessage], add_messages]
    current_agent: str
    market_regime: str  # bull, bear, sideways, volatile
    portfolio_snapshot: dict  # positions, cash, P&L
    pending_orders: list[dict]
    risk_assessment: dict
    cycle_count: int
    watchlist: list[str]
    active_strategies: list[str]
    errors: list[dict]


class TradingAgentState(TypedDict):
    """State for individual trading agent subgraphs."""

    messages: Annotated[list[BaseMessage], add_messages]
    agent_name: str
    market_data: dict  # OHLCV data + computed indicators
    signals: list[dict]  # Generated trading signals
    selected_strategy: dict  # Strategy chosen for current conditions
    risk_check: dict  # Risk evaluation results
    order_requests: list[dict]  # Orders to submit
    portfolio_snapshot: dict  # Current positions from supervisor
    watchlist: list[str]
    market_regime: str
