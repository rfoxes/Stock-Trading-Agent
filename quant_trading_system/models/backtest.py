"""Backtest result data models."""

from __future__ import annotations

from typing import Any

import pandas as pd
from pydantic import BaseModel, Field


class BacktestResult(BaseModel):
    """Summary of a completed backtest run.

    Attributes:
        total_return: Total return as a fraction (e.g. 0.12 = 12%).
        sharpe: Annualized Sharpe ratio.
        max_drawdown: Maximum drawdown as a positive fraction.
        daily_pnl: Daily P&L series indexed by date.
    """

    model_config = {"arbitrary_types_allowed": True}

    total_return: float = 0.0
    sharpe: float = 0.0
    max_drawdown: float = 0.0
    daily_pnl: Any = Field(default_factory=lambda: pd.Series(dtype=float))
