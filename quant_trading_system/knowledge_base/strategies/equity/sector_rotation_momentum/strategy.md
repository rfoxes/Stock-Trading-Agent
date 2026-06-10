---
id: equity_sector_rotation_momentum
name: Sector Rotation Momentum
type: equity
timeframe:
  - position
indicators:
  - relative_strength
  - sector_etfs
  - momentum
market_regime:
  - trending
  - rotational
gap_types:
  - sector_rotation
  - trending
parameters:
  momentum_lookback_months: 3
  top_n_sectors: 3
  rebalance_frequency: monthly
  sector_universe_size: 11
  min_momentum_pct: 0.0
  sma_filter_period: 200
  cash_threshold_pct: -5.0
  equal_weight: true
  skip_recent_month: false
  max_sector_allocation_pct: 40.0
status: active
---

# Sector Rotation Momentum

## Description

This position-level strategy systematically rotates into the strongest-performing sectors based on trailing 3-month relative strength, rebalancing monthly. The strategy is grounded in the well-documented cross-sectional momentum anomaly: sectors that have outperformed recently tend to continue outperforming over the next 1-3 months due to institutional herding, slow information diffusion, and behavioral biases. The universe consists of the 11 GICS sector ETFs (XLK, XLF, XLV, XLE, XLY, XLP, XLI, XLB, XLU, XLRE, XLC), and the portfolio holds the top 3 sectors by trailing return equally weighted. A 200-day SMA regime filter prevents allocation to sectors in downtrends, with the freed capital moved to cash or short-term treasuries. This approach delivers market-beating returns with moderate turnover and avoids the stock-specific risk of individual equity selection.

## Entry Rules

- At each monthly rebalance (first trading day of each month), calculate the trailing 3-month (63 trading days) total return for each of the 11 GICS sector ETFs.
- Rank all 11 sectors by their 3-month total return from highest to lowest.
- Select the top 3 sectors by ranking.
- A sector must have a 3-month return above 0% (absolute momentum filter). If fewer than 3 sectors meet this criterion, allocate the remaining capital to cash (money market or SHY).
- Each selected sector must be trading above its 200-day SMA (regime filter). If a top-3 sector is below its 200-day SMA, skip it and move to the next-ranked sector that is above its 200-day SMA.
- If no sectors pass both filters, move the entire portfolio to cash.
- Allocate equally across the selected sectors (e.g., 33.3% each for 3 sectors).
- Execute rebalance trades at market open on the rebalance date using market orders.

## Exit Rules

- **Monthly rebalance:** At each monthly rebalance, re-rank all sectors. Sell any held sector that is no longer in the top 3 and buy the new top 3 sector(s).
- **Regime filter exit:** If a held sector drops below its 200-day SMA mid-month, sell that sector position at the next open and reallocate to cash. Do not replace it with another sector until the next regular rebalance.
- **Crash filter:** If the S&P 500 drops more than 5% in any rolling 5-day period, move the entire portfolio to cash and skip the next monthly rebalance. Resume at the following month's rebalance.
- **No partial exits:** Sectors are either fully held at their target weight or fully exited.

## Risk Management

- Position size: equal weight across selected sectors (33.3% each for 3 sectors, or up to 50% each for 2 sectors if one is filtered out).
- No single sector allocation may exceed 40% of the portfolio.
- Expected monthly turnover is 1-2 sectors (low turnover keeps transaction costs manageable).
- Use sector ETFs rather than individual stocks to eliminate stock-specific risk and ensure liquidity.
- Monitor sector concentration: if the top 3 sectors are all from cyclical groups (XLK, XLY, XLI, XLF, XLE, XLB), limit cyclical exposure to 2 of the 3 positions and substitute the 3rd with the highest-ranked defensive sector (XLV, XLP, XLU, XLRE, XLC).
- Maximum portfolio drawdown tolerance: 15%. If the portfolio drawdown exceeds 15% from peak, move to 100% cash for one full month before resuming.
- Track rolling 12-month performance relative to SPY. If underperformance exceeds 10%, conduct a strategy review to determine whether the momentum factor is in a drawdown period or the strategy needs adjustment.
- Annual review: re-validate the 3-month lookback period by testing 1, 3, 6, and 12-month lookbacks on out-of-sample data. Adjust if a different lookback consistently outperforms.
