"""Market regime classification using technical indicators."""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd
import structlog

from quant_trading_system.tools.technical_indicators import compute_adx, compute_sma

logger = structlog.get_logger(__name__)


class RegimeClassifier:
    """Classifies market regime based on technical indicators.

    Regimes:
    - bull: Uptrend with moderate volatility
    - bear: Downtrend
    - sideways: No clear trend, low volatility
    - volatile: High volatility, uncertain direction
    """

    def __init__(self, lookback_days: int = 252) -> None:
        self._lookback = lookback_days

    def classify(self, df: pd.DataFrame) -> dict:
        """Classify market regime from OHLCV data.

        Args:
            df: DataFrame with at least Close, High, Low columns.

        Returns:
            Dict with regime, confidence, and supporting indicators.
        """
        if len(df) < 50:
            return {
                "regime": "unknown",
                "confidence": 0.0,
                "indicators": {},
                "reasoning": "Insufficient data for regime classification",
            }

        close = df["Close"]

        # 1. Trend direction: 200-day SMA slope
        sma_200 = compute_sma(close, min(200, len(close) - 1))
        sma_50 = compute_sma(close, min(50, len(close) - 1))

        sma_200_slope = self._compute_slope(sma_200, 20)
        price_vs_sma200 = (close.iloc[-1] / sma_200.iloc[-1] - 1) if sma_200.iloc[-1] > 0 else 0
        sma_50_vs_200 = (sma_50.iloc[-1] / sma_200.iloc[-1] - 1) if sma_200.iloc[-1] > 0 else 0

        # 2. Trend strength: ADX
        adx = compute_adx(df["High"], df["Low"], close, 14)
        current_adx = adx.iloc[-1] if not pd.isna(adx.iloc[-1]) else 0

        # 3. Volatility: Realized volatility (annualized)
        returns = close.pct_change().dropna()
        realized_vol = returns.tail(20).std() * np.sqrt(252) if len(returns) >= 20 else 0

        # 4. Classification logic
        regime = self._determine_regime(
            sma_200_slope=sma_200_slope,
            price_vs_sma200=price_vs_sma200,
            sma_50_vs_200=sma_50_vs_200,
            adx=current_adx,
            realized_vol=realized_vol,
        )

        indicators = {
            "sma_200_slope": round(sma_200_slope, 6),
            "price_vs_sma200": round(price_vs_sma200, 4),
            "sma_50_vs_200": round(sma_50_vs_200, 4),
            "adx": round(current_adx, 2),
            "realized_vol": round(realized_vol, 4),
        }

        confidence = self._compute_confidence(regime, indicators)

        result = {
            "regime": regime,
            "confidence": round(confidence, 2),
            "indicators": indicators,
            "reasoning": self._generate_reasoning(regime, indicators),
        }

        logger.info("regime_classified", **result)
        return result

    def _compute_slope(self, series: pd.Series, window: int = 20) -> float:
        """Compute the slope of a series over a window using linear regression."""
        tail = series.dropna().tail(window)
        if len(tail) < 5:
            return 0.0
        x = np.arange(len(tail))
        coefficients = np.polyfit(x, tail.values, 1)
        return coefficients[0] / tail.mean() if tail.mean() != 0 else 0.0

    def _determine_regime(
        self,
        sma_200_slope: float,
        price_vs_sma200: float,
        sma_50_vs_200: float,
        adx: float,
        realized_vol: float,
    ) -> str:
        """Determine regime based on indicator values."""
        # High volatility overrides
        if realized_vol > 0.30:
            return "volatile"

        # Strong trend
        if adx > 25:
            if sma_200_slope > 0 and price_vs_sma200 > 0:
                return "bull"
            elif sma_200_slope < 0 and price_vs_sma200 < 0:
                return "bear"

        # Moderate signals
        if sma_50_vs_200 > 0.02 and sma_200_slope > 0:
            return "bull"
        elif sma_50_vs_200 < -0.02 and sma_200_slope < 0:
            return "bear"

        # Elevated vol without clear trend
        if realized_vol > 0.20:
            return "volatile"

        return "sideways"

    def _compute_confidence(self, regime: str, indicators: dict) -> float:
        """Estimate confidence in the regime classification (0-1)."""
        adx = indicators.get("adx", 0)
        vol = indicators.get("realized_vol", 0)

        if regime in ("bull", "bear"):
            # Higher ADX = more confidence in trend
            return min(0.95, 0.5 + adx / 100)
        elif regime == "volatile":
            return min(0.90, 0.5 + vol)
        else:  # sideways
            # Low ADX = more confidence in sideways
            return min(0.85, 0.5 + (50 - adx) / 100) if adx < 50 else 0.4

    def _generate_reasoning(self, regime: str, indicators: dict) -> str:
        """Generate human-readable reasoning for the classification."""
        parts = [f"Market regime: {regime.upper()}."]

        adx = indicators.get("adx", 0)
        vol = indicators.get("realized_vol", 0)
        price_vs_sma = indicators.get("price_vs_sma200", 0)

        if regime == "bull":
            parts.append(f"Price is {price_vs_sma:.1%} above 200-SMA.")
            parts.append(f"ADX at {adx:.0f} indicates {'strong' if adx > 30 else 'moderate'} trend.")
        elif regime == "bear":
            parts.append(f"Price is {abs(price_vs_sma):.1%} below 200-SMA.")
            parts.append(f"ADX at {adx:.0f} confirms downtrend strength.")
        elif regime == "volatile":
            parts.append(f"Realized volatility at {vol:.1%} (annualized) is elevated.")
        else:
            parts.append(f"ADX at {adx:.0f} indicates no clear trend.")
            parts.append(f"Realized volatility at {vol:.1%} is moderate.")

        return " ".join(parts)
