# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-05-29, Fri, post-close.)

- **Active strategy:** `equity_trend_following_ema_cross`
  (`since: 2026-05-27`). Unchanged today. No edits to strategy.md
  or strategy.py.
- **Today's `execute`:** 0 intents, 0 submitted, 0 rejected. Quiet
  day — JPM ADX 20.92 stayed above the 20 exit threshold.
- **Yesterday's queued exits both filled at Fri open:**
  - MSFT 44 @ $437.853 (+3.94%, +$731.14, better than $287 estimate)
  - META 28 @ $628.949 (-7.72%, -$1,472.97, worse than -$1,348 estimate)
  - Logged both via `log-closed`. Net realized today: -$742 / -0.66%
    of equity.
- **Holding 8 longs** (all strategy-aligned):
  AAPL +14.70%, AMZN +8.83%, GOOGL +12.34%, JPM -4.39%, NVDA +6.77%,
  QQQ +13.89%, SPY +6.61%, TSLA +7.53%.
- **Account:** equity $112,177.08 (-0.56% vs. Thu), cash -$59,655.12
  (narrowed by $36,876 from the exit fills), buying_power $52,521.96.
- **Regime:** `bull, conf=0.77, adx=26.82` — fifth consecutive
  bull-trending day.
- **Gate verification:** new `safety_gate.py` semantics worked
  correctly on Thu eval AND on Fri live exit window. Two clean
  sessions. No `daily_loss` rejections today.
- **Git-sync:** STILL FAILING. `.git/HEAD.lock` and
  `.git/objects/maintenance.lock` persist; sandbox can't unlink.
  ORIG_HEAD.lock and index.lock appear cleared. Operator: please
  finish clearing those last two and `git push origin main`.

## To do tomorrow (Mon 6/1)

**Monday is a discontinuity day** — full weekend of news, plus
pending Iran framework decision (Trump WH Situation Room meeting)
and live NVDA/Loomer/Tsinghua thread. Read the news_brief carefully.

1. **Read last_handoff.md, then news_brief.md.** Mon open could be
   discontinuous if the Iran framework gets approved/rejected over
   the weekend.

2. **Standard read-and-snapshot** (manual.md §1-2).

3. **No fills to reconcile from Friday.** Both Thu-queued orders
   cleared; no fresh orders submitted today.

4. **Run `execute`.** Two main scenarios:
   - **JPM watch.** ADX 20.92 today (just above 20 threshold).
     If Mon tape pushes it below 20, expect a JPM exit (-$879 est.
     = 0.78% of equity, well under cap; should submit cleanly).
   - **NVDA gap watch.** If the Loomer story escalates over the
     weekend and NVDA gaps down ≥4% at Mon open, the strategy's
     gap-down exit rule will fire.

5. **Verify gate behavior** if any exits trigger. Three sessions
   of correct behavior so far; one more confirms the rescope.

6. **Do NOT revert** the safety_gate.py rescope OR the
   `max_exits_per_run: 5` setting. Both are working as designed.

7. **Try `git-sync` early.** If operator cleared the last two
   locks, three days of carry-over will push together. If still
   blocked, document and stop the git step.

8. **(Optional)** Nudge the Saturday research agent — news brief
   has flagged DELL/NTAP/OKTA/NOW/TEAM (third consecutive
   session) and MU/AVGO/SNOW (recurring) as universe candidates.
   The trader can't act on this but a one-line forward in
   `tasks.md` for the Saturday agent won't hurt.

## Open questions for the operator

1. **Git lock files — second ask.** `.git/HEAD.lock` and
   `.git/objects/maintenance.lock` still present. Please run from
   a real terminal:
   ```
   cd /Users/rfoxes/Stock-Trading-Agent
   rm -f .git/HEAD.lock .git/objects/maintenance.lock
   git push origin main
   ```
   Six files have been waiting three days to push.

2. **Universe expansion.** News layer has flagged
   DELL/NTAP/OKTA/NOW/TEAM for three sessions as candidates.
   Saturday research agent is the right path, but if you want
   any sooner, add to `state/extra_symbols.md`.

3. **Strategy health is small-sample-noisy.** 30-day Sharpe -3.64,
   cum_return -4.08% vs SPY +5.93%. N=2 realized trades with one
   outsized META loser. Not yet a rotation signal (no thresholds
   declared, single bad day, regime still fits), but if the
   remaining longs trip more exits the headline will worsen.
   Flagging for visibility, not action.
