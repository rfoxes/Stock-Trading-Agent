# Backtesting

The system includes two backtesting engines: VectorBT for equities and QuantLib for options.

## Equity Backtesting (VectorBT)

### How It Works

1. Fetch historical OHLCV data via MarketDataService (Alpaca or yfinance)
2. Compute technical indicators
3. Generate boolean entry/exit signal arrays
4. Pass to `vbt.Portfolio.from_signals()` for vectorized simulation
5. Extract metrics via QuantStats
6. Generate HTML tearsheet report

### Running a Backtest

```bash
# Format: STRATEGY_ID:SYMBOL:START_DATE:END_DATE
python main.py --backtest mean_reversion_bollinger:SPY:2020-01-01:2024-01-01
python main.py --backtest trend_following_ema_cross:AAPL:2019-01-01:2023-12-31
python main.py --backtest momentum_macd_histogram:QQQ:2018-01-01:2024-01-01
```

### Strategy IDs

Use the `id` field from the strategy YAML front matter:

| Strategy | ID |
|----------|-----|
| Bollinger Mean Reversion | `equity_mean_reversion_bollinger` |
| EMA Crossover | `equity_trend_following_ema_cross` |
| RSI Divergence | `rsi_divergence` |
| VWAP Reversion | `vwap_reversion` |
| Volume Breakout | `breakout_volume_confirmation` |
| MACD Momentum | `momentum_macd_histogram` |
| Gap and Go | `gap_and_go` |
| Opening Range Breakout | `opening_range_breakout` |
| Pairs Trading | `pairs_trading_cointegration` |
| Sector Rotation | `sector_rotation_momentum` |

### Walk-Forward Validation

The backtester supports walk-forward validation to prevent overfitting:

1. Split the data into N rolling windows (default: 5)
2. For each window, use 70% for in-sample (training) and 30% for out-of-sample (testing)
3. Generate signals on the training set, test on the out-of-sample set
4. Report average metrics across all out-of-sample windows

This prevents look-ahead bias and gives a more realistic estimate of strategy performance.

### Backtest Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `initial_cash` | `100,000` | Starting capital |
| `commission` | `0.001` | Commission per trade (0.1%) |
| `slippage` | `0.001` | Slippage per trade (0.1%) |
| `sl_stop` | None | Stop-loss as fraction (e.g., 0.02 for 2%) |
| `tp_stop` | None | Take-profit as fraction |

### Output Metrics

Each backtest produces:

| Metric | Description |
|--------|-------------|
| Total Return | Cumulative return over the period |
| Sharpe Ratio | Risk-adjusted return (annualized) |
| Sortino Ratio | Downside risk-adjusted return |
| Calmar Ratio | Return / max drawdown |
| Max Drawdown | Largest peak-to-trough decline |
| Win Rate | Percentage of profitable trades |
| Profit Factor | Gross profit / gross loss |
| Total Trades | Number of completed round-trip trades |
| Volatility | Annualized return volatility |

### HTML Reports

Backtests generate QuantStats HTML tearsheets saved to `./reports/`. These include:
- Equity curve
- Drawdown periods
- Monthly returns heatmap
- Rolling Sharpe ratio
- Return distribution
- Comparison to benchmark (if provided)

---

## Options Backtesting (QuantLib)

### How It Works

1. Define option legs (strike, expiration, type, side, quantity)
2. Fetch historical underlying prices
3. For each trading day, re-price each leg using QuantLib Black-Scholes-Merton
4. Track daily P&L mark-to-market
5. Handle expiration (ITM assignment vs OTM worthless)
6. Aggregate into portfolio-level metrics

### Pricing Engine

- **European options**: `AnalyticEuropeanEngine` with `BlackScholesMertonProcess`
- **American options**: `BinomialVanillaEngine` (200 steps) for early exercise
- **Day count**: `Actual365Fixed`
- **Vol model**: Rolling 21-day realized volatility as IV proxy (for historical backtests)

### Greeks

The options math module computes full Greeks for any option:

| Greek | Description |
|-------|-------------|
| Delta | Price sensitivity to $1 move in underlying |
| Gamma | Rate of change of delta |
| Theta | Time decay per day (negative for long options) |
| Vega | Sensitivity to 1% change in implied volatility |
| Rho | Sensitivity to 1% change in interest rates |

### Requirements

QuantLib is an optional dependency. Install with:
```bash
pip install QuantLib
```

Options backtesting tests are automatically skipped if QuantLib is not installed.

---

## Strategy Promotion Criteria

A strategy must meet ALL of the following to be promoted from testing to active:

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Sharpe ratio | > 1.0 on out-of-sample | Minimum risk-adjusted return |
| Max drawdown | < 20% | Capital preservation |
| Total trades | >= 100 | Statistical significance |
| Multi-regime | Positive in 2+ of 4 regimes | Robustness across conditions |

The four market regimes tested: bull, bear, sideways, volatile.

### Promotion Workflow

```
1. StrategyResearchAgent proposes new strategy
2. BacktestingAgent runs walk-forward backtest
3. PerformanceReporter checks promotion criteria
4. If passed → added to ChromaDB as "active"
5. If failed → conclusion written with recommendation (modify/watch/retire)
6. Claude interprets results and suggests parameter adjustments
```

---

## Programmatic Usage

```python
from quant_trading_system.backtesting.equity_backtester import EquityBacktester
from quant_trading_system.data.market_data_service import MarketDataService
from quant_trading_system.config import Settings

settings = Settings(_env_file=".env")
market_data = MarketDataService(settings)
backtester = EquityBacktester(market_data)

# Get price data
prices = market_data.get_bars("SPY", "1Day", "2020-01-01", "2024-01-01")

# Run SMA crossover backtest
result = backtester.backtest_sma_crossover(
    close=prices["Close"],
    fast_period=50,
    slow_period=200,
    initial_cash=100_000,
)

print(f"Sharpe: {result['sharpe']:.2f}")
print(f"Max DD: {result['max_drawdown']:.2%}")
print(f"Total trades: {result['total_trades']}")
```
