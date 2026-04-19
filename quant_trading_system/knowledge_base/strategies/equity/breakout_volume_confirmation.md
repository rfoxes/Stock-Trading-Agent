---
id: equity_breakout_volume_confirmation
name: Volume-Confirmed Breakout
type: equity
timeframe:
  - swing
  - intraday
indicators:
  - atr
  - volume
  - support_resistance
market_regime:
  - breakout
  - trending
parameters:
  consolidation_min_days: 5
  consolidation_max_days: 30
  volume_breakout_multiplier: 2.0
  volume_lookback: 20
  atr_period: 14
  atr_stop_multiplier: 1.0
  profit_target_risk_multiple: 3.0
  close_above_resistance_pct: 0.5
  max_atr_range_pct: 8.0
status: active
---

# Volume-Confirmed Breakout

## Description

This strategy captures directional moves that occur when price breaks above a well-defined resistance level with confirming volume expansion. The premise is that breakouts accompanied by volume at least 2x the 20-day average represent genuine institutional participation, significantly increasing the probability that the move will follow through. Resistance levels are identified by at least 3 touches over a minimum 5-day consolidation period. The ATR is used to dynamically size stops relative to current volatility, and the prior resistance level becomes support (role reversal) as the stop reference. This strategy targets a 3:1 reward-to-risk ratio, making it profitable even with a 35% win rate.

## Entry Rules

- Identify a horizontal resistance level with at least 3 price touches over the past 5 to 30 trading days.
- Price must close above the resistance level by at least 0.5% (filters out false breakouts and intraday wicks).
- Breakout-day volume must be at least 2.0x the 20-day average volume.
- ATR(14) must be below 8% of the stock price (avoids excessively volatile names where breakouts are unreliable).
- The stock must have been in a consolidation or base pattern prior to the breakout (range contraction visible via declining ATR or Bollinger Band width).
- Enter at market open on the session following the confirmed breakout close, or intraday if the breakout is confirmed before 2:00 PM ET.
- For intraday entries, wait for a 5-minute close above resistance before entering.

## Exit Rules

- **Stop loss:** Place the stop at the prior resistance level minus 1.0x ATR(14). This uses the role-reversal principle where old resistance becomes new support.
- **Profit target:** Set the target at 3.0x the distance from entry to the stop loss (3:1 reward-to-risk).
- **Breakout failure:** Exit immediately if price closes back below the breakout resistance level on a daily basis.
- **Trailing stop:** After the position gains 1.5x the initial risk, move the stop to breakeven. After 2.0x risk, trail the stop at 1.5x ATR(14) below the highest close.
- **Volume confirmation decay:** If average volume over the 3 days post-breakout is below the 20-day average, tighten the stop to 0.5x ATR(14) as the breakout may lack conviction.

## Risk Management

- Position size: risk no more than 1.25% of portfolio equity per trade.
- Calculate position size: (Portfolio Equity x 0.0125) / (Entry Price - Stop Price).
- Maximum of 4 breakout positions simultaneously.
- Avoid trading breakouts during the final week of a quarter (window dressing effects create false breakouts).
- If the overall market (S&P 500) is below its 50-day SMA, reduce position sizes by 50% as breakouts are less reliable in weak market environments.
- Track breakout win rate by market-cap tier; if win rate drops below 30% for a tier over 20 trades, pause breakout trading in that tier.
- Never chase a breakout that has already moved more than 2x ATR above the resistance level.
