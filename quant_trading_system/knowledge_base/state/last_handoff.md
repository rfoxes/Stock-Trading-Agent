# Handoff to tomorrow's Claude

(Run on the **2026-07-07 clock** — snapshot read 2026-07-07 ~09:10 PT. **⚠️ THIS WAS AN ANOMALOUS RUN — see the
BROKER-STATE WIPE below. Decision: FREEZE — NO execute, NO log-closed, flag operator.** The run also fired
**off-schedule at 09:09 PT mid-session** (`is_open: true`), not the canonical ~4 PM PT post-close slot, and the
**news brief was STALE** (header `2026-07-06`, one day old — treated as ABSENT). Ran the whole snapshot via the
venv.)

## ⚠️⚠️ TL;DR — BROKER-STATE WIPE, ENVIRONMENT FROZEN, OPERATOR ACTION REQUIRED

**The paper account came back FLAT this run. All four held longs (AVGO 26, META 16, MU 7, ORCL 38, ~$31.6k
market value) are GONE — `positions: []` — but cash is UNCHANGED to the penny ($71,809.59) and equity simply
collapsed to that cash number ($103,459.08 → $71,809.59, −$31,649).** This is NOT a set of strategy exits. I
did NOT trade, did NOT reconcile-by-fabrication, and did NOT execute. **This needs operator confirmation of the
cause before any reconciliation.**

**Why this is a reset/wipe, not normal closes (three independent tells):**
1. **Cash didn't move.** If the four longs had been *sold*, cash would have risen ~$31.6k and equity stayed
   ~$103.5k. Instead equity fell by the full position value and cash is identical to yesterday → the value
   vanished, it was not liquidated into cash.
2. **No `trade_closed` journal events.** `recent-trades --strategy-id equity_event_driven_catalyst` shows only
   the original AVGO/MU/ORCL *buys* (6/8, 6/10, 6/16); `equity_momentum_macd_histogram` shows only the 7/1
   META buy. **None of the four positions has a close event** — the harness never sold them.
3. **All provisional claims re-stamped to today.** `list-active` now shows `provisional_since: 2026-07-07`,
   `revalidate_by: 2026-07-21` for QCOM/SPCX/SYNA (were 06-20/06-26, deadlines 07-04/07-10), and the
   trend-following / event-driven / pairs claims flipped `since` to `2026-07-07`. The harness state was
   **re-bootstrapped today** — coincident with the account wipe.

**Leading hypothesis:** an **Alpaca paper-account reset / environment reinitialization** over the 7/6→7/7
boundary — positions wiped, the ~$71.8k cash retained, harness claim-state re-seeded with today's date.
Alternatives to rule out: a broker data glitch, or a manual liquidation that failed to credit cash (unlikely).
**Operator: please confirm on the Alpaca paper dashboard whether the account/positions were reset.**

**What I did NOT do and why (per manual.md "Recent feedback" doctrine added this run):**
- **No `cli log-closed`.** There was no real close — no cash basis, no `trade_closed` events. Logging closes
  with fabricated pnl_fractions would inject phantom realized losses into strategy Sharpe/win-rate stats that
  later drive rotation/validation. Reconciliation waits for the operator to confirm the cause.
- **No `cli execute`.** The strategies' journal view (positions open) is desynced from a flat broker; opening
  new positions into an unexplained, just-reset environment — on a stale brief, at an off-cycle time — is
  unsafe and exactly the "stop and flag operator" case. If a real 4 PM post-close run fires today with a fresh
  brief and a confirmed-clean account, that run can execute normally.
- **No triage / add-active.** P0 is already satisfied (`unclaimed_count: 0`, claimed 26, provisional 3). No
  new universe member appeared. Nothing to triage.

## Snapshot (7/7 ~09:10 PT, via venv)

- **`market-status`:** `is_open: true`, `now 2026-07-07T09:09 PT`, `next_open 2026-07-08 09:30 ET`. Off-cycle
  MID-SESSION firing (canonical run is ~4 PM PT post-close).
- **Account (re-confirmed twice, identical — not a transient glitch):** equity **$71,809.59**, cash
  **$71,809.59**, buying_power $287,238.36, portfolio_value $71,809.59, day_trade_count 0.
- **Positions:** **`[]` (EMPTY).** Was 4 longs yesterday.
- **Open orders:** clean (empty).
- **Regime:** bull, conf 0.72, ADX 22.17, realized_vol 0.1793 (SPY history intact — the regime classifier is
  unaffected; only the account/positions were wiped).
- **`list-active`:** universe **26**, claimed **26**, `unclaimed_count: 0`, `provisional_count: 3`
  (QCOM/SPCX/SYNA, all now `revalidate_by 2026-07-21`). 8 strategies active.
- **News brief:** header `2026-07-06` ≠ today → **STALE, treated as ABSENT.** (At 09:09 the 7/7 brief wouldn't
  exist yet anyway — the news agent writes it ~30 min before the 4 PM run.)
- **git-sync-queue:** only the Jun-1 test files — LaunchAgent healthy.

## Last known-good book (7/6 ~16:03 PT close, for the operator's reconciliation)

These are the four positions that vanished, at their last confirmed marks — so the operator can reconstruct if
the reset needs undoing:
- **AVGO 26** — avg $377.27, last cur $374.23, last unreal −0.81% (−$79.04).
- **META 16** — avg $605.28 (macd_histogram entry 7/1), last cur $600.40, last unreal −0.81% (−$78.01).
- **MU 7** — avg $982.90, last cur $975.69, last unreal −0.73% (−$50.49).
- **ORCL 38** — avg $177.28, last cur $144.15, last unreal −18.69% (−$1,258.81).
Last-good equity $103,459.08, cash $71,809.59 (cash is the one thing that survived unchanged).

## What happened on the (completed) 7/6 run, for continuity

7/6 was a normal post-close session: `cli execute` RAN and every strategy fired **0 intents** (0 submitted, 0
rejected, 0 errors) — a clean do-nothing day. Book was UP (+$792 to $103,459) on a risk-on semi rebound (AVGO
recovered from −4.46%→−0.81% on Broadcom-Apple-2031; META −3.70%→−0.81%; ORCL off its worst). That 7/6 run
wrote this handoff but was interrupted before writing tasks.md or running git-sync, so 7/6 never committed
separately; its outcome is captured here and folded into today's commit.

## Summary of what I did today (7/7)

1. **Read context.** daily_prompt.md, manual.md, tasks.md (the Mon-7/6 version — stale but read),
   last_handoff.md (the 7/6 version I wrote), news_brief.md. **Date-checked the brief — header `2026-07-06` ≠
   today → treated as ABSENT** (news pipeline gap re-flagged; also expected, since it's a 9 AM firing).
2. **Confirmed interpreter** — `.venv/bin/python3` throughout (bare `python3` still Homebrew 3.14.5, no deps).
3. **`market-status`** — `is_open: true` at 09:09 PT (off-cycle mid-session).
4. **Broker snapshot** — found the FLAT account / empty positions. **Re-ran account + positions to confirm
   stability** (identical second read → real state, not a glitch).
5. **Investigated the anomaly** — `recent-trades` for both position-owning strategies (no `trade_closed`
   events for the four names); `list-active` (provisional claims re-stamped to 2026-07-07). Cross-checked cash
   (unchanged) vs equity drop (= full position MV). Concluded: environment reset / broker wipe.
6. **Decision: FREEZE.** No execute, no log-closed, no triage/add-active. Documented the doctrine in
   manual.md "Recent feedback" and flagged the operator as P0.
7. **Checked git-sync-queue** — healthy (only Jun-1 test files).

## Observations and reasoning

- **The cash-vs-equity arithmetic is the decisive tell.** A genuine liquidation moves value from positions
  INTO cash (equity ≈ flat). Here equity dropped by exactly the position market value while cash held to the
  penny — value left the account entirely. That is not a trade; it's a state reset (or, less likely, a broker
  data fault). Everything else (no close events, re-stamped claims) corroborates.
- **Fabricating log-closed would be the worst move.** It's tempting to "reconcile" the four missing positions
  per the standard workflow, but attributing invented pnl_fractions to strategies that never sold — with no
  cash to back the numbers — would permanently distort their health metrics. Deferring is reversible;
  fabricating is not. When the mechanism of a disappearance is unexplained, document, don't reconcile.
- **Executing off-cycle into a reset book is the second-worst move.** At 09:09 mid-session with a stale brief
  and a book that was just wiped, any new entry would be an off-schedule bet on desynced state. If the
  canonical 4 PM run fires today against a confirmed-clean account with a fresh brief, that is the run that
  should trade.
- **The harness code is fine.** CLI works, broker is reachable, regime classifier and universe/claim state are
  intact. This is an account/positions data event, not a software outage — but it needs the operator to say
  what happened before the harness resumes trading.

## Final state at session end

- **Positions:** none (account flat). **Open orders:** none.
- **Account:** equity $71,809.59, cash $71,809.59, buying_power $287,238.36, day_trade_count 0.
- **Active set:** 8 strategies × 26/26 claimed (`unclaimed_count == 0`); 3 PROVISIONAL (QCOM/SPCX/SYNA, all
  `revalidate_by 2026-07-21`, all execution-quarantined).
- **Regime:** bull, conf 0.72, ADX 22.17, realized_vol 0.1793.
- **Code changes:** none. **Strategy changes:** none. **Manual:** appended one durable "Recent feedback"
  bullet (broker-state-wipe → FREEZE doctrine). **`cli execute`: deliberately NOT run.** **`cli log-closed`:
  deliberately NOT run.**

## Open issues for the operator

1. **[P0 — NEW, BLOCKING] Broker-state wipe / suspected paper-account reset (7/7).** All four longs gone,
   cash unchanged ($71,809.59), equity −$31,649, no `trade_closed` events, provisional claims re-stamped to
   2026-07-07. **Confirm on the Alpaca paper dashboard whether the account/positions were reset**, and tell
   the trader whether to (a) treat the flat book as the new baseline and resume trading, or (b) restore the
   four positions. Until confirmed, the harness is frozen (no execute, no reconciliation). Last-good book +
   marks are recorded above for restoration.
2. **[HIGH — timing] Task fired off-schedule at 09:09 PT mid-session (7/7), not the ~4 PM post-close slot.**
   Combined with the 7/3 holiday firing, the schedule is misbehaving. Confirm the intended trigger and whether
   a separate canonical 4 PM run will still fire today. Executing mid-session on a stale brief is undesirable.
3. **[HIGH] News pipeline — 7/7 brief absent at run time (header still `2026-07-06`).** Partly explained by the
   9 AM firing (brief is written ~30 min before the 4 PM run), but the flaky-pipeline history (misses 6/22,
   6/25, 6/29) still argues for a news-agent health-check/alert and the `_load_news_brief()` staleness guard.
4. **[HIGH, UNRESOLVED] Bare `python3` broken (Homebrew 3.14.5, no deps).** Run everything via
   `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`. Repoint the task/daily_prompt or reinstall deps.
5. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to today. Would feed a
   stale brief as live signal. Saturday item.
6. **[REOPENED] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order
   exists (did NOT bite this run — no order). Order-serialization path needs fixing.
7. **THREE provisional/quarantined claims — now all `revalidate_by 2026-07-21`** (QCOM/SPCX/SYNA; deadlines
   were reset with the state re-bootstrap). SPCX joined the Nasdaq-100 today (7/7) but stays quarantined until
   research validates. QCOM + SYNA (live onsemi merger-arb) same deadline now. Do NOT hand-promote.

## Git-sync status

Ran `cli git-sync --agent trader --message "..."` (via venv) as last action. State files changed
(last_handoff.md, tasks.md, manual.md). git-sync queues a JSON marker to `.git-sync-queue/`; the operator's
launchd LaunchAgent (`com.harness.gitrunner`) runs the actual push. Verified only the Jun-1 test files sit in
the queue — LaunchAgent healthy.
