"""Tests for application configuration and safety defaults."""

import pytest

from quant_trading_system.config import Settings


class TestDefaultSafety:
    """Verify that default configuration is always safe."""

    def test_default_is_paper_trading(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.ALPACA_PAPER is True
        assert settings.is_paper_trading is True
        assert settings.is_live_trading is False

    def test_default_real_money_disabled(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.REAL_MONEY_ENABLED is False
        assert settings.REAL_MONEY_CONFIRMATION is False

    def test_default_dry_run_off(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.DRY_RUN is False


class TestSafetyValidation:
    """Verify that unsafe configurations are rejected."""

    def test_live_without_enabled_flag_raises(self):
        with pytest.raises(ValueError, match="REAL_MONEY_ENABLED"):
            Settings(
                ALPACA_API_KEY="k",
                ALPACA_SECRET_KEY="s",
                ALPACA_PAPER=False,
                REAL_MONEY_ENABLED=False,
                REAL_MONEY_CONFIRMATION=True,
                _env_file=None,
            )

    def test_live_without_confirmation_flag_raises(self):
        with pytest.raises(ValueError, match="REAL_MONEY_CONFIRMATION"):
            Settings(
                ALPACA_API_KEY="k",
                ALPACA_SECRET_KEY="s",
                ALPACA_PAPER=False,
                REAL_MONEY_ENABLED=True,
                REAL_MONEY_CONFIRMATION=False,
                _env_file=None,
            )

    def test_live_without_both_flags_raises(self):
        with pytest.raises(ValueError):
            Settings(
                ALPACA_API_KEY="k",
                ALPACA_SECRET_KEY="s",
                ALPACA_PAPER=False,
                REAL_MONEY_ENABLED=False,
                REAL_MONEY_CONFIRMATION=False,
                _env_file=None,
            )

    def test_live_with_both_flags_succeeds(self):
        settings = Settings(
            ALPACA_API_KEY="k",
            ALPACA_SECRET_KEY="s",
            ALPACA_PAPER=False,
            REAL_MONEY_ENABLED=True,
            REAL_MONEY_CONFIRMATION=True,
            _env_file=None,
        )
        assert settings.is_live_trading is True
        assert settings.is_paper_trading is False


class TestRiskDefaults:
    """Verify risk limit defaults are conservative."""

    def test_position_size_limit(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.MAX_POSITION_SIZE_PCT == 0.10

    def test_max_concurrent_positions(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.MAX_CONCURRENT_POSITIONS == 20

    def test_daily_loss_limit(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.MAX_DAILY_LOSS_PCT == 0.02

    def test_drawdown_pause(self):
        settings = Settings(
            ALPACA_API_KEY="k", ALPACA_SECRET_KEY="s", _env_file=None
        )
        assert settings.MAX_DRAWDOWN_PAUSE_PCT == 0.15
