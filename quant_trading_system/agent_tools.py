"""Tool functions exposed to the orchestrator agent.

Every public function in this module is a tool the LLM can call. The tool
*schema* (name, description, input_schema as Anthropic expects) lives in
`tool_registry.py` — this file is just the Python implementations.

Conventions:
- Every function takes a `ctx: ToolContext` first, then keyword-only args.
- Return values are JSON-serializable dicts/lists/scalars (no DataFrames, no
  Pydantic models). The orchestrator passes them straight back to Claude.
- Errors return {"error": "..."} rather than raising; the agent should be able
  to read what went wrong and try something else.
- Trading tools tag every order with the caller-provided `strategy_id` and
  log to the journal so the next day's run can attribute outcomes.
"""

from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass
from typing import Any

import structlog

from quant_trading_system import health, journal, memory
from quant_trading_system.models.trade import (
    OrderRequest,
    OrderSide,
    OrderType,
    TimeInForce,
)

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Tool context
# ---------------------------------------------------------------------------


@dataclass
class ToolContext:
    """Bundle of shared dependencies passed into every tool call."""

    settings: Any
    market_data: Any
    regime_classifier: Any
    safety_gate: Any
    alpaca_client: Any | None
    run_id: str

    @property
    def is_dry_run(self) -> bool:
        return bool(getattr(self.settings, "DRY_RUN", False))


def _ok(payload: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, **payload}


def _err(msg: str, **extra) -> dict[str, Any]:
    return {"ok": False, "error": msg, **extra}


# ---------------------------------------------------------------------------
# Strategy I/O
# ---------------------------------------------------------------------------


def list_strategies(
    ctx: ToolContext,
    *,
    status: str | None = None,
    type: str | None = None,
    include_archived: bool = False,
) -> dict[str, Any]:
    """List strategies on disk."""
    items = memory.list_strategies(
        status=status, type_filter=type, include_archived=include_archived
    )
    return _ok({"count": len(items), "strategies": [s.summary_dict() for s in items]})


def read_strategy(ctx: ToolContext, *, strategy_id: str) -> dict[str, Any]:
    """Return the full markdown of one strategy (frontmatter + body)."""
    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return _err(f"strategy not found: {strategy_id}")
    return _ok({
        "id": sf.id,
        "type": sf.type,
        "path": str(sf.path),
        "frontmatter": sf.frontmatter,
        "body": sf.body,
    })


def update_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    frontmatter_updates: dict[str, Any] | None = None,
    body: str | None = None,
) -> dict[str, Any]:
    """Edit an existing strategy. Frontmatter merges; body fully replaces."""
    try:
        sf = memory.update_strategy(
            strategy_id, frontmatter_updates=frontmatter_updates, body=body
        )
    except FileNotFoundError as e:
        return _err(str(e))
    return _ok({
        "id": sf.id,
        "path": str(sf.path),
        "frontmatter": sf.frontmatter,
    })


def create_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    type: str,
    frontmatter: dict[str, Any],
    body: str,
) -> dict[str, Any]:
    """Create a new strategy file. Type must be 'equity' or 'options'."""
    try:
        sf = memory.create_strategy(strategy_id, type, frontmatter, body)
    except (FileExistsError, ValueError) as e:
        return _err(str(e))
    return _ok({"id": sf.id, "path": str(sf.path)})


def archive_strategy(
    ctx: ToolContext, *, strategy_id: str, reason: str = ""
) -> dict[str, Any]:
    """Move a strategy to the archived/ subdir and mark status=archived."""
    try:
        sf = memory.archive_strategy(strategy_id, reason=reason)
    except FileNotFoundError as e:
        return _err(str(e))
    return _ok({"id": sf.id, "path": str(sf.path), "status": sf.status})


# ---------------------------------------------------------------------------
# Conclusions / state files
# ---------------------------------------------------------------------------


def write_conclusion(ctx: ToolContext, *, content: str) -> dict[str, Any]:
    """Write today's conclusion file. Overwrites if it already exists."""
    p = memory.write_conclusion(content)
    return _ok({"path": str(p)})


def append_conclusion(ctx: ToolContext, *, content: str) -> dict[str, Any]:
    """Append to today's conclusion file (creates it if absent)."""
    p = memory.append_conclusion(content)
    return _ok({"path": str(p)})


def read_recent_conclusions(ctx: ToolContext, *, days: int = 14) -> dict[str, Any]:
    """Return the last `days` worth of daily conclusion files."""
    return _ok({"conclusions": memory.read_recent_conclusions(days=days)})


def read_handoff(ctx: ToolContext) -> dict[str, Any]:
    """Read the handoff note from yesterday's run."""
    return _ok({"content": memory.read_handoff()})


def write_handoff(ctx: ToolContext, *, content: str) -> dict[str, Any]:
    """Replace the handoff note for tomorrow's run. Always do this last."""
    p = memory.write_handoff(content)
    return _ok({"path": str(p)})


def get_active_strategy(ctx: ToolContext) -> dict[str, Any]:
    """Read which strategy is currently active and why."""
    return _ok(memory.read_active_strategy() or {"strategy_id": "", "since": "", "reason": ""})


def set_active_strategy(
    ctx: ToolContext, *, strategy_id: str, reason: str, notes: str = ""
) -> dict[str, Any]:
    """Switch the active strategy. Use sparingly — see harness instructions."""
    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return _err(f"strategy not found: {strategy_id}")
    p = memory.set_active_strategy(strategy_id, reason=reason, notes=notes)
    return _ok({"path": str(p), "strategy_id": strategy_id})


def read_summary(ctx: ToolContext) -> dict[str, Any]:
    """Read the rolling long-horizon summary."""
    return _ok({"content": memory.read_summary()})


def update_summary(ctx: ToolContext, *, content: str) -> dict[str, Any]:
    """Replace the rolling summary. Update only when there's a real new lesson."""
    p = memory.write_summary(content)
    return _ok({"path": str(p)})


# ---------------------------------------------------------------------------
# Market data
# ---------------------------------------------------------------------------


def get_bars(
    ctx: ToolContext,
    *,
    symbol: str,
    timeframe: str = "1Day",
    lookback_days: int = 60,
) -> dict[str, Any]:
    """Recent OHLCV bars. Returns the last 60 rows max to keep prompts small."""
    end = dt.date.today().isoformat()
    start = (dt.date.today() - dt.timedelta(days=lookback_days)).isoformat()
    try:
        df = ctx.market_data.get_bars(symbol, timeframe, start=start, end=end)
    except Exception as e:
        return _err(f"market_data error: {e}")
    if df.empty:
        return _err("no data", symbol=symbol, timeframe=timeframe)
    df = df.tail(60)
    rows = [
        {
            "date": str(idx.date()) if hasattr(idx, "date") else str(idx),
            "open": float(r["Open"]),
            "high": float(r["High"]),
            "low": float(r["Low"]),
            "close": float(r["Close"]),
            "volume": float(r["Volume"]),
        }
        for idx, r in df.iterrows()
    ]
    return _ok({"symbol": symbol, "timeframe": timeframe, "bars": rows})


def classify_regime(ctx: ToolContext, *, symbol: str = "SPY") -> dict[str, Any]:
    """Classify current market regime from a benchmark symbol (default SPY)."""
    try:
        df = ctx.market_data.get_bars(symbol, "1Day")
        result = ctx.regime_classifier.classify(df)
    except Exception as e:
        return _err(f"regime classification failed: {e}")
    return _ok(result)


def compute_indicator(
    ctx: ToolContext,
    *,
    symbol: str,
    indicator: str,
    period: int | None = None,
    lookback_days: int = 250,
) -> dict[str, Any]:
    """Compute a single technical indicator's most recent value(s).

    Supported indicators: sma, ema, rsi, macd, bbands, atr, adx, obv.
    """
    from quant_trading_system.tools import technical_indicators as ti

    end = dt.date.today().isoformat()
    start = (dt.date.today() - dt.timedelta(days=lookback_days)).isoformat()
    try:
        df = ctx.market_data.get_bars(symbol, "1Day", start=start, end=end)
    except Exception as e:
        return _err(f"market data error: {e}")
    if df.empty:
        return _err("no data", symbol=symbol)

    name = indicator.lower()
    try:
        if name == "sma":
            s = ti.compute_sma(df["Close"], period or 20)
            value = float(s.iloc[-1])
        elif name == "ema":
            s = ti.compute_ema(df["Close"], period or 20)
            value = float(s.iloc[-1])
        elif name == "rsi":
            s = ti.compute_rsi(df["Close"], period or 14)
            value = float(s.iloc[-1])
        elif name == "macd":
            m = ti.compute_macd(df["Close"])
            return _ok({
                "symbol": symbol,
                "indicator": "macd",
                "macd": float(m["MACD"].iloc[-1]),
                "signal": float(m["Signal"].iloc[-1]),
                "histogram": float(m["Histogram"].iloc[-1]),
            })
        elif name in ("bb", "bbands", "bollinger"):
            b = ti.compute_bollinger_bands(df["Close"], period or 20)
            return _ok({
                "symbol": symbol,
                "indicator": "bbands",
                "upper": float(b["Upper"].iloc[-1]),
                "middle": float(b["Middle"].iloc[-1]),
                "lower": float(b["Lower"].iloc[-1]),
            })
        elif name == "atr":
            s = ti.compute_atr(df["High"], df["Low"], df["Close"], period or 14)
            value = float(s.iloc[-1])
        elif name == "adx":
            s = ti.compute_adx(df["High"], df["Low"], df["Close"], period or 14)
            value = float(s.iloc[-1])
        elif name == "obv":
            s = ti.compute_obv(df["Close"], df["Volume"])
            value = float(s.iloc[-1])
        else:
            return _err(f"unknown indicator: {indicator}")
    except Exception as e:
        return _err(f"indicator computation failed: {e}")

    return _ok({
        "symbol": symbol,
        "indicator": name,
        "period": period,
        "value": value,
        "as_of": str(df.index[-1].date() if hasattr(df.index[-1], "date") else df.index[-1]),
    })


def get_quote(ctx: ToolContext, *, symbol: str) -> dict[str, Any]:
    """Latest bid/ask. May be None if outside Alpaca data hours."""
    try:
        q = ctx.market_data.get_latest_quote(symbol)
    except Exception as e:
        return _err(f"quote error: {e}")
    if q is None:
        return _err("no quote available", symbol=symbol)
    return _ok({"symbol": symbol, **q})


def market_status(ctx: ToolContext) -> dict[str, Any]:
    """Whether the US equities market is open right now and the next open time."""
    from quant_trading_system.scheduler.market_schedule import (
        is_market_open,
        next_market_open,
    )

    return _ok({
        "is_open": is_market_open(),
        "next_open_iso": next_market_open().isoformat(),
        "now_iso": dt.datetime.now().astimezone().isoformat(),
    })


# ---------------------------------------------------------------------------
# Portfolio / orders
# ---------------------------------------------------------------------------


def get_account(ctx: ToolContext) -> dict[str, Any]:
    """Account equity, cash, buying power."""
    if ctx.alpaca_client is None:
        return _ok({
            "equity": ctx.settings.PAPER_PORTFOLIO_SIZE,
            "cash": ctx.settings.PAPER_PORTFOLIO_SIZE,
            "buying_power": ctx.settings.PAPER_PORTFOLIO_SIZE,
            "note": "no broker client (DRY_RUN or unconfigured)",
        })
    try:
        return _ok(ctx.alpaca_client.get_account())
    except Exception as e:
        return _err(f"alpaca error: {e}")


def get_positions(ctx: ToolContext) -> dict[str, Any]:
    """All currently held positions."""
    if ctx.alpaca_client is None:
        return _ok({"positions": []})
    try:
        return _ok({"positions": ctx.alpaca_client.get_positions()})
    except Exception as e:
        return _err(f"alpaca error: {e}")


def get_open_orders(ctx: ToolContext) -> dict[str, Any]:
    """All open orders on Alpaca, including those queued for the next session."""
    if ctx.alpaca_client is None:
        return _ok({"orders": []})
    try:
        orders = ctx.alpaca_client.get_open_orders()
        out = []
        for o in orders:
            out.append({
                "id": str(o.id),
                "symbol": o.symbol,
                "qty": float(o.qty) if o.qty else 0.0,
                "side": o.side.value if o.side else "",
                "type": o.type.value if o.type else "",
                "time_in_force": o.time_in_force.value if o.time_in_force else "",
                "limit_price": float(o.limit_price) if o.limit_price else None,
                "stop_price": float(o.stop_price) if o.stop_price else None,
                "submitted_at": str(o.submitted_at) if getattr(o, "submitted_at", None) else "",
                "client_order_id": o.client_order_id or "",
            })
        return _ok({"orders": out})
    except Exception as e:
        return _err(f"alpaca error: {e}")


def get_recent_trades(
    ctx: ToolContext, *, days: int = 30, strategy_id: str | None = None
) -> dict[str, Any]:
    """Recent journal events: order submissions, rejections, closes."""
    events = journal.read_events(days=days, strategy_id=strategy_id)
    return _ok({"count": len(events), "events": events})


def get_strategy_health(
    ctx: ToolContext, *, strategy_id: str, lookback_days: int = 30
) -> dict[str, Any]:
    """Deterministic health snapshot for one strategy."""
    return _ok(
        health.compute_strategy_health(
            strategy_id,
            market_data=ctx.market_data,
            alpaca_client=ctx.alpaca_client,
            lookback_days=lookback_days,
        )
    )


def get_portfolio_health(
    ctx: ToolContext, *, lookback_days: int = 30
) -> dict[str, Any]:
    """Portfolio-wide health snapshot across all active strategies."""
    return _ok(
        health.compute_portfolio_health(
            market_data=ctx.market_data,
            alpaca_client=ctx.alpaca_client,
            lookback_days=lookback_days,
        )
    )


# ---------------------------------------------------------------------------
# Sizing
# ---------------------------------------------------------------------------


def kelly_position_size(
    ctx: ToolContext,
    *,
    win_rate: float,
    avg_win: float,
    avg_loss: float,
    portfolio_value: float | None = None,
    price_per_share: float,
    fraction: float = 0.5,
    max_position_pct: float | None = None,
) -> dict[str, Any]:
    """Return shares + dollar amount using fractional Kelly, capped by config."""
    from quant_trading_system.tools.kelly_criterion import (
        kelly_fraction,
        position_size,
    )

    if portfolio_value is None:
        if ctx.alpaca_client is not None:
            try:
                portfolio_value = float(ctx.alpaca_client.get_account()["equity"])
            except Exception:
                portfolio_value = ctx.settings.PAPER_PORTFOLIO_SIZE
        else:
            portfolio_value = ctx.settings.PAPER_PORTFOLIO_SIZE

    cap = max_position_pct if max_position_pct is not None else ctx.settings.MAX_POSITION_SIZE_PCT
    full = kelly_fraction(win_rate, avg_win, avg_loss)
    f = full * fraction
    shares = position_size(f, portfolio_value, price_per_share, max_position_pct=cap)
    return _ok({
        "kelly_fraction_full": round(full, 4),
        "kelly_fraction_used": round(f, 4),
        "shares": shares,
        "dollar_amount": round(shares * price_per_share, 2),
        "portfolio_value": round(portfolio_value, 2),
        "max_position_pct": cap,
    })


# ---------------------------------------------------------------------------
# Trading
# ---------------------------------------------------------------------------


def submit_order(
    ctx: ToolContext,
    *,
    symbol: str,
    side: str,
    qty: float,
    order_type: str = "market",
    strategy_id: str,
    time_in_force: str = "day",
    limit_price: float | None = None,
    stop_price: float | None = None,
    reasoning: str = "",
) -> dict[str, Any]:
    """Submit an order. Always passes through SafetyGate. Always tagged with
    strategy_id and logged to the trade journal."""
    try:
        order = OrderRequest(
            symbol=symbol.upper(),
            side=OrderSide(side.lower()),
            qty=qty,
            order_type=OrderType(order_type.lower()),
            time_in_force=TimeInForce(time_in_force.lower()),
            limit_price=limit_price,
            stop_price=stop_price,
            agent_name="orchestrator",
            strategy_name=strategy_id,
            reasoning=reasoning,
        )
    except (ValueError, TypeError) as e:
        return _err(f"invalid order: {e}")

    try:
        result = ctx.safety_gate.validate_and_submit(order)
    except Exception as e:
        return _err(f"safety_gate error: {e}")

    result_dict = {
        "order_id": result.order_id,
        "status": result.status.value,
        "mode": result.mode.value,
        "filled_qty": result.filled_qty,
        "filled_avg_price": result.filled_avg_price,
        "rejection_reason": result.rejection_reason,
        "safety_checks_passed": result.safety_checks_passed,
        "safety_checks_failed": result.safety_checks_failed,
    }

    journal.log_order(
        strategy_id=strategy_id,
        run_id=ctx.run_id,
        order_request=order.model_dump(),
        order_result=result_dict,
    )

    return _ok(result_dict)


def cancel_order(ctx: ToolContext, *, order_id: str) -> dict[str, Any]:
    """Cancel an open order on Alpaca."""
    if ctx.alpaca_client is None:
        return _err("no broker client connected")
    try:
        ctx.alpaca_client.cancel_order(order_id)
    except Exception as e:
        return _err(f"alpaca error: {e}")
    journal.log_event({
        "type": "order_cancelled",
        "run_id": ctx.run_id,
        "order_id": order_id,
    })
    return _ok({"order_id": order_id, "cancelled": True})


def propose_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    type: str,
    frontmatter: dict[str, Any],
    md_body: str,
    py_source: str,
    backtest_symbol: str = "SPY",
    backtest_start: str | None = None,
    backtest_end: str | None = None,
    skip_backtest: bool = False,
) -> dict[str, Any]:
    """Add a new strategy to the library, gated on the full ADD battery.

    The decision is fully deterministic via `strategy_evaluation.evaluate_for_addition`
    (PSR, walk-forward IS/OOS check, Sortino, max-drawdown, trade count). The
    agent does not override the result. Three outcomes:

      - ADD passed: strategy saved at status='testing'.
      - REJECT (blocked_by_data): backtest could not run; strategy retained
        at status='testing' with note "do not promote until verified".
      - REJECT (performance): strategy folder removed.
    """
    import datetime as _dt
    from quant_trading_system.strategy_evaluation import evaluate_for_addition

    if type not in ("equity", "options"):
        return _err(f"type must be 'equity' or 'options', got {type!r}")
    try:
        compile(py_source, f"<{strategy_id}>", "exec")
    except SyntaxError as e:
        return _err(f"strategy.py has a syntax error: {e}")
    if "def evaluate(" not in py_source:
        return _err("strategy.py must define `def evaluate(ctx):`")

    try:
        sf = memory.create_strategy(
            strategy_id=strategy_id,
            type=type,
            frontmatter_data=frontmatter,
            body=md_body,
            script=py_source,
        )
    except (FileExistsError, ValueError) as e:
        return _err(str(e))

    if type == "options" or skip_backtest:
        return _ok({
            "id": sf.id,
            "path": str(sf.dir),
            "status": sf.status,
            "evaluation": None,
            "note": (
                "options strategy added without battery (no chain data); "
                "kept at status='testing' for manual review"
                if type == "options"
                else "battery skipped on caller request; kept at status='testing'"
            ),
        })

    if backtest_end is None:
        backtest_end = _dt.date.today().isoformat()
    if backtest_start is None:
        backtest_start = (_dt.date.today() - _dt.timedelta(days=730)).isoformat()

    try:
        result = evaluate_for_addition(
            sf.id,
            symbol=backtest_symbol,
            start=backtest_start,
            end=backtest_end,
            market_data=ctx.market_data,
            regime_classifier=ctx.regime_classifier,
        )
    except Exception as e:
        return _ok({
            "id": sf.id,
            "path": str(sf.dir),
            "status": sf.status,
            "evaluation": {"error": f"battery raised: {e}"},
            "note": "kept at status='testing'; battery could not be evaluated",
        })

    # Tests blocked by missing data → keep with explicit warning, do not promote
    if result.get("blocked_by_data"):
        return _ok({
            "id": sf.id,
            "path": str(sf.dir),
            "status": sf.status,
            "evaluation": result,
            "note": (
                "kept at status='testing'; addition battery could not run "
                "(data unavailable). Do not promote until verified."
            ),
        })

    if result.get("decision") == "ADD":
        return _ok({
            "id": sf.id,
            "path": str(sf.dir),
            "status": sf.status,
            "evaluation": result,
            "note": "ADDED at status='testing'; addition battery passed all tests",
        })

    # REJECT on real test failure — remove the folder
    cleanup_err = None
    try:
        for f in sf.dir.iterdir():
            f.unlink()
        sf.dir.rmdir()
    except OSError as e:
        cleanup_err = str(e)
    note = (
        f"REJECTED by addition battery: {'; '.join(result.get('reasons', []))}. "
        + ("Folder removed." if not cleanup_err else f"Manual cleanup needed: {cleanup_err}")
    )
    return _ok({
        "id": strategy_id,
        "status": "rejected_but_not_cleaned" if cleanup_err else "rejected",
        "evaluation": result,
        "note": note,
    })


def evaluate_addition(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbol: str = "SPY",
    start: str | None = None,
    end: str | None = None,
) -> dict[str, Any]:
    """Run the addition test battery on an existing strategy (no side effects).

    Useful for retesting a candidate already on disk, or for the agent to
    inspect why something would be rejected without going through propose.
    """
    import datetime as _dt
    from quant_trading_system.strategy_evaluation import evaluate_for_addition

    if end is None:
        end = _dt.date.today().isoformat()
    if start is None:
        start = (_dt.date.today() - _dt.timedelta(days=730)).isoformat()
    try:
        return _ok(evaluate_for_addition(
            strategy_id,
            symbol=symbol, start=start, end=end,
            market_data=ctx.market_data,
            regime_classifier=ctx.regime_classifier,
        ))
    except Exception as e:
        return _err(f"battery raised: {e}")


def evaluate_replacement(
    ctx: ToolContext,
    *,
    existing_id: str,
    candidate_id: str,
    symbol: str = "SPY",
    start: str | None = None,
    end: str | None = None,
) -> dict[str, Any]:
    """Run the replacement test (paired bootstrap + Sharpe-delta) on two
    strategies. Decision is REPLACE only if candidate beats existing at
    p<0.05 AND Sharpe delta >= 0.10 absolute. Strict, deterministic.
    """
    import datetime as _dt
    from quant_trading_system.strategy_evaluation import evaluate_for_replacement

    if end is None:
        end = _dt.date.today().isoformat()
    if start is None:
        start = (_dt.date.today() - _dt.timedelta(days=730)).isoformat()
    try:
        return _ok(evaluate_for_replacement(
            existing_id, candidate_id,
            symbol=symbol, start=start, end=end,
            market_data=ctx.market_data,
            regime_classifier=ctx.regime_classifier,
        ))
    except Exception as e:
        return _err(f"battery raised: {e}")


def evaluate_archive(
    ctx: ToolContext,
    *,
    strategy_id: str,
) -> dict[str, Any]:
    """Run the archive test (conservative — 90-day rolling Sharpe<0 AND
    PSR<0.5, OR 60-day zero-trades). Reads the trade journal directly;
    no backtest involved.
    """
    from quant_trading_system.strategy_evaluation import evaluate_for_archive

    try:
        return _ok(evaluate_for_archive(strategy_id))
    except Exception as e:
        return _err(f"battery raised: {e}")


def simulate_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbol: str = "SPY",
    start: str | None = None,
    end: str | None = None,
) -> dict[str, Any]:
    """Run the walk-forward backtester without persisting any changes.

    Useful when the agent wants to test a hypothetical edit before applying
    it, or to verify an existing strategy's behavior over a window.
    """
    import datetime as _dt
    from quant_trading_system.strategy_backtest import run_backtest

    if end is None:
        end = _dt.date.today().isoformat()
    if start is None:
        start = (_dt.date.today() - _dt.timedelta(days=730)).isoformat()
    try:
        bt = run_backtest(
            strategy_id=strategy_id,
            symbol=symbol,
            start=start,
            end=end,
            market_data=ctx.market_data,
            regime_classifier=ctx.regime_classifier,
        )
    except Exception as e:
        return _err(f"backtester raised: {e}")
    return _ok(bt.to_dict())


def git_doctor(ctx: ToolContext) -> dict[str, Any]:
    """Report state of the git-sync queue + any stale .git/*.lock files.

    The harness sandbox CANNOT unlink files inside .git/, so this tool no
    longer tries. Instead it reports what's wedged and tells the operator
    how to fix it (one-time install of the launchd agents in
    scripts/install_git_safety.sh).
    """
    from quant_trading_system.git_sync import QUEUE_DIRNAME
    from quant_trading_system.memory import _REPO_ROOT
    import time as _time

    root = _REPO_ROOT
    lock_files: list[dict[str, Any]] = []
    git_dir = root / ".git"
    if git_dir.exists():
        for p in git_dir.rglob("*.lock"):
            try:
                age = int(_time.time() - p.stat().st_mtime)
            except OSError:
                age = -1
            lock_files.append({"path": str(p.relative_to(root)), "age_s": age})

    queue_dir = root / QUEUE_DIRNAME
    pending_markers = []
    if queue_dir.exists():
        pending_markers = sorted(
            str(p.relative_to(root))
            for p in queue_dir.glob("*.json")
        )

    notes: list[str] = []
    if lock_files:
        notes.append(
            f"{len(lock_files)} .git/*.lock file(s) present. The harness "
            "cannot remove them (sandbox permission boundary). If the "
            "launchd com.harness.gitlock agent is installed, they'll be "
            "swept within ~10s. Otherwise run "
            "scripts/install_git_safety.sh from a real terminal."
        )
    if pending_markers:
        notes.append(
            f"{len(pending_markers)} commit marker(s) pending in "
            f"{QUEUE_DIRNAME}/. The com.harness.gitrunner agent processes "
            "them every 30s. If they keep accumulating, the agent isn't "
            "installed — run scripts/install_git_safety.sh."
        )
    if not notes:
        notes.append("repo is clean — no stale locks, no pending commit markers.")

    return _ok({
        "repo": str(root),
        "stale_lock_count": len(lock_files),
        "stale_locks": lock_files,
        "pending_marker_count": len(pending_markers),
        "pending_markers": pending_markers[:20],
        "note": " ".join(notes),
    })


def git_sync(
    ctx: ToolContext,
    *,
    message: str,
    agent: str | None = None,
    push: bool = True,
    pull_first: bool = True,
) -> dict[str, Any]:
    """Commit and push everything that changed in the repo since the last sync.

    Called as the final action of each scheduled-task agent. If `agent` is
    given, the commit message is auto-prefixed with `[<agent> YYYY-MM-DD] `
    so commit history is consistently dated and attributed.

    Best-effort: a git error does not fail the run, just gets reported back
    so the agent can document it in its handoff.
    """
    import datetime as _dt
    from quant_trading_system.git_sync import git_sync as _do_sync

    full_message = message
    if agent:
        today = _dt.date.today().isoformat()
        prefix = f"[{agent} {today}] "
        if not message.startswith(prefix):
            full_message = prefix + message
    return _ok(_do_sync(
        ctx.settings,
        message=full_message,
        agent=agent or "manual",
        push=push,
        pull_first=pull_first,
    ))


def news_fetch(
    ctx: ToolContext,
    *,
    symbols: list[str] | None = None,
    include_positions: bool = True,
    lookback_hours: int = 24,
) -> dict[str, Any]:
    """Fetch Alpaca News for the composed universe and write per-symbol +
    per-sector HTMLs under knowledge_base/news/.

    When `symbols` is None, the universe is the composed one from
    `universe.compute_universe`: active strategies' declared symbols,
    currently-held positions, news-tracked subdirs, and operator-added
    symbols in `state/extra_symbols.md`. The env-var DEFAULT_WATCHLIST is
    only the bootstrap fallback when nothing else has anything (handled
    inside compute_universe). This means operator additions to
    extra_symbols.md are picked up automatically on the next run — no need
    to also pre-create the news subdir (the fetch will create it as a
    side-effect of writing the per-symbol HTML).

    Returns a summary dict; the news agent uses this to know what got written.
    """
    from quant_trading_system import news_service
    from quant_trading_system.universe import compute_universe

    if symbols:
        # Explicit override — respect the caller's list verbatim.
        universe = {s.upper() for s in symbols if s and s.strip()}
    else:
        # Use the composed universe (strategies + positions + news-tracked +
        # operator_extras + bootstrap fallback). compute_universe already
        # consults the broker for held positions when alpaca_client is set.
        composed = compute_universe(
            ctx.settings,
            alpaca_client=ctx.alpaca_client if include_positions else None,
        )
        universe = set(composed.symbols)
    if not universe:
        return _err("empty universe; nothing to fetch")
    return _ok(news_service.fetch_and_write(
        ctx.settings, sorted(universe), lookback_hours=lookback_hours,
    ))


def news_cleanup(ctx: ToolContext, *, retention_days: int = 90) -> dict[str, Any]:
    """Sweep dated news HTMLs older than `retention_days` days."""
    from quant_trading_system import news_service

    return _ok(news_service.cleanup_old(retention_days=retention_days))


def news_universe(ctx: ToolContext) -> dict[str, Any]:
    """Return the symbols / sectors / categories the news layer covers,
    derived from the composed universe (strategies + positions + news +
    operator additions). Bootstrap env-var watchlist is the fallback when
    nothing else has declared anything."""
    from quant_trading_system.news_service import (
        CATEGORIES,
        SYMBOL_TO_SECTOR,
        sector_for,
    )
    from quant_trading_system.universe import compute_universe

    universe = compute_universe(ctx.settings, alpaca_client=ctx.alpaca_client)
    by_sector: dict[str, list[str]] = {}
    for s in universe.symbols:
        by_sector.setdefault(sector_for(s), []).append(s)
    return _ok({
        "universe": universe.to_dict(),
        "sectors": by_sector,
        "categories": list(CATEGORIES),
        "sector_map": SYMBOL_TO_SECTOR,
    })


def universe_view(ctx: ToolContext, *, include_testing: bool = False) -> dict[str, Any]:
    """Return today's composed universe with provenance per symbol.

    Sources: active strategies' declared symbols/sectors, currently-held
    positions, news-tracked symbols (subdirs under news/stocks/),
    operator additions in state/extra_symbols.md. The env-var
    DEFAULT_WATCHLIST is used only as a fallback when none of the above
    have anything.
    """
    from quant_trading_system.universe import compute_universe

    universe = compute_universe(
        ctx.settings,
        alpaca_client=ctx.alpaca_client,
        include_testing_strategies=include_testing,
    )
    return _ok(universe.to_dict())


def promote_candidate(
    ctx: ToolContext,
    *,
    symbol: str,
    sector: str,
    reason: str = "",
    agent: str = "",
) -> dict[str, Any]:
    """Promote a symbol into the universe by appending it to extra_symbols.md,
    recording its sector in symbol_sectors.md, and creating its news folder.

    Used by the news agent (recurring-candidate flow + single-event flow) and
    by the trader (when the operator wants a specific name added immediately).
    Idempotent — re-running with the same symbol is a no-op apart from
    logging. **Sector is required** to prevent any newly-promoted symbol
    from silently rolling up to "uncategorized" in the sector view; the
    legacy "skip sector and figure it out later" path is gone.

    Args:
        symbol: ticker (e.g. "MRVL"). Case-insensitive; stored uppercase.
        sector: one of `news_service.ALLOWED_SECTORS` (e.g. "technology",
            "financials", "index"). Required.
        reason: short human-readable rationale (e.g. "3+ session recurrence
            in news brief candidates section"). Recorded as a comment line.
        agent: which agent is promoting ("news", "trader", "research", or "").
            Used only in the comment for audit.

    Returns:
        {"ok": True, "promoted": True/False, "symbol": ..., "already_present": ...,
         "extra_symbols_path": ..., "news_folder_created": ...,
         "sector": ..., "sector_recorded": True/False,
         "symbol_sectors_path": ...}
        promoted=False means the symbol was already in extra_symbols.md.
        sector_recorded=False means the sector entry was already present.
    """
    from pathlib import Path
    from quant_trading_system.universe import EXTRA_SYMBOLS_FILE, symbols_from_operator
    from quant_trading_system.news_service import (
        STOCKS_DIR,
        SYMBOL_SECTORS_FILE,
        ALLOWED_SECTORS,
        reload_sector_overrides,
        SYMBOL_TO_SECTOR,
    )

    sym = (symbol or "").strip().upper()
    if not sym or not sym.isalnum() or not (1 < len(sym) <= 5):
        return _err(f"invalid symbol: {symbol!r} (expect 2-5 uppercase alnum chars)")

    sec = (sector or "").strip().lower()
    if not sec:
        return _err("sector is required (one of: " + ", ".join(sorted(ALLOWED_SECTORS)) + ")")
    if sec not in ALLOWED_SECTORS:
        return _err(
            f"invalid sector: {sector!r} (expect one of: "
            + ", ".join(sorted(ALLOWED_SECTORS)) + ")"
        )

    already = sym in symbols_from_operator()
    extras_path = Path(EXTRA_SYMBOLS_FILE)
    extras_path.parent.mkdir(parents=True, exist_ok=True)
    if not extras_path.exists():
        extras_path.write_text(
            "# Extra symbols\n#\n# Operator/agent-declared additions to the harness universe.\n#\n",
            encoding="utf-8",
        )

    if not already:
        today = dt.date.today().isoformat()
        agent_tag = f"{agent}, " if agent else ""
        reason_tag = f": {reason}" if reason else ""
        block = f"\n# Added {today} ({agent_tag}promote-candidate){reason_tag}\n{sym}\n"
        with extras_path.open("a", encoding="utf-8") as f:
            f.write(block)

    # Record the sector. Skip if the symbol already has an identical entry
    # (idempotent); overwrite-via-append is fine because the reader takes
    # the *last* entry per symbol implicitly when iterating top-to-bottom
    # and the loader resolves on dict.update().
    sectors_path = Path(SYMBOL_SECTORS_FILE)
    sectors_path.parent.mkdir(parents=True, exist_ok=True)
    if not sectors_path.exists():
        sectors_path.write_text(
            "# Symbol → sector overrides\n#\n"
            "# Loaded at import time by news_service.SYMBOL_TO_SECTOR.\n#\n",
            encoding="utf-8",
        )
    existing_sec = SYMBOL_TO_SECTOR.get(sym)
    sector_recorded = False
    if existing_sec != sec:
        today = dt.date.today().isoformat()
        agent_tag = f"{agent}, " if agent else ""
        sector_block = (
            f"\n# Added {today} ({agent_tag}promote-candidate)\n{sym}: {sec}\n"
        )
        with sectors_path.open("a", encoding="utf-8") as f:
            f.write(sector_block)
        # Refresh the in-process map so a subsequent call in the same
        # process sees the new entry.
        reload_sector_overrides()
        sector_recorded = True

    # Ensure the news folder exists so news-fetch starts tracking next run.
    folder = STOCKS_DIR / sym
    created = not folder.exists()
    folder.mkdir(parents=True, exist_ok=True)

    return _ok({
        "promoted": not already,
        "symbol": sym,
        "already_present": already,
        "extra_symbols_path": str(extras_path),
        "news_folder_created": created,
        "sector": sec,
        "sector_recorded": sector_recorded,
        "symbol_sectors_path": str(sectors_path),
        "reason": reason,
        "agent": agent,
    })


def execute_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
) -> dict[str, Any]:
    """Run a strategy's strategy.py evaluate() function and submit its intents
    through SafetyGate. Returns a summary of what got submitted, rejected,
    or errored.

    This is the *only* sanctioned path for placing trades in the harness.
    The agent picks WHICH strategy is active; the strategy script decides
    what to trade.
    """
    from quant_trading_system import strategy_runtime

    return strategy_runtime.run_strategy(
        strategy_id,
        settings=ctx.settings,
        market_data=ctx.market_data,
        regime_classifier=ctx.regime_classifier,
        safety_gate=ctx.safety_gate,
        alpaca_client=ctx.alpaca_client,
        run_id=ctx.run_id,
    )


def execute_active_strategy(
    ctx: ToolContext,
    *,
    allow_unclaimed: bool = False,
) -> dict[str, Any]:
    """Run every strategy in the active set against its claimed symbols.

    Reads ``state/active_strategies.md`` (plural, multi-strategy) and
    runs each entry against its declared symbols. Each strategy sees only
    its slice of the universe via ``ctx.watchlist``.

    Falls back to the legacy singular ``state/active_strategy.md`` if the
    plural file is missing — that strategy runs against its full
    frontmatter-filtered universe, exactly like before the refactor.
    Backwards compatible with every prior session.

    Returns a multi-strategy summary including a ``unclaimed_symbols``
    list (library-gap diagnostic) — symbols the harness is tracking but
    no active strategy claims.

    **P0 unclaimed-gate (operator directive 2026-06-04).** By default,
    this function REFUSES to execute if any universe symbol is unclaimed.
    Operator policy: every symbol in the universe MUST be claimed by an
    active strategy before any execute run. To override (e.g., a one-off
    diagnostic), pass ``allow_unclaimed=True``. The CLI flag is
    ``--allow-unclaimed``. The previous "log it as a library gap and
    proceed" behaviour was explicitly deprecated by the operator after
    multiple sessions silently ignored unclaimed symbols.
    """
    from quant_trading_system import strategy_runtime
    from quant_trading_system.universe import compute_universe

    if not allow_unclaimed:
        try:
            universe = compute_universe(ctx.settings, alpaca_client=ctx.alpaca_client)
            gaps = memory.unclaimed_symbols(universe.symbols)
        except Exception as e:
            return _err(
                f"unclaimed-gate precheck failed: could not compute universe ({e}). "
                "Refusing to execute. Either fix the universe error or rerun with --allow-unclaimed."
            )
        # Subtract symbols that have been triaged and flagged as
        # true_library_gap (no library strategy clears baseline Sharpe).
        # Those are *tolerated* unclaimed — Saturday research owns them.
        # Symbols not yet triaged remain hard blockers; the trader must
        # run `cli triage-symbol <SYM>` for each before execute.
        flagged = set(memory.library_gap_symbols())
        blocking = [g for g in gaps if g.upper() not in flagged]
        if blocking:
            return _err(
                "UNCLAIMED_SYMBOLS_VIOLATION: refusing to execute. "
                f"{len(blocking)} symbol(s) in the universe have no active "
                f"strategy claim AND have not been triaged: {', '.join(blocking)}. "
                "Operator policy: every universe symbol must be either "
                "(a) claimed by an active strategy, or (b) algorithmically "
                "triaged via `cli triage-symbol <SYM> [--gap-type ...]` "
                "and flagged as a true library gap. Run triage-symbol for "
                "each blocking symbol; the harness will either auto-claim "
                "it (Sharpe ≥ 0.5 on a library candidate) or write a "
                "library-gap marker that lets execute proceed. "
                "Escape hatch (NOT for daily runs): rerun with `--allow-unclaimed`."
            )

    return _ok(strategy_runtime.run_active_strategies(
        settings=ctx.settings,
        market_data=ctx.market_data,
        regime_classifier=ctx.regime_classifier,
        safety_gate=ctx.safety_gate,
        alpaca_client=ctx.alpaca_client,
        run_id=ctx.run_id,
    ))


def list_active_strategies(ctx: ToolContext) -> dict[str, Any]:
    """List every strategy in ``state/active_strategies.md`` with its
    symbol claims, plus the library-gap diagnostic (symbols in the
    universe that no active strategy owns).
    """
    from quant_trading_system.universe import compute_universe

    claims = memory.read_active_strategies()
    try:
        universe = compute_universe(ctx.settings, alpaca_client=ctx.alpaca_client)
        universe_syms = list(universe.symbols)
    except Exception as e:
        universe_syms = []
        ctx_universe_error = str(e)
    else:
        ctx_universe_error = ""
    gaps = memory.unclaimed_symbols(universe_syms) if universe_syms else []
    provisional = memory.read_provisional_claims()
    return _ok({
        "active_strategies": [c.to_dict() for c in claims],
        "active_count": len(claims),
        "universe_size": len(universe_syms),
        "claimed_count": sum(len(c.symbols) for c in claims),
        "unclaimed_symbols": gaps,
        "unclaimed_count": len(gaps),
        # Option 3: claims that are attached for coverage but quarantined
        # from execution until research validates them.
        "provisional_claims": [p.to_dict() for p in provisional],
        "provisional_count": len(provisional),
        "universe_error": ctx_universe_error or None,
    })


def add_active_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbols: list[str],
    reason: str,
    replace: bool = False,
) -> dict[str, Any]:
    """Add a strategy to the active set (default: UNION new symbols with
    existing claim).

    Behaviour (2026-06-10): default is UNION. Pass ``replace=True`` to
    overwrite the whole symbol list (CLI flag: ``--replace``). The
    no-conflict rule is enforced regardless: every symbol can be claimed
    by at most one active strategy. If any of ``symbols`` is already
    claimed by another strategy, returns an error with the conflicting
    symbol(s) listed. Resolve via head-to-head backtest
    (cli head-to-head), not by manually overriding the claim.

    The triage / instantiate paths compute the union themselves and
    pass ``replace=False`` here, so calling add_active_strategy twice
    on the same symbol is a no-op (idempotent).
    """
    syms_upper = [s.strip().upper() for s in symbols if s.strip()]
    if not reason or not reason.strip():
        return _err("--reason is required: every claim must trace to a justification")
    try:
        claim = memory.add_active_strategy(
            strategy_id, symbols=syms_upper, reason=reason.strip(),
            replace=replace,
        )
    except ValueError as e:
        return _err(str(e))
    return _ok({"added": claim.to_dict(), "mode": "replace" if replace else "union"})


def remove_active_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    reason: str = "",
) -> dict[str, Any]:
    """Drop a strategy from the active set. Use when a strategy is
    archived, or when its symbol claims have been reassigned to another
    strategy after a head-to-head backtest.
    """
    removed = memory.remove_active_strategy(strategy_id, reason=reason)
    if not removed:
        return _err(f"strategy {strategy_id!r} was not in the active set")
    return _ok({"removed": strategy_id, "reason": reason})


def head_to_head_backtest(
    ctx: ToolContext,
    *,
    strategy_a: str,
    strategy_b: str,
    symbol: str,
    start: str,
    end: str,
) -> dict[str, Any]:
    """Run both strategies on the same symbol over the same window and
    report which had higher Sharpe + lower max drawdown.

    This is the canonical mechanism for resolving symbol-claim conflicts:
    if two strategies want AAPL, the one with the better risk-adjusted
    return on AAPL's history wins. The trader does NOT pick by feel; the
    research agent runs this and writes the result into
    ``active_strategies.md``.

    Light wrapper around ``run_backtest`` — runs it twice and compares
    the headline metrics. Falls back gracefully if the backtester isn't
    available or one strategy fails.
    """
    try:
        from quant_trading_system.strategy_backtest import run_backtest
    except Exception as e:
        return _err(f"backtester not available: {e}")

    results = {}
    for sid in (strategy_a, strategy_b):
        sf = memory.read_strategy(sid)
        if sf is None:
            return _err(f"strategy not found: {sid}")
        try:
            r_obj = run_backtest(
                strategy_id=sid,
                symbol=symbol,
                start=start,
                end=end,
                market_data=ctx.market_data,
                regime_classifier=ctx.regime_classifier,
            )
        except Exception as e:
            return _err(f"{sid} backtest failed on {symbol}: {e}")
        r = r_obj.to_dict() if hasattr(r_obj, "to_dict") else r_obj
        if r.get("error"):
            return _err(f"{sid} backtest failed on {symbol}: {r['error']}")
        results[sid] = {
            "sharpe": float(r.get("sharpe", 0.0) or 0.0),
            "max_drawdown": float(r.get("max_drawdown", 0.0) or 0.0),
            "total_return": float(r.get("total_return", 0.0) or 0.0),
            "trades": int(r.get("num_trades", 0) or 0),
        }

    a, b = results[strategy_a], results[strategy_b]
    # Winner: higher sharpe, tiebreak on smaller (less negative) max DD.
    if a["sharpe"] != b["sharpe"]:
        winner = strategy_a if a["sharpe"] > b["sharpe"] else strategy_b
    else:
        winner = strategy_a if a["max_drawdown"] > b["max_drawdown"] else strategy_b
    return _ok({
        "symbol": symbol.upper(),
        "window": {"start": start, "end": end},
        "a": {"strategy_id": strategy_a, **a},
        "b": {"strategy_id": strategy_b, **b},
        "winner": winner,
        "decision_basis": "higher Sharpe; tiebreak on smaller max drawdown",
    })


def triage_symbol(
    ctx: ToolContext,
    *,
    symbol: str,
    gap_type: str | None = None,
    start: str | None = None,
    end: str | None = None,
    baseline_sharpe: float = 0.5,
    auto_claim: bool = True,
    provisional: bool = True,
) -> dict[str, Any]:
    """Find the best library strategy for ``symbol`` and (optionally)
    claim it via ``add_active_strategy``.

    **Mandatory-attach doctrine (Option 3, operator directive 2026-06-16).**
    When ``provisional`` is True (the default), triage NEVER leaves a symbol
    strategy-less. If no candidate clears ``baseline_sharpe`` (or there is no
    rankable backtest at all — e.g. a brand-new IPO with no price history),
    it attaches the best-available strategy as a PROVISIONAL (unvalidated)
    claim: the symbol is added to active_strategies (coverage = 100%) AND
    recorded in ``state/provisional_claims.md`` with a ``revalidate_by``
    deadline. Provisional claims are QUARANTINED FROM EXECUTION
    (run_active_strategies skips them) until Saturday research re-triages and
    either promotes (clears baseline) or escalates them. Pass
    ``provisional=False`` to restore the legacy ``true_library_gap`` verdict
    (diagnostic / research use).

    This is the trader's pre-execute mechanism for handling unclaimed
    symbols. It is purely algorithmic:

      1. Build a candidate list. If ``gap_type`` is given, candidates =
         ``find_strategies_for_gap(gap_type)``. Else candidates = every
         active or testing equity strategy.
      2. Backtest each candidate on ``symbol`` over the given window
         (default: last 2 calendar years).
      3. Rank by Sharpe (tiebreak: smaller max DD).
      4. If the top candidate's Sharpe ≥ ``baseline_sharpe``, claim the
         symbol with that strategy (replacing the strategy's existing
         claims by union with the new symbol). Returns ``verdict:
         claimed``.
      5. Else returns ``verdict: true_library_gap`` — no library
         strategy beats baseline on this symbol. Trader logs the gap;
         Saturday research builds (or activates) a strategy that handles
         the gap_type the news brief tagged.

    No judgment, no character-match. Sharpe decides. If Sharpe is tied
    or every strategy errors, the verdict is true_library_gap.
    """
    import datetime as _dt
    from quant_trading_system.templates import find_strategies_for_gap
    from quant_trading_system.strategy_backtest import run_backtest as _bt

    sym = (symbol or "").strip().upper()
    if not sym:
        return _err("symbol required")

    # Default window: last 2 calendar years
    if not end:
        end = _dt.date.today().isoformat()
    if not start:
        end_d = _dt.date.fromisoformat(end)
        start = end_d.replace(year=end_d.year - 2).isoformat()

    def _provisional_attach(strategy_id, sharpe, why, scores_payload, candidates_payload):
        """Mandatory-attach fallback (Option 3): attach best-available
        strategy as a provisional, execution-gated claim instead of leaving
        a true_library_gap. The symbol becomes claimed (coverage) but is
        quarantined from execution until research validates it."""
        current = memory.read_active_strategies()
        existing = next(
            (set(c.symbols) for c in current if c.strategy_id == strategy_id),
            set(),
        )
        union_syms = sorted(existing | {sym})
        reason = (
            f"PROVISIONAL/UNVALIDATED triage {_dt.date.today().isoformat()}: {why} "
            f"Attached best-available {strategy_id} for coverage; QUARANTINED from "
            f"execution until Saturday research validates (clears baseline "
            f"{baseline_sharpe:.2f}) or escalates."
        )
        try:
            memory.add_active_strategy(strategy_id, symbols=union_syms, reason=reason)
        except ValueError as e:
            return _err(
                f"provisional triage selected {strategy_id} but add_active failed: {e}. "
                f"Symbol {sym} may already be claimed — resolve via cli head-to-head."
            )
        pc = memory.append_provisional_claim(
            sym, strategy_id=strategy_id, gap_type=gap_type or "unknown",
            reason=why, sharpe=sharpe, baseline_sharpe=baseline_sharpe,
        )
        # A provisional attach supersedes any prior library-gap marker.
        try:
            memory.clear_library_gap(sym)
        except Exception:
            pass
        return _ok({
            "symbol": sym,
            "gap_type": gap_type,
            "verdict": "provisional_claim",
            "reason": reason,
            "provisional": pc.to_dict(),
            "winner": {"strategy_id": strategy_id, "sharpe": sharpe},
            "candidates": candidates_payload,
            "scores": scores_payload,
            "claimed": True,
            "execution_quarantined": True,
        })

    # Build candidate list.
    if gap_type:
        candidates = find_strategies_for_gap(gap_type)
        if not candidates:
            reason_text = (
                f"no library strategy declares gap_types containing "
                f"{gap_type!r}. Saturday research must add or "
                "activate a template that handles this gap_type."
            )
            if provisional and auto_claim:
                return _provisional_attach(
                    memory.DEFAULT_FALLBACK_STRATEGY, None, reason_text, [], [],
                )
            try:
                memory.append_library_gap(
                    sym, gap_type=gap_type, reason=reason_text,
                    baseline_sharpe=baseline_sharpe,
                )
            except Exception:
                pass
            return _ok({
                "symbol": sym,
                "gap_type": gap_type,
                "verdict": "true_library_gap",
                "reason": reason_text,
                "candidates": [],
                "winner": None,
                "scores": [],
                "claimed": False,
                "library_gap_flagged": True,
            })
    else:
        candidates = []
        for sf in memory.list_strategies():
            if (sf.frontmatter or {}).get("status") == "archived":
                continue
            if sf.type != "equity":
                continue
            # Skip passive fallback strategies (e.g. equity_watch_only). They
            # never trade, so they are the mandatory-attach fallback, never a
            # ranked competitor against real trading strategies.
            if (sf.frontmatter or {}).get("role") == "watch":
                continue
            candidates.append(sf.id)
        if not candidates:
            return _err("no equity strategies available to triage")

    # Score every candidate.
    scores: list[dict[str, Any]] = []
    for sid in sorted(candidates):
        try:
            r_obj = _bt(
                strategy_id=sid,
                symbol=sym,
                start=start,
                end=end,
                market_data=ctx.market_data,
                regime_classifier=ctx.regime_classifier,
            )
        except Exception as e:
            scores.append({"strategy_id": sid, "error": f"backtest raised: {e}"})
            continue
        r = r_obj.to_dict() if hasattr(r_obj, "to_dict") else r_obj
        if r.get("error"):
            scores.append({"strategy_id": sid, "error": r["error"]})
            continue
        scores.append({
            "strategy_id": sid,
            "sharpe": float(r.get("sharpe", 0.0) or 0.0),
            "max_drawdown": float(r.get("max_drawdown", 0.0) or 0.0),
            "total_return": float(r.get("total_return", 0.0) or 0.0),
            "trades": int(r.get("num_trades", 0) or 0),
        })

    # Pick the winner from scoreable rows.
    rankable = [s for s in scores if "sharpe" in s]
    if not rankable:
        reason_text = (
            "every candidate backtest errored / no price history — cannot rank"
        )
        if provisional and auto_claim:
            return _provisional_attach(
                memory.DEFAULT_FALLBACK_STRATEGY, None, reason_text, scores, list(candidates),
            )
        try:
            memory.append_library_gap(
                sym, gap_type=gap_type or "unknown",
                reason=reason_text, baseline_sharpe=baseline_sharpe,
            )
        except Exception:
            pass
        return _ok({
            "symbol": sym,
            "gap_type": gap_type,
            "window": {"start": start, "end": end},
            "verdict": "true_library_gap",
            "reason": reason_text,
            "candidates": list(candidates),
            "winner": None,
            "scores": scores,
            "claimed": False,
            "library_gap_flagged": True,
        })
    # Sort by Sharpe desc, tiebreak by smaller |max DD|.
    rankable.sort(key=lambda s: (-s["sharpe"], s["max_drawdown"]))
    top = rankable[0]

    if top["sharpe"] < baseline_sharpe:
        reason_text = (
            f"top candidate {top['strategy_id']!r} has Sharpe "
            f"{top['sharpe']:.3f} < baseline {baseline_sharpe:.3f}. "
            "No library strategy is good enough on this symbol — "
            "log for Saturday research to build a new template."
        )
        if provisional and auto_claim:
            return _provisional_attach(
                top["strategy_id"], top["sharpe"], reason_text, rankable, list(candidates),
            )
        try:
            memory.append_library_gap(
                sym, gap_type=gap_type or "unknown",
                reason=reason_text,
                top_strategy=top["strategy_id"],
                top_sharpe=top["sharpe"],
                baseline_sharpe=baseline_sharpe,
            )
        except Exception:
            pass
        return _ok({
            "symbol": sym,
            "gap_type": gap_type,
            "window": {"start": start, "end": end},
            "verdict": "true_library_gap",
            "reason": reason_text,
            "candidates": list(candidates),
            "winner_below_baseline": top,
            "scores": rankable,
            "claimed": False,
            "library_gap_flagged": True,
        })

    if not auto_claim:
        return _ok({
            "symbol": sym,
            "gap_type": gap_type,
            "window": {"start": start, "end": end},
            "verdict": "winner_found",
            "winner": top,
            "scores": rankable,
            "claimed": False,
        })

    # Claim. Union with existing symbol claims for the winner.
    winner_id = top["strategy_id"]
    current = memory.read_active_strategies()
    existing_syms = next(
        (set(c.symbols) for c in current if c.strategy_id == winner_id),
        set(),
    )
    union_syms = sorted(existing_syms | {sym})
    reason = (
        f"triage-symbol {_dt.date.today().isoformat()}: "
        f"{winner_id} beat {len(rankable)-1} other candidate(s) on {sym} "
        f"with Sharpe {top['sharpe']:.3f} (vs baseline {baseline_sharpe:.2f})"
    )
    try:
        memory.add_active_strategy(winner_id, symbols=union_syms, reason=reason)
    except ValueError as e:
        return _err(
            f"triage selected {winner_id} but add_active failed: {e}. "
            "This usually means another strategy already claims this "
            "symbol — re-run with --no-claim to see scores, then resolve "
            "via cli head-to-head."
        )
    # If this symbol was previously flagged as a library gap, clear it.
    cleared_gap = False
    try:
        cleared_gap = memory.clear_library_gap(sym)
    except Exception:
        pass
    return _ok({
        "symbol": sym,
        "gap_type": gap_type,
        "window": {"start": start, "end": end},
        "verdict": "claimed",
        "winner": top,
        "scores": rankable,
        "claimed": True,
        "claim_reason": reason,
        "cleared_prior_library_gap": cleared_gap,
    })


def instantiate_template(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbol: str,
    start: str | None = None,
    end: str | None = None,
    reason: str,
    sharpe_floor: float = 0.5,
    max_dd_floor: float = -0.30,
) -> dict[str, Any]:
    """Run a stricter addition test for ``strategy_id`` on ``symbol``,
    then claim if the strategy clears the floors.

    The "instantiation" of a template against a new symbol is just:
    backtest the template's rules on the symbol, check the result clears
    a defensible Sharpe + max-DD floor, then claim. The trader uses this
    when the news brief surfaces a candidate with a known gap_type that
    has at most one template responder (so triage-symbol's ranking is
    degenerate); the research agent uses it to formalize claims for
    symbols where a single template is the obvious match.

    Returns claim metadata on pass, or the failing metrics + reason on
    reject.
    """
    import datetime as _dt
    from quant_trading_system.strategy_backtest import run_backtest as _bt

    sym = (symbol or "").strip().upper()
    if not sym:
        return _err("symbol required")
    if not reason or not reason.strip():
        return _err("--reason required: every claim must trace to a justification")

    if not end:
        end = _dt.date.today().isoformat()
    if not start:
        end_d = _dt.date.fromisoformat(end)
        start = end_d.replace(year=end_d.year - 2).isoformat()

    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return _err(f"strategy not found: {strategy_id}")

    try:
        r_obj = _bt(
            strategy_id=strategy_id,
            symbol=sym,
            start=start,
            end=end,
            market_data=ctx.market_data,
            regime_classifier=ctx.regime_classifier,
        )
    except Exception as e:
        return _err(f"backtest raised: {e}")
    r = r_obj.to_dict() if hasattr(r_obj, "to_dict") else r_obj
    if r.get("error"):
        return _err(f"backtest error: {r['error']}")

    sharpe = float(r.get("sharpe", 0.0) or 0.0)
    max_dd = float(r.get("max_drawdown", 0.0) or 0.0)
    failures: list[str] = []
    if sharpe < sharpe_floor:
        failures.append(f"Sharpe {sharpe:.3f} < floor {sharpe_floor:.2f}")
    if max_dd < max_dd_floor:
        failures.append(f"max_drawdown {max_dd:.3f} < floor {max_dd_floor:.2f}")

    if failures:
        return _ok({
            "symbol": sym,
            "strategy_id": strategy_id,
            "window": {"start": start, "end": end},
            "verdict": "rejected",
            "metrics": {
                "sharpe": sharpe, "max_drawdown": max_dd,
                "total_return": float(r.get("total_return", 0.0) or 0.0),
                "trades": int(r.get("num_trades", 0) or 0),
            },
            "failures": failures,
            "claimed": False,
        })

    # Pass — claim by union with existing symbols.
    current = memory.read_active_strategies()
    existing_syms = next(
        (set(c.symbols) for c in current if c.strategy_id == strategy_id),
        set(),
    )
    union_syms = sorted(existing_syms | {sym})
    full_reason = (
        f"instantiate-template {_dt.date.today().isoformat()}: {reason.strip()} "
        f"(Sharpe {sharpe:.3f}, max DD {max_dd:.3f} on [{start}, {end}])"
    )
    try:
        memory.add_active_strategy(strategy_id, symbols=union_syms, reason=full_reason)
    except ValueError as e:
        return _err(f"add_active failed: {e}")
    cleared_gap = False
    try:
        cleared_gap = memory.clear_library_gap(sym)
    except Exception:
        pass
    return _ok({
        "symbol": sym,
        "strategy_id": strategy_id,
        "window": {"start": start, "end": end},
        "verdict": "instantiated",
        "metrics": {
            "sharpe": sharpe, "max_drawdown": max_dd,
            "total_return": float(r.get("total_return", 0.0) or 0.0),
            "trades": int(r.get("num_trades", 0) or 0),
        },
        "claimed": True,
        "claim_reason": full_reason,
        "cleared_prior_library_gap": cleared_gap,
    })


def list_gap_registry(ctx: ToolContext) -> dict[str, Any]:
    """Show the gap_type → strategy_ids map. Coverage holes (gap_types
    with no responder) are the canonical list of "true" library gaps
    pending Saturday research.
    """
    from quant_trading_system.templates import (
        CANONICAL_GAP_TYPES, inverted_registry,
    )
    reg = inverted_registry()
    coverage_holes = sorted([gt for gt, ids in reg.items() if not ids])
    return _ok({
        "canonical_gap_types": list(CANONICAL_GAP_TYPES),
        "registry": reg,
        "coverage_holes": coverage_holes,
    })


def update_strategy_script(
    ctx: ToolContext, *, strategy_id: str, py_source: str
) -> dict[str, Any]:
    """Replace a strategy's strategy.py contents.

    Use this when a strategy's execution logic genuinely needs to change.
    Parameter-only tweaks should go through `update_strategy` (which edits
    the .md frontmatter) instead — keep prose and code in sync.
    """
    try:
        sf = memory.update_strategy_script(strategy_id, py_source)
    except FileNotFoundError as e:
        return _err(str(e))
    return _ok({"id": sf.id, "py_path": str(sf.py_path), "bytes": len(py_source)})


def log_trade_closed(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbol: str,
    pnl: float,
    pnl_pct: float | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """Record that a position closed. The agent calls this when reconciling
    yesterday's open positions against today's portfolio."""
    journal.log_event({
        "type": "trade_closed",
        "run_id": ctx.run_id,
        "strategy_id": strategy_id,
        "symbol": symbol.upper(),
        "pnl": float(pnl),
        "pnl_pct": float(pnl_pct) if pnl_pct is not None else None,
        "notes": notes,
    })
    return _ok({"logged": True})


# ---------------------------------------------------------------------------
# Backtest (stub — real backtester wiring is a follow-up)
# ---------------------------------------------------------------------------


def run_backtest(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbol: str,
    start: str,
    end: str,
) -> dict[str, Any]:
    """Run a backtest of a strategy on a symbol over a date range.

    NOTE: this currently routes to the existing equity backtester. The
    agent-facing surface is intentionally narrow; richer backtest options
    can be added once the harness is stable.
    """
    try:
        from quant_trading_system.backtesting.equity_backtester import (
            EquityBacktester,
        )
    except Exception as e:
        return _err(f"backtester not available: {e}")

    sf = memory.read_strategy(strategy_id)
    if sf is None:
        return _err(f"strategy not found: {strategy_id}")

    try:
        df = ctx.market_data.get_bars(symbol, "1Day", start=start, end=end)
        if df.empty:
            return _err("no market data for backtest", symbol=symbol)
        backtester = EquityBacktester()
        result = backtester.run(df, sf.frontmatter, strategy_id=strategy_id)
        # Whatever the backtester returns, normalize to a dict
        if hasattr(result, "model_dump"):
            result = result.model_dump()
        elif hasattr(result, "__dict__"):
            result = {k: v for k, v in vars(result).items() if not k.startswith("_")}
    except Exception as e:
        return _err(f"backtest failed: {e}")

    # Strip non-serializable bits
    safe = {}
    for k, v in result.items():
        try:
            import json

            json.dumps(v, default=str)
            safe[k] = v
        except Exception:
            safe[k] = str(v)
    return _ok({"strategy_id": strategy_id, "symbol": symbol, "result": safe})


# ---------------------------------------------------------------------------
# Tool dispatch table — used by the tool registry and the orchestrator
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS = {
    # strategy I/O
    "list_strategies": list_strategies,
    "read_strategy": read_strategy,
    "update_strategy": update_strategy,
    "create_strategy": create_strategy,
    "archive_strategy": archive_strategy,
    # conclusions / state
    "write_conclusion": write_conclusion,
    "append_conclusion": append_conclusion,
    "read_recent_conclusions": read_recent_conclusions,
    "read_handoff": read_handoff,
    "write_handoff": write_handoff,
    "get_active_strategy": get_active_strategy,
    "set_active_strategy": set_active_strategy,
    "read_summary": read_summary,
    "update_summary": update_summary,
    # market
    "get_bars": get_bars,
    "classify_regime": classify_regime,
    "compute_indicator": compute_indicator,
    "get_quote": get_quote,
    "market_status": market_status,
    # portfolio
    "get_account": get_account,
    "get_positions": get_positions,
    "get_open_orders": get_open_orders,
    "get_recent_trades": get_recent_trades,
    "get_strategy_health": get_strategy_health,
    "get_portfolio_health": get_portfolio_health,
    # sizing
    "kelly_position_size": kelly_position_size,
    # trading
    "submit_order": submit_order,
    "cancel_order": cancel_order,
    "log_trade_closed": log_trade_closed,
    # strategy execution
    "execute_strategy": execute_strategy,
    "execute_active_strategy": execute_active_strategy,
    "update_strategy_script": update_strategy_script,
    # research / library curation
    "propose_strategy": propose_strategy,
    "simulate_strategy": simulate_strategy,
    "evaluate_addition": evaluate_addition,
    "evaluate_replacement": evaluate_replacement,
    "evaluate_archive": evaluate_archive,
    # news layer
    "news_fetch": news_fetch,
    "news_cleanup": news_cleanup,
    "news_universe": news_universe,
    # universe (derived)
    "universe_view": universe_view,
    # git
    "git_sync": git_sync,
    "git_doctor": git_doctor,
    # backtest
    "run_backtest": run_backtest,
}
