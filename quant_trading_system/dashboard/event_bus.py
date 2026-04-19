"""Server-Sent Events (SSE) event bus for real-time dashboard updates."""

from __future__ import annotations

import asyncio
import json
import time
from collections import deque
from typing import Any


class EventBus:
    """In-memory event bus that supports SSE streaming to the dashboard.

    Events are published by the trading pipeline and consumed by the
    dashboard via Server-Sent Events.
    """

    def __init__(self, max_history: int = 500) -> None:
        self._subscribers: list[asyncio.Queue] = []
        self._history: deque[dict] = deque(maxlen=max_history)
        self._orders: list[dict] = []
        self._regime: dict = {}
        self._portfolio: dict = {}
        self._risk: dict = {}
        self._system_status: str = "idle"
        self._cycle_count: int = 0
        self._backtest_results: list[dict] = []

    def publish(self, event_type: str, data: Any) -> None:
        """Publish an event to all subscribers."""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": time.time(),
        }
        self._history.append(event)

        # Update cached state
        if event_type == "order":
            self._orders.append(data)
        elif event_type == "regime":
            self._regime = data
        elif event_type == "portfolio":
            self._portfolio = data
        elif event_type == "risk":
            self._risk = data
        elif event_type == "status":
            self._system_status = data.get("status", "idle")
        elif event_type == "cycle":
            self._cycle_count = data.get("cycle_count", 0)
        elif event_type == "backtest":
            self._backtest_results.append(data)

        # Push to all subscribers
        for queue in self._subscribers:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                pass  # Drop event if subscriber is slow

    async def subscribe(self):
        """Subscribe to events. Yields SSE-formatted strings."""
        queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        self._subscribers.append(queue)
        try:
            while True:
                event = await queue.get()
                yield self._format_sse(event)
        finally:
            self._subscribers.remove(queue)

    def _format_sse(self, event: dict) -> str:
        """Format an event as an SSE message."""
        data = json.dumps(event["data"], default=str)
        return f"event: {event['type']}\ndata: {data}\n\n"

    @property
    def orders(self) -> list[dict]:
        return list(self._orders)

    @property
    def regime(self) -> dict:
        return self._regime

    @property
    def portfolio(self) -> dict:
        return self._portfolio

    @property
    def risk(self) -> dict:
        return self._risk

    @property
    def system_status(self) -> str:
        return self._system_status

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    @property
    def backtest_results(self) -> list[dict]:
        return list(self._backtest_results)

    @property
    def log_history(self) -> list[dict]:
        return [e for e in self._history if e["type"] == "log"]

    def clear(self) -> None:
        self._orders.clear()
        self._history.clear()


# Global singleton
event_bus = EventBus()
