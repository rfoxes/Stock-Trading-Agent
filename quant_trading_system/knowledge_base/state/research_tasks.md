# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update (2026-06-16)

- **RUN VIA `.venv/bin/python3`, NOT bare `python3`.** Homebrew upgraded
  `/opt/homebrew/bin/python3` to 3.14.5 on 6/11; it has none of the harness
  deps, so every CLI call (incl. `git-sync`) fails `No module named 'requests'`.
  The working interpreter is `.venv/bin/python3` (Python 3.13.13, all deps).
  This last run and the trader's daily runs all use the venv. See
  `research_log/2026-06-16.md` §0.
- **Library size:** 19 strategies on disk (11 equity, 8 options). All `active`.
  0 archived.
- **Last week's adds/updates/archives:** none (all three zero — correct).
- **One metadata fix applied:** tagged 4 options strategies (`iron_condor_high_iv`,
  `jade_lizard`, `calendar_spread`, `long_straddle_earnings`) with `gap_types`
  → closed the `volatility_regime` registry coverage hole. `gap-registry` now
  reports `coverage_holes: []`.
- **Archive sweep:** 11/11 active equity strategies → KEEP.
- **Head-to-head:** ran 11 contested first-pass claims vs `trend_following`.
  Validated META/macd (0.043,16tr) and MRVL/breakout (1.31,8tr) solidly; HPE/CSCO/
  ORCL hold on thin evidence. **No reassignments** — every "trend_following wins"
  was degenerate (0-trade inaction or 1-trade fluke). Active set UNCHANGED.
- **Active set:** 7 strategies × 22/22 claimed (`unclaimed_count == 0`).
  `state/library_gaps.md` empty. No symbol-level gaps.
- **Structural blocker (3rd wk):** addition battery `num_trades ≥ 20` unreachable
  on single-symbol simulate. No operator response.

## To do this Saturday

1. **Confirm interpreter fix.** If bare `python3 -m quant_trading_system.cli
   list-active` still errors `No module named 'requests'`, the operator hasn't
   repointed the tasks — keep using `.venv/bin/python3` and re-flag as P0. If a
   `.git-sync-queue/` marker pile-up appears, also note the gitrunner LaunchAgent.

2. **Re-tag check (optional).** Verify `gap-registry` still `coverage_holes: []`.
   If the operator added/removed strategies, re-run the options `gap_types`
   tagging logic from `research_log/2026-06-16.md` §1.

3. **MSFT and ARM are NEGATIVE-fit claims — find a real responder, do NOT dump
   on trend_following.** Head-to-head this week: macd loses on MSFT
   (Sharpe −0.274/13tr); breakout loses on ARM (−1.154/12tr). `trend_following`
   only "wins" by doing 0 trades. These two are the best candidates for a
   *dedicated* responder once the `num_trades` floor or a new template lands.

4. **Do NOT re-run head-to-head on event_driven_catalyst symbols (AVGO/MU/ORCL).**
   Confirmed structurally un-backtestable: it enters on `news_brief` signal the
   backtester can't replay → 0 trades in every sim. Re-running is pure noise.
   Same for any 0-trade-vs-0-trade pair until open-q #3 (tiebreak) is fixed.

5. **MU Q3 FY26 print Tue 6/24 AMC.** After the print, `event_driven_catalyst`'s
   MU claim may finally get a *closed-trade* data point. Re-run
   `evaluate-archive equity_event_driven_catalyst` the following Saturday — it
   may then have real rolling-window evidence (currently rolling_sharpe null).

6. **News pipeline down since ~6/11.** Brief stale at 6/15, no 6/16 brief —
   likely the same interpreter outage. If still stale next Saturday, raise as a
   joint P0 with the operator (no live brief ⇒ event_driven_catalyst can't fire
   AND `_load_news_brief` feeds stale data as live — see open-q below).

7. **Archive sweep.** Re-run `evaluate-archive` on every `status: active` equity
   strategy. All KEEP this week.

## Open questions for the operator (unanswered — escalating)

1. **[NEW — HIGH] Repoint scheduled tasks/prompts to `.venv/bin/python3`,** or
   reinstall harness deps into Homebrew Python 3.14, or pin Python. Bare
   `python3` is dead for the harness as of 6/11. Affects trader, news, AND
   research scheduled tasks. The `weekly_research_prompt.md` "no virtualenv"
   line is now wrong.

2. **`num_trades ≥ 20` floor (3rd week).** Unreachable on single-symbol simulate
   (max observed ~16 on META/macd). Blocks every realistic ADD candidate.
   Suggested: (b) multi-symbol aggregation in `simulate`, or (a) lower floor ~10.

3. **Head-to-head degenerate 0-trade tiebreak (open-q, 2nd+ week).** A 0-trade
   strategy "wins" on Sharpe=0 / smaller-drawdown vs any negative-Sharpe active
   trader, and a 1-trade strategy "wins" on a fluke. Would have wrongly churned
   6 symbols this week. Suggested: "both <2 trades ⇒ winner: null."

4. **Event/overlay architecture (open-q, 3rd+ week).** Most real library gaps
   (macro_event_window/FOMC, export-control shock, underwriter_franchise,
   m_a_arbitrage, event_window_posture, keyword-detector asymmetry) are *overlay
   primitives* or *code fixes*, not standalone strategies — outside
   `propose-strategy`. Need an architectural decision or they stay open forever.

5. **`event_driven_catalyst` un-backtestable.** Needs a backtest news-replay
   fixture, or it can never be adjudicated by any battery / head-to-head.

6. **`_load_news_brief()` staleness guard** (trader-logged, code fix). Acute now
   that briefs are stale 6/11–6/15: stale briefs are fed to strategies as live
   signal. Reject/down-weight a brief whose `date_in_file != today`.
</content>
