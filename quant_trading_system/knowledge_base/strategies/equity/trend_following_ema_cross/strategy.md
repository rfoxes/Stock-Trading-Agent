---
id: equity_trend_following_ema_cross
name: EMA Crossover Trend Following
type: equity
timeframe:
  - swing
  - position
indicators:
  - ema_12
  - ema_26
  - adx
market_regime:
  - trending
  - high_momentum
parameters:
  fast_ema_period: 12
  slow_ema_period: 26
  adx_period: 14
  adx_entry_threshold: 25
  adx_exit_threshold: 20
  atr_period: 14
  atr_stop_multiplier: 2.5
  trailing_stop_atr_multiplier: 3.0
  max_exits_per_run: 5
status: active
---

# EMA Crossover Trend Following

## Description

This trend-following strategy uses the classic 12/26 EMA crossover as its directional signal, filtered by the ADX indicator to ensure entry only occurs in environments with sufficient trend strength. The 12-period EMA responds quickly to price changes while the 26-period EMA provides a smoother baseline; crossovers signal shifts in intermediate-term momentum. The ADX filter eliminates whipsaw entries in choppy, directionless markets where crossover systems historically underperform. The strategy aims to capture 60-70% of major trend moves while avoiding the initial and terminal noise. It is suitable for liquid large-cap and mid-cap equities with a history of trending behavior.

## Entry Rules

- Enter long when the 12-period EMA crosses above the 26-period EMA (golden cross).
- ADX(14) must be above 25 at the time of the crossover, confirming a trending environment.
- The +DI must be above the -DI to confirm the trend direction is bullish.
- Price must be above the 200-day SMA as a regime filter (only trade with the secular trend).
- Enter at market open on the session following the confirmed crossover signal.
- Minimum average daily volume of 500,000 shares.
- Do not enter if the stock has gapped more than 5% on the signal day (reduces adverse entry risk).

## Exit Rules

- **Death cross exit:** Close the position when the 12-period EMA crosses below the 26-period EMA.
- **ADX exit:** Close if ADX(14) drops below 20, indicating the trend is losing momentum and the market is becoming directionless.
- **Trailing stop:** Once the position is profitable by at least 1x ATR(14), implement a trailing stop at 3.0x ATR(14) below the highest close since entry.
- **Initial stop:** Place an initial stop-loss at 2.5x ATR(14) below the entry price.
- If the stock gaps down more than 4% on any day, close the position at market open regardless of other signals.
- **Staggered exit pacing (`max_exits_per_run`):** When multiple positions trigger an exit on the same run, the strategy collects all candidates, sorts them by ascending absolute dollar loss (profitable exits first), and submits at most `max_exits_per_run` per run. Default is 5 — high enough that a typical day's exit basket clears in one session while still guarding against degenerate cascades (e.g. 20 simultaneous exits on a flash event). SafetyGate's `daily_loss` check is now per-batch realized P&L (rescoped 2026-05-28), so the gate itself bounds the basket's combined realized loss to `MAX_DAILY_LOSS_PCT × equity`; this parameter is a soft secondary throttle. Lower to 1-2 for very conservative pacing; raise above 5 only when you want maximum basket throughput on a known unwind day.

## Risk Management

- Position size: risk no more than 1.5% of portfolio equity per trade.
- Calculate position size as: (Portfolio Equity x 0.015) / (Entry Price - Initial Stop Price).
- Maximum of 6 concurrent trend-following positions across all sectors.
- Maximum 2 positions per sector to limit concentration risk.
- Scale in: add 50% to the position if price pulls back to the 12-EMA while ADX remains above 25 (only one add allowed per trade).
- If the portfolio drawdown exceeds 8%, halt new entries until the drawdown recovers to 4%.
- Review the crossover against weekly charts to avoid trading counter to the higher timeframe trend.
