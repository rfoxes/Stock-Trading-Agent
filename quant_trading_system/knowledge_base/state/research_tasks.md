# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## ⚡ OPERATOR DIRECTIVE (2026-07-19) — SHORT-HORIZON MANDATE IS LIVE

The harness has transitioned to trading on a shorter timeline (days to a
few weeks — typically ~2-15 trading days; swing, not day trading). **Read
`research_manual.md` §"Short-horizon mandate" before this run.** Priority order is now:
(1) provisionals, (2) library gaps, (3) NEW short-horizon migration
workstream, (4) generic candidates. Concretely, starting this Saturday:

- **Migration kickoff:** begin head-to-head challenges of the best
  short-horizon strategies against `timeframe: position` incumbents'
  claims — `equity_trend_following_ema_cross` (AAPL/AMZN/CBRS/GOOGL/JPM/
  NUVL/NVDA/QQQ/SPY/TSLA/TSM), `equity_sector_rotation_momentum` (DELL).
  A few symbols per Saturday is fine. ALL standing guards apply (≥5
  trades on the deciding side; no 0-trade degenerate tiebreaks — this is
  the same Open Q#3 caution as before, so where both sides can't produce
  ≥5 trades, record-and-hold rather than churn). Incumbents that keep
  winning keep their claims.
- **Sourcing:** the operator has ALREADY seeded a cited, engine-screened
  candidate backlog at **`state/research_candidates.md`** (researched
  2026-07-19: RSI(2) pullback, Double 7s, IBS-filter `_v2` on bollinger,
  N-day washout reversal, gap+volume post-event drift [the replayable
  PEAD proxy — also a rankable challenger for the nine event-driven
  provisionals], turn-of-month on SPY/QQQ, 52wk-high momentum; plus a
  considered-and-rejected list). Work it a few entries per Saturday in
  the rank-3 slot — cheapest first (`_v2` update-path IBS filter), then
  the high-frequency Tier 1. Batteries decide; delete entries as
  verdicts land. New strategies must declare `timeframe:` + a time-stop
  rule (holds ≤ ~15 sessions).
- Provisional revalidation and gap-clearing are UNCHANGED and still come
  first. Batteries and thresholds unchanged; verdicts verbatim.

A new prompt file (`weekly_research_prompt_short_term.md`) exists for the
operator to paste into the scheduled task; until then this note + the
manual carry the directive. Keep this block until the operator confirms
the new prompt is pasted, then drop it.

## Status as of the last update (2026-07-11, committed 2026-07-13)

- **RUN VIA `.venv/bin/python3`.** Bare `python3` = Homebrew 3.14.5, no deps (`No module named 'requests'`).
  Working interpreter: `.venv/bin/python3` (3.13.13). Operator still hasn't repointed. (Open Q#1.)
- **This run started Saturday 7/11 and committed Monday 7/13** (session spanned the weekend; git-sync deferred).
  No trader run intervened (last commit `[trader 2026-07-10]`); working tree held exactly the 7/11 mutations,
  re-verified intact before commit. Not a re-run — one cycle, delayed commit.
- **Library:** 20 strategies (12 equity incl. `equity_watch_only`, 8 options). All `active`. 0 archived.
  `gap-registry coverage_holes: []`. **Adds/updates/archives this run: 0 / 0 / 0** (correct no-op — no novel
  candidate is backtestable on the daily/single-symbol/next-open engine that isn't data-blocked, trade-floor-
  blocked, or an update-variant of an existing strategy). See `research_log/2026-07-11.md`.
- **provisional_count 5 → 4. WULF CONVERTED** to `equity_rsi_divergence` (unrestricted triage 0.880 Sharpe / 12
  trades ≥ baseline). Released from `equity_event_driven_catalyst` via `add-active --replace --symbols
  AVGO,MU,ORCL,QCOM`, then `triage-symbol WULF` auto-claim; provisional marker cleared by hand via
  `memory.clear_provisional_claim('WULF')` (Open Q#8 bit again). WULF trades Monday under rsi_divergence (+HPE).
- **Archive sweep:** all 8 active-set equity strategies → KEEP. `event_driven_catalyst` is NOW archive-evaluable
  (3 `trade_closed` from the 7/8→7/9 AVGO/MU/ORCL exits) and passed KEEP (3 trades/90d, no trigger).
  `trend_following` healthy (rolling Sharpe 6.25, PSR 0.87, 10 trades). Freshly-deployed breakout/bollinger/rsi/
  sector/pairs → KEEP on "no trading evidence yet."
- **Web research:** PEAD/earnings (data + <20-trade blocked; but confirms `event_driven`'s max_hold_days=7 sits
  inside the empirical 5–20d PEAD drift window → defensible, no recalibration) and a Quantpedia June-2026
  trend-filtered short-term reversal (overlaps mean_reversion/rsi = update-variant; too selective to clear the
  20-trade floor) — both foregone, no battery run. Log §"Web research".
- **git-sync infra:** `.git-sync-queue/` has only Jun-1 test files → LaunchAgent healthy.

## PROVISIONAL claims remaining — 4 (PRIORITY ZERO next Saturday)

- **QCOM** (event_driven_catalyst, event_catalyst): HELD. Unrestricted triage → `mean_reversion_bollinger` 0.817
  but **only 3 trades** (<5 → fluke-prone). `revalidate_by 2026-07-21` (NOT auto-extended — scored `--no-claim`).
  Not structurally blocked — just thin.
- **SYNA** (pairs_cointegration, pairs_arbitrage): HELD. Unrestricted triage → `rsi_divergence` 0.731 but **only 4
  trades** (<5). `revalidate_by 2026-07-21` (not auto-extended). Thin, not blocked. NB: SYNA is pairs' ONLY claim
  — if it converts, pairs ends claimless (fine; don't archive it — `active`, no journal evidence → battery KEEP).
- **SPCX** (trend_following, volatility_regime): ESCALATED (structural). **19 bars < 60** (was 17 on 7/8, ~+1/wk)
  → un-backtestable until ~Sept/Oct. `revalidate_by 2026-07-21` (not auto-extended). Keep quarantined. Open Q#7.
- **SKHY** (equity_watch_only, event_catalyst): HELD (no history). 0 bars on 7/11 (permanent ticker began
  regular-way trading 7/13). `revalidate_by 2026-07-24`. **Structural like SPCX:** needs ~60 bars (~mid-Oct), so
  its 7/24 deadline will lapse first. Correct no-history → watch_only fallback (issue #5). Open Q#7 (extend to SKHY).

## To do this Saturday (2026-07-18)

1. **PRIORITY ZERO — re-run UNRESTRICTED `--no-claim` triage on all 4 provisionals.**
   `cli triage-symbol QCOM --no-claim`, `... SYNA --no-claim`, `... SPCX --no-claim`, `... SKHY --no-claim`.
   (Use `--no-claim` so you don't auto-extend `revalidate_by` on the ones you HOLD — manual feedback 2026-07-08.)
   - **QCOM / SYNA:** if the winner now shows **≥5 trades** AND clears baseline 0.5 → CONVERT (same mechanism as
     WULF this week: `add-active <incumbent> --replace --symbols <kept-only>` to release just the symbol, then
     `cli triage-symbol <SYM>` auto-claim, then VERIFY `provisional_count` dropped — if not, `memory.
     clear_provisional_claim('<SYM>')`; Open Q#8). If still <5 trades → HOLD.
     **NB deadline 2026-07-21 falls THIS coming week:** if 7/18 triage still shows <5 trades and you expect the
     7/21 deadline to lapse before the following Saturday (7/25), ESCALATE now as "borderline: clears baseline on
     <5 trades — accept thin sample or relax the num_trades floor? (operator)". Don't let it drift past 7/21 silent.
   - **SPCX:** `cli simulate equity_trend_following_ema_cross --symbol SPCX` bar count; needs ≥60 (had 19 on 7/11,
     ~1/wk → still ~40 short). Keep ESCALATED + quarantined. Do NOT auto-remove.
   - **SKHY:** `cli simulate ... --symbol SKHY` bar count (will have ~4–5 bars from the 7/13 regular-way start).
     Keep on `equity_watch_only`, quarantined. Structural until ~60 bars (~mid-Oct); 7/24 deadline will lapse —
     escalate alongside SPCX (operator: fixed non-auto-extending accrual deadline, or accept the long quarantine).

2. **Confirm interpreter + git-sync infra.** Bare `python3 ... list-active` should still error `No module named
   'requests'` → use `.venv/bin/python3`, re-flag Q#1. Check `.git-sync-queue/` for pile-up (only Jun-1 test
   markers = healthy).

3. **Archive sweep.** Re-run `cli evaluate-archive` on all 8 active-set equity strategies. All KEEP on 7/11.
   **Newly-evaluable to watch:** `event_driven_catalyst` (now has 3 closed trades; rolling Sharpe was null —
   re-check once ≥ a few more closes accumulate), and `mean_reversion_bollinger` (SMCI/CSCO) +
   `breakout_volume_confirmation` (ARM/BE/INTC/IRDM/MRVL/RKLB) + `rsi_divergence` (HPE/WULF) once they trade and
   log journal evidence.

4. **Re-tag check (optional).** Verify `gap-registry coverage_holes: []` still holds; re-apply options `gap_types`
   tagging from `research_log/2026-06-16.md` §1 if the operator added/removed strategies. (No-op 7/11.)

5. **Do NOT run head-to-head first-pass validations** (ARM/MRVL/INTC/CSCO/HPE/DELL/META/MSFT/SNDK + trend
   placeholders) — degenerate 0-trade tiebreak (Open Q#3). Record, hold.

6. **If the operator ships any structural fix,** the backlog unblocks: num_trades floor → PEAD/index-rebalance
   testable; news-replay fixture → event_driven adjudicable + QCOM's gap_type responder validatable; options-chain
   fixture → vol strategies + SPCX/SKHY testable sooner; clear-provisional-on-claim fix (Q#8) → no more manual
   marker clearing.

## Open questions for the operator (unanswered — escalating)

1. **[HIGH] Repoint scheduled tasks/prompts to `.venv/bin/python3`** (or reinstall harness deps / pin Python).
   Bare `python3` dead for the harness since 6/11. `weekly_research_prompt.md` "no virtualenv" line is stale.

2. **[num_trades ≥ 20 floor]** Blocks every realistic `evaluate-add` candidate (PEAD quarterly, index-rebalance
   0–1/symbol, trend-filtered pullback too selective). NB: triage's baseline check is Sharpe-only (WULF validated
   on 12 trades, SMCI on 5), so the 20-floor bites only the addition battery, not claims. Suggested: multi-symbol
   aggregation in `simulate`, or lower to ~10.

3. **[head-to-head 0-trade tiebreak]** A 0-trade strategy "wins" on Sharpe=0 / smaller-DD vs any negative-Sharpe
   trader; noise on any `event_driven_catalyst` symbol. Suggested: "both < ~5 trades ⇒ winner: null."

4. **[event/overlay architecture — SINGLE BIGGEST GAP-CLEARING BLOCKER]** Nearly every recurring gap
   (customer-win, competitor read-through, regulatory/antitrust, product-launch, earnings-window assignment,
   index-rebalance/forced-flow, macro/FOMC, capex-commitment) is an overlay primitive / claim-broadening / new
   category — NOT a standalone `propose-strategy` addition. Needs an architectural decision or these stay open.

5. **[event_driven_catalyst + pairs_cointegration un-backtestable]** event_driven enters on a non-replayable
   `news_brief` signal → 0 trades in every sim; pairs needs the short leg modeled → 0 trades on single-symbol sim.
   Neither can be adjudicated by any battery/head-to-head. Needs a news-replay fixture and a pairs-spread/second-leg
   model. (Consequence: their gap_types' *sole* responder can't validate; such provisionals can only be cleared by
   unrestricted triage to a different family — as WULF was this week.)

6. **[fallback-threshold, minor]** 0-trade Sharpe-0.0 backtest attaches a below-baseline *trading* provisional
   rather than `equity_watch_only`. Largely mooted (unrestricted triage found real responders for WULF/SMCI/RKLB/
   IRDM/BE), but still an open policy call: should a degenerate 0-trade score route to watch_only? (No-history
   already routes there correctly — SKHY.)

7. **[ESCALATED — SPCX + SKHY structural provisionals]** Both un-backtestable until ~60 bars accrue: SPCX 19 bars
   (~Sept/Oct), SKHY 0→~5 bars (~mid-Oct). Their `revalidate_by` (7/21, 7/24) will lapse well before then.
   Per-symbol operator options: (a) set a FIXED, non-auto-extending accrual deadline (~Oct) so escalation actually
   fires on time; (b) reassign to an equity-backtestable gap_type; or (c) remove from universe (operator's call —
   research never auto-removes). Until then both correctly stay quarantined (never trade). `--no-claim` scoring
   avoids the auto-extension that masks the lapse (manual feedback 2026-07-08).

8. **[MEDIUM] Cross-strategy validated claim doesn't clear the provisional marker.** `agent_tools.triage_symbol`'s
   `verdict:"claimed"` path clears library-gap but not provisional markers, so a symbol validly re-claimed by a
   *different* strategy stays execution-quarantined until `memory.clear_provisional_claim(sym)` is called by hand.
   Bit again on WULF this week (worked around). Fix: clear any provisional marker for the claimed symbol in the
   claim path, regardless of which strategy previously held it.

9. **[_load_news_brief() staleness guard]** (trader-logged) A stale brief can be fed to strategies as live signal
   — no `date_in_file == today` check. Bit the trader on 7/10 (brief stayed dated 7/9). Add the guard.
