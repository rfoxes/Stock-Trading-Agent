# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## ⚠️ READ FIRST — the harness changed today (2026-06-02)

Two architectural changes landed before today's run. Both take effect
automatically for you — they're built into the CLI and the doctrine.

### 1. Multi-strategy active set with library-gap mandate

The harness now supports multiple active strategies, each owning a
slice of the universe. The active set lives in
`state/active_strategies.md` (plural). Today's migration: the only
strategy in the set is `equity_trend_following_ema_cross`, owning the
8 inherited positions (AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA).
`cli list-active` shows the set + any unclaimed universe symbols.

**Algorithmic-only rule.** Every order traces to a strategy rule. You
never submit by hand, never loosen entry thresholds to "chase
activity", never override a strategy. If today's news warrants action
but no active strategy responds, **the library is incomplete** — log
the gap, do not trade. New section in `manual.md` §6-7 has the full
mandate; read it.

**News-brief responder tags.** The news agent now tags every material
event with `responder: <strategy_id>` or `responder: NONE — library
gap`, and there's a dedicated "## Library gaps" section in the brief.
Your job: scan that section, list each gap below in your tomorrow's
tasks.md (next iteration) under "## Library gaps for the research
agent". The Saturday research agent treats those as top-priority work.

**Conflict resolution.** If you want to add a new strategy that claims
a symbol another strategy already owns, the harness refuses (`cli
add-active` errors). Resolution is ALWAYS:
```
cli head-to-head <a> <b> --symbol X --start <ymd> --end <ymd>
```
Higher Sharpe wins; loser cedes. You don't pick by feel.

### 2. git-sync runs out-of-sandbox via launchd

`cli git-sync` no longer runs git — it queues a JSON marker in
`.git-sync-queue/` that the operator's launchd agent processes. You'll
see `{"ok": true, "queued": "..."}` — that's success. `committed` /
`pushed` are intentionally `false` on your side. If markers pile up,
tell the operator to run `bash scripts/install_git_safety.sh`.

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-06-01, Mon, post-close.)

- **Active strategy set (new):** one entry —
  `equity_trend_following_ema_cross` owns
  [AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA] (migrated 2026-06-02).
  Verify with `cli list-active`.
- **Today's `execute`:** 0 intents, 0 submitted, 0 rejected, 0 errors.
- **No fills overnight.** Cash unchanged at -$59,655.14. Same 8 longs.
- **Account:** equity $110,361.60 (-$1,815.48 / -1.62% vs. Fri),
  buying_power $50,706.46.
- **Regime:** `bull, conf=0.80, adx=29.69` — sixth consecutive
  bull-trending day; ADX strengthening from 26.82 Fri.
- **Position movement Fri → Mon (unrealized %):**
  AAPL +14.70% → +12.71%, AMZN +8.83% → +4.29%, GOOGL +12.34% → +9.32%,
  JPM -4.39% → -5.26%, NVDA +6.77% → +12.33%, QQQ +13.89% → +14.23%,
  SPY +6.61% → +6.75%, TSLA +7.53% → +2.48%.

## To do tomorrow (Tue 6/2)

**Tuesday is an elevated overnight-risk day.** Iran formally stopped
US negotiations and pledged to "fully close" the Strait of Hormuz; WTI
+7.7%, Brent +6.6%. Any overnight Hormuz-closure confirmation or
futures gap > 2% down would re-classify the news brief as HALT-WORTHY.

1. **Read last_handoff.md, then news_brief.md FIRST.** Iran/Hormuz is
   the dominant overnight watch.

2. **Standard read-and-snapshot.** Note: `cli list-active` is now part
   of the snapshot — it shows the active set and any unclaimed symbols
   (library-gap candidates).

3. **No fills to reconcile from Mon.**

4. **Run `cli execute`.** It iterates over the active set; today
   that's still just trend-following on the 8 positions. Watch items:
   - GOOGL: ~3pp dilution hit Mon; technicals held. Further weakness
     could fire an EMA-cross / ADX-fade exit.
   - JPM: ADX-fade exit candidate (~ -$1,053) if Tue pushes ADX below 20.
   - AMZN / TSLA: both gave back materially; further weakness could
     trigger.
   - NVDA: healthy trend; expected hold.

5. **HALT-WORTHY check:** if the brief is HALT-WORTHY or futures > 2%
   down from Iran escalation, you MAY skip `cli execute` and document.

6. **Library gaps — new responsibility starting today.** After reading
   `news_brief.md`, scan for any event tagged `responder: NONE —
   library gap` (or the dedicated "## Library gaps" section near the
   bottom). For each, write a one-line entry in tomorrow's tasks.md
   under a "## Library gaps for the research agent" section. **Present
   concrete example to expect from today's news brief:** AVGO Wed AMC
   earnings — no earnings-window strategy is active, so this should
   appear as `responder: NONE — library gap`. Log it.

7. **Do NOT revert** the safety_gate.py rescope, `max_exits_per_run`,
   the git-sync queue architecture, the new `active_strategies.md`
   file, or the launchd plists.

8. **Run `cli git-sync` as your last action.** Expect `"queued"` in
   the response — that's success. Then run `cli git-doctor` once. If
   pending_marker_count is high and stale_lock_count > 0, the operator
   hasn't installed the LaunchAgents; flag it in your handoff.

## Library gaps for the research agent (carry to research_tasks.md next Sat)

- **AVGO Wed 6/3 AMC earnings** — consensus $22.11B / $2.40 / AI +140%
  YoY; options 10.65% expected move. No active strategy fires on
  earnings-window catalysts. Saturday research priority: build/activate
  an event_driven_catalyst with earnings-window entry rules.
- **DELL, HPE, FLNC, MU, NTAP, OKTA, NOW, TEAM, SNOW** — flagged 4+
  consecutive sessions by news as universe candidates; no active
  strategy in the set claims any of them. Either expand the
  trend-following strategy's claim list (after a head-to-head on each
  symbol vs. its current best) or build a multi-name momentum strategy
  that owns them.
- **META, MSFT** — already in the legacy `state/active_strategy.md`
  reason text but NOT actually held positions, and now show as
  `unclaimed_symbols` in `cli list-active`. Decide: drop them from the
  universe (remove from any extras / strategy frontmatter), or claim
  them with trend-following.

## Open questions for the operator

1. **Please run `bash scripts/install_git_safety.sh` once from a real
   terminal.** This is the one-time fix for the git-lock wedge.
   Idempotent. Verify with `launchctl list | grep harness`.

2. **AVGO Wed AMC.** Decide whether to add to `state/extra_symbols.md`
   ahead of the research agent's Saturday cycle — without it, the
   trader won't even see AVGO if/when the research agent builds an
   earnings strategy.

3. **Strategy health gap widening.** 30-day cum_return -4.08% vs SPY
   +6.05% (-10 pp gap). Small-sample (N=2) but flagging for visibility.
