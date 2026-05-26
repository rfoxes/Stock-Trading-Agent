# ATTENTION — unexplained portfolio still needs operator review

**Status as of 2026-05-13 (post-close, post-scheduled-run):** the 4-day
broker outage is resolved and the bars-feed subscription issue has now
also been patched (see "Resolved" section below). One real anomaly
remains: the paper account holds 10 positions that the harness journal
does not explain.

## Open anomaly — unexplained portfolio in the paper account

The paper account is no longer in its expected baseline state. As of today's
post-close snapshot:

- **Equity:** $111,924.00 (previously baselined at $5,000 on 2026-05-11 via
  `kelly-size`).
- **Cash:** -$96,531.22 (margin used).
- **Buying power:** $15,392.78.
- **Open positions:** 10 long equity positions totalling ~$208,455 in market
  value, with ~$11,925 net unrealized P&L:

  | Symbol | Qty | Avg Entry | Current | Unrealized P&L | % |
  |--------|-----|-----------|---------|----------------|---|
  | AAPL | 72 | 271.30 | 298.63 | +1,968.0 | +10.1% |
  | AMZN | 76 | 248.53 | 270.40 | +1,661.8 | +8.8% |
  | GOOGL | 56 | 338.79 | 403.48 | +3,622.6 | +19.1% |
  | JPM | 64 | 313.04 | 301.00 | -770.4 | -3.8% |
  | META | 28 | 681.55 | 616.10 | -1,832.7 | -9.6% |
  | MSFT | 44 | 421.24 | 404.65 | -729.8 | -3.9% |
  | NVDA | 96 | 199.40 | 227.39 | +2,687.3 | +14.0% |
  | QQQ | 28 | 647.96 | 718.25 | +1,968.0 | +10.8% |
  | SPY | 35 | 708.81 | 743.64 | +1,218.9 | +4.9% |
  | TSLA | 48 | 403.98 | 448.36 | +2,130.2 | +11.0% |

**The harness journal contains zero events**
(`knowledge_base/journal/` still does not exist on disk, `recent-trades`
returns `count: 0`). None of these positions were submitted by the
orchestrator. Per the operating rules' "unexpected positions" guidance, the
harness has not closed or modified them — it is treating them as a manual
operator override and waiting for instructions.

**Action requested:** confirm whether these positions are intentional
(e.g. a seeded portfolio you want the harness to manage) or test data
that should be flat-closed before the harness starts trading on its own.
If they are intended, please tell the next run which strategy id to tag
them under so the journal can attribute future P&L correctly.

## Resolved — bars feed now uses IEX (operator-driven post-run patch)

`quant_trading_system/data/market_data_service.py` was edited after
today's scheduled run completed to default the Alpaca data feed to
IEX and read an `ALPACA_DATA_FEED` env override. Specifically:

- Added `_DATA_FEED = os.environ.get("ALPACA_DATA_FEED", "iex")` at
  module scope.
- Threaded `"feed": _DATA_FEED` into `get_bars`' params dict.
- Added `params={"feed": _DATA_FEED}` to `get_latest_quote`'s request.

Verified post-patch:
`bars SPY --days 60` returns 41 daily bars (2026-03-16 → 2026-05-13),
and `regime` returns
`bull, confidence=0.76, price_vs_sma200=+9.45%, adx=26.0`.

If you later upgrade the Alpaca subscription to a SIP-included tier,
set `export ALPACA_DATA_FEED=sip` in the scheduler environment — no
further code change needed.

**One calibration caveat to be aware of.** Volume figures are now
IEX-only (a fraction of the consolidated SIP tape). Equity strategies
in the library that key off *absolute* volume thresholds —
`equity_breakout_volume_confirmation`, `equity_gap_and_go`,
`equity_opening_range_breakout`, `equity_vwap_reversion` — will
under-trigger until their thresholds are recalibrated. Strategies that
use *relative* volume (today vs. its own 20-day average) are fine.
Tomorrow's handoff already tells the next run to either avoid those
strategies or to recalibrate them deliberately.

## What the harness will do until the open anomaly is addressed

The orchestrator will keep running its M-F 4:00 PM PT tick. As long as
the 10 unexplained positions remain unattributed, every run will:

  1. Snapshot the broker.
  2. Notice the unexplained positions and refuse to trade *against*
     them (no closing, no offsetting).
  3. Decide whether the harness should start trading *alongside* them
     — only with very limited buying power ($15,393 today) and a
     strategy pick that's defensible from the current regime.
  4. Write a conclusion explaining what it did or didn't do.

## Where to read the full diagnosis

`quant_trading_system/knowledge_base/conclusions/2026-05-13.md` (today),
plus 2026-05-07 / 2026-05-08 / 2026-05-11 / 2026-05-12 for the prior
outage detail, and `quant_trading_system/knowledge_base/state/last_handoff.md`
for the most recent inter-Claude note.

## How to clear this file

Delete `ATTENTION.md` once the unexplained portfolio has been resolved
one way or the other (closed, or assigned a strategy id so the harness
can attribute it in the journal).
