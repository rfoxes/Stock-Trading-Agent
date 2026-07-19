# Quant Trading Harness

A single-agent paper-trading harness. One Claude wakes up once per weekday,
reads its own markdown notes from yesterday, decides whether to keep, modify,
or rotate strategies, submits orders for tomorrow's session, and writes a
hand-off note for the next day's Claude.

No multi-agent network. No vector database. No daemon. Each run is a clean,
self-contained agent loop that reads from disk, acts, writes back to disk,
and exits. The markdown files in `quant_trading_system/knowledge_base/` are
the only source of truth.

**Safety**: paper trading by default. Live trading requires both
`REAL_MONEY_ENABLED` *and* `REAL_MONEY_CONFIRMATION` set to `true`, and
`ALPACA_PAPER=false`. The `SafetyGate` middleware rejects any order that
doesn't satisfy those gates plus per-position size, per-day loss, and
concurrent-position limits.

## Architecture

```
       Cowork mode                       Standalone mode
       (laptop, today)                   (Pi / cloud, later)
       ────────────────                  ─────────────────────
   ┌─────────────────────┐           ┌────────────────────────┐
   │ Cowork scheduled    │           │ system cron / launchd  │
   │ task @ 16:00 PT M-F │           │ @ 16:00 PT M-F         │
   └──────────┬──────────┘           └──────────┬─────────────┘
              │ fires session                   │ runs script
              ▼                                 ▼
   ┌─────────────────────┐           ┌────────────────────────┐
   │ Claude in Cowork    │           │ orchestrator.py        │
   │ + daily_prompt.md   │           │ + Anthropic API        │
   │ (Read/Write/Edit/   │           │ (tool-use loop with    │
   │  Bash → cli.py)     │           │  tool_registry schemas)│
   └──────────┬──────────┘           └──────────┬─────────────┘
              │                                 │
              └────────────┬────────────────────┘
                           ▼
   ┌──────────────────────────────────────────────────────────┐
   │ shared layer:                                            │
   │   agent_tools.py  →  SafetyGate  →  Alpaca               │
   │                  →  journal.py   →  trades/*.jsonl       │
   │                  →  memory.py    →  knowledge_base/*.md  │
   │                  →  health.py    →  (deterministic math) │
   └──────────────────────────────────────────────────────────┘
```

`agent_tools.py` is a set of plain Python functions. Standalone mode wraps
them in Anthropic tool schemas (`tool_registry.py`) and exposes them to
Claude via the API. Cowork mode wraps them in CLI subcommands (`cli.py`)
and exposes them to Cowork-Claude via bash. Either way, every order goes
through `brokers/safety_gate.py`, and every order is logged to
`trades/YYYY-MM.jsonl` with a `strategy_id` so tomorrow's run can
attribute outcomes.

## Two ways to run

The harness has two run modes that share the same memory layer (`knowledge_base/`),
the same trade journal (`trades/`), the same Python helpers, and the same safety
boundaries. The only thing that differs is *who* is doing the reasoning.

| Mode | Brain | Auth | Trigger | Use when |
|------|-------|------|---------|----------|
| **Cowork** (this is the recommended setup right now) | Claude inside Cowork session | your Claude account | Cowork scheduled task | Running on your laptop |
| **Standalone** | Anthropic API via `orchestrator.py` | `ANTHROPIC_API_KEY` | system cron / launchd | Running on a Pi or cloud VM (no Cowork available) |

Both modes:
- Read and write the same `knowledge_base/strategies/*.md`, `conclusions/*.md`, and `state/*.md` files.
- Submit orders only through `SafetyGate.validate_and_submit`.
- Write to the same `trades/YYYY-MM.jsonl` journal so health signals work across modes.

### Cowork mode (laptop, no API key)

In Cowork mode, Claude *is* the orchestrator: a scheduled task fires a Cowork
session, the session is given a daily-workflow prompt, and Claude does the
reasoning natively. Deterministic helpers (compute health, classify regime,
submit through SafetyGate, log to journal) are exposed as a CLI:

```
python3 -m quant_trading_system.cli <subcommand> ...
```

The harness deliberately depends only on libraries pre-installed in the
Cowork Linux sandbox: `requests`, `pandas`, `numpy`, `yaml`,
`python-dotenv`, plus stdlib. **No virtualenv, no `pip install` step.**
That's why Cowork mode actually works inside the scheduled-task sandbox —
the previous architecture failed because it relied on a macOS-host venv
that the sandbox couldn't see.

See `quant_trading_system/cli.py` for the full subcommand list, or run
`python3 -m quant_trading_system.cli --help`.

**Setup:**

```bash
# 1. Clone — no venv, no install step
git clone <repo-url> && cd Stock-Trading-Agent

# 2. Configure — Cowork mode does NOT need ANTHROPIC_API_KEY,
#    just Alpaca paper credentials.
cp .env.example .env
# Edit .env: ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_PAPER=true

# 3. Smoke-test the CLI manually
python3 -m quant_trading_system.cli list-strategies --status active
python3 -m quant_trading_system.cli market-status
python3 -m quant_trading_system.cli account     # hits Alpaca; needs valid creds
```

**Schedule it:**

1. Open `daily_prompt_short_term.md` in this repo and copy its contents.
2. In Cowork, create a scheduled task that fires M-F at 4:00 PM in
   `America/Los_Angeles`. Paste the prompt as the task's instruction.
3. Set the working directory to `/Users/<you>/Stock-Trading-Agent` (or
   ensure the prompt's absolute paths still match).

**Prompt sets — long-hold vs short-term (2026-07-19):** the harness
transitioned from holding longs to short-term trading (days to a few
weeks — typically ~2-15 trading days; swing, not day trading). Each of the three scheduled tasks (news, trader,
research) now uses the `*_short_term.md` variant of its prompt
(`daily_prompt_short_term.md`, `daily_news_prompt_short_term.md`,
`weekly_research_prompt_short_term.md`); the originals are retained for
reference/rollback and carry a SUPERSEDED banner. Same template either
way: trading is grounded in the daily news brief and Saturday research,
every order traces to a strategy rule, and Sharpe decides claims. The
durable doctrine lives in the manuals (`state/manual.md` §P1,
`state/news_manual.md` §"Short-term reorientation",
`state/research_manual.md` §"Short-horizon mandate"), so the change
applies even before the scheduled tasks are re-pasted. Note: the
transition never force-sells existing positions — exits always come from
the owning strategy's rules.

The laptop must be **awake and on AC power** at 4 PM PST or the run won't
fire. macOS sleeps by default on battery:

```
System Settings → Battery → "Prevent automatic sleeping on power adapter
when display is off" = on
```

Each daily run produces a `conclusions/YYYY-MM-DD.md` and updates
`state/last_handoff.md`. To inspect a run after it fires, read those files.

### Standalone mode (Pi / cloud, with API key)

In standalone mode, `orchestrator.py` is a Python script that calls the
Anthropic API directly. **This mode needs `pip install anthropic` (the
sandbox-friendly harness intentionally doesn't bundle it), plus your
Anthropic API key. Use it on a Pi or cloud VM where you control the
runtime, not inside Cowork's sandbox.**

```bash
# 1. On the deployment target (e.g. a Pi):
pip install anthropic               # the only extra dep beyond Cowork-mode
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env

# 2. First run — dry-run, off-session is allowed for testing
python3 -m quant_trading_system.orchestrator --dry-run --allow-non-session

# 3. Inspect outputs
ls runs/                                 # full transcript of the run
cat quant_trading_system/knowledge_base/conclusions/$(date +%F).md
cat quant_trading_system/knowledge_base/state/last_handoff.md
```

The `--dry-run` flag forces `SafetyGate` into simulation mode — orders are
validated and logged but never sent to Alpaca. `--allow-non-session` lets
you test on weekends and holidays.

To migrate from Cowork to standalone (e.g. moving onto the Pi), copy the
entire repo across — the markdown memory transfers as-is — add the API key
to `.env`, and add a crontab entry (see "Eventually: Raspberry Pi via cron"
below).

## Memory layout

```
quant_trading_system/knowledge_base/
├── strategies/
│   ├── equity/<id>.md              # 18 starter strategies (frontmatter + body)
│   ├── options/<id>.md
│   └── archived/                   # auto-populated when agent retires a strategy
├── conclusions/
│   └── YYYY-MM-DD.md               # one per run; the day's narrative log
└── state/
    ├── active_strategy.md          # which strategy is currently in use
    ├── last_handoff.md             # short note from yesterday's Claude to today's
    └── summary.md                  # rolling long-horizon takeaways

trades/
└── YYYY-MM.jsonl                   # append-only journal of all order events

runs/
└── YYYY-MM-DD-HHMM-<id>.json       # full transcript per run (debugging)

.harness.lock                       # acquired during run, refused if held
```

## What the agent does each run

The Cowork-mode workflow is spelled out in `daily_prompt.md` (paste that
into the scheduled task). The standalone-mode workflow is the system prompt
at the top of `orchestrator.py`. They describe the same procedure:

1. Read yesterday's handoff and recent conclusions.
2. Reconcile yesterday's open positions vs today's broker state; log any
   closes to the journal so future health signals can attribute them.
3. Read deterministic health for the active strategy (win rate, rolling
   Sharpe, max drawdown, P&L vs SPY, breached thresholds).
4. Classify the current regime.
5. If the active strategy's thresholds are breached *or* the regime no
   longer fits, rotate to a better-suited strategy.
6. Plan tomorrow's positions using the active strategy's rules + current
   data. Submit orders through SafetyGate (always tagged with
   `strategy_id`, always with stop/target documented in reasoning).
7. Write a conclusion file (`conclusions/YYYY-MM-DD.md`) with a summary
   of what was done and a recap of the day's reasoning.
8. Update the handoff note (`state/last_handoff.md`) with state +
   recommendations for tomorrow's Claude.
9. Stop. The run ends.

## Migration: Cowork → Raspberry Pi

When you're ready to move off the laptop, the markdown memory transfers
as-is:

```bash
# On the laptop:
git push

# On the Pi:
git clone <repo-url> && cd Stock-Trading-Agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in ALPACA_* and ANTHROPIC_API_KEY (Pi can't run Cowork)

# Add the cron entry (local time):
crontab -e
# 0 16 * * 1-5  cd /home/pi/Stock-Trading-Agent && /home/pi/Stock-Trading-Agent/.venv/bin/python -m quant_trading_system.orchestrator >> /home/pi/Stock-Trading-Agent/runs/cron.log 2>&1
```

The Pi being always-on means the run never fails for "laptop was asleep"
reasons. The harness checks the NYSE calendar and skips early on holidays
either way — no special handling needed.

## Safety model

Five gates, in order:

1. **Dry-run mode** — `DRY_RUN=true` short-circuits everything below.
2. **Live-money gate** — `ALPACA_PAPER=false` requires both
   `REAL_MONEY_ENABLED=true` and `REAL_MONEY_CONFIRMATION=true`. Default
   config will refuse to start if these are inconsistent.
3. **Restricted symbols** — anything in `RESTRICTED_SYMBOLS` is rejected.
4. **Position size** — single order can't exceed `MAX_POSITION_SIZE_PCT`
   of equity.
5. **Daily loss + concurrent positions** — `MAX_DAILY_LOSS_PCT`,
   `MAX_CONCURRENT_POSITIONS`.

The agent has no way to bypass these. `submit_order` always routes through
`SafetyGate.validate_and_submit`.

## Cleanup notes

The previous multi-agent design left a number of files that are no longer
imported by anything. They've been overwritten with deprecation stubs and
can be removed cleanly with:

```bash
git rm -r quant_trading_system/agents/
git rm -r quant_trading_system/graph/
git rm -r quant_trading_system/dashboard/
git rm    quant_trading_system/llm_factory.py
git rm    quant_trading_system/models/state.py
git rm    quant_trading_system/models/strategy.py
git rm    quant_trading_system/models/conclusion.py
git rm    quant_trading_system/knowledge_base/chroma_client.py
git rm    quant_trading_system/knowledge_base/strategy_loader.py
git rm    quant_trading_system/tools/llm_callback.py
git rm    tests/test_knowledge_base.py
git rm    tests/test_end_to_end.py
git rm    tests/test_risk_manager.py
git rm -r chroma_data/
```

None of these are referenced by the harness; the orchestrator runs without
them.

## License

MIT
