# Commands Reference

## CLI (`main.py`)

### Trading

```bash
# Dry run — run the full pipeline but don't submit any orders
# Safest way to test. No broker calls whatsoever.
python main.py --dry-run --once

# Dry run continuous — keeps running on schedule, still no broker calls
python main.py --dry-run

# Single paper trading cycle — runs one full supervisor cycle
python main.py --once

# Continuous paper trading — APScheduler manages market hours
python main.py

# Run specific agents only
python main.py --once --agents swing
python main.py --once --agents intraday,swing
python main.py --once --agents swing,position

# Override log level
python main.py --dry-run --once --log-level DEBUG
```

### Backtesting

```bash
# Format: --backtest STRATEGY_ID:SYMBOL:START_DATE:END_DATE
python main.py --backtest mean_reversion_bollinger:SPY:2020-01-01:2024-01-01
python main.py --backtest trend_following_ema_cross:AAPL:2019-01-01:2023-12-31
python main.py --backtest momentum_macd_histogram:QQQ:2018-01-01:2024-01-01
python main.py --backtest iron_condor_high_iv:SPY:2021-01-01:2024-01-01
```

HTML reports are saved to `./reports/`.

### Knowledge Base

```bash
# Seed ChromaDB with all 18 strategy files (run once after install)
python main.py --seed-kb
```

### All CLI Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | No broker calls. Full pipeline runs, orders are simulated. |
| `--once` | Run one cycle and exit (vs continuous scheduler mode) |
| `--agents AGENTS` | Comma-separated agents to activate: `intraday`, `swing`, `position` |
| `--log-level LEVEL` | Override log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `--seed-kb` | Load strategy files into ChromaDB and exit |
| `--backtest SPEC` | Run backtest with format `STRATEGY_ID:SYMBOL:START:END` |

---

## Makefile

```bash
# Install
make install          # pip install -r requirements.txt
make install-dev      # Install with dev tools (ruff, mypy, pytest)
make install-talib    # Install TA-Lib C library (macOS/Linux)

# Testing
make test             # Run all tests: pytest tests/ -v
make test-safety      # Safety-critical tests only (safety gate + config)
make test-cov         # Run with coverage report

# Code Quality
make lint             # Run ruff linter
make format           # Auto-format with ruff
make typecheck        # Run mypy type checker

# Run
make run              # python main.py (continuous mode)
make dry-run          # python main.py --dry-run --once

# Infrastructure
make docker-up        # Start PostgreSQL via Docker Compose
make docker-down      # Stop PostgreSQL
```

---

## Typical Workflows

### First-Time Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys
python main.py --seed-kb
python main.py --dry-run --once
```

### Daily Development

```bash
source .venv/bin/activate
make test                    # Verify nothing is broken
python main.py --dry-run --once --log-level DEBUG   # Test changes
```

### Running Backtests

```bash
# Test a strategy across different symbols
python main.py --backtest mean_reversion_bollinger:SPY:2020-01-01:2024-01-01
python main.py --backtest mean_reversion_bollinger:QQQ:2020-01-01:2024-01-01
python main.py --backtest mean_reversion_bollinger:AAPL:2020-01-01:2024-01-01
# Check reports/ directory for HTML tearsheets
```

### Paper Trading

```bash
# Single cycle (test during market hours)
python main.py --once

# Continuous (leave running during trading day)
python main.py
# Press Ctrl+C to stop
```

### Going Live (when ready)

```bash
# 1. Get live Alpaca API keys (not paper keys)
# 2. Update .env:
#    ALPACA_API_KEY=<live key>
#    ALPACA_SECRET_KEY=<live secret>
#    ALPACA_PAPER=false
#    REAL_MONEY_ENABLED=true
#    REAL_MONEY_CONFIRMATION=true
# 3. Use postgres checkpointer for crash recovery:
#    LANGGRAPH_CHECKPOINTER=postgres
#    make docker-up
# 4. Start with a single agent first:
python main.py --once --agents swing
```
