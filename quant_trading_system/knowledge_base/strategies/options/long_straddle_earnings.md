---
id: long_straddle_earnings
name: "Pre-Earnings Long Straddle"
type: options
timeframe:
  - intraday
  - swing
indicators:
  - iv_rank
  - historical_earnings_move
  - implied_move
market_regime:
  - any
parameters:
  entry_days_before_earnings: [5, 10]
  strike_selection: atm
  min_historical_vs_implied_ratio: 1.20
  earnings_lookback_quarters: 8
  max_iv_rank_at_entry: 60
  profit_target_pct: 30
  max_loss_pct: 50
  position_size_pct: 2
  min_avg_earnings_move_pct: 5
status: active
---

# Pre-Earnings Long Straddle

## Description

The Pre-Earnings Long Straddle is an event-driven volatility strategy that profits from the systematic IV expansion that occurs in the 5-10 trading days leading into an earnings announcement. Rather than betting on direction, this strategy captures the increase in option prices as implied volatility ramps into the event.

The key statistical edge comes from identifying underlyings where the options market is underpricing the expected move. When the historical average earnings move exceeds the current implied move by at least 20%, the straddle offers a positive expected value. The strategy can be executed as a pure IV play (exit before earnings) or as a full event trade (hold through earnings for a directional payoff).

This is a long premium (debit) strategy, making it fundamentally different from the other premium-selling strategies in this collection. It profits from volatility expansion and large moves, and loses from time decay and range-bound action.

## Entry Rules

- Identify stocks with upcoming earnings in the next 5-10 trading days.
- Calculate the historical average earnings move over the last 8 quarters (absolute percentage move from close before earnings to open after earnings).
- Calculate the current implied move from the ATM straddle price for the expiration nearest to earnings: implied move = straddle price / stock price * 100.
- Only enter if the historical average move is at least 1.20x the current implied move. For example, if the implied move is 5%, the historical average must be at least 6%.
- The stock should have a minimum average earnings move of 5% to ensure the absolute dollar move justifies transaction costs.
- IV rank at the time of entry should be below 60. If IV rank is already very high, much of the IV expansion has already occurred and the risk-reward is diminished.
- Buy the ATM straddle (ATM call + ATM put at the same strike nearest to the current stock price) using the nearest expiration that includes the earnings date.
- Ensure adequate liquidity: combined straddle bid-ask spread should be less than 5% of the straddle mid-price.
- Do not enter more than 10 trading days before earnings (theta decay will erode the position before the IV ramp begins).

## Exit Rules

- **Pre-Earnings Exit (IV Capture):**
  - Exit the straddle the day before earnings (or the morning of earnings day if earnings are after the close) to capture the IV expansion without taking event risk.
  - Target a 30% profit on the straddle from IV expansion alone. If achieved before the day before earnings, take profit.
  - This approach converts the trade into a pure volatility play with no binary event risk.

- **Through-Earnings Hold:**
  - If the historical-to-implied move ratio is above 1.50 (implying significant underpricing of the move), consider holding through earnings.
  - If holding through, accept that IV crush will reduce the straddle value by approximately 30-60% the morning after earnings. The actual stock move must exceed the implied move for the trade to profit.
  - Exit the morning after earnings at the open or within the first 30 minutes of trading.

- **Stop Loss:**
  - If the straddle loses 50% of its value at any point before earnings (due to the stock pinning at the strike with time decay), close the position.
  - If IV rank decreases rather than increasing after entry (unusual but possible in benign markets), close within 3 trading days to limit theta bleed.

## Risk Management

- **Position Sizing:** Limit each straddle to 2% of total portfolio value. This is a debit strategy with the potential for total loss of the premium paid.
- **Diversification:** Do not hold more than 3 earnings straddles simultaneously. Earnings seasons create correlation risk if multiple stocks react to the same macro theme.
- **Greeks Monitoring:**
  - Delta: The straddle starts delta-neutral (ATM call delta ~0.50, ATM put delta ~-0.50, net delta ~0.00). As the stock moves, delta will shift. Do not adjust delta; the strategy is designed to profit from a large move in either direction.
  - Gamma: The position is long gamma (beneficial). Gamma is highest ATM and increases as expiration approaches. This means the position will naturally accumulate delta in the direction of the move, amplifying profits from large moves.
  - Theta: The position is long premium, so theta works against you. Expect to lose approximately 2-5% of the straddle's value per day. The IV expansion must outpace theta decay for the pre-earnings exit to work. This is why entry timing (5-10 days out) is critical.
  - Vega: The position is long vega (beneficial for the IV expansion thesis). Each 1-point increase in IV will increase the straddle value by approximately (call vega + put vega). This is the primary profit driver for the pre-earnings exit.
- **Earnings Calendar:** Maintain a watchlist and screen for candidates at least 2 weeks before each earnings season. The best setups occur in weeks 2-4 of earnings season when market attention is dispersed.
- **Avoid Crowded Trades:** If a stock is widely discussed on social media or financial news as an earnings play, the IV expansion may already be priced in. Prefer less-followed names with consistent historical move patterns.
