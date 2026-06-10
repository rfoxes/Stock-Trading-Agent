---
id: equity_rsi_divergence
name: RSI Divergence
type: equity
timeframe:
  - swing
indicators:
  - rsi
  - price_action
market_regime:
  - range_bound
  - trend_exhaustion
gap_types:
  - divergence
  - mean_reversion
parameters:
  rsi_period: 14
  divergence_lookback: 20
  min_price_swing_pct: 3.0
  rsi_min_difference: 5
  profit_target_atr: 2.0
  stop_loss_atr: 1.5
  atr_period: 14
  max_hold_days: 15
status: active
---

# RSI Divergence

## Description

This strategy detects divergences between price action and the RSI oscillator to identify exhaustion points in prevailing trends. A bullish divergence occurs when price prints a lower low while RSI forms a higher low, signaling that selling momentum is weakening even as price continues to decline. Conversely, a bearish divergence occurs when price makes a higher high but RSI makes a lower high, indicating fading buying pressure. Divergences are reliable reversal signals when they occur at extreme RSI levels and are among the highest-probability setups in technical analysis. The strategy works best at the tail end of established trends and in range-bound markets where mean-reversion dynamics dominate.

## Entry Rules

- **Bullish divergence (long entry):** Price must print a lower low compared to a prior swing low within the past 20 bars, while RSI(14) prints a higher low (minimum 5-point RSI difference between the two lows).
- The prior and current price swing lows must be separated by at least 3% in price to qualify as a meaningful divergence.
- RSI at the second (current) low should be below 40 to ensure the divergence is occurring in a region where reversals are probable.
- Confirm the divergence with a bullish candlestick pattern (hammer, bullish engulfing, or morning star) on the signal bar or the bar immediately following.
- Enter on a break above the high of the confirmation candle.
- Avoid entry if the stock is within 5 days of an earnings announcement.

## Exit Rules

- **Profit target:** Exit at 2.0x ATR(14) above the entry price.
- **Bearish divergence exit:** Close longs if a bearish divergence forms (price higher high, RSI lower high) after entry.
- **Stop loss:** Exit at 1.5x ATR(14) below the entry price, placed at the time of entry.
- **Time stop:** Close the position after 15 trading days if neither the target nor the stop has been triggered.
- **RSI overbought exit:** If RSI(14) exceeds 70 during the trade, tighten the stop to 0.5x ATR(14) below the current price.

## Risk Management

- Position size: risk no more than 1% of portfolio equity per trade.
- Calculate position size: (Portfolio Equity x 0.01) / (Entry Price - Stop Price).
- Maximum of 4 divergence trades open simultaneously.
- Do not trade divergences in stocks with ADX > 40, as strong trends can override divergence signals (trend overpowers the signal).
- Only trade stocks with average daily dollar volume above $10 million.
- If two consecutive divergence trades result in losses, pause the strategy for 5 trading days before re-entering.
- Keep a log of divergence reliability by sector; reduce size in sectors with historical win rates below 45%.
