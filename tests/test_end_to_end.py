"""End-to-end integration tests.

These tests verify the complete pipeline from supervisor to order execution
using DRY_RUN mode and mocked LLM responses.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from quant_trading_system.config import Settings


@pytest.fixture
def e2e_settings(tmp_path):
    """Settings for end-to-end testing."""
    return Settings(
        ANTHROPIC_API_KEY="test-key",
        ALPACA_API_KEY="test-key",
        ALPACA_SECRET_KEY="test-secret",
        ALPACA_PAPER=True,
        DRY_RUN=True,
        LANGGRAPH_CHECKPOINTER="memory",
        CHROMA_PERSIST_DIR=str(tmp_path / "chroma"),
        DEFAULT_WATCHLIST="SPY",
        _env_file=None,
    )


class TestSafetyInvariant:
    """The most important test: safety invariant holds end-to-end."""

    def test_dry_run_never_touches_broker(self, e2e_settings):
        """In dry-run mode, no broker calls should ever happen."""
        from quant_trading_system.brokers.safety_gate import SafetyGate
        from quant_trading_system.models.trade import (
            OrderRequest,
            OrderSide,
            OrderStatus,
            TradingMode,
        )

        mock_client = MagicMock()
        gate = SafetyGate(e2e_settings, mock_client)

        # Submit 10 orders
        for i in range(10):
            order = OrderRequest(
                symbol=f"SYM{i}",
                side=OrderSide.BUY,
                qty=10,
                agent_name="test",
                strategy_name="test",
                reasoning="e2e test",
            )
            result = gate.validate_and_submit(order)
            assert result.status == OrderStatus.DRY_RUN
            assert result.mode == TradingMode.DRY_RUN

        # Verify NO broker calls whatsoever
        mock_client.submit_order.assert_not_called()
        mock_client.get_account.assert_not_called()
        mock_client.get_positions.assert_not_called()

    def test_paper_mode_default(self):
        """Default settings must always be paper trading."""
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.is_paper_trading is True
        assert settings.is_live_trading is False
        assert settings.REAL_MONEY_ENABLED is False
        assert settings.REAL_MONEY_CONFIRMATION is False


class TestKnowledgeBaseIntegration:
    """Test that strategies load and are searchable."""

    def test_seed_and_search(self, e2e_settings):
        """Seed KB and verify semantic search works."""
        from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient
        from quant_trading_system.knowledge_base.strategy_loader import StrategyLoader

        kb = KnowledgeBaseClient(e2e_settings)
        loader = StrategyLoader()
        count = loader.sync_to_chroma(kb)

        assert count >= 18

        # Search for options strategies
        results = kb.search_strategies("high volatility options selling strategy")
        assert len(results) > 0

        # Search for equity strategies
        results = kb.search_strategies("mean reversion oversold bouncing")
        assert len(results) > 0


class TestConfigSafety:
    """Additional config safety tests."""

    def test_cannot_create_live_config_without_flags(self):
        with pytest.raises(ValueError):
            Settings(
                ALPACA_API_KEY="k",
                ALPACA_SECRET_KEY="s",
                ALPACA_PAPER=False,
                _env_file=None,
            )

    def test_dry_run_overrides_everything(self, e2e_settings):
        """DRY_RUN=True should bypass all safety checks."""
        from quant_trading_system.brokers.safety_gate import SafetyGate
        from quant_trading_system.models.trade import OrderRequest, OrderSide, OrderStatus

        gate = SafetyGate(e2e_settings)

        # Even with no client, dry run should work
        order = OrderRequest(
            symbol="AAPL",
            side=OrderSide.BUY,
            qty=100000,  # Absurdly large
            agent_name="test",
            strategy_name="test",
            reasoning="test",
        )
        result = gate.validate_and_submit(order)
        assert result.status == OrderStatus.DRY_RUN
