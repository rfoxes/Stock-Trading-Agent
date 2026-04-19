"""Tests for the RiskManagerAgent."""

from __future__ import annotations

import pytest

from quant_trading_system.config import Settings
from quant_trading_system.models.trade import OrderRequest, OrderSide


@pytest.fixture
def risk_settings():
    return Settings(
        ALPACA_API_KEY="test",
        ALPACA_SECRET_KEY="test",
        MAX_POSITION_SIZE_PCT=0.10,
        MAX_SECTOR_CONCENTRATION_PCT=0.25,
        MAX_DRAWDOWN_PAUSE_PCT=0.15,
        _env_file=None,
    )


@pytest.fixture
def risk_manager(risk_settings):
    from quant_trading_system.agents.risk_manager import RiskManagerAgent
    return RiskManagerAgent(risk_settings)


@pytest.fixture
def empty_portfolio():
    return {
        "equity": 100_000.0,
        "cash": 100_000.0,
        "positions": [],
        "unrealized_pnl": 0.0,
    }


@pytest.fixture
def portfolio_with_tech():
    return {
        "equity": 100_000.0,
        "cash": 50_000.0,
        "positions": [
            {"symbol": "AAPL", "market_value": 15_000.0, "unrealized_pl": 500.0},
            {"symbol": "MSFT", "market_value": 15_000.0, "unrealized_pl": -200.0},
            {"symbol": "GOOGL", "market_value": 10_000.0, "unrealized_pl": 100.0},
        ],
        "unrealized_pnl": 400.0,
    }


class TestOrderEvaluation:
    """Test individual order risk evaluation."""

    def test_order_approved_empty_portfolio(self, risk_manager, empty_portfolio):
        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=10,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        result = risk_manager.evaluate_order(order, empty_portfolio)
        assert result["approved"] is True

    def test_drawdown_circuit_breaker(self, risk_manager):
        """Large drawdown should trigger circuit breaker."""
        portfolio = {
            "equity": 84_000.0,  # 16% drawdown from 100k (exceeds 15% threshold)
            "cash": 4_000.0,
            "positions": [
                {"symbol": "AAPL", "market_value": 80_000.0, "unrealized_pl": -16_000.0},
            ],
            "unrealized_pnl": -16_000.0,
            "peak_equity": 100_000.0,
        }
        order = OrderRequest(
            symbol="MSFT",
            side=OrderSide.BUY,
            qty=10,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        result = risk_manager.evaluate_order(order, portfolio)
        assert result["approved"] is False
        assert "drawdown" in result["reason"].lower()


class TestPortfolioEvaluation:
    """Test portfolio-level risk assessment."""

    def test_empty_portfolio_low_risk(self, risk_manager, empty_portfolio):
        result = risk_manager.evaluate_portfolio(empty_portfolio)
        assert result["risk_level"] in ("low", "medium")
        assert result["circuit_breaker_active"] is False

    def test_tech_heavy_portfolio(self, risk_manager, portfolio_with_tech):
        result = risk_manager.evaluate_portfolio(portfolio_with_tech)
        # Should identify tech concentration
        assert isinstance(result["sector_exposures"], dict)
        assert isinstance(result["warnings"], list)

    def test_circuit_breaker_triggers(self, risk_manager):
        portfolio = {
            "equity": 80_000.0,
            "cash": 0.0,
            "positions": [
                {"symbol": "AAPL", "market_value": 80_000.0, "unrealized_pl": -20_000.0},
            ],
            "unrealized_pnl": -20_000.0,
            "peak_equity": 100_000.0,
        }
        result = risk_manager.evaluate_portfolio(portfolio)
        assert result["circuit_breaker_active"] is True
