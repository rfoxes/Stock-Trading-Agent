# Handoff to tomorrow's Claude

(Run on the **2026-07-07 clock** — canonical post-close run, snapshot read **2026-07-07 ~16:03 PT**, `is_open:
false`, `next_open 2026-07-08 09:30 ET`. **✅ THE MORNING WIPE SELF-RESTORED — the harness is UN-FROZEN and ran
a normal session.** This is the "real 4 PM post-close run" the 09:09 handoff said could execute if the account
re-confirmed clean. It did. Ran everything via the venv.)

## 🔧 2026-07-08 INTERACTIVE OPERATOR SESSION — three durable changes (committed)

After the 7/7 automated run, the operator opened an interactive session and directed three changes. All are
live in the working tree and committed via git-sync. Tomorrow's run inherits them.

**1. Fixed `equity_event_driven_catalyst`: its documented exits are now actually enforced.** Investigation
(prompted by "why does ORCL sit at −20% unmanaged?") found the strategy implemented only its *negative-news*
exit; the **hard ATR stop** and **7-day time stop** it documents were dead letters — the stop was passed as
`stop_loss_pct` on the entry intent but the LIVE submission path ignores that field (only the backtester at
`strategy_backtest.py:395` consumes it), so no resting broker stop ever existed, and `max_hold_days` appeared in
zero Python. The backtester DID honor the stop, so the strategy's simulated stats flattered it and hid the live
gap. Fix: `evaluate()` now re-derives and re-checks both stops on every held position each run (there is no
resting order — the strategy is the stop). `.md` and `.py` synced. **The next `cli execute` will therefore sell
AVGO (time), MU (time), ORCL (hard) — verified by dry-run: 3 intents where there were 0. Expected, not an
anomaly.** Operator kept `max_hold_days: 7` ("that's fine"); calibration is a research item. On the "7 days is
arbitrary" question: the *concept* (catalyst alpha is time-concentrated; force turnover; don't let an
event-trade drift into a permanent hold) is principled — it's the discipline whose ABSENCE let ORCL ride to
−20%; the specific *value* 7 is an uncalibrated default and a fair thing to backtest.

**2. New `equity_watch_only` strategy + it's the mandatory-attach fallback.** Passive by design (`evaluate()` →
`[]`, never trades), `role: watch`, excluded from triage candidate scoring. `memory.DEFAULT_FALLBACK_STRATEGY`
now points to it, so a no-edge / no-history symbol is attached to watch_only ("watching, not trading") instead
of a real trading strategy laid on with no backtest. Watching is now an explicit, legitimate RESTING grade.

**3. News → universe → strategy, universally (operator directive).** news_manual §9 "Tier 0": the news agent
promotes EVERY stock it *materially reports on* (subject of an item, not an incidental cross-mention) on first
appearance — the 3-session recurrence gate is demoted to a prioritization hint. Mandatory-attach then guarantees
each a strategy (VALIDATED or WATCH). Directive recorded in `manual.md` P0 and `news_manual.md` §9. Rationale
(operator verbatim): "everytime news reports on a stock, bring it into the universe and give it a strategy —
that can just be to keep watch, doesn't have to be buy or sell."

Verification done this session: both edited strategies pass `validate-strategy`; `list-active` and
`list-strategies` load cleanly (harness not broken); the watch fallback wiring confirmed by a no-side-effect
check (fallback constant, `role: watch` exclusion, `evaluate()`→`[]`). Existing provisional claims
(QCOM/SPCX/SYNA) are untouched — the fallback change only affects FUTURE attaches.

**Execution decision:** the AVGO/MU/ORCL exits were NOT fired in this session — they'll go out on the next
scheduled post-close `cli execute` (same fill timing since the market is closed now). If that run somehow does
NOT fire, run `cli execute` manually to place them.

---

## ✅ TL;DR — THE 7/7 09:09 "WIPE" WAS TRANSIENT; BOOK RESTORED; EXECUTE RAN CLEAN

The account that came back FLAT at 09:09 this morning (all four longs gone, cash unchanged) **self-restored by
the post-close run.** At 16:03 PT the four longs are **back at their exact prior qty and avg-entry**, cash is
still $71,809.59 to the penny, equity is back to **$103,098.75**. The news agent independently observed the same
restoration ~30 min earlier ($103,106.76). I re-snapshotted, confirmed broker↔journal consistency (no phantom
closes), lifted the freeze on that evidence, and ran the standard workflow. **`cli execute` ran: 0 intents, 0
submitted, 0 rejected, 0 errors — a clean do-nothing day on the restored book.** No `log-closed` (nothing
actually closed). No triage (P0 already satisfied). No strategy edits.

**Why un-freezing was correct (evidence, not a hunch):**
1. **Positions restored to the penny.** AVGO 26 @ $377.27, META 16 @ $605.28, MU 7 @ $982.90, ORCL 38 @ $177.28
   — identical qty AND avg-entry to the 7/6 last-good book. A reset that dropped and re-created positions would
   not reproduce exact average entry prices; these are the same lots.
2. **Broker ↔ journal consistent.** `recent-trades` for both position-owning strategies shows only the original
   BUYS (event_driven_catalyst: MU 6/8, ORCL 6/10, AVGO 6/16; macd_histogram: META 7/1) — **zero `trade_closed`
   events** during the glitch window. The only close on record is a stale 6/8 META round-trip that predates the
   current position. The morning glitch left NO journal artifacts.
3. **Canonical post-close run + fresh brief.** 16:03 PT (the proper slot, not the 09:09 off-cycle firing), and
   the 7/7 news brief is correctly dated today (written ~30 min pre-run).

Doctrine written up: `manual.md` "Recent feedback" now carries the **un-freeze condition** completing the
morning's freeze bullet. (Freeze on an unexplained flat book; resume on a re-confirmed consistent one — both
evidence-driven.)

## Snapshot (7/7 ~16:03 PT, via venv)

- **`market-status`:** `is_open: false`, `now 2026-07-07T16:03 PT`, `next_open 2026-07-08 09:30 ET`. Canonical
  post-close slot ✓ (contrast the morning run's 09:09 mid-session firing).
- **Account:** equity **$103,098.75**, cash **$71,809.59** (unchanged, as expected — positions were never
  sold), buying_power $374,848.01, portfolio_value $103,098.75, day_trade_count 0.
- **Positions (all four RESTORED):**
  - **AVGO 26** — avg $377.27, cur $369.01, unreal **−2.19%** (−$214.76).
  - **META 16** — avg $605.28, cur $615.60, unreal **+1.71% (+$165.19), GREEN** (Muse Image launch + upgrade).
  - **MU 7** — avg $982.90, cur $923.50, unreal **−6.04%** (−$415.80) — deepened on the Samsung-driven chip rout.
  - **ORCL 38** — avg $177.28, cur $141.60, unreal **−20.13%** (−$1,355.71) — still the book's worst.
- **Open orders:** none.
- **Regime:** bull, conf 0.72, ADX 22.17, realized_vol 0.1793 (unchanged — the classifier was never affected).
- **`list-active`:** universe **26**, claimed **26**, `unclaimed_count: 0`, `provisional_count: 3`
  (QCOM/SPCX/SYNA, all `revalidate_by 2026-07-21`). 8 strategies active.
- **`cli execute`:** `submitted_count 0`, `rejected_count 0`, `error_count 0`; every non-quarantined strategy
  fired 0 intents. `provisional_quarantined: [QCOM, SPCX, SYNA]`; `skipped`: SPCX (trend-following), QCOM
  (event_driven_catalyst), SYNA (pairs) — all `provisional_unvalidated_claim (execution-quarantined)`.
- **News brief:** header `2026-07-07` = today ✓ (fresh). Assessment **NOTABLE** (chip rout + Hormuz oil spike),
  NOT halt-worthy. 0 promotions, universe stays 26.

## Two nuances confirmed this run (for whoever reconciles the provisional state)

1. **Provisional quarantine is SYMBOL-level, not strategy-level.** Execute skipped ONLY QCOM/SPCX/SYNA. So
   `equity_event_driven_catalyst` DID evaluate its held names AVGO/MU/ORCL (returned 0 intents — they ride their
   rules) and `equity_trend_following_ema_cross` DID evaluate its 11 non-SPCX symbols. Only the 3 structured
   `provisional_claims` symbols are quarantined. **The claim-REASON prose is misleading** — the 7/7 re-bootstrap
   stamped a QCOM-specific "PROVISIONAL/QUARANTINED" string onto the *whole* event_driven_catalyst claim (which
   includes the 3 traded held names). The structured `provisional_claims` field (the real source of truth) is
   correct. This is cosmetic prose drift, not a trading bug — but a `list-active` reader could misread it. Flag
   for reconciliation via re-triage, NOT a hand-edit (direct YAML edits to `active_strategies.md` are forbidden).
2. **ORCL −20% is a strategy-LOGIC gap, not "no responder."** event_driven_catalyst DOES own and evaluate ORCL;
   the problem is its `evaluate()` never generates the exit it documents at entry. The 6/10 entry reasoning
   states "Stop @ 175.11 ... 7-day time stop applies," but the order submitted was a plain **market buy with
   `stop_price: null`** — no broker-side stop was ever placed, and evaluate() doesn't produce a stop/time-stop
   exit intent. So both the price stop (breached long ago) and the 7-day time stop (27 days elapsed) are dead
   letters. Precise diagnosis for Saturday research: **event_driven_catalyst implements entry but not exit.**

## Summary of what I did today (7/7 post-close)

1. **Read context** — daily_prompt.md, manual.md, tasks.md (the 7/7-morning FROZEN version), last_handoff.md
   (the 09:09 wipe report), news_brief.md. **Date-checked the brief — header `2026-07-07` = today → FRESH** (the
   news agent's own broker-state note pre-flagged that the wipe looked transient/self-restored).
2. **Confirmed interpreter** — `.venv/bin/python3` throughout (bare `python3` still Homebrew 3.14.5, no deps).
3. **`market-status`** — 16:03 PT canonical post-close (not the morning off-cycle firing).
4. **Broker snapshot** — account/positions/open-orders/regime. **Found the four longs RESTORED** to exact prior
   qty/avg-entry, cash unchanged, equity back to ~$103,099.
5. **P0 check** — `list-active`: unclaimed 0, provisional 3. No new unclaimed symbol; no triage needed.
6. **Verified broker↔journal consistency** — `recent-trades` on both position-owning strategies: only original
   buys, **zero phantom `trade_closed` events**. Confirmed nothing to reconcile / no `log-closed`.
7. **Lifted the freeze on evidence** (restored book + consistent journal + canonical post-close + fresh brief).
8. **`cli execute`** — ran clean: 0 intents / 0 submitted / 0 rejected / 0 errors; QCOM/SPCX/SYNA quarantined.
9. **Wrote up the un-freeze doctrine** in `manual.md` "Recent feedback"; updated tasks.md + this handoff;
   git-sync last.

## Observations and reasoning

- **The exact-avg-entry match is the decisive un-freeze tell.** A true reset that re-created positions would
  not reproduce fractional average entry prices ($605.275625, $177.276579) to the digit. These are the original
  lots re-appearing — the morning read was a transient broker/data glitch, not a durable state change. Combined
  with cash unchanged and zero close events, the book is provably the same book.
- **Un-freezing on evidence (not operator word) was the right call and is now doctrine.** The morning freeze was
  correct given an unexplained flat book. But the freeze isn't a wait-for-human latch — it's a wait-for-a-
  consistent-state latch. Once the state re-confirmed consistent (positions back, journal clean, canonical run,
  fresh brief), continuing to sit frozen would have been its own error (missing a legitimate trading session for
  no reason). Symmetric evidence in, symmetric decision out.
- **Nothing to reconcile — and that's the point.** The temptation on a "positions reappeared" day is to log
  *something*. But the journal never recorded closes, so there are no closes to attribute. Reconcile only what
  broker AND journal jointly support; here they jointly support "4 longs open, untouched."
- **The clean 0-intent execute is the mandate working, not inaction to fix.** NOTABLE tape (chip rout + oil),
  but every held name is `responder: NONE` (informational) and no strategy's entry/exit rule fired. Manufacturing
  action from a two-sided news cluster would be curve-fitting. The strategies looked and passed; that's correct.
- **ORCL is the one genuine standing problem, and it's a code gap, not a market call.** −20% unmanaged because
  event_driven_catalyst has no exit implementation. I did NOT hand-exit it (forbidden) and did NOT rush a
  same-day strategy.py edit on a recovery day without a backtest. It's the top Saturday research item, now with
  a sharpened diagnosis (implement the exit side: price stop + 7-day time stop as real exit intents).

## Final state at session end

- **Positions:** AVGO 26 / META 16 / MU 7 / ORCL 38 (all restored). **Open orders:** none.
- **Account:** equity $103,098.75, cash $71,809.59, buying_power $374,848.01, day_trade_count 0.
- **Active set:** 8 strategies × 26/26 claimed (`unclaimed_count == 0`); 3 PROVISIONAL (QCOM/SPCX/SYNA,
  `revalidate_by 2026-07-21`, execution-quarantined).
- **Regime:** bull, conf 0.72, ADX 22.17, realized_vol 0.1793.
- **Code changes:** none. **Strategy changes:** none. **Manual:** appended one durable "Recent feedback" bullet
  (broker-wipe UN-FREEZE condition). **`cli execute`: RAN, 0 intents.** **`cli log-closed`: correctly NOT run.**

## Open issues for the operator

1. **[RESOLVED — FYI] The 7/7 09:09 broker-state wipe was TRANSIENT and self-restored by post-close.** No action
   needed on the account (four longs back at exact prior lots, cash intact, equity ~$103,099). If you can still
   confirm on the Alpaca dashboard what caused the 09:09 flat read (paper-account flicker?), it would help
   harden the pipeline, but the harness has resumed normal operation.
2. **[HIGH — timing, STILL OPEN] The schedule is firing off-cycle.** 7/7 fired at 09:09 mid-session AND at the
   canonical ~16:03 post-close (this run) — two firings in one day; plus the 7/3 holiday firing. Confirm the
   intended trigger; the double-fire risks acting twice on one session. (Today it was benign — the morning run
   froze and this one executed clean — but it should be one canonical post-close run/day.)
3. **[HIGH, UNRESOLVED] Bare `python3` broken (Homebrew 3.14.5, no deps).** Everything runs via
   `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`. Repoint the task/daily_prompt or reinstall deps.
4. **[MEDIUM] News-pipeline staleness guard.** Today's brief was fresh, but `_load_news_brief()` still never
   compares `date_in_file` to today — a stale brief would feed as live signal. Saturday item.
5. **[MEDIUM] Provisional claim-REASON prose is misleading** (see nuance #1 above) — the whole
   event_driven_catalyst / trend_following claim reasons read "QUARANTINED" but only QCOM/SPCX/SYNA actually are.
   Reconcile via re-triage, not a hand-edit.
6. **[REOPENED] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists
   (did NOT bite this run — no order).
7. **THREE provisional/quarantined claims** — QCOM/SPCX/SYNA, all `revalidate_by 2026-07-21`. Saturday research
   owns validation. SPCX joined the Nasdaq-100 7/7 but stays quarantined. Do NOT hand-promote.

## Git-sync status

Ran `cli git-sync --agent trader --message "..."` (via venv) as last action. State files changed
(last_handoff.md, tasks.md, manual.md). git-sync queues a JSON marker to `.git-sync-queue/`; the operator's
launchd LaunchAgent (`com.harness.gitrunner`) runs the actual push. Expect `{"ok": true, "queued": ...}`.
