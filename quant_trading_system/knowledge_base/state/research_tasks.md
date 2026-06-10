# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update

- **Library size:** 19 strategies on disk (11 equity, 8 options). All
  `status: active`. 0 archived. (`equity_event_driven_catalyst` flipped
  from `testing` → `active` mid-week by operator.)
- **Last week's additions:** none.
- **Last week's updates/archives:** none.
  - 1 add attempted: `equity_momentum_macd_histogram_v3` (3-bar exit
    confirmation as min-hold proxy) — REJECTED by addition battery
    (num_trades 16 < 20, PSR 0.380, sortino -0.220, OOS/IS overfit) AND
    KEEP by replacement battery (sharpe delta -0.276, p=0.624). Cleaned up.
  - 13 canonical head-to-head verdicts re-run (see
    `research_log/2026-06-10.md`). Three new substantive results vs the
    6/6 run: INTC swap recommended (breakout_vol → trend_following), NUVL
    swap recommended (trend_following → event_driven_catalyst), ORCL claim
    confirmed (event_driven_catalyst retains).
  - Archive sweep: all 11 active equity strategies returned KEEP.
- **Active set:** 7 strategies × 22/22 claimed (`unclaimed_count == 0`).
  Trader did NOT apply the 6/6 swap recommendations Monday; instead
  preserved the first-pass character-match assignments and added 3 new
  universe symbols via direct YAML edit (`add-active` is buggy). P0
  unclaimed-gate is preserved.
- **Backtester:** all CLI paths still working end-to-end.
- **Outstanding calibration question: addition battery's
  `min_num_trades = 20` is unreachable on single-symbol simulate.**
  Continues to be the dominant structural blocker. v3's REJECT this week
  was triggered first by `num_trades 16 < 20`. No operator response.

## To do this Saturday

1. **Verify trader applied the 6/10 swap recommendations.**
   Run `cli list-active`. Expected outcome (if trader executed):
   - `equity_trend_following_ema_cross` claims INTC (gained from
     breakout_volume_confirmation).
   - `equity_event_driven_catalyst` claims NUVL (gained from
     trend_following_ema_cross).
   - All other claims unchanged.
   If trader did NOT swap, examine `state/last_handoff.md` for the reason
   and re-document in this Saturday's log.

2. **Re-run head-to-head on the still-contested pairs (the 6/6 recs
   trader didn't apply).** With another week of journal data, MSFT, ARM,
   AVGO, MU, DELL may now show real signal:
   - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross`
     on MSFT
   - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross`
     on ARM
   - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross`
     on AVGO, MU (MU especially — prints 6/24)
   - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross`
     on DELL

3. **MU post-print check (6/24).** If MU printed Tuesday 6/24, the
   `equity_event_driven_catalyst` claim on MU has its first real lifetime
   data point. Re-run `cli evaluate-archive equity_event_driven_catalyst`
   — should now have meaningful trade history. If the strategy stopped
   the position at $813.44 before the print, the data point is "stop
   triggered" and the strategy didn't fire its on-character rule.

4. **Don't re-attempt MACD v4.** The "minimum-hold" intuition from
   operator does not survive backtest (see this week's log #3). v3 was
   directionally worse than v1 on META. A tighter exit threshold gives
   back winners. Recommend NOT building v4 unless a different mechanism
   (e.g., add-on trailing stop, not delayed exit) is proposed.

5. **Address the `min_num_trades = 20` calibration question.** Still no
   operator response. Two-week-old open question. Consider raising
   priority — every Saturday candidate falls at this same hurdle.

6. **Universe-expansion candidates** carry-forward (STM, VSH, FLEX, PINS,
   CRWD). News brief Tue 6/9 showed: ORCL + NUVL promoted; VSH session 1
   tracked; STM session 2; CRWD provisional session 3; FLEX session 2;
   PINS session 2. Defer to operator/news-agent promotion mechanics.

7. **Recurring archive sweep.** Run `cli evaluate-archive` on every
   `status: active` strategy. With `equity_event_driven_catalyst` now
   having lifetime trading evidence (MU buy 6/9), it's now within the
   eligible set for the rolling-Sharpe / 60-day-zero checks.

8. **Verify daily news brief writing resumed.** Trader's Wed 6/10
   handoff shows the news agent did not write a brief for 6/10 (file
   header still 6/9). If the gap persists into next Saturday, raise as
   high-priority operator issue.

9. Write `knowledge_base/research_log/<today>.md` and replace this file
   with next Saturday's task list.

## Open questions for the operator

(Same four as 2026-06-06 — no operator response yet.)

1. **Addition battery's `min_num_trades = 20` floor.** Unreachable on
   single-symbol simulate. Suggested: (a) lower floor to ~10, (b) extend
   simulate to multi-symbol, or (c) extend default window to 3-5 years.
   Suggested: (b).

2. **Event-overlay architecture.** Most pressing real library gaps
   (WWDC, NFP/CPI/FOMC, peer-earnings, tier-1 customer-win, M&A target
   pin) are overlay rules, not standalone strategies. Outside
   `propose-strategy` scope. Architectural decision needed.

3. **Tiebreak semantics on head-to-head when both have 0 trades.** The
   `smaller max_drawdown` tiebreak picks the *silent* strategy by default
   (0-trade max_drawdown is 0.00). This decided the NUVL verdict this
   week. Suggested: change to "if both have 0 trades, return tie
   (`winner: null`)" and let operator decide.

4. **AAPL WWDC June 8-12 (Day-3-5 active this week; ends Fri).** No
   event-window rule. Trader will not adjust posture. Carrying forward;
   cannot be addressed via addition battery without an overlay primitive.

5. **`cli add-active` REPLACE-instead-of-APPEND bug.** Carry-forward from
   trader's open issue #2. Workaround in place (direct YAML edit). Affects
   normal claim modification flow.
