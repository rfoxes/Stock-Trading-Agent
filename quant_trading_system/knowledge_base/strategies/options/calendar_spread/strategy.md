---
id: calendar_spread
name: "Calendar Spread (Time Decay)"
type: options
timeframe:
  - swing
indicators:
  - iv_term_structure
  - theta
  - vega
market_regime:
  - neutral
  - low_volatility
gap_types:
  - volatility_regime
parameters:
  front_month_dte: [25, 35]
  back_month_dte: [55, 70]
  strike_selection: atm
  max_debit_pct_of_stock: 3
  profit_target_pct: 25
  max_loss_pct: 50
  term_structure_threshold: 0.02
  min_front_month_iv: 20
  max_portfolio_allocation_pct: 5
status: active
---

# Calendar Spread (Time Decay)

## Description

The Calendar Spread (also known as a time spread or horizontal spread) exploits the differential rate of theta decay between a near-term short option and a longer-term long option at the same strike price. The front-month option decays faster than the back-month option, causing the spread to widen over time if the underlying remains near the strike.

The ideal setup occurs when the IV term structure is flat or inverted (front-month IV is equal to or greater than back-month IV). In this condition, you are selling relatively expensive near-term options and buying relatively cheaper longer-term options, creating a favorable vega skew. As the term structure normalizes (front-month IV decays faster or back-month IV expands), the spread benefits from both theta and vega dynamics.

This is a debit strategy with limited risk (the debit paid) and theoretically unlimited but practically capped profit potential, maximized when the underlying closes precisely at the strike on front-month expiration.

## Entry Rules

- Identify underlyings trading in a defined range with low realized volatility (historical volatility in the 20th-40th percentile).
- Check the IV term structure: front-month IV should be within 2 percentage points of back-month IV (flat) or higher than back-month IV (inverted). The term structure ratio (front IV / back IV) should be >= 0.98.
- Front-month IV should be at least 20% annualized to ensure adequate premium in the short leg.
- Sell the front-month option at 25-35 DTE. Buy the back-month option at 55-70 DTE. Both at the same ATM strike.
- Use puts for the calendar if the underlying is below the strike, calls if above (to avoid early exercise risk on ITM short calls near ex-dividend).
- The net debit should not exceed 3% of the underlying stock price. For a $100 stock, the calendar should cost no more than $3.00.
- Verify no earnings or ex-dividend dates fall between the front-month and back-month expirations, as these events will distort the term structure.
- Ensure adequate liquidity: open interest > 500 on each expiration's strike, bid-ask spread < $0.10 per leg.

## Exit Rules

- **Profit Target:** Close the calendar at 25% profit over the initial debit. If the spread was purchased for $2.00, close at $2.50.
- **Front-Month Expiration Approach:** If the front-month option has fewer than 7 DTE and the spread is profitable, close the entire position. Do not hold the short leg into expiration week due to pin risk and assignment uncertainty.
- **Underlying Moves Away:** If the underlying moves more than 1.5 standard deviations from the strike (based on the front-month implied volatility), the calendar will lose value rapidly. Close if the underlying moves more than 5% from the strike.
- **Stop Loss:** Close the position if it loses 50% of the initial debit (e.g., a $2.00 spread is now worth $1.00).
- **Term Structure Normalization:** If the term structure steepens significantly in your favor (back-month IV rises relative to front-month), consider taking early profit even below the 25% target as the vega edge has been captured.
- **Rolling the Front Month:** If the front-month option reaches 80% of max profit with more than 10 DTE remaining, consider buying it back and selling a new front-month option to create a "rolling calendar" for additional theta capture. Only roll if the new position can be established for a net credit.

## Risk Management

- **Position Sizing:** Limit each calendar to 5% of portfolio value. The maximum loss is the initial debit paid, but this can represent the full investment if the underlying moves sharply.
- **Directional Risk:** The calendar is delta-neutral at inception but becomes directionally biased as the underlying moves. If the stock rallies, the position develops negative delta (bearish). If it drops, positive delta (bullish). Close positions that drift significantly off-center.
- **Greeks Monitoring:**
  - Theta: The net theta is positive because the short front-month option decays faster than the long back-month option. Expected daily theta is approximately 0.5-1.5% of the spread's value. This is the primary profit driver.
  - Vega: The position is net long vega because the back-month option has higher vega than the front-month. An increase in overall IV benefits the position; a decrease hurts it. This is why entering during low IV environments is preferred: you want IV to increase or stay stable, not decrease further.
  - Gamma: The position is net short gamma (the short front-month has higher gamma). Large daily moves in the underlying hurt the position. This reinforces the need for a range-bound market thesis.
  - Delta: Starts near zero. Monitor daily. If net delta exceeds +/- 0.15, the underlying has moved too far from the strike.
- **Event Risk:** Avoid holding calendars through earnings or major macro events. The abrupt IV change and potential gap move will overwhelm the theta edge.
- **Maximum Concurrent Positions:** No more than 3 calendar spreads open simultaneously, ideally on uncorrelated underlyings.
