"""Tests for the SafetyGate — the most critical safety component.

Every test here verifies that the system cannot accidentally execute
real-money trades or violate risk limits.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from quant_trading_system.brokers.safety_gate import SafetyError, SafetyGate
from quant_trading_system.config import Settings
from quant_trading_system.models.trade import (
    OrderRequest,
    OrderSide,
    OrderStatus,
    OrderType,
    TimeInForce,
    TradingMode,
)


class TestDryRunMode:
    """Dry-run mode must NEVER call the broker."""

    def test_dry_run_returns_simulated_result(self, dry_run_settings, sample_buy_order):
        mock_client = MagicMock()
        gate = SafetyGate(dry_run_settings, mock_client)

        result = gate.validate_and_submit(sample_buy_order)

        assert result.status == OrderStatus.DRY_RUN
        assert result.mode == TradingMode.DRY_RUN
        assert result.order_id.startswith("dry-run-")
        assert result.filled_qty == sample_buy_order.qty

    def test_dry_run_never_calls_broker(self, dry_run_settings, sample_buy_order):
        mock_client = MagicMock()
        gate = SafetyGate(dry_run_settings, mock_client)

        gate.validate_and_submit(sample_buy_order)

        mock_client.submit_order.assert_not_called()
        mock_client.get_account.assert_not_called()
        mock_client.get_positions.assert_not_called()

    def test_dry_run_works_without_client(self, dry_run_settings, sample_buy_order):
        gate = SafetyGate(dry_run_settings, alpaca_client=None)
        result = gate.validate_and_submit(sample_buy_order)
        assert result.status == OrderStatus.DRY_RUN


class TestLiveMoneyGate:
    """Live trading must be blocked unless both safety flags are True."""

    def test_live_without_enabled_raises_safety_error(self, sample_buy_order):
        # Config validator should catch this at Settings creation
        with pytest.raises(ValueError):
            Settings(
                ALPACA_API_KEY="k",
                ALPACA_SECRET_KEY="s",
                ALPACA_PAPER=False,
                REAL_MONEY_ENABLED=False,
                REAL_MONEY_CONFIRMATION=True,
                _env_file=None,
            )

    def test_live_without_confirmation_raises_safety_error(self, sample_buy_order):
        # We need to bypass the config validator to test SafetyGate directly
        settings = MagicMock()
        settings.DRY_RUN = False
        settings.ALPACA_PAPER = False
        settings.REAL_MONEY_ENABLED = True
        settings.REAL_MONEY_CONFIRMATION = False
        settings.RESTRICTED_SYMBOLS = []

        gate = SafetyGate(settings, alpaca_client=MagicMock())

        with pytest.raises(SafetyError, match="REAL_MONEY_CONFIRMATION"):
            gate.validate_and_submit(sample_buy_order)

    def test_live_without_enabled_raises_at_gate(self, sample_buy_order):
        settings = MagicMock()
        settings.DRY_RUN = False
        settings.ALPACA_PAPER = False
        settings.REAL_MONEY_ENABLED = False
        settings.REAL_MONEY_CONFIRMATION = True
        settings.RESTRICTED_SYMBOLS = []

        gate = SafetyGate(settings, alpaca_client=MagicMock())

        with pytest.raises(SafetyError, match="REAL_MONEY_ENABLED"):
            gate.validate_and_submit(sample_buy_order)

    def test_live_without_both_flags_raises_at_gate(self, sample_buy_order):
        settings = MagicMock()
        settings.DRY_RUN = False
        settings.ALPACA_PAPER = False
        settings.REAL_MONEY_ENABLED = False
        settings.REAL_MONEY_CONFIRMATION = False
        settings.RESTRICTED_SYMBOLS = []

        gate = SafetyGate(settings, alpaca_client=MagicMock())

        with pytest.raises(SafetyError):
            gate.validate_and_submit(sample_buy_order)


class TestPaperTradingPassthrough:
    """Paper trading orders should pass through safety checks normally."""

    def test_paper_order_submits_successfully(
        self, paper_settings, mock_alpaca_client, sample_buy_order
    ):
        gate = SafetyGate(paper_settings, mock_alpaca_client)
        result = gate.validate_and_submit(sample_buy_order)

        assert result.status == OrderStatus.SUBMITTED
        assert result.mode == TradingMode.PAPER
        assert "paper_trading_mode" in result.safety_checks_passed

    def test_paper_mode_in_result(self, paper_settings, mock_alpaca_client, sample_buy_order):
        gate = SafetyGate(paper_settings, mock_alpaca_client)
        result = gate.validate_and_submit(sample_buy_order)
        assert result.mode == TradingMode.PAPER


class TestPositionSizeLimit:
    """Orders exceeding position size limits must be rejected."""

    def test_oversized_position_rejected(self, paper_settings, mock_alpaca_client):
        # 100k equity, limit is 10%, so 15k order should be rejected
        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=100,
            order_type=OrderType.LIMIT,
            limit_price=150.0,  # 100 * 150 = 15k = 15% of 100k
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(paper_settings, mock_alpaca_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.REJECTED
        assert "position_size" in result.safety_checks_failed

    def test_acceptable_position_passes(self, paper_settings, mock_alpaca_client):
        # 100k equity, limit is 10%, so 5k order should pass
        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=10,
            order_type=OrderType.LIMIT,
            limit_price=150.0,  # 10 * 150 = 1.5k = 1.5% of 100k
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(paper_settings, mock_alpaca_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.SUBMITTED

    def test_market_order_without_price_skips_size_check(
        self, paper_settings, mock_alpaca_client, sample_buy_order
    ):
        """Market orders without limit_price skip position size check."""
        gate = SafetyGate(paper_settings, mock_alpaca_client)
        result = gate.validate_and_submit(sample_buy_order)
        assert result.status == OrderStatus.SUBMITTED
        assert "position_size" in result.safety_checks_passed


class TestDailyLossLimit:
    """Orders should be rejected when daily losses exceed threshold."""

    def test_daily_loss_exceeds_limit_rejects(self, paper_settings):
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "equity": 100_000.0,
            "buying_power": 97_000.0,
            "cash": 97_000.0,
            "portfolio_value": 97_000.0,
        }
        # Positions with large unrealized losses (> 2% of 100k = $2000)
        mock_client.get_positions.return_value = [
            {"symbol": "AAPL", "unrealized_pl": -2500.0},
        ]
        mock_order = MagicMock()
        mock_order.id = "mock-123"
        mock_order.status.value = "accepted"
        mock_order.filled_qty = 0
        mock_order.filled_avg_price = 0
        mock_client.submit_order.return_value = mock_order

        order = OrderRequest(
            symbol="MSFT",
            side=OrderSide.BUY,
            qty=5,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(paper_settings, mock_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.REJECTED
        assert "daily_loss" in result.safety_checks_failed


class TestMaxConcurrentPositions:
    """Orders should be rejected at max concurrent positions."""

    def test_at_max_positions_rejects_buy(self, paper_settings):
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "equity": 100_000.0,
            "buying_power": 50_000.0,
            "cash": 50_000.0,
            "portfolio_value": 100_000.0,
        }
        # Create 20 positions (the max)
        mock_client.get_positions.return_value = [
            {"symbol": f"SYM{i}", "unrealized_pl": 0.0} for i in range(20)
        ]
        mock_order = MagicMock()
        mock_order.id = "mock-123"
        mock_order.status.value = "accepted"
        mock_order.filled_qty = 0
        mock_order.filled_avg_price = 0
        mock_client.submit_order.return_value = mock_order

        order = OrderRequest(
            symbol="NEWSTOCK",
            side=OrderSide.BUY,
            qty=5,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(paper_settings, mock_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.REJECTED
        assert "max_positions" in result.safety_checks_failed

    def test_sell_allowed_at_max_positions(self, paper_settings):
        """Sells should be allowed even at max positions (reducing exposure)."""
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "equity": 100_000.0,
            "buying_power": 50_000.0,
            "cash": 50_000.0,
            "portfolio_value": 100_000.0,
        }
        mock_client.get_positions.return_value = [
            {"symbol": f"SYM{i}", "unrealized_pl": 0.0} for i in range(20)
        ]
        mock_order = MagicMock()
        mock_order.id = "mock-123"
        mock_order.status.value = "accepted"
        mock_order.filled_qty = 5
        mock_order.filled_avg_price = 150.0
        mock_client.submit_order.return_value = mock_order

        order = OrderRequest(
            symbol="SYM0",
            side=OrderSide.SELL,
            qty=5,
            agent_name="test",
            strategy_name="test",
            reasoning="Reducing position",
        )
        gate = SafetyGate(paper_settings, mock_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.SUBMITTED


class TestRestrictedSymbols:
    """Orders for restricted symbols must be rejected."""

    def test_restricted_symbol_rejected(self, mock_alpaca_client):
        settings = Settings(
            ALPACA_API_KEY="k",
            ALPACA_SECRET_KEY="s",
            ALPACA_PAPER=True,
            RESTRICTED_SYMBOLS="GME,AMC",
            _env_file=None,
        )
        order = OrderRequest(
            symbol="GME",
            side=OrderSide.BUY,
            qty=10,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(settings, mock_alpaca_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.REJECTED
        assert "restricted_symbol" in result.safety_checks_failed

    def test_non_restricted_symbol_passes(self, paper_settings, mock_alpaca_client):
        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=10,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(paper_settings, mock_alpaca_client)
        result = gate.validate_and_submit(order)
        assert result.status == OrderStatus.SUBMITTED


class TestLiveTradingWithBothFlags:
    """Live trading should work when properly configured."""

    def test_live_order_passes_with_both_flags(self, live_settings):
        mock_client = MagicMock()
        mock_client.get_account.return_value = {
            "equity": 100_000.0,
            "buying_power": 100_000.0,
            "cash": 100_000.0,
            "portfolio_value": 100_000.0,
        }
        mock_client.get_positions.return_value = []
        mock_order = MagicMock()
        mock_order.id = "live-order-123"
        mock_order.status.value = "accepted"
        mock_order.filled_qty = 10
        mock_order.filled_avg_price = 150.0
        mock_client.submit_order.return_value = mock_order

        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=10,
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        gate = SafetyGate(live_settings, mock_client)
        result = gate.validate_and_submit(order)

        assert result.status == OrderStatus.SUBMITTED
        assert result.mode == TradingMode.LIVE
        assert "live_money_gate" in result.safety_checks_passed


class TestSafetyGateWithoutClient:
    """SafetyGate should work without a broker client (for testing)."""

    def test_no_client_returns_simulated_submit(self, paper_settings, sample_buy_order):
        gate = SafetyGate(paper_settings, alpaca_client=None)
        result = gate.validate_and_submit(sample_buy_order)

        assert result.status == OrderStatus.SUBMITTED
        assert result.order_id.startswith("no-client-")

    def test_no_client_skips_position_checks(self, paper_settings, sample_buy_order):
        gate = SafetyGate(paper_settings, alpaca_client=None)
        result = gate.validate_and_submit(sample_buy_order)
        # Should still have all check names in passed list
        assert "position_size" in result.safety_checks_passed
        assert "daily_loss" in result.safety_checks_passed
        assert "max_positions" in result.safety_checks_passed
