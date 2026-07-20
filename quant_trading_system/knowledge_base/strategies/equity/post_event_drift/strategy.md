---
id: equity_post_event_drift
name: Post-Event Gap Drift (price/volume-proxied PEAD)
type: equity
timeframe:
  - swing
indicators:
  - gap_size
  - volume
  - atr
market_regime:
  - momentum
  - high_volatility
gap_types:
  - earnings_window
  - event_catalyst
  - gap_play
parameters:
  gap_entry_min_pct: 4.0
  volume_mult_min: 2.5
  volume_lookback: 20
  require_close_upper_half: true
  hold_max_sessions: 15
  target_atr_multiplier: 2.0
  stop_atr_multiplier: 1.5
  atr_period: 14
  min_avg_dollar_volume: 5000000
  risk_pct_per_trade: 0.01
  max_position_pct: 0.10
  max_concurrent_positions: 3
status: testing
---

# Post-Event Gap Drift (price/volume-proxied PEAD)

## Description

Post-earnings announcement drift is one of the oldest documented
anomalies (Ball & Brown 1968 lineage): prices keep drifting in the
direction of an earnings surprise for weeks after the print. The existing
`equity_event_driven_catalyst` reads the news brief to find events — which
makes it structurally un-backtestable (0 trades in every simulation; the
root cause of the degenerate provisionals, research_tasks Open Q#5).

This strategy detects the event day FROM THE PRICE BAR ITSELF, so every
battery, triage, and head-to-head can replay it:

    event day := overnight gap up ≥ 4% vs prior close
                 AND volume ≥ 2.5× the prior 20-day average
                 AND close in the upper half of the day's range (holds
                 the gap)

A large gap on a volume surge that closes strong is, empirically, almost
always a real catalyst (earnings, guidance, M&A, regulatory). We enter
the NEXT open — deliberately not chasing the gap itself, but buying the
drift after the market has shown the gap holds — and ride it inside the
empirical drift window with ATR brackets and a session-counted time exit.

Sources: https://quantpedia.com/strategies/post-earnings-announcement-effect
and https://quantpedia.com/50-years-in-pead-research/ (documented drift
persists ~4 weeks to a quarter; 2.6-9.4%/quarter abnormal in the
literature).

Seeded 2026-07-19 by operator research (`research_candidates.md`).
`status: testing` — MUST pass `cli evaluate-add equity_post_event_drift`
and/or clear triage baseline before claiming any symbol. If validated,
this is the intended REPLAYABLE responder for `earnings_window` /
`event_catalyst` gaps (the recurring "TSM printed, no responder" gap) and
a rankable unrestricted-triage challenger for the event-driven
provisionals (GS/MS/PYPL/UNH/RIVN/QCOM...).

## Entry Rules

- Today's bar is an event day per the definition above (all three
  conditions; the volume average excludes today).
- 20-day average dollar volume ≥ $5M.
- No negative news markers for the symbol in today's brief (veto filter;
  inert in backtests — a gap up with negative-tagged news is a short
  squeeze or a relief pop, not a clean catalyst).
- Not already held; at most 3 concurrent positions from this strategy.
- Signal computes post-close on the event day; market order at the next
  open.

## Exit Rules

- **Invalidation:** close below the event day's LOW — the gap thesis is
  dead. (The event day is re-located from bars each session: the most
  recent event day at/before today; a fresh event resets the reference.)
- **Target:** +2.0× ATR(14) above entry (`take_profit_pct` bracket;
  re-checked live each session).
- **Hard stop:** 1.5× ATR(14) below entry (`stop_loss_pct` bracket;
  re-checked live each session).
- **Session-counted time exit:** more than `hold_max_sessions` (15) bars
  since the most recent event day — derived from bars, so it is enforced
  in BACKTESTS as well as live (unlike journal-dated time stops).
- **News exit:** brief carries negative markers for the held name (live
  only).

## Risk Management

- Risk 1% of equity per trade; position capped at 10% of equity.
- Size = (equity × 1%) / (entry × ATR-stop distance).
- Max 3 concurrent positions; one lot per symbol; never add on the way
  down.

## Implementation notes

- Trade count scales with how eventful the symbol is: on high-news names
  (ARM/SMCI/MU/INTC cohort) a 2-year window should clear the 20-trade
  battery floor; on quiet mega-caps it will not — pick backtest symbols
  accordingly before concluding REJECT-by-floor.
- Gap threshold 4% / volume 2.5× are literature-informed starting priors;
  calibrate via backtest (variants through the `_v2` + evaluate-update
  path).
