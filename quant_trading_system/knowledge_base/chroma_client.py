"""ChromaDB client for the strategy knowledge base."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import structlog

if TYPE_CHECKING:
    import chromadb

    from quant_trading_system.config import Settings
    from quant_trading_system.models.strategy import Conclusion, Strategy

logger = structlog.get_logger(__name__)


class KnowledgeBaseClient:
    """Interface to ChromaDB for strategy and conclusion storage.

    Collections:
    - strategies: One document per strategy with metadata for filtering.
    - conclusions: One document per conclusion event (backtest, trade, etc.).
    """

    def __init__(self, settings: Settings) -> None:
        import chromadb

        self._client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self._strategies = self._client.get_or_create_collection(
            name="strategies",
            metadata={"hnsw:space": "cosine"},
        )
        self._conclusions = self._client.get_or_create_collection(
            name="conclusions",
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "knowledge_base_initialized",
            persist_dir=settings.CHROMA_PERSIST_DIR,
            strategies_count=self._strategies.count(),
            conclusions_count=self._conclusions.count(),
        )

    @property
    def strategies_collection(self):
        return self._strategies

    @property
    def conclusions_collection(self):
        return self._conclusions

    def add_strategy(self, strategy: Strategy) -> None:
        """Add or update a strategy in ChromaDB."""
        metadata = {
            "type": strategy.type.value,
            "status": strategy.status.value,
            "name": strategy.name,
        }
        # ChromaDB metadata values must be str, int, float, or bool
        if strategy.timeframes:
            metadata["timeframes"] = ",".join(strategy.timeframes)
        if strategy.indicators:
            metadata["indicators"] = ",".join(strategy.indicators)
        if strategy.market_regime:
            metadata["market_regime"] = ",".join(strategy.market_regime)

        self._strategies.upsert(
            ids=[strategy.id],
            documents=[strategy.content],
            metadatas=[metadata],
        )
        logger.debug("strategy_added", strategy_id=strategy.id, name=strategy.name)

    def get_strategy(self, strategy_id: str) -> Optional[dict]:
        """Get a strategy by ID."""
        result = self._strategies.get(ids=[strategy_id])
        if result["ids"]:
            return {
                "id": result["ids"][0],
                "content": result["documents"][0] if result["documents"] else "",
                "metadata": result["metadatas"][0] if result["metadatas"] else {},
            }
        return None

    def search_strategies(
        self,
        query: str,
        n_results: int = 5,
        strategy_type: Optional[str] = None,
        timeframe: Optional[str] = None,
    ) -> list[dict]:
        """Semantic search for strategies matching a query."""
        where_filter = {}
        if strategy_type:
            where_filter["type"] = strategy_type
        # ChromaDB doesn't support substring matching on metadata easily,
        # so we rely on semantic search for timeframe matching

        kwargs = {"query_texts": [query], "n_results": n_results}
        if where_filter:
            kwargs["where"] = where_filter

        results = self._strategies.query(**kwargs)

        strategies = []
        for i in range(len(results["ids"][0])):
            strategies.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i] if results["documents"] else "",
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
            })

        logger.debug(
            "strategy_search",
            query=query,
            results_count=len(strategies),
        )
        return strategies

    def add_conclusion(self, conclusion: Conclusion) -> None:
        """Store a conclusion in ChromaDB."""
        import uuid

        conclusion_id = conclusion.id or str(uuid.uuid4())
        metadata = {
            "conclusion_type": conclusion.conclusion_type.value,
            "strategy_id": conclusion.strategy_id,
            "recommendation": conclusion.recommendation.value,
            "timestamp": conclusion.timestamp.isoformat(),
        }
        if conclusion.agent_id:
            metadata["agent_id"] = conclusion.agent_id
        if conclusion.ticker:
            metadata["ticker"] = conclusion.ticker
        if conclusion.metrics:
            for key, value in conclusion.metrics.items():
                if isinstance(value, (int, float, str, bool)):
                    metadata[f"metric_{key}"] = value

        self._conclusions.upsert(
            ids=[conclusion_id],
            documents=[conclusion.content_for_embedding],
            metadatas=[metadata],
        )
        logger.info(
            "conclusion_added",
            conclusion_id=conclusion_id,
            strategy_id=conclusion.strategy_id,
            recommendation=conclusion.recommendation.value,
        )

    def search_conclusions(
        self,
        query: str,
        n_results: int = 10,
        strategy_id: Optional[str] = None,
    ) -> list[dict]:
        """Search conclusions by semantic similarity."""
        kwargs = {"query_texts": [query], "n_results": n_results}
        if strategy_id:
            kwargs["where"] = {"strategy_id": strategy_id}

        results = self._conclusions.query(**kwargs)

        conclusions = []
        for i in range(len(results["ids"][0])):
            conclusions.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i] if results["documents"] else "",
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0.0,
            })
        return conclusions

    def get_all_strategies(self) -> list[dict]:
        """Get all strategies from the collection."""
        result = self._strategies.get()
        strategies = []
        for i in range(len(result["ids"])):
            strategies.append({
                "id": result["ids"][i],
                "content": result["documents"][i] if result["documents"] else "",
                "metadata": result["metadatas"][i] if result["metadatas"] else {},
            })
        return strategies

    def delete_strategy(self, strategy_id: str) -> None:
        """Remove a strategy from the collection."""
        self._strategies.delete(ids=[strategy_id])
        logger.info("strategy_deleted", strategy_id=strategy_id)
