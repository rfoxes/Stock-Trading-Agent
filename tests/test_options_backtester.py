"""Tests for options math, OptionLeg model, and backtester components.

All QuantLib-dependent tests are skipped automatically when QuantLib is not
installed, so the rest of the test suite is never blocked.
"""

from __future__ import annotations

import math
from datetime import date

import pytest


# ---------------------------------------------------------------------------
# Skip the entire module if QuantLib is missing
# ---------------------------------------------------------------------------
ql = pytest.importorskip("QuantLib", reason="QuantLib is not installed")


from quant_trading_system.tools.options_math import (
    black_scholes_price,
    greeks,
    implied_volatility,
    price_american_option,
    to_ql_date,
    from_ql_date,
)
from quant_trading_system.data.options_data import OptionLeg


# ---------------------------------------------------------------------------
# Date-helper tests
# ---------------------------------------------------------------------------

class TestDateHelpers:
    def test_round_trip(self):
        d = date(2025, 6, 15)
        assert from_ql_date(to_ql_date(d)) == d

    def test_leap_year(self):
        d = date(2024, 2, 29)
        assert from_ql_date(to_ql_date(d)) == d


# ---------------------------------------------------------------------------
# Black-Scholes pricing tests
# ---------------------------------------------------------------------------

class TestBlackScholesPrice:
    """Verify prices against known analytical values."""

    def test_atm_call_price(self):
        """ATM call: S=100, K=100, r=5%, vol=20%, T=1y should be ~10.45."""
        price = black_scholes_price(
            spot=100.0,
            strike=100.0,
            rate=0.05,
            vol=0.20,
            time_to_expiry_years=1.0,
            option_type="call",
        )
        assert price == pytest.approx(10.45, abs=0.15)

    def test_deep_itm_call(self):
        """Deep ITM call should be close to intrinsic + time value."""
        price = black_scholes_price(
            spot=150.0,
            strike=100.0,
            rate=0.05,
            vol=0.20,
            time_to_expiry_years=1.0,
            option_type="call",
        )
        intrinsic = 150.0 - 100.0 * math.exp(-0.05)
        assert price > intrinsic

    def test_deep_otm_put(self):
        """Deep OTM put should be very cheap."""
        price = black_scholes_price(
            spot=150.0,
            strike=100.0,
            rate=0.05,
            vol=0.20,
            time_to_expiry_years=1.0,
            option_type="put",
        )
        assert price < 1.0

    def test_zero_vol_call(self):
        """With near-zero vol, call price should be ~max(S - K*exp(-rT), 0)."""
        price = black_scholes_price(
            spot=110.0,
            strike=100.0,
            rate=0.05,
            vol=0.001,
            time_to_expiry_years=1.0,
            option_type="call",
        )
        expected = 110.0 - 100.0 * math.exp(-0.05)
        assert price == pytest.approx(expected, abs=0.5)


# ---------------------------------------------------------------------------
# Put-call parity
# ---------------------------------------------------------------------------

class TestPutCallParity:
    """C - P = S - K * exp(-rT)."""

    @pytest.mark.parametrize(
        "spot,strike,rate,vol,T",
        [
            (100, 100, 0.05, 0.20, 1.0),
            (110, 100, 0.03, 0.30, 0.5),
            (90, 100, 0.08, 0.25, 2.0),
            (100, 120, 0.05, 0.15, 0.25),
        ],
    )
    def test_parity(self, spot, strike, rate, vol, T):
        call = black_scholes_price(spot, strike, rate, vol, T, "call")
        put = black_scholes_price(spot, strike, rate, vol, T, "put")
        parity_rhs = spot - strike * math.exp(-rate * T)
        assert (call - put) == pytest.approx(parity_rhs, abs=0.01)


# ---------------------------------------------------------------------------
# Implied volatility
# ---------------------------------------------------------------------------

class TestImpliedVolatility:
    def test_round_trip(self):
        """Price with known vol, then recover that vol from the price."""
        known_vol = 0.25
        price = black_scholes_price(100, 100, 0.05, known_vol, 1.0, "call")
        recovered = implied_volatility(price, 100, 100, 0.05, 1.0, "call")
        assert recovered == pytest.approx(known_vol, abs=0.001)

    def test_put_iv(self):
        known_vol = 0.30
        price = black_scholes_price(100, 110, 0.05, known_vol, 0.5, "put")
        recovered = implied_volatility(price, 100, 110, 0.05, 0.5, "put")
        assert recovered == pytest.approx(known_vol, abs=0.001)


# ---------------------------------------------------------------------------
# Greeks
# ---------------------------------------------------------------------------

class TestGreeks:
    def test_atm_call_delta(self):
        """Delta of an ATM call should be roughly 0.5 (slightly above due to drift)."""
        g = greeks(100, 100, 0.05, 0.20, 1.0, "call")
        assert 0.45 < g["delta"] < 0.70

    def test_atm_put_delta(self):
        """Delta of an ATM put should be roughly -0.5."""
        g = greeks(100, 100, 0.05, 0.20, 1.0, "put")
        assert -0.70 < g["delta"] < -0.30

    def test_gamma_positive(self):
        """Gamma should always be positive for long vanilla options."""
        g = greeks(100, 100, 0.05, 0.20, 1.0, "call")
        assert g["gamma"] > 0

    def test_vega_positive(self):
        """Vega should be positive (option value increases with vol)."""
        g = greeks(100, 100, 0.05, 0.20, 1.0, "call")
        assert g["vega"] > 0

    def test_theta_negative_for_long(self):
        """Theta should be negative (time decay erodes value)."""
        g = greeks(100, 100, 0.05, 0.20, 1.0, "call")
        assert g["theta"] < 0

    def test_put_call_delta_relationship(self):
        """delta_call - delta_put should be approximately 1."""
        g_call = greeks(100, 100, 0.05, 0.20, 1.0, "call")
        g_put = greeks(100, 100, 0.05, 0.20, 1.0, "put")
        assert (g_call["delta"] - g_put["delta"]) == pytest.approx(1.0, abs=0.01)


# ---------------------------------------------------------------------------
# American option pricing
# ---------------------------------------------------------------------------

class TestAmericanOption:
    def test_american_put_geq_european(self):
        """American put should be >= European put (early exercise premium)."""
        eu = black_scholes_price(100, 100, 0.05, 0.20, 1.0, "put")
        am = price_american_option(100, 100, 0.05, 0.20, 1.0, "put")
        assert am >= eu - 0.01  # small tolerance for numerical noise

    def test_american_call_equals_european(self):
        """For non-dividend stock, American call = European call."""
        eu = black_scholes_price(100, 100, 0.05, 0.20, 1.0, "call")
        am = price_american_option(100, 100, 0.05, 0.20, 1.0, "call")
        assert am == pytest.approx(eu, abs=0.10)


# ---------------------------------------------------------------------------
# OptionLeg model validation
# ---------------------------------------------------------------------------

class TestOptionLeg:
    def test_valid_call_leg(self):
        leg = OptionLeg(
            symbol="AAPL",
            strike=150.0,
            expiration=date(2025, 6, 20),
            option_type="call",
            side="buy",
            qty=5,
        )
        assert leg.symbol == "AAPL"
        assert leg.option_type == "call"
        assert leg.side == "buy"
        assert leg.qty == 5

    def test_valid_put_leg(self):
        leg = OptionLeg(
            symbol="SPY",
            strike=400.0,
            expiration=date(2025, 9, 19),
            option_type="put",
            side="sell",
            qty=1,
        )
        assert leg.option_type == "put"
        assert leg.side == "sell"

    def test_default_qty(self):
        leg = OptionLeg(
            symbol="MSFT",
            strike=300.0,
            expiration=date(2025, 12, 19),
            option_type="call",
            side="buy",
        )
        assert leg.qty == 1

    def test_invalid_option_type(self):
        with pytest.raises(Exception):
            OptionLeg(
                symbol="AAPL",
                strike=150.0,
                expiration=date(2025, 6, 20),
                option_type="straddle",  # type: ignore[arg-type]
                side="buy",
                qty=1,
            )

    def test_invalid_side(self):
        with pytest.raises(Exception):
            OptionLeg(
                symbol="AAPL",
                strike=150.0,
                expiration=date(2025, 6, 20),
                option_type="call",
                side="hold",  # type: ignore[arg-type]
                qty=1,
            )

    def test_qty_must_be_positive(self):
        with pytest.raises(Exception):
            OptionLeg(
                symbol="AAPL",
                strike=150.0,
                expiration=date(2025, 6, 20),
                option_type="call",
                side="buy",
                qty=0,
            )
