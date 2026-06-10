---
id: equity_opening_range_breakout
name: Opening Range Breakout (ORB)
type: equity
timeframe:
  - intraday
indicators:
  - opening_range
  - atr
  - volume
market_regime:
  - trending
  - breakout
gap_types:
  - intraday_range
  - breakout
parameters:
  opening_range_minutes: 15
  atr_period: 14
  volume_confirmation_multiplier: 1.5
  stop_at_opposite_range: true
  profit_target_range_multiple: 2.0
  min_range_atr_ratio: 0.3
  max_range_atr_ratio: 0.75
  session_close_cutoff_min: 45
  min_avg_daily_volume: 1000000
status: active
---

# Opening Range Breakout (ORB)

## Description

The Opening Range Breakout strategy is a classic intraday system that trades the breakout of the price range established during the first 15 minutes of the regular trading session (9:30-9:45 AM ET). The opening range captures the initial battle between buyers and sellers as overnight orders, pre-market positions, and early institutional flows establish a balance area. A decisive break above or below this range, confirmed by volume expansion, signals the likely direction for the remainder of the session. Backtests show that the 15-minute opening range provides an optimal balance between range definition and signal timeliness. The strategy is filtered to avoid setups where the opening range is too narrow (whipsaw prone) or too wide (insufficient reward-to-risk).

## Entry Rules

- Define the opening range as the high and low of the first 15 minutes of trading (9:30-9:45 AM ET).
- **Long entry:** Buy when price breaks above the opening range high on a 1-minute close, provided the breakout candle's volume exceeds 1.5x the average 1-minute volume for that time of day.
- **Short entry:** Sell short when price breaks below the opening range low on a 1-minute close with the same volume confirmation.
- The opening range size must be between 0.3x and 0.75x the 14-day ATR. Ranges below 0.3x ATR are too tight and produce whipsaws; ranges above 0.75x ATR are too wide and compress the reward-to-risk ratio.
- Only trade stocks with average daily volume above 1 million shares.
- If price breaks out of the range but immediately reverses and closes back within the range within 2 minutes, invalidate the signal (false breakout filter).
- Prioritize stocks from a pre-screened watchlist based on relative volume and catalyst presence.

## Exit Rules

- **Stop loss:** Place the stop at the opposite end of the opening range. For long positions, the stop is at the opening range low; for shorts, at the opening range high.
- **Profit target:** Primary target is 2.0x the opening range size from the breakout level.
- **Trailing stop:** After 1.0x the opening range in profit, trail the stop at 0.5x the opening range size below the highest price (for longs) or above the lowest price (for shorts).
- **Time stop:** Close all ORB positions at least 45 minutes before the market close (by 3:15 PM ET).
- **Range recapture:** If price breaks out but then recaptures the opposite end of the opening range, exit immediately. This signals a reversal and potential move in the opposite direction.
- Never hold ORB positions overnight.

## Risk Management

- Position size: risk no more than 0.75% of portfolio equity per trade.
- Calculate position size: (Portfolio Equity x 0.0075) / (Opening Range Size x Entry Price).
- Maximum of 3 ORB trades per session.
- Only trade the first valid breakout from the opening range; do not re-enter if the first breakout fails unless price forms a new micro-range and breaks out with volume.
- On days with scheduled FOMC, CPI, or NFP releases, skip the ORB strategy entirely as the opening range is distorted by pre-data positioning.
- If two consecutive ORB trades are stopped out, do not take a third trade that day.
- Monitor sector ETF for directional alignment: trade long ORBs only if the sector ETF is also breaking above its opening range (or at minimum holding above VWAP).
- Maximum allowable daily loss on ORB trades is 1.5% of portfolio equity.
