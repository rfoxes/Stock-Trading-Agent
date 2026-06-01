# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-06-01, Mon, post-close.)

- **Active strategy:** `equity_trend_following_ema_cross`
  (`since: 2026-05-27`). Unchanged today.
- **Today's `execute`:** 0 intents, 0 submitted, 0 rejected, 0 errors.
- **No fills overnight.** Cash unchanged at -$59,655.14 (same to the
  penny as Fri close). Same 8 longs.
- **Account:** equity $110,361.60 (-$1,815.48 / -1.62% vs. Fri),
  buying_power $50,706.46. Pure MTM drift — no realized P&L.
- **Regime:** `bull, conf=0.80, adx=29.69` — sixth consecutive
  bull-trending day; ADX strengthening from 26.82 Fri.
- **Position movement Fri → today (unrealized %):**
  AAPL +14.70% → +12.71%, AMZN +8.83% → +4.29%, GOOGL +12.34% → +9.32%
  (cap-raise hit), JPM -4.39% → -5.26%, NVDA +6.77% → +12.33%
  (HPE/Computex tailwind), QQQ +13.89% → +14.23%, SPY +6.61% → +6.75%,
  TSLA +7.53% → +2.48%.
- **GOOGL $80B equity raise:** AH-announced Sun/Mon. Stock absorbed the
  dilution print; strategy is technical and did not exit.
- **JPM watch:** strategy did NOT fire an exit, so ADX presumably still
  > 20. Position deteriorated ~1 pp on the day.
- **Gate verification:** N/A today — no orders submitted.

## **CRITICAL — read first: git-sync architecture changed today**

The recurring `.git/*.lock` wedge is fixed *architecturally*, not by
another in-sandbox patch. The harness sandbox CANNOT unlink files inside
`.git/` (Operation not permitted). So `cli git-sync` no longer tries.
Instead:

1. **`cli git-sync` now writes a JSON marker** into
   `<repo>/.git-sync-queue/` describing the commit you want made.
2. A launchd LaunchAgent on the operator's mac
   (`com.harness.gitrunner`) polls that queue every 30 seconds and runs
   `git add / commit / push` from outside the sandbox where it has full
   permission.
3. A sibling agent (`com.harness.gitlock`) sweeps stale `.git/*.lock`
   files every 10 seconds as a safety net.

**What you should expect to see** from `cli git-sync --agent trader ...`:

```json
{"ok": true, "queued": ".git-sync-queue/20260602T...trader_...json", ...}
```

That's success. `committed`/`pushed` are intentionally `false` — you
queued the commit; the runner does the rest.

**What to do if markers stack up** in `.git-sync-queue/` (visible via
`cli git-doctor`):

- The operator hasn't installed the LaunchAgents yet. Tell them to run
  `bash scripts/install_git_safety.sh` from a real terminal — once.
- Do NOT try to delete the markers yourself (sandbox can't unlink).
- Do NOT try to run `git` commands yourself (same reason).

The OPERATOR has not yet confirmed they ran `install_git_safety.sh` —
the 3 stale `.git/HEAD.lock` / `.git/ORIG_HEAD.lock` /
`.git/objects/maintenance.lock` files are still on disk. Flag this in
the operator-questions section if still wedged.

## To do tomorrow (Tue 6/2)

**Tuesday is an elevated overnight-risk day.** Iran formally stopped US
negotiations Mon and pledged to "fully close" the Strait of Hormuz; WTI
+7.7%, Brent +6.6%. Any overnight Hormuz-closure confirmation or futures
gap > 2% down would re-classify the news brief as HALT-WORTHY.

1. **Read last_handoff.md, then news_brief.md FIRST.** Iran/Hormuz tape
   is the dominant overnight watch item.

2. **Standard read-and-snapshot** (manual.md §1-2).

3. **No fills to reconcile from Monday.** Strategy submitted nothing.

4. **Run `execute`.** Watch items:
   - **GOOGL:** position took ~3 pp hit on dilution Mon; technicals
     held. If Tue tape brings further weakness, strategy may fire an
     EMA-cross or ADX-fade exit. Don't override.
   - **JPM:** still the longest-standing watch-item. ADX presumably
     still > 20 (no exit Mon). If Tue pushes it below, expect a JPM
     exit at ~-$1,053 (0.95% of equity).
   - **AMZN / TSLA:** both gave back materially Mon (AMZN -4.5 pp,
     TSLA -5 pp). If either continues to weaken, an exit signal could
     trigger.
   - **NVDA:** +5.5 pp on the day on HPE blowout / Computex
     follow-through. Healthy trend; expect to hold.

5. **HALT-WORTHY check:** If the news brief is HALT-WORTHY or pre-market
   futures show > 2% down gap from Iran escalation, you MAY skip `cli
   execute` and document the deferral. Discretionary.

6. **Verify the gate** if any exits trigger. Four sessions of correct
   rescoped behavior confirmed would close that question.

7. **Do NOT revert** the safety_gate.py rescope OR
   `max_exits_per_run: 5`. Three sessions of correct behavior.

8. **Run `cli git-sync` as your last action**, expect to see `"queued"`
   in the response (not `"committed"`). Then run `cli git-doctor` once
   to read out the queue state — if there are 4+ pending markers and 3+
   stale locks, the operator hasn't installed the LaunchAgents yet;
   say so in `last_handoff.md` and the operator-questions section.

9. **AVGO Wed AMC prep:** the news layer flagged AVGO as the single most
   actionable upcoming catalyst (consensus $22.11B / $2.40 / AI +140%
   YoY; options 10.65% expected move). Saturday research agent is the
   right path. Note it in tomorrow's handoff if not yet added.

## Open questions for the operator

1. **One-time install — please run from a real terminal:**
   ```
   bash /Users/rfoxes/Stock-Trading-Agent/scripts/install_git_safety.sh
   ```
   This installs two launchd LaunchAgents:
   - `com.harness.gitlock` — sweeps stale `.git/*.lock` files every 10s
   - `com.harness.gitrunner` — processes `.git-sync-queue/` markers
     every 30s, running git from outside the sandbox

   After this, the harness's `git-sync` will Just Work. No more "4
   consecutive days of accumulated edits." The script is idempotent —
   safe to re-run any time.

   Verify with: `launchctl list | grep harness`
   Watch live: `tail -f /tmp/harness-gitrunner.log`

2. **Old `.git/*.lock` files**: please also clear these once during the
   first install (the script does this automatically as part of its
   final step):
   ```
   rm -f /Users/rfoxes/Stock-Trading-Agent/.git/HEAD.lock \
         /Users/rfoxes/Stock-Trading-Agent/.git/ORIG_HEAD.lock \
         /Users/rfoxes/Stock-Trading-Agent/.git/objects/maintenance.lock
   ```

3. **Universe expansion candidates.** News layer flagged for 4
   consecutive sessions: DELL, NTAP, OKTA, NOW, TEAM, MU, AVGO, SNOW,
   HPE (new), FLNC (new). The Saturday research agent is the right path,
   but if any belong in the universe sooner, add to
   `state/extra_symbols.md`.

4. **Strategy health still small-sample-noisy.** 30-day Sharpe -3.64,
   cum_return -4.08% vs SPY +6.05% (gap widened). N=2 realized trades.
   Not yet a rotation signal, but watch.
