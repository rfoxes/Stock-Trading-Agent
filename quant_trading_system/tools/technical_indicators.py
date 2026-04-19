"""Technical indicator wrappers with TA-Lib primary and pandas_ta fallback."""

from __future__ import annotations

import numpy as np
import pandas as pd

# Try TA-Lib first, fall back to pandas_ta
try:
    import talib

    _USE_TALIB = True
except ImportError:
    _USE_TALIB = False

import pandas_ta as pta


def compute_sma(series: pd.Series, period: int = 20) -> pd.Series:
    """Simple Moving Average."""
    if _USE_TALIB:
        return pd.Series(talib.SMA(series.values, timeperiod=period), index=series.index)
    return pta.sma(series, length=period)


def compute_ema(series: pd.Series, period: int = 20) -> pd.Series:
    """Exponential Moving Average."""
    if _USE_TALIB:
        return pd.Series(talib.EMA(series.values, timeperiod=period), index=series.index)
    return pta.ema(series, length=period)


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index."""
    if _USE_TALIB:
        return pd.Series(talib.RSI(series.values, timeperiod=period), index=series.index)
    return pta.rsi(series, length=period)


def compute_macd(
    series: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """MACD with signal line and histogram.

    Returns DataFrame with columns: MACD, Signal, Histogram.
    """
    if _USE_TALIB:
        macd, signal_line, hist = talib.MACD(
            series.values, fastperiod=fast, slowperiod=slow, signalperiod=signal
        )
        return pd.DataFrame(
            {"MACD": macd, "Signal": signal_line, "Histogram": hist},
            index=series.index,
        )
    result = pta.macd(series, fast=fast, slow=slow, signal=signal)
    if result is not None:
        result.columns = ["MACD", "Histogram", "Signal"]
    return result


def compute_bollinger_bands(
    series: pd.Series, period: int = 20, std_dev: float = 2.0
) -> pd.DataFrame:
    """Bollinger Bands.

    Returns DataFrame with columns: Upper, Middle, Lower.
    """
    if _USE_TALIB:
        upper, middle, lower = talib.BBANDS(
            series.values, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev
        )
        return pd.DataFrame(
            {"Upper": upper, "Middle": middle, "Lower": lower},
            index=series.index,
        )
    result = pta.bbands(series, length=period, std=std_dev)
    if result is not None:
        cols = result.columns.tolist()
        return pd.DataFrame(
            {"Lower": result[cols[0]], "Middle": result[cols[1]], "Upper": result[cols[2]]},
            index=series.index,
        )
    return pd.DataFrame(index=series.index)


def compute_atr(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> pd.Series:
    """Average True Range."""
    if _USE_TALIB:
        return pd.Series(
            talib.ATR(high.values, low.values, close.values, timeperiod=period),
            index=close.index,
        )
    return pta.atr(high, low, close, length=period)


def compute_vwap(
    high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series
) -> pd.Series:
    """Volume Weighted Average Price."""
    return pta.vwap(high, low, close, volume)


def compute_adx(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> pd.Series:
    """Average Directional Index."""
    if _USE_TALIB:
        return pd.Series(
            talib.ADX(high.values, low.values, close.values, timeperiod=period),
            index=close.index,
        )
    result = pta.adx(high, low, close, length=period)
    if result is not None:
        # pandas_ta returns DataFrame with ADX, DMP, DMN columns
        adx_col = [c for c in result.columns if "ADX" in c][0]
        return result[adx_col]
    return pd.Series(dtype=float, index=close.index)


def compute_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On-Balance Volume."""
    if _USE_TALIB:
        return pd.Series(talib.OBV(close.values, volume.values), index=close.index)
    return pta.obv(close, volume)


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute all standard indicators on an OHLCV DataFrame.

    Expects columns: Open, High, Low, Close, Volume.
    Returns a new DataFrame with all indicator columns added.
    """
    result = df.copy()

    result["SMA_20"] = compute_sma(df["Close"], 20)
    result["SMA_50"] = compute_sma(df["Close"], 50)
    result["SMA_200"] = compute_sma(df["Close"], 200)
    result["EMA_12"] = compute_ema(df["Close"], 12)
    result["EMA_26"] = compute_ema(df["Close"], 26)
    result["RSI_14"] = compute_rsi(df["Close"], 14)

    macd = compute_macd(df["Close"])
    if macd is not None:
        result["MACD"] = macd["MACD"]
        result["MACD_Signal"] = macd["Signal"]
        result["MACD_Histogram"] = macd["Histogram"]

    bb = compute_bollinger_bands(df["Close"])
    if not bb.empty:
        result["BB_Upper"] = bb["Upper"]
        result["BB_Middle"] = bb["Middle"]
        result["BB_Lower"] = bb["Lower"]

    result["ATR_14"] = compute_atr(df["High"], df["Low"], df["Close"], 14)
    result["ADX_14"] = compute_adx(df["High"], df["Low"], df["Close"], 14)
    result["OBV"] = compute_obv(df["Close"], df["Volume"])

    if "Volume" in df.columns:
        vwap = compute_vwap(df["High"], df["Low"], df["Close"], df["Volume"])
        if vwap is not None:
            result["VWAP"] = vwap

    return result
