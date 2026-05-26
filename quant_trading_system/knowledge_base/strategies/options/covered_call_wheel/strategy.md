---
id: covered_call_wheel
name: "The Wheel Strategy"
type: options
timeframe:
  - swing
  - position
indicators:
  - iv_rank
  - iv_percentile
  - delta
  - support_levels
market_regime:
  - neutral
  - slightly_bullish
parameters:
  short_put_delta: 0.30
  short_call_delta: 0.30
  min_iv_rank: 30
  dte_range: [30, 45]
  profit_target_pct: 50
  max_portfolio_allocation_pct: 20
  min_stock_price: 20
  max_stock_price: 200
  min_option_volume: 500
  annualized_return_target_pct: 12
status: active
---

# The Wheel Strategy

## Description

The Wheel is a perpetual premium-harvesting strategy that cycles between selling cash-secured puts and covered calls on high-quality stocks the trader is willing to own at a discount. The strategy exploits elevated implied volatility (IV rank > 30) to collect above-average premium while maintaining a disciplined entry via put assignment and exit via call assignment. It produces steady income in neutral-to-slightly-bullish environments, with returns primarily driven by theta decay and the volatility risk premium.

The core edge comes from selling options at the 0.30 delta level, which historically corresponds to roughly a 70% probability of expiring out of the money. By targeting 30-45 DTE options, the strategy captures the steepest portion of the theta decay curve while leaving enough time to manage positions if the underlying moves adversely.

## Entry Rules

- **Cash-Secured Put Phase:**
  - Select stocks with strong fundamentals that you would be willing to hold for 6-12 months at the put strike price.
  - Confirm IV rank is above 30 (ideally above 40) to ensure adequate premium collection.
  - Sell cash-secured puts at the 0.30 delta strike, targeting 30-45 DTE.
  - The put strike should be at or below a visible technical support level.
  - Ensure the annualized return on the put premium is at least 12% (premium / strike price * 365 / DTE).
  - Verify the option has adequate liquidity: open interest > 500 contracts and bid-ask spread < 10% of the mid price.
  - Only allocate a maximum of 20% of portfolio value to any single wheel position.

- **Covered Call Phase (after put assignment):**
  - Once assigned shares via put exercise, immediately sell a covered call at 0.30 delta, 30-45 DTE.
  - Set the call strike at or above your cost basis (stock purchase price minus total put premium collected) whenever possible.
  - If IV rank is still elevated (> 40), consider selling the call at a slightly closer strike (0.35 delta) to capture additional premium.
  - If IV rank has dropped below 20, consider waiting for a volatility expansion before selling, or sell at 0.25 delta with longer DTE (45-60 days).

## Exit Rules

- **Cash-Secured Put:**
  - Close the short put at 50% of max profit to free capital and reduce gamma risk.
  - If the underlying drops through the put strike by more than 5%, consider rolling down and out (lower strike, later expiration) for a net credit.
  - If the put is assigned, transition to the covered call phase.
  - Never roll a put for a net debit.

- **Covered Call:**
  - Close the short call at 50% of max profit and re-sell at a new 30-45 DTE cycle.
  - If the underlying rallies through the call strike, allow assignment and collect the full premium plus capital gains up to the strike.
  - After call assignment, return to the cash-secured put phase.
  - If the underlying drops significantly (> 10% from entry), suspend call selling and reassess the fundamental thesis before continuing.

## Risk Management

- **Position Sizing:** Maximum 20% of total portfolio per underlying. Never run more than 5 simultaneous wheel positions to maintain diversification.
- **Delta Exposure:** Monitor net portfolio delta. The combined delta from all wheel positions should not exceed 0.50 per unit of portfolio risk.
- **Underlying Selection:** Only wheel stocks with a market cap above $10 billion, average daily volume above 2 million shares, and no pending binary events (FDA decisions, merger votes, etc.).
- **Loss Threshold:** If the assigned stock drops more than 15% below your cost basis, reassess the fundamental thesis. Close the position entirely if the thesis is broken.
- **Earnings:** Do not sell new options within 10 days of an earnings announcement unless you are comfortable with the potential gap risk. Close or roll existing positions before earnings if they are near the strike.
- **Greeks Awareness:**
  - Theta: Expect to capture roughly 2-4% of the option's value per day in the final 30 days. Theta accelerates as expiration approaches.
  - Delta: At 0.30 delta, the position has approximately 70% probability of expiring OTM. Monitor delta drift as the underlying moves.
  - Gamma: Gamma risk increases as expiration nears. Close positions at 50% profit or with more than 14 DTE remaining to avoid sharp gamma-driven P&L swings.
  - Vega: The position is short vega; a spike in IV will cause a mark-to-market loss even if the underlying hasn't moved. This is acceptable as long as the position is held to expiration or the 50% profit target.
