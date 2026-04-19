# Architecture

## Overview

The quantitative trading system is a multi-agent architecture built on LangGraph's `StateGraph` framework with Claude (Anthropic) as the reasoning core. Each agent operates as a specialized node within a directed graph, coordinated by a central supervisor that routes tasks based on market conditions, resolves inter-agent conflicts, and enforces risk constraints.

Key design principles:

- **Paper trading by default.** The system ships configured for Alpaca paper trading. Live trading requires explicit, multi-flag opt-in (see [safety.md](safety.md)).
- **Extensible agent network.** New trading horizons or research agents can be added by defining a sub-graph and registering it with the supervisor.
- **LLM-as-reasoner, code-as-guardrail.** Claude interprets market data, selects strategies, and writes conclusions. Hard limits (position size, drawdown, correlation) are enforced in deterministic Python code that the LLM cannot bypass.

---

## Agent Network

### SupervisorAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Role | Orchestrate all sub-agents |
| Implementation | Custom `StateGraph` (not the pre-built LangGraph supervisor utility) |

The supervisor is the entry point for every trading cycle. It:

1. Receives the current `SupervisorState` (portfolio snapshot, market regime, watchlist).
2. Decides which sub-agents to invoke based on the market regime and the current schedule window.
3. Collects proposed orders from each trading agent.
4. Resolves conflicts when multiple horizon agents propose opposing actions on the same symbol (e.g., intraday short vs. swing long).
5. Forwards the merged order set to the RiskManagerAgent for portfolio-level veto checks.
6. Submits surviving orders through the SafetyGate.

A hard cap of **10 iterations per cycle** prevents runaway loops. If the supervisor exhausts its iteration budget, it logs a warning and exits the cycle without submitting orders.

---

### IntradayTradingAgent

| Property | Value |
|---|---|
| Model | Claude Haiku |
| Bars | 1-minute and 5-minute |
| Holding period | Minutes to hours (closed by EOD) |
| Max position size | 5% of equity |
| Max stop-loss | 1% |

Strategies:

- **VWAP reversion** -- fade moves that deviate significantly from the session VWAP.
- **Opening Range Breakout (ORB)** -- trade the breakout of the first 15-minute range with volume confirmation.
- **Gap fade / gap continuation** -- classify the gap at open and trade accordingly.

Claude Haiku is chosen for speed: intraday decisions must complete within seconds, and the reasoning required is more pattern-matching than deep analysis.

---

### SwingTradingAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Bars | Daily |
| Holding period | 3-20 days |

Strategies:

- **Bollinger Band mean reversion** -- enter when price touches the outer band with confirming RSI divergence.
- **EMA crossover** -- 9/21 EMA cross with ADX filter for trend strength.
- **RSI reversal** -- oversold/overbought RSI with volume spike confirmation.
- **MACD divergence** -- price-MACD divergence as an early reversal signal.

Position sizing uses **half-Kelly criterion** to balance growth against drawdown risk.

---

### PositionTradingAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Bars | Weekly |
| Holding period | 3+ weeks |
| Max position size | 15% of equity |
| Stop-loss width | 5% |

Strategies:

- **Trend following** -- ride established trends using weekly EMA alignment and ADX confirmation.
- **Sector rotation** -- shift allocation toward sectors showing relative strength on a rolling 4-week basis.

Wider stops and larger position sizes reflect the longer horizon and reduced noise in weekly data.

---

### StrategyResearchAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Role | Discover and validate new trading strategies |

Workflow:

1. Analyze recent market data and the existing strategy knowledge base in ChromaDB.
2. Propose a new strategy hypothesis with entry/exit rules, target regime, and expected edge.
3. Hand off the hypothesis to the BacktestingAgent for quantitative validation.
4. If the backtest meets performance thresholds (Sharpe > 1.0, max drawdown < 20%, sufficient trade count), promote the strategy to the active knowledge base.
5. If the backtest fails, write a rejection conclusion to the KB explaining why.

---

### BacktestingAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Equity engine | VectorBT (`EquityBacktester`) |
| Options engine | QuantLib (`OptionsBacktester`) |

The agent wraps two backtesting engines:

- **EquityBacktester** -- built on VectorBT for vectorized, high-performance equity strategy backtesting. Produces Sharpe ratio, max drawdown, win rate, profit factor, and equity curve.
- **OptionsBacktester** -- built on QuantLib for options strategy evaluation including Greeks, P&L surfaces, and volatility modeling.

Claude interprets the raw backtest results, writes human-readable conclusions, and stores them in the knowledge base. It flags statistical concerns such as insufficient sample size, look-ahead bias risk, or overfitting to a narrow regime.

---

### KnowledgeBaseAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Vector store | ChromaDB |
| Output | ChromaDB entries + Markdown files |

The KnowledgeBaseAgent is the system's long-term memory. It:

- Handles semantic queries from other agents (e.g., "What strategies work well in high-volatility bear regimes?").
- Writes strategy conclusions, backtest results, and research findings to both ChromaDB (for vector search) and Markdown files (for human review).
- Manages two ChromaDB collections:
  - `strategies` -- canonical strategy definitions with entry/exit rules, target regime, and performance metadata.
  - `conclusions` -- timestamped research conclusions, backtest summaries, and post-trade reviews.

---

### RiskManagerAgent

| Property | Value |
|---|---|
| Model | Claude Sonnet |
| Authority | Veto power over any proposed order |

The RiskManagerAgent is the final gate before order submission. It performs four checks:

1. **Correlation check** -- if the proposed position would bring portfolio correlation above **0.7** (using predefined correlation groups), the order is rejected.
2. **Sector concentration** -- no single sector may exceed **25%** of total portfolio value. Orders that would breach this limit are rejected.
3. **Drawdown circuit breaker** -- if the portfolio drawdown from peak exceeds **15%** (`MAX_DRAWDOWN_PAUSE_PCT`), all new entries are halted. Only exit orders are permitted.
4. **Portfolio delta monitoring** -- tracks net portfolio delta for directional risk awareness. (Placeholder for future options integration.)

The RiskManagerAgent has unconditional veto power. No order reaches the broker without passing all four checks.

---

## Internal Agent Flow

Each trading agent (Intraday, Swing, Position) follows the same four-node sub-graph:

```
MarketAnalysis --> StrategySelection --> RiskEvaluation --> OrderExecution
```

### Node 1: MarketAnalysis

- Fetch OHLCV data from MarketDataService at the agent's target timeframe.
- Compute technical indicators: RSI, MACD, Bollinger Bands, ATR, VWAP, ADX, OBV.
- Claude interprets the indicator values in context: "RSI at 28 with increasing volume suggests oversold bounce potential" rather than mechanical threshold triggers.

### Node 2: StrategySelection

- Query ChromaDB for strategies tagged with the current market regime.
- Claude evaluates which strategy best fits the current market context, considering recent performance of each strategy and confluence of signals.
- Output: a selected strategy with specific entry/exit parameters.

### Node 3: RiskEvaluation

- Compute position size using **Kelly Criterion** (half-Kelly for Swing, full Kelly capped for Position).
- Check correlation of the proposed position against existing holdings.
- Set stop-loss and take-profit levels based on ATR multiples and strategy rules.
- Output: sized order request with risk parameters attached.

### Node 4: OrderExecution

- All orders pass through `SafetyGate.validate_and_submit()`. There is no alternative execution path.
- The SafetyGate enforces position size limits, daily loss limits, and the live-money gate before forwarding to the broker.
- Returns an `OrderResult` (real or simulated depending on mode).

---

## Data Flow

```
MarketDataService
    |
    |  Alpaca (primary) / yfinance (fallback)
    v
TechnicalIndicators
    |
    |  TA-Lib (primary) / pandas_ta (fallback)
    v
RegimeClassifier
    |
    |  Classifies: bull / bear / sideways / volatile
    v
Trading Agents
```

### MarketDataService

- **Primary**: Alpaca Markets API for real-time and historical bars.
- **Fallback**: yfinance for historical data when Alpaca is unavailable or rate-limited.

### TechnicalIndicators

- **Primary**: TA-Lib (C-backed, fast).
- **Fallback**: pandas_ta (pure Python, slower but no C dependency).
- Computed indicators: RSI, MACD, Bollinger Bands, ATR, VWAP, ADX, OBV, EMA (9, 21, 50, 200), SMA (50, 200).

### RegimeClassifier

Classifies the current market into one of four regimes based on three inputs:

| Input | Metric | Threshold |
|---|---|---|
| Trend direction | Slope of 200-day SMA | Positive = bullish bias, negative = bearish bias |
| Trend strength | ADX (14-period) | > 25 = trending, < 20 = range-bound |
| Volatility | Realized volatility (20-day) | > 1.5x historical median = volatile |

Regime matrix:

| Regime | Trend | ADX | Volatility |
|---|---|---|---|
| Bull | Up | > 25 | Normal |
| Bear | Down | > 25 | Normal |
| Sideways | Any | < 20 | Normal |
| Volatile | Any | Any | Elevated |

---

## State Management

### SupervisorState

```python
class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_agent: str
    market_regime: str
    portfolio_snapshot: dict
    pending_orders: list[dict]
    risk_assessment: dict
    cycle_count: int
    watchlist: list[str]
    active_strategies: list[str]
    errors: list[str]
```

### TradingAgentState

```python
class TradingAgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    agent_name: str
    market_data: dict
    signals: list[dict]
    selected_strategy: dict
    risk_check: dict
    order_requests: list[dict]
    portfolio_snapshot: dict
    watchlist: list[str]
    market_regime: str
```

Both state classes use LangGraph's message reducer pattern: `Annotated[list[BaseMessage], add_messages]`. This ensures that messages from different nodes are appended rather than overwritten, preserving the full reasoning chain for debugging and audit.

---

## Persistence

### ChromaDB (Vector Store)

- **strategies collection** -- canonical strategy definitions with metadata (regime, horizon, historical Sharpe, last backtest date). Queried by agents using semantic search to find regime-appropriate strategies.
- **conclusions collection** -- timestamped research outputs, backtest summaries, trade reviews, and lessons learned. Provides institutional memory across sessions.

### PostgreSQL (Checkpoints)

- LangGraph checkpoint persistence for crash recovery. If the system restarts mid-cycle, it resumes from the last checkpoint rather than replaying the entire cycle.
- **Fallback**: `MemorySaver` (in-memory) for local development. No persistence across restarts, but eliminates the PostgreSQL dependency for quick iteration.

### Markdown Files

- Human-readable strategy documentation auto-generated by the KnowledgeBaseAgent.
- Auto-generated conclusion reports after each research cycle.
- Serves as a secondary, version-controllable record alongside ChromaDB.

---

## Model Allocation

| Component | Model | Reason |
|---|---|---|
| Supervisor routing | Claude Sonnet | Complex multi-agent orchestration requiring nuanced decision-making about agent sequencing and conflict resolution |
| Market analysis | Claude Sonnet | Nuanced interpretation of technical indicators in context, not just threshold checks |
| Strategy selection | Claude Sonnet | Reasoning about regime-strategy fit requires weighing multiple factors and historical context |
| Risk evaluation | Claude Sonnet | Portfolio-level risk reasoning across correlated positions and sector exposures |
| Intraday analysis | Claude Haiku | Speed over depth -- intraday decisions must complete in seconds, and patterns are more mechanical |
| Order execution | Claude Haiku | Deterministic formatting of order parameters, minimal reasoning required |

---

## Scheduling (APScheduler)

All scheduled jobs use APScheduler with a `CronTrigger`. The system uses `exchange_calendars` for NYSE holiday handling -- jobs are skipped on market holidays and early-close days are handled with adjusted times.

All times are in US/Eastern.

| Job | Time (ET) | Agent / Action |
|---|---|---|
| Pre-market scan | 8:00 AM | MarketDataService refresh, RegimeClassifier update, watchlist generation |
| Intraday cycle | Every 5 minutes, 9:30 AM - 3:55 PM | IntradayTradingAgent full cycle (analysis through execution) |
| Swing daily | 3:50 PM | SwingTradingAgent daily analysis and order generation |
| Position weekly | Friday 3:50 PM | PositionTradingAgent weekly analysis and rebalancing |
| Post-market review | 4:15 PM | Daily P&L calculation, trade journaling, KnowledgeBase update |
| Weekend research | Saturday 10:00 AM | StrategyResearchAgent proposes hypotheses, BacktestingAgent validates |

### Schedule Notes

- The intraday cycle runs every 5 minutes during market hours. Each cycle is independent: if a cycle is still running when the next trigger fires, the new cycle is skipped (max_instances=1).
- The swing and position agents run at 3:50 PM (10 minutes before close) to allow time for order submission and fill before the closing auction.
- Weekend research runs on Saturday morning to avoid interfering with weekday trading operations.
- `exchange_calendars` is queried at startup and daily to determine whether the current day is a trading day. All jobs are no-ops on non-trading days (except weekend research).
