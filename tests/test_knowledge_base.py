"""Tests for the knowledge base: strategy loading, ChromaDB, and search."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from quant_trading_system.config import Settings
from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient
from quant_trading_system.knowledge_base.strategy_loader import StrategyLoader
from quant_trading_system.models.strategy import (
    Conclusion,
    ConclusionType,
    Recommendation,
    Strategy,
    StrategyStatus,
    StrategyType,
)


@pytest.fixture
def temp_chroma_dir():
    """Temporary directory for ChromaDB test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def kb_settings(temp_chroma_dir):
    """Settings with temporary ChromaDB directory."""
    return Settings(
        ALPACA_API_KEY="test",
        ALPACA_SECRET_KEY="test",
        CHROMA_PERSIST_DIR=temp_chroma_dir,
        _env_file=None,
    )


@pytest.fixture
def kb_client(kb_settings):
    """ChromaDB knowledge base client."""
    return KnowledgeBaseClient(kb_settings)


@pytest.fixture
def strategy_loader():
    """Strategy loader pointing to the real strategies directory."""
    strategies_dir = Path(__file__).parent.parent / "quant_trading_system" / "knowledge_base" / "strategies"
    return StrategyLoader(strategies_dir)


class TestStrategyLoader:
    """Test loading strategies from Markdown files."""

    def test_loads_all_strategies(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        # 10 equity + 8 options = 18 total
        assert len(strategies) >= 18

    def test_equity_strategies_loaded(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        equity = [s for s in strategies if s.type == StrategyType.EQUITY]
        assert len(equity) >= 10

    def test_options_strategies_loaded(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        options = [s for s in strategies if s.type == StrategyType.OPTIONS]
        assert len(options) >= 8

    def test_strategies_have_required_fields(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        for s in strategies:
            assert s.id, f"Strategy missing id: {s.name}"
            assert s.name, f"Strategy missing name: {s.id}"
            assert s.type in (StrategyType.EQUITY, StrategyType.OPTIONS)
            assert s.content, f"Strategy missing content: {s.id}"

    def test_strategies_have_indicators(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        for s in strategies:
            assert len(s.indicators) > 0, f"Strategy {s.id} has no indicators"

    def test_bollinger_strategy_details(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        bb = next((s for s in strategies if "bollinger" in s.id), None)
        assert bb is not None
        assert "bollinger" in bb.name.lower() or "bollinger" in bb.id.lower()
        assert bb.type == StrategyType.EQUITY

    def test_iron_condor_strategy_details(self, strategy_loader):
        strategies = strategy_loader.load_all_strategies()
        ic = next((s for s in strategies if "iron_condor" in s.id), None)
        assert ic is not None
        assert ic.type == StrategyType.OPTIONS


class TestChromaDBOperations:
    """Test ChromaDB CRUD and search operations."""

    def test_add_and_get_strategy(self, kb_client):
        strategy = Strategy(
            id="test_strategy",
            name="Test Strategy",
            type=StrategyType.EQUITY,
            timeframes=["swing"],
            indicators=["rsi", "macd"],
            content="Buy when RSI is oversold and MACD crosses up.",
            status=StrategyStatus.ACTIVE,
        )
        kb_client.add_strategy(strategy)

        result = kb_client.get_strategy("test_strategy")
        assert result is not None
        assert result["id"] == "test_strategy"
        assert "RSI" in result["content"]

    def test_search_strategies(self, kb_client):
        # Add a few strategies
        kb_client.add_strategy(Strategy(
            id="momentum_1",
            name="Momentum Strategy",
            type=StrategyType.EQUITY,
            indicators=["rsi", "macd"],
            content="A momentum strategy using RSI and MACD crossovers for trend following.",
        ))
        kb_client.add_strategy(Strategy(
            id="mean_rev_1",
            name="Mean Reversion",
            type=StrategyType.EQUITY,
            indicators=["bollinger_bands"],
            content="A mean reversion strategy using Bollinger Bands for oversold conditions.",
        ))

        # Search should return relevant results
        results = kb_client.search_strategies("oversold mean reversion bollinger")
        assert len(results) > 0
        # Mean reversion should rank higher for this query
        ids = [r["id"] for r in results]
        assert "mean_rev_1" in ids

    def test_search_by_type_filter(self, kb_client):
        kb_client.add_strategy(Strategy(
            id="equity_strat",
            name="Equity Strat",
            type=StrategyType.EQUITY,
            indicators=["sma"],
            content="A simple equity strategy.",
        ))
        kb_client.add_strategy(Strategy(
            id="options_strat",
            name="Options Strat",
            type=StrategyType.OPTIONS,
            indicators=["iv_rank"],
            content="A simple options strategy.",
        ))

        equity_results = kb_client.search_strategies(
            "strategy", strategy_type="equity"
        )
        assert all(r["metadata"].get("type") == "equity" for r in equity_results)

    def test_delete_strategy(self, kb_client):
        kb_client.add_strategy(Strategy(
            id="to_delete",
            name="Delete Me",
            type=StrategyType.EQUITY,
            indicators=["sma"],
            content="This will be deleted.",
        ))
        kb_client.delete_strategy("to_delete")
        result = kb_client.get_strategy("to_delete")
        assert result is None

    def test_upsert_updates_existing(self, kb_client):
        strategy = Strategy(
            id="upsert_test",
            name="Original Name",
            type=StrategyType.EQUITY,
            indicators=["sma"],
            content="Original content.",
        )
        kb_client.add_strategy(strategy)

        # Update
        strategy.name = "Updated Name"
        strategy.content = "Updated content with new rules."
        kb_client.add_strategy(strategy)

        result = kb_client.get_strategy("upsert_test")
        assert "Updated" in result["content"]


class TestConclusionStorage:
    """Test conclusion storage and retrieval."""

    def test_add_and_search_conclusion(self, kb_client):
        conclusion = Conclusion(
            id="test_conclusion_1",
            conclusion_type=ConclusionType.BACKTEST_RESULT,
            strategy_id="mean_reversion_bollinger",
            summary="Backtested on SPY 2020-2024. Sharpe 1.3, max drawdown 12%.",
            metrics={"sharpe": 1.3, "max_drawdown": 0.12, "win_rate": 0.58},
            recommendation=Recommendation.PROMOTE,
        )
        kb_client.add_conclusion(conclusion)

        results = kb_client.search_conclusions("mean reversion backtest results")
        assert len(results) > 0
        assert results[0]["metadata"]["strategy_id"] == "mean_reversion_bollinger"

    def test_conclusion_with_metrics(self, kb_client):
        conclusion = Conclusion(
            id="test_conclusion_2",
            conclusion_type=ConclusionType.LIVE_TRADE_RESULT,
            strategy_id="ema_cross",
            summary="Live paper trade on AAPL. Won 3/5 trades.",
            metrics={"win_rate": 0.6, "avg_return": 0.015},
            recommendation=Recommendation.WATCH,
        )
        kb_client.add_conclusion(conclusion)

        results = kb_client.search_conclusions("AAPL trade results")
        assert len(results) > 0


class TestSyncToChroma:
    """Test syncing strategy files to ChromaDB."""

    def test_sync_loads_all_strategies(self, kb_client, strategy_loader):
        count = strategy_loader.sync_to_chroma(kb_client)
        assert count >= 18

        # Verify we can search for synced strategies
        results = kb_client.search_strategies("high volatility options strategy")
        assert len(results) > 0

    def test_synced_strategies_searchable(self, kb_client, strategy_loader):
        strategy_loader.sync_to_chroma(kb_client)

        # Search for iron condor
        results = kb_client.search_strategies("iron condor high implied volatility")
        assert len(results) > 0
        # Iron condor should be in the results
        ids = [r["id"] for r in results]
        assert any("iron_condor" in id_ for id_ in ids)

    def test_get_all_strategies(self, kb_client, strategy_loader):
        strategy_loader.sync_to_chroma(kb_client)
        all_strats = kb_client.get_all_strategies()
        assert len(all_strats) >= 18
