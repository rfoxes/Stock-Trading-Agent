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
    """Fetch Alpaca News for the universe (watchlist + held positions) and
    write per-symbol + per-sector HTMLs under knowledge_base/news/.

    Returns a summary dict; the news agent uses this to know what got written.
    """
    from quant_trading_system import news_service

    universe = set(s.upper() for s in (symbols or ctx.settings.watchlist))
    if include_positions and ctx.alpaca_client is not None:
        try:
            for p in ctx.alpaca_client.get_positions():
                sym = str(p.get("symbol", "")).upper()
                if sym:
                    universe.add(sym)
        except Exception as e:
            logger.warning("news_fetch_position_lookup_failed err=%s", e)
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


def execute_active_strategy(ctx: ToolContext) -> dict[str, Any]:
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
    no active strategy claims. The trader writes those into tasks.md so
    the Saturday research agent can fill the gap.
    """
    from quant_trading_system import strategy_runtime

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
    return _ok({
        "active_strategies": [c.to_dict() for c in claims],
        "active_count": len(claims),
        "universe_size": len(universe_syms),
        "claimed_count": sum(len(c.symbols) for c in claims),
        "unclaimed_symbols": gaps,
        "unclaimed_count": len(gaps),
        "universe_error": ctx_universe_error or None,
    })


def add_active_strategy(
    ctx: ToolContext,
    *,
    strategy_id: str,
    symbols: list[str],
    reason: str,
) -> dict[str, Any]:
    """Add a strategy to the active set with an explicit symbol-claim list.

    Enforces the no-conflict rule: every symbol can be claimed by at most
    one active strategy. If any of ``symbols`` is already claimed by
    another strategy, returns an error with the conflicting symbol(s)
    listed. Resolve via head-to-head backtest (cli head-to-head), not by
    manually overriding the claim.
    """
    syms_upper = [s.strip().upper() for s in symbols if s.strip()]
    if not reason or not reason.strip():
        return _err("--reason is required: every claim must trace to a justification")
    try:
        claim = memory.add_active_strategy(
            strategy_id, symbols=syms_upper, reason=reason.strip(),
        )
    except ValueError as e:
        return _err(str(e))
    return _ok({"added": claim.to_dict()})


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
        from quant_trading_system.backtesting.equity_backtester import (
            EquityBacktester,
        )
    except Exception as e:
        return _err(f"backtester not available: {e}")

    results = {}
    for sid in (strategy_a, strategy_b):
        sf = memory.read_strategy(sid)
        if sf is None:
            return _err(f"strategy not found: {sid}")
        try:
            df = ctx.market_data.get_bars(symbol, "1Day", start=start, end=end)
        except Exception as e:
            return _err(f"data fetch failed for {symbol}: {e}")
        if df.empty:
            return _err(f"no bars for {symbol} in [{start}, {end}]")
        try:
            bt = EquityBacktester(strategy_frontmatter=sf.frontmatter or {})
            r = bt.run(df, symbol=symbol)
            results[sid] = {
                "sharpe": float(r.get("sharpe", 0.0)),
                "max_drawdown": float(r.get("max_drawdown", 0.0)),
                "total_return": float(r.get("total_return", 0.0)),
                "trades": int(r.get("trades", 0)),
            }
        except Exception as e:
            return _err(f"{sid} backtest failed on {symbol}: {e}")

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
