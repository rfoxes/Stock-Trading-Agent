---
id: equity_short_term_reversal
name: Short-Term Washout Reversal
type: equity
timeframe:
  - swing
indicators:
  - sma
  - atr
  - volume
market_regime:
  - range_bound
  - high_volatility
gap_types:
  - mean_reversion
parameters:
  decline_window: 5
  decline_entry_pct: 6.0
  trend_ma_period: 200
  trend_ma_min_periods: 60
  exit_ma_period: 5
  target_atr_multiplier: 1.5
  stop_atr_multiplier: 2.0
  atr_period: 14
  max_hold_days: 7
  min_avg_dollar_volume: 5000000
  risk_pct_per_trade: 0.01
  max_position_pct: 0.10
  max_concurrent_positions: 4
status: testing
---

# Short-Term Washout Reversal

## Description

Long-only, per-symbol adaptation of the classic short-term reversal
anomaly: stocks that fall hard over ~a week tend to bounce over the
following days. Lehmann (1990) documented weekly contrarian profits;
De Groot, Huij & Zhou (2012) showed the effect survives trading costs in
liquid large caps. The academic construction is a weekly-rebalanced
long-short portfolio, which this engine cannot hold (no short leg,
per-symbol backtests) — this adaptation buys a single name after an
N-day decline beyond a threshold, but only above its long-term trend so
we are buying a dip in a healthy name, not a knife in a broken one.

Sources: Lehmann (1990), *Fads, Martingales, and Market Efficiency*;
De Groot, Huij & Zhou (2012) summarized at
https://quantpedia.com/strategies/short-term-reversal-in-stocks

Seeded 2026-07-19 by operator research (`research_candidates.md`).
`status: testing` — MUST pass `cli evaluate-add equity_short_term_reversal`
and/or clear triage baseline before claiming any symbol. If the battery
blocks on the trade floor, loosen `decline_entry_pct` before abandoning —
a too-selective variant already failed the floor once (research_log
2026-07-11); if it blocks on Sharpe, that is a verdict, not a calibration
problem.

## Entry Rules

- 5-session return ≤ −6.0% (`decline_window`, `decline_entry_pct`).
- Close above the 200-day SMA (min_periods 60 engine adaptation) — the
  trend guard that separates a washout from a downtrend.
- 20-day average dollar volume ≥ $5M.
- No negative news markers for the symbol in today's brief (veto filter —
  a real adverse event is not a washout; inert in backtests).
- Not already held; at most 4 concurrent positions from this strategy.
- Signal computes post-close; market order at the next open.

## Exit Rules

- **Strength exit:** close above the 5-day SMA (bounce underway).
- **Target:** +1.5× ATR(14) above entry (attached as `take_profit_pct`
  bracket; re-checked live each session).
- **Hard stop:** 2.0× ATR(14) below entry (attached as `stop_loss_pct`
  bracket; re-checked live each session).
- **Time stop:** 7 calendar days (journal-dated; the reversion thesis
  decays fast).

## Risk Management

- Risk 1% of equity per trade; position capped at 10% of equity.
- Size = (equity × 1%) / (entry × ATR-stop distance).
- Max 4 concurrent positions; one lot per symbol; never add to a loser.
