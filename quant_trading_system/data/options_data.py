"""Options data service for fetching chains, historical IV, and IV rank.

Provides the ``OptionLeg`` model for describing multi-leg option positions
and an ``OptionsDataService`` that pulls data from yfinance with graceful
fallback when data is unavailable.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Literal, Optional

import numpy as np
import pandas as pd
import structlog
from pydantic import BaseModel, Field

from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class OptionLeg(BaseModel):
    """A single leg of an options position.

    Attributes:
        symbol: Underlying ticker symbol (e.g. ``"AAPL"``).
        strike: Strike price.
        expiration: Expiration date.
        option_type: ``"call"`` or ``"put"``.
        side: ``"buy"`` (long) or ``"sell"`` (short / written).
        qty: Number of contracts.
    """

    symbol: str
    strike: float
    expiration: date
    option_type: Literal["call", "put"]
    side: Literal["buy", "sell"]
    qty: int = Field(default=1, ge=1)


# ---------------------------------------------------------------------------
# Options data service
# ---------------------------------------------------------------------------

class OptionsDataService:
    """Fetch options chains, compute historical IV proxies, and IV rank."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self._settings = settings

    # ----- Options chain -----

    def get_options_chain(
        self,
        symbol: str,
        expiration_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """Get an options chain for *symbol* at a given expiration.

        Attempts ``yfinance`` first.  If *expiration_date* is ``None``, the
        nearest available expiration is used.

        Returns:
            DataFrame with columns including ``strike``, ``lastPrice``,
            ``bid``, ``ask``, ``volume``, ``openInterest``,
            ``impliedVolatility``, and ``option_type`` (``"call"``/``"put"``).
            Returns an empty DataFrame on failure.
        """
        try:
            return self._chain_yfinance(symbol, expiration_date)
        except Exception as exc:
            logger.warning(
                "options_chain_fetch_failed",
                symbol=symbol,
                expiration=str(expiration_date),
                error=str(exc),
            )
            return pd.DataFrame()

    def _chain_yfinance(
        self, symbol: str, expiration_date: Optional[date]
    ) -> pd.DataFrame:
        import yfinance as yf

        ticker = yf.Ticker(symbol)
        available_expirations = ticker.options  # tuple of date strings

        if not available_expirations:
            logger.warning("no_options_expirations", symbol=symbol)
            return pd.DataFrame()

        # Select the requested expiration or the nearest available one
        if expiration_date is not None:
            exp_str = expiration_date.isoformat()
            if exp_str not in available_expirations:
                # Pick the closest available expiration
                exp_dates = [datetime.strptime(e, "%Y-%m-%d").date() for e in available_expirations]
                closest = min(exp_dates, key=lambda d: abs((d - expiration_date).days))
                exp_str = closest.isoformat()
                logger.info(
                    "expiration_snapped",
                    requested=expiration_date.isoformat(),
                    used=exp_str,
                    symbol=symbol,
                )
        else:
            exp_str = available_expirations[0]

        chain = ticker.option_chain(exp_str)

        calls = chain.calls.copy()
        calls["option_type"] = "call"
        puts = chain.puts.copy()
        puts["option_type"] = "put"

        combined = pd.concat([calls, puts], ignore_index=True)
        combined["expiration"] = exp_str
        combined["underlying"] = symbol

        logger.debug(
            "options_chain_fetched",
            symbol=symbol,
            expiration=exp_str,
            rows=len(combined),
        )
        return combined

    # ----- Historical (realized) volatility as IV proxy -----

    def get_historical_iv(
        self,
        symbol: str,
        lookback_days: int = 252,
    ) -> pd.Series:
        """Compute annualized realized volatility as an IV proxy.

        Uses close-to-close log returns over a rolling 21-day window,
        annualized by ``sqrt(252)``.

        Args:
            symbol: Underlying ticker.
            lookback_days: Number of calendar days of history to fetch.

        Returns:
            ``pd.Series`` indexed by date with annualized realized vol values.
        """
        try:
            import yfinance as yf

            end = datetime.utcnow()
            start = end - timedelta(days=lookback_days)
            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))

            if hist.empty or len(hist) < 22:
                logger.warning("insufficient_history_for_iv", symbol=symbol, rows=len(hist))
                return pd.Series(dtype=float)

            log_returns = np.log(hist["Close"] / hist["Close"].shift(1)).dropna()
            realized_vol = log_returns.rolling(window=21).std() * np.sqrt(252)
            realized_vol = realized_vol.dropna()
            realized_vol.name = "realized_vol"

            logger.debug("historical_iv_computed", symbol=symbol, points=len(realized_vol))
            return realized_vol

        except Exception as exc:
            logger.warning("historical_iv_failed", symbol=symbol, error=str(exc))
            return pd.Series(dtype=float)

    # ----- IV rank & percentile -----

    def get_iv_rank(
        self,
        symbol: str,
        lookback_days: int = 252,
    ) -> dict[str, float | None]:
        """Compute IV rank and IV percentile for *symbol*.

        IV rank  = (current - min) / (max - min)
        IV percentile = fraction of past readings below the current level

        Args:
            symbol: Underlying ticker.
            lookback_days: Calendar days of history.

        Returns:
            Dictionary with ``current_iv``, ``iv_rank``, ``iv_percentile``,
            ``iv_high``, and ``iv_low``.  Values are ``None`` when data is
            insufficient.
        """
        result: dict[str, float | None] = {
            "current_iv": None,
            "iv_rank": None,
            "iv_percentile": None,
            "iv_high": None,
            "iv_low": None,
        }

        vol_series = self.get_historical_iv(symbol, lookback_days)
        if vol_series.empty:
            return result

        current = float(vol_series.iloc[-1])
        iv_high = float(vol_series.max())
        iv_low = float(vol_series.min())

        result["current_iv"] = current
        result["iv_high"] = iv_high
        result["iv_low"] = iv_low

        # IV rank
        if iv_high != iv_low:
            result["iv_rank"] = (current - iv_low) / (iv_high - iv_low)
        else:
            result["iv_rank"] = 0.0

        # IV percentile
        result["iv_percentile"] = float((vol_series < current).sum()) / len(vol_series)

        logger.debug(
            "iv_rank_computed",
            symbol=symbol,
            current_iv=round(current, 4),
            iv_rank=round(result["iv_rank"], 4) if result["iv_rank"] is not None else None,
        )
        return result
