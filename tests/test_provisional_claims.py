"""Tests for Option 3 / mandatory-attach provisional claims.

Covers:
  1. The provisional-claim memory helpers (append/read/clear/symbols round-trip).
  2. The execution gate in run_active_strategies — provisional symbols are
     attached for coverage but never passed to a strategy for execution, and a
     strategy whose entire claim is provisional is skipped entirely (rather than
     falling back to its frontmatter universe and trading MORE).
"""

from __future__ import annotations

import datetime as dt

import pytest

from quant_trading_system import memory, strategy_runtime
from quant_trading_system import universe as universe_mod
from quant_trading_system.memory import ActiveStrategyClaim


@pytest.fixture
def temp_provisional_file(tmp_path, monkeypatch):
    """Redirect the provisional-claims file to a temp path."""
    f = tmp_path / "provisional_claims.md"
    monkeypatch.setattr(memory, "PROVISIONAL_CLAIMS_FILE", f)
    # _ensure_dirs() touches KB dirs; make sure parent exists.
    monkeypatch.setattr(memory, "_ensure_dirs", lambda: None)
    return f


def test_append_read_round_trip(temp_provisional_file):
    assert memory.read_provisional_claims() == []
    pc = memory.append_provisional_claim(
        "spcx",
        strategy_id="equity_trend_following_ema_cross",
        gap_type="volatility_regime",
        reason="no price history; attached best-available",
        sharpe=None,
        baseline_sharpe=0.5,
    )
    assert pc.symbol == "SPCX"
    claims = memory.read_provisional_claims()
    assert len(claims) == 1
    c = claims[0]
    assert c.symbol == "SPCX"
    assert c.strategy_id == "equity_trend_following_ema_cross"
    assert c.sharpe is None
    # revalidate_by is provisional_since + the default horizon.
    since = dt.date.fromisoformat(c.provisional_since)
    by = dt.date.fromisoformat(c.revalidate_by)
    assert (by - since).days == memory.PROVISIONAL_REVALIDATION_DAYS


def test_append_is_idempotent_per_symbol(temp_provisional_file):
    memory.append_provisional_claim(
        "SPCX", strategy_id="s1", gap_type="g", reason="r1")
    memory.append_provisional_claim(
        "SPCX", strategy_id="s2", gap_type="g", reason="r2")
    claims = memory.read_provisional_claims()
    assert len(claims) == 1
    assert claims[0].strategy_id == "s2"  # refreshed, not duplicated


def test_clear_and_symbols(temp_provisional_file):
    memory.append_provisional_claim("AAA", strategy_id="s", gap_type="g", reason="r")
    memory.append_provisional_claim("BBB", strategy_id="s", gap_type="g", reason="r")
    assert memory.provisional_claim_symbols() == {"AAA", "BBB"}
    assert memory.clear_provisional_claim("aaa") is True
    assert memory.provisional_claim_symbols() == {"BBB"}
    assert memory.clear_provisional_claim("AAA") is False  # already gone


def _patch_runtime(monkeypatch, claims, provisional, recorder):
    """Stub run_active_strategies' collaborators so we can inspect what each
    strategy was asked to trade."""
    monkeypatch.setattr(memory, "read_active_strategies", lambda: claims)
    monkeypatch.setattr(memory, "provisional_claim_symbols", lambda: provisional)
    monkeypatch.setattr(memory, "unclaimed_symbols", lambda *_a, **_k: [])

    def fake_run_strategy(strategy_id, **kwargs):
        recorder[strategy_id] = kwargs.get("claimed_symbols")
        return {"ok": True, "submitted": [], "rejected": [], "errors": []}

    monkeypatch.setattr(strategy_runtime, "run_strategy", fake_run_strategy)

    class _Univ:
        symbols = ["AAPL", "SPY", "SPCX"]

    monkeypatch.setattr(universe_mod, "compute_universe", lambda *_a, **_k: _Univ())


def test_execution_gate_subtracts_provisional(monkeypatch):
    """A strategy with mixed validated + provisional symbols runs on the
    validated ones only; the provisional symbol is reported under skipped."""
    recorder: dict[str, object] = {}
    claims = [
        ActiveStrategyClaim(
            strategy_id="equity_trend_following_ema_cross",
            symbols=["AAPL", "SPY", "SPCX"],
            since="2026-06-16",
            reason="x",
        ),
    ]
    _patch_runtime(monkeypatch, claims, {"SPCX"}, recorder)

    out = strategy_runtime.run_active_strategies(
        settings=None, market_data=None, regime_classifier=None,
        safety_gate=None, alpaca_client=None, run_id="t",
    )

    assert out["ok"] is True
    # Strategy ran, but only on the validated slice.
    assert recorder["equity_trend_following_ema_cross"] == ["AAPL", "SPY"]
    assert out["provisional_quarantined"] == ["SPCX"]
    assert any(s["symbols"] == ["SPCX"] for s in out["skipped"])


def test_execution_gate_skips_all_provisional_strategy(monkeypatch):
    """A strategy whose ENTIRE claim is provisional is skipped — it must NOT
    run with claimed_symbols=None (which would trade its frontmatter universe)."""
    recorder: dict[str, object] = {}
    claims = [
        ActiveStrategyClaim(
            strategy_id="solo_provisional",
            symbols=["SPCX"],
            since="2026-06-16",
            reason="x",
        ),
        ActiveStrategyClaim(
            strategy_id="normal",
            symbols=["AAPL"],
            since="2026-06-16",
            reason="x",
        ),
    ]
    _patch_runtime(monkeypatch, claims, {"SPCX"}, recorder)

    out = strategy_runtime.run_active_strategies(
        settings=None, market_data=None, regime_classifier=None,
        safety_gate=None, alpaca_client=None, run_id="t",
    )

    # solo_provisional was never run.
    assert "solo_provisional" not in recorder
    # normal strategy ran on its validated symbol.
    assert recorder["normal"] == ["AAPL"]


def test_empty_provisional_is_noop(monkeypatch):
    """When nothing is provisional, behaviour is identical to before — each
    strategy runs on its full claim."""
    recorder: dict[str, object] = {}
    claims = [
        ActiveStrategyClaim(
            strategy_id="normal",
            symbols=["AAPL", "SPY"],
            since="2026-06-16",
            reason="x",
        ),
    ]
    _patch_runtime(monkeypatch, claims, set(), recorder)

    out = strategy_runtime.run_active_strategies(
        settings=None, market_data=None, regime_classifier=None,
        safety_gate=None, alpaca_client=None, run_id="t",
    )

    assert recorder["normal"] == ["AAPL", "SPY"]
    assert out["provisional_quarantined"] == []
    assert out["skipped"] == []
