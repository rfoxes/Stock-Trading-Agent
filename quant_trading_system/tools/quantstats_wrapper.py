"""Thin wrapper around QuantStats for performance metrics and reports."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import structlog

logger = structlog.get_logger(__name__)


def compute_metrics(returns: pd.Series) -> dict:
    """Compute all key performance metrics from a returns series.

    Args:
        returns: Daily returns series (not cumulative).

    Returns:
        Dictionary of performance metrics.
    """
    import quantstats as qs

    if returns.empty or len(returns) < 2:
        return {
            "sharpe": 0.0,
            "sortino": 0.0,
            "calmar": 0.0,
            "max_drawdown": 0.0,
            "total_return": 0.0,
            "annualized_return": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "volatility": 0.0,
        }

    # Clean returns
    returns = returns.dropna()

    try:
        sharpe = qs.stats.sharpe(returns)
        sortino = qs.stats.sortino(returns)
        calmar = qs.stats.calmar(returns)
        max_dd = qs.stats.max_drawdown(returns)
        total_ret = qs.stats.comp(returns)
        annual_ret = qs.stats.cagr(returns)
        win_rate = qs.stats.win_rate(returns)
        profit_factor = qs.stats.profit_factor(returns)
        volatility = qs.stats.volatility(returns)
    except Exception as e:
        logger.warning("quantstats_metric_error", error=str(e))
        return {
            "sharpe": 0.0,
            "sortino": 0.0,
            "calmar": 0.0,
            "max_drawdown": 0.0,
            "total_return": float(returns.sum()),
            "annualized_return": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "volatility": 0.0,
        }

    return {
        "sharpe": float(sharpe) if pd.notna(sharpe) else 0.0,
        "sortino": float(sortino) if pd.notna(sortino) else 0.0,
        "calmar": float(calmar) if pd.notna(calmar) else 0.0,
        "max_drawdown": float(max_dd) if pd.notna(max_dd) else 0.0,
        "total_return": float(total_ret) if pd.notna(total_ret) else 0.0,
        "annualized_return": float(annual_ret) if pd.notna(annual_ret) else 0.0,
        "win_rate": float(win_rate) if pd.notna(win_rate) else 0.0,
        "profit_factor": float(profit_factor) if pd.notna(profit_factor) else 0.0,
        "volatility": float(volatility) if pd.notna(volatility) else 0.0,
    }


def generate_html_report(
    returns: pd.Series,
    benchmark: Optional[pd.Series] = None,
    output_path: str = "backtest_report.html",
    title: str = "Backtest Report",
) -> str:
    """Generate a QuantStats HTML tearsheet.

    Returns the output file path.
    """
    import quantstats as qs

    if returns.empty:
        logger.warning("empty_returns_no_report")
        return ""

    try:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        qs.reports.html(
            returns,
            benchmark=benchmark,
            output=str(output),
            title=title,
        )
        logger.info("report_generated", path=str(output))
        return str(output)

    except Exception as e:
        logger.error("report_generation_failed", error=str(e))
        return ""
