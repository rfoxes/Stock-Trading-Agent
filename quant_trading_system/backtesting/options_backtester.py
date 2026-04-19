"""Options backtesting engine with daily mark-to-market via QuantLib.

Replays historical price data for a multi-leg options position, re-pricing
each leg daily using Black-Scholes (updating spot, vol, and time-to-expiry),
and produces a ``BacktestResult`` summary with P&L series and risk metrics.
"""

from __future__ import annotations

import math
from datetime import date, timedelta
from typing import Optional

import numpy as np
import pandas as pd
import structlog

from quant_trading_system.config import Settings
from quant_trading_system.data.options_data import OptionLeg
from quant_trading_system.models.backtest import BacktestResult

logger = structlog.get_logger(__name__)

# Contract multiplier (standard US equity options)
_CONTRACT_MULTIPLIER = 100

# Default risk-free rate
_DEFAULT_RATE = 0.05


class OptionsBacktester:
    """Backtest a multi-leg options position against historical data.

    The backtester:
    1. Fetches daily underlying prices via yfinance.
    2. Computes rolling realized vol to estimate IV each day.
    3. Re-prices each leg daily with QuantLib Black-Scholes.
    4. Handles expiration (ITM assignment vs worthless expiry).
    5. Produces a ``BacktestResult`` with P&L, Sharpe, and drawdown.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self._settings = settings
        self._rate = _DEFAULT_RATE

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_backtest(
        self,
        legs: list[OptionLeg],
        underlying: str,
        start_date: date,
        end_date: date,
        initial_cash: float = 100_000.0,
    ) -> BacktestResult:
        """Run a historical backtest for an options position.

        Args:
            legs: Option legs that make up the position.
            underlying: Underlying ticker symbol.
            start_date: Backtest start date.
            end_date: Backtest end date.
            initial_cash: Starting cash balance.

        Returns:
            ``BacktestResult`` with performance metrics and daily P&L.
        """
        from quant_trading_system.tools.options_math import black_scholes_price

        # --- Fetch historical data ---
        prices = self._fetch_underlying_prices(underlying, start_date, end_date)
        if prices.empty:
            logger.error("no_price_data", underlying=underlying)
            return self._empty_result(initial_cash)

        # --- Compute rolling vol (21-day window, annualized) ---
        log_returns = np.log(prices / prices.shift(1)).dropna()
        rolling_vol = log_returns.rolling(window=21, min_periods=5).std() * np.sqrt(252)
        rolling_vol = rolling_vol.fillna(method="bfill").fillna(0.20)

        # --- Determine entry prices for each leg ---
        first_date = prices.index[0]
        first_spot = float(prices.iloc[0])
        first_vol = float(rolling_vol.iloc[0]) if not rolling_vol.empty else 0.20

        entry_prices: dict[int, float] = {}
        for i, leg in enumerate(legs):
            tte = self._time_to_expiry(first_date, leg.expiration)
            if tte <= 0:
                entry_prices[i] = max(0.0, self._intrinsic(first_spot, leg))
            else:
                entry_prices[i] = black_scholes_price(
                    spot=first_spot,
                    strike=leg.strike,
                    rate=self._rate,
                    vol=first_vol,
                    time_to_expiry_years=tte,
                    option_type=leg.option_type,
                )

        # Initial cost / credit
        initial_position_value = 0.0
        for i, leg in enumerate(legs):
            sign = -1.0 if leg.side == "buy" else 1.0  # buy = cash outflow
            initial_position_value += sign * entry_prices[i] * leg.qty * _CONTRACT_MULTIPLIER

        cash = initial_cash + initial_position_value  # credit adds, debit subtracts

        # --- Daily mark-to-market ---
        daily_pnl_records: list[tuple[date, float]] = []
        portfolio_values: list[float] = [initial_cash]

        for idx in range(len(prices)):
            current_date = prices.index[idx]
            if hasattr(current_date, "date"):
                current_date_d = current_date.date()
            else:
                current_date_d = current_date
            spot = float(prices.iloc[idx])
            vol = float(rolling_vol.iloc[idx]) if idx < len(rolling_vol) else 0.20

            # Price each leg
            position_mtm = 0.0
            for i, leg in enumerate(legs):
                tte = self._time_to_expiry(current_date_d, leg.expiration)

                if tte <= 0:
                    # Expired — settle at intrinsic value
                    leg_price = max(0.0, self._intrinsic(spot, leg))
                elif tte < 1 / 365:
                    # Very close to expiry — use intrinsic as floor
                    leg_price = max(
                        self._intrinsic(spot, leg),
                        black_scholes_price(
                            spot=spot,
                            strike=leg.strike,
                            rate=self._rate,
                            vol=vol,
                            time_to_expiry_years=max(tte, 1e-6),
                            option_type=leg.option_type,
                        ),
                    )
                else:
                    leg_price = black_scholes_price(
                        spot=spot,
                        strike=leg.strike,
                        rate=self._rate,
                        vol=vol,
                        time_to_expiry_years=tte,
                        option_type=leg.option_type,
                    )

                # Long legs have positive MTM, short legs negative
                sign = 1.0 if leg.side == "buy" else -1.0
                position_mtm += sign * leg_price * leg.qty * _CONTRACT_MULTIPLIER

            total_value = cash + position_mtm
            daily_change = total_value - portfolio_values[-1]
            daily_pnl_records.append((current_date_d, daily_change))
            portfolio_values.append(total_value)

        # --- Build P&L series ---
        if daily_pnl_records:
            pnl_index, pnl_values = zip(*daily_pnl_records)
            daily_pnl = pd.Series(pnl_values, index=pd.DatetimeIndex(pnl_index), name="daily_pnl")
        else:
            daily_pnl = pd.Series(dtype=float, name="daily_pnl")

        # --- Compute metrics ---
        total_return = (portfolio_values[-1] - initial_cash) / initial_cash if initial_cash else 0.0
        sharpe = self._sharpe_ratio(daily_pnl)
        max_dd = self._max_drawdown(portfolio_values)

        return BacktestResult(
            total_return=total_return,
            sharpe=sharpe,
            max_drawdown=max_dd,
            daily_pnl=daily_pnl,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _time_to_expiry(current: date, expiration: date) -> float:
        """Time to expiry in years (Actual/365)."""
        delta = (expiration - current).days
        return max(delta / 365.0, 0.0)

    @staticmethod
    def _intrinsic(spot: float, leg: OptionLeg) -> float:
        """Intrinsic value of a single option contract (per share)."""
        if leg.option_type == "call":
            return max(spot - leg.strike, 0.0)
        else:
            return max(leg.strike - spot, 0.0)

    @staticmethod
    def _fetch_underlying_prices(symbol: str, start: date, end: date) -> pd.Series:
        """Fetch daily close prices via yfinance."""
        try:
            import yfinance as yf

            ticker = yf.Ticker(symbol)
            hist = ticker.history(
                start=start.isoformat(),
                end=(end + timedelta(days=1)).isoformat(),
            )
            if hist.empty:
                return pd.Series(dtype=float)
            return hist["Close"]
        except Exception as exc:
            logger.warning("price_fetch_failed", symbol=symbol, error=str(exc))
            return pd.Series(dtype=float)

    @staticmethod
    def _sharpe_ratio(daily_pnl: pd.Series, risk_free_daily: float = 0.0) -> float:
        """Annualized Sharpe ratio from a daily P&L series."""
        if daily_pnl.empty or daily_pnl.std() == 0:
            return 0.0
        excess = daily_pnl.mean() - risk_free_daily
        return float(excess / daily_pnl.std() * math.sqrt(252))

    @staticmethod
    def _max_drawdown(portfolio_values: list[float]) -> float:
        """Maximum drawdown as a positive fraction (e.g. 0.15 = 15%)."""
        if len(portfolio_values) < 2:
            return 0.0
        peak = portfolio_values[0]
        max_dd = 0.0
        for val in portfolio_values[1:]:
            if val > peak:
                peak = val
            dd = (peak - val) / peak if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd
        return max_dd

    def _empty_result(self, initial_cash: float) -> BacktestResult:
        """Return a zero-valued result when backtesting cannot proceed."""
        return BacktestResult(
            total_return=0.0,
            sharpe=0.0,
            max_drawdown=0.0,
            daily_pnl=pd.Series(dtype=float, name="daily_pnl"),
        )
