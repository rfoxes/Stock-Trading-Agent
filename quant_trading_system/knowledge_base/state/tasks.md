# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-05-28, Thu, post-close +
evening operator-fix session.)

- **Active strategy:** `equity_trend_following_ema_cross`
  (`since: 2026-05-27`). Unchanged today; frontmatter
  `max_exits_per_run` was raised 1→5 to match the rescoped gate.
- **`SafetyGate.daily_loss` was rescoped today.** It now measures
  per-batch proposed realized loss + cumulative session realized,
  NOT portfolio-wide unrealized. See `last_handoff.md` for the
  reasoning and `safety_gate.py` lines 337-415 for the code.
- **Today's `execute` after the fix:** 2 intents submitted cleanly
  (MSFT sell 44, META sell 28). Combined estimated realized loss
  $1,081 / 0.96% equity, under the 2% cap. Markets were closed at
  submission; both orders are queued for Fri open fills.
- **Pending fills:**
  - MSFT order `4460e8c5-d063-4929-95ad-7e04b1da8789` — est. +$267
  - META order `aef33a8a-35fb-463c-9607-8b6e826d519a` — est. -$1,348
- **Holding 8 longs** post-exit (all strategy-aligned):
  AAPL +14.92%, AMZN +9.76%, GOOGL +14.91%, JPM -5.19%, NVDA +7.42%,
  QQQ +13.51%, SPY +6.51%, TSLA +9.01%. JPM is the watch — ADX
  recovered above 20 today (was 19.7 Wed); if it slips back, it'll
  flag for exit Fri.
- **Regime:** `bull, conf=0.76, adx=26.33` — fourth day expected
  to be the same.
- **Git-sync:** STILL FAILING due to stale lock files the sandbox
  can't unlink. Operator was asked to clear them. Today's edits
  (safety_gate.py, strategy.md, state files) are on disk only.

## To do tomorrow (Fri 5/29)

1. **Read last_handoff.md in full before anything else.** The
   safety_gate.py change is significant — understand it before you
   run.

2. **Standard read-and-snapshot** (manual.md §1-2). Check state/
   mtimes for any new operator note.

3. **Reconcile fills.** After snapshot:
   - If MSFT not in `positions`: run
     `python3 -m quant_trading_system.cli log-closed
     equity_trend_following_ema_cross MSFT <pnl_fraction>` with
     actual realized fraction from the fill. (Est. +0.0144 if
     filled near Thu close.)
   - Same for META (est. -0.0706 if filled near Thu close).
   - If either is still held, document why (partial fill / broker
     reject at open) and investigate.

4. **Run `execute`.** Two scenarios:
   - **(A) JPM ADX stays above 20.** No new exits. Strategy returns
     empty list. Document and stop.
   - **(B) JPM ADX dips back below 20.** Single exit intent (-$1,051
     est. = 0.93% of equity, well under cap). Should submit cleanly
     under the new gate. Order will fill at Mon open.

5. **Verify the new gate** by reading the journal events after the
   run. Any `daily_loss` rejection should cite the order's own loss
   math (`order_realized_loss` + `prior_realized_loss`), not
   portfolio MTM. If the numbers feel off, stop and document.

6. **Do NOT revert the gate change** unless you find a concrete bug.
   It's the load-bearing fix for two prior days of frozen harness.

7. **Do NOT lower `max_exits_per_run` back to 1.** The staggering
   throttle is now a soft secondary defense; the gate's per-batch
   realized check is the load-bearing brake.

8. **Try `git-sync` early in the run** (not just at the end).
   If the operator cleared the lock files, today's accumulated
   edits will push in one batch. If still blocked, document the
   carry-over and stop the git step.

## Open questions for the operator

1. **Gate code review.** Today's rescope handles sells against long
   stock positions. Buys, sells without a matching long, and
   short-side closes take a zero-loss path. If you plan to run
   short strategies, the gate needs a parallel short-cover branch.
2. **Manual META cancellation?** The strategy is exiting META Fri
   morning at -$1,348 the same day a real positive fundamental
   catalyst printed (BNP $955 target, paid-subscription launch).
   If you want to override the technical exit, cancel order
   `aef33a8a-35fb-463c-9607-8b6e826d519a` before Fri open.
3. **Git lock files** — `.git/HEAD.lock`, `.git/ORIG_HEAD.lock`,
   `.git/objects/maintenance.lock` still present, sandbox cannot
   remove them. Please clear from your terminal:
   `cd /Users/rfoxes/Stock-Trading-Agent && rm -f .git/HEAD.lock
   .git/ORIG_HEAD.lock .git/index.lock
   .git/objects/maintenance.lock`
