"""LangGraph checkpointer factory."""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)


def create_checkpointer(settings: Settings):
    """Create a LangGraph checkpointer based on settings.

    Returns MemorySaver for development or PostgresSaver for production.
    """
    if settings.LANGGRAPH_CHECKPOINTER == "postgres":
        try:
            from langgraph.checkpoint.postgres import PostgresSaver

            checkpointer = PostgresSaver.from_conn_string(settings.DATABASE_URL)
            checkpointer.setup()
            logger.info("checkpointer_initialized", type="postgres")
            return checkpointer
        except Exception as e:
            logger.warning(
                "postgres_checkpointer_failed_falling_back_to_memory",
                error=str(e),
            )

    from langgraph.checkpoint.memory import MemorySaver

    logger.info("checkpointer_initialized", type="memory")
    return MemorySaver()
