---
id: equity_rsi2_pullback
name: RSI(2) Pullback in Uptrend
type: equity
timeframe:
  - swing
indicators:
  - rsi
  - sma
  - atr
  - volume
market_regime:
  - trending
  - range_bound
gap_types:
  - mean_reversion
parameters:
  rsi_period: 2
  rsi_entry_max: 10.0
  rsi_exit_min: 70.0
  exit_ma_period: 5
  trend_ma_period: 200
  trend_ma_min_periods: 60
  stop_loss_pct: 4.0
  max_hold_days: 10
  min_avg_dollar_volume: 5000000
  risk_pct_per_trade: 0.01
  max_position_pct: 0.10
  max_concurrent_positions: 4
status: testing
---

# RSI(2) Pullback in Uptrend

## Description

Larry Connors' 2-period RSI pullback system: buy sharp, short-lived dips in
stocks that are in a long-term uptrend, and sell into the snapback within a
few sessions. A 2-period RSI below 10 marks a statistically extreme
short-term washout; the 200-day SMA filter restricts entries to secular
uptrends so the dip being bought is noise, not a regime change. Decades of
published backtests report high win rates with short holds (2-7 sessions).

Sources: Connors & Alvarez, *Short Term Trading Strategies That Work*
(2008); rules + long-run evidence summarized at
https://www.quantifiedstrategies.com/rsi-2-strategy/ and
https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2

Seeded 2026-07-19 by operator research under the short-horizon mandate
(`research_candidates.md`). `status: testing` — MUST pass the addition
battery (`cli evaluate-add equity_rsi2_pullback`) and/or clear triage
baseline Sharpe before claiming any symbol. Never activate by hand.

## Entry Rules

- Close is above the 200-day SMA (computed with min_periods 60 so the
  filter is usable early in a backtest window; documented engine
  adaptation).
- RSI(2) closes below 10 (parameter `rsi_entry_max`; the literature finds
  lower thresholds → higher forward returns — 5 is a valid variant).
- 20-day average dollar volume ≥ $5M (liquidity floor).
- The day's news brief has no negative markers for the symbol (news used
  as a veto filter only, never as a trigger; inert in backtests).
- Not already holding the symbol; at most 4 concurrent positions from
  this strategy.
- Signal computes post-close; enter with a market order at the next open.

## Exit Rules

- **Strength exit:** close above the 5-day SMA (the classic Connors exit).
- **Momentum exit:** RSI(2) closes above 70.
- **Trend break:** close below the 200-day SMA — the uptrend premise is
  gone.
- **Hard stop:** 4.0% below entry (also attached as `stop_loss_pct`
  bracket so backtests track it intra-bar; live, the strategy re-checks
  the level every session — the strategy is the stop).
- **Time stop:** exit after 10 calendar days if still held (journal-dated;
  skipped when the position's age cannot be proven).

## Risk Management

- Risk 1% of equity per trade; position capped at 10% of equity.
- Position size = (equity × 1%) / (entry × stop distance 4%).
- Max 4 concurrent positions from this strategy.
- No adding to losers; one lot per symbol.

## Implementation notes

- Fully price-derived: replayable by `cli simulate` / triage / the
  addition battery with no news or calendar dependencies.
- Trade frequency is the highest in the short-horizon backlog — chosen
  deliberately so the 20-trade addition-battery floor is reachable on a
  single liquid symbol over a 2-year window.
