"""Options support: OCC symbol parsing, contract/leg models, helpers.

OCC symbol format (21 chars):
    Root (6, left-padded with spaces or unpadded)
    Expiration date (6 digits, YYMMDD)
    Right (1: C or P)
    Strike (8 digits, in thousandths, e.g. 00150000 = $150.00)

Examples:
    AAPL250620C00150000  → AAPL, 2025-06-20, Call,  strike $150
    SPY 250620P00420000  → SPY,  2025-06-20, Put,   strike $420
    BRK.B250620C00350000 → BRK.B  (rare; alpaca uses dots)

This module deliberately stays small. The harness uses it for:
  - Building option symbols from (underlying, expiration, type, strike)
  - Parsing option symbols back into structured form
  - Representing multi-leg positions as `OptionsOrderRequest`
  - Tiny helpers strategies can use to find strikes / compute IV rank
"""

from __future__ import annotations

import datetime as dt
import math
import re
from dataclasses import dataclass, field
from typing import Any, Iterable

import pandas as pd


_OCC_RE = re.compile(
    r"^(?P<root>[A-Z0-9.\-]{1,6})"
    r"(?P<exp>\d{6})"
    r"(?P<right>[CP])"
    r"(?P<strike>\d{8})$"
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OptionContract:
    """One option contract: a strike + expiration + right on an underlying."""

    underlying: str
    expiration: dt.date
    strike: float
    right: str  # "C" | "P"

    def __post_init__(self) -> None:
        # frozen dataclass — can't assign; just sanity-check
        if self.right not in ("C", "P"):
            raise ValueError(f"right must be C or P, got {self.right!r}")
        if self.strike <= 0:
            raise ValueError("strike must be positive")

    @property
    def dte(self) -> int:
        return (self.expiration - dt.date.today()).days

    @property
    def occ_symbol(self) -> str:
        return build_occ_symbol(
            self.underlying, self.expiration, self.right, self.strike,
        )

    def __str__(self) -> str:
        return self.occ_symbol


@dataclass
class OptionLeg:
    """One leg of a multi-leg options position.

    `side` is "buy" or "sell" (i.e. long or short the contract).
    `ratio` is the leg's quantity ratio (almost always 1; jade lizards can be
    different). `qty` is the total contracts for this leg in this order.
    """

    contract: OptionContract
    side: str  # "buy" | "sell"
    ratio: int = 1
    qty: int = 1

    def __post_init__(self) -> None:
        if self.side.lower() not in ("buy", "sell"):
            raise ValueError(f"side must be buy/sell, got {self.side!r}")
        if self.qty < 1:
            raise ValueError(f"qty must be >= 1, got {self.qty}")

    def to_alpaca_leg(self) -> dict[str, Any]:
        """Alpaca's /v2/orders legs[] entry shape."""
        return {
            "symbol": self.contract.occ_symbol,
            "side": self.side.lower(),
            "ratio_qty": str(self.ratio),
            "position_intent": "buy_to_open" if self.side.lower() == "buy" else "sell_to_open",
        }


# ---------------------------------------------------------------------------
# OCC symbol helpers
# ---------------------------------------------------------------------------


def build_occ_symbol(
    underlying: str, expiration: dt.date, right: str, strike: float,
) -> str:
    """Build an OCC option symbol from components."""
    if right.upper() not in ("C", "P"):
        raise ValueError(f"right must be C or P, got {right!r}")
    root = underlying.upper()
    exp_str = expiration.strftime("%y%m%d")
    strike_thousandths = int(round(strike * 1000))
    return f"{root}{exp_str}{right.upper()}{strike_thousandths:08d}"


def parse_occ_symbol(symbol: str) -> OptionContract:
    """Parse an OCC symbol into an OptionContract. Raises ValueError if invalid."""
    s = symbol.strip().upper()
    m = _OCC_RE.match(s)
    if not m:
        raise ValueError(f"not a valid OCC symbol: {symbol!r}")
    underlying = m.group("root")
    exp = dt.datetime.strptime(m.group("exp"), "%y%m%d").date()
    right = m.group("right")
    strike = int(m.group("strike")) / 1000.0
    return OptionContract(
        underlying=underlying, expiration=exp, right=right, strike=strike,
    )


# ---------------------------------------------------------------------------
# Strike / delta helpers
# ---------------------------------------------------------------------------


def find_strike_by_delta(
    chain: list[dict[str, Any]],
    target_delta: float,
    right: str,
    *,
    expiration: dt.date | None = None,
) -> dict[str, Any] | None:
    """From a chain (Alpaca's `OptionsSnapshot` shape), find the strike whose
    abs(delta) is closest to target_delta for the given right and (optional)
    expiration.

    Returns the snapshot dict, or None if nothing matches.
    """
    candidates = []
    for snap in chain:
        sym = snap.get("symbol", "")
        try:
            contract = parse_occ_symbol(sym)
        except ValueError:
            continue
        if contract.right != right.upper():
            continue
        if expiration is not None and contract.expiration != expiration:
            continue
        greeks = snap.get("greeks") or {}
        delta = greeks.get("delta")
        if delta is None:
            continue
        candidates.append((abs(abs(float(delta)) - abs(target_delta)), snap, contract))
    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0])
    return candidates[0][1]


def find_atm_strike(
    chain: list[dict[str, Any]], spot: float, right: str,
    *, expiration: dt.date | None = None,
) -> dict[str, Any] | None:
    """Closest-to-money strike for the given right + expiration."""
    candidates = []
    for snap in chain:
        sym = snap.get("symbol", "")
        try:
            contract = parse_occ_symbol(sym)
        except ValueError:
            continue
        if contract.right != right.upper():
            continue
        if expiration is not None and contract.expiration != expiration:
            continue
        candidates.append((abs(contract.strike - spot), snap, contract))
    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0])
    return candidates[0][1]


def expirations_in_dte_range(
    chain: list[dict[str, Any]], min_dte: int, max_dte: int,
) -> list[dt.date]:
    """Distinct expirations in the chain whose DTE falls in the range."""
    today = dt.date.today()
    out: set[dt.date] = set()
    for snap in chain:
        sym = snap.get("symbol", "")
        try:
            contract = parse_occ_symbol(sym)
        except ValueError:
            continue
        d = (contract.expiration - today).days
        if min_dte <= d <= max_dte:
            out.add(contract.expiration)
    return sorted(out)


# ---------------------------------------------------------------------------
# IV rank
# ---------------------------------------------------------------------------


def compute_iv_rank(historical_iv: pd.Series, current_iv: float | None = None) -> float | None:
    """IV rank = (current_iv − min_252d) / (max_252d − min_252d), clipped to [0, 100].

    `historical_iv` is a daily series of at-the-money IV (annualized, as a
    fraction; e.g. 0.20 for 20% vol). `current_iv` defaults to the last value.
    Returns None if there's insufficient history.
    """
    s = historical_iv.dropna().tail(252)
    if len(s) < 30:
        return None
    if current_iv is None:
        current_iv = float(s.iloc[-1])
    lo = float(s.min())
    hi = float(s.max())
    if hi <= lo:
        return 50.0
    rank = (current_iv - lo) / (hi - lo) * 100.0
    return max(0.0, min(100.0, rank))


# ---------------------------------------------------------------------------
# Black-Scholes (used by strategies + backtester later)
# ---------------------------------------------------------------------------


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(
    spot: float, strike: float, dte_days: int, iv: float, right: str,
    rate: float = 0.05, dividend: float = 0.0,
) -> float:
    """Black-Scholes price for one option. iv as a fraction (0.20 = 20%)."""
    if dte_days <= 0:
        # At/after expiration: intrinsic value
        if right.upper() == "C":
            return max(0.0, spot - strike)
        return max(0.0, strike - spot)
    t = dte_days / 365.0
    if iv <= 0:
        return max(
            0.0, (spot - strike) if right.upper() == "C" else (strike - spot),
        )
    d1 = (math.log(spot / strike) + (rate - dividend + 0.5 * iv * iv) * t) / (
        iv * math.sqrt(t)
    )
    d2 = d1 - iv * math.sqrt(t)
    if right.upper() == "C":
        return (
            spot * math.exp(-dividend * t) * _phi(d1)
            - strike * math.exp(-rate * t) * _phi(d2)
        )
    return (
        strike * math.exp(-rate * t) * _phi(-d2)
        - spot * math.exp(-dividend * t) * _phi(-d1)
    )
