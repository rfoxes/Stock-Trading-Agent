"""Technical indicators in pure pandas + numpy.

The Cowork sandbox doesn't have TA-Lib or pandas_ta available, so this
implements the indicators the harness actually uses (SMA, EMA, RSI, MACD,
Bollinger, ATR, ADX, OBV, VWAP) directly.

These are textbook implementations — close enough to the canonical
definitions for regime classification and strategy entry/exit checks.
For backtests requiring exact SDK-equivalence, install TA-Lib instead.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_sma(series: pd.Series, period: int = 20) -> pd.Series:
    return series.rolling(window=period, min_periods=period).mean()


def compute_ema(series: pd.Series, period: int = 20) -> pd.Series:
    return series.ewm(span=period, adjust=False, min_periods=period).mean()


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def compute_macd(
    series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame:
    fast_ema = compute_ema(series, fast)
    slow_ema = compute_ema(series, slow)
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False, min_periods=signal).mean()
    hist = macd_line - signal_line
    return pd.DataFrame(
        {"MACD": macd_line, "Signal": signal_line, "Histogram": hist},
        index=series.index,
    )


def compute_bollinger_bands(
    series: pd.Series, period: int = 20, std_dev: float = 2.0
) -> pd.DataFrame:
    middle = compute_sma(series, period)
    std = series.rolling(window=period, min_periods=period).std()
    upper = middle + std_dev * std
    lower = middle - std_dev * std
    return pd.DataFrame(
        {"Upper": upper, "Middle": middle, "Lower": lower},
        index=series.index,
    )


def compute_atr(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low).abs(),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    # Wilder smoothing — equivalent to EMA with alpha=1/period
    atr = tr.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    return atr


def compute_adx(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> pd.Series:
    """Average Directional Index — Wilder's classic formulation."""
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    atr = compute_atr(high, low, close, period)
    plus_di = 100.0 * (
        plus_dm.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean() / atr
    )
    minus_di = 100.0 * (
        minus_dm.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean() / atr
    )
    dx = (
        100.0
        * ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan))
    )
    adx = dx.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    return adx


def compute_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    direction = np.sign(close.diff().fillna(0.0))
    return (direction * volume).cumsum()


def compute_vwap(
    high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series
) -> pd.Series:
    typical = (high + low + close) / 3.0
    cum_vol = volume.cumsum().replace(0.0, np.nan)
    return (typical * volume).cumsum() / cum_vol


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add all standard indicators as columns to an OHLCV DataFrame."""
    result = df.copy()
    result["SMA_20"] = compute_sma(df["Close"], 20)
    result["SMA_50"] = compute_sma(df["Close"], 50)
    result["SMA_200"] = compute_sma(df["Close"], 200)
    result["EMA_12"] = compute_ema(df["Close"], 12)
    result["EMA_26"] = compute_ema(df["Close"], 26)
    result["RSI_14"] = compute_rsi(df["Close"], 14)
    macd = compute_macd(df["Close"])
    result["MACD"] = macd["MACD"]
    result["MACD_Signal"] = macd["Signal"]
    result["MACD_Histogram"] = macd["Histogram"]
    bb = compute_bollinger_bands(df["Close"])
    result["BB_Upper"] = bb["Upper"]
    result["BB_Middle"] = bb["Middle"]
    result["BB_Lower"] = bb["Lower"]
    result["ATR_14"] = compute_atr(df["High"], df["Low"], df["Close"], 14)
    result["ADX_14"] = compute_adx(df["High"], df["Low"], df["Close"], 14)
    if "Volume" in df.columns:
        result["OBV"] = compute_obv(df["Close"], df["Volume"])
        result["VWAP"] = compute_vwap(df["High"], df["Low"], df["Close"], df["Volume"])
    return result
