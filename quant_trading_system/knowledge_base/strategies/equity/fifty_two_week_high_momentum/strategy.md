---
id: equity_52wk_high_momentum
name: 52-Week High Proximity Momentum
type: equity
timeframe:
  - swing
indicators:
  - rolling_high
  - sma
  - atr
  - volume
market_regime:
  - trending
  - high_momentum
gap_types:
  - breakout
  - trending
parameters:
  high_lookback: 252
  high_min_periods: 126
  proximity_entry_pct: 2.0
  volume_mult_min: 1.5
  volume_lookback: 20
  exit_ma_period: 20
  stop_atr_multiplier: 2.5
  atr_period: 14
  max_hold_days: 30
  min_avg_dollar_volume: 5000000
  risk_pct_per_trade: 0.01
  max_position_pct: 0.10
  max_concurrent_positions: 4
status: testing
---

# 52-Week High Proximity Momentum

## Description

George & Hwang (2004, Journal of Finance) showed that nearness to the
52-week high predicts returns better than conventional past-return
momentum (0.65%/mo for the 52-week-high sort vs 0.38%/mo classic
momentum) — the mechanism is anchoring: traders under-react near a
salient price ceiling, and once price pushes through, the suppressed move
completes. This implementation trades the crossing: enter when the close
first moves into the proximity band of the prior 52-week high on
above-average volume, ride with a wide ATR stop, exit on trend loss or
the time stop. This is the multi-week end of the short-horizon band.

Sources: https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf ;
practitioner summary:
https://alphaarchitect.com/the-secret-to-momentum-is-the-52-week-high/

Overlap note (research_manual §Novelty): the incumbent
`equity_breakout_volume_confirmation` is an N-day-high breakout. This
strategy's anchor (prior 252-bar high, proximity band, crossing
condition) is structurally different, so it is filed as an addition
candidate — but if the battery-relevant difference turns out to be just
the anchor length, adjudicate it against the incumbent via
`cli evaluate-update` instead of keeping both.

Seeded 2026-07-19 by operator research (`research_candidates.md`).
`status: testing` — MUST pass `cli evaluate-add equity_52wk_high_momentum`
and/or clear triage baseline before claiming. Per-symbol trade frequency
is the lowest in the backlog — expect to need the widest backtest window
for the 20-trade floor, and treat a floor-block as "insufficient sample,"
not proof of edge.

## Entry Rules

- The prior 52-week closing high is computed EXCLUDING today
  (`high_lookback` 252 bars, min_periods 126 — engine adaptation so the
  anchor exists early in a backtest window).
- Today's close crosses INTO the proximity band: close ≥ 98% of the prior
  high (`proximity_entry_pct` 2.0) AND yesterday's close was below
  yesterday's band — entry fires on the crossing only, never while
  coasting inside the band.
- Session volume ≥ 1.5× the 20-day average (participation confirmation).
- 20-day average dollar volume ≥ $5M.
- No negative news markers in today's brief (veto filter).
- Not already held; at most 4 concurrent positions from this strategy.
- Signal computes post-close; market order at the next open.

## Exit Rules

- **Trend-loss exit:** close below the 20-day SMA (`exit_ma_period`).
- **Hard stop:** 2.5× ATR(14) below entry (`stop_loss_pct` bracket;
  re-checked live each session).
- **Time stop:** 30 calendar days (~21 sessions, journal-dated) — the cap
  that keeps this inside the short-horizon mandate rather than drifting
  into George & Hwang's original 6-12 month holds.

## Risk Management

- Risk 1% of equity per trade; position capped at 10% of equity.
- Size = (equity × 1%) / (entry × ATR-stop distance).
- Max 4 concurrent positions; one lot per symbol.
