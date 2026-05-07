"""Application configuration via Pydantic Settings with safe defaults.

Safety invariant: ALPACA_PAPER can only be False when both
REAL_MONEY_ENABLED and REAL_MONEY_CONFIRMATION are True.
"""

from __future__ import annotations

from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the harness."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Anthropic (the only LLM provider for the harness) ---
    ANTHROPIC_API_KEY: str = ""
    SUPERVISOR_MODEL: str = "claude-sonnet-4-6"

    # --- Alpaca ---
    ALPACA_API_KEY: str = ""
    ALPACA_SECRET_KEY: str = ""
    ALPACA_PAPER: bool = True

    # --- Safety Gate ---
    REAL_MONEY_ENABLED: bool = False
    REAL_MONEY_CONFIRMATION: bool = False

    # --- Portfolio ---
    PAPER_PORTFOLIO_SIZE: float = 100_000.0

    # --- Risk Limits ---
    MAX_POSITION_SIZE_PCT: float = 0.10
    MAX_SECTOR_CONCENTRATION_PCT: float = 0.25
    MAX_DRAWDOWN_PAUSE_PCT: float = 0.15
    MAX_DAILY_LOSS_PCT: float = 0.02
    MAX_CONCURRENT_POSITIONS: int = 20
    RESTRICTED_SYMBOLS: str = ""

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

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "console"

    # --- Dry Run (skip broker submission entirely) ---
    DRY_RUN: bool = False

    @model_validator(mode="after")
    def validate_safety_flags(self) -> "Settings":
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
        return (
            not self.ALPACA_PAPER
            and self.REAL_MONEY_ENABLED
            and self.REAL_MONEY_CONFIRMATION
        )
