---
id: equity_momentum_macd_histogram
name: MACD Histogram Momentum
type: equity
timeframe:
  - swing
indicators:
  - macd
  - histogram
  - signal_line
market_regime:
  - trending
  - momentum
parameters:
  macd_fast_period: 12
  macd_slow_period: 26
  macd_signal_period: 9
  min_histogram_slope_bars: 3
  adx_filter_period: 14
  adx_min_threshold: 20
  atr_period: 14
  atr_stop_multiplier: 2.0
  profit_target_atr: 3.0
  max_hold_days: 20
status: active
---

# MACD Histogram Momentum

## Description

This momentum strategy uses the MACD histogram as its primary signal, focusing on the rate of change of the MACD line relative to its signal line. The histogram represents the spread between the MACD and signal lines, and its crossing above zero indicates that bullish momentum is accelerating. More importantly, the histogram's slope (rising or falling) provides an early read on momentum shifts before the MACD line itself crosses. This strategy captures the middle portion of momentum moves, entering when acceleration is confirmed and exiting when momentum begins to decelerate. It pairs well with trend-following strategies by providing earlier exit signals.

## Entry Rules

- The MACD histogram must cross above zero from below (negative to positive transition).
- The histogram must have been increasing for at least 3 consecutive bars leading into the zero crossing, confirming building momentum rather than a stall.
- The MACD line (12,26) must be above the signal line (9-period EMA of MACD) at the time of entry.
- ADX(14) must be above 20 to confirm the stock is in a trending environment.
- Price must be above the 50-day SMA to ensure alignment with the intermediate trend.
- Enter at market open on the session following the confirmed histogram zero-cross.
- Avoid entry if the histogram zero-cross occurs on a day where the stock gapped more than 3%.

## Exit Rules

- **Primary exit:** Close the position when the MACD histogram crosses back below zero (momentum reversal).
- **Momentum decay:** Exit if the histogram posts 3 consecutive declining bars while still positive, as this signals momentum deceleration even if the histogram remains above zero.
- **Stop loss:** Place an initial stop at 2.0x ATR(14) below the entry price.
- **Profit target:** Take profit at 3.0x ATR(14) above the entry price, or trail using the histogram signal, whichever comes first.
- **Time stop:** Exit after 20 trading days if still open, as the MACD is a medium-term oscillator and signals degrade over longer holding periods.
- **Signal line divergence:** If the MACD line flattens while the histogram is narrowing, exit 50% of the position preemptively.

## Risk Management

- Position size: risk no more than 1% of portfolio equity per trade.
- Calculate position size: (Portfolio Equity x 0.01) / (Entry Price x ATR Stop Distance).
- Maximum of 5 MACD momentum trades open simultaneously.
- Avoid stocks with pending binary events (FDA decisions, legal rulings, earnings within 5 days).
- If 3 consecutive MACD trades result in losses, pause the strategy for 10 trading days and review whether market conditions have shifted to a non-trending regime.
- Correlation check: avoid holding more than 2 positions with a 60-day correlation above 0.75.
- Scale out: close 50% at 1.5x ATR profit and let the remainder ride with a trailing stop at 1.0x ATR below the highest close.
