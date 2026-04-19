"""LLM factory — creates the right chat model based on configuration.

Supports:
- anthropic: ChatAnthropic (Claude) — requires ANTHROPIC_API_KEY
- ollama: ChatOllama (local, free) — requires Ollama running locally
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from langchain_core.language_models.chat_models import BaseChatModel

    from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)


def create_llm(
    settings: Settings,
    model_name: str | None = None,
    max_tokens: int = 1024,
) -> BaseChatModel:
    """Create a chat model based on the configured LLM provider.

    Args:
        settings: Application settings.
        model_name: Model name override. If None, uses ANALYSIS_MODEL from settings.
        max_tokens: Maximum tokens for the response.

    Returns:
        A LangChain chat model (ChatAnthropic, ChatOllama, etc.)
    """
    provider = settings.LLM_PROVIDER.lower()
    model = model_name or settings.ANALYSIS_MODEL

    if provider == "ollama":
        return _create_ollama(model, settings, max_tokens)
    elif provider == "anthropic":
        return _create_anthropic(model, settings, max_tokens)
    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER: {provider}. Supported: 'anthropic', 'ollama'"
        )


def _create_anthropic(
    model: str, settings: Settings, max_tokens: int
) -> BaseChatModel:
    from langchain_anthropic import ChatAnthropic

    logger.debug("creating_anthropic_llm", model=model)
    return ChatAnthropic(
        model=model,
        api_key=settings.ANTHROPIC_API_KEY,
        max_tokens=max_tokens,
    )


def _create_ollama(
    model: str, settings: Settings, max_tokens: int
) -> BaseChatModel:
    from langchain_ollama import ChatOllama

    # Map Claude model names to Ollama equivalents if the user hasn't overridden
    ollama_model = settings.OLLAMA_MODEL or _map_to_ollama_model(model)

    logger.debug("creating_ollama_llm", model=ollama_model, base_url=settings.OLLAMA_BASE_URL)
    return ChatOllama(
        model=ollama_model,
        base_url=settings.OLLAMA_BASE_URL,
        num_predict=max_tokens,
    )


def _map_to_ollama_model(claude_model: str) -> str:
    """Map Claude model names to reasonable Ollama defaults."""
    lower = claude_model.lower()
    if "haiku" in lower:
        return "llama3.2"  # Fast, small — similar role to Haiku
    elif "sonnet" in lower:
        return "llama3.1"  # Capable — similar role to Sonnet
    elif "opus" in lower:
        return "llama3.1:70b"
    else:
        return "llama3.1"  # Default
