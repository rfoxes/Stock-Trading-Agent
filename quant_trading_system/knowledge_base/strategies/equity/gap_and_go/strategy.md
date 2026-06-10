---
id: equity_gap_and_go
name: Gap and Go
type: equity
timeframe:
  - intraday
indicators:
  - gap_size
  - volume
  - vwap
market_regime:
  - high_volatility
  - momentum
gap_types:
  - gap_play
parameters:
  min_gap_pct: 2.0
  max_gap_pct: 8.0
  premarket_volume_min: 500000
  premarket_volume_multiplier: 3.0
  first_candle_hold_min: 5
  stop_loss_below_premarket_low: true
  atr_period: 14
  profit_target_gap_fill_pct: 50.0
  max_position_hold_hours: 6
  relative_volume_min: 2.5
status: active
---

# Gap and Go

## Description

This intraday momentum strategy capitalizes on stocks that gap up at the open with strong pre-market volume and continue higher throughout the session. Gaps represent overnight information asymmetry being priced in, and when accompanied by heavy pre-market trading volume, they signal strong institutional or news-driven demand. The strategy enters after a brief consolidation post-open to confirm the gap will hold, then rides the momentum. The key insight is that gaps with genuine catalysts (earnings beats, upgrades, sector news) and 3x+ normal pre-market volume have a high probability of continuation rather than gap-fill in the first session. The VWAP serves as a dynamic support level after the gap.

## Entry Rules

- The stock must gap up at least 2.0% but no more than 8.0% from the prior session's close (gaps above 8% are prone to reversal and gap-fill).
- Pre-market volume must exceed 500,000 shares and be at least 3.0x the stock's average pre-market volume over the past 20 sessions.
- Wait for the first 5-minute candle to complete after the open. Enter only if the first 5-minute candle closes in the upper 50% of its range (no immediate reversal).
- Price must hold above VWAP during the first 5 minutes.
- Relative volume (compared to the time-of-day average) must be at least 2.5x.
- Identify a clear catalyst for the gap (earnings, news, upgrade). Avoid trading "mystery" gaps with no identifiable catalyst.
- Enter via a buy-stop order 1 cent above the high of the first 5-minute candle.

## Exit Rules

- **Momentum exit:** Sell if price makes a 5-minute close below VWAP at any point after entry. VWAP acts as the intraday trend line, and losing it signals the gap momentum has failed.
- **Profit target:** Take partial profits (50%) at a move equal to 50% of the initial gap size above the opening price.
- **Trailing stop:** After 50% target is hit, trail the remaining position with a stop at the low of the prior 15-minute candle.
- **Time stop:** Close all remaining positions by 3:00 PM ET. Never hold gap-and-go positions overnight.
- **Immediate stop:** If price drops below the pre-market low at any point, exit the full position immediately.
- **Weakness signal:** Exit if three consecutive 5-minute candles have lower highs within the first hour.

## Risk Management

- Position size: risk no more than 0.75% of portfolio equity per trade (elevated intraday volatility warrants smaller sizing).
- Calculate position size: (Portfolio Equity x 0.0075) / (Entry Price - Pre-market Low).
- Maximum of 2 gap-and-go trades per session (focus on the highest-conviction setups).
- Minimum stock price of $8 to ensure reasonable spreads and avoid micro-cap illiquidity.
- If the first gap trade of the day is a loss, reduce the second trade's size by 50%.
- Do not trade gap-and-go on FOMC meeting days or during the first 30 minutes after a major economic data release.
- Track daily P&L for the strategy; if the intraday loss exceeds 1.5% of portfolio equity, halt gap-and-go trading for the day.
- Avoid stocks with a float below 10 million shares unless average daily volume exceeds 5 million (small-float squeezes are unpredictable).
