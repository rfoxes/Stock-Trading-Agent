---
id: bull_put_spread
name: "Bull Put Credit Spread"
type: options
timeframe:
  - swing
indicators:
  - delta
  - iv_rank
  - support_levels
  - trend
market_regime:
  - bullish
  - neutral
parameters:
  short_put_delta: 0.30
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

# Bull Put Credit Spread

## Description

The Bull Put Credit Spread is a directionally biased, defined-risk strategy that profits when the underlying stays above the short put strike through expiration. By selling a higher-strike put and buying a lower-strike put, the trader collects a net credit while limiting downside risk to the spread width minus the credit received.

This strategy combines directional bias (bullish or neutral) with premium selling. The short put is placed below a technical support level at the 0.30 delta, providing a statistical buffer of approximately 1 standard deviation of downside. The strategy benefits from both theta decay and the underlying moving higher or staying flat, giving it a broader profit zone than a pure directional trade.

## Entry Rules

- Confirm the underlying is in an established uptrend: price should be above the 50-day EMA and the 50-day EMA should be sloping upward (higher than its value 10 days ago).
- IV rank should be above 25 to ensure the credit received justifies the risk. Prefer entries when IV rank is between 30-60.
- Sell the short put at the 0.30 delta strike, targeting 30-45 DTE.
- Buy the long put 5 points ($5) below the short put strike to define maximum risk.
- The net credit must be at least 30% of the spread width (e.g., at least $1.50 on a $5-wide spread).
- Place the short put strike below a clearly identifiable support level (recent swing low, moving average confluence, or high-volume node on the volume profile).
- Verify no earnings, ex-dividend dates, or major macro events (FOMC, CPI) fall within the expiration window.
- Minimum open interest of 300 contracts on each strike; bid-ask spread no wider than $0.08 per leg.
- Do not enter if the underlying has already moved more than 2% in the current session (avoid chasing momentum).

## Exit Rules

- Close the spread at 50% of max profit. If you collected $1.50, close when the spread can be bought back for $0.75 or less.
- Close at 21 DTE if the profit target has not been reached, to limit gamma risk in the final weeks.
- If the underlying breaks below the support level used for entry by more than 1%, close the spread immediately regardless of P&L.
- Set a maximum loss at 2x the premium received. For a $1.50 credit, close if the spread reaches a $3.00 loss.
- If the underlying gaps down through the short strike overnight, evaluate at the open. Close if the stock opens below the long put strike.
- If assigned on the short put (early assignment), immediately sell the shares and close the long put, or convert to a wheel strategy if the stock meets wheel criteria.

## Risk Management

- **Position Sizing:** Risk no more than 3% of total portfolio per spread. Max risk = (spread width - credit) * contracts * 100. For example, a $5-wide spread with $1.50 credit has $3.50 max risk per contract ($350).
- **Concentration Limits:** No more than 3 bull put spreads in the same sector. Total capital at risk across all bull put spreads should not exceed 15% of portfolio.
- **Greeks Monitoring:**
  - Delta: The position is net positive delta (bullish). Starting delta is approximately +0.20 to +0.25 per contract after accounting for the long put. Monitor delta drift as the underlying moves.
  - Theta: The position is net positive theta (benefits from time passing). Expected theta capture is roughly 1-2% of max profit per day at 30-45 DTE.
  - Gamma: Gamma is negative (adverse). As the underlying approaches the short strike and expiration nears, gamma increases rapidly. This is the primary reason to close at 21 DTE if the trade is not profitable.
  - Vega: The position is net short vega. An IV spike (e.g., from a market selloff) will increase the spread's value and cause a mark-to-market loss. This is partially offset by the long put's vega.
- **Correlation with Portfolio:** If you hold a long stock portfolio, bull put spreads add to your downside risk. Size accordingly and consider reducing stock exposure when running multiple spreads.
- **Rolling Rules:** If the short put is threatened, consider rolling down and out for a net credit. Only roll if the new position still places the short strike below a support level. Maximum of 1 roll per position.
