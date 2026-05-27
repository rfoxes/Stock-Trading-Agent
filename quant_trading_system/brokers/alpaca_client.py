"""Thin Alpaca REST wrapper using `requests`.

Replaces the previous `alpaca-py` SDK dependency, which isn't available in
the Cowork Linux sandbox where the harness actually runs. Surface stays the
same: `get_account`, `get_positions`, `submit_order`, `get_order`,
`cancel_order`, `get_open_orders`. Return shapes are dicts (not SDK objects)
so callers can JSON-encode them directly.

This client should NEVER be called directly by the agent. All orders go
through SafetyGate.
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

import requests

if TYPE_CHECKING:
    from quant_trading_system.config import Settings

logger = logging.getLogger(__name__)

PAPER_BASE = "https://paper-api.alpaca.markets"
LIVE_BASE = "https://api.alpaca.markets"

DEFAULT_TIMEOUT = 15  # seconds


class AlpacaError(RuntimeError):
    """Raised on a non-2xx response or network error."""

    def __init__(self, status: int, body: str, *, url: str = "") -> None:
        super().__init__(f"alpaca {status}: {body[:300]}")
        self.status = status
        self.body = body
        self.url = url


class AlpacaClient:
    """REST-only client. Same surface as the old alpaca-py wrapper."""

    def __init__(self, settings: "Settings") -> None:
        self._settings = settings
        self._base = PAPER_BASE if settings.ALPACA_PAPER else LIVE_BASE
        self._session = requests.Session()
        self._session.headers.update({
            "APCA-API-KEY-ID": settings.ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": settings.ALPACA_SECRET_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        logger.info("alpaca_client_initialized paper=%s base=%s", settings.ALPACA_PAPER, self._base)

    # -- internal --------------------------------------------------------

    def _request(self, method: str, path: str, *, json_body: dict | None = None,
                 params: dict | None = None) -> Any:
        url = f"{self._base}{path}"
        try:
            resp = self._session.request(
                method=method,
                url=url,
                json=json_body,
                params=params,
                timeout=DEFAULT_TIMEOUT,
            )
        except requests.RequestException as e:
            raise AlpacaError(0, f"network: {e}", url=url) from e
        if resp.status_code >= 400:
            raise AlpacaError(resp.status_code, resp.text, url=url)
        # Some endpoints (DELETE) return empty body
        if not resp.content:
            return None
        try:
            return resp.json()
        except json.JSONDecodeError:
            return resp.text

    # -- account / positions --------------------------------------------

    def get_account(self) -> dict:
        a = self._request("GET", "/v2/account")
        return {
            "equity": float(a.get("equity", 0.0)),
            "buying_power": float(a.get("buying_power", 0.0)),
            "cash": float(a.get("cash", 0.0)),
            "portfolio_value": float(a.get("portfolio_value", a.get("equity", 0.0))),
            "day_trade_count": int(a.get("daytrade_count", 0)),
        }

    def get_positions(self) -> list[dict]:
        positions = self._request("GET", "/v2/positions") or []
        out = []
        for p in positions:
            out.append({
                "symbol": p.get("symbol", ""),
                "qty": float(p.get("qty", 0)),
                "side": p.get("side", "long"),
                "market_value": float(p.get("market_value") or 0.0),
                "unrealized_pl": float(p.get("unrealized_pl") or 0.0),
                "unrealized_plpc": float(p.get("unrealized_plpc") or 0.0),
                "current_price": float(p.get("current_price") or 0.0),
                "avg_entry_price": float(p.get("avg_entry_price") or 0.0),
            })
        return out

    # -- orders ----------------------------------------------------------

    def submit_order(self, body: dict) -> dict:
        """Submit an order. `body` is the raw Alpaca request payload (dict).

        The harness's SafetyGate is responsible for assembling the body from
        an OrderRequest. Returning the raw response lets SafetyGate read fields
        like `id`, `filled_qty`, etc. without depending on SDK objects.
        """
        logger.info(
            "alpaca_submit_order symbol=%s side=%s qty=%s type=%s tif=%s",
            body.get("symbol"),
            body.get("side"),
            body.get("qty"),
            body.get("type"),
            body.get("time_in_force"),
        )
        return self._request("POST", "/v2/orders", json_body=body)

    def get_order(self, order_id: str) -> dict:
        return self._request("GET", f"/v2/orders/{order_id}")

    def cancel_order(self, order_id: str) -> None:
        logger.info("alpaca_cancel_order order_id=%s", order_id)
        self._request("DELETE", f"/v2/orders/{order_id}")

    def get_open_orders(self) -> list[dict]:
        """Return all open orders. Shape mirrors the Alpaca order JSON."""
        orders = self._request("GET", "/v2/orders", params={"status": "open"}) or []
        return orders if isinstance(orders, list) else []

    # -- bars (used by MarketDataService too, but kept here for symmetry) -

    def get_bars(
        self,
        symbol: str,
        timeframe: str,
        start_iso: str,
        end_iso: str,
        limit: int = 1000,
    ) -> list[dict]:
        """Fetch historical bars from Alpaca's data API.

        Note: Alpaca uses a different host for market data (data.alpaca.markets),
        but the same auth headers. Returns the raw `bars` list from the response.
        """
        # Override base for data API
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/bars"
        params = {
            "timeframe": timeframe,
            "start": start_iso,
            "end": end_iso,
            "limit": limit,
            "adjustment": "raw",
        }
        try:
            resp = self._session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as e:
            raise AlpacaError(0, f"network: {e}", url=url) from e
        if resp.status_code >= 400:
            raise AlpacaError(resp.status_code, resp.text, url=url)
        data = resp.json() or {}
        return data.get("bars", []) or []

    def get_latest_quote(self, symbol: str) -> dict | None:
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest"
        try:
            resp = self._session.get(url, timeout=DEFAULT_TIMEOUT)
        except requests.RequestException as e:
            logger.warning("latest_quote_network_error symbol=%s err=%s", symbol, e)
            return None
        if resp.status_code >= 400:
            logger.warning("latest_quote_http_error symbol=%s status=%s", symbol, resp.status_code)
            return None
        data = resp.json() or {}
        q = data.get("quote") or {}
        if not q:
            return None
        bid = float(q.get("bp", 0.0))
        ask = float(q.get("ap", 0.0))
        return {
            "bid": bid,
            "ask": ask,
            "bid_size": int(q.get("bs", 0)),
            "ask_size": int(q.get("as", 0)),
            "mid": (bid + ask) / 2 if bid and ask else 0.0,
        }

    # -- options ---------------------------------------------------------

    def get_options_chain(
        self,
        underlying: str,
        *,
        expiration: str | None = None,
        feed: str = "indicative",
    ) -> list[dict]:
        """Fetch options chain snapshots for an underlying.

        Returns a list of snapshot dicts, each containing:
            symbol, latestQuote ({bid, ask, bidSize, askSize, ts}),
            greeks ({delta, gamma, theta, vega, rho}),
            impliedVolatility, openInterest, …

        Uses Alpaca's `/v1beta1/options/snapshots/{underlying}` endpoint.
        Auto-paginates up to a hard cap.
        """
        url = f"https://data.alpaca.markets/v1beta1/options/snapshots/{underlying.upper()}"
        params: dict[str, Any] = {"feed": feed, "limit": 100}
        if expiration:
            params["expiration_date"] = expiration
        out: list[dict] = []
        page_token: str | None = None
        pages = 0
        while True:
            p = dict(params)
            if page_token:
                p["page_token"] = page_token
            try:
                resp = self._session.get(url, params=p, timeout=DEFAULT_TIMEOUT)
            except requests.RequestException as e:
                logger.warning("alpaca_options_chain_request_failed sym=%s err=%s", underlying, e)
                return out
            if resp.status_code >= 400:
                logger.warning(
                    "alpaca_options_chain_http_error sym=%s status=%s body=%s",
                    underlying, resp.status_code, resp.text[:200],
                )
                return out
            data = resp.json() or {}
            snaps = data.get("snapshots") or {}
            # Alpaca returns snapshots as {option_symbol: {...}}
            for sym, snap in snaps.items():
                snap = dict(snap or {})
                snap["symbol"] = sym
                # Hoist greeks for easy access
                g = snap.get("greeks") or {}
                snap["greeks"] = {
                    "delta": float(g.get("delta", 0.0)) if g.get("delta") is not None else None,
                    "gamma": float(g.get("gamma", 0.0)) if g.get("gamma") is not None else None,
                    "theta": float(g.get("theta", 0.0)) if g.get("theta") is not None else None,
                    "vega": float(g.get("vega", 0.0)) if g.get("vega") is not None else None,
                    "rho": float(g.get("rho", 0.0)) if g.get("rho") is not None else None,
                }
                out.append(snap)
            page_token = data.get("next_page_token") or None
            pages += 1
            if not page_token or pages >= 20:
                break
        return out

    def submit_options_order(self, body: dict) -> dict:
        """Submit a multi-leg options order.

        `body` is the raw Alpaca request payload; SafetyGate assembles it
        with `order_class: "mleg"` and `legs: [{symbol, side, ratio_qty, position_intent}, ...]`.
        """
        logger.info(
            "alpaca_submit_options_order qty=%s order_class=%s n_legs=%s",
            body.get("qty"), body.get("order_class"), len(body.get("legs") or []),
        )
        return self._request("POST", "/v2/orders", json_body=body)
