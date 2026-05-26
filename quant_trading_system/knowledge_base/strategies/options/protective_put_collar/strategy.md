---
id: protective_put_collar
name: "Protective Put Collar"
type: options
timeframe:
  - position
indicators:
  - delta
  - portfolio_beta
  - vix
market_regime:
  - uncertain
  - bearish
parameters:
  put_delta: 0.30
  call_delta: 0.30
  dte_range: [45, 90]
  max_net_debit: 0.50
  vix_entry_threshold: 18
  portfolio_beta_max: 1.5
  roll_trigger_dte: 14
  max_portfolio_coverage_pct: 100
  rebalance_frequency_days: 30
status: active
---

# Protective Put Collar

## Description

The Protective Put Collar is a hedging strategy applied to existing long stock positions to limit downside risk while partially or fully financing the hedge by selling upside potential. The structure consists of three components: a long stock position, a long OTM protective put, and a short OTM covered call. The call premium offsets the put purchase cost, creating a low-cost or zero-cost hedge.

This strategy is deployed when the market outlook is uncertain or mildly bearish and the trader wants to protect unrealized gains without liquidating the stock position (which may trigger tax consequences or lose a favorable cost basis). The collar creates a defined risk/reward envelope: downside is protected below the put strike, and upside is capped at the call strike.

The collar is particularly effective when VIX is below its mean and starts rising, as the put appreciates in value both from delta and vega, while the short call benefits from the same IV increase being offset by directional losses.

## Entry Rules

- Apply to existing long stock positions where you have unrealized gains of at least 10% and want to protect profits.
- Enter when market conditions show signs of uncertainty: VIX rising above 18 and/or trending higher, breadth deterioration, or macro event risk (FOMC, elections, geopolitical tension).
- Buy a protective put at the 0.30 delta strike (approximately 10-15% below current price), targeting 45-90 DTE.
- Sell a covered call at the 0.30 delta strike (approximately 10-15% above current price) at the same expiration as the put.
- The net cost of the collar (put premium minus call premium) should be no more than $0.50 per share. Ideally the collar is established for a net credit or zero cost.
- If IV skew is pronounced (puts are significantly more expensive than calls), widen the call to 0.25 delta or narrow the put to 0.35 delta to achieve cost neutrality.
- Portfolio beta-weight the collar: if your stock has a beta of 1.3, the effective hedge ratio is 1.3x. Size the collar to cover the beta-adjusted exposure.
- Ensure adequate liquidity on both the put and call strikes: open interest > 200 contracts each, bid-ask spread < $0.15 per leg.

## Exit Rules

- **Collar Expiration Management:** Roll the entire collar forward 14 days before expiration. Buy back the short call, sell the long put, and re-establish a new collar at 45-90 DTE with updated 0.30 delta strikes.
- **Bullish Reversal:** If the market outlook turns decisively bullish (VIX drops below 14, breadth improves, uptrend resumes), close the put and the call to remove the collar and allow full upside participation. Only do this if you have captured at least some profit on the put leg from the uncertain period.
- **Stock Hits Call Strike:** If the stock rallies to the short call strike and you want to keep the shares, buy back the call (accept the loss) and reassess. If willing to sell at the call strike, allow assignment.
- **Stock Hits Put Strike:** If the stock declines to the put strike, evaluate whether to exercise the put (sell the stock at the put strike) or sell the put for intrinsic value and keep the shares. Exercising crystallizes the loss at the put strike, which was the intended floor.
- **Stock Liquidation:** If you sell the stock for any reason, simultaneously close both option legs to avoid naked exposure.

## Risk Management

- **Position Sizing:** Apply collars to positions that represent more than 10% of portfolio value, as these are the positions most in need of downside protection.
- **Cost Control:** The net debit of the collar erodes potential return. Track the annualized cost of the collar as a percentage of the stock's value. If the annualized cost exceeds 3%, the collar is too expensive; wait for better IV conditions or adjust strike deltas.
- **Greeks Monitoring:**
  - Delta: The net delta of the collared position is approximately 0.40 (long stock delta of 1.00, minus short call delta of ~0.30, plus long put delta of ~-0.30). This means the position participates in roughly 40% of the stock's moves within the collar range.
  - Theta: The position is roughly theta-neutral if the collar is established at zero cost. If a net debit was paid, theta works slightly against you as the put decays. If a net credit was received, theta works slightly in your favor.
  - Vega: The position is net long vega (long put vega > short call vega at the same delta due to skew). This means rising IV benefits the collar, which is desirable since you entered the collar expecting uncertainty and potential volatility.
  - Gamma: Net gamma is near zero but slightly positive. Large moves help the collar marginally: if the stock drops, the put's delta increases (providing more protection); if the stock rallies, the call's delta increases but the stock gains offset this.
- **Tax Considerations:** Collars with strikes too close to ATM may be considered constructive sales by the IRS, potentially triggering capital gains. Ensure the collar is sufficiently wide (both strikes at least 10% OTM) to avoid this classification. Consult a tax advisor.
- **Portfolio-Level Hedging:** For portfolios with multiple correlated positions, consider a single index collar (SPY or QQQ options) beta-weighted to the portfolio rather than individual collars on each stock. This is more capital-efficient.
- **Rebalancing:** Review and rebalance collars every 30 days or when the stock moves more than 10% from the initial entry. Adjust strikes to maintain the 0.30 delta target on both legs.
