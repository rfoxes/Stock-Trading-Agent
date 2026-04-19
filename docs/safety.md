# Safety

## Overview

The system uses a defense-in-depth approach to prevent accidental real-money trading. Five independent layers ensure that no single misconfiguration, code bug, or LLM hallucination can result in unintended live trades. Each layer is designed to fail safe: if any layer encounters an ambiguous state, it blocks the operation.

---

## Layer 1: Configuration Validation

The application configuration is defined as a Pydantic `Settings` class with a `model_validator` that enforces safe defaults at startup. The system cannot start with an unsafe configuration.

### Rules

- `ALPACA_PAPER` defaults to `true`. Setting it to `false` signals intent to use a live brokerage account.
- If `ALPACA_PAPER=false`, the validator requires **both** `REAL_MONEY_ENABLED=true` **and** `REAL_MONEY_CONFIRMATION=true`. If either flag is missing or false, a `ValueError` is raised and the application refuses to start.
- Both `REAL_MONEY_ENABLED` and `REAL_MONEY_CONFIRMATION` default to `false`.

### Effect

```
ALPACA_PAPER=true  (default)  --> Paper trading. System starts normally.
ALPACA_PAPER=false, flags missing --> ValueError. System does not start.
ALPACA_PAPER=false, one flag set  --> ValueError. System does not start.
ALPACA_PAPER=false, both flags set --> Live trading permitted. System starts with warnings.
```

This means a fresh deployment with no environment variables configured will always default to paper trading. Enabling live trading requires deliberate, explicit action in two separate configuration values.

---

## Layer 2: SafetyGate Middleware

The `SafetyGate` class is the sole pathway to the broker. Every order in the system passes through `SafetyGate.validate_and_submit()`. There is no alternative execution path -- agents cannot call the broker directly.

### Validation Sequence

When `validate_and_submit()` is called, it runs the following checks in order. The first failure stops execution and returns a rejection.

#### Check 1: Dry-Run Gate

If `DRY_RUN=true`, the order is logged with full details and a simulated `OrderResult` is returned. The broker is never contacted. No further checks are evaluated.

#### Check 2: Live Money Gate

If the system is not in dry-run mode and is configured for live trading (`ALPACA_PAPER=false`), both `REAL_MONEY_ENABLED` and `REAL_MONEY_CONFIRMATION` must be `true`. If either is missing, a `SafetyError` is raised. This is a redundant check with Layer 1 -- it exists to catch any scenario where configuration could be modified after startup.

#### Check 3: Restricted Symbols

The order symbol is checked against a configurable blacklist (`RESTRICTED_SYMBOLS`). If the symbol is restricted, the order is rejected. This prevents trading in symbols that are known to be problematic (e.g., halted securities, securities under regulatory review, or symbols the operator wants to exclude).

#### Check 4: Position Size Limit

The order's dollar value (price x quantity) is divided by total account equity. If this ratio exceeds `MAX_POSITION_SIZE_PCT` (default: **10%**), the order is rejected.

```
order_value / account_equity > MAX_POSITION_SIZE_PCT  -->  REJECTED
```

#### Check 5: Daily Loss Limit

The system tracks cumulative daily losses (realized + unrealized). If total losses for the current trading day exceed `MAX_DAILY_LOSS_PCT` (default: **2%**) of account equity, the order is rejected.

```
(realized_losses + unrealized_losses) / account_equity > MAX_DAILY_LOSS_PCT  -->  REJECTED
```

#### Check 6: Maximum Concurrent Positions

If the account already holds `MAX_CONCURRENT_POSITIONS` (default: **20**) open positions, new buy orders are rejected. Sell orders are always permitted regardless of this limit -- the system must always be able to reduce exposure.

### Order Submission

If all checks pass, the order is forwarded to the broker API. The result is logged and returned to the calling agent.

---

## Layer 3: RiskManagerAgent

The RiskManagerAgent operates at the portfolio level, evaluating proposed orders in the context of existing holdings. It has unconditional veto power.

### Check 1: Correlation Check

Proposed positions are evaluated against existing holdings using predefined correlation groups. If adding the position would bring the portfolio's weighted average pairwise correlation above **0.7**, the order is vetoed.

Correlation groups are maintained as a static mapping (e.g., AAPL/MSFT/GOOGL in "mega-cap tech") rather than computed dynamically, ensuring deterministic behavior without requiring a correlation matrix computation on every order.

### Check 2: Sector Concentration

No single sector may exceed **25%** of total portfolio value. If a proposed order would push a sector's allocation above this threshold, the order is vetoed.

Sector assignments are maintained as a static mapping updated periodically, not queried in real-time.

### Check 3: Drawdown Circuit Breaker

If the portfolio's drawdown from its peak equity value exceeds `MAX_DRAWDOWN_PAUSE_PCT` (default: **15%**), the circuit breaker activates:

- All new entry orders are blocked.
- Exit orders (sells, stop-loss triggers) are still permitted.
- The circuit breaker remains active until drawdown recovers below the threshold or is manually reset.

This prevents the system from compounding losses during adverse market conditions.

### Check 4: Portfolio Delta Monitoring

The system tracks net portfolio delta (directional exposure). This is currently a monitoring-only check that logs warnings when delta exceeds configurable thresholds. It is a placeholder for future options integration where delta-neutral portfolio management will be enforced.

---

## Layer 4: Dry-Run Mode

Dry-run mode provides a complete simulation of the trading pipeline without any broker interaction.

### Activation

Set the `--dry-run` CLI flag or `DRY_RUN=true` environment variable.

### Behavior

- The full pipeline executes: market data fetch, technical analysis, strategy selection, risk evaluation, and order generation.
- At the SafetyGate, instead of calling the broker, a simulated `OrderResult` is constructed and returned.
- **No broker calls whatsoever** -- `get_account()`, `get_positions()`, and `submit_order()` are all skipped. Market data is still fetched from public APIs (Alpaca data API or yfinance), but no authenticated trading endpoints are contacted.
- All agent reasoning, strategy selection, and risk evaluation logic runs identically to production mode.

### Use Cases

- Testing agent logic and prompt changes without even paper-money risk.
- Validating the full pipeline after code changes before deploying to paper trading.
- Running the system in CI/CD for integration tests.
- Demonstrating the system to stakeholders.

---

## Layer 5: Structured Audit Logging

Every decision point in the system is logged using `structlog` in JSON format, creating a complete audit trail.

### Logged Fields

Every order-related log entry includes:

| Field | Description |
|---|---|
| `agent_name` | Which agent generated the order (e.g., `intraday`, `swing`) |
| `strategy_name` | The strategy that produced the signal (e.g., `vwap_reversion`) |
| `symbol` | The ticker symbol |
| `side` | `buy` or `sell` |
| `qty` | Number of shares |
| `reasoning` | Claude's natural-language explanation for the trade |
| `safety_checks_passed` | List of SafetyGate checks that passed |
| `safety_checks_failed` | List of SafetyGate checks that failed (if any) |
| `cycle_id` | Unique identifier for the trading cycle |
| `timestamp` | ISO 8601 timestamp |

### LLM Call Logging

A custom LangChain callback handler logs metadata for every Claude API call:

| Field | Description |
|---|---|
| `model` | The model name (e.g., `claude-sonnet-4-20250514`) |
| `input_tokens` | Number of input tokens |
| `output_tokens` | Number of output tokens |
| `latency_ms` | Round-trip latency in milliseconds |
| `agent_name` | Which agent made the call |
| `node_name` | Which graph node made the call |

This enables cost tracking, latency monitoring, and debugging of LLM behavior across the agent network.

---

## Risk Limits Reference

All risk limits are configurable via environment variables. Defaults are chosen to be conservative.

| Environment Variable | Default | Description |
|---|---|---|
| `ALPACA_PAPER` | `true` | Use Alpaca paper trading endpoint |
| `REAL_MONEY_ENABLED` | `false` | First gate for live trading |
| `REAL_MONEY_CONFIRMATION` | `false` | Second gate for live trading (both required) |
| `DRY_RUN` | `false` | Simulate all orders without broker contact |
| `MAX_POSITION_SIZE_PCT` | `10%` | Maximum single position as percentage of equity |
| `MAX_DAILY_LOSS_PCT` | `2%` | Maximum daily loss before all new orders are rejected |
| `MAX_CONCURRENT_POSITIONS` | `20` | Maximum number of simultaneous open positions |
| `MAX_DRAWDOWN_PAUSE_PCT` | `15%` | Portfolio drawdown threshold that halts all new entries |
| `MAX_SECTOR_CONCENTRATION_PCT` | `25%` | Maximum allocation to any single sector |
| `MAX_CORRELATION_THRESHOLD` | `0.7` | Maximum weighted pairwise correlation before position is rejected |
| `INTRADAY_MAX_POSITION_PCT` | `5%` | Maximum intraday position size as percentage of equity |
| `INTRADAY_MAX_STOP_PCT` | `1%` | Maximum intraday stop-loss distance |
| `POSITION_MAX_POSITION_PCT` | `15%` | Maximum position trading size as percentage of equity |
| `POSITION_MAX_STOP_PCT` | `5%` | Maximum position trading stop-loss distance |
| `RESTRICTED_SYMBOLS` | `""` | Comma-separated list of symbols that cannot be traded |
| `SUPERVISOR_MAX_ITERATIONS` | `10` | Maximum iterations per supervisor cycle |

---

## Test Coverage

Safety-critical code has dedicated test suites that verify every defensive layer.

### test_safety_gate.py

15+ test cases covering every path through the SafetyGate:

- Dry-run mode returns simulated results without broker calls.
- Live money gate rejects orders when flags are not set.
- Restricted symbol list blocks blacklisted tickers.
- Position size check rejects oversized orders.
- Position size check permits correctly sized orders.
- Daily loss check rejects orders when loss limit is breached.
- Daily loss check permits orders when within limit.
- Max concurrent positions rejects new buys at the limit.
- Max concurrent positions always permits sells.
- Multiple checks can fail simultaneously (first failure wins).
- Edge cases: zero-quantity orders, negative prices, missing account data.

### test_config.py

- Default configuration values are always safe (paper trading, dry-run off, both money flags off).
- Setting `ALPACA_PAPER=false` without both flags raises `ValueError`.
- Setting only one of the two flags raises `ValueError`.
- Setting both flags with `ALPACA_PAPER=false` succeeds.

### test_dry_run.py

- Full pipeline runs in dry-run mode without errors.
- No broker API calls are made (mocked and verified).
- Simulated `OrderResult` is returned with expected structure.
- Agent reasoning and strategy selection run identically to production.

### test_risk_manager.py

- Correlation check vetoes positions that exceed the threshold.
- Sector concentration check vetoes positions that breach the limit.
- Drawdown circuit breaker halts new entries when drawdown exceeds threshold.
- Drawdown circuit breaker permits exit orders during halt.
- Portfolio delta is logged but does not block orders.
- Multiple risk violations are detected and reported.

### test_end_to_end.py

- Full pipeline integration test with `DRY_RUN=True`.
- Supervisor invokes correct agents based on market regime.
- Orders pass through all safety layers.
- Final output matches expected structure.
- No real broker calls are made during the test.
