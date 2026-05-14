# ATTENTION — broker network restored, but two new anomalies need operator review

**Status as of 2026-05-13 (4:00 PM PT scheduled run):** the Alpaca broker
endpoints (`/v2/account`, `/v2/positions`, `/v2/orders`) are reachable again
from the scheduler sandbox after a 4-day outage (2026-05-07 / 2026-05-08 /
2026-05-11 / 2026-05-12). However, two new issues prevent the harness from
operating normally and need a human decision before the next run.

## Anomaly 1 — unexplained portfolio in the paper account

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

## Anomaly 2 — market-data subscription blocks bars / regime

Every call to `/v2/stocks/{symbol}/bars` on `data.alpaca.markets` returns:

```
403 {"message":"subscription does not permit querying recent SIP data"}
```

This affects every timeframe and every symbol tested today (SPY direct;
the regime classifier internally fans out to several symbols and all of
them fail). Effects:

- `regime` always reports `unknown` with `confidence=0.0`. The harness
  cannot classify the market regime, which is a prerequisite for
  `set-active`.
- `bars`, `indicator`, and `backtest` are all unusable.
- `quote` works for the bid side, but the ask side comes back as `0.0`
  on after-hours quotes (also likely a subscription/feed issue).

The CLI's `bars` subcommand has no `--feed` flag, so we cannot switch to
the IEX feed from the command line without a code change. Adding
`feed=iex` to `quant_trading_system/data/market_data_service.py:81`'s
params dict would be the minimal fix; an operator-side fix would be to
upgrade the Alpaca paper account to a tier that includes recent SIP
data.

**Action requested:** either upgrade the data subscription, or patch
`market_data_service.py` to request the IEX feed by default. Until one
of these happens, the harness cannot legitimately classify regime,
health-check strategies (they need price history to compute returns),
or evaluate setups.

## What the harness will do until then

The orchestrator will keep running its M-F 4:00 PM PT tick. Until the
above two items are addressed, every run will:

  1. Snapshot the broker (now reachable).
  2. Notice the unexplained positions and refuse to trade against them.
  3. Notice `regime` returns `unknown` and refuse to set an active
     strategy (cannot defend the pick without regime data).
  4. Write a short conclusion saying so and stop.

That is the correct behaviour per the operating rules ("If anything is
anomalous, document the situation in the conclusion and stop"). It is
also a no-op on the durable record — no orders submitted, no strategy
changes, no edits to strategy files.

## Where to read the full diagnosis

`quant_trading_system/knowledge_base/conclusions/2026-05-13.md` (today),
plus 2026-05-07 / 2026-05-08 / 2026-05-11 / 2026-05-12 for the prior
outage detail, and `quant_trading_system/knowledge_base/state/last_handoff.md`
for the most recent inter-Claude note.

## How to clear this file

Delete `ATTENTION.md` once (a) the unexplained portfolio has been resolved
one way or the other (closed, or assigned a strategy id), and (b) the bars
endpoint returns real data so `regime` can classify a real market.
