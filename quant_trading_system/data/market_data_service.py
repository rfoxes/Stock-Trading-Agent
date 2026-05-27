"""Market data via Alpaca's data REST API.

No alpaca-py, no yfinance. Just `requests` against
https://data.alpaca.markets. Uses the same key/secret as the trading API.

Returns pandas DataFrames with columns Open, High, Low, Close, Volume —
shape preserved for the existing regime classifier and indicators.
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import time
from typing import Optional

import pandas as pd
import requests

from quant_trading_system.config import Settings

logger = logging.getLogger(__name__)


_DATA_BASE = "https://data.alpaca.markets"
# Which Alpaca data feed to request. Default IEX so the free paper tier works;
# set ALPACA_DATA_FEED=sip in the environment if the account is upgraded.
_DATA_FEED = os.environ.get("ALPACA_DATA_FEED", "iex").strip() or "iex"
_TIMEFRAME_MAP = {
    "1Min": "1Min",
    "5Min": "5Min",
    "15Min": "15Min",
    "1Hour": "1Hour",
    "1Day": "1Day",
    "1Week": "1Week",
}

# Simple in-process TTL cache (per get_bars argument set)
_cache: dict[str, tuple[float, pd.DataFrame]] = {}
_CACHE_TTL_S = 60


def _cache_key(symbol: str, timeframe: str, start: str, end: str) -> str:
    return f"{symbol}:{timeframe}:{start}:{end}"


class MarketDataService:
    """Bars + latest-quote service."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._session = requests.Session()
        if settings.ALPACA_API_KEY and settings.ALPACA_SECRET_KEY:
            self._session.headers.update({
                "APCA-API-KEY-ID": settings.ALPACA_API_KEY,
                "APCA-API-SECRET-KEY": settings.ALPACA_SECRET_KEY,
                "Accept": "application/json",
            })
            logger.info("market_data_initialized")
        else:
            logger.warning("market_data_no_credentials")

    def get_bars(
        self,
        symbol: str,
        timeframe: str = "1Day",
        start: Optional[str] = None,
        end: Optional[str] = None,
        limit: int = 500,
    ) -> pd.DataFrame:
        if start is None:
            start = (dt.date.today() - dt.timedelta(days=365 * 2)).isoformat()
        if end is None:
            end = dt.date.today().isoformat()

        key = _cache_key(symbol, timeframe, start, end)
        if key in _cache:
            t, df = _cache[key]
            if time.time() - t < _CACHE_TTL_S:
                return df

        tf = _TIMEFRAME_MAP.get(timeframe, "1Day")
        url = f"{_DATA_BASE}/v2/stocks/{symbol}/bars"
        params = {
            "timeframe": tf,
            "start": start,
            "end": end,
            "limit": limit,
            "adjustment": "raw",
            "feed": _DATA_FEED,
        }
        try:
            resp = self._session.get(url, params=params, timeout=15)
        except requests.RequestException as e:
            logger.warning("alpaca_bars_request_failed symbol=%s err=%s", symbol, e)
            return _empty_bars()

        if resp.status_code >= 400:
            logger.warning(
                "alpaca_bars_http_error symbol=%s status=%s body=%s",
                symbol,
                resp.status_code,
                resp.text[:200],
            )
            return _empty_bars()

        data = resp.json() or {}
        bars = data.get("bars") or []
        if not bars:
            return _empty_bars()

        df = pd.DataFrame(bars)
        # Alpaca columns: t,o,h,l,c,v,n,vw
        rename = {"o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"}
        df = df.rename(columns=rename)
        if "t" in df.columns:
            df["t"] = pd.to_datetime(df["t"], utc=True, errors="coerce")
            df = df.set_index("t")
        keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
        df = df[keep]
        # Coerce numeric
        for c in keep:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df.dropna(subset=[c for c in keep if c != "Volume"])
        _cache[key] = (time.time(), df)
        return df

    def get_multiple_bars(
        self,
        symbols: list[str],
        timeframe: str = "1Day",
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> dict[str, pd.DataFrame]:
        return {s: self.get_bars(s, timeframe, start, end) for s in symbols}

    def get_options_chain(
        self,
        underlying: str,
        *,
        expiration: Optional[str] = None,
    ) -> list[dict]:
        """Fetch options chain snapshots from Alpaca.

        Returns a list of snapshot dicts (each with `symbol`, `latestQuote`,
        `greeks`, `impliedVolatility`, `openInterest`). Empty list if data is
        unavailable. Strategies use this via ctx.get_options_chain().
        """
        url = f"{_DATA_BASE}/v1beta1/options/snapshots/{underlying.upper()}"
        params: dict[str, object] = {"feed": "indicative", "limit": 100}
        if expiration:
            params["expiration_date"] = expiration
        out: list[dict] = []
        page_token = None
        pages = 0
        while True:
            p = dict(params)
            if page_token:
                p["page_token"] = page_token
            try:
                resp = self._session.get(url, params=p, timeout=15)
            except requests.RequestException as e:
                logger.warning("options_chain_request_failed sym=%s err=%s", underlying, e)
                return out
            if resp.status_code >= 400:
                logger.warning(
                    "options_chain_http_error sym=%s status=%s body=%s",
                    underlying, resp.status_code, resp.text[:200],
                )
                return out
            data = resp.json() or {}
            snaps = data.get("snapshots") or {}
            for sym, snap in snaps.items():
                s = dict(snap or {})
                s["symbol"] = sym
                out.append(s)
            page_token = data.get("next_page_token") or None
            pages += 1
            if not page_token or pages >= 20:
                break
        return out

    def get_latest_quote(self, symbol: str) -> Optional[dict]:
        url = f"{_DATA_BASE}/v2/stocks/{symbol}/quotes/latest"
        try:
            resp = self._session.get(url, params={"feed": _DATA_FEED}, timeout=15)
        except requests.RequestException as e:
            logger.warning("latest_quote_request_failed symbol=%s err=%s", symbol, e)
            return None
        if resp.status_code >= 400:
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


def _empty_bars() -> pd.DataFrame:
    return pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
