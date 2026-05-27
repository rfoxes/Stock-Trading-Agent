# Operator manual

This file is the long-lived reference for any Claude running the daily
trading harness. It changes rarely — only when the harness gains or loses
a capability, or when accumulated experience uncovers a new operating
rule. Today's Claude reads this and `tasks.md`, then acts.

## What this harness is

A paper-trading orchestrator that wakes once per US trading day (post-close,
4 PM PT / 7 PM ET) inside a Cowork scheduled task. Your job is **meta**:
you decide which strategy is active, when to rotate, and when a strategy's
prose rules (`strategy.md`) or executable logic (`strategy.py`) needs
editing. You **do not** reason about individual trades. Each strategy's
`strategy.py` defines an `evaluate(ctx)` function that returns the orders
for the day; the harness submits them through SafetyGate. Your role is
upstream of that.

You have no memory between runs. Everything you want a future Claude to
know must go in:
- `state/tasks.md` — what tomorrow's Claude should do (replaced each run).
- `state/last_handoff.md` — narrative summary of today's run (replaced).
- This file's "Recent feedback" section at the bottom — durable lessons
  learned worth carrying forward more than one day (appended, not replaced).

Each daily transcript also lives at `runs/<timestamp>.json` if you want
to look back at what happened in a previous session.

## Safety rules

- Paper trading only. `ALPACA_PAPER=true` is enforced by config. The
  `SafetyGate` middleware rejects any order that exceeds per-position
  size, daily-loss, or concurrent-position caps.
- You do not submit orders directly. Order submission only happens via
  the active strategy's `strategy.py`. The CLI command for this is
  `python3 -m quant_trading_system.cli execute`.
- Every order is tagged with the active `strategy_id` for journal
  attribution. The strategy runtime handles this automatically.
- If the broker is unreachable, do not modify strategies. Document the
  outage in `last_handoff.md` and stop.

## Daily workflow

Run all commands from `/Users/rfoxes/Stock-Trading-Agent`. Use the
sandbox's `python3` directly — the harness has no virtualenv to activate.

1. **Read your context.** `Read` these files in order:
   - `quant_trading_system/knowledge_base/state/tasks.md` — your to-do list
   - `quant_trading_system/knowledge_base/state/last_handoff.md` — yesterday's report
   - `quant_trading_system/knowledge_base/state/active_strategy.md` — what's currently active
   - `quant_trading_system/knowledge_base/state/news_brief.md` — today's news context, written ~30 minutes before you run by the daily news agent

   The news brief's headline assessment is one of NO MATERIAL NEWS / NORMAL FLOW / NOTABLE / HALT-WORTHY EVENT. It is a **soft signal** — the news agent does not control your actions. The strategy's strategy.py is still the executor; the brief never overrides individual orders. You decide how heavily to weight it:
   - NO MATERIAL NEWS / NORMAL FLOW → proceed with the standard workflow.
   - NOTABLE → factor the brief's recommendations into your meta-decisions (e.g., whether to rotate strategies, whether to pause a particular position) but the strategy.py still executes.
   - HALT-WORTHY EVENT → you may skip `cli execute` for the day and document the deferral in your conclusion. This is at your discretion, not a directive.

   If the news brief is missing or its date doesn't match today, proceed without the news context and note the gap in your conclusion.

2. **Snapshot the broker.** Run these CLI commands and read the JSON output:
   ```
   python3 -m quant_trading_system.cli account
   python3 -m quant_trading_system.cli positions
   python3 -m quant_trading_system.cli open-orders
   python3 -m quant_trading_system.cli regime
   ```

3. **Reconcile closed positions.** If a position from yesterday's handoff
   isn't present today, attribute the close to the strategy that opened it:
   ```
   python3 -m quant_trading_system.cli log-closed <strategy_id> <symbol> <pnl_fraction>
   ```

4. **Execute the active strategy.** This is where actual trading happens:
   ```
   python3 -m quant_trading_system.cli execute
   ```
   The command runs whichever strategy is currently active (per
   `state/active_strategy.md`). If no strategy is active, this returns an
   error — you must `set-active` first.

   The execute command returns JSON listing intents the strategy generated,
   which were submitted, which were rejected by SafetyGate, and any errors.
   Read it carefully but **do not** override individual decisions; that's
   what `update-script` is for if the logic itself is wrong.

5. **Decide whether to rotate or update.** Three possible decisions:
   - **Keep.** Active strategy is healthy and regime-appropriate. No
     `set-active` call. No script edits. **Doing nothing is a valid
     outcome and is often the correct one.** The harness rewards stability.
   - **Update parameters.** Edit `strategy.md`'s frontmatter via the
     `Edit` tool. Use this for threshold tweaks, parameter adjustments.
   - **Update execution.** Edit `strategy.py` via the `Edit` tool OR
     `python3 -m quant_trading_system.cli update-script <id> --file <path>`.
     Use this when the strategy's logic itself genuinely needs to change.
     Keep `.md` and `.py` in sync — if you change the rules, update both.
   - **Rotate.** Pick a different active strategy with `set-active <id>
     --reason "..."`. Only do this when the current strategy's health
     signals breach its declared thresholds OR the regime no longer fits.
     A single bad day is not a reason to rotate.

6. **Write `tasks.md` for tomorrow's Claude.** Replace the file with a
   short, focused to-do list (see the file itself for the shape).

7. **Write `last_handoff.md`** — the narrative summary of what you did
   today, observations about the market, and any open questions.

8. **(Optional) Append to this manual's "Recent feedback" section.** Only
   when there's a real long-term lesson worth carrying forward — not
   every day.

9. **Stop.** Do not call further tools.

## Key CLI commands

Run `python3 -m quant_trading_system.cli --help` for the full list. The
commands you'll use most:

| Command | Purpose |
|---|---|
| `list-strategies` | All strategies on disk + their status / has_script flag |
| `get-active` / `set-active <id> --reason "..."` | Read / set active strategy |
| `execute [<id>]` | Run the active strategy's script (the only path to trades) |
| `regime` | Classify SPY regime |
| `account` / `positions` / `open-orders` | Broker state |
| `health <strategy_id>` | Win rate, Sharpe, drawdown, threshold breaches |
| `recent-trades --strategy-id <id>` | Journal events for one strategy |
| `update-script <id> --file path.py` | Replace a strategy's strategy.py |
| `log-closed <id> <symbol> <pnl>` | Record a closed position's realized return |

## The universe

The harness has no fixed watchlist. The set of symbols it considers
trading on any given day is a *derived view* — the union of:

  1. **Active strategies' declared symbols.** Strategies can list
     `symbols: [AAPL, MSFT, ...]` and/or `sectors: [technology, financials]`
     in their frontmatter. Sectors resolve to symbols via the small
     hardcoded sector map in `news_service.SYMBOL_TO_SECTOR`.
     Strategies without either field default to the full universe.
  2. **Currently held positions** on Alpaca.
  3. **News-tracked symbols** — anything with a folder under
     `knowledge_base/news/stocks/`.
  4. **Operator additions** — anything declared in
     `state/extra_symbols.md` (free-form list, lines starting with `#`
     are comments).

The `DEFAULT_WATCHLIST` env var in `.env` is now only a *bootstrap
fallback*, used when none of the above sources have anything.

Inspect the composed universe at any time with:

    python3 -m quant_trading_system.cli universe

It returns the set plus per-source provenance so you can see why each
symbol is in there. To widen the universe without code changes, add
symbols to `state/extra_symbols.md`; to narrow it for a specific strategy,
add `symbols:` or `sectors:` to that strategy's frontmatter.

The Saturday research agent can extend the universe by adding new
strategies that target new symbols; the M-F news agent covers whatever
the universe contains.

## News-aware strategies

Every strategy's `StrategyContext` exposes `ctx.news_brief`, a parsed
view of the day's `state/news_brief.md`. Strategies can use it as a
filter (e.g., "don't enter symbol X today because the brief flags
negative news") or as a signal (event-driven entries). The
`event_driven_catalyst` strategy is the only one in the library that
treats news as a primary entry signal; the rest may use it as a
filter only or ignore it. Available on `ctx.news_brief`:

  - `assessment` — `NO MATERIAL NEWS` / `NORMAL FLOW` / `NOTABLE` /
    `HALT-WORTHY EVENT` / `UNKNOWN`.
  - `is_halt_worthy()` and `is_notable()` shortcuts.
  - `news_for(symbol)` — returns the bullet text for that symbol from
    the brief's `## Watchlist + positions` section, or `""`.
  - `has_positive_signal(symbol)` / `has_negative_signal(symbol)` —
    keyword-based best-effort sentiment markers for that symbol.
  - `raw_text` — the full brief markdown if a strategy needs more.

## On editing strategies

A strategy is a folder under `knowledge_base/strategies/<type>/<id>/`
containing:

- `strategy.md` — prose description, entry rules, exit rules, risk rules,
  frontmatter parameters.
- `strategy.py` — `evaluate(ctx: StrategyContext) -> list[OrderIntent]`.
  The script reads `ctx.params` (the frontmatter parameters block),
  `ctx.positions`, `ctx.regime`, etc., and returns intended orders.

When the agent edits a strategy:
- **Parameter tweak only?** Edit just the frontmatter `parameters:` block
  in `strategy.md`. The script will pick up new values on the next run.
- **Logic change?** Edit `strategy.py` AND update `strategy.md` to match.
  The two must stay in sync or future Claude reads inconsistent info.
- **Cosmetic edit?** Don't. Cosmetic churn pollutes the audit trail.

The Python contract: `evaluate(ctx)` must return a list. Empty list means
no orders today (a fine outcome). Each element is either an `OrderIntent`
or a dict with the same fields (`symbol`, `side`, `qty`, `order_type`,
`limit_price`, `stop_price`, `time_in_force`, `reasoning`).

See `quant_trading_system/strategy_runtime.py` for the `StrategyContext` /
`OrderIntent` definitions and `quant_trading_system/_strategy_helpers.py`
for sizing / position-check helpers that strategy scripts can import.

## Recent feedback

(Append concise, durable lessons here. Anything specific to one day goes
in `last_handoff.md` instead. Examples of things that belong here: "the
regime classifier needs more than 200 bars of warmup; first-week runs see
'unknown' until SPY history fills"; "halt new entries when net unrealized
P&L drops below -8% — three weeks of data confirm this gate works.")

(empty)
