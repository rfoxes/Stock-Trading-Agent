# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update

- **Library size:** 19 strategies on disk (11 equity, 8 options).
  18 `active`, 1 `testing` (`equity_event_driven_catalyst`). 0 archived.
- **Last week's additions:** none.
- **Last week's updates/archives:** none.
  - 1 add attempted: `equity_momentum_macd_histogram_v2` — REJECTED by
    addition battery (num_trades 2 < 20, PSR 0.894 < 0.95, sortino
    0.315 < 0.5, OOS/IS -0.33 < 0.5). Cleaned up.
  - 1 ARCHIVE verdict was returned on `equity_rsi_divergence` but
    NOT applied — appears to be an evaluate-archive bug counting
    broker-rejected events as evidence. See log for details.
- **Backtester:** FIXED (last week's universe= patch landed). `cli
  simulate` and `cli evaluate-add` work end-to-end.
- **Blocker #1: `cli head-to-head` broken.** `agent_tools.py:1316`
  passes `strategy_frontmatter=` to `EquityBacktester()` but the
  constructor only accepts `market_data=`. Operator was notified.
- **Blocker #2: `cli evaluate-archive` counts broker-rejected events
  as lifetime history.** False-positive ARCHIVE on a 4-day-old
  strategy (`equity_rsi_divergence`). Operator was notified.
- **Calibration insight: addition battery's `min_num_trades = 20` is
  unreachable on single-symbol simulate.** Most active strategy maxes
  out at 16 trades/2yr on the most active large-cap. Added to
  `research_manual.md` "Recent feedback".

## To do this Saturday

1. **Verify the two infrastructure fixes:**
   - `cli head-to-head equity_momentum_macd_histogram equity_trend_following_ema_cross --symbol META --start 2024-06-08 --end 2026-06-08`
     should return `ok: true` with a `winner` field.
   - `cli evaluate-archive equity_rsi_divergence` should return KEEP
     with "no lifetime trading evidence" or similar (not ARCHIVE).
   - If both fixed → resume the operator-requested adjudication queue
     in step 2. If either still broken → document and skip.

2. **(Gated on head-to-head fix.) Run canonical head-to-head on the
   9 strategy/symbol pairs surveyed via simulate-substitute last week
   (see `research_log/2026-06-06.md` table).** For each:
   - If head-to-head produces a clear winner that differs from the
     current claim in `active_strategies.md`, document the recommendation
     in this Saturday's log. **Do not edit `active_strategies.md`** — the
     trader does that via `cli remove-active` / `cli add-active` on
     Monday based on the research log.
   - Targets in priority order:
     1. META → macd_histogram vs trend_following_ema_cross (Fri
        round-trip is fresh evidence — examine the test result for
        whether trend_following's silence is actually a stronger signal).
     2. MRVL → breakout_volume_confirmation vs trend_following_ema_cross
        (last week's substitute showed +1.46 vs 0.00 — likely confirms).
     3. HPE → rsi_divergence vs trend_following_ema_cross.
     4. CSCO → mean_reversion_bollinger vs trend_following_ema_cross.
     5. ARM → breakout_volume_confirmation vs trend_following_ema_cross.
     6. MSFT → macd_histogram vs trend_following_ema_cross.
     7-9. AVGO, MU, DELL — both incumbent and candidate were silent in
          substitute. May still be silent under canonical head-to-head.

3. **(Gated on archive-battery fix.) Re-run evaluate-archive on
   `equity_rsi_divergence`** to confirm the fix returns KEEP.

4. **MACD histogram v3 attempt — different angle.** Last week's v2
   (3-bar rising + ADX>20) was too restrictive. Try a *minimum-hold*
   variant instead: same v1 entry, but require a minimum 3-session
   hold before any exit can fire. This addresses the trader's
   round-trip flag without restricting entries. If the addition
   battery is recalibrated (lower trade floor or multi-symbol), this
   should be testable. If the 20-trade floor is unchanged, document
   and skip.

5. **Investigate `equity_event_driven_catalyst` (`status: testing`).**
   It's been in testing since before the M-F harness existed. The
   strategy has never fired and is claimed on AVGO + MU. Either
   promote to `active` (if it would have fired in backtest) or
   archive (if it can't). Run `cli evaluate-add` on it.

6. **Universe-expansion candidates** (news layer keeps flagging
   STM, TSM, CRWD, PINS, SNOW, NTAP, OKTA, NOW, TEAM). If the operator
   wants these into the universe, add via `state/extra_symbols.md`
   and they'll need claims. Defer to operator direction.

7. **Recurring archive sweep.** Run `cli evaluate-archive` on
   `equity_trend_following_ema_cross` (only strategy with successful
   journal history). Likely KEEP again given small N.

8. Write `knowledge_base/research_log/<today>.md` and replace this
   file with next Saturday's task list.

## Open questions for the operator

1. **`cli head-to-head` broken** (blocking all symbol-claim
   adjudication). See `research_log/2026-06-06.md` § "Infrastructure
   issue #1" for the exact line and suggested one-line fix.

2. **`cli evaluate-archive` counts broker-rejected events as lifetime
   evidence.** See `research_log/2026-06-06.md` § "Infrastructure
   issue #2". False-positive ARCHIVE on `equity_rsi_divergence`.
   Suggested fix: require ≥1 successful order or close for the
   lifetime-history safety check.

3. **Addition battery's `min_num_trades = 20` is unreachable** on
   single-symbol simulate for the current library calibration. Either
   lower the floor (~10), add multi-symbol simulate support, or
   accept that single-symbol additions are blocked by design. See
   `research_log/2026-06-06.md` § "Structural insight" for the data.

4. **Event-overlay architecture.** The M-F trader's library-gap list
   is all event-overlay rules (WWDC window, NFP window, peer-earnings
   spillover, etc.) — not standalone strategies. These cannot be
   added via `propose-strategy` because they aren't backtestable in
   isolation. Is this in scope for the research agent, or should I
   keep flagging them for operator direction?

5. **AAPL WWDC June 8-12 starts Monday.** No event-window rule. Trader
   will not adjust posture. Carrying forward; cannot be addressed via
   addition battery.
