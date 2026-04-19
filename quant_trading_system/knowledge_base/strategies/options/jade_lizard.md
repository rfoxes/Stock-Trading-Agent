---
id: jade_lizard
name: "Jade Lizard"
type: options
timeframe:
  - swing
indicators:
  - iv_rank
  - delta
  - skew
market_regime:
  - neutral
  - slightly_bullish
parameters:
  short_put_delta: 0.25
  short_call_delta: 0.20
  call_spread_width: 5
  min_iv_rank: 35
  dte_range: [30, 45]
  profit_target_pct: 50
  max_loss_pct_of_portfolio: 5
  min_put_skew_premium_pct: 10
  credit_exceeds_call_width: true
status: active
---

# Jade Lizard

## Description

The Jade Lizard is a three-legged options strategy combining a short OTM put with a short OTM call spread (bear call spread) on the same underlying and expiration. The defining characteristic is that the total credit received exceeds the width of the call spread, eliminating all upside risk. If the stock rallies past the call spread, the position still profits because the credit exceeds the maximum loss on the call spread side. The only risk is to the downside, from the naked short put.

This structure exploits volatility skew: because puts typically trade at a higher implied volatility than calls (especially in equities), the short put generates disproportionate premium relative to the call spread. The strategy is ideal for stocks with pronounced put skew (at least 10% higher IV on the put side) and elevated overall IV rank (above 35).

The Jade Lizard functions as a more capital-efficient alternative to a short strangle, with the key advantage of eliminating upside risk through the long call wing. The trade-off is a lower total credit compared to a naked strangle.

## Entry Rules

- Select underlyings with IV rank above 35 and pronounced put skew (OTM put IV at least 10% higher than equidistant OTM call IV).
- Sell the OTM put at 0.25 delta, targeting 30-45 DTE.
- Sell the OTM call at 0.20 delta, same expiration as the short put.
- Buy the long call 5 points ($5) above the short call to create the bear call spread component.
- **Critical Rule:** The total credit from all three legs must exceed the width of the call spread. For a $5-wide call spread, the total credit must be at least $5.01. This ensures zero upside risk.
  - Example: Short put credit = $3.00, short call credit = $2.50, long call debit = -$0.40. Total credit = $5.10 > $5.00 call spread width. Upside risk eliminated.
- If the total credit does not exceed the call spread width, do not enter the trade. Either wait for higher IV or widen the put strike (increase delta to 0.30) to collect more premium.
- Verify no earnings, ex-dividend dates, or major catalysts within the expiration window.
- Ensure adequate liquidity on all three strikes: open interest > 200 contracts each, bid-ask spread < $0.10 per leg.
- The underlying should be trading in a stable-to-moderately-bullish trend. Avoid stocks in a pronounced downtrend (the naked put is the primary risk).

## Exit Rules

- Close the entire position at 50% of max profit. If total credit was $5.10, close when the position can be bought back for $2.55.
- Close at 21 DTE if the profit target has not been reached, to avoid elevated gamma risk on the short put.
- If the underlying drops below the short put strike by more than 3%, close the position immediately. The put is the unlimited-risk leg and should be managed aggressively.
- If the underlying rallies through the short call strike, the position is still profitable (credit > call spread width). Allow the call spread to go to max loss; the total position remains net positive. However, if the underlying continues far above the long call strike, close to free up capital.
- If assigned on the short put, take the stock and evaluate whether to transition into a covered call or wheel strategy.
- **Rolling:** If the short put is threatened, roll down and out for a net credit. Only roll if the new position maintains the critical credit-exceeds-call-width condition. Maximum of 1 roll.

## Risk Management

- **Position Sizing:** The maximum risk is on the downside: (short put strike * 100) - total credit per contract. This is equivalent to being assigned on the put minus the credit. Size the position so that max loss on put assignment does not exceed 5% of portfolio value.
- **Margin Requirement:** The margin is based on the naked short put (the call spread is defined risk). Ensure sufficient margin for the short put, typically 20% of the underlying value minus the OTM amount plus the premium.
- **Greeks Monitoring:**
  - Delta: The position starts with a small net positive delta (slightly bullish). The short put contributes positive delta (~+0.25), the short call spread contributes negative delta (~-0.15 net). Aggregate starting delta is approximately +0.10 per unit.
  - Theta: The position is strongly net positive theta, benefiting from decay on three short option legs (two short, one long). Daily theta is higher than a simple put spread or call spread alone.
  - Gamma: Net negative gamma. The naked short put has the most gamma exposure. As the underlying approaches the put strike and expiration nears, gamma risk increases significantly on the downside.
  - Vega: The position is net short vega. A broad IV expansion (e.g., market selloff) will cause mark-to-market losses, particularly on the short put. This risk is concentrated to the downside.
- **Skew Monitoring:** If put skew normalizes (put IV drops relative to call IV) after entry, the trade's edge diminishes. Consider closing early if skew inverts (calls become more expensive than puts), as this signals a potential bullish breakout that changes the risk profile.
- **Downside Hedge:** For larger positions, consider adding a long put 10-15 points below the short put to convert the jade lizard into an iron condor + extra put spread. This caps downside risk at the cost of reduced credit.
- **Concentration Limits:** No more than 2 jade lizards on correlated underlyings. The naked put component creates correlated downside risk in a broad market selloff.
