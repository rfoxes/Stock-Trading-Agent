"""Risk assessment model for portfolio-level risk evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RiskAssessment(BaseModel):
    """Portfolio-level risk assessment produced by the RiskManagerAgent."""

    approved: bool
    reason: str
    portfolio_beta: float = Field(default=1.0, description="Weighted portfolio beta estimate")
    sector_exposures: dict[str, float] = Field(
        default_factory=dict,
        description="Percentage of equity in each sector",
    )
    max_position_correlation: float = Field(
        default=0.0,
        description="Highest estimated pairwise correlation among held positions",
    )
    recommendation: str = Field(
        default="",
        description="Human-readable risk recommendation",
    )
