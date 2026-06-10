---
id: equity_pairs_trading_cointegration
name: Pairs Trading (Statistical Arbitrage)
type: equity
timeframe:
  - swing
  - position
indicators:
  - spread_zscore
  - cointegration
  - correlation
market_regime:
  - range_bound
  - mean_reverting
  - all_regimes
gap_types:
  - pairs_arbitrage
  - mean_reversion
parameters:
  zscore_entry_threshold: 2.0
  zscore_exit_threshold: 0.0
  zscore_stop_threshold: 3.5
  lookback_period: 60
  correlation_min: 0.80
  cointegration_pvalue_max: 0.05
  half_life_max_days: 30
  half_life_min_days: 3
  rebalance_hedge_ratio_days: 20
  adf_test_significance: 0.05
  max_hold_days: 30
status: active
---

# Pairs Trading (Statistical Arbitrage)

## Description

This market-neutral strategy identifies pairs of stocks with a statistically cointegrated relationship and trades the mean-reversion of their price spread. Unlike simple correlation-based pair selection, cointegration ensures a long-run equilibrium relationship exists, meaning the spread between the two stocks is stationary and will revert to its mean. The strategy uses the Engle-Granger two-step method or the Johansen test to establish cointegration, then monitors the z-score of the spread for entry signals. By being simultaneously long one stock and short the other, the strategy is hedged against broad market moves, sector risk, and systematic factors. It generates returns from the relative value convergence of the pair, making it largely independent of market direction.

## Entry Rules

- Select candidate pairs from within the same sector or industry group with a rolling 60-day Pearson correlation above 0.80.
- Run the Engle-Granger cointegration test (or Johansen test for robustness) on the pair's price series over the past 60 trading days. The p-value must be below 0.05 to confirm cointegration.
- Calculate the spread using the hedge ratio derived from OLS regression: Spread = Price_A - (Hedge_Ratio x Price_B).
- Compute the z-score of the spread: Z = (Current Spread - Mean Spread) / Std Dev of Spread, using the 60-day lookback window.
- **Long the spread:** When z-score drops below -2.0 (spread is unusually compressed), go long Stock A and short Stock B in the hedge-ratio-weighted proportion.
- **Short the spread:** When z-score rises above +2.0 (spread is unusually wide), go short Stock A and long Stock B.
- The spread's estimated half-life of mean reversion (from the Ornstein-Uhlenbeck process) must be between 3 and 30 days. Faster half-lives are noise; slower ones tie up capital.
- Both stocks must have average daily dollar volume above $20 million to ensure borrow availability and liquidity.

## Exit Rules

- **Mean-reversion target:** Close both legs of the trade when the z-score returns to 0.0 (the spread has mean-reverted).
- **Stop loss:** Close the trade if the z-score exceeds 3.5 in the direction against the position (spread divergence is accelerating rather than reverting).
- **Cointegration breakdown:** Re-test cointegration weekly. If the p-value rises above 0.10, close the position immediately as the statistical relationship may be deteriorating.
- **Time stop:** Close the trade after 30 trading days if the z-score has not reverted to 0.0. The half-life estimate suggests reversion should occur within this window; failure to do so suggests structural change.
- **Partial exit:** Close 50% of the position when the z-score reaches 0.5 (toward zero) to lock in partial profits.
- Recalculate the hedge ratio every 20 trading days and adjust leg sizes if the ratio has shifted by more than 10%.

## Risk Management

- Position size: risk no more than 2% of portfolio equity per pair trade (applied to the gross notional of both legs combined).
- Dollar-neutralize each pair: the dollar value of the long leg must equal the dollar value of the short leg at entry (adjusted by beta or hedge ratio).
- Maximum of 5 pair trades open simultaneously.
- Maximum of 2 pairs from the same sector to avoid hidden sector concentration.
- Monitor the pair's realized correlation during the trade; if it drops below 0.50, close the position as the pair relationship may be breaking down.
- Ensure short borrow is available and borrow cost is below 5% annualized before entry.
- Stress-test each pair against a 3-sigma market move to ensure the net exposure remains within acceptable bounds.
- If portfolio-level drawdown from pairs trading exceeds 5%, halt all new pairs entries until a post-mortem review is completed.
