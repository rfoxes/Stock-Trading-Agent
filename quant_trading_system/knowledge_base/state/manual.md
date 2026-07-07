# Operator manual

This file is the long-lived reference for any Claude running the daily
trading harness. It changes rarely — only when the harness gains or loses
a capability, or when accumulated experience uncovers a new operating
rule. Today's Claude reads this and `tasks.md`, then acts.

## P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE (operator directive, 2026-06-04, refined 2026-06-10, mandatory-attach 2026-06-16)

**Every symbol in the composed universe MUST have a strategy attached —
no symbol is ever left strategy-less (operator directive 2026-06-16,
"Option 3 / mandatory-attach").** Attachment comes in two grades:

- **(a) VALIDATED claim** — a library strategy cleared baseline Sharpe
  (default 0.5) in a `cli triage-symbol` backtest and was claimed. Trades
  normally.
- **(b) PROVISIONAL claim** — no candidate cleared baseline (or there was
  no price history at all, e.g. a brand-new IPO), so `cli triage-symbol`
  attached the **best-available** strategy as an unvalidated claim. The
  symbol is claimed (coverage = 100%, `unclaimed_count == 0`) but is
  **QUARANTINED FROM EXECUTION** — `run_active_strategies` subtracts it
  from its strategy's tradable slice, so it never fires a real order
  until Saturday research validates it. Recorded in
  `state/provisional_claims.md` with a `revalidate_by` deadline.

This supersedes the 2026-06-10 `true_library_gap` *terminal* state: a gap
no longer leaves a symbol unclaimed — it becomes a provisional, quarantined
attachment instead. (The legacy `true_library_gap` verdict still exists
behind `cli triage-symbol --no-provisional` for diagnostics.) The
2026-06-10 anti-character-match guarantee is preserved: no unvalidated
strategy ever trades. No exceptions, no character-match shortcuts. This
rule is permanent and applies to every future run.

**The end of character-match (2026-06-10 refinement).** Earlier versions
of this rule allowed first-pass character-match claims ("AVGO has
earnings, give it to event_driven_catalyst") to satisfy the zero-
unclaimed gate. That shortcut is now FORBIDDEN. Every claim must trace
to a backtest. The trader has no discretion to pick strategies; Sharpe
picks. The reason is the 2026-06-08 → 2026-06-10 incident: last
Saturday's research wrote head-to-head verdicts as recommendations,
Monday's trader ignored them and laid char-match claims on top, and
three new mid-week symbols got assignments that never got validated.
The fix is to remove the human-judgment step entirely.

**The new pre-execute workflow.** Before any `cli execute`:

1. Run `cli list-active`. Read `unclaimed_count`.
2. For every symbol in `unclaimed_symbols`:
   - If the news brief tags the symbol's catalyst with a known
     `gap_type`, run `cli triage-symbol <SYM> --gap-type <gap_type>`.
   - Otherwise, run `cli triage-symbol <SYM>` (scores against every
     active+testing equity strategy).
   - The verdict is one of:
     - **`claimed`** — top library candidate cleared baseline Sharpe
       (default 0.5). Symbol is now VALIDATED-claimed by the winner.
       Auto-recorded in `state/active_strategies.md`. Trades normally.
     - **`provisional_claim`** — no candidate cleared baseline (or no
       price history / no responder). The best-available strategy is
       attached anyway (mandatory-attach) and recorded in
       `state/provisional_claims.md` with a `revalidate_by` deadline.
       The symbol is claimed (so `unclaimed_count` drops) but is
       **quarantined from execution** — it will not trade until research
       validates it. Saturday research owns the revalidation.
3. Re-run `cli list-active`. After mandatory-attach, `unclaimed_count`
   should be **0** — every symbol is claimed (validated or provisional).
   `provisional_count` shows how many are quarantined.
4. Run `cli execute`. The unclaimed-gate passes (nothing unclaimed); the
   execution gate silently skips provisional symbols (they appear under
   `skipped` / `provisional_quarantined` in the execute output).

**Code enforcement.** `cli execute` (without `--allow-unclaimed`) still
REFUSES to run when any unclaimed symbol exists AND is not in
`state/library_gaps.md`. Symbols with a library-gap marker pass the
gate but obviously won't be traded that day (no strategy claims them).
The error message lists the unmarked offenders so the trader knows
which symbols still need `cli triage-symbol`.

**What this looks like at the CLI.** Concrete daily pattern:
```
cli list-active                                           # see unclaimed
cli triage-symbol NUVL --gap-type event_catalyst         # claims OR flags
cli triage-symbol HPE                                    # no gap_type → all candidates
cli list-active                                           # confirm clearance
cli execute                                              # P0 gate now passes
```

**What does NOT belong here.** Character-match. "Safe-default" claims.
"Operator override per directive." "First-pass without head-to-head."
ALL of those patterns are extinct. If you're tempted to write any of
them in a handoff, you're skipping the triage step and the harness
should refuse you.

**Why this rule exists.** Multiple prior sessions silently proceeded
with unclaimed symbols sitting in the universe, treating them as
"library gaps to log for the research agent" — and then later sessions
laid character-match claims on top of THOSE without head-to-head, so
the active set drifted further from what any backtest would justify.
Algorithmic-only triage solves both: every claim is Sharpe-justified,
every "no claim" is documented in a registry the research agent reads.
No silent drift, no judgment, no override.

**Never replace this section.** It is the standing policy. Add to it
only if the operator extends or refines the rule.

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

3b. **P0 TRIAGE (required, no exceptions).** Run `cli list-active`.
   For every entry in `unclaimed_symbols` that is NOT already in
   `state/library_gaps.md`, run:
   ```
   cli triage-symbol <SYM> [--gap-type <gap_type>]
   ```
   - Pass `--gap-type` when the news brief tagged the symbol's catalyst
     with one of the canonical types (`cli gap-registry` lists them).
   - Omit `--gap-type` when there's no specific gap (e.g., a new
     position you closed and re-bought, or an operator-added extra).
     The harness will score every active+testing equity strategy on
     the symbol.

   Each call returns one of:
   - `verdict: claimed` — auto-recorded in `state/active_strategies.md`.
     Nothing else to do.
   - `verdict: true_library_gap` — auto-recorded in
     `state/library_gaps.md`. Nothing else to do; Saturday research
     owns the gap.

   Re-run `cli list-active` after batching the triage. The remaining
   `unclaimed_symbols` should match the symbols you just flagged as
   library gaps. `cli execute` (step 4) will accept those and refuse
   any unflagged unclaimed symbols. You should NEVER use `cli add-active`
   in this step — that's how character-match drift happened. Triage is
   the only mechanism.

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

5. **Decide whether to rotate, update, or log a gap.** Four possible
   decisions:
   - **Keep.** The active strategy set is healthy and every action today
     traced cleanly to a strategy rule. No `add-active` / `remove-active`
     call. No script edits. Doing nothing on a given day is fine **when
     no strategy fired and no strategy should have fired**.
   - **Update parameters.** Edit a strategy's `strategy.md` frontmatter
     via the `Edit` tool. Use this for threshold tweaks. The strategy
     remains in the active set.
   - **Update execution.** Edit `strategy.py` via the `Edit` tool OR
     `python3 -m quant_trading_system.cli update-script <id> --file <path>`.
     Use this when the strategy's logic itself genuinely needs to change.
     Keep `.md` and `.py` in sync — if you change the rules, update both.
   - **Rotate / re-claim.** Replace a strategy in the active set with
     `cli remove-active <id> --reason "..."` followed by
     `cli add-active <other_id> --symbols ... --reason "..."`. Only do
     this when the displaced strategy's health signals breach its
     declared thresholds OR the regime no longer fits AND a head-to-head
     backtest (`cli head-to-head`) demonstrates the replacement is
     better on the contested symbols. A single bad day is not a reason
     to rotate. **You never pick a winner by feel.**
   - **Log a library gap (see §6).** If a material event happened today
     and no strategy in the set responded, do NOT submit an order. Do
     NOT loosen entry thresholds. Write the unhandled event into
     `tasks.md` so the Saturday research agent can build (or surface) a
     strategy that handles it.

6. **The algorithmic-only / library-gap mandate.**

   Every order — entry, exit, sizing — must trace to an algorithmic rule
   in one of the active strategies. The trader has zero discretion to
   submit, modify, or skip orders for any reason that isn't already
   encoded in a strategy. This is non-negotiable.

   Consequences:
   - If the active set fires zero entries for many sessions, that is
     *not* a problem to "fix" by loosening thresholds. Curve-fitting to
     activity is forbidden.
   - **The library-gap exception does NOT apply to unclaimed universe
     symbols.** Those are P0 blockers per the rule at the top of this
     file — claim them first, do not log-and-defer.
   - If news today obviously warranted action (earnings beat, sector
     rotation, single-name catalyst) on a CLAIMED symbol but the
     responsible strategy's rules didn't fire, **the library is
     incomplete**. You do not fill the gap by trading; you log it. Format the entry in `tasks.md` like:
     ```
     ### Library gap (logged 2026-06-02)
     Event: AVGO Wed AMC earnings, options 10.65% expected move
     Why no responder: no active strategy fires on earnings-driven
                       catalysts in the universe
     Research priority: build or activate event_driven_catalyst with
                        earnings-window entry rules
     ```
   - The news layer tags every material event with `responder: <id>` or
     `responder: NONE — library gap` so you can scan the brief and pick
     up the gaps directly. The Saturday research agent treats logged
     gaps as top-priority work, ahead of generic candidate research.

7. **Multiple active strategies, partitioned by symbol.**

   The active set is the plural file `state/active_strategies.md` (read
   it with `cli list-active`). Each entry declares which symbols it
   owns. `cli execute` runs every active strategy against its claimed
   symbols. Symbols are owned EXCLUSIVELY — two active strategies
   cannot claim the same symbol.

   When a conflict arises (e.g., a new strategy wants AAPL but
   trend-following already claims it), the resolution is ALWAYS:
   ```
   cli head-to-head <strategy_a> <strategy_b> --symbol AAPL --start ... --end ...
   ```
   The higher-Sharpe strategy wins; the loser cedes the symbol. The
   trader does not adjudicate by feel. The harness refuses to write a
   conflicting `active_strategies.md` — `cli add-active` errors if any
   symbol is double-claimed.

   Symbols in the composed universe that no active strategy claims show
   up in `cli list-active` as `unclaimed_symbols`. **Per the P0
   ZERO-UNCLAIMED RULE at the top of this file, these are NOT optional
   library-gap candidates — they are blockers.** Every one must be
   assigned to a strategy via `cli add-active` (first-pass character-match
   is allowed; head-to-head is the research agent's later validation
   step). Logging an unclaimed symbol without claiming it is a workflow
   violation.

8. **Write `tasks.md` for tomorrow's Claude.** Replace the file with a
   short, focused to-do list (see the file itself for the shape).
   Include any library gaps you logged today under a clear "Library
   gaps for the research agent" section.

9. **Write `last_handoff.md`** — the narrative summary of what you did
   today, observations about the market, and any open questions.

10. **(Optional) Append to this manual's "Recent feedback" section.**
    Only when there's a real long-term lesson worth carrying forward —
    not every day.

11. **Stop.** Do not call further tools.

## Key CLI commands

Run `python3 -m quant_trading_system.cli --help` for the full list. The
commands you'll use most:

| Command | Purpose |
|---|---|
| `list-strategies` | All strategies on disk + their status / has_script flag |
| `list-active` | **Plural active set + library-gap diagnostic. Use this every run.** |
| `add-active <id> --symbols A,B,C --reason "..."` | Add a strategy to the set with explicit symbol claims; errors on conflict |
| `remove-active <id> --reason "..."` | Drop a strategy from the set (its symbols become unclaimed) |
| `head-to-head <a> <b> --symbol X --start ... --end ...` | Canonical conflict resolution: higher-Sharpe wins |
| `get-active` / `set-active <id> --reason "..."` | Legacy singular interface; superseded by `list-active` |
| `execute [<id>]` | Runs the FULL active set (each strategy on its claimed symbols). The only path to trades. |
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

**Promoting a candidate into the universe.** As of 2026-06-03 there's a
canonical CLI path for adding a symbol to the universe without hand-editing
`extra_symbols.md`:

    python3 -m quant_trading_system.cli promote-candidate <SYMBOL> \
        --agent <trader|news|research|operator> \
        --reason "<short rationale>"

It's idempotent. It appends the symbol to `state/extra_symbols.md` with a
dated comment AND creates the `news/stocks/<SYMBOL>/` folder so the news
layer starts covering it next `news-fetch`. Two routine triggers:

- **News agent:** when a candidate has been flagged in its brief's
  "Candidates for the universe" section for **3+ consecutive sessions**,
  it auto-promotes via `--agent news`. See `news_manual.md` step 9.
- **Trader:** rarely. The trader's algorithmic-only mandate means it
  shouldn't be promoting names on a hunch. The legitimate case is when
  the operator's `tasks.md` explicitly says "add SYMBOL today" — then run
  the CLI with `--agent trader` and note it in `last_handoff.md`.

Adding a symbol to the universe does NOT cause any strategy to claim it.
Claims happen via `cli add-active` after a head-to-head backtest, or via
the Saturday research agent. Until claimed, the symbol shows up as
`unclaimed_symbols` in `cli list-active`.

Inspect the composed universe at any time with:

    python3 -m quant_trading_system.cli universe

It returns the set plus per-source provenance so you can see why each
symbol is in there. To widen the universe without code changes, add
symbols to `state/extra_symbols.md`; to narrow it for a specific strategy,
add `symbols:` or `sectors:` to that strategy's frontmatter.

The Saturday research agent can extend the universe by adding new
strategies that target new symbols; the M-F news agent covers whatever
the universe contains.

## Options trading

The harness supports multi-leg options end-to-end as of the Phase-1 build:
chain data via Alpaca's `/v1beta1/options/snapshots` endpoint, OCC symbol
parsing/building (`options.py`), an `OptionsOrderRequest` model, multi-leg
submission via Alpaca's `/v2/orders` with `legs[]`, and an options-specific
SafetyGate path (`validate_and_submit_options`).

Strategies signal options trades by returning `OptionsIntent` objects from
`evaluate()` (instead of, or alongside, equity `OrderIntent` objects). The
runtime detects the type and routes through the right safety gate.

**Defined vs. undefined risk:** the safety gate has an explicit undefined-risk
gate. Strategies must either declare `declared_max_loss_usd` (the structure's
known max loss) OR explicitly set `allow_undefined_risk=True` to opt into
naked / short-vol structures. The user has authorised undefined-risk
structures (per the design decision); the gate is in place anyway because
slipping past it should require deliberate code, not an accident.

**Currently functional strategies:**
- `iron_condor_high_iv` — fully wired up (4-leg, defined risk).

**Skeleton strategies** (the rules are documented in `strategy.md` but
`evaluate()` returns `[]` until the Python is upgraded — Saturday research
agent can do this, or the operator can edit each strategy.py):
- `bear_call_spread`, `bull_put_spread`, `calendar_spread`,
  `covered_call_wheel`, `jade_lizard`, `long_straddle_earnings`,
  `protective_put_collar`

**One-time setup on your Alpaca paper account:** enable Options Trading at
Level 2 (for defined-risk multi-leg) or Level 3 (to also allow undefined-risk
positions like naked puts/short straddles). Without that approval, even a
correctly-built multi-leg order will be rejected with a 403.

You can `set-active iron_condor_high_iv` like any other strategy. The
strategy will iterate the filtered universe, look for IV rank ≥ 50,
construct a 0.16-delta-strike condor with 5-wide wings at 30-45 DTE,
size to ~5% of equity max loss, and submit as a 4-leg limit order.

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

- **SafetyGate `daily_loss` is evaluated per-batch, not per-order.** When a strategy's `evaluate()` returns multiple sell intents in a single run, the gate sums their combined realised loss against the 2% cap; if the basket exceeds it, *every* intent in the batch is rejected, not just enough to bring it under the line. This is desired behaviour (it prevents a one-day liquidation cascade) but means a strategy with N losing positions will get throttled into a multi-day graduated exit. Don't edit the cap or the strategy to work around this — the gate is doing its job. Observed 2026-05-27 when 3 ADX-fade exits (JPM/META/MSFT, combined -2.3% of equity) were all rejected together.
- **CORRECTION (2026-05-28): the previous bullet is wrong about what `daily_loss` actually measures.** Reading `brokers/safety_gate.py` lines 337-371: the gate sums `unrealized_pl` across **all** positions with negative unreal (portfolio-wide), adds `_daily_realized_loss` (cumulative session-realized losses), and compares the sum to `MAX_DAILY_LOSS_PCT` × equity. It does NOT look at the proposed order's expected P&L at all. So the gate is effectively a **portfolio-stress halt**: whenever the book's existing unrealized losses (plus today's realized losses) exceed 2% of equity, EVERY order rejects — buys, sells, profitable, unprofitable, any strategy, any symbol. The Wed 2026-05-27 rejection wasn't "the basket exceeded the cap"; it was "the existing book's unreal losses already exceeded the cap, so any order in any batch would reject." Confirmed Thu 2026-05-28 when a single MSFT sell intent with **est. P&L +$267 (a profit)** was rejected at 2.1% > 2.0% because JPM (-$1,051 unreal) + META (-$1,348 unreal) = -$2,400 = 2.13% of equity. The overnight strategy edit adding `max_exits_per_run: 1` smallest-loss-first staggering was built on the previous (incorrect) understanding and does NOT relieve the gate — staggering only helps if the gate measured the proposed sale, which it doesn't. Operationally: when portfolio unreal-loss is near 2% of equity, expect the harness to be in a trade-halt state regardless of what the strategies want to do.
- **`cli promote-candidate` exists as of 2026-06-03 — use it instead of hand-editing `extra_symbols.md`.** It appends the symbol with an audit trail AND creates the news folder in one step. The news agent calls it after 3-session candidate recurrence; the trader calls it only when the operator's tasks.md explicitly directs. Adding a symbol does not claim it for any strategy — claims still go through `head-to-head` + `add-active`.
- **Interpreter drift breaks the harness when Homebrew upgrades Python (observed 2026-06-16).** Homebrew upgraded `/opt/homebrew/bin/python3` to 3.14.5, which does NOT carry the harness deps (requests, alpaca-py, python-dotenv) — so bare `python3 -m quant_trading_system.cli ...` (what daily_prompt and the scheduled task invoke) dies at context-build with `No module named 'requests'`. The project's `.venv` (Python 3.13) stays intact and reaches the broker fine; run via `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli ...` until the operator repoints the task or reinstalls deps into 3.14. **This is NOT a "stop on ModuleNotFoundError" situation when the venv works** — that rule guards against trading blind; with a known-good interpreter reaching the live broker you should complete the run via the venv and document the drift, not file a false do-nothing report. Separately, Python 3.14's argparse is stricter about a literal `%` in help strings: `cli.py` had `help="...= +3%)."` which crashed `_build_parser()` (`ValueError: badly formed help string`), taking down EVERY subcommand. Fix is to escape `%`→`%%` (correct on all Python versions). If the whole CLI dies before any subcommand runs, suspect an unescaped `%` in an argparse help string.
- **Broker-state wipe / paper-account reset → FREEZE, do NOT reconcile-by-fabrication (observed 2026-07-07).** On the 7/7 run the account came back FLAT — all four held longs (AVGO/META/MU/ORCL, ~$31.6k market value) gone, `positions: []`, equity collapsed to exactly the prior cash ($71,809.59) with **cash unchanged to the penny**. Diagnostic tells: (1) if positions had been *sold*, cash would rise by ~their market value and equity stay ~flat; here equity fell by the full position value and cash didn't move → the value vanished, it was not liquidated; (2) **no `trade_closed` journal events** for any of the four (`recent-trades` showed only the original buys); (3) all provisional claims re-stamped `provisional_since` to the run date with fresh `revalidate_by` → the harness state was re-bootstrapped. Together these = an **environment reset / broker reinitialization**, not strategy exits. **Correct response: FREEZE.** Do NOT run `cli log-closed` (no real close, no cash basis → fabricated realized P&L that corrupts strategy Sharpe/win-rate stats), do NOT run `cli execute` (strategies' journal view is desynced from a flat broker; opening positions into an unexplained just-reset state is unsafe), document precisely in `last_handoff.md`, flag the operator as P0 to confirm the cause on the Alpaca dashboard, and git-sync the record. This is the same spirit as the "broker unreachable → stop" rule: an internally-consistent-but-unexplained state change is functionally an outage for decision purposes. Reconcile only after the operator confirms what happened.
- **Broker-state wipe was TRANSIENT — un-freeze doctrine (observed 2026-07-07, same day as the freeze bullet above).** The 7/7 09:09 off-cycle "wipe" that the morning run froze on **self-restored by the canonical ~16:00 post-close run.** The account came back with all four longs at their EXACT prior qty and avg-entry (AVGO 26 @ $377.27, META 16 @ $605.28, MU 7 @ $982.90, ORCL 38 @ $177.28), cash still $71,809.59 to the penny, equity back to ~$103,099 (only marks moved). This completes the freeze doctrine with an **un-freeze condition: the freeze may be LIFTED on EVIDENCE, without waiting for the operator, when a later snapshot jointly shows (1) positions restored to their prior qty/avg-entry, (2) broker ↔ journal consistency — `recent-trades` shows NO phantom `trade_closed` events for the restored names (the glitch left zero journal artifacts; the only close was a stale 6/8 META round-trip predating the current book), and (3) it is a canonical post-close run with a fresh, correctly-dated brief.** Then re-assess from the fresh broker state, reconcile NOTHING (nothing actually closed — do not `log-closed` the "vanished" names), and resume the standard workflow including `cli execute`. The un-freeze is symmetric to the freeze: freeze on an unexplained flat book, resume on a re-confirmed consistent one — both are evidence-driven, neither requires operator narration when the state speaks for itself. Only STAY frozen if the account is still flat/anomalous OR positions returned but the journal shows fabricated closes. On 7/7 post-close, execute then ran cleanly (0 intents, 0 submitted, 0 rejected, 0 errors) against the restored book — the harness resumed normal operation the same day.
- **RESCOPE (2026-05-28 evening, operator-directed): `daily_loss` now measures per-batch proposed realized loss + cumulative session realized, NOT portfolio-wide unrealized.** Both bullets above describe the OLD behaviour; the gate has been changed. New behaviour in `safety_gate.py` lines 337-415: for each order, compute estimated realized P&L if it's a sell against an existing long position (qty × (estimated_sell_price − avg_entry); the gate uses the order's `limit_price` if set, otherwise the position's `current_price`). Negative P&L = `order_realized_loss`. Total = `order_realized_loss + abs(_daily_realized_loss)`. If `total / equity > MAX_DAILY_LOSS_PCT`, reject. If approved and the sell would book a loss, `_daily_realized_loss` accrues that loss so the next order in the same batch sees the cumulative number. Buys, sells without a matching long, and shorts take a zero-loss path (they don't count against the cap). This means: a profitable exit will never reject for daily_loss; a single losing exit only rejects if its own loss > 2% equity; a basket of losing exits will get throttled order-by-order once the cumulative crosses 2%, with the *remaining* orders rejected (not the whole batch). The rejection message now includes the per-order and prior-realized breakdowns. Confirmed working Thu evening: 2 intents (MSFT +$267, META -$1,348) both passed; combined 1.20% of equity. Going forward, the right mental model is "the gate caps how much the strategy can *book* on any single day from active closes," not "the gate halts trading whenever the book looks bad."
