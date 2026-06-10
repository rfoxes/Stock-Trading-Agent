---
id: equity_mean_reversion_bollinger
name: Bollinger Band Mean Reversion
type: equity
timeframe:
  - swing
  - intraday
indicators:
  - bollinger_bands
  - rsi
  - volume
market_regime:
  - range_bound
  - low_volatility
gap_types:
  - mean_reversion
parameters:
  bb_period: 20
  bb_std_dev: 2.0
  rsi_period: 14
  rsi_oversold: 30
  rsi_exit: 50
  volume_multiplier: 1.5
  volume_lookback: 20
  stop_loss_pct: 2.0
  max_hold_days: 10
status: active
---

# Bollinger Band Mean Reversion

## Description

This strategy exploits short-term price extremes by entering long positions when price dislocates below the lower Bollinger Band while confirming oversold conditions via RSI and above-average volume. The core thesis is that prices oscillate around a moving average and tend to revert after statistically significant deviations (2 standard deviations). The volume filter ensures that the selloff is capitulatory rather than a slow grind lower, increasing the probability of a sharp snapback. This strategy performs best in range-bound or mildly trending markets and should be avoided during strong directional trends or regime changes.

## Entry Rules

- Price must close below the lower Bollinger Band (20-period SMA, 2.0 standard deviations).
- RSI(14) must be below 30, confirming oversold momentum.
- Current session volume must exceed 1.5x the 20-day average daily volume, indicating capitulation or forced selling.
- The stock must have a minimum average daily dollar volume of $5 million to ensure liquidity.
- Avoid entry if earnings are scheduled within the next 3 trading days.
- Enter at market open on the following session or use a limit order at the prior close price.

## Exit Rules

- **Primary target:** Close the position when price touches or closes above the middle Bollinger Band (20-period SMA).
- **Momentum exit:** Close if RSI(14) crosses above 50, indicating mean reversion is underway and momentum is normalizing.
- **Stop loss:** Exit if price falls 2.0% below the entry price (hard stop, non-negotiable).
- **Time stop:** Exit after 10 trading days if neither the target nor stop has been hit, as the mean-reversion thesis weakens with time.
- Whichever exit condition triggers first takes precedence.

## Risk Management

- Position size: risk no more than 1% of total portfolio equity per trade.
- Calculate position size as: (Portfolio Equity x 0.01) / (Entry Price x 0.02).
- Maximum concurrent mean-reversion positions: 5.
- Do not add to losing positions.
- Reduce position size by 50% during earnings season (higher gap risk).
- Correlate positions: avoid holding more than 2 positions in the same sector.
- If the VIX is above 35, reduce position size by 50% due to elevated tail risk.
