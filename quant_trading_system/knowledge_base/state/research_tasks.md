# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update (2026-07-08)

- **RUN VIA `.venv/bin/python3`.** Bare `python3` = Homebrew 3.14.5, no deps (`No module named
  'requests'`). Working interpreter: `.venv/bin/python3` (3.13.13). Operator hasn't repointed. (Open Q#1.)
- **This run fired Wednesday 7/8, off-cycle** (schedule-timing issue). Ran the full workflow anyway.
- **Library:** 20 strategies (12 equity incl. `equity_watch_only`, 8 options). All `active`. 0 archived.
  `gap-registry coverage_holes: []`. **Adds/updates/archives this run: 0 / 0 / 0** (correct no-op on
  membership; no novel candidate is backtestable on the daily/single-symbol/next-open engine). See
  `research_log/2026-07-08.md`.
- **BIG CHANGE — provisional_count 7 → 3.** 4 provisionals CONVERTED to validated via UNRESTRICTED triage
  (last week's "structurally un-validatable" was a gap-type-filter artifact — see manual feedback 2026-07-08):
  - **SMCI** → `equity_mean_reversion_bollinger` (0.814 / 5 trades) — trades Monday.
  - **RKLB** → `equity_breakout_volume_confirmation` (1.059 / 9 trades) — trades Monday.
  - **BE**   → `equity_breakout_volume_confirmation` (1.483 / 6 trades) — trades Monday.
  - **IRDM** → `equity_breakout_volume_confirmation` (0.832 / 9 trades) — trades Monday.
  Incumbents shrunk to preserve live claims: `event_driven_catalyst` → {AVGO,MU,ORCL,QCOM};
  `pairs_cointegration` → {SYNA}. Provisional markers cleared via `memory.clear_provisional_claim` (harness
  doesn't auto-clear cross-strategy claims — Open Q#8).
- **Archive sweep:** all 8 active-set equity strategies → KEEP. trend_following HEALTHY (rolling Sharpe 6.25,
  PSR 0.87, 10 trades). event_driven_catalyst still 0 trades in window (will gain evidence once 7/8 exits log).
- **Web research:** PEAD (needs EPS-surprise fundamentals + quarterly < 20-trade floor) and generic
  Quantpedia breakout/momentum (redundant or intraday) — both foregone. Overnight-drift assessed and rejected
  (collapses to 1-day momentum on a next-open-fill engine). No battery run. Log §"Web research".
- **git-sync infra:** `.git-sync-queue/` has only Jun-1 test files → LaunchAgent healthy.

## PROVISIONAL claims remaining — 3 (PRIORITY ZERO next Saturday)

- **QCOM** (event_driven_catalyst, event_catalyst): HELD. Unrestricted triage → `mean_reversion_bollinger`
  0.817 but **only 3 trades** (<5 → fluke-prone). `revalidate_by 2026-07-21` (NOT auto-extended — scored with
  `--no-claim`). **Not** structurally un-validatable anymore — just thin.
- **SYNA** (pairs_cointegration, pairs_arbitrage): HELD. Unrestricted triage → `rsi_divergence` 0.731 but
  **only 4 trades** (<5). `revalidate_by 2026-07-21` (not auto-extended). Thin, not blocked.
- **SPCX** (trend_following, volatility_regime): ESCALATED (structural). 17 bars < 60 → un-backtestable until
  ~September (IPO bar accrual). `revalidate_by 2026-07-21` (not auto-extended). Keep quarantined. Open Q#7.

## To do this Saturday

1. **PRIORITY ZERO — re-run UNRESTRICTED `--no-claim` triage on all 3 remaining provisionals.**
   `cli triage-symbol QCOM --no-claim`, `... SYNA --no-claim`, `... SPCX --no-claim`. (Use `--no-claim` so you
   don't auto-extend `revalidate_by` for the ones you hold — manual feedback 2026-07-08.)
   - **QCOM / SYNA:** if the winner now shows **≥5 trades** and clears baseline 0.5 → CONVERT: `add-active
     <incumbent> --replace --symbols <kept-only>` to release the symbol (event_driven keeps AVGO,MU,ORCL;
     pairs keeps nothing else — it'd become empty, so instead just release SYNA and let pairs hold whatever
     remains, or archive-consider pairs if it ends with 0 symbols), then `cli triage-symbol <SYM>` (auto-claim)
     + verify `provisional_count` dropped (else `memory.clear_provisional_claim('<SYM>')`). If still <5 trades,
     HOLD again. If their **original 2026-07-21** deadline has passed and still <5 trades, escalate as
     "borderline: clears baseline on <5 trades — accept thin sample or relax num_trades? (operator)".
   - **SPCX:** check `cli simulate equity_trend_following_ema_cross --symbol SPCX` bar count; needs ≥60 (had 17
     on 7/8). Keep ESCALATED + quarantined until it accrues 60 bars (~Sept). Do NOT auto-remove.
   - NB: if you release SYNA from `pairs_cointegration` and it becomes the strategy's ONLY claim removed, pairs
     may end with an empty claim list — decide whether to leave it claimless (fine, it's a library strategy) or
     note it. Don't archive it (still `active`, un-backtestable, no journal evidence → archive battery = KEEP).

2. **Confirm interpreter + git-sync infra.** Bare `python3 ... list-active` should still error
   `No module named 'requests'` → use `.venv/bin/python3`, re-flag Q#1. Check `.git-sync-queue/` for pile-up.

3. **Archive sweep.** Re-run `cli evaluate-archive` on all 8 active-set equity strategies. All KEEP on 7/8.
   **Watch event_driven_catalyst:** once the 7/8 AVGO/MU/ORCL exits are logged (log-closed by the trader), it
   gains lifetime trading evidence and becomes archive-evaluable — check its rolling Sharpe/PSR then.
   Also newly-evaluable soon: mean_reversion_bollinger (SMCI) + breakout_volume_confirmation (RKLB/BE/IRDM)
   once they trade.

4. **Re-tag check (optional).** Verify `gap-registry coverage_holes: []` still holds; re-apply options
   `gap_types` tagging from `research_log/2026-06-16.md` §1 if the operator added/removed strategies.

5. **Do NOT run head-to-head first-pass validations** (ARM/MRVL/INTC/CSCO/HPE/DELL/META/MSFT/SNDK + trend
   placeholders) — degenerate 0-trade tiebreak (Open Q#3). Record, hold. MSFT & ARM remain NEGATIVE-fit
   claims — best candidates for a dedicated responder once the num_trades floor lands. Hold.

6. **If the operator ships any structural fix,** the backlog unblocks: num_trades floor → PEAD/index-rebalance
   testable; news-replay fixture → event_driven adjudicable + QCOM's gap_type responder validatable; options-chain
   fixture → vol strategies + SPCX testable; clear-provisional-on-claim fix (Q#8) → no more manual marker clearing.

## Open questions for the operator (unanswered — escalating)

1. **[HIGH] Repoint scheduled tasks/prompts to `.venv/bin/python3`** (or reinstall harness deps / pin Python).
   Bare `python3` dead for the harness since 6/11. `weekly_research_prompt.md` "no virtualenv" line is stale.

2. **[num_trades ≥ 20 floor]** Blocks every realistic `evaluate-add` candidate (PEAD quarterly, index-rebalance
   0–1/symbol). NB: triage's baseline check is Sharpe-only (validated SMCI on 5 trades), so the 20-floor bites
   only the addition battery, not claims. Suggested: multi-symbol aggregation in `simulate`, or lower to ~10.

3. **[head-to-head 0-trade tiebreak]** A 0-trade strategy "wins" on Sharpe=0 / smaller-DD vs any negative-Sharpe
   trader; noise on any `event_driven_catalyst` symbol. Suggested: "both < ~5 trades ⇒ winner: null."

4. **[event/overlay architecture — SINGLE BIGGEST GAP-CLEARING BLOCKER]** Nearly every recurring gap
   (customer-win, competitor read-through, regulatory/antitrust, product-launch, earnings-window assignment,
   index-rebalance/forced-flow, macro/FOMC) is an overlay primitive / claim-broadening / new category — NOT a
   standalone `propose-strategy` addition. Needs an architectural decision or these stay open forever.

5. **[event_driven_catalyst + pairs_cointegration un-backtestable]** event_driven enters on a non-replayable
   `news_brief` signal → 0 trades in every sim; pairs needs the short leg modeled → 0 trades on single-symbol
   sim. Neither can be adjudicated by any battery/head-to-head. Needs a news-replay fixture and a
   pairs-spread/second-leg model. (Consequence: their gap_types' *sole* responder can't validate; provisionals
   whose gap_type points only at these can only be cleared by unrestricted triage to a different family.)

6. **[fallback-threshold, minor]** 0-trade Sharpe-0.0 backtest attaches a below-baseline *trading* provisional
   rather than `equity_watch_only`. Partly mooted (unrestricted triage found real responders for all 4 new
   names 7/8), but still an open policy call: should a degenerate 0-trade score route to watch_only?

7. **[ESCALATED — SPCX only remaining structural provisional]** 17 bars < 60 → un-backtestable until ~Sept.
   Per-symbol operator options: (a) set a FIXED, non-auto-extending ~Sept deadline for bar accrual so
   escalation actually fires; (b) reassign SPCX to an equity-backtestable gap_type; or (c) remove from universe
   (operator's call — research never auto-removes). Until then it correctly stays quarantined (never trades).
   NOTE: `--no-claim` scoring now avoids the auto-extension that masked the lapse (manual feedback 2026-07-08).

8. **[NEW, MEDIUM] Cross-strategy validated claim doesn't clear the provisional marker.**
   `agent_tools.triage_symbol`'s `verdict:"claimed"` path clears library-gap but not provisional markers, so a
   symbol validly re-claimed by a *different* strategy stays execution-quarantined until
   `memory.clear_provisional_claim(sym)` is called by hand. Fix: clear any provisional marker for the claimed
   symbol in the claim path, regardless of which strategy previously held it. (Worked around manually 7/8.)

9. **[_load_news_brief() staleness guard]** (trader-logged) A stale brief can be fed to strategies as live
   signal — no `date_in_file == today` check.
