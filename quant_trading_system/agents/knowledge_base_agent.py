"""Knowledge Base Agent — interface for other agents to query and write to the KB.

Provides a clean API for strategy queries, conclusion writing (to both ChromaDB
and markdown files), and strategy status management.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import structlog

if TYPE_CHECKING:
    from quant_trading_system.config import Settings
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient
    from quant_trading_system.models.strategy import Conclusion

logger = structlog.get_logger(__name__)

# Directory for markdown conclusion files
_CONCLUSIONS_DIR = Path(__file__).resolve().parent.parent / "knowledge_base" / "conclusions"


class KnowledgeBaseAgent:
    """Interface for other agents to query and write to the knowledge base.

    Wraps the KnowledgeBaseClient with agent-friendly methods and adds
    markdown file output for conclusions.
    """

    def __init__(self, settings: Settings, knowledge_base: KnowledgeBaseClient) -> None:
        self._settings = settings
        self._kb = knowledge_base
        self._log = logger.bind(agent="knowledge_base")

        # Ensure conclusions directory exists
        _CONCLUSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def query_strategies(
        self,
        query: str,
        strategy_type: Optional[str] = None,
        n_results: int = 5,
    ) -> list[dict]:
        """Search the knowledge base for strategies matching a query.

        Args:
            query: Natural language query describing desired strategies.
            strategy_type: Optional filter (e.g., "equity", "options").
            n_results: Maximum number of results to return.

        Returns:
            List of strategy dicts with id, content, metadata, and distance.
        """
        self._log.info("query_strategies", query=query[:100], n_results=n_results)

        try:
            results = self._kb.search_strategies(
                query=query,
                n_results=n_results,
                strategy_type=strategy_type,
            )
            self._log.info("query_strategies_complete", results_count=len(results))
            return results
        except Exception as e:
            self._log.error("query_strategies_failed", error=str(e))
            return []

    def get_strategy_conclusions(
        self,
        strategy_id: str,
        n_results: int = 10,
    ) -> list[dict]:
        """Get conclusions associated with a specific strategy.

        Args:
            strategy_id: The strategy ID to fetch conclusions for.
            n_results: Maximum number of conclusions to return.

        Returns:
            List of conclusion dicts.
        """
        self._log.info("get_strategy_conclusions", strategy_id=strategy_id)

        try:
            results = self._kb.search_conclusions(
                query=f"strategy {strategy_id}",
                n_results=n_results,
                strategy_id=strategy_id,
            )
            self._log.info(
                "get_strategy_conclusions_complete",
                strategy_id=strategy_id,
                results_count=len(results),
            )
            return results
        except Exception as e:
            self._log.error("get_strategy_conclusions_failed", error=str(e))
            return []

    def write_conclusion(self, conclusion: Conclusion) -> None:
        """Write a conclusion to both ChromaDB and a markdown file.

        Args:
            conclusion: The Conclusion model to persist.
        """
        self._log.info(
            "write_conclusion",
            strategy_id=conclusion.strategy_id,
            conclusion_type=conclusion.conclusion_type.value,
            recommendation=conclusion.recommendation.value,
        )

        # Write to ChromaDB
        try:
            self._kb.add_conclusion(conclusion)
        except Exception as e:
            self._log.error("write_conclusion_chromadb_failed", error=str(e))

        # Write to markdown file
        try:
            self._write_conclusion_markdown(conclusion)
        except Exception as e:
            self._log.error("write_conclusion_markdown_failed", error=str(e))

    def _write_conclusion_markdown(self, conclusion: Conclusion) -> None:
        """Write a conclusion as a markdown file in knowledge_base/conclusions/."""
        timestamp_str = conclusion.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp_str}_{conclusion.strategy_id}_{conclusion.conclusion_type.value}.md"
        filepath = _CONCLUSIONS_DIR / filename

        metrics_section = ""
        if conclusion.metrics:
            metrics_lines = [f"| {k} | {v} |" for k, v in conclusion.metrics.items()]
            metrics_section = (
                "\n## Metrics\n\n"
                "| Metric | Value |\n"
                "|--------|-------|\n"
                + "\n".join(metrics_lines)
            )

        modification_section = ""
        if conclusion.modification_notes:
            modification_section = f"\n## Modification Notes\n\n{conclusion.modification_notes}\n"

        content = f"""---
strategy_id: {conclusion.strategy_id}
conclusion_type: {conclusion.conclusion_type.value}
recommendation: {conclusion.recommendation.value}
agent_id: {conclusion.agent_id}
ticker: {conclusion.ticker}
timestamp: {conclusion.timestamp.isoformat()}
---

# Conclusion: {conclusion.strategy_id}

**Type:** {conclusion.conclusion_type.value}
**Recommendation:** {conclusion.recommendation.value}
**Timestamp:** {conclusion.timestamp.isoformat()}

## Summary

{conclusion.summary}
{metrics_section}
{modification_section}
"""

        filepath.write_text(content, encoding="utf-8")
        self._log.info("conclusion_markdown_written", filepath=str(filepath))

    def update_strategy_status(self, strategy_id: str, new_status: str) -> None:
        """Update the status of a strategy in the knowledge base.

        Args:
            strategy_id: The strategy to update.
            new_status: New status value (e.g., "active", "testing", "deprecated", "proposed").
        """
        self._log.info(
            "update_strategy_status",
            strategy_id=strategy_id,
            new_status=new_status,
        )

        try:
            # Fetch existing strategy
            strategy = self._kb.get_strategy(strategy_id)
            if strategy is None:
                self._log.warning("strategy_not_found", strategy_id=strategy_id)
                return

            # Update metadata with new status
            metadata = strategy.get("metadata", {})
            metadata["status"] = new_status

            # Re-upsert with updated metadata
            self._kb.strategies_collection.upsert(
                ids=[strategy_id],
                documents=[strategy.get("content", "")],
                metadatas=[metadata],
            )

            self._log.info(
                "strategy_status_updated",
                strategy_id=strategy_id,
                new_status=new_status,
            )
        except Exception as e:
            self._log.error("update_strategy_status_failed", error=str(e))
