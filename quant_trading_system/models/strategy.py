"""Strategy and conclusion data models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StrategyType(str, Enum):
    EQUITY = "equity"
    OPTIONS = "options"


class StrategyStatus(str, Enum):
    ACTIVE = "active"
    TESTING = "testing"
    DEPRECATED = "deprecated"
    PROPOSED = "proposed"


class Timeframe(str, Enum):
    INTRADAY = "intraday"
    SWING = "swing"
    POSITION = "position"


class ConclusionType(str, Enum):
    BACKTEST_RESULT = "backtest_result"
    LIVE_TRADE_RESULT = "live_trade_result"
    STRATEGY_UPDATE = "strategy_update"
    REGIME_CHANGE = "regime_change"


class Recommendation(str, Enum):
    PROMOTE = "promote"
    DEMOTE = "demote"
    RETIRE = "retire"
    MODIFY = "modify"
    WATCH = "watch"


class Strategy(BaseModel):
    """A trading strategy loaded from Markdown + YAML front matter."""

    id: str
    name: str
    type: StrategyType
    timeframes: list[str] = Field(default_factory=list)
    description: str = ""
    entry_rules: list[str] = Field(default_factory=list)
    exit_rules: list[str] = Field(default_factory=list)
    indicators: list[str] = Field(default_factory=list)
    parameters: dict = Field(default_factory=dict)
    risk_management: dict = Field(default_factory=dict)
    status: StrategyStatus = StrategyStatus.ACTIVE
    market_regime: list[str] = Field(default_factory=list)
    content: str = ""  # Full markdown content for ChromaDB embedding

    @classmethod
    def from_frontmatter(cls, metadata: dict, content: str) -> Strategy:
        """Create a Strategy from parsed YAML front matter and Markdown content."""
        timeframes = metadata.get("timeframe", metadata.get("timeframes", []))
        if isinstance(timeframes, str):
            timeframes = [timeframes]

        return cls(
            id=metadata.get("id", ""),
            name=metadata.get("name", ""),
            type=StrategyType(metadata.get("type", "equity")),
            timeframes=timeframes,
            indicators=metadata.get("indicators", []),
            parameters=metadata.get("parameters", {}),
            risk_management=metadata.get("risk_management", {}),
            market_regime=metadata.get("market_regime", []),
            status=StrategyStatus(metadata.get("status", "active")),
            content=content,
        )


class Conclusion(BaseModel):
    """A conclusion written after a backtest, trade, or analysis."""

    id: str = Field(default_factory=lambda: "")
    conclusion_type: ConclusionType
    strategy_id: str
    agent_id: str = ""
    ticker: str = ""
    summary: str
    metrics: dict = Field(default_factory=dict)
    recommendation: Recommendation
    modification_notes: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @property
    def content_for_embedding(self) -> str:
        """Generate text content for ChromaDB embedding."""
        parts = [
            f"Strategy: {self.strategy_id}",
            f"Type: {self.conclusion_type.value}",
            f"Summary: {self.summary}",
            f"Recommendation: {self.recommendation.value}",
        ]
        if self.modification_notes:
            parts.append(f"Notes: {self.modification_notes}")
        if self.metrics:
            metrics_str = ", ".join(f"{k}: {v}" for k, v in self.metrics.items())
            parts.append(f"Metrics: {metrics_str}")
        return "\n".join(parts)
