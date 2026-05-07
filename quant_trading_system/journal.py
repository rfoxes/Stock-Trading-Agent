"""Append-only trade journal.

Every order that the harness submits goes through SafetyGate, and every
submitted (or rejected) order is logged here as one JSONL line. The journal is
how the agent attributes outcomes to strategies later: when next morning's run
asks "how did `mean_reversion_bollinger` do over the last 30 days?", the
deterministic health module reads from here.

Files are bucketed by month (`trades/YYYY-MM.jsonl`) so individual files stay
human-grep-able. Entries are never edited in place.
"""

from __future__ import annotations

import datetime as dt
import json
import uuid
from pathlib import Path
from typing import Any, Iterable

from quant_trading_system.memory import TRADES_DIR, _ensure_dirs


def _journal_path_for(when: dt.datetime | None = None) -> Path:
    when = when or dt.datetime.now()
    return TRADES_DIR / f"{when.strftime('%Y-%m')}.jsonl"


def log_event(event: dict[str, Any]) -> None:
    """Append one event dict to the current month's journal.

    Caller is responsible for putting reasonable fields in. Standard fields:
        type           — "order_submitted" | "order_rejected" | "trade_closed" | …
        timestamp      — ISO8601 string (auto-filled if missing)
        event_id       — uuid (auto-filled if missing)
        strategy_id    — which strategy authored this event
        run_id         — id of the harness run that wrote it
        ...            — anything else the caller wants to record
    """
    _ensure_dirs()
    e = dict(event)
    e.setdefault("event_id", uuid.uuid4().hex[:12])
    e.setdefault("timestamp", dt.datetime.now().isoformat(timespec="seconds"))
    path = _journal_path_for()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(e, default=str) + "\n")


def log_order(
    *,
    strategy_id: str,
    run_id: str,
    order_request: dict[str, Any],
    order_result: dict[str, Any],
) -> None:
    """Convenience wrapper for logging an order submission outcome."""
    status = order_result.get("status", "unknown")
    log_event({
        "type": "order_submitted" if status not in ("rejected",) else "order_rejected",
        "strategy_id": strategy_id,
        "run_id": run_id,
        "symbol": order_request.get("symbol"),
        "side": order_request.get("side"),
        "qty": order_request.get("qty"),
        "order_type": order_request.get("order_type"),
        "limit_price": order_request.get("limit_price"),
        "stop_price": order_request.get("stop_price"),
        "time_in_force": order_request.get("time_in_force"),
        "reasoning": order_request.get("reasoning", "")[:500],
        "result_status": status,
        "result_mode": order_result.get("mode"),
        "result_order_id": order_result.get("order_id"),
        "result_filled_qty": order_result.get("filled_qty"),
        "result_filled_avg_price": order_result.get("filled_avg_price"),
        "result_rejection_reason": order_result.get("rejection_reason", ""),
        "result_safety_checks_passed": order_result.get("safety_checks_passed", []),
        "result_safety_checks_failed": order_result.get("safety_checks_failed", []),
    })


def read_events(
    days: int = 30,
    strategy_id: str | None = None,
    types: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Return all journal events within the lookback window, oldest first.

    Reads only the months that overlap the window for efficiency.
    """
    _ensure_dirs()
    cutoff = dt.datetime.now() - dt.timedelta(days=days)
    types_set = set(types) if types else None

    # Walk back month-by-month from now until we're past the cutoff.
    months_to_read: list[Path] = []
    m = dt.date.today().replace(day=1)
    while True:
        p = TRADES_DIR / f"{m.strftime('%Y-%m')}.jsonl"
        if p.exists():
            months_to_read.append(p)
        # Stop once this month is fully before the cutoff.
        next_first = (m.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        if dt.datetime.combine(next_first, dt.time.min) < cutoff:
            break
        # Step back one month
        prev_last = m - dt.timedelta(days=1)
        m = prev_last.replace(day=1)
        # Guard: don't walk back forever
        if m.year < 2000:
            break

    out: list[dict[str, Any]] = []
    for p in sorted(months_to_read):
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = e.get("timestamp")
                try:
                    ts_dt = dt.datetime.fromisoformat(ts) if ts else None
                except ValueError:
                    ts_dt = None
                if ts_dt is None or ts_dt < cutoff:
                    continue
                if strategy_id is not None and e.get("strategy_id") != strategy_id:
                    continue
                if types_set is not None and e.get("type") not in types_set:
                    continue
                out.append(e)
    out.sort(key=lambda e: e.get("timestamp", ""))
    return out
