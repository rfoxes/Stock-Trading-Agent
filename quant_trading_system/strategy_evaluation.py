"""Test-driven strategy curation. Removes agent discretion from add / update /
archive decisions.

The Saturday research agent gathers candidates; this module runs a battery of
statistical tests on them and emits a deterministic decision. The agent
applies the decision verbatim — it does NOT override.

Three deciders, three call signatures:

    evaluate_for_addition(strategy_id, symbol, start, end, ...)
        -> {"decision": "ADD" | "REJECT", "reasons": [...], "metrics": {...}}

    evaluate_for_replacement(existing_id, candidate_id, symbol, start, end, ...)
        -> {"decision": "REPLACE" | "KEEP", "reasons": [...], "metrics": {...}}

    evaluate_for_archive(strategy_id, ...)
        -> {"decision": "ARCHIVE" | "KEEP", "reasons": [...], "metrics": {...}}

Run on the same data, these return the same answer. There is no judgment.

The thresholds are concentrated here so they're easy to audit and tune. They
are documented in `state/research_manual.md`.
"""

from __future__ import annotations

import datetime as dt
import logging
import math
import random
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from quant_trading_system import journal, memory
from quant_trading_system.strategy_backtest import (
    GateThresholds,
    _probabilistic_sharpe_ratio,
    run_backtest,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Thresholds (documented in research_manual.md)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AdditionThresholds:
    # Statistical significance
    min_psr: float = 0.95
    min_oos_to_is_sharpe_ratio: float = 0.50  # OOS Sharpe must be >= 50% of IS
    # Risk-adjusted return
    min_sortino: float = 0.5
    # Tail risk
    max_drawdown_floor: float = -0.30
    # Sample size
    min_num_trades: int = 20
    # Walk-forward window split (fraction in-sample)
    is_fraction: float = 0.70


@dataclass(frozen=True)
class ReplacementThresholds:
    # Paired bootstrap on trade returns
    bootstrap_iters: int = 5000
    max_p_value: float = 0.05  # candidate must beat existing at p < 0.05
    # Sharpe must improve by at least a CI-width-equivalent
    min_sharpe_delta: float = 0.10  # absolute Sharpe units


@dataclass(frozen=True)
class ArchiveThresholds:
    # Conservative: 90-day rolling Sharpe + PSR check
    rolling_window_days: int = 90
    min_rolling_sharpe: float = 0.0   # must NOT be below this to keep
    min_rolling_psr: float = 0.5
    # Conservative: 60-day zero-trades check
    zero_trades_window_days: int = 60


_ADD_TH = AdditionThresholds()
_REPLACE_TH = ReplacementThresholds()
_ARCHIVE_TH = ArchiveThresholds()


# ---------------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------------


def _sharpe(returns: list[float]) -> float:
    if not returns or len(returns) < 2:
        return 0.0
    s = pd.Series(returns)
    std = float(s.std())
    if std == 0:
        return 0.0
    return float(s.mean() / std * math.sqrt(252))


def _split_dates(start: str, end: str, is_fraction: float) -> tuple[str, str]:
    """Return (is_end, oos_start) for a walk-forward split."""
    sd = dt.date.fromisoformat(start)
    ed = dt.date.fromisoformat(end)
    span = (ed - sd).days
    split = sd + dt.timedelta(days=int(span * is_fraction))
    return split.isoformat(), split.isoformat()


# ---------------------------------------------------------------------------
# Decision 1: ADD
# ---------------------------------------------------------------------------


def evaluate_for_addition(
    strategy_id: str,
    *,
    symbol: str,
    start: str,
    end: str,
    market_data,
    regime_classifier,
    thresholds: AdditionThresholds | None = None,
) -> dict[str, Any]:
    """Run the addition battery on a candidate strategy.

    Decision is fully deterministic given the data + thresholds. No agent
    discretion. Returns a dict the caller applies verbatim.
    """
    th = thresholds or _ADD_TH

    # 1. Full-window backtest — supplies trade count, max DD, Sortino, PSR
    full = run_backtest(
        strategy_id=strategy_id, symbol=symbol, start=start, end=end,
        market_data=market_data, regime_classifier=regime_classifier,
        thresholds=GateThresholds(min_num_trades=1, min_sharpe=-99, min_total_return=-99,
                                  max_drawdown_floor=-99),
    )
    if full.error:
        return {
            "decision": "REJECT",
            "reasons": [f"backtest could not run: {full.error}"],
            "metrics": full.to_dict(),
            "blocked_by_data": True,
        }

    # 2. Walk-forward split — sanity-check no overfit
    is_end, oos_start = _split_dates(start, end, th.is_fraction)
    is_run = run_backtest(
        strategy_id=strategy_id, symbol=symbol, start=start, end=is_end,
        market_data=market_data, regime_classifier=regime_classifier,
        thresholds=GateThresholds(min_num_trades=1, min_sharpe=-99, min_total_return=-99,
                                  max_drawdown_floor=-99),
    )
    oos_run = run_backtest(
        strategy_id=strategy_id, symbol=symbol, start=oos_start, end=end,
        market_data=market_data, regime_classifier=regime_classifier,
        thresholds=GateThresholds(min_num_trades=1, min_sharpe=-99, min_total_return=-99,
                                  max_drawdown_floor=-99),
    )

    # 3. Apply each test; collect reasons for rejection
    reasons: list[str] = []
    if full.num_trades < th.min_num_trades:
        reasons.append(f"num_trades {full.num_trades} < {th.min_num_trades}")
    if full.psr < th.min_psr:
        reasons.append(f"PSR {full.psr:.3f} < {th.min_psr}")
    if full.sortino < th.min_sortino:
        reasons.append(f"sortino {full.sortino:.3f} < {th.min_sortino}")
    if full.max_drawdown < th.max_drawdown_floor:
        reasons.append(f"max_dd {full.max_drawdown:.3f} < floor {th.max_drawdown_floor}")
    # OOS/IS Sharpe ratio: only meaningful if IS Sharpe is positive
    if is_run.sharpe > 0:
        ratio = oos_run.sharpe / is_run.sharpe
        if ratio < th.min_oos_to_is_sharpe_ratio:
            reasons.append(
                f"OOS/IS sharpe ratio {ratio:.2f} < {th.min_oos_to_is_sharpe_ratio} "
                f"(OOS={oos_run.sharpe:.2f}, IS={is_run.sharpe:.2f}) — possible overfit"
            )
    else:
        reasons.append(f"in-sample sharpe {is_run.sharpe:.2f} <= 0 — no edge to confirm")

    decision = "ADD" if not reasons else "REJECT"
    return {
        "decision": decision,
        "reasons": reasons,
        "thresholds": {
            "min_psr": th.min_psr,
            "min_sortino": th.min_sortino,
            "max_drawdown_floor": th.max_drawdown_floor,
            "min_num_trades": th.min_num_trades,
            "min_oos_to_is_sharpe_ratio": th.min_oos_to_is_sharpe_ratio,
        },
        "metrics": {
            "full": full.to_dict(),
            "in_sample": is_run.to_dict(),
            "out_of_sample": oos_run.to_dict(),
        },
    }


# ---------------------------------------------------------------------------
# Decision 2: REPLACE (paired bootstrap on trade returns)
# ---------------------------------------------------------------------------


def _paired_bootstrap_pvalue(
    existing_trade_returns: list[float],
    candidate_trade_returns: list[float],
    *,
    iters: int,
    seed: int = 42,
) -> float:
    """Return the bootstrap p-value for H0: candidate_mean <= existing_mean.

    Resamples both populations with replacement, computes the difference in
    means, and reports the fraction of bootstrap samples in which the
    difference is <= 0.

    The two strategies may have different trade counts (different entry
    criteria), so we resample each independently and compare means.
    """
    if not existing_trade_returns or not candidate_trade_returns:
        return 1.0
    rng = random.Random(seed)
    e = existing_trade_returns
    c = candidate_trade_returns
    n_e, n_c = len(e), len(c)
    not_better = 0
    for _ in range(iters):
        e_sample = [e[rng.randrange(n_e)] for _ in range(n_e)]
        c_sample = [c[rng.randrange(n_c)] for _ in range(n_c)]
        diff = sum(c_sample) / n_c - sum(e_sample) / n_e
        if diff <= 0:
            not_better += 1
    return not_better / iters


def evaluate_for_replacement(
    existing_id: str,
    candidate_id: str,
    *,
    symbol: str,
    start: str,
    end: str,
    market_data,
    regime_classifier,
    thresholds: ReplacementThresholds | None = None,
) -> dict[str, Any]:
    """Compare a candidate variant against an existing strategy on the same
    window. Decision is REPLACE only if candidate beats existing at the
    declared significance level AND Sharpe improvement exceeds the buffer.
    """
    th = thresholds or _REPLACE_TH

    existing = run_backtest(
        strategy_id=existing_id, symbol=symbol, start=start, end=end,
        market_data=market_data, regime_classifier=regime_classifier,
        thresholds=GateThresholds(min_num_trades=1, min_sharpe=-99, min_total_return=-99,
                                  max_drawdown_floor=-99),
    )
    candidate = run_backtest(
        strategy_id=candidate_id, symbol=symbol, start=start, end=end,
        market_data=market_data, regime_classifier=regime_classifier,
        thresholds=GateThresholds(min_num_trades=1, min_sharpe=-99, min_total_return=-99,
                                  max_drawdown_floor=-99),
    )
    if existing.error or candidate.error:
        return {
            "decision": "KEEP",
            "reasons": [
                f"comparison could not run (existing.error={existing.error!r}, candidate.error={candidate.error!r})"
            ],
            "metrics": {"existing": existing.to_dict(), "candidate": candidate.to_dict()},
            "blocked_by_data": True,
        }

    reasons: list[str] = []
    sharpe_delta = candidate.sharpe - existing.sharpe
    if sharpe_delta < th.min_sharpe_delta:
        reasons.append(
            f"sharpe improvement {sharpe_delta:.3f} < required {th.min_sharpe_delta}"
        )
    p = _paired_bootstrap_pvalue(
        existing.trade_returns, candidate.trade_returns,
        iters=th.bootstrap_iters,
    )
    if p >= th.max_p_value:
        reasons.append(
            f"bootstrap p-value {p:.3f} >= {th.max_p_value} (not statistically better)"
        )

    decision = "REPLACE" if not reasons else "KEEP"
    return {
        "decision": decision,
        "reasons": reasons,
        "thresholds": {
            "max_p_value": th.max_p_value,
            "min_sharpe_delta": th.min_sharpe_delta,
            "bootstrap_iters": th.bootstrap_iters,
        },
        "metrics": {
            "existing": existing.to_dict(),
            "candidate": candidate.to_dict(),
            "sharpe_delta": round(sharpe_delta, 4),
            "bootstrap_p_value": round(p, 4),
        },
    }


# ---------------------------------------------------------------------------
# Decision 3: ARCHIVE (conservative — 90-day rolling Sharpe/PSR, 60-day no-trades)
# ---------------------------------------------------------------------------


def evaluate_for_archive(
    strategy_id: str,
    *,
    thresholds: ArchiveThresholds | None = None,
    journal_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Should this strategy be archived?

    The test uses the trade journal — actual realized results from the live
    paper account, not a backtest. A strategy gets archived only if the
    operator-side evidence over the conservative window says it stopped
    working.
    """
    th = thresholds or _ARCHIVE_TH

    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return {
            "decision": "KEEP",
            "reasons": [f"strategy not found: {strategy_id}"],
            "metrics": {},
            "blocked_by_data": True,
        }
    if sf.status == "archived":
        return {
            "decision": "KEEP",
            "reasons": ["already archived"],
            "metrics": {"current_status": sf.status},
        }
    # Only fire the archive battery on strategies that have actually been active.
    # status='testing' / 'proposed' / 'deprecated' strategies never got their
    # chance and should not be auto-archived for "stopped firing."
    if sf.status != "active":
        return {
            "decision": "KEEP",
            "reasons": [
                f"current status is {sf.status!r}; archive battery only "
                "applies to status='active' strategies (the weekday agent "
                "must have used the strategy for the archive evidence to mean anything)"
            ],
            "metrics": {"current_status": sf.status},
        }

    # Distinguish "never traded" (no successful journal events) from "stopped".
    # Broker rejections (`order_rejected`) are NOT trading evidence — they
    # mean the strategy tried but the broker refused (e.g., insufficient
    # qty from symbol-claim overlap). The archive battery requires evidence
    # the strategy actually got off the ground; rejections don't qualify.
    lifetime_events = journal.read_events(days=365 * 5, strategy_id=strategy_id)
    lifetime_trading_events = [
        e for e in lifetime_events
        if e.get("type") in ("order_submitted", "trade_closed")
    ]
    if not lifetime_trading_events:
        return {
            "decision": "KEEP",
            "reasons": [
                "strategy has no successful lifetime trading evidence "
                "(submitted orders or closed trades); archive battery requires "
                "trading evidence to evaluate (a strategy that never traded "
                "successfully can't be diagnosed as having 'stopped working')",
            ],
            "metrics": {
                "lifetime_events": len(lifetime_events),
                "lifetime_trading_events": 0,
            },
        }

    # Pull the strategy's journal events over the longer of the two windows
    window_days = max(th.rolling_window_days, th.zero_trades_window_days)
    events = journal_events if journal_events is not None else journal.read_events(
        days=window_days, strategy_id=strategy_id,
    )
    closes = [e for e in events if e.get("type") == "trade_closed"]
    trade_returns = []
    for c in closes:
        pnl = c.get("pnl")
        if pnl is None:
            continue
        try:
            trade_returns.append(float(pnl))
        except (TypeError, ValueError):
            continue

    # Test 1: zero-trades window
    zero_trades_cutoff = (
        dt.datetime.now() - dt.timedelta(days=th.zero_trades_window_days)
    ).isoformat()
    recent_events = [e for e in events if e.get("timestamp", "") >= zero_trades_cutoff]
    recent_actions = [e for e in recent_events
                      if e.get("type") in ("order_submitted", "trade_closed")]
    triggered_zero_trades = (len(recent_actions) == 0)

    # Test 2: rolling-window Sharpe and PSR
    rolling_cutoff = (
        dt.datetime.now() - dt.timedelta(days=th.rolling_window_days)
    ).isoformat()
    rolling_closes = [c for c in closes if c.get("timestamp", "") >= rolling_cutoff]
    rolling_returns = []
    for c in rolling_closes:
        pnl = c.get("pnl")
        if pnl is None:
            continue
        try:
            rolling_returns.append(float(pnl))
        except (TypeError, ValueError):
            continue

    rolling_sharpe = _sharpe(rolling_returns) if len(rolling_returns) >= 5 else None
    rolling_psr = (
        _probabilistic_sharpe_ratio(rolling_returns) if len(rolling_returns) >= 5 else None
    )
    triggered_sharpe_psr = (
        rolling_sharpe is not None
        and rolling_psr is not None
        and rolling_sharpe < th.min_rolling_sharpe
        and rolling_psr < th.min_rolling_psr
    )

    reasons_for_archive: list[str] = []
    if triggered_zero_trades:
        reasons_for_archive.append(
            f"no orders or closes in last {th.zero_trades_window_days} days "
            f"(strategy has stopped firing)"
        )
    if triggered_sharpe_psr:
        reasons_for_archive.append(
            f"rolling Sharpe {rolling_sharpe:.3f} < {th.min_rolling_sharpe} "
            f"AND rolling PSR {rolling_psr:.3f} < {th.min_rolling_psr} "
            f"over {th.rolling_window_days}-day window"
        )

    if reasons_for_archive:
        return {
            "decision": "ARCHIVE",
            "reasons": reasons_for_archive,
            "thresholds": {
                "rolling_window_days": th.rolling_window_days,
                "min_rolling_sharpe": th.min_rolling_sharpe,
                "min_rolling_psr": th.min_rolling_psr,
                "zero_trades_window_days": th.zero_trades_window_days,
            },
            "metrics": {
                "rolling_sharpe": rolling_sharpe,
                "rolling_psr": rolling_psr,
                "trades_in_rolling_window": len(rolling_returns),
                "actions_in_zero_trades_window": len(recent_actions),
            },
        }
    return {
        "decision": "KEEP",
        "reasons": [
            "no archive trigger fired — strategy is either active enough or hasn't "
            "accumulated enough evidence to fail",
        ],
        "thresholds": {
            "rolling_window_days": th.rolling_window_days,
            "min_rolling_sharpe": th.min_rolling_sharpe,
            "min_rolling_psr": th.min_rolling_psr,
            "zero_trades_window_days": th.zero_trades_window_days,
        },
        "metrics": {
            "rolling_sharpe": rolling_sharpe,
            "rolling_psr": rolling_psr,
            "trades_in_rolling_window": len(rolling_returns),
            "actions_in_zero_trades_window": len(recent_actions),
        },
    }
