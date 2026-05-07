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
    # backtest
    "run_backtest": run_backtest,
}
