---
id: equity_turn_of_month
name: Turn-of-the-Month (Index ETFs)
type: equity
timeframe:
  - swing
indicators:
  - calendar
  - sma
symbols:
  - SPY
  - QQQ
market_regime:
  - trending
  - range_bound
parameters:
  entry_weekdays_before_eom: 4
  exit_trading_day_of_month: 3
  stop_loss_pct: 3.0
  max_hold_days: 12
  use_trend_filter: false
  trend_ma_period: 200
  trend_ma_min_periods: 60
  risk_pct_per_trade: 0.01
  max_position_pct: 0.10
status: testing
---

# Turn-of-the-Month (Index ETFs)

## Description

The turn-of-the-month effect: equity index returns concentrate in the
last ~4 trading days and first ~3 trading days of each month — one of the
most persistent calendar seasonalities on record (pension inflows,
month-end rebalancing). The canonical construction (long SPY from T-4
through T+3, flat otherwise) has historically captured a disproportionate
share of index returns while in the market ~1/3 of the time.

Sources: Lakonishok & Smidt (1988) lineage;
https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes and
https://quantpedia.com/an-examination-of-the-turn-of-the-month-effect/
(futures evidence: Carcano & Tornero).

Purely calendar-driven — no news, no indicators required — so it is
trivially replayable by every battery, and its ~12 round-trips/year give
~24 trades over a 2-year window (clears the addition battery's 20-trade
floor, barely; always use the full window).

Frontmatter restricts this strategy to SPY and QQQ: the anomaly is an
index-flow effect, not a single-stock effect.

Seeded 2026-07-19 by operator research (`research_candidates.md`).
`status: testing` — MUST pass `cli evaluate-add equity_turn_of_month`
and/or clear triage baseline before claiming. If validated, it is a
natural head-to-head challenger for the SPY/QQQ placeholders currently
parked on trend-following.

## Entry Rules

- Signal (computed post-close): exactly 4 weekdays remain in the calendar
  month after today (`entry_weekdays_before_eom`). The market buy fills at
  the next open ≈ the 4th-to-last trading day. (Weekday counting stands in
  for a holiday calendar; a mid-window holiday shifts entry by one day —
  a documented, deterministic approximation.)
- Optional trend filter (off by default, per the literature): close >
  200-day SMA when `use_trend_filter` is true.
- Not already held.

## Exit Rules

- **Calendar exit:** once the new month has printed
  `exit_trading_day_of_month` (3) or more session bars, sell — fills at
  the open of ~the 4th trading day. Bars-in-month are counted from the
  data itself, so this exit is enforced in backtests too.
- **Safety stop:** 3.0% below entry (`stop_loss_pct` bracket; re-checked
  live).
- **Failsafe time stop:** 12 calendar days (journal-dated) — only fires
  if the calendar exit somehow failed to.

## Risk Management

- Risk 1% of equity per trade; position capped at 10% of equity.
- One lot per symbol; the window is ~7 sessions by construction.
