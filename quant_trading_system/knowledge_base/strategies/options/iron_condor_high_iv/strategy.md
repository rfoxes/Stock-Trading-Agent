---
id: iron_condor_high_iv
name: "Iron Condor (High IV)"
type: options
timeframe:
  - swing
indicators:
  - iv_rank
  - iv_percentile
  - vix
  - expected_move
market_regime:
  - sideways
  - high_volatility
parameters:
  short_strike_delta: 0.16
  long_wing_width: 5
  min_iv_rank: 50
  min_iv_percentile: 50
  dte_range: [30, 45]
  premium_to_width_ratio: 0.33
  profit_target_pct: 50
  max_loss_multiplier: 2.0
  vix_min: 18
  max_portfolio_risk_pct: 5
status: active
---

# Iron Condor (High IV)

## Description

The Iron Condor is a market-neutral, defined-risk strategy that profits from time decay and implied volatility contraction in range-bound markets. By selling both an OTM put spread and an OTM call spread simultaneously, the trader collects premium from both sides while capping maximum loss at the width of the wider spread minus total premium received.

This variant specifically targets high-IV environments (IV rank > 50), where the volatility risk premium is statistically most favorable. Selling options at the 0.16 delta (approximately 1 standard deviation) places the short strikes at the boundary of the expected move, giving the position roughly a 68% probability of full profit at expiration. The key edge is the mean-reverting nature of implied volatility: when IV is elevated, it tends to contract, creating a tailwind for short vega positions.

## Entry Rules

- Confirm IV rank is above 50 and IV percentile is above 50 (indicating volatility is historically elevated for this underlying).
- Check that VIX is above 18 to ensure the broader market supports elevated premium levels.
- Sell the short put and short call at the 0.16 delta strike (approximately 1 standard deviation OTM), targeting 30-45 DTE.
- Buy protective wings 5 points (or $5 wide) beyond each short strike to define risk.
- The total credit received must be at least 1/3 (33%) of the width of the widest spread. For example, on $5-wide spreads, collect at least $1.65 in total premium.
- Verify the underlying has no earnings, ex-dividend dates, or major catalysts within the expiration window.
- The underlying should be trading within a defined range with no strong directional momentum (ADX < 25 preferred).
- Ensure adequate liquidity: bid-ask spread on each leg should be no wider than $0.10, and open interest > 200 contracts per strike.

## Exit Rules

- Close the entire iron condor at 50% of max profit. This typically occurs 15-25 days into the trade if the underlying remains range-bound.
- If one side is tested (underlying moves within 1% of a short strike), consider closing the tested side for a loss and leaving the untested side open, or rolling the tested side out in time for a credit.
- Close the position at 21 DTE if the profit target has not been reached, to avoid accelerating gamma risk.
- Set a maximum loss at 2x the premium received. For example, if you collected $1.65, close if the position reaches a $3.30 loss.
- If IV rank drops below 20 while the position is open, consider closing early even below the 50% profit target, as the volatility contraction edge has been realized.
- Never hold through expiration week unless the underlying is well-centered between the short strikes.

## Risk Management

- **Position Sizing:** Risk no more than 2-5% of total portfolio on any single iron condor. Calculate max risk as (spread width - premium received) * number of contracts.
- **Correlation Risk:** Do not run more than 3 iron condors on correlated underlyings (e.g., multiple tech stocks or multiple indices). A broad market move will cause simultaneous losses.
- **Greeks Monitoring:**
  - Delta: The net position delta should start near zero. If net delta exceeds +/- 0.15 per contract, consider adjusting by rolling the untested side closer.
  - Gamma: Gamma is the primary risk. It increases as expiration approaches and as the underlying nears a short strike. Close positions early (21+ DTE) to limit gamma exposure.
  - Theta: This is the primary profit driver. Expect to collect roughly 1-3% of max profit per day in the 30-45 DTE window. Theta accelerates after 21 DTE but so does gamma risk.
  - Vega: The position is short vega. A 1-point rise in IV will cause a mark-to-market loss of approximately (vega * 1.0) per contract. This is acceptable as the strategy assumes IV mean reversion.
- **Adjustment Rules:**
  - If the short put is breached, roll the put spread down and out for a net credit, extending DTE by 7-14 days.
  - If the short call is breached, roll the call spread up and out for a net credit.
  - Never roll for a net debit. If no credit is available, close the position and accept the loss.
  - Maximum of 2 rolls per position. After 2 rolls, close regardless of P&L.
- **Portfolio-Level:** Total notional exposure from all iron condors should not exceed 30% of portfolio value.
