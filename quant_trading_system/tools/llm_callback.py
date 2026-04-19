"""Custom LangChain callback handler for structured LLM logging."""

from __future__ import annotations

import time
from typing import Any
from uuid import UUID

import structlog
from langchain_core.callbacks import BaseCallbackHandler

logger = structlog.get_logger("llm")


class LLMLoggingCallback(BaseCallbackHandler):
    """Logs token usage, latency, and model info for every LLM invocation."""

    def __init__(self) -> None:
        self._start_times: dict[UUID, float] = {}

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        self._start_times[run_id] = time.time()
        model = serialized.get("kwargs", {}).get("model", "unknown")
        logger.debug(
            "llm_call_start",
            run_id=str(run_id),
            model=model,
            prompt_count=len(prompts),
        )

    def on_llm_end(
        self,
        response: Any,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        elapsed = time.time() - self._start_times.pop(run_id, time.time())

        # Extract token usage if available
        usage = {}
        if hasattr(response, "llm_output") and response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})
            usage = {
                "prompt_tokens": token_usage.get("prompt_tokens", 0),
                "completion_tokens": token_usage.get("completion_tokens", 0),
                "total_tokens": token_usage.get("total_tokens", 0),
            }

        logger.info(
            "llm_call_end",
            run_id=str(run_id),
            latency_ms=round(elapsed * 1000, 2),
            **usage,
        )

    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        **kwargs: Any,
    ) -> None:
        elapsed = time.time() - self._start_times.pop(run_id, time.time())
        logger.error(
            "llm_call_error",
            run_id=str(run_id),
            latency_ms=round(elapsed * 1000, 2),
            error=str(error),
        )
