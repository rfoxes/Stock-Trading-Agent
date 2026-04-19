"""Tests for dry-run mode end-to-end."""

from __future__ import annotations

import pytest

from quant_trading_system.config import Settings
from quant_trading_system.brokers.safety_gate import SafetyGate
from quant_trading_system.models.trade import (
    OrderRequest,
    OrderSide,
    OrderStatus,
    TradingMode,
)


@pytest.fixture
def dry_run_settings():
    return Settings(
        ALPACA_API_KEY="test",
        ALPACA_SECRET_KEY="test",
        DRY_RUN=True,
        ALPACA_PAPER=True,
        _env_file=None,
    )


class TestDryRunMode:
    """Verify dry-run mode works correctly end-to-end."""

    def test_dry_run_all_order_types(self, dry_run_settings):
        """All order types should succeed in dry-run."""
        from quant_trading_system.models.trade import OrderType

        gate = SafetyGate(dry_run_settings)

        for order_type in OrderType:
            order = OrderRequest(
                symbol="AAPL",
                side=OrderSide.BUY,
                qty=10,
                order_type=order_type,
                limit_price=150.0 if order_type in (OrderType.LIMIT, OrderType.STOP_LIMIT) else None,
                stop_price=145.0 if order_type in (OrderType.STOP, OrderType.STOP_LIMIT) else None,
                agent_name="test",
                strategy_name="test",
                reasoning=f"Testing {order_type.value}",
            )
            result = gate.validate_and_submit(order)
            assert result.status == OrderStatus.DRY_RUN
            assert result.mode == TradingMode.DRY_RUN

    def test_dry_run_preserves_order_details(self, dry_run_settings):
        """Dry-run result should contain the original request."""
        gate = SafetyGate(dry_run_settings)

        order = OrderRequest(
            symbol="TSLA",
            side=OrderSide.SELL,
            qty=50,
            agent_name="swing_agent",
            strategy_name="mean_reversion",
            reasoning="RSI oversold bounce",
        )
        result = gate.validate_and_submit(order)

        assert result.original_request is not None
        assert result.original_request.symbol == "TSLA"
        assert result.original_request.agent_name == "swing_agent"
        assert result.filled_qty == 50

    def test_dry_run_no_client_needed(self, dry_run_settings):
        """Dry-run should work without any broker client."""
        gate = SafetyGate(dry_run_settings, alpaca_client=None)

        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=10,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        result = gate.validate_and_submit(order)
        assert result.status == OrderStatus.DRY_RUN

    def test_dry_run_bypasses_all_checks(self, dry_run_settings):
        """Dry-run should not check position size, daily loss, etc."""
        gate = SafetyGate(dry_run_settings)

        # Absurdly large order that would normally fail checks
        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=999_999,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        result = gate.validate_and_submit(order)
        assert result.status == OrderStatus.DRY_RUN
        assert result.filled_qty == 999_999
