---
id: equity_vwap_reversion
name: VWAP Reversion (Intraday)
type: equity
timeframe:
  - intraday
indicators:
  - vwap
  - volume_profile
  - rsi
market_regime:
  - range_bound
  - mean_reverting
gap_types:
  - mean_reversion
parameters:
  rsi_period: 9
  rsi_oversold: 35
  rsi_overbought: 65
  min_vwap_deviation_pct: 0.5
  max_vwap_deviation_pct: 2.0
  volume_profile_poc_tolerance: 0.3
  stop_loss_pct: 0.75
  session_start_buffer_min: 15
  session_end_cutoff_min: 30
  atr_period: 14
status: active
---

# VWAP Reversion (Intraday)

## Description

This intraday mean-reversion strategy exploits the tendency of price to revert to the Volume Weighted Average Price (VWAP) throughout the trading session. VWAP represents the true average price institutional participants have transacted at during the day, making it a natural attractor. When price deviates significantly below VWAP while RSI confirms oversold conditions, there is a high probability of reversion back to the VWAP. The volume profile is used to identify areas where significant institutional activity has occurred, providing additional confluence. This strategy works best on liquid stocks during range-bound intraday sessions and should be avoided during strong trending days (e.g., after major news catalysts).

## Entry Rules

- Price must be trading at least 0.5% below the session VWAP but no more than 2.0% below (extreme deviations often signal a trend day and invalidate mean-reversion).
- RSI(9) on the 5-minute chart must be below 35.
- The current price must be near a high-volume node on the intraday volume profile (within 0.3% of a Point of Control or Value Area Low).
- Do not enter during the first 15 minutes of the session (opening volatility) or the last 30 minutes (closing imbalances).
- The stock must have traded at least 50% of its average daily volume by the time of entry (ensures sufficient liquidity and participation).
- Enter with a limit order at the current ask or use a marketable limit order.
- Avoid entry on days with scheduled Fed announcements, earnings, or major macro releases.

## Exit Rules

- **Primary target:** Close the position when price touches the session VWAP.
- **Extended target:** If momentum is strong (RSI > 55), hold 50% of the position for a move to VWAP + 0.3%.
- **Stop loss:** Exit if price falls 0.75% below the entry price.
- **Time stop:** Close all positions by 3:30 PM ET regardless of profit/loss status (avoid end-of-day volatility).
- **Trend day filter:** If price makes 3 consecutive new session lows after entry, exit immediately as the session is likely trending.
- Never hold positions overnight.

## Risk Management

- Position size: risk no more than 0.5% of portfolio equity per trade (intraday trades have tighter risk budgets).
- Calculate position size: (Portfolio Equity x 0.005) / (Entry Price x 0.0075).
- Maximum of 3 VWAP reversion trades per session.
- If 2 trades hit their stop in a single session, cease trading for the remainder of the day.
- Minimum stock price of $10 to avoid excessive percentage volatility.
- Minimum average daily volume of 2 million shares.
- Monitor the broader market (SPY) for trend-day confirmation; if SPY is down more than 1.5% from the open, reduce position sizes by 50%.
- Keep a running tally of daily P&L; if the intraday drawdown exceeds 1.5% of portfolio equity, stop trading for the day.
