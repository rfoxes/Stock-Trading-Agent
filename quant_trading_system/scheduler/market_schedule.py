"""Market hours scheduling using APScheduler."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

if TYPE_CHECKING:
    from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)

ET = ZoneInfo("America/New_York")


def is_market_open() -> bool:
    """Check if the US stock market is currently open."""
    try:
        import exchange_calendars as xcals

        nyse = xcals.get_calendar("XNYS")
        now = datetime.now(ET)
        today = now.date()

        if not nyse.is_session(today):
            return False

        market_open = now.replace(hour=9, minute=30, second=0)
        market_close = now.replace(hour=16, minute=0, second=0)
        return market_open <= now <= market_close

    except ImportError:
        # Fallback: weekday check only
        now = datetime.now(ET)
        if now.weekday() >= 5:  # Saturday or Sunday
            return False
        market_open = now.replace(hour=9, minute=30, second=0)
        market_close = now.replace(hour=16, minute=0, second=0)
        return market_open <= now <= market_close


def next_market_open() -> datetime:
    """Get the next market open time."""
    try:
        import exchange_calendars as xcals

        nyse = xcals.get_calendar("XNYS")
        now = datetime.now(ET)
        # Get the next session
        sessions = nyse.sessions_window(now.date(), 5)
        for session in sessions:
            open_time = datetime.combine(session, datetime.min.time().replace(hour=9, minute=30))
            open_time = open_time.replace(tzinfo=ET)
            if open_time > now:
                return open_time
    except ImportError:
        pass

    # Fallback
    now = datetime.now(ET)
    next_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now >= next_open:
        from datetime import timedelta

        next_open += timedelta(days=1)
    while next_open.weekday() >= 5:
        from datetime import timedelta

        next_open += timedelta(days=1)
    return next_open


class MarketScheduler:
    """Manages scheduled trading jobs aligned with market hours."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._scheduler = BackgroundScheduler(timezone=ET)
        self._setup_jobs()

    def _setup_jobs(self) -> None:
        """Configure all scheduled jobs."""

        # Pre-market scan: 8:00 AM ET, weekdays
        self._scheduler.add_job(
            self._pre_market_scan,
            CronTrigger(hour=8, minute=0, day_of_week="mon-fri", timezone=ET),
            id="pre_market_scan",
            name="Pre-Market Scan",
        )

        # Intraday cycle: every N minutes during market hours
        interval = self._settings.INTRADAY_INTERVAL_MINUTES
        self._scheduler.add_job(
            self._intraday_cycle,
            CronTrigger(
                minute=f"*/{interval}",
                hour="9-15",
                day_of_week="mon-fri",
                timezone=ET,
            ),
            id="intraday_cycle",
            name="Intraday Cycle",
        )

        # Swing daily cycle: near market close
        swing_time = self._settings.SWING_REBALANCE_TIME.split(":")
        self._scheduler.add_job(
            self._swing_daily_cycle,
            CronTrigger(
                hour=int(swing_time[0]),
                minute=int(swing_time[1]),
                day_of_week="mon-fri",
                timezone=ET,
            ),
            id="swing_daily_cycle",
            name="Swing Daily Cycle",
        )

        # Position weekly cycle
        self._scheduler.add_job(
            self._position_weekly_cycle,
            CronTrigger(
                hour=15,
                minute=50,
                day_of_week=self._settings.POSITION_REBALANCE_DAY[:3],
                timezone=ET,
            ),
            id="position_weekly_cycle",
            name="Position Weekly Cycle",
        )

        # Post-market review: 4:15 PM ET
        self._scheduler.add_job(
            self._post_market_review,
            CronTrigger(hour=16, minute=15, day_of_week="mon-fri", timezone=ET),
            id="post_market_review",
            name="Post-Market Review",
        )

        # Weekend research
        self._scheduler.add_job(
            self._weekend_research,
            CronTrigger(hour=10, minute=0, day_of_week="sat", timezone=ET),
            id="weekend_research",
            name="Weekend Research",
        )

        logger.info("scheduler_jobs_configured", job_count=len(self._scheduler.get_jobs()))

    def start(self) -> None:
        """Start the scheduler."""
        self._scheduler.start()
        logger.info("scheduler_started")

    def stop(self) -> None:
        """Stop the scheduler."""
        self._scheduler.shutdown(wait=False)
        logger.info("scheduler_stopped")

    def _guard_market_hours(self) -> bool:
        """Check if market is open before trading."""
        if not is_market_open():
            logger.debug("market_closed_skipping")
            return False
        return True

    def _pre_market_scan(self) -> None:
        """Run pre-market data refresh and regime classification."""
        logger.info("pre_market_scan_start")
        # This will be wired to the full pipeline in production
        # For now, just log
        logger.info("pre_market_scan_complete")

    def _intraday_cycle(self) -> None:
        """Run the intraday trading agent."""
        if not self._guard_market_hours():
            return
        logger.info("intraday_cycle_start")
        # Wire to: run_single_cycle with agents=["intraday"]
        logger.info("intraday_cycle_complete")

    def _swing_daily_cycle(self) -> None:
        """Run the swing trading agent."""
        if not self._guard_market_hours():
            return
        logger.info("swing_daily_cycle_start")
        # Wire to: run_single_cycle with agents=["swing"]
        logger.info("swing_daily_cycle_complete")

    def _position_weekly_cycle(self) -> None:
        """Run the position trading agent."""
        if not self._guard_market_hours():
            return
        logger.info("position_weekly_cycle_start")
        # Wire to: run_single_cycle with agents=["position"]
        logger.info("position_weekly_cycle_complete")

    def _post_market_review(self) -> None:
        """Generate daily P&L report and update knowledge base."""
        logger.info("post_market_review_start")
        logger.info("post_market_review_complete")

    def _weekend_research(self) -> None:
        """Run strategy research and backtesting."""
        logger.info("weekend_research_start")
        # Wire to: StrategyResearchAgent + BacktestingAgent
        logger.info("weekend_research_complete")
