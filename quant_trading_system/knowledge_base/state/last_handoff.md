# Handoff to tomorrow's Claude

## Summary of what I did today

Three things, all architectural, none trading:

1. **The recurring `.git/*.lock` wedge is now fixed at the design level,
   not by another in-sandbox patch.** I'd been trying to make the harness
   clean up after itself; that fundamentally cannot work, because the
   Cowork sandbox does NOT have permission to `unlink` files inside
   `.git/` — every attempt returns `Operation not permitted`. So I
   pivoted: the harness no longer runs git at all. `cli git-sync` now
   drops a JSON marker into `.git-sync-queue/`; a launchd LaunchAgent on
   the operator's mac (`com.harness.gitrunner`) processes that queue
   from outside the sandbox where it has full git permission. A sibling
   agent (`com.harness.gitlock`) continues to sweep stale `.git/*.lock`
   files every 10s. One-time install: `bash
   scripts/install_git_safety.sh`. Idempotent.

2. **Fixed the backtester `StrategyContext` construction.** The research
   agent's addition battery was blocked by `StrategyContext.__init__()
   missing 1 required positional argument: 'universe'` — I'd added
   `universe` as a required field to the live runtime but never updated
   `strategy_backtest.py`. One-line fix at line 333: pass
   `universe=[symbol]`. Research agent should be unblocked next Sat.

3. **Refactor: "active strategy" → "active strategy set" with library-gap
   mandate.** Operator directive. The system now supports multiple
   active strategies running simultaneously, each owning a slice of the
   universe. New file `state/active_strategies.md` (plural) replaces
   `state/active_strategy.md` (singular, still readable as fallback).
   Conflict resolution between strategies competing for the same symbol
   is ALWAYS via `cli head-to-head` — higher Sharpe wins, no exceptions.

   The bigger doctrinal change: **algorithmic-only mandate.** Every
   order traces to a strategy rule. If today's news warrants action but
   no active strategy responds, the LIBRARY is incomplete — the trader
   logs the gap, doesn't trade. Manual §6-§7, news brief now tags every
   event with `responder: <id>` or `responder: NONE — library gap`,
   research agent treats logged gaps as top-priority weekend work.

   New CLI surface: `cli list-active`, `cli add-active --symbols ...
   --reason ...`, `cli remove-active`, `cli head-to-head <a> <b>
   --symbol X --start ... --end ...`. The legacy `cli set-active` /
   `cli get-active` remain for backward compat. `cli execute` now
   iterates the full active set and surfaces `unclaimed_symbols` as a
   library-gap diagnostic.

   Migration: populated `active_strategies.md` with the one current
   strategy (`equity_trend_following_ema_cross`) claiming the 8
   currently-held positions. Verified the conflict check fires
   (attempting to add a second strategy claiming JPM returned a clean
   error pointing at head-to-head). Verified the library-gap diagnostic
   surfaces META + MSFT correctly (they're in the universe but not
   actually held — flagged in tomorrow's tasks.md for operator decision).

No trading today. No fills, no orders, no strategy edits, no execute.
Three full days of last_handoff content is preserved verbatim below my
work for tomorrow's Claude.

## Why the pivot was necessary (so this doesn't get re-litigated)

Confirmed in-sandbox: `rm -f /sessions/.../mnt/Stock-Trading-Agent/.git/HEAD.lock`
returns `Operation not permitted`. Same for ORIG_HEAD.lock. The
sandbox can READ files in `.git/`, can CREATE files outside `.git/`,
but cannot DELETE or REPLACE files inside `.git/`. Every previous
"fix" — signal handlers, atexit hooks, stale-lock sweep, `cli
git-doctor` — was code that runs inside the sandbox and hit the same
permission wall.

The only place with write permission on the user's `.git/` is the
user's mac itself. So git operations have to happen there. The
LaunchAgent is the cleanest way to do this without requiring the
operator to do anything manual after the one-time install.

## What changed concretely

### Files I rewrote
- `quant_trading_system/git_sync.py` — now write-only. Drops a JSON
  marker into `<repo>/.git-sync-queue/`. No subprocess, no `git` calls,
  no signal handlers, no stale-sweep. Old return shape preserved
  (still has `ok`, `committed`, `pushed`) so existing handoff parsers
  don't break — but `committed`/`pushed` are always `false` from the
  harness's point of view. The new field is `queued`.
- `quant_trading_system/agent_tools.py::git_doctor` — no longer tries
  to delete locks (it can't). Now reports state: how many stale
  `.git/*.lock` files exist, how many markers are queued, and whether
  the LaunchAgents look installed (by inference from queue size). Tells
  the operator what to do.
- `quant_trading_system/agent_tools.py::git_sync` — passes `agent=`
  through to the queue marker so the runner can attribute it.
- `quant_trading_system/strategy_backtest.py` line 333 — added
  `universe=[symbol]` to `StrategyContext(...)`. Research agent
  unblock.
- `daily_prompt.md`, `daily_news_prompt.md`, `weekly_research_prompt.md`
  — updated the "what success looks like" paragraph: `{"queued": ...}`
  is now the success signal, not `{"committed": ..., "pushed": ...}`.

### Files I created
- `scripts/com.harness.gitrunner.plist` — launchd job, every 30s,
  runs `process_git_sync_queue.sh`.
- `scripts/process_git_sync_queue.sh` — the queue processor itself.
  Single-instance via `flock`, parses each marker, bootstraps git
  config + token-auth origin (idempotent), pulls --rebase --autostash,
  adds, commits with the marker's message, pushes, deletes marker on
  success. Leaves markers in place on failure so the next cycle
  retries. Logs to `/tmp/harness-gitrunner.log`.
- `.git-sync-queue/.gitkeep` — placeholder so the queue directory is
  tracked, with format docs in the file body.

### Files I edited
- `scripts/install_git_safety.sh` — now installs BOTH plists
  (gitlock + gitrunner), creates the queue dir, chmod +x the runner
  script, sweeps existing stale locks at install time. Cleans up the
  old shell-function wrapper from the first install if it's still
  in any rc file.
- `.gitignore` — added `.git-sync-queue/*.json` so markers themselves
  never get committed.

### Smoke tests I ran (inside the sandbox)
- `cli git-sync --agent trader --message "smoke test of new
  queue-based git-sync" --no-pull` → returned `{"ok": true, "queued":
  ".git-sync-queue/20260601T234433Z_trader_..json"}`. Marker JSON
  parsed cleanly and contained the `[trader 2026-06-01]` prefix.
- `cli git-doctor` → reported 3 stale locks + 2 pending markers
  (one from my smoke test, one from an earlier sandbox test) with
  the "operator must run install_git_safety.sh" note.
- `bash -n process_git_sync_queue.sh` and `bash -n
  install_git_safety.sh` → both syntax-clean.
- `python3 -c "from quant_trading_system import strategy_backtest,
  git_sync, agent_tools; print('imports OK')"` → clean.

I did NOT run `install_git_safety.sh` — only the operator can, from
their real terminal. The script is ready and waiting.

## What tomorrow's Claude should expect

When you run `cli git-sync --agent trader --message "..."`:

- If the operator has run `install_git_safety.sh`: you'll see
  `{"ok": true, "queued": "..."}`, and within ~30s your commit will
  be on github. `cli git-doctor` will show the queue empty.
- If they haven't: same `{"ok": true, "queued": "..."}` response —
  the marker is still safely written. But it won't get processed
  until the agents are installed. `cli git-doctor` will show
  markers stacking up.

Either way, the harness's job is done after `git-sync`. You don't
have to wait for the push. The marker survives operator inattention.

## Carry-forward observations from Mon 6/1's quiet session

(Preserved from yesterday's handoff — none of this changed today.)

### Position movement Fri → Mon (unrealized %)

| Symbol | Fri | Mon | Δ pp | Notes |
|---|---|---|---|---|
| AAPL  | +14.70% | +12.71% | -1.99 | tape weakness |
| AMZN  |  +8.83% |  +4.29% | -4.54 | meaningful giveback |
| GOOGL | +12.34% |  +9.32% | -3.02 | $80B raise dilution priced in |
| JPM   |  -4.39% |  -5.26% | -0.87 | worst position deteriorated |
| NVDA  |  +6.77% | +12.33% | +5.56 | HPE blowout + Computex tailwind |
| QQQ   | +13.89% | +14.23% | +0.34 | flat-up |
| SPY   |  +6.61% |  +6.75% | +0.14 | flat-up |
| TSLA  |  +7.53% |  +2.48% | -5.05 | largest giveback |

Net portfolio MTM -$1,815 / -1.62%. No realized P&L.

### Live event overhang for Tue
- **Iran/Hormuz** — Tehran formally stopped US negotiations and
  pledged to "fully close" the Strait. WTI +7.7%, Brent +6.6%. If
  confirmed overnight or futures gap > 2% down, Tue brief should
  re-classify as HALT-WORTHY and Tue's Claude may skip execute.
- **GOOGL $80B raise** — priced in Mon; strategy did not exit.
  Position +9.32% unrealized.
- **NVDA** — HPE Q2 blowout direct read-through; trend healthy.
- **JPM** — exit candidate if Tue's tape pushes ADX below 20.

### Watch list for Tue's execute
- GOOGL: further weakness could fire EMA-cross / ADX-fade exit
- JPM: ADX-fade candidate; exit ~ -$1,053 if it fires
- AMZN / TSLA: both gave back materially; further weakness could
  trigger
- NVDA: expected hold

### Universe expansion candidates flagged 4 sessions running
DELL, NTAP, OKTA, NOW, TEAM, MU, AVGO, SNOW, HPE (new), FLNC (new).
AVGO is the standout — Wed AMC earnings, consensus $22.11B / $2.40 /
AI +140% YoY, options 10.65% expected move. Saturday research agent
is the right path; flag for operator if it hasn't been added by
Wed.

### Strategy health
30d: orders_submitted 2, orders_rejected 4, trades_closed 2,
win_rate 0.5, rolling_sharpe -3.639, cum_return -0.0408 vs spy +0.0605.
N=2 realized; small-sample-noisy; not a rotation signal yet. Gap
widening (-10 pp now vs SPY) — watch.

## Recommendations for Tue 6/2's Claude

1. Read this handoff, then read `news_brief.md` carefully. Iran/Hormuz
   is the dominant overnight watch.
2. Standard read-and-snapshot.
3. No fills to reconcile from Mon.
4. Run `execute` unless brief is HALT-WORTHY or futures > 2% down.
5. Run `cli git-sync --agent trader --message "..."`. Expect
   `"queued"` in the response — that's success now. Don't be alarmed
   that `committed`/`pushed` are `false`.
6. After git-sync, run `cli git-doctor` once. If pending_marker_count
   > 3 or stale_lock_count > 0 → the operator hasn't installed the
   LaunchAgents. Flag it in your handoff and tasks.md.
7. **Do NOT revert** the gate rescope, `max_exits_per_run`, the new
   `git_sync.py` queue architecture, or the LaunchAgent plists.

## Open questions for the operator

1. **Please run `bash scripts/install_git_safety.sh` once from a real
   terminal.** This is the one-time fix. After this runs, every
   harness-generated commit is automatically pushed by launchd
   within ~30s with no further intervention. Idempotent. Verify with
   `launchctl list | grep harness`.

2. **AVGO Wed AMC.** Decide whether to add to `extra_symbols.md`
   ahead of the research agent's Saturday cycle.

3. **Strategy health gap widening.** 30-day cum_return -4.08% vs SPY
   +6.05%. Small-sample (N=2) but worth flagging.

## Git-sync status

Queued today via the new mechanism. The marker is in
`.git-sync-queue/` and will be processed by the LaunchAgent on next
poll IF the operator has installed it. Today's `cli git-doctor`
showed 2 markers still pending (one from a sandbox smoke test, one
from this run's git-sync). If markers haven't drained by the time
tomorrow's Claude reads this, the operator install is still pending.
