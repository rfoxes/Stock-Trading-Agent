"""Application configuration — stdlib + python-dotenv only.

Replaces the previous pydantic-settings implementation. The Cowork sandbox
where this runs doesn't have pydantic available, so this is a deliberate
zero-pip-dep version.

Safety invariant: ALPACA_PAPER can only be False when both
REAL_MONEY_ENABLED and REAL_MONEY_CONFIRMATION are True.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

try:  # optional — used to load .env files automatically
    from dotenv import load_dotenv as _load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    _load_dotenv = None  # type: ignore


def _envbool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on", "y", "t")


def _envstr(name: str, default: str) -> str:
    val = os.environ.get(name)
    return default if val is None else val


def _envfloat(name: str, default: float) -> float:
    val = os.environ.get(name)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default


def _envint(name: str, default: int) -> int:
    val = os.environ.get(name)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


@dataclass
class Settings:
    """Central configuration for the harness.

    Construct via Settings.load() — that handles loading the .env file before
    reading values. Direct construction works too (uses os.environ as-is).
    """

    # --- Anthropic (only required for standalone mode) ---
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

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"  # console | json (json adds JSON formatter)

    # --- Dry Run ---
    DRY_RUN: bool = False

    # ------------------------------------------------------------------
    # Loader
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, env_file: str | os.PathLike | None = ".env") -> "Settings":
        """Load .env (if present) and read values from os.environ.

        After construction, runs the safety validator.
        """
        if env_file and _load_dotenv is not None:
            p = Path(env_file)
            if p.exists():
                _load_dotenv(dotenv_path=str(p), override=False)
        s = cls(
            ANTHROPIC_API_KEY=_envstr("ANTHROPIC_API_KEY", ""),
            SUPERVISOR_MODEL=_envstr("SUPERVISOR_MODEL", "claude-sonnet-4-6"),
            ALPACA_API_KEY=_envstr("ALPACA_API_KEY", ""),
            ALPACA_SECRET_KEY=_envstr("ALPACA_SECRET_KEY", ""),
            ALPACA_PAPER=_envbool("ALPACA_PAPER", True),
            REAL_MONEY_ENABLED=_envbool("REAL_MONEY_ENABLED", False),
            REAL_MONEY_CONFIRMATION=_envbool("REAL_MONEY_CONFIRMATION", False),
            PAPER_PORTFOLIO_SIZE=_envfloat("PAPER_PORTFOLIO_SIZE", 100_000.0),
            MAX_POSITION_SIZE_PCT=_envfloat("MAX_POSITION_SIZE_PCT", 0.10),
            MAX_SECTOR_CONCENTRATION_PCT=_envfloat("MAX_SECTOR_CONCENTRATION_PCT", 0.25),
            MAX_DRAWDOWN_PAUSE_PCT=_envfloat("MAX_DRAWDOWN_PAUSE_PCT", 0.15),
            MAX_DAILY_LOSS_PCT=_envfloat("MAX_DAILY_LOSS_PCT", 0.02),
            MAX_CONCURRENT_POSITIONS=_envint("MAX_CONCURRENT_POSITIONS", 20),
            RESTRICTED_SYMBOLS=_envstr("RESTRICTED_SYMBOLS", ""),
            DEFAULT_WATCHLIST=_envstr(
                "DEFAULT_WATCHLIST", "SPY,QQQ,AAPL,MSFT,GOOGL,AMZN,NVDA,META,TSLA,JPM"
            ),
            LOG_LEVEL=_envstr("LOG_LEVEL", "INFO"),
            LOG_FORMAT=_envstr("LOG_FORMAT", "console"),
            DRY_RUN=_envbool("DRY_RUN", False),
        )
        s._validate()
        return s

    def _validate(self) -> None:
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
        if self.LOG_FORMAT not in ("console", "json"):
            raise ValueError(f"LOG_FORMAT must be 'console' or 'json', got {self.LOG_FORMAT!r}")

    # ------------------------------------------------------------------
    # Compatibility shims (the old pydantic Settings supported _env_file=...)
    # ------------------------------------------------------------------

    def __init__(self, *, _env_file: str | None = None, **kwargs: Any) -> None:
        # Allow ``Settings(_env_file=".env")`` for backward compatibility, and
        # ``Settings(FOO=1)`` for direct field overrides.
        if _env_file is not None and _load_dotenv is not None:
            p = Path(_env_file)
            if p.exists():
                _load_dotenv(dotenv_path=str(p), override=False)
        # Default field values pulled from environment
        for f in fields(self):
            if f.name in kwargs:
                continue
            default = f.default if f.default is not field else None
            env = os.environ.get(f.name)
            if env is None:
                kwargs.setdefault(f.name, default)
            elif f.type == "bool" or f.type is bool:
                kwargs[f.name] = env.strip().lower() in ("1", "true", "yes", "on", "y", "t")
            elif f.type == "float" or f.type is float:
                try:
                    kwargs[f.name] = float(env)
                except ValueError:
                    kwargs[f.name] = default
            elif f.type == "int" or f.type is int:
                try:
                    kwargs[f.name] = int(env)
                except ValueError:
                    kwargs[f.name] = default
            else:
                kwargs[f.name] = env
        for f in fields(self):
            object.__setattr__(self, f.name, kwargs.get(f.name, f.default))
        self._validate()

    # ------------------------------------------------------------------
    # Convenience properties (preserved from the pydantic version)
    # ------------------------------------------------------------------

    @property
    def watchlist(self) -> list[str]:
        return [s.strip() for s in self.DEFAULT_WATCHLIST.split(",") if s.strip()]

    @property
    def restricted_symbols_list(self) -> list[str]:
        if not self.RESTRICTED_SYMBOLS:
            return []
        return [s.strip() for s in self.RESTRICTED_SYMBOLS.split(",") if s.strip()]

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
