"""Small helpers strategy scripts can import.

Keeping these in one place stops every strategy.py from re-implementing
position sizing, position lookup, etc. Strategies still own their own
*logic*; this just removes the boring scaffolding.
"""

from __future__ import annotations

import math
from typing import Any, Iterable

import pandas as pd


def has_position(positions: list[dict[str, Any]], symbol: str) -> bool:
    sym = symbol.upper()
    for p in positions or []:
        if str(p.get("symbol", "")).upper() == sym and float(p.get("qty", 0) or 0) != 0:
            return True
    return False


def position_qty(positions: list[dict[str, Any]], symbol: str) -> float:
    sym = symbol.upper()
    for p in positions or []:
        if str(p.get("symbol", "")).upper() == sym:
            return float(p.get("qty", 0) or 0)
    return 0.0


def share_count(
    equity: float,
    risk_pct: float,
    entry_price: float,
    stop_distance_pct: float,
    max_position_pct: float = 0.10,
) -> int:
    """Risk-based sizing.

    Risk per trade is `equity * risk_pct`. Per-share loss at the stop is
    `entry_price * stop_distance_pct`. Shares = risk-dollars / per-share-loss,
    then capped at `max_position_pct * equity / entry_price`.

    Returns integer shares (floor). Zero if any input is non-positive.
    """
    if equity <= 0 or entry_price <= 0 or stop_distance_pct <= 0 or risk_pct <= 0:
        return 0
    risk_dollars = equity * risk_pct
    per_share_loss = entry_price * stop_distance_pct
    raw = risk_dollars / per_share_loss
    cap = (equity * max_position_pct) / entry_price
    shares = math.floor(min(raw, cap))
    return max(0, int(shares))


def last_close(bars: pd.DataFrame) -> float | None:
    if bars is None or bars.empty or "Close" not in bars.columns:
        return None
    return float(bars["Close"].iloc[-1])


def crossed_above(series: pd.Series, level_series: pd.Series, lookback: int = 2) -> bool:
    """True if `series` crossed above `level_series` within the last `lookback` bars."""
    s, l = series.dropna(), level_series.dropna()
    n = min(len(s), len(l))
    if n < lookback + 1:
        return False
    s = s.iloc[-(lookback + 1):]
    l = l.iloc[-(lookback + 1):]
    return bool((s.iloc[0] <= l.iloc[0]) and (s.iloc[-1] > l.iloc[-1]))


def crossed_below(series: pd.Series, level_series: pd.Series, lookback: int = 2) -> bool:
    s, l = series.dropna(), level_series.dropna()
    n = min(len(s), len(l))
    if n < lookback + 1:
        return False
    s = s.iloc[-(lookback + 1):]
    l = l.iloc[-(lookback + 1):]
    return bool((s.iloc[0] >= l.iloc[0]) and (s.iloc[-1] < l.iloc[-1]))


def average_volume(bars: pd.DataFrame, window: int = 20) -> float:
    if bars is None or bars.empty or "Volume" not in bars.columns:
        return 0.0
    return float(bars["Volume"].tail(window).mean())


def filter_existing(symbols: Iterable[str], positions: list[dict[str, Any]]) -> list[str]:
    """Return only the symbols you don't already have a position in."""
    return [s for s in symbols if not has_position(positions, s)]
