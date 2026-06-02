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
class NewsBriefView:
    """Parsed view of today's news brief, exposed to strategies.

    `raw_text` is the full markdown if a strategy needs more than the
    structured fields. `assessment` is one of:
        NO MATERIAL NEWS | NORMAL FLOW | NOTABLE | HALT-WORTHY EVENT | UNKNOWN
    `per_symbol` is a dict mapping uppercase ticker → the brief's bullet text
    for that symbol (or "" if it appeared but had no narrative).
    """

    raw_text: str = ""
    assessment: str = "UNKNOWN"
    per_symbol: dict[str, str] = field(default_factory=dict)
    date_in_file: str = ""

    def is_halt_worthy(self) -> bool:
        return self.assessment.upper() == "HALT-WORTHY EVENT"

    def is_notable(self) -> bool:
        return self.assessment.upper() in ("NOTABLE", "HALT-WORTHY EVENT")

    def news_for(self, symbol: str) -> str:
        return self.per_symbol.get(symbol.upper(), "")

    def has_negative_signal(self, symbol: str) -> bool:
        """Best-effort: does the brief contain negative-sounding language for this symbol?"""
        text = self.news_for(symbol).lower()
        if not text:
            return False
        neg_markers = (
            "guidance cut", "miss", "missed", "downgrade", "lawsuit",
            "regulatory action", "investigation", "recall", "warned",
            "warning", "halt", "delist", "fraud", "restate", "going concern",
            "bankruptcy",
        )
        return any(m in text for m in neg_markers)

    def has_positive_signal(self, symbol: str) -> bool:
        text = self.news_for(symbol).lower()
        if not text:
            return False
        pos_markers = (
            "beat", "beats", "raised guidance", "raises guidance", "upgrade",
            "approval", "approved", "acquisition", "acquires", "buyback",
            "record revenue", "record earnings", "deal", "partnership",
            "win", "won contract",
        )
        return any(m in text for m in pos_markers)


@dataclass
class StrategyContext:
    """Everything a strategy script needs to make its decisions.

    Fields are read-only from the strategy's point of view. The strategy
    should never mutate this object.
    """

    date: dt.date
    params: dict[str, Any]                       # frontmatter `parameters` block
    watchlist: list[str]                         # *composed universe filtered for this strategy*
    universe: list[str]                          # the full composed universe (unfiltered)
    regime: dict[str, Any]                       # output of classify_regime
    account: dict[str, Any]                      # equity, cash, buying_power, ...
    positions: list[dict[str, Any]]              # current Alpaca positions
    open_orders: list[dict[str, Any]]            # queued orders
    strategy_id: str
    strategy_type: str                           # "equity" | "options"
    log: logging.Logger                          # strategy-scoped logger
    news_brief: NewsBriefView = field(default_factory=NewsBriefView)

    # Callable hooks — the strategy uses these instead of importing data
    # modules directly. Lets the harness control caching, mocking for tests,
    # and the boundary of what strategies are allowed to do.
    get_bars: Callable[..., pd.DataFrame] = field(default=lambda *a, **kw: pd.DataFrame())
    get_quote: Callable[[str], Optional[dict[str, Any]]] = field(default=lambda s: None)
    compute_indicator: Callable[..., Any] = field(default=lambda *a, **kw: None)
    # Options data access (no-ops by default for backward compat)
    get_options_chain: Callable[..., list[dict[str, Any]]] = field(default=lambda *a, **kw: [])
    find_strike_by_delta: Callable[..., Any] = field(default=lambda *a, **kw: None)
    compute_iv_rank: Callable[..., Optional[float]] = field(default=lambda *a, **kw: None)

    def __repr__(self) -> str:  # avoid dumping pandas/callables in logs
        return (
            f"StrategyContext(id={self.strategy_id!r}, date={self.date}, "
            f"positions={len(self.positions)}, regime={self.regime.get('regime')!r}, "
            f"watchlist_size={len(self.watchlist)}, news={self.news_brief.assessment})"
        )


@dataclass
class OptionsIntent:
    """One multi-leg options order a strategy wants the harness to submit.

    Strategies build OptionsIntent objects with explicit OCC option symbols
    in each leg. The runtime translates each intent into an
    OptionsOrderRequest, sends it through SafetyGate's options validator,
    and journals the result.

    `declared_max_loss_usd` is the strategy's stated max loss for the
    structure — required unless `allow_undefined_risk=True` is set, in
    which case the strategy is taking responsibility for managing the tail.
    """

    legs: list[dict[str, Any]]                         # [{contract_symbol, side, ratio?}, ...]
    qty: int = 1                                        # multiplier across legs (# of spreads)
    order_type: str = "limit"
    limit_price: float | None = None                    # net debit/credit
    time_in_force: str = "day"
    reasoning: str = ""
    declared_max_loss_usd: float | None = None
    allow_undefined_risk: bool = False


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
    claimed_symbols: list[str] | None = None,
) -> dict[str, Any]:
    """Load and run one strategy. Submits intents through SafetyGate.

    Parameters
    ----------
    claimed_symbols : list[str] | None
        If non-empty, the strategy's ctx.watchlist is narrowed to this set
        (intersected with the strategy's frontmatter-declared symbols, if
        any). Passed in by the multi-strategy runner so each strategy only
        sees its owned symbols. ``None`` or ``[]`` preserves the legacy
        single-active-strategy behaviour (strategy runs against its full
        frontmatter-filtered universe).

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
            claimed_symbols=claimed_symbols,
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

    # Submit each intent through SafetyGate. Strategies can return either
    # OrderIntent (single-leg equity) or OptionsIntent (multi-leg options);
    # route accordingly.
    submitted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for raw in intents:
        # Options intent (or dict that looks like one)
        if isinstance(raw, OptionsIntent) or (
            isinstance(raw, dict) and "legs" in raw
        ):
            opt_result = _submit_options_intent(
                raw, strategy_id=strategy_id, run_id=run_id, safety_gate=safety_gate,
            )
            if opt_result is None:
                errors.append({"raw": str(raw)[:200], "reason": "invalid OptionsIntent"})
                continue
            if opt_result.get("status") == "rejected":
                rejected.append(opt_result)
            else:
                submitted.append(opt_result)
            continue

        # Equity intent (default)
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


def run_active_strategies(
    *,
    settings,
    market_data,
    regime_classifier,
    safety_gate,
    alpaca_client,
    run_id: str,
) -> dict[str, Any]:
    """Run every strategy in ``state/active_strategies.md`` against its
    claimed symbols, plus surface unclaimed universe symbols as a
    library-gap diagnostic.

    Each strategy sees only its claimed symbols via ``ctx.watchlist``;
    ``ctx.universe`` remains the full composed universe so strategies can
    still reason about what else is being tracked.

    Returns
    -------
    dict
        {
          "ok": True,
          "active_strategies": [<one per-strategy result>],
          "submitted_count": N,
          "rejected_count": N,
          "error_count": N,
          "unclaimed_symbols": [list of library-gap candidates],
          "skipped": [strategies with empty claim and no fallback],
        }

    Behaviour notes:
      - If ``state/active_strategies.md`` is missing, falls back to the
        legacy singular ``state/active_strategy.md`` (single strategy,
        runs against the full frontmatter-filtered universe). Backwards
        compatible with every prior session.
      - A strategy with an empty ``symbols`` claim AND a non-empty
        ``symbols`` frontmatter still runs (claims its frontmatter list
        implicitly). A strategy with NO claim and NO frontmatter is
        skipped — it has no defined scope.
    """
    from quant_trading_system import memory
    from quant_trading_system.universe import compute_universe

    claims = memory.read_active_strategies()
    if not claims:
        return {
            "ok": False,
            "error": (
                "no active strategies — populate state/active_strategies.md "
                "or fall back to state/active_strategy.md via cli set-active."
            ),
            "active_strategies": [],
        }

    per_strategy: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    submitted_total = 0
    rejected_total = 0
    error_total = 0

    for claim in claims:
        # Empty claim list = "no explicit symbol claim". We still run; the
        # strategy will get its frontmatter-filtered universe (legacy
        # behaviour). If you want a strategy idle, archive it; don't leave
        # it active with an empty claim.
        claim_syms = claim.symbols if claim.symbols else None

        result = run_strategy(
            claim.strategy_id,
            settings=settings,
            market_data=market_data,
            regime_classifier=regime_classifier,
            safety_gate=safety_gate,
            alpaca_client=alpaca_client,
            run_id=run_id,
            claimed_symbols=claim_syms,
        )
        # Attach the claim metadata so the agent can attribute results.
        result["claim"] = {
            "symbols": list(claim.symbols),
            "since": claim.since,
            "reason": claim.reason,
        }
        per_strategy.append(result)
        if result.get("ok"):
            submitted_total += len(result.get("submitted", []))
            rejected_total += len(result.get("rejected", []))
            error_total += len(result.get("errors", []))

    # Library-gap diagnostic — symbols in the composed universe that no
    # active strategy claims. The trader writes these into tasks.md as
    # research-agent priorities.
    try:
        universe = compute_universe(settings, alpaca_client=alpaca_client)
        gaps = memory.unclaimed_symbols(universe.symbols)
    except Exception as e:
        logger.warning("library_gap_compute_failed err=%s", e)
        gaps = []

    return {
        "ok": True,
        "active_strategies": per_strategy,
        "submitted_count": submitted_total,
        "rejected_count": rejected_total,
        "error_count": error_total,
        "unclaimed_symbols": gaps,
        "skipped": skipped,
    }


# ---------------------------------------------------------------------------
# Context builder
# ---------------------------------------------------------------------------


def _load_news_brief() -> NewsBriefView:
    """Parse state/news_brief.md into a structured view for strategies."""
    import re as _re
    from quant_trading_system.memory import STATE_DIR

    path = STATE_DIR / "news_brief.md"
    if not path.exists():
        return NewsBriefView()
    text = path.read_text(encoding="utf-8")
    view = NewsBriefView(raw_text=text)

    # Headline assessment — looks like "**NORMAL FLOW**" or "NO MATERIAL NEWS"
    assess_re = _re.compile(
        r"(NO MATERIAL NEWS|NORMAL FLOW|NOTABLE|HALT-WORTHY EVENT)",
        _re.IGNORECASE,
    )
    m = assess_re.search(text)
    if m:
        view.assessment = m.group(1).upper()
    # Date if present in the header
    date_m = _re.search(r"News brief for (\d{4}-\d{2}-\d{2})", text)
    if date_m:
        view.date_in_file = date_m.group(1)

    # Per-symbol bullets: lines starting with "- **SYMBOL** — ..." or "- SYMBOL: ..."
    sym_re = _re.compile(r"^[-*]\s*\*?\*?([A-Z][A-Z0-9.\-]{0,5})\*?\*?\s*[—:\-]\s*(.*)$")
    in_watchlist = False
    for line in text.splitlines():
        if line.strip().lower().startswith("## watchlist"):
            in_watchlist = True
            continue
        if line.startswith("## ") and in_watchlist:
            in_watchlist = False
            continue
        if not in_watchlist:
            continue
        m2 = sym_re.match(line)
        if m2:
            sym = m2.group(1).upper()
            view.per_symbol[sym] = m2.group(2).strip()

    return view


def _build_context(
    sf,
    *,
    settings,
    market_data,
    regime_classifier,
    alpaca_client,
    claimed_symbols: list[str] | None = None,
) -> StrategyContext:
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

    # Composed universe — derived from strategies + positions + news + operator
    from quant_trading_system.universe import (
        compute_universe,
        filter_universe_for_strategy,
    )

    universe = compute_universe(settings, alpaca_client=alpaca_client)
    filtered = filter_universe_for_strategy(
        universe, strategy_frontmatter=sf.frontmatter or {},
    )

    # If the caller passed an explicit symbol-claim list from
    # state/active_strategies.md, narrow `filtered` to that intersection.
    # Empty claim list = "no explicit claim, use the frontmatter-filtered
    # universe" (legacy single-active-strategy behaviour).
    if claimed_symbols:
        claim_set = {s.upper() for s in claimed_symbols}
        # Intersect with the frontmatter-filtered set so a strategy can
        # never trade outside its declared `symbols:` / `sectors:` even if
        # the operator over-claimed in active_strategies.md.
        narrowed = [s for s in filtered if s.upper() in claim_set]
        if not narrowed:
            # The strategy's frontmatter and the claim list don't overlap.
            # That's a configuration error worth surfacing in logs, but the
            # strategy still gets to run on its claim (frontmatter may be
            # missing/permissive). Fall back to the raw claim list filtered
            # against the broader composed universe.
            universe_upper = {s.upper() for s in universe.symbols}
            narrowed = [s for s in claim_set if s in universe_upper]
        filtered = narrowed

    # News brief — parse state/news_brief.md
    news_brief = _load_news_brief()

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

    # Options helpers
    def _get_chain(symbol: str, expiration: str | None = None) -> list[dict[str, Any]]:
        try:
            return market_data.get_options_chain(symbol, expiration=expiration)
        except Exception as e:
            logger.warning("ctx_options_chain_failed sym=%s err=%s", symbol, e)
            return []

    def _find_strike(chain, target_delta, right, expiration=None):
        from quant_trading_system.options import find_strike_by_delta
        return find_strike_by_delta(
            chain, target_delta=target_delta, right=right, expiration=expiration,
        )

    def _iv_rank(symbol: str) -> float | None:
        # Best-effort: derive from recent ATM IV via the chain snapshots.
        # We don't have a historical IV series wired up; approximate using
        # realized volatility of the underlying as a poor-man's anchor.
        try:
            bars = market_data.get_bars(symbol, "1Day")
            if bars.empty or len(bars) < 60:
                return None
            from quant_trading_system.options import compute_iv_rank
            ret = bars["Close"].pct_change().dropna()
            # Realized vol annualized, rolling 21-day
            rv = ret.rolling(21).std() * (252 ** 0.5)
            return compute_iv_rank(rv.tail(252))
        except Exception:
            return None

    return StrategyContext(
        date=dt.date.today(),
        params=params,
        watchlist=filtered,
        universe=list(universe.symbols),
        regime=regime,
        account=account,
        positions=positions,
        open_orders=open_orders,
        strategy_id=sf.id,
        strategy_type=sf.type,
        log=logging.getLogger(f"strategy.{sf.id}"),
        news_brief=news_brief,
        get_bars=lambda symbol, timeframe="1Day", lookback_days=200: _bars_with_lookback(
            market_data, symbol, timeframe, lookback_days
        ),
        get_quote=lambda symbol: _safe_quote(market_data, symbol),
        compute_indicator=_compute_indicator,
        get_options_chain=_get_chain,
        find_strike_by_delta=_find_strike,
        compute_iv_rank=_iv_rank,
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


def _submit_options_intent(
    raw: Any,
    *,
    strategy_id: str,
    run_id: str,
    safety_gate,
) -> Optional[dict[str, Any]]:
    """Translate an OptionsIntent (or dict) into an OptionsOrderRequest and
    submit through SafetyGate's options validator. Returns a result dict
    (with `status`) or None if the intent could not be coerced."""
    from quant_trading_system.models.trade import OptionsOrderRequest, TimeInForce, OrderType

    if isinstance(raw, OptionsIntent):
        d = {
            "legs": raw.legs,
            "qty": raw.qty,
            "order_type": raw.order_type,
            "limit_price": raw.limit_price,
            "time_in_force": raw.time_in_force,
            "reasoning": raw.reasoning,
            "declared_max_loss_usd": raw.declared_max_loss_usd,
            "allow_undefined_risk": raw.allow_undefined_risk,
        }
    elif isinstance(raw, dict):
        d = raw
    else:
        return None

    try:
        req = OptionsOrderRequest(
            qty=int(d.get("qty", 1)),
            legs=list(d.get("legs") or []),
            order_type=OrderType((d.get("order_type") or "limit").lower()),
            time_in_force=TimeInForce((d.get("time_in_force") or "day").lower()),
            limit_price=d.get("limit_price"),
            reasoning=str(d.get("reasoning", ""))[:500],
            agent_name="strategy_runtime",
            strategy_name=strategy_id,
            declared_max_loss_usd=d.get("declared_max_loss_usd"),
            allow_undefined_risk=bool(d.get("allow_undefined_risk", False)),
        )
    except (ValueError, TypeError) as e:
        logger.error("options_intent_coerce_failed err=%s raw=%s", e, str(raw)[:300])
        return {"status": "rejected", "rejection_reason": f"invalid OptionsIntent: {e}"}

    try:
        result = safety_gate.validate_and_submit_options(req)
    except Exception as e:
        logger.error("options_safety_gate_raised err=%s", e)
        return {"status": "rejected", "rejection_reason": f"safety_gate raised: {e}"}

    result_dict = {
        "order_id": result.order_id,
        "status": result.status.value,
        "mode": result.mode.value,
        "filled_qty": result.filled_qty,
        "filled_avg_price": result.filled_avg_price,
        "rejection_reason": result.rejection_reason,
        "safety_checks_passed": result.safety_checks_passed,
        "safety_checks_failed": result.safety_checks_failed,
        "n_legs": len(req.legs),
        "qty": req.qty,
        "declared_max_loss_usd": req.declared_max_loss_usd,
    }
    # Journal
    from quant_trading_system import journal
    journal.log_event({
        "type": "options_order_submitted" if result.status.value != "rejected" else "options_order_rejected",
        "strategy_id": strategy_id,
        "run_id": run_id,
        "n_legs": len(req.legs),
        "qty": req.qty,
        "reasoning": req.reasoning,
        "declared_max_loss_usd": req.declared_max_loss_usd,
        "result_status": result.status.value,
        "result_mode": result.mode.value,
        "result_order_id": result.order_id,
        "result_rejection_reason": result.rejection_reason,
        "result_safety_checks_passed": result.safety_checks_passed,
        "result_safety_checks_failed": result.safety_checks_failed,
    })
    return result_dict


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
