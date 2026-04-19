"""QuantLib wrappers for options pricing and Greeks computation.

Provides Black-Scholes pricing, implied volatility calculation, Greeks,
and American option pricing via binomial trees. All QuantLib imports are
guarded so the rest of the system works even if QuantLib is not installed.
"""

from __future__ import annotations

import threading
from datetime import date
from typing import Literal

# ---------------------------------------------------------------------------
# Guarded QuantLib import
# ---------------------------------------------------------------------------
try:
    import QuantLib as ql

    _HAS_QUANTLIB = True
except ImportError:  # pragma: no cover
    ql = None  # type: ignore[assignment]
    _HAS_QUANTLIB = False

_QL_LOCK = threading.Lock()

_MISSING_MSG = (
    "QuantLib is required for options math but is not installed. "
    "Install it with: pip install QuantLib-Python  (or pip install QuantLib)"
)


def _require_quantlib() -> None:
    if not _HAS_QUANTLIB:
        raise ImportError(_MISSING_MSG)


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def to_ql_date(dt: date) -> ql.Date:
    """Convert a Python ``date`` to a QuantLib ``Date``."""
    _require_quantlib()
    return ql.Date(dt.day, dt.month, dt.year)


def from_ql_date(ql_date) -> date:
    """Convert a QuantLib ``Date`` to a Python ``date``."""
    _require_quantlib()
    return date(ql_date.year(), ql_date.month(), ql_date.dayOfMonth())


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _option_type_to_ql(option_type: Literal["call", "put"]):
    """Map a string option type to the QuantLib constant."""
    if option_type == "call":
        return ql.Option.Call
    elif option_type == "put":
        return ql.Option.Put
    else:
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")


def _build_bsm_process(spot: float, rate: float, vol: float, eval_date):
    """Build a ``BlackScholesMertonProcess`` with flat term structures."""
    day_count = ql.Actual365Fixed()
    calendar = ql.NullCalendar()

    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
    rate_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_date, ql.QuoteHandle(ql.SimpleQuote(rate)), day_count)
    )
    div_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_date, ql.QuoteHandle(ql.SimpleQuote(0.0)), day_count)
    )
    vol_ts = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(eval_date, calendar, ql.QuoteHandle(ql.SimpleQuote(vol)), day_count)
    )
    return ql.BlackScholesMertonProcess(spot_handle, div_ts, rate_ts, vol_ts)


def _make_european_option(strike: float, time_to_expiry_years: float, option_type: str, eval_date):
    """Create a European ``VanillaOption`` and its exercise/payoff objects."""
    day_count = ql.Actual365Fixed()
    maturity_date = eval_date + ql.Period(int(round(time_to_expiry_years * 365)), ql.Days)
    exercise = ql.EuropeanExercise(maturity_date)
    payoff = ql.PlainVanillaPayoff(_option_type_to_ql(option_type), strike)
    return ql.VanillaOption(payoff, exercise), maturity_date


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def black_scholes_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    time_to_expiry_years: float,
    option_type: Literal["call", "put"],
) -> float:
    """Price a European option using the Black-Scholes-Merton model.

    Args:
        spot: Current underlying price.
        strike: Option strike price.
        rate: Risk-free interest rate (annualized, e.g. 0.05 for 5%).
        vol: Annualized volatility (e.g. 0.20 for 20%).
        time_to_expiry_years: Time to expiration in years.
        option_type: ``"call"`` or ``"put"``.

    Returns:
        Theoretical option price.
    """
    _require_quantlib()

    with _QL_LOCK:
        eval_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = eval_date

        process = _build_bsm_process(spot, rate, vol, eval_date)
        option, _ = _make_european_option(strike, time_to_expiry_years, option_type, eval_date)
        option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
        return float(option.NPV())


def implied_volatility(
    market_price: float,
    spot: float,
    strike: float,
    rate: float,
    time_to_expiry_years: float,
    option_type: Literal["call", "put"],
) -> float:
    """Compute implied volatility from a market price using Newton's method.

    Args:
        market_price: Observed market price of the option.
        spot: Current underlying price.
        strike: Option strike price.
        rate: Risk-free interest rate (annualized).
        time_to_expiry_years: Time to expiration in years.
        option_type: ``"call"`` or ``"put"``.

    Returns:
        Implied volatility as a decimal (e.g. 0.25 for 25%).
    """
    _require_quantlib()

    with _QL_LOCK:
        eval_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = eval_date

        # We need an initial process to set up the option — vol doesn't matter
        # because QuantLib's impliedVolatility will search for the correct one.
        process = _build_bsm_process(spot, rate, 0.20, eval_date)
        option, _ = _make_european_option(strike, time_to_expiry_years, option_type, eval_date)
        option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

        return float(
            option.impliedVolatility(
                market_price,
                process,
                1e-6,   # accuracy
                1000,   # maxEvaluations
                0.001,  # minVol
                10.0,   # maxVol
            )
        )


def greeks(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    time_to_expiry_years: float,
    option_type: Literal["call", "put"],
) -> dict[str, float]:
    """Compute option Greeks (delta, gamma, theta, vega, rho).

    Args:
        spot: Current underlying price.
        strike: Option strike price.
        rate: Risk-free interest rate (annualized).
        vol: Annualized volatility.
        time_to_expiry_years: Time to expiration in years.
        option_type: ``"call"`` or ``"put"``.

    Returns:
        Dictionary with keys: ``delta``, ``gamma``, ``theta``, ``vega``, ``rho``.
    """
    _require_quantlib()

    with _QL_LOCK:
        eval_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = eval_date

        process = _build_bsm_process(spot, rate, vol, eval_date)
        option, _ = _make_european_option(strike, time_to_expiry_years, option_type, eval_date)
        option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

        return {
            "delta": float(option.delta()),
            "gamma": float(option.gamma()),
            "theta": float(option.theta()),
            "vega": float(option.vega()),
            "rho": float(option.rho()),
        }


def price_american_option(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    time_to_expiry_years: float,
    option_type: Literal["call", "put"],
    steps: int = 200,
) -> float:
    """Price an American-style option using a binomial tree.

    Args:
        spot: Current underlying price.
        strike: Option strike price.
        rate: Risk-free interest rate (annualized).
        vol: Annualized volatility.
        time_to_expiry_years: Time to expiration in years.
        option_type: ``"call"`` or ``"put"``.
        steps: Number of binomial tree steps (default 200).

    Returns:
        Theoretical American option price.
    """
    _require_quantlib()

    with _QL_LOCK:
        eval_date = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = eval_date

        day_count = ql.Actual365Fixed()
        maturity_date = eval_date + ql.Period(int(round(time_to_expiry_years * 365)), ql.Days)

        exercise = ql.AmericanExercise(eval_date, maturity_date)
        payoff = ql.PlainVanillaPayoff(_option_type_to_ql(option_type), strike)
        option = ql.VanillaOption(payoff, exercise)

        process = _build_bsm_process(spot, rate, vol, eval_date)
        engine = ql.BinomialVanillaEngine(process, "crr", steps)
        option.setPricingEngine(engine)

        return float(option.NPV())
