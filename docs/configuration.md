# Configuration Reference

All configuration is via environment variables. Copy `.env.example` to `.env` and edit.

## LLM Provider

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `anthropic` | `"anthropic"` for Claude (paid) or `"ollama"` for local models (free) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL (only when `LLM_PROVIDER=ollama`) |
| `OLLAMA_MODEL` | _(auto)_ | Ollama model name (e.g. `llama3.2`, `mistral`, `qwen2.5`). If empty, auto-maps from Claude model names |

### Using Ollama (free, local)

```bash
# 1. Install Ollama
brew install ollama
brew services start ollama

# 2. Pull a model
ollama pull llama3.2

# 3. Set in .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

When `LLM_PROVIDER=ollama`, the `ANTHROPIC_API_KEY` is not needed.

### Auto-mapping (when OLLAMA_MODEL is empty)

If you don't set `OLLAMA_MODEL`, Claude model names are auto-mapped:
- `claude-*-haiku-*` → `llama3.2` (fast, small)
- `claude-*-sonnet-*` → `llama3.1` (capable)
- `claude-*-opus-*` → `llama3.1:70b` (large)

## API Keys

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Only when `LLM_PROVIDER=anthropic` | Anthropic API key for Claude |
| `ALPACA_API_KEY` | Yes | Alpaca trading API key (paper or live) |
| `ALPACA_SECRET_KEY` | Yes | Alpaca trading secret key |

Get Alpaca keys at [alpaca.markets](https://alpaca.markets) (paper trading is free).
Get Anthropic key at [console.anthropic.com](https://console.anthropic.com).

## Safety Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ALPACA_PAPER` | `true` | Paper trading mode. **Must be `true` unless both flags below are `true`** |
| `REAL_MONEY_ENABLED` | `false` | First safety flag for live trading |
| `REAL_MONEY_CONFIRMATION` | `false` | Second safety flag for live trading |
| `DRY_RUN` | `false` | Run full pipeline without any broker calls at all |

To enable live trading, you must set ALL THREE:
```bash
ALPACA_PAPER=false
REAL_MONEY_ENABLED=true
REAL_MONEY_CONFIRMATION=true
```

If `ALPACA_PAPER=false` without both flags, the system raises a `ValueError` at startup and refuses to run.

## Risk Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_POSITION_SIZE_PCT` | `0.10` | Max single position as fraction of portfolio (10%) |
| `MAX_SECTOR_CONCENTRATION_PCT` | `0.25` | Max exposure in any one sector (25%) |
| `MAX_DAILY_LOSS_PCT` | `0.02` | Max daily loss before halting new orders (2%) |
| `MAX_DRAWDOWN_PAUSE_PCT` | `0.15` | Max portfolio drawdown before circuit breaker (15%) |
| `MAX_CONCURRENT_POSITIONS` | `20` | Max number of simultaneous positions |
| `PAPER_PORTFOLIO_SIZE` | `100000` | Starting paper trading portfolio value ($) |
| `RESTRICTED_SYMBOLS` | `[]` | Comma-separated list of symbols to block |

## Model Allocation

| Variable | Default | Used By |
|----------|---------|---------|
| `SUPERVISOR_MODEL` | `claude-sonnet-4-5-20250514` | Supervisor routing and conflict resolution |
| `ANALYSIS_MODEL` | `claude-sonnet-4-5-20250514` | Market analysis, strategy selection, backtesting interpretation |
| `ROUTING_MODEL` | `claude-haiku-4-5-20251001` | Fast routing decisions, intraday agent |
| `EXECUTION_MODEL` | `claude-haiku-4-5-20251001` | Order execution (minimal reasoning needed) |

### Cost Optimization

The system uses a tiered model allocation to balance quality and cost:
- **Sonnet** for tasks requiring nuanced reasoning (strategy selection, risk evaluation, result interpretation)
- **Haiku** for fast, deterministic tasks (routing, execution, intraday analysis)

To reduce costs during testing, you can set all models to Haiku:
```bash
SUPERVISOR_MODEL=claude-haiku-4-5-20251001
ANALYSIS_MODEL=claude-haiku-4-5-20251001
```

## Scheduling

| Variable | Default | Description |
|----------|---------|-------------|
| `INTRADAY_INTERVAL_MINUTES` | `5` | How often the intraday agent runs during market hours |
| `SWING_REBALANCE_TIME` | `15:50` | When the swing agent runs daily (ET, 24h format) |
| `POSITION_REBALANCE_DAY` | `friday` | Day of week for position agent |
| `STRATEGY_RESEARCH_INTERVAL_DAYS` | `7` | Days between strategy research cycles |

All times are in US/Eastern timezone. The scheduler uses `exchange_calendars` for NYSE holiday handling.

## Watchlist

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_WATCHLIST` | `SPY,QQQ,AAPL,MSFT,GOOGL,AMZN,NVDA,META,TSLA,JPM` | Comma-separated symbols to monitor |

## Infrastructure

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://trading:trading@localhost:5432/trading_system` | PostgreSQL connection string |
| `LANGGRAPH_CHECKPOINTER` | `memory` | `memory` for development, `postgres` for production |
| `CHROMA_PERSIST_DIR` | `./chroma_data` | Directory for ChromaDB persistent storage |

### Memory vs PostgreSQL Checkpointer

- **memory**: No external dependencies. State is lost when the process stops. Good for development and testing.
- **postgres**: Requires PostgreSQL. Enables crash recovery, audit trail, and state persistence across restarts. Use `make docker-up` to start PostgreSQL.

## Logging

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Python log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `LOG_FORMAT` | `console` | `console` for human-readable, `json` for machine-parseable |

For production, use:
```bash
LOG_FORMAT=json
LOG_LEVEL=INFO
```

For debugging:
```bash
LOG_FORMAT=console
LOG_LEVEL=DEBUG
```
