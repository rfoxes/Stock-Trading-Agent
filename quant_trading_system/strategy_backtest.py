"""Walk-forward backtester that calls a strategy's `evaluate()` directly.

The harness's central design is that strategies are Python functions called
by the runtime each scheduled day. A faithful backtest reproduces that
exact loop: for each historical date in a backtest window, build the same
StrategyContext that a live run would build (using historical bars sliced
up to that date), call `evaluate(ctx)`, and apply the returned intents to
a simulated portfolio.

This is intentionally a *minimum-credibility* backtester, not a full
research-grade one:
  - One symbol or a small set of symbols per run; no cross-asset universe.
  - Market orders fill at next bar's open (gap-aware).
  - Limit orders fill if the next bar's range reaches the limit.
  - Stops/take-profits derived from `OrderIntent.stop_loss_pct` /
    `take_profit_pct` are tracked as separate exits at next-bar OHLC.
  - No slippage, no commissions (paper trading default).
  - No options support (returns an error for type=options strategies).

It's good enough to act as a sanity gate before adding a strategy to the
library. Strategies that don't pass this gate are clearly broken; passing
it doesn't mean a strategy is good, only that it isn't obviously dead.

Pure pandas + numpy. Works in the Cowork sandbox without vectorbt.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import logging
import math
import statistics
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

from quant_trading_system import memory
from quant_trading_system.strategy_runtime import OrderIntent, StrategyContext

logger = logging.getLogger(__name__)


@dataclass
class BacktestResult:
    strategy_id: str
    symbol: str
    start: str
    end: str
    bars_used: int
    initial_capital: float
    final_equity: float
    total_return: float
    cagr: float
    sharpe: float
    sortino: float = 0.0
    calmar: float = 0.0
    psr: float = 0.0            # Probabilistic Sharpe Ratio, vs benchmark=0
    max_drawdown: float = 0.0
    win_rate: float | None = None
    num_trades: int = 0
    error: str = ""
    passed_gate: bool = False
    gate_reason: str = ""
    notes: list[str] = field(default_factory=list)
    # Raw series for downstream tests — kept compact so JSON serialization works
    equity_curve: list[float] = field(default_factory=list)
    bar_returns: list[float] = field(default_factory=list)
    trade_returns: list[float] = field(default_factory=list)

    def to_dict(self, *, include_series: bool = False) -> dict[str, Any]:
        d = {
            "strategy_id": self.strategy_id,
            "symbol": self.symbol,
            "start": self.start,
            "end": self.end,
            "bars_used": self.bars_used,
            "initial_capital": round(self.initial_capital, 2),
            "final_equity": round(self.final_equity, 2),
            "total_return": round(self.total_return, 4),
            "cagr": round(self.cagr, 4),
            "sharpe": round(self.sharpe, 4),
            "sortino": round(self.sortino, 4),
            "calmar": round(self.calmar, 4),
            "psr": round(self.psr, 4),
            "max_drawdown": round(self.max_drawdown, 4),
            "win_rate": round(self.win_rate, 4) if self.win_rate is not None else None,
            "num_trades": self.num_trades,
            "passed_gate": self.passed_gate,
            "gate_reason": self.gate_reason,
            "error": self.error,
            "notes": self.notes,
        }
        if include_series:
            d["equity_curve"] = self.equity_curve
            d["bar_returns"] = self.bar_returns
            d["trade_returns"] = self.trade_returns
        return d


# ---------------------------------------------------------------------------
# Default gate thresholds
# ---------------------------------------------------------------------------


@dataclass
class GateThresholds:
    """Minimum-credibility bar for a new strategy. Easy to relax or tighten."""

    min_sharpe: float = 0.3
    min_total_return: float = 0.0
    max_drawdown_floor: float = -0.40  # don't accept anything below -40% peak-to-trough
    min_num_trades: int = 5
    min_win_rate: float | None = None  # None = don't gate on win rate

    def evaluate(self, r: BacktestResult) -> tuple[bool, str]:
        reasons: list[str] = []
        if r.num_trades < self.min_num_trades:
            reasons.append(f"too few trades ({r.num_trades} < {self.min_num_trades})")
        if r.sharpe < self.min_sharpe:
            reasons.append(f"sharpe {r.sharpe:.2f} < {self.min_sharpe}")
        if r.total_return < self.min_total_return:
            reasons.append(f"return {r.total_return:.2%} < {self.min_total_return:.2%}")
        if r.max_drawdown < self.max_drawdown_floor:
            reasons.append(f"max_dd {r.max_drawdown:.2%} < floor {self.max_drawdown_floor:.2%}")
        if self.min_win_rate is not None and (r.win_rate is None or r.win_rate < self.min_win_rate):
            wr = "n/a" if r.win_rate is None else f"{r.win_rate:.2%}"
            reasons.append(f"win_rate {wr} < {self.min_win_rate}")
        if reasons:
            return False, "; ".join(reasons)
        return True, "passed all thresholds"


# ---------------------------------------------------------------------------
# Backtest engine
# ---------------------------------------------------------------------------


def _load_strategy_module(py_path: Path):
    mod_name = f"_strategy_bt_{uuid.uuid4().hex[:6]}"
    spec = importlib.util.spec_from_file_location(mod_name, str(py_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {py_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_indicator_callable(bars_slice: pd.DataFrame) -> Callable:
    """Return a compute_indicator(symbol, indicator, period=None, df=None) that
    works against the historical slice. For backtest, the strategy can compute
    indicators on any provided df."""
    from quant_trading_system.tools import technical_indicators as ti

    def _ci(symbol: str, name: str, period: int | None = None,
            df: pd.DataFrame | None = None) -> Any:
        b = df if df is not None else bars_slice
        if b is None or b.empty:
            return None
        n = name.lower()
        try:
            if n == "sma": return float(ti.compute_sma(b["Close"], period or 20).iloc[-1])
            if n == "ema": return float(ti.compute_ema(b["Close"], period or 20).iloc[-1])
            if n == "rsi": return float(ti.compute_rsi(b["Close"], period or 14).iloc[-1])
            if n == "atr": return float(ti.compute_atr(b["High"], b["Low"], b["Close"], period or 14).iloc[-1])
            if n == "adx": return float(ti.compute_adx(b["High"], b["Low"], b["Close"], period or 14).iloc[-1])
        except Exception:
            return None
        return None
    return _ci


def run_backtest(
    strategy_id: str,
    symbol: str,
    *,
    start: str,
    end: str,
    market_data,
    regime_classifier,
    initial_capital: float = 100_000.0,
    thresholds: GateThresholds | None = None,
) -> BacktestResult:
    """Walk forward day-by-day, calling the strategy's evaluate() at each step.

    Each historical day is treated as a 'today': the strategy sees bars up
    to (but not including) that day's close; its intents are filled at the
    NEXT day's open. Stop/take-profit exits are tracked at next day's H/L.
    """
    th = thresholds or GateThresholds()
    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=0, initial_capital=initial_capital, final_equity=0,
            total_return=0, cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
            num_trades=0, error=f"strategy not found: {strategy_id}",
        )
    if sf.type == "options":
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=0, initial_capital=initial_capital, final_equity=0,
            total_return=0, cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
            num_trades=0,
            error="backtester does not support options strategies (no chain data)",
        )
    if not sf.py_path.exists():
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=0, initial_capital=initial_capital, final_equity=0,
            total_return=0, cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
            num_trades=0, error=f"strategy.py missing at {sf.py_path}",
        )

    try:
        module = _load_strategy_module(sf.py_path)
    except Exception as e:
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=0, initial_capital=initial_capital, final_equity=0,
            total_return=0, cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
            num_trades=0, error=f"strategy.py import failed: {e}",
        )
    if not hasattr(module, "evaluate"):
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=0, initial_capital=initial_capital, final_equity=0,
            total_return=0, cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
            num_trades=0, error="strategy.py does not define evaluate()",
        )

    try:
        bars = market_data.get_bars(symbol, "1Day", start=start, end=end)
    except Exception as e:
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=0, initial_capital=initial_capital, final_equity=0,
            total_return=0, cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
            num_trades=0, error=f"market_data error: {e}",
        )
    if bars.empty or len(bars) < 60:
        return BacktestResult(
            strategy_id=strategy_id, symbol=symbol, start=start, end=end,
            bars_used=len(bars), initial_capital=initial_capital,
            final_equity=initial_capital, total_return=0, cagr=0, sharpe=0,
            max_drawdown=0, win_rate=None, num_trades=0,
            error=f"insufficient bars ({len(bars)} < 60)",
        )

    # --- Walk forward ---
    cash = float(initial_capital)
    shares = 0.0
    entry_price = 0.0
    stop_price: float | None = None
    target_price: float | None = None
    equity_curve: list[float] = []
    closed_trade_returns: list[float] = []  # per-trade returns as fractions of position notional
    params = dict(sf.frontmatter.get("parameters") or {})

    # Pre-cache market_data shim: strategy's ctx.get_bars must return only bars
    # up to "today", to avoid look-ahead bias.
    def _historical_get_bars(slice_end: pd.Timestamp):
        def _gb(sym: str, timeframe: str = "1Day", lookback_days: int = 200) -> pd.DataFrame:
            if sym.upper() != symbol.upper():
                # Multi-symbol strategies aren't supported by this single-symbol
                # backtester; return empty so they degrade to no-op.
                return pd.DataFrame()
            slc = bars.loc[:slice_end]
            if lookback_days and len(slc) > lookback_days:
                slc = slc.tail(lookback_days)
            return slc
        return _gb

    # Iterate "today = i" where i ranges over indices with enough history
    # and a next-bar to fill against.
    n = len(bars)
    warmup = 50  # need at least some history for indicators to be valid
    for i in range(warmup, n - 1):
        today_ts = bars.index[i]
        next_ts = bars.index[i + 1]
        next_open = float(bars["Open"].iloc[i + 1])
        next_high = float(bars["High"].iloc[i + 1])
        next_low = float(bars["Low"].iloc[i + 1])
        next_close = float(bars["Close"].iloc[i + 1])

        # 1. Check stop/target on next bar before considering new entries
        if shares > 0:
            exited = False
            exit_price = None
            exit_reason = ""
            if stop_price is not None and next_low <= stop_price:
                exit_price = stop_price
                exit_reason = "stop"
                exited = True
            elif target_price is not None and next_high >= target_price:
                exit_price = target_price
                exit_reason = "target"
                exited = True
            if exited:
                trade_return = (exit_price / entry_price) - 1.0
                closed_trade_returns.append(trade_return)
                cash += shares * exit_price
                shares = 0.0
                entry_price = 0.0
                stop_price = None
                target_price = None

        # 2. Build today's context and call evaluate()
        positions = []
        if shares > 0:
            positions.append({
                "symbol": symbol,
                "qty": shares,
                "side": "long",
                "avg_entry_price": entry_price,
                "current_price": float(bars["Close"].iloc[i]),
                "unrealized_pl": shares * (float(bars["Close"].iloc[i]) - entry_price),
                "unrealized_plpc": (float(bars["Close"].iloc[i]) - entry_price) / entry_price if entry_price else 0.0,
                "market_value": shares * float(bars["Close"].iloc[i]),
            })
        equity_now = cash + shares * float(bars["Close"].iloc[i])
        account = {
            "equity": equity_now,
            "cash": cash,
            "buying_power": cash,
            "portfolio_value": equity_now,
            "day_trade_count": 0,
        }

        ctx = StrategyContext(
            date=today_ts.date() if hasattr(today_ts, "date") else dt.date.today(),
            params=params,
            watchlist=[symbol],
            regime={"regime": "unknown", "confidence": 0.0},  # cheap; could classify if needed
            account=account,
            positions=positions,
            open_orders=[],
            strategy_id=sf.id,
            strategy_type=sf.type,
            log=logging.getLogger(f"backtest.{sf.id}"),
            get_bars=_historical_get_bars(today_ts),
            get_quote=lambda s: None,
            compute_indicator=_build_indicator_callable(bars.loc[:today_ts]),
        )

        try:
            intents = module.evaluate(ctx)
        except Exception as e:
            # A misbehaving strategy aborts the backtest with a clear error
            return BacktestResult(
                strategy_id=strategy_id, symbol=symbol, start=start, end=end,
                bars_used=i, initial_capital=initial_capital,
                final_equity=equity_now, total_return=equity_now/initial_capital - 1,
                cagr=0, sharpe=0, max_drawdown=0, win_rate=None,
                num_trades=len(closed_trade_returns),
                error=f"evaluate() raised at bar {i}: {e}",
            )
        if intents is None:
            intents = []

        # 3. Apply intents at next bar's open. Single-symbol support: handle the
        # FIRST matching intent we see (if multiple, the rest are ignored — keep
        # it simple).
        for raw in intents:
            it = _to_intent(raw)
            if it is None or it.symbol.upper() != symbol.upper():
                continue
            if it.side == "buy" and shares == 0:
                # Determine fill price
                if it.order_type == "market":
                    fill = next_open
                elif it.order_type == "limit" and it.limit_price is not None:
                    if next_low <= it.limit_price:
                        fill = min(next_open, it.limit_price)
                    else:
                        continue
                else:
                    continue
                qty = float(it.qty)
                cost = qty * fill
                if cost > cash:
                    # Can't afford; skip
                    continue
                cash -= cost
                shares = qty
                entry_price = fill
                if it.stop_loss_pct:
                    stop_price = round(fill * (1 - float(it.stop_loss_pct)), 4)
                if it.take_profit_pct:
                    target_price = round(fill * (1 + float(it.take_profit_pct)), 4)
                break
            elif it.side == "sell" and shares > 0:
                # Market sell at next open
                fill = next_open
                trade_return = (fill / entry_price) - 1.0
                closed_trade_returns.append(trade_return)
                cash += shares * fill
                shares = 0.0
                entry_price = 0.0
                stop_price = None
                target_price = None
                break

        # 4. Mark-to-market equity at next bar close
        equity_curve.append(cash + shares * next_close)

    # --- Finalize ---
    if shares > 0:
        # Close at last bar's close
        last_close = float(bars["Close"].iloc[-1])
        trade_return = (last_close / entry_price) - 1.0
        closed_trade_returns.append(trade_return)
        cash += shares * last_close
        shares = 0.0

    final_equity = cash
    total_return = (final_equity / initial_capital) - 1.0
    bars_in_window = len(equity_curve)
    years = bars_in_window / 252 if bars_in_window > 0 else 0.0
    cagr = (final_equity / initial_capital) ** (1.0 / years) - 1.0 if years > 0 else 0.0

    if equity_curve and len(equity_curve) > 1:
        returns = pd.Series(equity_curve).pct_change().dropna()
        std = float(returns.std())
        mean = float(returns.mean())
        sharpe = (mean / std * math.sqrt(252)) if std > 0 else 0.0
        # Sortino: only downside std deviation
        downside = returns[returns < 0]
        ds = float(downside.std()) if len(downside) > 1 else 0.0
        sortino = (mean / ds * math.sqrt(252)) if ds > 0 else 0.0
        eq = pd.Series(equity_curve)
        rolling_peak = eq.cummax()
        max_dd = float((eq / rolling_peak - 1.0).min())
        # Calmar = CAGR / |max_dd|
        calmar = (cagr / abs(max_dd)) if max_dd < 0 else 0.0
        # Probabilistic Sharpe Ratio (López de Prado / Bailey)
        bar_returns_list = [float(x) for x in returns.tolist()]
        psr = _probabilistic_sharpe_ratio(bar_returns_list)
    else:
        sharpe = 0.0
        sortino = 0.0
        calmar = 0.0
        max_dd = 0.0
        psr = 0.0
        bar_returns_list = []

    wins = [r for r in closed_trade_returns if r > 0]
    win_rate = (len(wins) / len(closed_trade_returns)) if closed_trade_returns else None

    result = BacktestResult(
        strategy_id=strategy_id, symbol=symbol, start=start, end=end,
        bars_used=bars_in_window, initial_capital=initial_capital,
        final_equity=final_equity, total_return=total_return,
        cagr=cagr, sharpe=sharpe, sortino=sortino, calmar=calmar, psr=psr,
        max_drawdown=max_dd, win_rate=win_rate,
        num_trades=len(closed_trade_returns),
        equity_curve=[float(x) for x in equity_curve],
        bar_returns=bar_returns_list,
        trade_returns=[float(x) for x in closed_trade_returns],
    )
    passed, why = th.evaluate(result)
    result.passed_gate = passed
    result.gate_reason = why
    return result


# ---------------------------------------------------------------------------
# Statistical helpers (used by run_backtest and by strategy_evaluation.py)
# ---------------------------------------------------------------------------


def _standard_normal_cdf(z: float) -> float:
    """Φ(z) via stdlib math.erf. Pure stdlib, no scipy needed."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _probabilistic_sharpe_ratio(
    returns: list[float],
    sr_benchmark_annual: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """Bailey & López de Prado's Probabilistic Sharpe Ratio.

    PSR(SR*) = Φ((SR_hat - SR*) * sqrt(T-1) / sqrt(1 - γ3·SR_hat + (γ4-1)/4·SR_hat^2))

    SR_hat and SR* are per-period (NOT annualised) inside the formula.
    Returns a probability in [0, 1].
    """
    if not returns or len(returns) < 5:
        return 0.0
    s = pd.Series(returns)
    mean = float(s.mean())
    std = float(s.std())
    if std == 0:
        return 0.0
    sr_hat = mean / std
    sr_star = sr_benchmark_annual / math.sqrt(periods_per_year)
    n = len(returns)
    # Sample skew & kurt; pandas' kurt is excess by default
    try:
        skew = float(s.skew())
    except Exception:
        skew = 0.0
    try:
        excess_kurt = float(s.kurt())
    except Exception:
        excess_kurt = 0.0
    raw_kurt = excess_kurt + 3.0
    denom_sq = 1.0 - skew * sr_hat + ((raw_kurt - 1.0) / 4.0) * (sr_hat ** 2)
    if denom_sq <= 0:
        return 0.0
    z = (sr_hat - sr_star) * math.sqrt(n - 1) / math.sqrt(denom_sq)
    return _standard_normal_cdf(z)


def _to_intent(raw: Any) -> OrderIntent | None:
    if isinstance(raw, OrderIntent):
        return raw
    if not isinstance(raw, dict):
        return None
    try:
        return OrderIntent(
            symbol=str(raw["symbol"]),
            side=str(raw["side"]),
            qty=float(raw["qty"]),
            order_type=str(raw.get("order_type", "market")),
            limit_price=raw.get("limit_price"),
            stop_price=raw.get("stop_price"),
            time_in_force=str(raw.get("time_in_force", "day")),
            reasoning=str(raw.get("reasoning", "")),
            stop_loss_pct=raw.get("stop_loss_pct"),
            take_profit_pct=raw.get("take_profit_pct"),
        )
    except (KeyError, ValueError, TypeError):
        return None
