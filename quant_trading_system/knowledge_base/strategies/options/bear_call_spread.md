---
id: bear_call_spread
name: "Bear Call Credit Spread"
type: options
timeframe:
  - swing
indicators:
  - delta
  - iv_rank
  - resistance_levels
  - trend
market_regime:
  - bearish
  - neutral
parameters:
  short_call_delta: 0.30
  spread_width: 5
  min_iv_rank: 25
  dte_range: [30, 45]
  profit_target_pct: 50
  max_loss_multiplier: 2.0
  min_credit_to_width_ratio: 0.30
  trend_confirmation_ema: 50
  max_portfolio_risk_pct: 3
status: active
---

# Bear Call Credit Spread

## Description

The Bear Call Credit Spread is a directionally bearish, defined-risk strategy that profits when the underlying stays below the short call strike through expiration. By selling a lower-strike call and buying a higher-strike call, the trader collects a net credit while capping upside risk to the spread width minus the credit received.

This strategy is the mirror image of the bull put spread, designed for bearish or neutral market conditions. The short call is placed above a technical resistance level at the 0.30 delta, providing approximately a 70% statistical probability of the trade expiring profitable. The strategy benefits from theta decay, a declining underlying, or sideways price action, making it versatile in non-bullish environments.

## Entry Rules

- Confirm the underlying is in a downtrend or at resistance: price should be below the 50-day EMA and the 50-day EMA should be sloping downward (lower than its value 10 days ago), OR price is testing a well-defined resistance level with bearish rejection signals.
- IV rank should be above 25 to ensure the credit received justifies the risk. Prefer entries when IV rank is between 30-60.
- Sell the short call at the 0.30 delta strike, targeting 30-45 DTE.
- Buy the long call 5 points ($5) above the short call strike to define maximum risk.
- The net credit must be at least 30% of the spread width (e.g., at least $1.50 on a $5-wide spread).
- Place the short call strike above a clearly identifiable resistance level (recent swing high, descending trendline, high-volume node, or declining moving average).
- Verify no earnings, ex-dividend dates, or major macro events (FOMC, CPI) fall within the expiration window.
- Minimum open interest of 300 contracts on each strike; bid-ask spread no wider than $0.08 per leg.
- Do not enter if the underlying has already dropped more than 2% in the current session (avoid selling into a momentum flush that may reverse).

## Exit Rules

- Close the spread at 50% of max profit. If you collected $1.50, close when the spread can be bought back for $0.75 or less.
- Close at 21 DTE if the profit target has not been reached, to limit gamma risk in the final weeks.
- If the underlying breaks above the resistance level used for entry by more than 1%, close the spread immediately regardless of P&L.
- Set a maximum loss at 2x the premium received. For a $1.50 credit, close if the spread reaches a $3.00 loss.
- If the underlying gaps up through the short strike overnight on news, evaluate at the open. Close if the stock opens above the long call strike.
- If early assignment occurs on the short call (common near ex-dividend dates), immediately cover the short stock position and close the long call.

## Risk Management

- **Position Sizing:** Risk no more than 3% of total portfolio per spread. Max risk = (spread width - credit) * contracts * 100. For a $5-wide spread with $1.50 credit, max risk is $350 per contract.
- **Concentration Limits:** No more than 3 bear call spreads in the same sector. Total capital at risk across all bear call spreads should not exceed 15% of portfolio.
- **Greeks Monitoring:**
  - Delta: The position is net negative delta (bearish). Starting delta is approximately -0.20 to -0.25 per contract. Monitor delta as the underlying moves; if the stock rallies toward the short strike, delta will become more negative, accelerating losses.
  - Theta: The position is net positive theta (benefits from time passing). Expected theta capture is roughly 1-2% of max profit per day at 30-45 DTE.
  - Gamma: Gamma is negative (adverse). As the underlying approaches the short call strike and expiration nears, gamma increases. Close at 21 DTE minimum to manage gamma exposure.
  - Vega: The position is net short vega. An IV expansion will increase the spread's value and cause an unrealized loss, though this effect diminishes as expiration approaches. Significant IV expansion typically accompanies selloffs (which benefit this position directionally), creating a partial natural hedge.
- **Dividend Risk:** If the underlying pays a dividend and the short call is ITM near the ex-date, there is a heightened risk of early assignment. Monitor ex-dividend dates and close or roll the position before the ex-date if the short call is ITM or near ATM.
- **Rolling Rules:** If the short call is threatened, roll up and out for a net credit. Only roll if the new short strike is above a valid resistance level. Maximum of 1 roll per position; if no credit is available for the roll, close the position.
- **Portfolio Hedge Consideration:** Bear call spreads can serve as a hedge for a long stock portfolio. If used as a hedge, sizing can be more aggressive (up to 5% of portfolio) since losses on the spread are offset by gains in the stock portfolio.
