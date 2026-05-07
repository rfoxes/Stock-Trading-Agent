"""Market hours utilities — pure stdlib.

The harness no longer runs a long-lived APScheduler daemon (each scheduled
run fires a fresh process via Cowork or cron). What's left here is just the
two helpers `is_market_open()` and `next_market_open()`, used by the
`market_status` tool.

These work without `exchange_calendars` (and without `apscheduler`) by
falling back to a weekday check + a small hardcoded NYSE holiday list. If
`exchange_calendars` IS available, we use it for accuracy.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta, tzinfo
from typing import Iterable

try:
    from zoneinfo import ZoneInfo  # py3.9+
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

logger = logging.getLogger(__name__)


def _et_tz() -> tzinfo | None:
    if ZoneInfo is None:
        return None
    return ZoneInfo("America/New_York")


# Hardcoded NYSE full-day holidays for 2025-2027. Expand as needed.
# (Half-days like Black Friday are treated as full days here — close enough
# for the agent's "should I be doing things" check.)
_NYSE_HOLIDAYS: set[date] = {
    # 2025
    date(2025, 1, 1), date(2025, 1, 20), date(2025, 2, 17),
    date(2025, 4, 18), date(2025, 5, 26), date(2025, 6, 19),
    date(2025, 7, 4), date(2025, 9, 1), date(2025, 11, 27),
    date(2025, 12, 25),
    # 2026
    date(2026, 1, 1), date(2026, 1, 19), date(2026, 2, 16),
    date(2026, 4, 3), date(2026, 5, 25), date(2026, 6, 19),
    date(2026, 7, 3), date(2026, 9, 7), date(2026, 11, 26),
    date(2026, 12, 25),
    # 2027
    date(2027, 1, 1), date(2027, 1, 18), date(2027, 2, 15),
    date(2027, 3, 26), date(2027, 5, 31), date(2027, 6, 18),
    date(2027, 7, 5), date(2027, 9, 6), date(2027, 11, 25),
    date(2027, 12, 24),
}


def _is_session_day(d: date) -> bool:
    if d.weekday() >= 5:
        return False
    if d in _NYSE_HOLIDAYS:
        return False
    return True


def _try_xcals_session_day(d: date) -> bool | None:
    """Use exchange_calendars if available; otherwise return None."""
    try:
        import exchange_calendars as xcals  # type: ignore
    except ImportError:
        return None
    try:
        return bool(xcals.get_calendar("XNYS").is_session(d))
    except Exception:
        return None


def is_session_day(d: date | None = None) -> bool:
    d = d or date.today()
    via_xcals = _try_xcals_session_day(d)
    if via_xcals is not None:
        return via_xcals
    return _is_session_day(d)


def is_market_open() -> bool:
    """True if the US equities market is currently in regular session."""
    et = _et_tz()
    now = datetime.now(et) if et else datetime.now()
    if not is_session_day(now.date()):
        return False
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    return market_open <= now <= market_close


def next_market_open() -> datetime:
    """Next regular-session open time."""
    et = _et_tz()
    now = datetime.now(et) if et else datetime.now()
    candidate = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now >= candidate:
        candidate = candidate + timedelta(days=1)
    while not is_session_day(candidate.date()):
        candidate = candidate + timedelta(days=1)
    return candidate


# ---------------------------------------------------------------------------
# Legacy MarketScheduler — kept as a stub so legacy imports still work, but
# the harness no longer runs a daemon.
# ---------------------------------------------------------------------------


class MarketScheduler:
    """DEPRECATED. The harness uses external schedulers (Cowork / cron).

    Kept as a stub so any old imports don't crash. Calling start() raises.
    """

    def __init__(self, *args, **kwargs) -> None:
        logger.warning("market_scheduler_deprecated; use Cowork scheduled task or cron")

    def start(self) -> None:
        raise RuntimeError(
            "MarketScheduler is removed. The harness runs as a one-shot script "
            "triggered externally — see daily_prompt.md (Cowork) or README "
            "(cron on Pi)."
        )

    def stop(self) -> None:
        return None
