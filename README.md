# Autonomous Quantitative Trading System

A fully autonomous, multi-agent quantitative trading system powered by Claude (Anthropic) that learns and applies trading strategies for US equities and options.

**Safety first**: The system defaults to paper trading mode. Real money execution requires two explicit flags (`REAL_MONEY_ENABLED=true` AND `REAL_MONEY_CONFIRMATION=true`).

## Architecture

```
SupervisorAgent (Claude Sonnet)
├── IntradayTradingAgent        # 1-5 min bars, minutes-hours holding
├── SwingTradingAgent           # Daily bars, 3-20 day holding
├── PositionTradingAgent        # Weekly bars, 3+ week holding
├── StrategyResearchAgent       # Discovers + evaluates new strategies
├── BacktestingAgent            # VectorBT + QuantLib backtests
├── KnowledgeBaseAgent          # ChromaDB + Markdown strategy persistence
└── RiskManagerAgent            # Portfolio-level risk with veto power

Order Flow: Trading Agent → RiskManager (veto) → SafetyGate (veto) → Broker
```

## Quick Start

```bash
# 1. Clone and set up environment (requires Python 3.11-3.13)
git clone <repo-url> && cd Stock-Trading-Agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your ALPACA_API_KEY, ALPACA_SECRET_KEY

# 3. Choose LLM provider in .env:
#    Option A (free): LLM_PROVIDER=ollama  (requires: brew install ollama && ollama pull llama3.2)
#    Option B (paid): LLM_PROVIDER=anthropic  (requires: ANTHROPIC_API_KEY)

# 4. Seed the strategy knowledge base
python main.py --seed-kb

# 5. Run a dry run (no broker calls at all)
python main.py --dry-run --once

# 6. Run a paper trading cycle
python main.py --once
```

## Commands

```bash
# Trading
python main.py --dry-run --once            # Safe test — no broker calls
python main.py --once                      # Single paper trading cycle
python main.py                             # Continuous mode with scheduler
python main.py --once --agents swing       # Run specific agent(s)

# Backtesting
python main.py --backtest mean_reversion_bollinger:SPY:2020-01-01:2024-01-01

# Knowledge Base
python main.py --seed-kb                   # Load strategies into ChromaDB

# Testing
make test                                  # All tests
make test-safety                           # Safety-critical tests only
make test-cov                              # Tests with coverage
```

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | System design, agent network, data flow, state management |
| [Strategies](docs/strategies.md) | All 18 pre-loaded strategies with entry/exit rules and parameters |
| [Safety](docs/safety.md) | Five-layer safety design, SafetyGate, risk limits |
| [Configuration](docs/configuration.md) | All environment variables, model allocation, scheduling |
| [Backtesting](docs/backtesting.md) | VectorBT equity + QuantLib options backtesting, promotion criteria |
| [Commands](docs/commands.md) | Full CLI reference and Makefile shortcuts |

## Technology Stack

| Layer | Tool |
|---|---|
| Agent Orchestration | LangGraph |
| LLM Reasoning | Claude (Anthropic API) |
| Equity Backtesting | VectorBT |
| Options Pricing | QuantLib-Python |
| Paper/Live Trading | Alpaca (alpaca-py) |
| Market Data | Alpaca Data API + yfinance |
| Knowledge Base | ChromaDB |
| Technical Analysis | TA-Lib / pandas_ta |
| Performance Analysis | QuantStats |
| Scheduling | APScheduler |
| Logging | structlog (JSON) |

## License

MIT
