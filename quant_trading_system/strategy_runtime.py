"""Runtime that loads a strategy.py and runs its evaluate() function.

The harness's central architectural rule: the *agent* never reasons about
individual orders. The agent picks the active strategy and decides when to
rotate or update; the *strategy script* decides what to trade. This module
is the bridge — it loads a strategy's `strategy.py`, calls its `evaluate(ctx)`
function, and submits whatever orders it returns through SafetyGate.

A strategy script must define:

    def evaluate(ctx: StrategyContext) -> list[OrderIntent]:
        '''Return today's intended orders. Empty list = no action today.'''

Anything else in the script (helper functions, indicator caches, etc.) is the
strategy author's business. The `ctx` object is the only sanctioned way to
reach market data, account state, and the strategy's own parameters.

Strategies live as folders under ``knowledge_base/strategies/<type>/<id>/``,
containing ``strategy.md`` (prose rules + frontmatter parameters) and
``strategy.py`` (this contract). The .py is loaded dynamically by file path,
so the strategies dir does not need to be a Python package.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import logging
import traceback
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

from quant_trading_system import journal, memory
from quant_trading_system.models.trade import (
    OrderRequest,
    OrderSide,
    OrderType,
    TimeInForce,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Inputs and outputs of an evaluate() call
# ---------------------------------------------------------------------------


@dataclass
class StrategyContext:
    """Everything a strategy script needs to make its decisions.

    Fields are read-only from the strategy's point of view. The strategy
    should never mutate this object.
    """

    date: dt.date
    params: dict[str, Any]                       # frontmatter `parameters` block
    watchlist: list[str]                         # symbols the operator wants considered
    regime: dict[str, Any]                       # output of classify_regime
    account: dict[str, Any]                      # equity, cash, buying_power, ...
    positions: list[dict[str, Any]]              # current Alpaca positions
    open_orders: list[dict[str, Any]]            # queued orders
    strategy_id: str
    strategy_type: str                           # "equity" | "options"
    log: logging.Logger                          # strategy-scoped logger

    # Callable hooks — the strategy uses these instead of importing data
    # modules directly. Lets the harness control caching, mocking for tests,
    # and the boundary of what strategies are allowed to do.
    get_bars: Callable[..., pd.DataFrame] = field(default=lambda *a, **kw: pd.DataFrame())
    get_quote: Callable[[str], Optional[dict[str, Any]]] = field(default=lambda s: None)
    compute_indicator: Callable[..., Any] = field(default=lambda *a, **kw: None)

    def __repr__(self) -> str:  # avoid dumping pandas/callables in logs
        return (
            f"StrategyContext(id={self.strategy_id!r}, date={self.date}, "
            f"positions={len(self.positions)}, regime={self.regime.get('regime')!r})"
        )


@dataclass
class OrderIntent:
    """One intended order a strategy wants the harness to submit.

    Keep this lean — symbol/side/qty/type are required, anything else is
    optional. The harness translates this into an OrderRequest, tags it with
    `strategy_id`, and submits through SafetyGate. If SafetyGate rejects, the
    rejection is journaled (so health signals see the intent even if it
    didn't fire).
    """

    symbol: str
    side: str                                    # "buy" | "sell"
    qty: float
    order_type: str = "market"                   # "market" | "limit" | "stop" | "stop_limit"
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = "day"
    reasoning: str = ""                          # short, human-readable
    # Optional bracket: if provided, the harness will follow up with stop /
    # take-profit orders. Each value is a fraction (e.g. 0.02 = 2%).
    stop_loss_pct: Optional[float] = None
    take_profit_pct: Optional[float] = None


# ---------------------------------------------------------------------------
# Loader — dynamic import of strategy.py by file path
# ---------------------------------------------------------------------------


def _load_strategy_module(py_path: Path):
    """Dynamically import strategy.py. Returns the module object."""
    if not py_path.exists():
        raise FileNotFoundError(f"strategy.py not found at {py_path}")
    # Unique module name so re-loads in the same process don't collide
    mod_name = f"_strategy_{py_path.parent.name}_{uuid.uuid4().hex[:6]}"
    spec = importlib.util.spec_from_file_location(mod_name, str(py_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build spec for {py_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# The run function — called by agent_tools.execute_strategy
# ---------------------------------------------------------------------------


def run_strategy(
    strategy_id: str,
    *,
    settings,
    market_data,
    regime_classifier,
    safety_gate,
    alpaca_client,
    run_id: str,
) -> dict[str, Any]:
    """Load and run one strategy. Submits intents through SafetyGate.

    Returns a dict with:
        strategy_id, intent_count, submitted, rejected, errors, evaluate_error
    """
    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return {"ok": False, "error": f"strategy not found: {strategy_id}"}
    if not getattr(sf, "py_path", None) or not sf.py_path.exists():
        return {
            "ok": False,
            "error": f"strategy has no strategy.py ({sf.dir})",
            "strategy_id": strategy_id,
        }
    if sf.status != "active":
        return {
            "ok": False,
            "error": f"strategy is not active (status={sf.status})",
            "strategy_id": strategy_id,
        }

    # Build context
    try:
        ctx = _build_context(
            sf,
            settings=settings,
            market_data=market_data,
            regime_classifier=regime_classifier,
            alpaca_client=alpaca_client,
        )
    except Exception as e:
        return {"ok": False, "error": f"context build failed: {e}", "strategy_id": strategy_id}

    # Import + evaluate
    try:
        module = _load_strategy_module(sf.py_path)
    except Exception as e:
        logger.error("strategy_import_failed id=%s err=%s\n%s", strategy_id, e, traceback.format_exc())
        return {"ok": False, "error": f"import failed: {e}", "strategy_id": strategy_id}

    if not hasattr(module, "evaluate"):
        return {"ok": False, "error": "strategy.py does not define evaluate()", "strategy_id": strategy_id}

    try:
        intents = module.evaluate(ctx)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error("strategy_evaluate_failed id=%s err=%s\n%s", strategy_id, e, tb)
        # Record the failure to the journal so tomorrow's run sees it
        journal.log_event({
            "type": "strategy_error",
            "strategy_id": strategy_id,
            "run_id": run_id,
            "error": str(e),
            "traceback": tb[-2000:],
        })
        return {
            "ok": False,
            "error": f"evaluate() raised: {e}",
            "strategy_id": strategy_id,
            "evaluate_error": True,
        }

    if intents is None:
        intents = []
    if not isinstance(intents, list):
        return {
            "ok": False,
            "error": f"evaluate() returned {type(intents).__name__}, expected list",
            "strategy_id": strategy_id,
        }

    # Submit each intent through SafetyGate
    submitted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for raw in intents:
        intent = _coerce_intent(raw)
        if intent is None:
            errors.append({"raw": str(raw)[:200], "reason": "could not coerce to OrderIntent"})
            continue
        try:
            order = OrderRequest(
                symbol=intent.symbol.upper(),
                side=OrderSide(intent.side.lower()),
                qty=float(intent.qty),
                order_type=OrderType(intent.order_type.lower()),
                time_in_force=TimeInForce(intent.time_in_force.lower()),
                limit_price=intent.limit_price,
                stop_price=intent.stop_price,
                agent_name="strategy_runtime",
                strategy_name=strategy_id,
                reasoning=intent.reasoning[:500],
            )
        except (ValueError, TypeError) as e:
            errors.append({"intent": intent.__dict__, "reason": f"invalid order: {e}"})
            continue

        try:
            result = safety_gate.validate_and_submit(order)
        except Exception as e:
            errors.append({"intent": intent.__dict__, "reason": f"safety_gate raised: {e}"})
            continue

        result_dict = {
            "order_id": result.order_id,
            "status": result.status.value,
            "mode": result.mode.value,
            "filled_qty": result.filled_qty,
            "filled_avg_price": result.filled_avg_price,
            "rejection_reason": result.rejection_reason,
            "safety_checks_passed": result.safety_checks_passed,
            "safety_checks_failed": result.safety_checks_failed,
            "symbol": order.symbol,
            "side": order.side.value,
            "qty": order.qty,
        }
        journal.log_order(
            strategy_id=strategy_id,
            run_id=run_id,
            order_request=order.model_dump(),
            order_result=result_dict,
        )
        if result.status.value in ("rejected",):
            rejected.append(result_dict)
        else:
            submitted.append(result_dict)

    return {
        "ok": True,
        "strategy_id": strategy_id,
        "intent_count": len(intents),
        "submitted": submitted,
        "rejected": rejected,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Context builder
# ---------------------------------------------------------------------------


def _build_context(sf, *, settings, market_data, regime_classifier, alpaca_client) -> StrategyContext:
    # Account / positions / open orders (best-effort)
    account: dict[str, Any] = {}
    positions: list[dict[str, Any]] = []
    open_orders: list[dict[str, Any]] = []
    if alpaca_client is not None:
        try:
            account = alpaca_client.get_account()
        except Exception as e:
            logger.warning("ctx_account_fetch_failed err=%s", e)
        try:
            positions = alpaca_client.get_positions()
        except Exception as e:
            logger.warning("ctx_positions_fetch_failed err=%s", e)
        try:
            open_orders = alpaca_client.get_open_orders()
        except Exception as e:
            logger.warning("ctx_open_orders_fetch_failed err=%s", e)
    if not account:
        equity = float(getattr(settings, "PAPER_PORTFOLIO_SIZE", 100_000.0))
        account = {
            "equity": equity,
            "cash": equity,
            "buying_power": equity,
            "portfolio_value": equity,
            "day_trade_count": 0,
        }

    # Regime — best-effort, default to unknown
    regime: dict[str, Any] = {"regime": "unknown", "confidence": 0.0}
    try:
        spy = market_data.get_bars("SPY", "1Day")
        if not spy.empty:
            regime = regime_classifier.classify(spy)
    except Exception as e:
        logger.warning("ctx_regime_failed err=%s", e)

    params = dict(sf.frontmatter.get("parameters") or {})

    # Provide indicator helper that knows about ctx caching is overkill; lean
    # version: defer to tools.technical_indicators on whatever bars the strategy
    # already has.
    from quant_trading_system.tools import technical_indicators as ti

    def _compute_indicator(symbol: str, name: str, period: int | None = None,
                           df: pd.DataFrame | None = None) -> Any:
        bars = df if df is not None else market_data.get_bars(symbol, "1Day")
        if bars.empty:
            return None
        n = name.lower()
        if n == "sma":
            return float(ti.compute_sma(bars["Close"], period or 20).iloc[-1])
        if n == "ema":
            return float(ti.compute_ema(bars["Close"], period or 20).iloc[-1])
        if n == "rsi":
            return float(ti.compute_rsi(bars["Close"], period or 14).iloc[-1])
        if n == "atr":
            return float(ti.compute_atr(bars["High"], bars["Low"], bars["Close"], period or 14).iloc[-1])
        if n == "adx":
            return float(ti.compute_adx(bars["High"], bars["Low"], bars["Close"], period or 14).iloc[-1])
        if n in ("bb", "bbands", "bollinger"):
            b = ti.compute_bollinger_bands(bars["Close"], period or 20)
            return {
                "upper": float(b["Upper"].iloc[-1]),
                "middle": float(b["Middle"].iloc[-1]),
                "lower": float(b["Lower"].iloc[-1]),
            }
        if n == "macd":
            m = ti.compute_macd(bars["Close"])
            return {
                "macd": float(m["MACD"].iloc[-1]),
                "signal": float(m["Signal"].iloc[-1]),
                "histogram": float(m["Histogram"].iloc[-1]),
            }
        if n == "obv":
            return float(ti.compute_obv(bars["Close"], bars["Volume"]).iloc[-1])
        if n == "vwap":
            return float(ti.compute_vwap(bars["High"], bars["Low"], bars["Close"], bars["Volume"]).iloc[-1])
        return None

    return StrategyContext(
        date=dt.date.today(),
        params=params,
        watchlist=list(settings.watchlist),
        regime=regime,
        account=account,
        positions=positions,
        open_orders=open_orders,
        strategy_id=sf.id,
        strategy_type=sf.type,
        log=logging.getLogger(f"strategy.{sf.id}"),
        get_bars=lambda symbol, timeframe="1Day", lookback_days=200: _bars_with_lookback(
            market_data, symbol, timeframe, lookback_days
        ),
        get_quote=lambda symbol: _safe_quote(market_data, symbol),
        compute_indicator=_compute_indicator,
    )


def _bars_with_lookback(market_data, symbol: str, timeframe: str, lookback_days: int) -> pd.DataFrame:
    end = dt.date.today().isoformat()
    start = (dt.date.today() - dt.timedelta(days=lookback_days)).isoformat()
    return market_data.get_bars(symbol, timeframe, start=start, end=end)


def _safe_quote(market_data, symbol: str) -> Optional[dict[str, Any]]:
    try:
        return market_data.get_latest_quote(symbol)
    except Exception:
        return None


def _coerce_intent(raw: Any) -> Optional[OrderIntent]:
    """Accept either an OrderIntent or a plain dict and return OrderIntent."""
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
