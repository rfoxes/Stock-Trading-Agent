---
id: equity_double_seven
name: Double Seven (7-Day Low / 7-Day High)
type: equity
timeframe:
  - swing
indicators:
  - sma
  - atr
  - volume
market_regime:
  - trending
  - range_bound
gap_types:
  - mean_reversion
parameters:
  entry_low_period: 7
  exit_high_period: 7
  trend_ma_period: 200
  trend_ma_min_periods: 60
  stop_atr_multiplier: 2.0
  atr_period: 14
  max_hold_days: 10
  min_avg_dollar_volume: 5000000
  risk_pct_per_trade: 0.01
  max_position_pct: 0.10
  max_concurrent_positions: 4
status: testing
---

# Double Seven (7-Day Low / 7-Day High)

## Description

Connors & Alvarez's "Double 7s": in a long-term uptrend, buy when the
close sets a 7-day closing low, sell when the close sets a 7-day closing
high. A deliberately minimal two-rule mean-reversion system — the book's
backtest reported 1,189 trades averaging +0.63% per trade on index ETFs.
Published follow-ups note the edge weakened after ~2010; that is exactly
what the addition battery's out-of-sample split exists to adjudicate, and
REJECT is a legitimate verdict.

Sources: Connors & Alvarez, *Short Term Trading Strategies That Work*
(2008);
https://www.quantifiedstrategies.com/larry-connors-double-seven-strategy-does-it-still-work/
and the co-author's own re-examination:
https://alvarezquanttrading.com/blog/double-7s-strategy/

Seeded 2026-07-19 by operator research under the short-horizon mandate
(`research_candidates.md`). `status: testing` — MUST pass
`cli evaluate-add equity_double_seven` and/or clear triage baseline before
claiming any symbol. Never activate by hand.

## Entry Rules

- Close is above the 200-day SMA (min_periods 60 engine adaptation).
- Today's close is the lowest close of the last 7 sessions
  (`entry_low_period`).
- 20-day average dollar volume ≥ $5M.
- No negative news markers for the symbol in today's brief (veto filter
  only; inert in backtests).
- Not already held; at most 4 concurrent positions from this strategy.
- Signal computes post-close; market order at the next open.

## Exit Rules

- **Primary exit:** today's close is the highest close of the last 7
  sessions (`exit_high_period`).
- **Trend break:** close below the 200-day SMA.
- **Hard stop:** 2.0× ATR(14) below entry (the book version has no stop;
  this harness requires one — attached as `stop_loss_pct` bracket for the
  backtester and re-checked every session live).
- **Time stop:** exit after 10 calendar days (journal-dated; skipped when
  age cannot be proven).

## Risk Management

- Risk 1% of equity per trade; position capped at 10% of equity.
- Size = (equity × 1%) / (entry × ATR-stop distance).
- Max 4 concurrent positions from this strategy; one lot per symbol.

## Implementation notes

- Fully price-derived and replayable by the backtester (variants: test 5-
  and 10-day lookbacks via the `<id>_v2` + evaluate-update path, not by
  editing this file in place).
