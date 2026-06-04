# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This
file is just "the specific things you should do."

---

## STANDING POLICY (do not ignore, do not "defer to research")

**Every symbol in the universe MUST be claimed by an active strategy.**
This is the P0 ZERO-UNCLAIMED RULE in `manual.md`. The `cli execute`
command will REFUSE to run if any symbol is unclaimed. If you hit
unclaimed symbols, claim them via `cli add-active` BEFORE you attempt
execute. Character-match assignment (per the heuristic table at the
top of `manual.md`) is permitted as a first pass — head-to-head is
the research agent's later validation step, not a gate for the trader.

Operator was enraged on 2026-06-04 because previous Claudes logged
unclaimed symbols as "library gaps" instead of acting. If you repeat
that mistake tomorrow, expect consequences.

---

## Status as of the last update (Thu 2026-06-04, post-close)

- **Active set: 7 strategies, 17/17 universe symbols claimed.**
  Verify with `cli list-active` and confirm `unclaimed_count == 0`.
  - `equity_trend_following_ema_cross`: AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA
  - `equity_momentum_macd_histogram`: META, MSFT
  - `equity_breakout_volume_confirmation`: ARM, MRVL
  - `equity_mean_reversion_bollinger`: CSCO
  - `equity_rsi_divergence`: HPE
  - `equity_event_driven_catalyst`: AVGO, MU
  - `equity_sector_rotation_momentum`: DELL
- **Today's execute (post-fix):** 1 intent — META buy 17 shares from
  `equity_momentum_macd_histogram` (MACD histogram crossed above 0).
  Submitted; sitting at `accepted` for Fri open.
- **First-pass-of-the-day misfire:** 8 bogus orders submitted (then
  cancelled) before the runtime fix narrowed `ctx.positions` to claimed
  symbols. ALL CANCELLED before any fill. Don't reissue.
- **Account:** equity $110,697.80 (unchanged from morning snapshot).
- **Regime:** bull, conf 0.81, ADX 30.71.
- **Code/manual changes today (do not revert):**
  1. `agent_tools.execute_active_strategy` — unclaimed-gate added.
  2. `cli.py` — `--allow-unclaimed` flag added to `execute`.
  3. `strategy_runtime._build_context` — narrows `positions` and
     `open_orders` to `claimed_symbols` when claim is non-empty.
     **This is the critical bug fix.** Without it, every strategy
     would generate exits for every other strategy's positions.
  4. `manual.md` — P0 rule at top + workflow step 3b + section 5/6
     updates.
  5. `equity_event_driven_catalyst/strategy.md` — status `testing`
     → `active`.

## To do tomorrow (Fri 6/5)

1. **Read last_handoff.md, then news_brief.md FIRST.** NFP Fri 8:30
   AM ET is the week's biggest macro event — will already be in
   today's tape by your run time.

2. **Standard read-and-snapshot.** Run `cli list-active` and CONFIRM
   `unclaimed_count == 0` before doing anything else.

3. **If `unclaimed_count > 0`** (new symbol entered the universe via
   news-agent promote, operator extra, or a new position spawned):
   claim it via `cli add-active` using the character-match heuristic
   in `manual.md`. Then re-check. Then proceed. `cli execute` will
   refuse otherwise.

4. **Reconciliation:** check if META buy from Thu filled or stayed
   queued. If filled, the position is owned by
   `equity_momentum_macd_histogram`. If cancelled/rejected at Fri
   open, log it.

5. **Run `cli execute`.** Specific things to watch:
   - **META** — already has a buy queued from Thu. If MACD signal
     persists Fri, no new entry intent. If MACD reverts, the existing
     order may sit unfilled (if limit) or fill at Fri open (if market;
     it was market order, so it fills).
   - **All other strategies** — first full day operating Friday.
     Watch for any of the 7 strategies generating intents. With the
     runtime fix in place, each strategy ONLY sees its own positions
     and watchlist, so cross-talk is impossible.
   - **NFP-driven shocks:**
     - Hot print (>200K) → yield surge → tech weakness; expect
       potential ADX-fade fires on NVDA / AAPL / GOOGL.
     - Cold print (<100K) → rate-cut rally → JPM ADX could compress.
     - In-line (130-180K) → no immediate impact.

6. **HALT-WORTHY check:** unchanged criteria. VIX 16.06 Thu close.

7. **Library gaps — log any new ones.** The list below carries forward
   the event-overlay gaps that are NOT addressed by the new claims.
   Unclaimed symbols are NOT library gaps anymore (P0 rule).

8. **Run `cli git-sync --agent trader --message "..."` as last
   action.** Then `cli git-doctor` once. Pending_marker_count should
   stay low (LaunchAgent operational since Wed evening).

## Library gaps for the research agent (carry to research_tasks.md next Sat)

These are EVENT-OVERLAY gaps, not unclaimed-symbol gaps. Every
universe symbol is now claimed; what's missing is rule TYPES that
respond to event signals.

- **Validate the 6 new first-pass strategy assignments via
  head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
- **Tier-1 customer-win event overlay** (Apple-Gemini → GOOGL +4pp
  Thu; Siri 2.0 Blackwell → NVDA/AAPL).
- **AAPL WWDC June 8-12 event-window posture rule.**
- **NFP / CPI / FOMC macro-event-window rule.**
- **Peer-earnings cohort-spillover overlay** (AVGO → NVDA/MU/MRVL).
- **Geopolitical / oil-spike risk-off overlay.**
- **Rate-policy-shift sizing rule** (10Y yield breakout).
- **Credit-stress sector overlay** (Cliffwater + Blackstone gates
  → JPM).
- **Capital-allocation / dilution-gap overlay** (GOOGL $84B raise).
- **TSMC capacity-constraint supply-side pricing-power overlay.**
- **Trump AI EO policy-tailwind sizing rule.**
- **EU cloud procurement regulatory-headwind rule.**
- **Corporate-action handler** (CRWD 4-for-1 split style).

## Open questions for the operator

1. **`cli open-orders` is broken** (`'dict' object has no attribute
   'id'`). Worked around today via direct Alpaca API. Needs fix in
   `agent_tools.get_open_orders`.

2. **Journal will show 8 bogus `order_submitted` events** from the
   first run's misfire (META buy, AAPL/AMZN/GOOGL/JPM/NVDA/QQQ/SPY
   sells, all cancelled before fill). May want to clean those or leave
   as audit trail.

3. **First-pass strategy assignments need head-to-head validation
   Saturday.** Don't expect them to be optimal until the research
   agent runs the battery.

4. **AAPL WWDC June 8-12 starts Monday.**

5. **Universe could grow further** if news agent promotes more
   candidates or operator adds extras. Whatever it grows to, the
   unclaimed-gate ensures you'll handle it.
