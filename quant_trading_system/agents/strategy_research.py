"""Strategy Research Agent — discovers and proposes new trading strategies.

Does not trade directly. Instead, it analyzes recent market data and existing
strategies in the knowledge base to propose modifications or new strategy ideas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog
from langchain_core.messages import HumanMessage, SystemMessage

if TYPE_CHECKING:
    from quant_trading_system.config import Settings
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

logger = structlog.get_logger(__name__)

RESEARCH_PROMPT = """You are a quantitative strategy researcher for an automated trading system.

## Current Market Data (recent daily bars)
{market_summary}

## Existing Strategies in Knowledge Base
{existing_strategies}

## Task
Analyze the current market conditions and existing strategies. Propose up to 3 strategy modifications or new strategy ideas that could improve performance.

For each proposed strategy, provide:
1. A clear name and description
2. Whether it is a modification of an existing strategy or a new idea
3. Entry and exit rules
4. Recommended indicators and parameters
5. Expected market regime where it would perform best
6. Risk management guidelines

Respond in JSON format as a list:
[
  {{
    "name": "...",
    "type": "modification|new",
    "base_strategy_id": "...(if modification, else null)",
    "description": "...",
    "entry_rules": ["..."],
    "exit_rules": ["..."],
    "indicators": ["..."],
    "parameters": {{}},
    "market_regime": ["bull|bear|sideways|volatile"],
    "risk_management": {{"max_position_pct": 0.1, "stop_loss_pct": 0.03}},
    "reasoning": "..."
  }}
]
"""


class StrategyResearchAgent:
    """Discovers and proposes new trading strategies.

    Uses Claude to analyze recent market data and existing strategies
    in the knowledge base, then proposes modifications or new ideas.
    """

    def __init__(
        self,
        settings: Settings,
        market_data: MarketDataService,
        knowledge_base: KnowledgeBaseClient,
    ) -> None:
        self._settings = settings
        self._market_data = market_data
        self._knowledge_base = knowledge_base
        from quant_trading_system.llm_factory import create_llm

        self._llm = create_llm(settings, model_name=settings.ANALYSIS_MODEL, max_tokens=4096)
        self._log = logger.bind(agent="strategy_research")

    def research_cycle(self) -> list[dict]:
        """Run a full research cycle to propose new or modified strategies.

        Steps:
            1. Fetch recent market data for the default watchlist.
            2. Search existing strategies in the knowledge base.
            3. Use Claude to propose modifications or new strategy ideas.
            4. Return a list of proposed strategies as dicts.

        Returns:
            List of proposed strategy dicts.
        """
        self._log.info("research_cycle_start")

        # Step 1: Fetch recent market data for watchlist
        market_summary = self._fetch_market_summary()

        # Step 2: Search existing strategies in KB
        existing_strategies = self._fetch_existing_strategies()

        # Step 3: Use Claude to propose strategies
        proposals = self._generate_proposals(market_summary, existing_strategies)

        self._log.info("research_cycle_complete", proposals_count=len(proposals))
        return proposals

    def _fetch_market_summary(self) -> str:
        """Fetch recent market data and build a summary string."""
        watchlist = self._settings.watchlist
        summaries = []

        for symbol in watchlist[:10]:
            try:
                df = self._market_data.get_bars(symbol, "1Day")
                if df.empty:
                    continue

                latest = df.iloc[-1]
                # Compute basic stats over recent period
                recent = df.tail(20)
                summary = (
                    f"{symbol}: Close={latest['Close']:.2f}, "
                    f"20d_high={recent['High'].max():.2f}, "
                    f"20d_low={recent['Low'].min():.2f}, "
                    f"20d_avg_vol={recent['Volume'].mean():.0f}, "
                    f"20d_return={((latest['Close'] / recent.iloc[0]['Close']) - 1) * 100:.1f}%"
                )
                summaries.append(summary)
            except Exception as e:
                self._log.warning("market_data_fetch_failed", symbol=symbol, error=str(e))

        return "\n".join(summaries) if summaries else "No market data available."

    def _fetch_existing_strategies(self) -> str:
        """Fetch all existing strategies from the knowledge base."""
        try:
            strategies = self._knowledge_base.get_all_strategies()
            if not strategies:
                return "No existing strategies in knowledge base."

            summaries = []
            for s in strategies[:20]:  # Limit to 20 strategies
                content_preview = s.get("content", "")[:300]
                metadata = s.get("metadata", {})
                summaries.append(
                    f"- ID: {s['id']}, Name: {metadata.get('name', 'unknown')}, "
                    f"Type: {metadata.get('type', 'unknown')}, "
                    f"Status: {metadata.get('status', 'unknown')}\n"
                    f"  {content_preview}..."
                )
            return "\n".join(summaries)
        except Exception as e:
            self._log.error("kb_fetch_failed", error=str(e))
            return "Error fetching existing strategies."

    def _generate_proposals(self, market_summary: str, existing_strategies: str) -> list[dict]:
        """Use Claude to generate strategy proposals."""
        try:
            prompt = RESEARCH_PROMPT.format(
                market_summary=market_summary,
                existing_strategies=existing_strategies,
            )

            response = self._llm.invoke([
                SystemMessage(
                    content=(
                        "You are a quantitative strategy researcher. "
                        "Respond only in valid JSON as a list of strategy proposals."
                    )
                ),
                HumanMessage(content=prompt),
            ])

            # Parse the response
            import json

            content = response.content.strip()
            # Handle markdown code blocks if present
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])

            proposals = json.loads(content)

            if not isinstance(proposals, list):
                self._log.warning("proposals_not_list", type=type(proposals).__name__)
                return []

            self._log.info("proposals_generated", count=len(proposals))
            return proposals

        except json.JSONDecodeError as e:
            self._log.error("proposals_json_parse_failed", error=str(e))
            return []
        except Exception as e:
            self._log.error("proposals_generation_failed", error=str(e))
            return []
