# Strategy Library

The system ships with 18 pre-loaded strategies (10 equity, 8 options). Each strategy is defined as a Markdown file with YAML front matter in `quant_trading_system/knowledge_base/strategies/`. They are indexed in ChromaDB for semantic search by the trading agents.

## How Strategies Work

1. **Storage**: Each strategy is a `.md` file with YAML front matter (parameters, indicators, regime) and Markdown body (entry/exit rules, risk management)
2. **Indexing**: On `--seed-kb`, the StrategyLoader reads all files and upserts them into ChromaDB
3. **Selection**: During a trading cycle, the StrategySelectionNode queries ChromaDB with the current market regime and receives ranked matches
4. **Learning**: After every backtest or trade, conclusions are written back to the KB, updating strategy metadata over time

## Strategy File Format

```yaml
---
id: strategy_slug
name: Human-Readable Name
type: equity | options
timeframe:
  - intraday | swing | position
indicators:
  - rsi
  - macd
market_regime:
  - bull | bear | sideways | volatile
parameters:
  param_name: value
status: active | testing | deprecated
---

# Strategy Name

## Description
What the strategy does and why it works.

## Entry Rules
- Specific condition 1
- Specific condition 2

## Exit Rules
- Take-profit condition
- Stop-loss condition

## Risk Management
- Position sizing rules
- Maximum exposure
```

---

## Equity Strategies (10)

### 1. Bollinger Band Mean Reversion
- **File**: `strategies/equity/mean_reversion_bollinger.md`
- **Timeframe**: Swing, Intraday
- **Regime**: Range-bound, Low volatility
- **Indicators**: Bollinger Bands (20, 2.0), RSI (14), Volume
- **Entry**: Price closes below lower BB + RSI < 30 + volume > 1.5x 20-day average
- **Exit**: Price touches middle BB (SMA 20) or RSI > 50
- **Stop**: 2% below entry
- **Logic**: When price is statistically oversold (2 standard deviations below mean) with capitulation volume, it tends to revert to the mean

### 2. EMA Crossover Trend Following
- **File**: `strategies/equity/trend_following_ema_cross.md`
- **Timeframe**: Swing, Position
- **Regime**: Bull, Trending
- **Indicators**: EMA 12, EMA 26, ADX (14)
- **Entry**: EMA 12 crosses above EMA 26 when ADX > 25 (confirming trend strength)
- **Exit**: EMA 12 crosses below EMA 26 (death cross) or ADX drops below 20
- **Stop**: 2x ATR below entry
- **Logic**: Classic trend-following system filtered by trend strength to avoid whipsaws in sideways markets

### 3. RSI Divergence
- **File**: `strategies/equity/rsi_divergence.md`
- **Timeframe**: Swing
- **Regime**: Any (reversal signal)
- **Indicators**: RSI (14), Price action (swing highs/lows)
- **Entry (Bullish)**: Price makes lower low but RSI makes higher low — momentum weakening in selloff
- **Entry (Bearish)**: Price makes higher high but RSI makes lower high — momentum weakening in rally
- **Exit**: Target at prior swing high/low or RSI reaches overbought/oversold
- **Logic**: Divergence between price and momentum often precedes reversals

### 4. VWAP Reversion (Intraday)
- **File**: `strategies/equity/vwap_reversion.md`
- **Timeframe**: Intraday
- **Regime**: Range-bound
- **Indicators**: VWAP, RSI (9), Volume profile
- **Entry**: Price 0.5-2% below VWAP with RSI(9) < 35 during first 2 hours of trading
- **Exit**: Price touches VWAP or RSI > 55
- **Stop**: 1% below entry or VWAP deviation > 2%
- **Logic**: VWAP acts as a magnet for institutional order flow; deviations tend to revert

### 5. Volume-Confirmed Breakout
- **File**: `strategies/equity/breakout_volume_confirmation.md`
- **Timeframe**: Swing, Intraday
- **Regime**: Transitioning (breakout of range)
- **Indicators**: ATR (14), Volume (20-day avg), Support/Resistance levels
- **Entry**: Price breaks above resistance with volume > 2x 20-day average
- **Exit**: Trailing stop at 1.5x ATR or first close below breakout level
- **Stop**: Prior resistance level (now support)
- **Logic**: High-volume breakouts have higher follow-through probability; low-volume breakouts often fail

### 6. MACD Histogram Momentum
- **File**: `strategies/equity/momentum_macd_histogram.md`
- **Timeframe**: Swing
- **Regime**: Trending (bull or bear)
- **Indicators**: MACD (12, 26, 9), Histogram
- **Entry**: Histogram crosses above zero with 3 consecutive rising bars
- **Exit**: Histogram crosses below zero or 3 consecutive declining bars
- **Stop**: 2% below entry
- **Logic**: The histogram measures the rate of change of momentum — rising histogram = accelerating trend

### 7. Gap and Go
- **File**: `strategies/equity/gap_and_go.md`
- **Timeframe**: Intraday
- **Regime**: Any (event-driven)
- **Indicators**: Gap size (%), Pre-market volume, VWAP
- **Entry**: Stock gaps up 2-8% with pre-market volume > 3x average, buy on first pullback to VWAP
- **Exit**: End of day (no overnight holds) or first lower high on 5-min chart
- **Stop**: Below VWAP or below pre-market low
- **Logic**: Large gaps with strong volume indicate institutional interest; the continuation pattern exploits momentum

### 8. Opening Range Breakout (ORB)
- **File**: `strategies/equity/opening_range_breakout.md`
- **Timeframe**: Intraday
- **Indicators**: First 15-minute high/low, ATR, Volume
- **Entry**: Price breaks above the 15-minute opening range high with volume > 1.5x average
- **Exit**: End of day, or target at 2x the opening range width
- **Stop**: Opening range low (for long trades)
- **Logic**: The first 15 minutes establish the battle lines for the day; a breakout with volume signals directional commitment

### 9. Pairs Trading (Statistical Arbitrage)
- **File**: `strategies/equity/pairs_trading_cointegration.md`
- **Timeframe**: Swing, Position
- **Regime**: Any (market-neutral)
- **Indicators**: Spread z-score, Cointegration test (Engle-Granger or Johansen), Correlation
- **Entry**: Z-score of the pair spread exceeds 2.0 — go long the underperformer, short the outperformer
- **Exit**: Z-score reverts to 0 (mean)
- **Stop**: Z-score exceeds 3.0 (spread blowout)
- **Logic**: Cointegrated pairs maintain a long-run equilibrium; large deviations are temporary and tend to revert

### 10. Sector Rotation Momentum
- **File**: `strategies/equity/sector_rotation_momentum.md`
- **Timeframe**: Position
- **Regime**: Any
- **Indicators**: 3-month relative strength of sector ETFs (XLK, XLF, XLV, XLE, XLI, etc.)
- **Entry**: Buy the top 3 sectors by 3-month relative strength
- **Exit**: Monthly rebalance — sell sectors that drop out of top 3
- **Logic**: Sector momentum persists over 3-12 month periods; riding winners and cutting losers captures this anomaly

---

## Options Strategies (8)

### 1. The Wheel Strategy
- **File**: `strategies/options/covered_call_wheel.md`
- **Timeframe**: Swing, Position
- **Regime**: Neutral, Slightly bullish
- **Indicators**: IV rank, Delta, Support levels
- **Setup**: Sell cash-secured puts at 0.30 delta, 30-45 DTE, on stocks you want to own
- **If Assigned**: Sell covered calls at 0.30 delta until shares are called away
- **Entry Criteria**: IV rank > 30, stock above major support, fundamentally sound
- **Exit**: Let options expire worthless (keep premium) or get assigned and repeat
- **Risk**: Willing to own the stock at the strike price; max loss = strike - premium

### 2. Iron Condor (High IV)
- **File**: `strategies/options/iron_condor_high_iv.md`
- **Timeframe**: Swing
- **Regime**: Sideways, High volatility
- **Indicators**: IV rank, IV percentile, VIX, Expected move
- **Setup**: Sell OTM put spread + OTM call spread, short strikes at 0.16 delta (1 standard deviation)
- **Entry Criteria**: IV rank > 50, VIX > 18, target 1/3 of wing width in premium
- **Exit**: Close at 50% of max profit, or close if either short strike is breached
- **Profit Target**: 50% of max credit received
- **Max Risk**: Width of wider spread minus credit received

### 3. Bull Put Credit Spread
- **File**: `strategies/options/bull_put_spread.md`
- **Timeframe**: Swing
- **Regime**: Bullish, Neutral
- **Indicators**: Delta, IV rank, Support levels, Trend
- **Setup**: Sell put at 0.30 delta, buy put $5 lower, 30-45 DTE
- **Entry Criteria**: Stock above 50 EMA (uptrend), short strike below support, IV rank > 30
- **Exit**: Close at 50% profit or if short strike breached
- **Max Risk**: Width of spread minus credit

### 4. Bear Call Credit Spread
- **File**: `strategies/options/bear_call_spread.md`
- **Timeframe**: Swing
- **Regime**: Bearish, Neutral
- **Indicators**: Delta, IV rank, Resistance levels, Trend
- **Setup**: Sell call at 0.30 delta, buy call $5 higher, 30-45 DTE
- **Entry Criteria**: Stock below 50 EMA (downtrend), short strike above resistance, IV rank > 30
- **Exit**: Close at 50% profit or if short strike breached

### 5. Pre-Earnings Long Straddle
- **File**: `strategies/options/long_straddle_earnings.md`
- **Timeframe**: Intraday, Swing
- **Regime**: Any (event-driven)
- **Indicators**: IV rank, Historical earnings move, Implied move
- **Setup**: Buy ATM call + ATM put, 5-10 days before earnings
- **Entry Criteria**: Current implied move < 1.2x average historical earnings move (IV underpriced)
- **Exit**: Close the day before earnings (capture IV expansion) or hold through if expecting large move
- **Risk**: Total premium paid (both legs); profits if stock moves more than the straddle cost

### 6. Calendar Spread
- **File**: `strategies/options/calendar_spread.md`
- **Timeframe**: Swing
- **Regime**: Neutral, Low volatility
- **Indicators**: IV term structure, Theta, Vega
- **Setup**: Sell front-month option (25-35 DTE), buy back-month option (55-70 DTE) at same strike (ATM)
- **Entry Criteria**: Term structure flat or inverted (front IV >= back IV)
- **Exit**: Close when front option reaches 50% decay or when term structure normalizes
- **Logic**: Front-month decays faster than back-month; profit from differential theta

### 7. Protective Put Collar
- **File**: `strategies/options/protective_put_collar.md`
- **Timeframe**: Position
- **Regime**: Uncertain, Bearish
- **Indicators**: Delta, Portfolio beta, VIX
- **Setup**: On existing long stock: buy 0.30 delta put + sell 0.30 delta call, 45-90 DTE
- **Entry Criteria**: VIX rising, portfolio needs downside protection, max net debit $0.50
- **Exit**: Roll or close at expiration
- **Logic**: Call premium finances the put purchase, creating a cost-efficient hedge

### 8. Jade Lizard
- **File**: `strategies/options/jade_lizard.md`
- **Timeframe**: Swing
- **Regime**: Neutral, Slightly bullish
- **Indicators**: IV rank, Delta, Skew
- **Setup**: Sell OTM put (0.25 delta) + sell OTM call spread (0.20 delta short call, $5 wide)
- **Entry Criteria**: Total credit must exceed width of call spread (eliminates upside risk), IV rank > 40
- **Exit**: Close at 50% of max profit
- **Unique Feature**: No upside risk when credit > call spread width; only risk is below the put strike

---

## Adding New Strategies

1. Create a new `.md` file in `strategies/equity/` or `strategies/options/`
2. Follow the YAML front matter format above
3. Run `python main.py --seed-kb` to load it into ChromaDB
4. The StrategyResearchAgent may also propose new strategies autonomously — these are written to the `conclusions/` directory and can be promoted to full strategies

## Strategy Lifecycle

```
Proposed (by StrategyResearchAgent or human)
    → Backtested (by BacktestingAgent)
        → Promoted (Sharpe > 1.0, DD < 20%, 100+ trades)
            → Active (used by trading agents)
                → Monitored (conclusions written after every use)
                    → Deprecated (if performance degrades)
```
