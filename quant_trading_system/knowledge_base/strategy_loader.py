"""Load strategy documents from Markdown files and sync to ChromaDB."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import frontmatter
import structlog

from quant_trading_system.models.strategy import Strategy

if TYPE_CHECKING:
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

logger = structlog.get_logger(__name__)


class StrategyLoader:
    """Loads strategy Markdown files and syncs them to ChromaDB."""

    def __init__(self, strategies_dir: Path | None = None) -> None:
        if strategies_dir is None:
            strategies_dir = Path(__file__).parent / "strategies"
        self._strategies_dir = strategies_dir

    def load_all_strategies(self) -> list[Strategy]:
        """Read all .md files from the strategies directory tree."""
        strategies = []
        if not self._strategies_dir.exists():
            logger.warning("strategies_dir_not_found", path=str(self._strategies_dir))
            return strategies

        for md_file in sorted(self._strategies_dir.rglob("*.md")):
            try:
                strategy = self._load_strategy_file(md_file)
                strategies.append(strategy)
                logger.debug("strategy_loaded", id=strategy.id, file=str(md_file))
            except Exception as e:
                logger.error("strategy_load_failed", file=str(md_file), error=str(e))

        logger.info("strategies_loaded", count=len(strategies))
        return strategies

    def _load_strategy_file(self, filepath: Path) -> Strategy:
        """Parse a single Markdown strategy file with YAML front matter."""
        post = frontmatter.load(str(filepath))
        metadata = dict(post.metadata)
        content = post.content

        # Use filename as fallback ID
        if "id" not in metadata:
            metadata["id"] = filepath.stem

        return Strategy.from_frontmatter(metadata, content)

    def sync_to_chroma(self, client: KnowledgeBaseClient) -> int:
        """Load all strategies and sync them to ChromaDB. Returns count synced."""
        strategies = self.load_all_strategies()
        for strategy in strategies:
            client.add_strategy(strategy)
        logger.info("strategies_synced_to_chroma", count=len(strategies))
        return len(strategies)
