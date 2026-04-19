"""Performance reporting for backtests using QuantStats."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import structlog

from quant_trading_system.tools.quantstats_wrapper import compute_metrics, generate_html_report

logger = structlog.get_logger(__name__)


class PerformanceReporter:
    """Generate performance reports from backtest results."""

    def __init__(self, output_dir: str = "./reports") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        backtest_result: dict,
        strategy_name: str = "strategy",
        benchmark_returns: Optional[pd.Series] = None,
    ) -> dict:
        """Generate a full performance report from a backtest result.

        Args:
            backtest_result: Dict from EquityBacktester.run_backtest().
            strategy_name: Name for the report title and filename.
            benchmark_returns: Optional benchmark returns for comparison.

        Returns:
            Dict with metrics and report file path.
        """
        returns = backtest_result.get("returns_series")
        if returns is None or returns.empty:
            logger.warning("no_returns_for_report", strategy=strategy_name)
            return {"metrics": {}, "report_path": ""}

        # Compute comprehensive metrics
        metrics = compute_metrics(returns)

        # Add backtest-specific metrics
        metrics["total_trades"] = backtest_result.get("total_trades", 0)
        metrics["initial_cash"] = backtest_result.get("initial_cash", 0)
        metrics["final_value"] = backtest_result.get("final_value", 0)

        # Generate HTML report
        report_path = generate_html_report(
            returns=returns,
            benchmark=benchmark_returns,
            output_path=str(self._output_dir / f"{strategy_name}_report.html"),
            title=f"Backtest Report: {strategy_name}",
        )

        logger.info(
            "performance_report_generated",
            strategy=strategy_name,
            sharpe=metrics["sharpe"],
            total_return=metrics["total_return"],
        )

        return {
            "metrics": metrics,
            "report_path": report_path,
        }

    def compare_strategies(
        self,
        results: dict[str, dict],
    ) -> pd.DataFrame:
        """Compare multiple backtest results side-by-side.

        Args:
            results: Dict mapping strategy_name -> backtest_result.

        Returns:
            DataFrame with strategies as rows and metrics as columns.
        """
        comparison = {}
        for name, result in results.items():
            returns = result.get("returns_series")
            if returns is not None and not returns.empty:
                metrics = compute_metrics(returns)
                metrics["total_trades"] = result.get("total_trades", 0)
                comparison[name] = metrics

        df = pd.DataFrame(comparison).T
        df = df.sort_values("sharpe", ascending=False)

        logger.info("strategy_comparison", strategies=len(df))
        return df

    def meets_promotion_criteria(
        self,
        backtest_result: dict,
        min_sharpe: float = 1.0,
        max_drawdown: float = 0.20,
        min_trades: int = 100,
    ) -> dict:
        """Check if a strategy meets promotion criteria.

        Returns:
            Dict with 'promoted' bool and reasons.
        """
        returns = backtest_result.get("returns_series")
        if returns is None or returns.empty:
            return {"promoted": False, "reasons": ["No returns data"]}

        metrics = compute_metrics(returns)
        total_trades = backtest_result.get("total_trades", 0)

        reasons = []
        passed = True

        if metrics["sharpe"] < min_sharpe:
            reasons.append(f"Sharpe {metrics['sharpe']:.2f} < {min_sharpe}")
            passed = False
        else:
            reasons.append(f"Sharpe {metrics['sharpe']:.2f} >= {min_sharpe} [PASS]")

        if abs(metrics["max_drawdown"]) > max_drawdown:
            reasons.append(f"Max drawdown {metrics['max_drawdown']:.2%} > {max_drawdown:.2%}")
            passed = False
        else:
            reasons.append(f"Max drawdown {metrics['max_drawdown']:.2%} <= {max_drawdown:.2%} [PASS]")

        if total_trades < min_trades:
            reasons.append(f"Total trades {total_trades} < {min_trades}")
            passed = False
        else:
            reasons.append(f"Total trades {total_trades} >= {min_trades} [PASS]")

        return {"promoted": passed, "reasons": reasons, "metrics": metrics}
