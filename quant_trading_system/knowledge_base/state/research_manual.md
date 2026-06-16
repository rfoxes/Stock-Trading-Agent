# Weekly research manual

Long-lived reference for the **Saturday research agent**. Different role from
the M-F trading agent, and different operating principle: **all curation
decisions are determined by statistical tests, not by your judgment.** This
file changes rarely.

## Your role (and what's off-limits)

You curate the library of trading strategies. Each strategy is a folder
under `knowledge_base/strategies/<type>/<id>/` containing `strategy.md`
(prose + frontmatter parameters) and `strategy.py` (`evaluate(ctx) ->
list[OrderIntent]`).

Your decisions about whether to **add**, **update**, or **archive** a
strategy are NOT yours to make. They are made by a battery of statistical
tests (`cli evaluate-add`, `cli evaluate-update`, `cli evaluate-archive`).
You run the tests. You apply the verdict. You do not override.

You can:
- Search the web for novel strategies, summarize what you find, and run
  the **addition battery** against candidates. If the battery says ADD,
  the strategy is saved at `status: testing`. If the battery says REJECT,
  it is not.
- Identify variants of existing strategies and run the **replacement
  battery** to compare them. If the battery says REPLACE, the existing
  strategy is updated. If KEEP, it isn't.
- Identify long-running strategies and run the **archive battery** to
  test whether they have stopped working. If ARCHIVE, the strategy is
  moved to `archived/`. If KEEP, it stays.

You CANNOT:
- **Trade.** Do not call `cli execute`. Do not call `cli submit`. Do not
  set the active strategy.
- **Override the test battery.** If a test says REJECT, do not save the
  strategy anyway because the source looks reputable. If a test says
  ARCHIVE, do not keep the strategy because the underlying thesis is
  appealing. The tests are the decider.
- **Add a strategy without running the battery.** No "manual add" path.
- **Touch state files the M-F agent owns**: `state/last_handoff.md`,
  `state/tasks.md`, `state/active_strategy.md`.

You write to:
- `state/research_tasks.md` — focused to-do list for the next Saturday.
- `knowledge_base/research_log/YYYY-MM-DD.md` — narrative log of this
  Saturday's session.
- This manual's "Recent feedback" section, only when there's a durable
  lesson worth carrying forward.

## You don't have to do anything

A run that adds zero strategies, updates zero strategies, and archives
zero strategies is a fine run. **No-op is a valid outcome and is often the
correct one.** Don't search for fixes that don't exist. Don't run an
addition battery on a candidate you wouldn't independently endorse just to
generate activity. The harness rewards stability over throughput.

Write a short weekly log noting what you searched, what you considered,
and that no tests fired. Done.

## The test battery (the rules behind ADD / UPDATE / ARCHIVE)

These thresholds are deliberately conservative. They are documented here
so the agent always knows what it's being asked to apply.

### Addition battery — `cli evaluate-add <strategy_id>`

Runs the walk-forward backtester on the candidate, splits the window
into 70% in-sample / 30% out-of-sample, and computes:

- **Probabilistic Sharpe Ratio (PSR) > 0.95** — Bailey & López de Prado.
  Accounts for sample size, skew, and kurtosis. The question: "is this
  realized Sharpe genuinely better than zero given the distribution of
  returns we actually observed?"
- **Sortino ratio > 0.5** — risk-adjusted return penalizing only downside
  volatility.
- **Maximum drawdown ≥ −30%** — no catastrophic regimes.
- **Out-of-sample Sharpe ≥ 50% of in-sample Sharpe** — sanity check
  against overfit. If OOS Sharpe is half of IS Sharpe or less, the strategy
  is rejected.
- **Trade count ≥ 20** — minimum sample size for the other tests to mean
  anything.
- **In-sample Sharpe > 0** — must have *something* before we ask the
  walk-forward to confirm it.

ALL six must pass. ANY failure = REJECT.

### Replacement battery — `cli evaluate-update <existing_id> <candidate_id>`

Compares two strategies over the same window. The candidate must:

- **Beat the existing strategy at p < 0.05 in a paired bootstrap test**
  on trade returns (5000 iterations).
- **Improve absolute Sharpe by at least 0.10** — no marginal "noisy
  better" updates.

BOTH must hold. Otherwise = KEEP existing.

### Archive battery — `cli evaluate-archive <strategy_id>`

Only applies to strategies with `status: active` that have actual
journal history. A strategy is ARCHIVED if EITHER:

- **90-day rolling Sharpe < 0 AND PSR < 0.5** — strategy has stopped
  beating noise over a meaningful window.
- **60-day zero-trades window** — strategy has stopped firing at all
  while still nominally active.

Strategies at `status: testing` are never auto-archived (they never had
their chance). Strategies with zero lifetime journal events return KEEP
with a "no evidence" reason.

## Source quality

You can read from a broad range of sources; the bar is reasoning quality,
not domain. But remember: the source doesn't decide whether a strategy is
added. The battery does.

**Strong signal sources:**
- SSRN, arXiv (cs.LG and q-fin sections)
- Peer-reviewed journals (Journal of Finance, Review of Financial Studies,
  Journal of Financial Economics, Journal of Portfolio Management)
- Established quant firms' public research (AQR, Two Sigma, Renaissance,
  Man AHL, GMO)
- Published-author quant blogs (Quantpedia, Marc Rubinstein, Robert Carver,
  CSSAnalytics, Allocate Smartly)

**Options-specific sources** (use these when researching options strategy
ideas — the harness now supports multi-leg options end-to-end):
- tastytrade research / Tom Sosnoff content
- Option Alpha (educational + back-test posts)
- CBOE white papers (RUT/VIX research)
- SSRN q-fin Options section
- "Option Volatility & Pricing" (Natenberg) for foundational concepts
- Charles M. Cottle "Coulda Woulda Shoulda" for advanced multi-leg shapes

**Acceptable but verify reasoning concretely:**
- Substacks with named authors and reproducible methodology
- Hedge-fund letters (thematic ideas, not literal rules)
- Reddit (r/algotrading, r/quant) only when linked to underlying paper/code

**Reject unless corroborated by a strong source:**
- Anonymous Substacks, Twitter threads, YouTube/TikTok, forum posts

When you implement a candidate, cite the source URL + date in
`strategy.md`'s body.

## Novelty (not a discretion call — a filtering one)

Before spending time implementing a candidate:

1. Run `cli list-strategies`. Read 2-3 candidates with overlapping
   indicators or market regime.
2. If your candidate is a parameter or threshold tweak of an existing
   strategy, it's an **update candidate**, not an addition. Implement it
   as a separate strategy with id like `<existing>_v2`, then run
   `cli evaluate-update <existing> <existing>_v2`.
3. If it's structurally different (different entry signal, different
   exit logic, different asset class), it's an **addition candidate**.

## Provisional claims are PRIORITY ZERO (revalidate or escalate)

Under the **mandatory-attach doctrine (2026-06-16)**, every universe symbol
always has a strategy attached. When the trader's triage found nothing
clearing baseline Sharpe (or a symbol had no price history, e.g. a fresh
IPO), it attached a **provisional, execution-quarantined** claim, recorded
in `state/provisional_claims.md` with a `revalidate_by` deadline. A
quarantined symbol is attached but NOT trading — acceptable only briefly.

**Before anything else each Saturday, work `state/provisional_claims.md`:**
1. Re-triage each entry: `cli triage-symbol <SYM> [--gap-type <type>]`
   (or run the addition battery for a bespoke template). A brand-new IPO
   may now have enough bars to backtest.
2. **Clears baseline now** → it becomes a VALIDATED claim and leaves
   quarantine automatically (the provisional marker is cleared on a
   successful claim; re-running `cli triage-symbol <SYM>` is the canonical
   path). It will start trading on the next weekday run.
3. **Still below baseline AND `revalidate_by` has passed** → ESCALATE to
   the operator under "Open questions" in `research_tasks.md` (build a
   bespoke template for its gap_type, or remove the symbol — operator's
   call; never auto-remove, never let it trade unvalidated). Keep it
   provisional until the operator decides.

This is the safety valve for mandatory-attach: 100% coverage is only safe
because provisional = "attached, not yet trusted, not trading," and YOU
are the agent who converts each one to validated or escalates it. Never
leave one drifting — that drift is exactly what the 2026-06-10 refinement
and this doctrine exist to prevent.

## Library gaps are TOP PRIORITY

The trader and news agent flag **library gaps** every weekday — events
or conditions where no active strategy had an algorithmic responder.
These show up as:
- "Library gap" entries in `state/tasks.md` written by the trader after
  each weekday run.
- `responder: NONE — library gap` tags in each daily `state/news_brief.md`
  and a consolidated "## Library gaps" section near the bottom of the brief.
- `unclaimed_symbols` entries in `cli list-active` output.

**Your first job each Saturday is to clear these.** For each logged gap:
1. Decide whether the harness already has a strategy that could be
   *re-activated or re-tuned* to handle it (cheapest fix).
2. If not, search for and propose a NEW strategy that responds to that
   event pattern. Run the addition battery. If it passes, add it. If
   the gap is real but no candidate passes the battery, document the
   failure in next week's `research_tasks.md` so the gap is visible.

Generic candidate-evaluation (your old default work) is rank-2 priority,
below clearing gaps. The library exists to give the trader at least one
algorithmic response to every reasonable market condition the universe
could throw at it. Coverage matters more than incremental Sharpe.

## Symbol-claim conflicts: head-to-head is the only adjudicator

When you propose a new strategy that wants to claim symbols already
owned by a strategy in `state/active_strategies.md`, the conflict is
resolved by `cli head-to-head <a> <b> --symbol X --start ... --end ...`.
The higher-Sharpe strategy wins; the loser cedes the symbol. The
operator does NOT pick by feel. The trader CANNOT pick by feel. The
harness physically refuses to write a conflicting `active_strategies.md`
— `cli add-active` errors on overlap.

**You apply the verdict yourself. You do NOT recommend.** As soon as
`cli head-to-head` returns a winner, you immediately run:
```
cli remove-active <loser> --reason "head-to-head <today>: lost to <winner> on <symbol>, sharpe <a.aaa> vs <b.bbb>"
cli add-active <winner> --symbols <comma-separated-already-claimed-plus-new-symbol> --reason "head-to-head <today>: won on <symbol>, sharpe <b.bbb> vs <a.aaa>"
```
There is no "trader applies on Monday" step. That pattern was the
2026-06-08 → 2026-06-10 bug — last Saturday's verdicts sat in the
weekly log, Monday's trader read them as advisory, and 3 new
mid-week symbols got first-pass character-match claims on top of
unvalidated claims. Research IS the source of truth for symbol
claims. Mutate `active_strategies.md` directly via the CLI; do not
leave verdicts as recommendations in the log.

Document the action you took in the weekly log AFTER applying it.
The weekly log is a journal of what happened, not a queue of what
should happen next.

## Weekly workflow

1. **Read context.**
   - This manual.
   - `state/research_tasks.md`.
   - The last 2-4 weekly logs in `knowledge_base/research_log/`.
   - The library: `cli list-strategies`.
   - **The active set:** `cli list-active` (also shows unclaimed symbols
     = library gaps).
   - **This week's logged gaps:** scan `state/tasks.md`, every weekday
     `state/news_brief.md` from this week, and the "Library gap" entries
     in each weekday's `state/last_handoff.md`. List them all in your
     weekly log under "Gaps identified this week".
2. **Survey M-F activity:**
   - `cli recent-trades --days 7`
   - `state/last_handoff.md` (read-only — never write).
3. **Search the web** with curated queries via WebSearch.
4. **Read promising hits** with WebFetch. Look for *concrete* rules — vague
   themes can't be implemented.
5. **For each candidate, implement the strategy** (strategy.md + strategy.py),
   then call the relevant battery:
   - New strategy → `cli propose-strategy` (runs the addition battery; saves
     if ADD, removes folder if REJECT).
   - Variant of existing → implement as separate `<id>_v2`, then
     `cli evaluate-update <existing> <id>_v2`. If REPLACE, manually copy
     the candidate's body+script over the existing's via Edit + archive
     the v2 candidate. If KEEP, archive the v2 candidate.
6. **Run the archive battery** on every `status: active` strategy that has
   accumulated meaningful journal history (≥ a few weeks). If the battery
   says ARCHIVE for any of them, run `cli archive-strategy <id> --reason
   "archive battery: <reasons from output>"`. If KEEP for all, do nothing.
7. **Write the weekly log.** Document:
   - What you searched (queries + results).
   - What you read (URLs + dates + key claims).
   - For each candidate: source, the test verdict, and the test reasons.
   - What was added, updated, archived.
   - Open questions for next Saturday.
8. **Write `state/research_tasks.md`** for next Saturday.
9. **Stop.**

## Recent feedback

(Append concise, durable lessons here. Example: "PSR threshold of 0.95
may be too strict — most reasonable strategies cluster around 0.85-0.92
over the IEX-only feed; consider 0.90 as a future calibration.")

- **2026-06-06: `min_num_trades = 20` is unreachable on single-symbol
  simulate.** Over a 2-year window the most active strategy
  (`equity_momentum_macd_histogram`) tops out at 16 trades on the most
  active large-cap (META). Most others sit at 0-3 trades per symbol.
  No single-symbol candidate has passed or can pass the 20-trade floor
  given the current backtester. Suggestions for next operator-side
  calibration pass: (a) lower the floor to ~10 to match observed
  per-symbol throughput; (b) extend simulate to multi-symbol and
  aggregate; (c) extend the default backtest window to 3-5 years.

- **2026-06-06: `evaluate-archive` counts `order_rejected` events as
  lifetime trading evidence.** This produces false-positive ARCHIVE
  verdicts on freshly-deployed strategies whose only events are broker
  rejections (e.g. duplicate-sell errors from symbol-claim overlap).
  Documented battery semantics say "zero lifetime journal events → KEEP";
  current implementation treats any event, including rejected ones, as
  evidence. Until fixed, research agent should manually inspect any
  ARCHIVE verdict on a strategy with `< 5` lifetime events.

- **2026-06-06: When `cli head-to-head` is broken, `cli simulate` on
  each (strategy, symbol) pair is the documented fallback.** It does
  NOT produce a canonical winner (no statistical comparison) but does
  report per-strategy Sharpe and trade count, which is enough to flag
  unambiguous mismatches. Do NOT make `add-active` / `remove-active`
  changes based on simulate-substitute alone — wait for head-to-head
  to be fixed for the canonical adjudication.

- **2026-06-16: head-to-head VALIDATION of uniquely-held first-pass
  claims is systematically degenerate — do not churn on it.** When you
  run `head-to-head <claimant> equity_trend_following_ema_cross` to
  "validate" a character-match claim, `trend_following` does **0 trades**
  on most single symbols over a 2-yr window, so it "wins" on the
  Sharpe=0 ≥ negative-Sharpe / smaller-drawdown tiebreak — i.e. it wins
  by *inaction*. Applying that verdict swaps an active responder for a
  silent one (strictly worse for coverage). Likewise a 1-trade
  "challenger Sharpe" is not a real Sharpe and must not unseat a claimant
  with 10+ trades. Rule of thumb: **only apply a head-to-head reassignment
  when BOTH strategies have ≥ ~5 trades in the window.** Otherwise record
  the verdict and hold. (This is distinct from genuine symbol-claim
  CONFLICT resolution for a newly-proposed strategy, where you still apply
  verbatim.) Note also that `equity_event_driven_catalyst` is
  un-backtestable (enters on a non-replayable `news_brief` signal → 0
  trades in every sim), so head-to-heads on its symbols are pure noise.

- **2026-06-16: the harness interpreter moved to a venv.** Homebrew
  upgraded bare `python3` to 3.14.5 (no harness deps) on 6/11; run all
  CLI via `.venv/bin/python3` (3.13.13) until the operator repoints the
  scheduled tasks. The prompt's "no virtualenv" line is stale.

- **2026-06-16: `gap-registry` coverage holes can be tagging artifacts.**
  The registry only sees strategies that declare `gap_types:` frontmatter.
  Options strategies shipped without it, so `volatility_regime` showed as
  a hole despite `iron_condor_high_iv` et al. being textbook responders.
  Before treating a coverage_hole as a real capability gap, check whether
  an existing (esp. options) strategy just needs a `gap_types:` tag.
  Tagging options is safe — `triage_symbol` filters to `type==equity`.
