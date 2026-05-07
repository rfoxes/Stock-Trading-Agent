"""Deterministic strategy health signals.

The harness keeps LLM judgment in one place — the orchestrator agent. This
module is its opposite: pure math over the journal and market data, nothing
agentic. The orchestrator calls these functions, sees the numbers, and decides
what to do (rotate, modify thresholds, archive, etc.).

The signals returned here are coarse on purpose. They're meant to be
*indicators* — concrete inputs to a judgment call, not the call itself.

Limitations of the current implementation:
- Strategy-level realized P&L attribution requires bridging journal entries to
  Alpaca fills + closes. Until that reconciliation step is in place, the
  realized-pnl numbers below are best-effort: they count submitted orders, then
  use Alpaca's per-position unrealized P&L for any positions the strategy
  appears to have opened. Closed-trade Sharpe/win-rate over a strategy will
  improve as the journal accumulates `trade_closed` events.
"""

from __future__ import annotations

import datetime as dt
import math
import statistics
from typing import Any

import pandas as pd

from quant_trading_system import journal, memory


def _safe_div(a: float, b: float, default: float = 0.0) -> float:
    return a / b if b not in (0, 0.0) else default


def _percent_change(series: pd.Series) -> pd.Series:
    return series.pct_change().dropna()


def compute_spy_return(
    market_data,  # MarketDataService
    days: int = 30,
) -> float:
    """Total return on SPY over the last `days` calendar days."""
    try:
        end = dt.date.today().isoformat()
        start = (dt.date.today() - dt.timedelta(days=days + 5)).isoformat()
        df = market_data.get_bars("SPY", "1Day", start=start, end=end)
        if df.empty or len(df) < 2:
            return 0.0
        return float(df["Close"].iloc[-1] / df["Close"].iloc[0] - 1.0)
    except Exception:
        return 0.0


def _events_to_realized_pnl(events: list[dict[str, Any]]) -> list[float]:
    """Pull `pnl` fields off `trade_closed` events. Empty list if none yet."""
    pnls: list[float] = []
    for e in events:
        if e.get("type") != "trade_closed":
            continue
        pnl = e.get("pnl")
        if pnl is None:
            continue
        try:
            pnls.append(float(pnl))
        except (TypeError, ValueError):
            continue
    return pnls


def _rolling_sharpe(returns: list[float], periods_per_year: int = 252) -> float:
    """Annualized Sharpe of a list of trade-level returns. 0 if not computable."""
    if len(returns) < 2:
        return 0.0
    mean = statistics.fmean(returns)
    try:
        sd = statistics.stdev(returns)
    except statistics.StatisticsError:
        return 0.0
    if sd == 0:
        return 0.0
    # Treat each trade as one "period". periods_per_year normalizes loosely;
    # for trade-level returns this is an approximation. The orchestrator is
    # told the number of trades alongside the Sharpe so it can weight it.
    return float(mean / sd * math.sqrt(periods_per_year))


def _max_drawdown(returns: list[float]) -> float:
    """Max drawdown of cumulative returns expressed as a negative fraction."""
    if not returns:
        return 0.0
    cum = 1.0
    peak = 1.0
    mdd = 0.0
    for r in returns:
        cum *= 1 + r
        peak = max(peak, cum)
        dd = cum / peak - 1.0
        mdd = min(mdd, dd)
    return float(mdd)


def compute_strategy_health(
    strategy_id: str,
    *,
    market_data=None,  # MarketDataService, optional
    alpaca_client=None,  # AlpacaClient, optional
    lookback_days: int = 30,
) -> dict[str, Any]:
    """Compute a deterministic health snapshot for one strategy.

    Returns a dict the orchestrator can read at a glance. `thresholds_breached`
    is the list of frontmatter thresholds (if any) that the strategy itself
    declared and that the current numbers fail to meet.
    """
    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return {"strategy_id": strategy_id, "error": "strategy_not_found"}

    events = journal.read_events(days=lookback_days, strategy_id=strategy_id)
    submits = [e for e in events if e.get("type") == "order_submitted"]
    rejects = [e for e in events if e.get("type") == "order_rejected"]
    closes = [e for e in events if e.get("type") == "trade_closed"]

    realized_returns = _events_to_realized_pnl(closes)
    wins = [r for r in realized_returns if r > 0]
    losses = [r for r in realized_returns if r < 0]

    win_rate = _safe_div(len(wins), len(realized_returns)) if realized_returns else None
    avg_win = statistics.fmean(wins) if wins else None
    avg_loss = statistics.fmean(losses) if losses else None
    rolling_sharpe = _rolling_sharpe(realized_returns) if len(realized_returns) >= 2 else None
    max_dd = _max_drawdown(realized_returns) if realized_returns else None
    cum_return = (
        math.prod(1 + r for r in realized_returns) - 1 if realized_returns else None
    )

    spy_return = compute_spy_return(market_data, lookback_days) if market_data else None
    pnl_vs_spy = (
        cum_return - spy_return
        if (cum_return is not None and spy_return is not None)
        else None
    )

    # Best-effort current exposure for this strategy (open positions whose
    # entry was logged under this strategy_id within the journal window).
    open_position_unrealized = 0.0
    if alpaca_client is not None:
        try:
            symbols_from_strategy = {
                s.get("symbol") for s in submits if s.get("symbol")
            }
            positions = alpaca_client.get_positions()
            for p in positions:
                if p.get("symbol") in symbols_from_strategy:
                    open_position_unrealized += float(p.get("unrealized_pl", 0.0) or 0.0)
        except Exception:
            pass

    # Threshold check based on strategy frontmatter
    thresholds = (sf.frontmatter.get("thresholds") or {})
    breached: list[str] = []

    def breach(label: str, current: float | None, op: str, limit: float) -> None:
        if current is None or limit is None:
            return
        if op == "lt" and current < limit:
            breached.append(f"{label}={current:.4f} < min {limit}")
        elif op == "gt" and current > limit:
            breached.append(f"{label}={current:.4f} > max {limit}")

    breach("rolling_sharpe", rolling_sharpe, "lt", thresholds.get("min_rolling_sharpe"))
    breach("win_rate", win_rate, "lt", thresholds.get("min_win_rate"))
    breach("max_drawdown", max_dd, "lt", thresholds.get("max_drawdown"))
    breach("pnl_vs_spy", pnl_vs_spy, "lt", thresholds.get("min_pnl_vs_spy"))

    return {
        "strategy_id": strategy_id,
        "lookback_days": lookback_days,
        "orders_submitted": len(submits),
        "orders_rejected": len(rejects),
        "trades_closed": len(realized_returns),
        "win_rate": round(win_rate, 4) if win_rate is not None else None,
        "avg_win": round(avg_win, 4) if avg_win is not None else None,
        "avg_loss": round(avg_loss, 4) if avg_loss is not None else None,
        "rolling_sharpe": round(rolling_sharpe, 4) if rolling_sharpe is not None else None,
        "max_drawdown": round(max_dd, 4) if max_dd is not None else None,
        "cum_return": round(cum_return, 4) if cum_return is not None else None,
        "spy_return": round(spy_return, 4) if spy_return is not None else None,
        "pnl_vs_spy": round(pnl_vs_spy, 4) if pnl_vs_spy is not None else None,
        "open_position_unrealized": round(open_position_unrealized, 2),
        "thresholds": thresholds,
        "thresholds_breached": breached,
        "status": sf.status,
    }


def compute_portfolio_health(
    *,
    market_data=None,
    alpaca_client=None,
    lookback_days: int = 30,
) -> dict[str, Any]:
    """Top-level snapshot across all active strategies. Cheap to call."""
    actives = memory.list_strategies(status="active")
    snapshots = [
        compute_strategy_health(
            s.id,
            market_data=market_data,
            alpaca_client=alpaca_client,
            lookback_days=lookback_days,
        )
        for s in actives
    ]
    spy_return = compute_spy_return(market_data, lookback_days) if market_data else None
    return {
        "as_of": dt.date.today().isoformat(),
        "lookback_days": lookback_days,
        "active_strategy_count": len(actives),
        "spy_return": round(spy_return, 4) if spy_return is not None else None,
        "per_strategy": snapshots,
    }
