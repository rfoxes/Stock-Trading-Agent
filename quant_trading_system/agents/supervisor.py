"""Supervisor agent — orchestrates all trading agents."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import structlog
from langchain_core.messages import HumanMessage, SystemMessage

from quant_trading_system.llm_factory import create_llm
from quant_trading_system.models.state import SupervisorState

if TYPE_CHECKING:
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.brokers.safety_gate import SafetyGate
    from quant_trading_system.config import Settings
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.data.regime_classifier import RegimeClassifier
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

logger = structlog.get_logger(__name__)

SUPERVISOR_SYSTEM_PROMPT = """You are the Supervisor of an autonomous quantitative trading system.
Your role is to orchestrate trading agents across three time horizons:
- intraday_agent: Minutes-to-hours trades (only during market hours)
- swing_agent: 3-20 day trades (daily analysis)
- position_agent: 3+ week trades (weekly analysis)

Current market regime: {market_regime}
Portfolio snapshot: {portfolio_snapshot}
Active strategies: {active_strategies}

Based on the current market conditions and portfolio state, decide which agent(s) to activate next.
Respond with the agent name to activate, or "done" if no action is needed.

Rules:
1. Never activate intraday_agent outside market hours.
2. Resolve conflicts between agents (e.g., one wants to buy, another sell the same stock).
3. Respect risk limits — if drawdown is high, reduce activity.
4. Log your reasoning for audit purposes.
"""


class SupervisorAgent:
    """Orchestrates trading sub-agents through the LangGraph supervisor node."""

    def __init__(
        self,
        settings: Settings,
        safety_gate: SafetyGate,
        market_data: MarketDataService,
        regime_classifier: RegimeClassifier,
        knowledge_base: KnowledgeBaseClient,
        alpaca_client: AlpacaClient | None = None,
    ) -> None:
        self._settings = settings
        self._safety_gate = safety_gate
        self._market_data = market_data
        self._regime = regime_classifier
        self._kb = knowledge_base
        self._alpaca = alpaca_client
        self._llm = create_llm(settings, model_name=settings.SUPERVISOR_MODEL)

    def supervisor_node(self, state: SupervisorState) -> dict:
        """LangGraph node: Supervisor decision-making."""
        cycle_id = str(uuid.uuid4())[:8]
        structlog.contextvars.bind_contextvars(cycle_id=cycle_id)

        from quant_trading_system.dashboard.event_bus import event_bus

        log = logger.bind(cycle_count=state.get("cycle_count", 0))
        log.info("supervisor_cycle_start")
        event_bus.publish("log", {"level": "info", "message": f"Supervisor cycle {state.get('cycle_count', 0)} starting"})
        event_bus.publish("status", {"status": "running"})

        # Get portfolio snapshot
        portfolio = self._get_portfolio_snapshot()
        event_bus.publish("portfolio", portfolio)

        # Classify market regime
        try:
            spy_data = self._market_data.get_bars("SPY", "1Day")
            regime_info = self._regime.classify(spy_data)
            market_regime = regime_info["regime"]
            event_bus.publish("regime", regime_info)
        except Exception as e:
            log.warning("regime_classification_failed", error=str(e))
            market_regime = state.get("market_regime", "unknown")
            regime_info = {"regime": market_regime, "confidence": 0}

        # Get active strategies from knowledge base
        try:
            active_strats = self._kb.get_all_strategies()
            active_names = [s["metadata"].get("name", s["id"]) for s in active_strats[:10]]
        except Exception:
            active_names = state.get("active_strategies", [])

        # Ask Claude for routing decision
        prompt = SUPERVISOR_SYSTEM_PROMPT.format(
            market_regime=market_regime,
            portfolio_snapshot=portfolio,
            active_strategies=active_names,
        )

        try:
            response = self._llm.invoke([
                SystemMessage(content=prompt),
                HumanMessage(content=(
                    f"Cycle {state.get('cycle_count', 0)}. "
                    f"Regime: {market_regime} (confidence: {regime_info.get('confidence', 0)}). "
                    f"Errors from last cycle: {state.get('errors', [])}. "
                    "Which agent should run next? Respond with the agent name or 'done'."
                )),
            ])
            decision = response.content.strip().lower()
        except Exception as e:
            log.error("supervisor_llm_error", error=str(e))
            decision = "swing_agent"  # Safe default

        # Parse decision
        if "intraday" in decision:
            next_agent = "intraday_agent"
        elif "swing" in decision:
            next_agent = "swing_agent"
        elif "position" in decision:
            next_agent = "position_agent"
        else:
            next_agent = ""

        log.info("supervisor_decision", next_agent=next_agent or "done", raw=decision)
        event_bus.publish("log", {"level": "info", "message": f"Supervisor decision: {next_agent or 'done'}"})
        event_bus.publish("cycle", {"cycle_count": state.get("cycle_count", 0) + 1})

        return {
            "current_agent": next_agent,
            "market_regime": market_regime,
            "portfolio_snapshot": portfolio,
            "active_strategies": active_names,
            "cycle_count": state.get("cycle_count", 0) + 1,
        }

    def _get_portfolio_snapshot(self) -> dict:
        """Get current portfolio state from Alpaca or return empty."""
        if self._alpaca is None:
            return {
                "equity": self._settings.PAPER_PORTFOLIO_SIZE,
                "cash": self._settings.PAPER_PORTFOLIO_SIZE,
                "positions": [],
                "unrealized_pnl": 0.0,
            }
        try:
            account = self._alpaca.get_account()
            positions = self._alpaca.get_positions()
            return {
                "equity": account.get("equity", 0),
                "cash": account.get("cash", 0),
                "positions": positions,
                "unrealized_pnl": sum(p.get("unrealized_pl", 0) for p in positions),
            }
        except Exception as e:
            logger.warning("portfolio_snapshot_error", error=str(e))
            return {
                "equity": self._settings.PAPER_PORTFOLIO_SIZE,
                "cash": self._settings.PAPER_PORTFOLIO_SIZE,
                "positions": [],
                "unrealized_pnl": 0.0,
            }
