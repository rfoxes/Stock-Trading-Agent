"""Derived universe — replaces the static `DEFAULT_WATCHLIST` env var.

The harness is wiki-driven: anything the wiki tracks is part of the universe.
This module computes the universe at runtime as the union of four sources:

  1. Active strategies' declared symbols (frontmatter `symbols:` or `sectors:`).
  2. Currently held positions on the broker.
  3. Symbols the news layer is already tracking (subdirs under news/stocks/).
  4. Operator-declared additions in `state/extra_symbols.md` (free-form list).

`DEFAULT_WATCHLIST` in `.env` is kept only as a *bootstrap fallback*: used
when none of the above sources have anything. Once any strategy is active or
any position is open, the env var is no longer the source of truth.

A small sector map ships in `news_service.SYMBOL_TO_SECTOR`; the universe
module uses it to resolve `sectors: [...]` filters in strategy frontmatter
to actual symbols.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

from quant_trading_system import memory
from quant_trading_system.config import Settings

logger = logging.getLogger(__name__)


EXTRA_SYMBOLS_FILE = memory.STATE_DIR / "extra_symbols.md"


@dataclass
class Universe:
    """Composed universe with provenance for each symbol."""

    symbols: list[str] = field(default_factory=list)
    by_source: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbols": self.symbols,
            "count": len(self.symbols),
            "by_source": self.by_source,
        }


# ---------------------------------------------------------------------------
# Source 1: active strategies' declared symbols
# ---------------------------------------------------------------------------


def _expand_sectors(sectors: list[str]) -> set[str]:
    """Resolve sector names to symbols via news_service.SYMBOL_TO_SECTOR."""
    from quant_trading_system.news_service import SYMBOL_TO_SECTOR

    wanted = {s.lower() for s in sectors}
    return {
        sym for sym, sec in SYMBOL_TO_SECTOR.items() if sec.lower() in wanted
    }


def symbols_from_strategies(include_testing: bool = False) -> set[str]:
    """Symbols declared by every active (and optionally testing) strategy."""
    statuses = ("active",)
    if include_testing:
        statuses = ("active", "testing")
    out: set[str] = set()
    for sf in memory.list_strategies():
        if sf.status not in statuses:
            continue
        fm = sf.frontmatter or {}
        explicit = fm.get("symbols") or []
        if isinstance(explicit, str):
            explicit = [explicit]
        for s in explicit:
            if isinstance(s, str) and s.strip():
                out.add(s.upper().strip())
        sectors = fm.get("sectors") or []
        if isinstance(sectors, str):
            sectors = [sectors]
        out.update(_expand_sectors([s for s in sectors if isinstance(s, str)]))
    return out


# ---------------------------------------------------------------------------
# Source 2: currently held positions
# ---------------------------------------------------------------------------


def symbols_from_positions(alpaca_client: Any) -> set[str]:
    if alpaca_client is None:
        return set()
    try:
        positions = alpaca_client.get_positions() or []
    except Exception as e:
        logger.warning("universe_positions_lookup_failed err=%s", e)
        return set()
    return {
        str(p.get("symbol", "")).upper()
        for p in positions
        if str(p.get("symbol", "")).strip()
    }


# ---------------------------------------------------------------------------
# Source 3: news-tracked symbols (anything with a news/stocks/<SYMBOL>/ dir)
# ---------------------------------------------------------------------------


def symbols_from_news() -> set[str]:
    from quant_trading_system.news_service import STOCKS_DIR

    if not STOCKS_DIR.exists():
        return set()
    return {
        d.name.upper()
        for d in STOCKS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }


# ---------------------------------------------------------------------------
# Source 4: operator's extra_symbols.md
# ---------------------------------------------------------------------------

# Match standalone uppercase tickers (2-5 chars, optional .X suffix for class B etc.).
# We require >= 2 chars to avoid catching English single letters (A, I) and the
# real but rare 1-char tickers (T, F, V) — those can be added via explicit
# declarations if needed.
_TICKER_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,4}(?:[.\-][A-Z]{1,2})?)\b")


def symbols_from_operator() -> set[str]:
    """Parse state/extra_symbols.md for operator-declared additions.

    Format is intentionally forgiving — anything that looks like a ticker
    (1-5 uppercase chars at a word boundary) is picked up. Lines starting
    with `#` are treated as comments.
    """
    if not EXTRA_SYMBOLS_FILE.exists():
        return set()
    text = EXTRA_SYMBOLS_FILE.read_text(encoding="utf-8")
    out: set[str] = set()
    # Common English words / abbreviations that look like tickers — skip these.
    stop = {
        "AN", "THE", "AND", "OR", "BUT", "IF", "TO", "OF", "IN",
        "ON", "AT", "BY", "FOR", "IS", "IT", "BE", "AS", "WE", "DO", "NOT",
        "NO", "YES", "ANY", "ALL", "ADD", "BUY", "SELL", "USD", "EUR",
        "MD", "PT", "AI", "EU", "US", "UK", "GDP", "CPI", "PPI", "FOMC",
        "ETF", "ETFS", "IPO", "ATM", "OTM", "ITM", "OPG", "GTC", "IOC",
        "FOK", "DAY", "ISN", "DONT", "DOESNT", "WONT", "CANT", "ITS",
        "EG", "IE", "ETC", "VS", "PER", "API", "URL", "URI", "CSV", "TSV",
        "JSON", "HTML", "MD",
    }
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        for m in _TICKER_RE.findall(s):
            if m in stop:
                continue
            out.add(m)
    return out


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------


def compute_universe(
    settings: Settings,
    *,
    alpaca_client: Any = None,
    include_testing_strategies: bool = False,
) -> Universe:
    """Compose today's universe from all four sources."""
    by_source: dict[str, list[str]] = {}

    from_strats = symbols_from_strategies(include_testing=include_testing_strategies)
    if from_strats:
        by_source["strategies"] = sorted(from_strats)

    from_positions = symbols_from_positions(alpaca_client)
    if from_positions:
        by_source["positions"] = sorted(from_positions)

    from_news_dir = symbols_from_news()
    if from_news_dir:
        by_source["news_tracked"] = sorted(from_news_dir)

    from_operator_file = symbols_from_operator()
    if from_operator_file:
        by_source["operator_extras"] = sorted(from_operator_file)

    composed = from_strats | from_positions | from_news_dir | from_operator_file

    if not composed:
        # Bootstrap fallback — only used when nothing else has anything
        fallback = {s.upper() for s in settings.watchlist}
        composed = fallback
        if fallback:
            by_source["bootstrap_env_DEFAULT_WATCHLIST"] = sorted(fallback)

    return Universe(symbols=sorted(composed), by_source=by_source)


def filter_universe_for_strategy(
    universe: Universe,
    *,
    strategy_frontmatter: dict[str, Any],
) -> list[str]:
    """Narrow the universe to what one strategy says it trades.

    Strategies can declare `symbols: [...]` (explicit) and/or
    `sectors: [...]` (resolved via SYMBOL_TO_SECTOR). If neither is
    declared, the strategy gets the full universe.
    """
    if not strategy_frontmatter:
        return list(universe.symbols)
    explicit = strategy_frontmatter.get("symbols") or []
    if isinstance(explicit, str):
        explicit = [explicit]
    sectors = strategy_frontmatter.get("sectors") or []
    if isinstance(sectors, str):
        sectors = [sectors]
    if not explicit and not sectors:
        return list(universe.symbols)

    wanted: set[str] = set()
    for s in explicit:
        if isinstance(s, str) and s.strip():
            wanted.add(s.upper().strip())
    if sectors:
        wanted.update(_expand_sectors([s for s in sectors if isinstance(s, str)]))

    universe_set = set(universe.symbols)
    return sorted(wanted & universe_set) or sorted(wanted)
