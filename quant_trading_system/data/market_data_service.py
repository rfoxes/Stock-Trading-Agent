"""Market data service with Alpaca primary and yfinance fallback."""

from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import structlog

from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)

# Simple TTL cache
_cache: dict[str, tuple[float, pd.DataFrame]] = {}
_CACHE_TTL = 60  # seconds


def _cache_key(symbol: str, timeframe: str, start: str, end: str) -> str:
    return f"{symbol}:{timeframe}:{start}:{end}"


class MarketDataService:
    """Fetches market data from Alpaca with yfinance fallback."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._alpaca_client = None

        if settings.ALPACA_API_KEY:
            try:
                from alpaca.data.historical import StockHistoricalDataClient

                self._alpaca_client = StockHistoricalDataClient(
                    api_key=settings.ALPACA_API_KEY,
                    secret_key=settings.ALPACA_SECRET_KEY,
                )
                logger.info("market_data_alpaca_initialized")
            except Exception as e:
                logger.warning("alpaca_data_client_failed", error=str(e))

    def get_bars(
        self,
        symbol: str,
        timeframe: str = "1Day",
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 500,
    ) -> pd.DataFrame:
        """Get OHLCV bars for a symbol.

        Args:
            symbol: Ticker symbol.
            timeframe: "1Min", "5Min", "15Min", "1Hour", "1Day", "1Week".
            start: Start date (YYYY-MM-DD).
            end: End date (YYYY-MM-DD).
            limit: Max number of bars.

        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume.
        """
        if start is None:
            start = (datetime.utcnow() - timedelta(days=365 * 2)).strftime("%Y-%m-%d")
        if end is None:
            end = datetime.utcnow().strftime("%Y-%m-%d")

        # Check cache
        key = _cache_key(symbol, timeframe, start, end)
        if key in _cache:
            cached_time, cached_df = _cache[key]
            if time.time() - cached_time < _CACHE_TTL:
                logger.debug("cache_hit", symbol=symbol)
                return cached_df

        # Try Alpaca first
        df = self._get_bars_alpaca(symbol, timeframe, start, end, limit)
        if df is not None and not df.empty:
            _cache[key] = (time.time(), df)
            return df

        # Fallback to yfinance
        logger.info("falling_back_to_yfinance", symbol=symbol)
        df = self._get_bars_yfinance(symbol, timeframe, start, end)
        if df is not None and not df.empty:
            _cache[key] = (time.time(), df)
            return df

        logger.warning("no_data_available", symbol=symbol)
        return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])

    def _get_bars_alpaca(
        self, symbol: str, timeframe: str, start: str, end: str, limit: int
    ) -> Optional[pd.DataFrame]:
        """Fetch bars from Alpaca."""
        if self._alpaca_client is None:
            return None

        try:
            from alpaca.data.requests import StockBarsRequest
            from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

            tf_map = {
                "1Min": TimeFrame(1, TimeFrameUnit.Minute),
                "5Min": TimeFrame(5, TimeFrameUnit.Minute),
                "15Min": TimeFrame(15, TimeFrameUnit.Minute),
                "1Hour": TimeFrame(1, TimeFrameUnit.Hour),
                "1Day": TimeFrame(1, TimeFrameUnit.Day),
                "1Week": TimeFrame(1, TimeFrameUnit.Week),
            }

            tf = tf_map.get(timeframe)
            if tf is None:
                logger.warning("unsupported_timeframe_alpaca", timeframe=timeframe)
                return None

            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=tf,
                start=datetime.strptime(start, "%Y-%m-%d"),
                end=datetime.strptime(end, "%Y-%m-%d"),
                limit=limit,
            )
            bars = self._alpaca_client.get_stock_bars(request)
            df = bars.df

            if df.empty:
                return None

            # Normalize multi-index if present
            if isinstance(df.index, pd.MultiIndex):
                df = df.droplevel("symbol")

            # Standardize column names
            df = df.rename(columns={
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            })
            df = df[["Open", "High", "Low", "Close", "Volume"]]

            logger.debug("alpaca_bars_fetched", symbol=symbol, rows=len(df))
            return df

        except Exception as e:
            logger.warning("alpaca_bars_error", symbol=symbol, error=str(e))
            return None

    def _get_bars_yfinance(
        self, symbol: str, timeframe: str, start: str, end: str
    ) -> Optional[pd.DataFrame]:
        """Fetch bars from yfinance as fallback."""
        try:
            import yfinance as yf

            yf_interval_map = {
                "1Min": "1m",
                "5Min": "5m",
                "15Min": "15m",
                "1Hour": "1h",
                "1Day": "1d",
                "1Week": "1wk",
            }
            interval = yf_interval_map.get(timeframe, "1d")

            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start, end=end, interval=interval)

            if df.empty:
                return None

            # Standardize columns
            df = df.rename(columns={
                "Open": "Open",
                "High": "High",
                "Low": "Low",
                "Close": "Close",
                "Volume": "Volume",
            })
            df = df[["Open", "High", "Low", "Close", "Volume"]]

            logger.debug("yfinance_bars_fetched", symbol=symbol, rows=len(df))
            return df

        except Exception as e:
            logger.warning("yfinance_bars_error", symbol=symbol, error=str(e))
            return None

    def get_multiple_bars(
        self,
        symbols: list[str],
        timeframe: str = "1Day",
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> dict[str, pd.DataFrame]:
        """Get bars for multiple symbols."""
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_bars(symbol, timeframe, start, end)
        return results

    def get_latest_quote(self, symbol: str) -> Optional[dict]:
        """Get the latest quote for a symbol."""
        if self._alpaca_client is None:
            return None

        try:
            from alpaca.data.requests import StockLatestQuoteRequest

            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quotes = self._alpaca_client.get_stock_latest_quote(request)

            if symbol in quotes:
                q = quotes[symbol]
                return {
                    "bid": float(q.bid_price),
                    "ask": float(q.ask_price),
                    "bid_size": int(q.bid_size),
                    "ask_size": int(q.ask_size),
                    "mid": (float(q.bid_price) + float(q.ask_price)) / 2,
                }
            return None
        except Exception as e:
            logger.warning("latest_quote_error", symbol=symbol, error=str(e))
            return None
