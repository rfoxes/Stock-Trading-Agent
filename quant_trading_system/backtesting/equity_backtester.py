"""Equity backtesting engine using VectorBT."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
import structlog

from quant_trading_system.tools.quantstats_wrapper import compute_metrics

if TYPE_CHECKING:
    from quant_trading_system.data.market_data_service import MarketDataService

logger = structlog.get_logger(__name__)


class EquityBacktester:
    """Vectorized equity backtesting using VectorBT.

    Supports walk-forward validation and multiple signal generation methods.
    """

    def __init__(self, market_data: MarketDataService | None = None) -> None:
        self._market_data = market_data

    def run_backtest(
        self,
        close: pd.Series,
        entries: pd.Series,
        exits: pd.Series,
        initial_cash: float = 100_000.0,
        commission: float = 0.001,
        slippage: float = 0.001,
        sl_stop: Optional[float] = None,
        tp_stop: Optional[float] = None,
    ) -> dict:
        """Run a vectorized backtest with VectorBT.

        Args:
            close: Price series.
            entries: Boolean series for entry signals.
            exits: Boolean series for exit signals.
            initial_cash: Starting capital.
            commission: Commission per trade (fraction).
            slippage: Slippage per trade (fraction).
            sl_stop: Stop-loss as fraction (e.g., 0.02 for 2%).
            tp_stop: Take-profit as fraction.

        Returns:
            Dictionary with performance metrics and VectorBT portfolio stats.
        """
        import vectorbt as vbt

        log = logger.bind(
            data_points=len(close),
            entry_signals=int(entries.sum()),
            exit_signals=int(exits.sum()),
        )
        log.info("backtest_start")

        # Ensure boolean dtype
        entries = entries.astype(bool)
        exits = exits.astype(bool)

        # Build portfolio
        portfolio_kwargs = {
            "close": close,
            "entries": entries,
            "exits": exits,
            "init_cash": initial_cash,
            "fees": commission,
            "slippage": slippage,
            "freq": "1D",
        }

        if sl_stop is not None:
            portfolio_kwargs["sl_stop"] = sl_stop
        if tp_stop is not None:
            portfolio_kwargs["tp_stop"] = tp_stop

        portfolio = vbt.Portfolio.from_signals(**portfolio_kwargs)

        # Extract stats
        stats = portfolio.stats()
        returns = portfolio.returns()

        # Compute additional metrics via QuantStats
        qs_metrics = compute_metrics(returns)

        result = {
            "total_return": float(stats.get("Total Return [%]", 0)) / 100,
            "sharpe": qs_metrics["sharpe"],
            "sortino": qs_metrics["sortino"],
            "calmar": qs_metrics["calmar"],
            "max_drawdown": qs_metrics["max_drawdown"],
            "annualized_return": qs_metrics["annualized_return"],
            "win_rate": qs_metrics["win_rate"],
            "profit_factor": qs_metrics["profit_factor"],
            "volatility": qs_metrics["volatility"],
            "total_trades": int(stats.get("Total Trades", 0)),
            "initial_cash": initial_cash,
            "final_value": float(stats.get("End Value", initial_cash)),
            "returns_series": returns,
            "equity_curve": portfolio.value(),
        }

        log.info(
            "backtest_complete",
            total_return=f"{result['total_return']:.2%}",
            sharpe=f"{result['sharpe']:.2f}",
            max_drawdown=f"{result['max_drawdown']:.2%}",
            total_trades=result["total_trades"],
        )

        return result

    def run_walk_forward(
        self,
        close: pd.Series,
        signal_generator,
        train_pct: float = 0.70,
        n_splits: int = 5,
        initial_cash: float = 100_000.0,
        commission: float = 0.001,
    ) -> dict:
        """Walk-forward validation with rolling train/test splits.

        Args:
            close: Full price series.
            signal_generator: Callable(close) -> (entries, exits) that generates signals.
            train_pct: Fraction of each window for training.
            n_splits: Number of walk-forward windows.
            initial_cash: Starting capital.
            commission: Commission per trade.

        Returns:
            Dictionary with in-sample and out-of-sample results.
        """
        total_len = len(close)
        window_size = total_len // n_splits
        train_size = int(window_size * train_pct)

        in_sample_results = []
        out_of_sample_results = []

        for i in range(n_splits):
            start = i * window_size
            end = min(start + window_size, total_len)
            train_end = start + train_size

            if train_end >= end:
                continue

            # In-sample
            train_close = close.iloc[start:train_end]
            entries, exits = signal_generator(train_close)
            is_result = self.run_backtest(train_close, entries, exits, initial_cash, commission)
            in_sample_results.append(is_result)

            # Out-of-sample
            test_close = close.iloc[train_end:end]
            entries, exits = signal_generator(test_close)
            oos_result = self.run_backtest(test_close, entries, exits, initial_cash, commission)
            out_of_sample_results.append(oos_result)

        # Aggregate
        def avg_metric(results: list[dict], key: str) -> float:
            values = [r[key] for r in results if isinstance(r.get(key), (int, float))]
            return float(np.mean(values)) if values else 0.0

        return {
            "n_splits": n_splits,
            "in_sample": {
                "avg_sharpe": avg_metric(in_sample_results, "sharpe"),
                "avg_return": avg_metric(in_sample_results, "total_return"),
                "avg_max_drawdown": avg_metric(in_sample_results, "max_drawdown"),
                "avg_win_rate": avg_metric(in_sample_results, "win_rate"),
                "results": in_sample_results,
            },
            "out_of_sample": {
                "avg_sharpe": avg_metric(out_of_sample_results, "sharpe"),
                "avg_return": avg_metric(out_of_sample_results, "total_return"),
                "avg_max_drawdown": avg_metric(out_of_sample_results, "max_drawdown"),
                "avg_win_rate": avg_metric(out_of_sample_results, "win_rate"),
                "results": out_of_sample_results,
            },
        }

    def backtest_sma_crossover(
        self,
        close: pd.Series,
        fast_period: int = 50,
        slow_period: int = 200,
        initial_cash: float = 100_000.0,
    ) -> dict:
        """Convenience method: backtest a simple SMA crossover strategy.

        Useful for validation — known strategy with predictable behavior.
        """
        from quant_trading_system.tools.technical_indicators import compute_sma

        sma_fast = compute_sma(close, fast_period)
        sma_slow = compute_sma(close, slow_period)

        # Entry: fast crosses above slow
        entries = (sma_fast > sma_slow) & (sma_fast.shift(1) <= sma_slow.shift(1))
        # Exit: fast crosses below slow
        exits = (sma_fast < sma_slow) & (sma_fast.shift(1) >= sma_slow.shift(1))

        # Fill NaN with False
        entries = entries.fillna(False)
        exits = exits.fillna(False)

        return self.run_backtest(close, entries, exits, initial_cash)
