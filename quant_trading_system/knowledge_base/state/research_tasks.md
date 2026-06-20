# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update (2026-06-20)

- **RUN VIA `.venv/bin/python3`, NOT bare `python3`.** Homebrew 3.14.5 still lacks
  harness deps; bare `python3 -m quant_trading_system.cli ...` fails
  `No module named 'requests'`. Working interpreter: `.venv/bin/python3` (3.13.13).
  5th+ run on the venv. Operator hasn't repointed the tasks. (Open Q#1.)
- **Library size:** 19 strategies on disk (11 equity, 8 options). All `active` status.
  0 archived. `gap-registry coverage_holes: []`.
- **This week's adds/updates/archives: none (all three zero — correct).** Every
  library gap this week is an overlay/architecture/activation gap blocked by already-
  escalated structural issues; none is `propose-strategy`-shaped. See
  `research_log/2026-06-20.md` §1–2.
- **PRIORITY-ZERO provisional claim — SPCX:** re-triaged 6/20, still
  **insufficient bars (5 < 60)** — fresh IPO, no backtest possible. Its gap_type
  `volatility_regime` has only options responders (no chain-data backtest). Remains
  PROVISIONAL/quarantined on `equity_trend_following_ema_cross`. The re-triage
  **auto-bumped `revalidate_by` to 2026-07-04** (original was 6/30). NOT escalation-
  due yet (original deadline hadn't passed). Doubly stuck — see To-Do #1 + Open Q#7.
- **Archive sweep:** 7/7 active equity strategies → KEEP (trend_following healthy:
  rolling Sharpe 1.10, PSR 0.56, 7 trades; others have no/thin trading evidence).
- **Head-to-head:** none run, intentional — degenerate 0-trade tiebreak (Open Q#3)
  makes them invalid while it stands. Active set UNCHANGED.
- **Active set:** 7 strategies × 23/23 claimed (`unclaimed_count == 0`),
  `provisional_count == 1` (SPCX). `state/library_gaps.md` → `gaps: []`.
- **Web research:** VIX-regime equity timer and index-rebalance strategy both
  researched and NOT run (foregone REJECT — num_trades floor + claim-conflict; index
  effect is also empirically disappearing per HBS/S&P DJI). Log §2.

## To do this Saturday

1. **PRIORITY ZERO — re-triage SPCX again.** `cli triage-symbol SPCX
   --gap-type volatility_regime`. Check `cli simulate
   equity_trend_following_ema_cross --symbol SPCX` for bar count — it had 5 bars on
   6/20; needs 60 before any equity backtest. **If `revalidate_by` (now 2026-07-04,
   but note the re-triage keeps auto-extending it) has effectively lapsed AND it still
   can't be ranked, ESCALATE under Open Q#7** — do NOT let it trade unvalidated, do
   NOT auto-remove. SPCX won't accrue 60 bars until ~September; flag that the
   auto-extending deadline is masking a permanent block.

2. **Confirm interpreter + git-sync infra.** If bare `python3 ... list-active` still
   errors `No module named 'requests'`, keep using `.venv/bin/python3` and re-flag
   Q#1. Check `.git-sync-queue/` for marker pile-up (none on 6/20 → LaunchAgent OK).

3. **Re-tag check (optional).** Verify `gap-registry coverage_holes: []` still holds.
   If the operator added/removed strategies, re-apply the options `gap_types` tagging
   from `research_log/2026-06-16.md` §1.

4. **MU Q3 FY26 printed Wed 6/24 AMC.** `equity_event_driven_catalyst`'s MU claim may
   finally have a *closed-trade* data point. Re-run `cli evaluate-archive
   equity_event_driven_catalyst` — it may now have real rolling-window evidence
   (was rolling_sharpe null / 0 trades in window on 6/20).

5. **MSFT & ARM remain NEGATIVE-fit claims — do NOT dump on trend_following.** macd
   loses on MSFT (−0.274/13tr), breakout loses on ARM (−1.154/12tr); trend_following
   only "wins" by 0 trades. Best candidates for a *dedicated* responder once the
   num_trades floor (Q#2) or a new template lands. Hold until then.

6. **Do NOT re-run head-to-head on event_driven_catalyst symbols (AVGO/MU/ORCL)** or
   any 0-trade-vs-0-trade pair — pure noise until Q#3 (tiebreak) is fixed.

7. **Archive sweep.** Re-run `cli evaluate-archive` on every `status: active` equity
   strategy. All KEEP on 6/20.

## Open questions for the operator (unanswered — escalating)

1. **[HIGH] Repoint scheduled tasks/prompts to `.venv/bin/python3`** (or reinstall
   harness deps into Homebrew 3.14, or pin Python). Bare `python3` dead for the
   harness since 6/11. Affects trader, news, AND research tasks. The
   `weekly_research_prompt.md` "no virtualenv" line is stale.

2. **`num_trades ≥ 20` floor (4th+ week).** Unreachable on single-symbol simulate
   (max ~16 on META/macd). Blocks every realistic ADD candidate, incl. every
   event-scheduled gap-filler researched this week (FOMC ~8/yr, index-rebalance
   ~4/yr, VIX-regime flips). Suggested: (b) multi-symbol aggregation in `simulate`,
   or (a) lower floor ~10.

3. **Head-to-head degenerate 0-trade tiebreak (3rd+ week).** A 0-trade strategy
   "wins" on Sharpe=0 / smaller-DD vs any negative-Sharpe active trader; a 1-trade
   strategy wins on a fluke. Invalidates all outstanding first-pass-claim
   validations. Suggested: "both < ~5 trades ⇒ winner: null."

4. **Event/overlay architecture (4th+ week).** Nearly every recurring library gap
   (event_catalyst on price-claimed names, semi industrial-policy, index-rebalance/
   forced-flow, macro_event_window/FOMC, AI-capex-crowding, export-control, M&A-arb)
   is an *overlay primitive*, *claim-set broadening*, or *new category* — NOT a
   standalone `propose-strategy` addition. Needs an architectural decision or these
   stay open forever. This is the single biggest blocker to clearing gaps.

5. **`event_driven_catalyst` un-backtestable.** Needs a backtest news-replay fixture,
   or it can never be adjudicated by any battery / head-to-head.

6. **`_load_news_brief()` staleness guard** (trader-logged code fix). A stale brief is
   fed to strategies as live signal (no `date_in_file == today` check).

7. **[NEW] SPCX provisional deadline auto-extends — masks a permanent block.** Each
   `cli triage-symbol SPCX` re-stamps `revalidate_by` (6/30 → 7/04 on 6/20), so the
   doctrine's "escalate once the deadline passes" never fires. SPCX is doubly stuck:
   needs ~60 trading bars (~Sept) before *any* equity backtest, AND its gap_type
   `volatility_regime` has only options responders the backtester can't run (no chain
   data). Operator decision needed: (a) options-chain backtest fixture; (b) a fixed
   (non-auto-extending) ~Sept deadline for IPO bar-accrual; or (c) reassign SPCX to an
   equity-backtestable gap_type. Until then it correctly stays quarantined (never
   trades) but will never validate either.
