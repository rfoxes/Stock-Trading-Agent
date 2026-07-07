# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update (2026-07-07)

- **RUN VIA `.venv/bin/python3`, NOT bare `python3`.** Homebrew 3.14.5 still lacks
  harness deps; bare `python3 -m quant_trading_system.cli ...` fails
  `No module named 'requests'`. Working interpreter: `.venv/bin/python3` (3.13.13).
  Many runs on the venv. Operator hasn't repointed the tasks. (Open Q#1.)
- **This run covered the ~2.5-week gap since 6/20** (6/27 Saturday produced no log;
  this was the delayed 7/04 run executing 7/07 post-holiday).
- **Library size:** 19 strategies (11 equity, 8 options). All `active`. 0 archived.
  `gap-registry coverage_holes: []`.
- **Adds/updates/archives this run: 0 / 0 / 0 (correct no-op).** Every gap is
  overlay/assignment/taxonomy/options-not-backtestable — none `propose-strategy`-shaped.
  See `research_log/2026-07-07.md`.
- **Archive sweep:** all 8 active-set equity strategies → KEEP. trend_following
  HEALTHY (rolling Sharpe 6.25, PSR 0.87, 10 trades). event_driven_catalyst STILL
  `rolling_sharpe null` / 0 trades in window even after MU's 6/24 print (un-adjudicable).
- **Head-to-head:** none run (degenerate first-pass validations, Open Q#3). Active
  set UNCHANGED.
- **Web research:** PEAD (SUE) and index-rebalance both researched, both foregone
  REJECT (cross-sectional / low-freq vs single-symbol backtester + 20-trade floor).
  Not implemented. Log §"Web research".
- **PROVISIONAL claims (PRIORITY ZERO) — all 3 re-triaged, none cleared, all still
  quarantined:**
  - **SPCX** (trend_following, `volatility_regime`): 16 bars now (was 5), still `<60`
    → un-backtestable; gap_type is options-only (no chain data). Orig. deadline
    **2026-07-04 LAPSED** → **ESCALATED (Open Q#7)**. Re-triage auto-bumped
    `revalidate_by` → 2026-07-21. Won't accrue 60 bars until ~September.
  - **QCOM** (event_driven, `event_catalyst`): Sharpe 0.0 / 0 trades — responder is
    un-backtestable, can NEVER clear baseline via triage. Orig. deadline 7/10;
    re-triage auto-bumped → 7/21.
  - **SYNA** (pairs_cointegration, `pairs_arbitrage`): Sharpe 0.0 / 0 trades — needs
    the short-ON leg modeled; single-symbol sim = 0 trades forever. Orig. deadline
    7/10; re-triage auto-bumped → 7/21.

## To do this Saturday

1. **PRIORITY ZERO — re-triage all 3 provisionals, but escalation logic first.**
   `cli triage-symbol SPCX --gap-type volatility_regime`, `... QCOM --gap-type
   event_catalyst`, `... SYNA --gap-type pairs_arbitrage`. **BEFORE re-triaging,
   note that re-triage AUTO-EXTENDS `revalidate_by` (masks the lapse — Open Q#7).**
   Judge escalation by the STRUCTURAL block, not the file's live deadline:
   - **SPCX:** check bar count via `cli simulate equity_trend_following_ema_cross
     --symbol SPCX` — needs ≥60 (had 16 on 7/07). Will not clear until ~Sept.
     Keep ESCALATED, keep quarantined. Do NOT auto-remove.
   - **QCOM & SYNA:** their orig. 7/10 deadline has now passed AND they are
     structurally un-validatable (un-backtestable responders). **Both are now
     hard-escalation-due — keep under Open Q#7, keep quarantined.**
   All three: never let trade unvalidated, never auto-remove.

2. **Confirm interpreter + git-sync infra.** If bare `python3 ... list-active` still
   errors `No module named 'requests'`, use `.venv/bin/python3` and re-flag Q#1.
   Check `.git-sync-queue/` for marker pile-up (only Jun-1 test files on 7/07 →
   LaunchAgent OK).

3. **Archive sweep.** Re-run `cli evaluate-archive` on all 8 active-set equity
   strategies. All KEEP on 7/07.

4. **Re-tag check (optional).** Verify `gap-registry coverage_holes: []` still holds.
   If the operator added/removed strategies, re-apply the options `gap_types` tagging
   from `research_log/2026-06-16.md` §1.

5. **Do NOT run head-to-head first-pass validations** (ARM/MRVL/INTC/CSCO/HPE/DELL/
   META/MSFT/AVGO/MU/ORCL) — degenerate 0-trade tiebreak (Open Q#3). Record, hold.
   MSFT & ARM remain NEGATIVE-fit claims (macd −0.274/13tr on MSFT; breakout
   −1.154/12tr on ARM) — best candidates for a dedicated responder once the
   num_trades floor lands. Hold.

6. **If the operator ships any of the structural fixes below,** the whole gap
   backlog unblocks at once (num_trades floor → PEAD/index-rebalance/FOMC become
   testable; news-replay fixture → event_driven adjudicable; options-chain fixture →
   vol strategies + SPCX testable). Re-attempt the relevant candidates that day.

## Open questions for the operator (unanswered — escalating)

1. **[HIGH] Repoint scheduled tasks/prompts to `.venv/bin/python3`** (or reinstall
   harness deps into Homebrew 3.14, or pin Python). Bare `python3` dead for the
   harness since 6/11. Affects trader, news, AND research tasks. The
   `weekly_research_prompt.md` "no virtualenv" line is stale.

2. **`num_trades ≥ 20` floor (5th+ week).** Unreachable on single-symbol simulate
   (max ~16 on META/macd). Blocks every realistic ADD candidate, incl. PEAD
   (quarterly, cross-sectional), index-rebalance (0–1/symbol), FOMC (~8/yr),
   VIX-regime flips. Suggested: (b) multi-symbol aggregation in `simulate`, or
   (a) lower floor to ~10.

3. **Head-to-head degenerate 0-trade tiebreak (4th+ week).** A 0-trade strategy
   "wins" on Sharpe=0 / smaller-DD vs any negative-Sharpe active trader; a 1-trade
   strategy wins on a fluke. Invalidates all outstanding first-pass-claim
   validations. Suggested: "both < ~5 trades ⇒ winner: null."

4. **Event/overlay architecture (5th+ week) — SINGLE BIGGEST GAP-CLEARING BLOCKER.**
   Nearly every recurring library gap (event_catalyst on price-claimed names:
   regulatory/antitrust, restructuring, capital-return, pricing/margin,
   product-line, short-interest, litigation; earnings-window assignment;
   index-rebalance/forced-flow; macro/FOMC) is an *overlay primitive*, *claim-set
   broadening*, or *new category* — NOT a standalone `propose-strategy` addition.
   Needs an architectural decision or these stay open forever.

5. **`event_driven_catalyst` un-backtestable.** Enters on a non-replayable
   `news_brief` signal → 0 trades in every sim; `rolling_sharpe null` even after
   MU's 6/24 print. Needs a backtest news-replay fixture, or it can never be
   adjudicated by any battery / head-to-head — and QCOM (its provisional) can never
   validate.

6. **`_load_news_brief()` staleness guard** (trader-logged code fix). A stale brief is
   fed to strategies as live signal (no `date_in_file == today` check).

7. **[ESCALATED — all 3 provisionals structurally un-validatable + auto-extending
   deadline masks the lapse.]** The doctrine's "escalate once `revalidate_by` passes"
   never fires because each mandatory `cli triage-symbol` RE-STAMPS `revalidate_by`
   (7/07: SPCX 7/04→7/21; QCOM 7/10→7/21; SYNA 7/10→7/21). All three are permanently
   un-validatable by the current machinery:
   - **SPCX:** needs ~60 trading bars (~Sept, IPO) before *any* equity backtest, AND
     gap_type `volatility_regime` has only options responders (no chain data).
   - **QCOM:** sole responder `event_driven_catalyst` is un-backtestable (0 trades
     always) → Sharpe pinned at 0.0.
   - **SYNA:** sole responder `pairs_cointegration` needs the short-ON leg; single-
     symbol sim = 0 trades → Sharpe pinned at 0.0.
   Operator decision needed, per symbol: (a) build the missing backtest fixture
   (options-chain for SPCX/vol; news-replay for QCOM; pairs-spread/second-leg for
   SYNA); (b) set a FIXED, non-auto-extending deadline (e.g. SPCX ~Sept for bar
   accrual) so escalation actually fires; (c) reassign the symbol to an
   equity-backtestable gap_type; or (d) remove from universe (operator's call —
   research never auto-removes). Until then all three correctly stay quarantined
   (never trade) but will never validate. **Fix the auto-extension masking first —
   it hides every future lapse.**
