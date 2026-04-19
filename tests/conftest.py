"""Shared test fixtures."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from quant_trading_system.config import Settings
from quant_trading_system.models.trade import OrderRequest, OrderSide, OrderType, TimeInForce


@pytest.fixture
def paper_settings() -> Settings:
    """Settings configured for paper trading (safe defaults)."""
    return Settings(
        ANTHROPIC_API_KEY="test-key",
        ALPACA_API_KEY="test-alpaca-key",
        ALPACA_SECRET_KEY="test-alpaca-secret",
        ALPACA_PAPER=True,
        REAL_MONEY_ENABLED=False,
        REAL_MONEY_CONFIRMATION=False,
        DRY_RUN=False,
        LANGGRAPH_CHECKPOINTER="memory",
        _env_file=None,
    )


@pytest.fixture
def dry_run_settings() -> Settings:
    """Settings configured for dry-run mode."""
    return Settings(
        ANTHROPIC_API_KEY="test-key",
        ALPACA_API_KEY="test-alpaca-key",
        ALPACA_SECRET_KEY="test-alpaca-secret",
        ALPACA_PAPER=True,
        DRY_RUN=True,
        LANGGRAPH_CHECKPOINTER="memory",
        _env_file=None,
    )


@pytest.fixture
def live_settings() -> Settings:
    """Settings configured for live trading (both safety flags enabled)."""
    return Settings(
        ANTHROPIC_API_KEY="test-key",
        ALPACA_API_KEY="test-alpaca-key",
        ALPACA_SECRET_KEY="test-alpaca-secret",
        ALPACA_PAPER=False,
        REAL_MONEY_ENABLED=True,
        REAL_MONEY_CONFIRMATION=True,
        DRY_RUN=False,
        LANGGRAPH_CHECKPOINTER="memory",
        _env_file=None,
    )


@pytest.fixture
def mock_alpaca_client() -> MagicMock:
    """Mock AlpacaClient that returns sensible defaults."""
    client = MagicMock()
    client.get_account.return_value = {
        "equity": 100_000.0,
        "buying_power": 100_000.0,
        "cash": 100_000.0,
        "portfolio_value": 100_000.0,
        "day_trade_count": 0,
    }
    client.get_positions.return_value = []

    # Mock order submission
    mock_order = MagicMock()
    mock_order.id = "mock-order-123"
    mock_order.status.value = "accepted"
    mock_order.filled_qty = 0
    mock_order.filled_avg_price = 0
    client.submit_order.return_value = mock_order

    return client


@pytest.fixture
def sample_buy_order() -> OrderRequest:
    """A simple market buy order for testing."""
    return OrderRequest(
        symbol="AAPL",
        side=OrderSide.BUY,
        qty=10,
        order_type=OrderType.MARKET,
        time_in_force=TimeInForce.DAY,
        agent_name="test_agent",
        strategy_name="test_strategy",
        reasoning="Test order for unit testing",
    )


@pytest.fixture
def sample_limit_order() -> OrderRequest:
    """A limit buy order with a price for position size testing."""
    return OrderRequest(
        symbol="AAPL",
        side=OrderSide.BUY,
        qty=100,
        order_type=OrderType.LIMIT,
        time_in_force=TimeInForce.DAY,
        limit_price=150.0,
        agent_name="test_agent",
        strategy_name="test_strategy",
        reasoning="Test limit order",
    )
