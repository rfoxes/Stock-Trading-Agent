---
id: equity_mean_reversion_bollinger_v2
name: Bollinger Band Mean Reversion (IBS-filtered v2)
type: equity
timeframe:
  - swing
  - intraday
indicators:
  - bollinger_bands
  - rsi
  - volume
  - ibs
market_regime:
  - range_bound
  - low_volatility
gap_types:
  - mean_reversion
parameters:
  bb_period: 20
  bb_std_dev: 2.0
  rsi_period: 14
  rsi_oversold: 30
  rsi_exit: 50
  volume_multiplier: 1.5
  volume_lookback: 20
  stop_loss_pct: 2.0
  max_hold_days: 10
  ibs_entry_max: 0.2
  ibs_exit_min: 0.8
status: testing
---

# Bollinger Band Mean Reversion (IBS-filtered v2)

## Description

UPDATE CANDIDATE for `equity_mean_reversion_bollinger` — identical to the
incumbent in every rule except one added entry filter and one added exit
accelerator based on Internal Bar Strength:

    IBS = (close − low) / (high − low)

Pagonidis (2013) documents that low IBS (close near the day's low)
predicts above-average next-day returns and high IBS below-average ones;
an IBS filter improved equity-index-ETF strategy returns by ~10pp while
cutting time-in-market ~45%. Requiring IBS < 0.2 at entry means we only
buy band breaks that closed weak (a genuine washout into the close), and
IBS > 0.8 accelerates the exit when a held name closes at the top of its
range.

Sources: Pagonidis, *The IBS Effect: Mean Reversion in Equity ETFs*
(2013),
https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf ;
replications: https://jonathankinlay.com/2019/07/the-internal-bar-strength-indicator/
and https://arxiv.org/pdf/2306.12434

Caveat (documented, acceptable): the published IBS edge is measured
close-to-close, while this harness fills at the next OPEN — part of the
overnight component is forfeited. Whether the filter still improves OUR
engine's fills is precisely what the replacement battery measures.

Seeded 2026-07-19 by operator research (`research_candidates.md`).
`status: testing`. Adjudication path: run
`cli evaluate-update equity_mean_reversion_bollinger equity_mean_reversion_bollinger_v2`
and apply REPLACE/KEEP verbatim. Do NOT run the addition battery on this —
it is a variant, not a new strategy (research_manual §Novelty).

## Entry Rules

All of the incumbent's entry rules, unchanged:

- Price closes below the lower Bollinger Band (20-period SMA, 2.0 std).
- RSI(14) below 30.
- Session volume ≥ 1.5× the 20-day average (capitulation confirmation).
- Minimum average daily dollar volume $5M.
- Avoid entry if earnings are scheduled within the next 3 trading days.
- Enter at the next session's open (market order).

Plus the v2 filter:

- **IBS < 0.2** — the day closed in the bottom fifth of its range. A bar
  with zero range scores a neutral 0.5 and therefore does not qualify.

## Exit Rules

All of the incumbent's exits, unchanged (first to trigger wins):

- Target: close at/above the middle Bollinger Band.
- Momentum: RSI(14) crosses above 50.
- Hard stop: 2.0% below entry.
- Time stop: 10 trading days.

Plus the v2 accelerator:

- **IBS > 0.8** — the held name closed at the top of its range; take the
  strength as the reversion largely done and exit next open.

## Risk Management

Identical to the incumbent: 1% risk per trade, max 5 concurrent
mean-reversion positions, no adding to losers, halve size in earnings
season, ≤2 positions per sector.
