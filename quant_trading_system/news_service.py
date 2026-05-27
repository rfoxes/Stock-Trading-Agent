"""News service — Alpaca News API fetch + per-symbol/sector/category HTML
writing + 90-day retention sweep.

The deterministic part of the daily news layer. The Cowork news agent calls
this module via the CLI (`cli news-fetch`, `cli news-cleanup`) to do the
mechanical work; the agent itself layers on WebSearch / WebFetch and writes
the final brief.

Source:
    Alpaca News API — https://data.alpaca.markets/v1beta1/news
    Same APCA-API-KEY-ID / APCA-API-SECRET-KEY as the trading and bar APIs.
    Free tier; no extra credentials.

Layout written to disk:
    knowledge_base/news/stocks/<SYMBOL>/<YYYY-MM-DD>.html
    knowledge_base/news/sectors/<SECTOR>/<YYYY-MM-DD>.html
    knowledge_base/news/categories/<CATEGORY>/<YYYY-MM-DD>.html
    knowledge_base/news/daily_summary/<YYYY-MM-DD>.html      (written by the agent)
"""

from __future__ import annotations

import datetime as dt
import html
import logging
from pathlib import Path
from typing import Any, Iterable

import requests

from quant_trading_system.config import Settings
from quant_trading_system.memory import KB_DIR

logger = logging.getLogger(__name__)


NEWS_DIR = KB_DIR / "news"
STOCKS_DIR = NEWS_DIR / "stocks"
SECTORS_DIR = NEWS_DIR / "sectors"
CATEGORIES_DIR = NEWS_DIR / "categories"
SUMMARY_DIR = NEWS_DIR / "daily_summary"

_NEWS_API = "https://data.alpaca.markets/v1beta1/news"
DEFAULT_RETENTION_DAYS = 90


# ---------------------------------------------------------------------------
# Sector classification (small hardcoded map; the current watchlist is small)
# ---------------------------------------------------------------------------

# Override / extend by editing this dict. If a symbol isn't here, the news
# agent should fall back to "uncategorized" rather than guess.
SYMBOL_TO_SECTOR: dict[str, str] = {
    "SPY": "index",
    "QQQ": "index",
    "AAPL": "technology",
    "MSFT": "technology",
    "GOOGL": "technology",
    "AMZN": "technology",
    "NVDA": "technology",
    "META": "technology",
    "TSLA": "consumer_discretionary",
    "JPM": "financials",
}

CATEGORIES = (
    "macro", "earnings", "geopolitics", "policy",
    "volatility", "options_flow",
)


def sector_for(symbol: str) -> str:
    return SYMBOL_TO_SECTOR.get(symbol.upper(), "uncategorized")


def ensure_dirs() -> None:
    for d in (NEWS_DIR, STOCKS_DIR, SECTORS_DIR, CATEGORIES_DIR, SUMMARY_DIR):
        d.mkdir(parents=True, exist_ok=True)
    for sec in set(SYMBOL_TO_SECTOR.values()) | {"uncategorized"}:
        (SECTORS_DIR / sec).mkdir(parents=True, exist_ok=True)
    for cat in CATEGORIES:
        (CATEGORIES_DIR / cat).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Alpaca News API
# ---------------------------------------------------------------------------


def fetch_alpaca_news(
    settings: Settings,
    symbols: Iterable[str],
    *,
    since: dt.datetime | None = None,
    until: dt.datetime | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Fetch news items from Alpaca for the given symbols.

    Returns a list of dicts. Each item has at least:
        headline, summary, url, source, created_at, symbols
    """
    if not settings.ALPACA_API_KEY:
        logger.warning("alpaca_news_no_credentials")
        return []
    syms = ",".join(sorted(set(s.upper() for s in symbols if s)))
    if not syms:
        return []
    if since is None:
        since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)
    if until is None:
        until = dt.datetime.now(dt.timezone.utc)
    params = {
        "symbols": syms,
        "start": since.isoformat(),
        "end": until.isoformat(),
        "limit": limit,
        "sort": "desc",
        "include_content": "false",
        "exclude_contentless": "true",
    }
    headers = {
        "APCA-API-KEY-ID": settings.ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": settings.ALPACA_SECRET_KEY,
        "Accept": "application/json",
    }
    out: list[dict[str, Any]] = []
    page_token: str | None = None
    pages = 0
    while True:
        p = dict(params)
        if page_token:
            p["page_token"] = page_token
        try:
            resp = requests.get(_NEWS_API, headers=headers, params=p, timeout=15)
        except requests.RequestException as e:
            logger.warning("alpaca_news_request_failed err=%s", e)
            break
        if resp.status_code >= 400:
            logger.warning("alpaca_news_http_error status=%s body=%s",
                           resp.status_code, resp.text[:200])
            break
        data = resp.json() or {}
        items = data.get("news") or []
        out.extend(items)
        page_token = data.get("next_page_token") or None
        pages += 1
        if not page_token or pages >= 5:  # hard cap pages to keep runs bounded
            break
    return out


# ---------------------------------------------------------------------------
# HTML composition
# ---------------------------------------------------------------------------


def _escape(s: Any) -> str:
    return html.escape(str(s or ""), quote=True)


def _render_news_html(title: str, items: list[dict[str, Any]], as_of: str) -> str:
    head = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{_escape(title)}</title>
<style>
  body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:920px;margin:2em auto;padding:0 1em;color:#222}}
  h1{{font-size:1.4em}}
  .item{{border-bottom:1px solid #ddd;padding:0.8em 0}}
  .meta{{color:#888;font-size:0.85em;margin-top:0.2em}}
  .summary{{margin-top:0.4em}}
  a{{color:#0066cc;text-decoration:none}}
  a:hover{{text-decoration:underline}}
  .empty{{color:#666;font-style:italic}}
</style></head><body>
<h1>{_escape(title)}</h1>
<p class="meta">As of {_escape(as_of)} — {len(items)} item{'s' if len(items) != 1 else ''}</p>
"""
    if not items:
        return head + '<p class="empty">No news items for this window.</p></body></html>'
    body = []
    for it in items:
        headline = _escape(it.get("headline", ""))
        summary = _escape(it.get("summary", ""))
        url = _escape(it.get("url", ""))
        source = _escape(it.get("source", ""))
        created = _escape(it.get("created_at", ""))
        syms = ", ".join(_escape(s) for s in (it.get("symbols") or []))
        body.append(
            f'<div class="item">'
            f'<div><a href="{url}" target="_blank" rel="noopener">{headline}</a></div>'
            f'<div class="meta">{source} · {created} · {syms}</div>'
            f'<div class="summary">{summary}</div>'
            f'</div>'
        )
    return head + "\n".join(body) + "\n</body></html>"


def write_symbol_html(symbol: str, date: str, items: list[dict[str, Any]]) -> Path:
    ensure_dirs()
    folder = STOCKS_DIR / symbol.upper()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{date}.html"
    title = f"{symbol.upper()} — news for {date}"
    path.write_text(_render_news_html(title, items, dt.datetime.now().isoformat()), encoding="utf-8")
    return path


def write_sector_html(sector: str, date: str, items: list[dict[str, Any]]) -> Path:
    ensure_dirs()
    folder = SECTORS_DIR / sector
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{date}.html"
    title = f"{sector} sector — news for {date}"
    path.write_text(_render_news_html(title, items, dt.datetime.now().isoformat()), encoding="utf-8")
    return path


def write_category_html(category: str, date: str, items: list[dict[str, Any]]) -> Path:
    ensure_dirs()
    folder = CATEGORIES_DIR / category
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{date}.html"
    title = f"{category} — news for {date}"
    path.write_text(_render_news_html(title, items, dt.datetime.now().isoformat()), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# High-level: fetch everything for a universe and write all HTMLs
# ---------------------------------------------------------------------------


def fetch_and_write(
    settings: Settings,
    symbols: list[str],
    *,
    date: str | None = None,
    lookback_hours: int = 24,
) -> dict[str, Any]:
    """For each symbol in `symbols`, fetch Alpaca news and write the per-symbol
    HTML. Then aggregate by sector and write per-sector HTMLs. The agent does
    macro/earnings/policy/geopolitics separately via WebSearch.
    """
    ensure_dirs()
    if date is None:
        date = dt.date.today().isoformat()
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=lookback_hours)

    summary: dict[str, Any] = {
        "date": date,
        "lookback_hours": lookback_hours,
        "symbols": {},
        "sectors": {},
        "total_items": 0,
    }

    # Group symbols by sector so we batch the Alpaca call (Alpaca accepts comma-sep)
    by_sector: dict[str, list[str]] = {}
    for s in symbols:
        by_sector.setdefault(sector_for(s), []).append(s.upper())

    # Per-symbol fetch + write
    all_items_by_symbol: dict[str, list[dict[str, Any]]] = {}
    for s in symbols:
        items = fetch_alpaca_news(settings, [s], since=since)
        all_items_by_symbol[s.upper()] = items
        path = write_symbol_html(s, date, items)
        summary["symbols"][s.upper()] = {
            "count": len(items),
            "path": str(path),
        }
        summary["total_items"] += len(items)

    # Per-sector roll-up
    for sector, syms in by_sector.items():
        merged: list[dict[str, Any]] = []
        for s in syms:
            merged.extend(all_items_by_symbol.get(s, []))
        # De-dup by id
        seen = set()
        deduped = []
        for it in merged:
            iid = it.get("id")
            if iid in seen:
                continue
            seen.add(iid)
            deduped.append(it)
        # Sort by created_at desc
        deduped.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        path = write_sector_html(sector, date, deduped)
        summary["sectors"][sector] = {
            "count": len(deduped),
            "path": str(path),
            "symbols": syms,
        }

    return summary


# ---------------------------------------------------------------------------
# Retention sweep
# ---------------------------------------------------------------------------


def cleanup_old(retention_days: int = DEFAULT_RETENTION_DAYS) -> dict[str, Any]:
    """Delete dated HTML files older than `retention_days` from news/*/."""
    ensure_dirs()
    cutoff = (dt.date.today() - dt.timedelta(days=retention_days)).isoformat()
    deleted: list[str] = []
    failed: list[str] = []
    for parent in (STOCKS_DIR, SECTORS_DIR, CATEGORIES_DIR, SUMMARY_DIR):
        if not parent.exists():
            continue
        for path in parent.rglob("*.html"):
            stem = path.stem  # expects YYYY-MM-DD
            if len(stem) != 10 or stem[4] != "-" or stem[7] != "-":
                continue
            if stem < cutoff:
                try:
                    path.unlink()
                    deleted.append(str(path))
                except OSError as e:
                    failed.append(f"{path}: {e}")
    return {
        "retention_days": retention_days,
        "cutoff_date": cutoff,
        "deleted_count": len(deleted),
        "deleted": deleted[:50],  # cap the response
        "failed": failed[:50],
    }
