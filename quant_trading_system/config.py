"""Application configuration via Pydantic Settings with safe defaults."""

from __future__ import annotations

from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the trading system.

    Safety invariant: ALPACA_PAPER can only be False when both
    REAL_MONEY_ENABLED and REAL_MONEY_CONFIRMATION are True.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Anthropic ---
    ANTHROPIC_API_KEY: str = ""

    # --- Alpaca ---
    ALPACA_API_KEY: str = ""
    ALPACA_SECRET_KEY: str = ""
    ALPACA_PAPER: bool = True

    # --- Safety Gate ---
    REAL_MONEY_ENABLED: bool = False
    REAL_MONEY_CONFIRMATION: bool = False

    # --- Database ---
    DATABASE_URL: str = "postgresql://trading:trading@localhost:5432/trading_system"
    LANGGRAPH_CHECKPOINTER: Literal["postgres", "memory"] = "memory"

    # --- ChromaDB ---
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # --- Portfolio ---
    PAPER_PORTFOLIO_SIZE: float = 100_000.0

    # --- Risk Limits ---
    MAX_POSITION_SIZE_PCT: float = 0.10
    MAX_SECTOR_CONCENTRATION_PCT: float = 0.25
    MAX_DRAWDOWN_PAUSE_PCT: float = 0.15
    MAX_DAILY_LOSS_PCT: float = 0.02
    MAX_CONCURRENT_POSITIONS: int = 20
    RESTRICTED_SYMBOLS: str = ""

    # --- LLM Provider ---
    # "anthropic" for Claude (paid, requires ANTHROPIC_API_KEY)
    # "ollama" for local models (free, requires Ollama running)
    LLM_PROVIDER: str = "anthropic"

    # --- Ollama (only used when LLM_PROVIDER=ollama) ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = ""  # Override auto-mapping (e.g. "llama3.1", "mistral", "qwen2.5")

    # --- Agent Model Allocation ---
    SUPERVISOR_MODEL: str = "claude-sonnet-4-5-20250514"
    ANALYSIS_MODEL: str = "claude-sonnet-4-5-20250514"
    ROUTING_MODEL: str = "claude-haiku-4-5-20251001"
    EXECUTION_MODEL: str = "claude-haiku-4-5-20251001"

    # --- Watchlist ---
    DEFAULT_WATCHLIST: str = "SPY,QQQ,AAPL,MSFT,GOOGL,AMZN,NVDA,META,TSLA,JPM"

    @property
    def watchlist(self) -> list[str]:
        return [s.strip() for s in self.DEFAULT_WATCHLIST.split(",") if s.strip()]

    @property
    def restricted_symbols_list(self) -> list[str]:
        if not self.RESTRICTED_SYMBOLS:
            return []
        return [s.strip() for s in self.RESTRICTED_SYMBOLS.split(",") if s.strip()]

    # --- Scheduling ---
    INTRADAY_INTERVAL_MINUTES: int = 5
    SWING_REBALANCE_TIME: str = "15:50"
    POSITION_REBALANCE_DAY: str = "friday"
    STRATEGY_RESEARCH_INTERVAL_DAYS: int = 7

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "console"

    # --- Dry Run ---
    DRY_RUN: bool = False

    @model_validator(mode="after")
    def validate_safety_flags(self) -> Settings:
        """Ensure live trading cannot be enabled without both safety flags."""
        if not self.ALPACA_PAPER:
            if not self.REAL_MONEY_ENABLED:
                raise ValueError(
                    "ALPACA_PAPER=false requires REAL_MONEY_ENABLED=true. "
                    "Live trading is disabled for safety."
                )
            if not self.REAL_MONEY_CONFIRMATION:
                raise ValueError(
                    "ALPACA_PAPER=false requires REAL_MONEY_CONFIRMATION=true. "
                    "Live trading is disabled for safety."
                )
        return self

    @property
    def is_paper_trading(self) -> bool:
        return self.ALPACA_PAPER

    @property
    def is_live_trading(self) -> bool:
        return not self.ALPACA_PAPER and self.REAL_MONEY_ENABLED and self.REAL_MONEY_CONFIRMATION
