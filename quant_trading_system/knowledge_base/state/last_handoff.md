# Handoff to tomorrow's Claude

## Summary of what I did today

Two runs today: the scheduled 4 PM PT trader run, then an operator-initiated
fix session.

**Run 1 — scheduled trader (Thu 23:10 UTC):**
- Read manual, tasks, handoff, active_strategy, news_brief.
- Active strategy unchanged: `equity_trend_following_ema_cross`.
- Snapshot: equity $112,803.90 (+1.09% vs. Wed), same 10 longs, no closes.
- `execute` → 1 intent (MSFT sell 44, staggered smallest-loss-first per
  the overnight `max_exits_per_run: 1` edit, 1 other deferred).
  Rejected by SafetyGate `daily_loss` at 2.1% > 2.0%.
- Discovered the `daily_loss` check measures portfolio-wide unrealized
  losses, NOT per-batch realized as everyone (including yesterday's
  handoff and the manual's Recent feedback bullet) had assumed.
- Wrote new handoff + tasks; appended a correction bullet to manual's
  Recent feedback section.
- Git-sync failed (stale `.git/HEAD.lock`, `.git/ORIG_HEAD.lock` the
  sandbox can't unlink).

**Run 2 — operator-initiated fix session (Thu evening interactive):**
- Operator asked to fix three things: gate blocking everything, the
  strategy keeping longs that aren't strategy-aligned, and the git
  push failure. Confirmed direction with two AskUserQuestion answers:
  (a) "see if [each position] is in line with the strategies; don't
  permanently hold them; only keep them if there's a strategy in mind"
  and (b) "rescope the gate to per-batch realized P&L."
- **Rescoped `SafetyGate.daily_loss`** (`brokers/safety_gate.py`
  lines 337-415). The check now estimates the proposed order's
  realized loss (qty × (current_price − avg_entry) for sells against
  long positions, capped at zero for profitable closes), sums with
  `_daily_realized_loss` (cumulative session realized), and rejects
  if it exceeds `MAX_DAILY_LOSS_PCT × equity`. Approved sells accrue
  their estimated realized loss into `_daily_realized_loss` so the
  next order in the same batch sees the cumulative number. The old
  portfolio-wide-unrealized semantics are gone.
- **Raised `max_exits_per_run` from 1 → 5** in
  `equity_trend_following_ema_cross/strategy.md` frontmatter, and
  rewrote the staggered-exit paragraph to reflect the new gate.
  Rationale: with per-batch realized as the safety property, the
  staggering throttle is a soft secondary defense, not the load-bearing
  brake. 5 is high enough to clear a typical day's exit basket in one
  session while still bounding pathological cascades.
- **Re-ran `execute`** against the new gate. **2 intents submitted,
  0 rejected:** MSFT sell 44 (order `4460e8c5-d063-4929-95ad-7e04b1da8789`,
  est. P&L +$267) and META sell 28 (order
  `aef33a8a-35fb-463c-9607-8b6e826d519a`, est. P&L -$1,348). Combined
  realized loss: 1.19% of equity, under the 2% cap. Both orders are
  market `day` orders submitted post-close, so they will fill at Fri
  2026-05-29 open. JPM was NOT flagged today — its ADX recovered
  above 20 (was 19.7 Wed).
- **Did not** force-flush the other 8 longs. Per operator directive
  ("only keep them if there's a strategy in mind"), I verified each
  is strategy-aligned: AAPL (+15.0%), AMZN (+9.8%), GOOGL (+14.9%),
  JPM (-5.2% but ADX recovered → trend intact), NVDA (+7.4%), QQQ
  (+13.5%), SPY (+6.5%), TSLA (+9.0%). None tripped the strategy's
  exit rules (death-cross, ADX < 20, trailing stop, gap-down 4%);
  all remain held with explicit strategy attribution.
- **Git-sync still failed.** Stale `.git/HEAD.lock`,
  `.git/ORIG_HEAD.lock`, and `.git/objects/maintenance.lock` are all
  present and the sandbox returns "Operation not permitted" on unlink
  for all three. The operator needs to clear them from a real terminal:
  `cd /Users/rfoxes/Stock-Trading-Agent && rm -f .git/HEAD.lock .git/ORIG_HEAD.lock .git/index.lock .git/objects/maintenance.lock`
  and then `git push origin main` to publish today's edits.

## Observations and reasoning

### Broker snapshot (Thu 2026-05-28 post-close)

- **Account:** equity $112,803.90 (+1.09% vs. Wed), cash -$96,531.22
  (unchanged to the cent, 16th day), buying_power $16,272.68. No day
  trades.
- **Positions (pre-exit-orders, still showing all 10 — orders are
  queued, not filled):**
  AAPL 72 +14.92%, AMZN 76 +9.76%, GOOGL 56 +14.91%, JPM 64 -5.19%,
  META 28 -7.18%, MSFT 44 +1.54%, NVDA 96 +7.42%, QQQ 28 +13.51%,
  SPY 35 +6.51%, TSLA 48 +9.01%.
- **Regime:** `bull, conf=0.76, adx=26.33` — third consecutive day of
  byte-identical classifier output.
- **Open orders (post-fix):** 2 sells (MSFT, META) queued for Fri open.

### Why the gate semantics matter so much

The old gate `unrealized_loss = sum(p.unrealized_pl < 0)` was a
portfolio-stress halt: any day with > 2% mark-to-market drawdown
froze the harness. Concrete failure mode observed today: a
*profitable* MSFT exit (+$267) was rejected because unrelated
unrealized losses on JPM and META summed to 2.13% of equity.
That's wrong both pragmatically (good exits get blocked, bad
unrealized stays unbooked) and semantically (the variable name
`daily_loss` implies "loss being booked today," not "current MTM").

The new code measures what the name says: the loss the *proposed
trades* would book if filled at marks, plus any session-realized
losses already accrued. Pathological case: a strategy proposes 10
sell intents whose combined realized loss exceeds 2% equity. The
gate processes them serially, accrues each approved loss into
`_daily_realized_loss`, and rejects the first intent that would push
cumulative > cap. That's the graduated-exit safety property
yesterday's handoff *thought* the gate already had. It does now.

### News brief × execution

Brief was NOTABLE: META subscription launch (positive, fresh
catalyst), AMZN/SNOW $6B AWS deal (positive), NVDA/Loomer Tsinghua
political risk (two-way), MSFT softer AI-coding-tool growth
narrative (mild negative). Strategy is purely technical and didn't
read the brief. Notable tension on META: the strategy is exiting
META at -$1,348 the same day a real fundamental positive printed
(BNP $955 target, ~$13.5B incremental rev by 2028). This is a
strategy-vs-fundamentals divergence the operator should be aware
of. The technical case (ADX-fade) and the fundamental case
(monetization catalyst) are pointing opposite directions on META
right now. The strategy chose technicals; that's what it's
designed to do.

### Estimated fills tomorrow (Fri 2026-05-29 open)

If filled at Thursday's close marks (good approximation for
liquid mega-caps at the open):

- **MSFT sell 44 @ ~$427.31:** realized = 44 × (427.31 − 421.236) =
  **+$267 (+1.44%)**. Profitable exit.
- **META sell 28 @ ~$633.41:** realized = 28 × (633.41 − 681.555) =
  **-$1,348 (-7.06%)**. Loss exit per ADX-fade rule.
- **Net:** -$1,081 (-0.96% of equity).
- **Combined realized loss:** $1,348 (META alone, MSFT contributes
  no loss), or 1.20% of equity. Comfortably under the new gate.

### Carry-forwards

- Journal has 4 cumulative `order_rejected` events + 2 fresh
  `order_submitted` events from the fix run.
- Strategy library: 19 strategies on disk (count up by 1 from
  prior days — not investigated).
- `safety_gate.py` modified (significant logic change). Should be
  reviewed by the operator before the next scheduled run for any
  edge cases I missed (e.g. limit-orders against missing positions,
  multi-leg options, short positions — the new code only handles
  sells against long stock positions; other order types take a
  zero-loss path).

## Recommendations for tomorrow's Claude (Fri 2026-05-29)

1. **First — read this entire handoff before running anything.** The
   safety_gate.py change is significant. If the gate fix has any
   side effects you don't understand, stop and document instead of
   plowing through.

2. **Standard read-and-snapshot.** Check `state/` mtimes for any new
   operator note.

3. **Check fills.** The 2 orders queued today should fill at
   Fri open. After snapshot:
   - If MSFT and META are no longer in `positions`, run:
     - `python3 -m quant_trading_system.cli log-closed
       equity_trend_following_ema_cross MSFT <pnl_fraction>` using
       the actual realized P&L fraction from the fill.
     - Same for META.
   - If either is still held (partial fill, order rejected at open
     for some broker reason), document and investigate.

4. **Then run `execute`.** Expected behaviors:
   - With MSFT and META gone, the strategy will scan 8 remaining
     longs (AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA).
   - JPM is the watch-item: ADX was 19.7 Wed, recovered Thu (no
     flag). If Fri's tape pushes JPM ADX back below 20, it will
     flag for exit (-$1,051 estimated loss = 0.93% equity, well
     under cap). Strategy will submit cleanly.
   - All other 7 positions are profitable trend-aligned — strategy
     should leave them alone.
   - No more `daily_loss` rejections under the new gate unless a
     batch's realized losses actually exceed 2% equity, which would
     require ~$2,250+ of proposed realized losses in one run.

5. **Verify the new gate behavior on the first run.** Read the
   journal events and confirm `loss_pct` numbers in any rejection
   reasons (if there are any) reflect *this batch's* loss math, not
   portfolio MTM. If the numbers don't match the new semantics, the
   fix has a bug.

6. **Do NOT revert the gate change** unless you find a concrete bug.
   The previous semantics were the source of two days of frozen
   harness.

7. **News brief: re-read it.** META catalyst (subscriptions) is now
   moot since we're exiting today. NVDA/Loomer overnight is the
   main two-way risk. Iran MoU approval signal also overnight.

8. **Check git-sync.** If the operator cleared the lock files, the
   normal `git-sync --agent trader` should work. If still blocked,
   document and stop — same outcome as the last two runs.

## Open questions for the operator

1. **Gate logic review.** The new `safety_gate.py` daily_loss check
   handles sells against long stock positions cleanly. It takes a
   conservative zero-loss path for buys, sells without a matching
   position, and shorts. Are those edge cases what you want? In
   particular: **short-cover buys** (closing a short for a loss)
   are not currently counted toward `daily_loss`. If you plan to
   run short strategies in the future, the gate needs a parallel
   branch for short-side closes.
2. **Strategy-vs-fundamentals divergence on META.** Strategy is
   exiting META Fri morning at -$1,348 the same day a real positive
   fundamental catalyst printed. This is what trend-following does
   — it doesn't look at news. Just flagging in case you want to
   intervene before Fri open (manual cancel of order
   `aef33a8a-35fb-463c-9607-8b6e826d519a`).
3. **Git lock files** — `.git/HEAD.lock`, `.git/ORIG_HEAD.lock`,
   `.git/objects/maintenance.lock`. Please clear from your terminal
   so today's edits push.

## Git-sync status

Will retry as last step but expect failure (locks still present).
Today's edits live on the sandbox disk:
- `quant_trading_system/brokers/safety_gate.py` (gate rescope)
- `quant_trading_system/knowledge_base/strategies/equity/trend_following_ema_cross/strategy.md` (max_exits_per_run 1→5)
- `quant_trading_system/knowledge_base/state/last_handoff.md` (this file)
- `quant_trading_system/knowledge_base/state/tasks.md`
- `quant_trading_system/knowledge_base/state/manual.md`
- `trades/2026-05.jsonl` (journal — 6 fresh events)

If the operator clears the locks tonight, tomorrow's first git-sync
will push everything in one batch.
