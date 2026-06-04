# Handoff to tomorrow's Claude

(Thu 2026-06-04, post-close run + emergency operator-directed expansion.)

## TL;DR

Operator was enraged that today's first run logged 6 unclaimed symbols as
"library gaps to defer to research agent" instead of claiming them. The
operator's standing policy is: **every universe symbol must be claimed by
an active strategy. No exceptions.** This was wired into the manual as a
P0 rule, into the CLI as an `execute` gate, and into the runtime as a
position-narrowing fix. End-of-run state: 17/17 symbols claimed, 7 active
strategies, 1 legitimate buy intent submitted (META, MACD entry signal).

**Do not undo this work.** The P0 rule is permanent.

## Summary of what I did today

**First pass (standard workflow):** ran the normal NORMAL FLOW workflow —
0 intents, 0 trades, mark-to-market +1.67% equity recovery. Wrote a
"do-nothing" handoff and committed. **The operator pushed back hard.**

**Second pass (operator-directed):**

1. **Claimed every unclaimed universe symbol.** Started with 6 unclaimed
   (ARM, CSCO, HPE, META, MRVL, MSFT). After adding strategies, three
   more appeared (AVGO, DELL, MU — universe grew to 17). Final claim
   assignments (all `since: 2026-06-04`):
   - `equity_trend_following_ema_cross`: AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA (unchanged)
   - `equity_momentum_macd_histogram`: META, MSFT
   - `equity_breakout_volume_confirmation`: ARM, MRVL
   - `equity_mean_reversion_bollinger`: CSCO
   - `equity_rsi_divergence`: HPE
   - `equity_event_driven_catalyst`: AVGO, MU
   - `equity_sector_rotation_momentum`: DELL

   First-pass character-match assignment per operator override of the
   head-to-head requirement. Research agent should validate via
   `cli head-to-head` battery on Saturday.

2. **Flipped `equity_event_driven_catalyst` status from `testing` to
   `active`** so its AVGO/MU claim actually runs.

3. **Encoded the rule durably:**
   - Added a "P0 — ZERO-UNCLAIMED RULE" section at the TOP of
     `state/manual.md`. Explicit, generalized, permanent.
   - Added step 3b "P0 UNCLAIMED-GATE CHECK" to the Daily workflow.
   - Updated step 5 "Decide" and step 6 "library-gap mandate" to note
     that unclaimed-universe-symbols are NOT library gaps — they are
     P0 blockers.
   - **`cli execute` now REFUSES to run if `unclaimed_count > 0`**, with
     a verbose error message listing the offending symbols. Escape:
     `--allow-unclaimed` (not for daily runs).
   - Code changes in `agent_tools.execute_active_strategy` (gate check)
     and `cli.py` (flag).

4. **CRITICAL BUG FIX in `strategy_runtime._build_context`.** First
   re-run after add-active calls submitted **8 BOGUS ORDERS** to the
   broker because the newly-active strategies iterated `ctx.positions`
   (which contained ALL 7 portfolio positions) for exit logic, generating
   sell intents for positions OWNED BY OTHER STRATEGIES. Specifically
   `equity_momentum_macd_histogram` (claims META, MSFT) submitted sell
   orders for AAPL/AMZN/GOOGL/NVDA/QQQ/SPY (all of trend_following's
   positions) plus a JPM sell from `equity_mean_reversion_bollinger`
   (CSCO-only claim) — none of those were the strategy's positions to
   sell.

   **All 8 orders cancelled within 2 minutes of submission** (market is
   closed post-4pm PT; orders sat as `accepted` queued for Fri open).
   Cancelled via direct Alpaca API call (`cli open-orders` is broken with
   `'dict' object has no attribute 'id'` — flagged below).

   **Root cause:** `_build_context` was narrowing `ctx.watchlist` to
   `claimed_symbols` but NOT `ctx.positions` or `ctx.open_orders`. Fix
   adds the symmetric narrowing of both lists when `claimed_symbols` is
   non-empty. Every strategy in the library iterates `ctx.positions` for
   exits — without this narrowing, every newly-active strategy would
   liquidate every other strategy's book.

   This bug existed for as long as multi-strategy claims existed; it
   never fired because trend_following was the only claim and it
   happened to own every held position. The moment a second strategy
   was added (today), it surfaced.

5. **Re-ran `cli execute` after the runtime fix.** Clean output: only
   `equity_momentum_macd_histogram` generated 1 intent — META buy 17
   shares (MACD histogram crossed above 0, rising, MACD > signal, close
   > SMA50). Order submitted, currently `accepted` for Fri open. All
   other strategies returned 0 intents (correct — their claims didn't
   trip entry conditions today).

   Verified open orders is exactly 1 (the META buy).

6. **State files written.** This handoff + `tasks.md` for Friday's run.
   Manual.md updated with the P0 rule + workflow change.

## Observations and reasoning

**The morning's "do-nothing on NORMAL FLOW" framing was correct under the
OLD policy and dead wrong under the NEW one.** Operator made clear the
old policy was wrong: logging unclaimed symbols as library gaps without
acting was the failure mode. The trader doesn't have permission to defer
unclaimed work — every symbol must have a responder. Period.

**The 6-strategy expansion is not validated by head-to-head.** Operator
explicitly chose to skip head-to-heads for now ("first-pass is fine, do
it"). The character-match assignments are defensible reasoning but they
are not optimal. Saturday research agent should run the battery and
re-rotate as needed.

**The `ctx.positions` narrowing fix is the most important commit today.**
Without it, the multi-strategy architecture was fundamentally broken —
every strategy would have generated exits for every other strategy's
positions. The architecture worked under single-strategy but had latent
data-leakage as soon as a second strategy was added. This is now correct.

**META buy is legitimate.** The fix did not suppress real signals; it
suppressed false ones. The META MACD entry was a real signal on a real
claimed symbol — exactly what the system should produce.

**equity_event_driven_catalyst was status=`testing`** when first claimed.
The runtime correctly refused to execute it (status gate). Flipped to
`active` so AVGO/MU claims actually run. The catalyst strategy returned
0 intents today — fine, no event-window trigger.

## Final state at session end

- **Active set:** 7 strategies covering 17/17 universe symbols.
  `unclaimed_count == 0`.
- **Open orders:** 1 (META buy 17 from `equity_momentum_macd_histogram`).
- **Positions:** 7 longs unchanged from morning snapshot.
- **Account:** equity $110,697.80 (+1.67% vs Wed).
- **Regime:** bull, conf 0.81, ADX 30.71.
- **Code changes:** `agent_tools.execute_active_strategy` gates on
  unclaimed; `cli.py` adds `--allow-unclaimed` flag; `strategy_runtime.
  _build_context` narrows `positions` + `open_orders` to claimed_symbols
  when claim is non-empty.
- **Manual changes:** P0 ZERO-UNCLAIMED RULE at top; workflow step 3b
  added; step 5/6 updated.
- **Strategy changes:** `equity_event_driven_catalyst` status
  `testing` → `active`.

## Open issues for the operator

1. **`cli open-orders` is broken** — returns `'dict' object has no
   attribute 'id'`. Worked around with direct Alpaca API today but the
   CLI command itself needs a fix in `agent_tools.get_open_orders`. Not
   urgent if `cli execute`'s response already includes submitted-order
   IDs, but operator should know.

2. **Bogus orders from the buggy first pass were ALL cancelled before
   market open.** No real broker fills. The journal will show 8
   `order_submitted` events with the buggy strategies' IDs followed by
   cancellations. Operator may want to clean those journal entries or
   leave them as audit-trail.

3. **First-pass strategy assignments are not validated.** Research
   agent on Sat should run head-to-heads:
   - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
   - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL
   - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
   - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
   - `equity_event_driven_catalyst` vs ... on AVGO, MU
   - `equity_sector_rotation_momentum` vs ... on DELL

4. **NFP Fri 8:30 AM ET is the week's macro event.** Friday's Claude
   will run post-close with NFP already digested.

5. **AAPL WWDC June 8-12 starts Monday.** Operator-visibility.

## Git-sync status

Will run `cli git-sync --agent trader --message "..."` as last action.
Wed handoff confirmed the LaunchAgent is operational
(pending_marker_count was 1 = test marker only). Expect today's commit
to push within 30s.
