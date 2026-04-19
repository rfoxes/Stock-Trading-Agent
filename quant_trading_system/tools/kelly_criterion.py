"""Kelly Criterion position sizing."""

from __future__ import annotations

import math


def kelly_fraction(win_rate: float, avg_win: float, avg_loss: float) -> float:
    """Calculate the full Kelly fraction for position sizing.

    Args:
        win_rate: Probability of winning (0-1).
        avg_win: Average winning trade return (positive).
        avg_loss: Average losing trade return (positive, will be treated as loss).

    Returns:
        Kelly fraction (0-1). Clamped to [0, 1].
    """
    if avg_loss <= 0 or avg_win <= 0 or not (0 < win_rate < 1):
        return 0.0

    # Kelly formula: f = (bp - q) / b
    # where b = avg_win / avg_loss, p = win_rate, q = 1 - win_rate
    b = avg_win / avg_loss
    p = win_rate
    q = 1.0 - p
    f = (b * p - q) / b

    return max(0.0, min(1.0, f))


def half_kelly(win_rate: float, avg_win: float, avg_loss: float) -> float:
    """Half Kelly — more conservative, recommended for live trading.

    Using half Kelly reduces the volatility of returns significantly
    while only giving up ~25% of the growth rate.
    """
    return kelly_fraction(win_rate, avg_win, avg_loss) / 2.0


def position_size(
    kelly_f: float,
    portfolio_value: float,
    price_per_share: float,
    max_position_pct: float = 0.10,
) -> int:
    """Convert Kelly fraction to number of shares.

    Applies an additional cap at max_position_pct of portfolio.

    Returns:
        Number of whole shares to purchase.
    """
    if price_per_share <= 0 or portfolio_value <= 0:
        return 0

    # Cap Kelly fraction at max position percentage
    effective_fraction = min(kelly_f, max_position_pct)
    dollar_amount = portfolio_value * effective_fraction
    shares = math.floor(dollar_amount / price_per_share)
    return max(0, shares)
