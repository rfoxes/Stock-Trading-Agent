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
  - 1 add attempted: `equity_momentum_macd_histogram_v2` — REJECTED
    by addition battery (num_trades 2 < 20). Cleaned up.
  - 9 canonical head-to-head verdicts recorded (see
    `research_log/2026-06-06.md`). Recommended swaps for trader to
    apply Monday: MSFT/ARM/AVGO/MU/DELL all move to
    `equity_trend_following_ema_cross`.
- **Mid-session bug fixes (operator instruction):**
  1. `cli head-to-head` was broken (stale `EquityBacktester` kwarg).
     Now delegates to `strategy_backtest.run_backtest`. Verified
     end-to-end.
  2. `cli evaluate-archive` falsely ARCHIVED a 4-day-old strategy
     because broker-rejected events were counted as lifetime
     evidence. Now requires `order_submitted` or `trade_closed`.
     Verified — rsi_divergence now correctly returns KEEP.
- **Backtester:** all CLI paths (`simulate`, `evaluate-add`,
  `evaluate-update`, `evaluate-archive`, `head-to-head`) now work
  end-to-end.
- **Outstanding calibration question: addition battery's
  `min_num_trades = 20` is unreachable on single-symbol simulate.**
  Most active strategy maxes out at 16 trades/2yr on the most active
  large-cap. Documented in `research_manual.md` "Recent feedback".

## To do this Saturday

1. **Verify trader applied the recommended head-to-head swaps Monday.**
   Run `cli list-active`. Expected outcome (if trader executed the
   recommendation):
   - `equity_trend_following_ema_cross` claims AAPL, AMZN, ARM, AVGO,
     DELL, GOOGL, JPM, MSFT, MU, NVDA, QQQ, SPY, TSLA (13 symbols).
   - `equity_momentum_macd_histogram` claims META (1).
   - `equity_breakout_volume_confirmation` claims MRVL (1).
   - `equity_mean_reversion_bollinger` claims CSCO (1).
   - `equity_rsi_divergence` claims HPE (1).
   - 17/17 claimed.
   If trader did NOT swap, examine `state/last_handoff.md` for the
   reason and re-document the recommended swaps in this Saturday's
   log.

2. **Re-run head-to-head once we have more journal data.** This week
   would be the first opportunity to re-test the AVGO/MU/DELL pairs
   if any of those strategies actually fire during the week — the
   2024-06 → 2026-06 window will have advanced and we may see real
   signal. Same pairs as last week's table.

3. **MACD histogram v3 attempt — minimum-hold variant.** Previous v2
   (3-bar rising + ADX>20) was too restrictive (cut trades from 16 to
   2 on META). Try a *minimum-hold* variant: same v1 entry, but
   require a 3-session hold before any exit can fire. This addresses
   the Fri 2026-06-05 META 1-day round-trip without restricting
   entries. May still fail the 20-trade floor; document and skip if so.

4. **Investigate `equity_event_driven_catalyst` (`status: testing`).**
   It's in testing but has never fired in backtest or live. AVGO/MU
   were claimed to it but the canonical head-to-head moved them
   away. Either promote to `active` (if it would have fired in backtest)
   or archive (if it can't). Run `cli evaluate-add` on it.

5. **Address the `min_num_trades = 20` calibration question.** If
   operator hasn't responded to last week's note, consider proposing a
   multi-symbol simulate as the actual fix. Implementation sketch in
   open questions below.

6. **Universe-expansion candidates** (news layer keeps flagging
   STM, TSM, CRWD, PINS, SNOW, NTAP, OKTA, NOW, TEAM). If the operator
   wants these into the universe, add via `state/extra_symbols.md`
   and they'll need claims. Defer to operator direction.

7. **Recurring archive sweep.** Run `cli evaluate-archive` on every
   `status: active` strategy. With the bug-fix in place this is now a
   reliable sweep.

8. Write `knowledge_base/research_log/<today>.md` and replace this
   file with next Saturday's task list.

## Open questions for the operator

1. **Addition battery's `min_num_trades = 20` is unreachable on
   single-symbol simulate.** Either: (a) lower the floor (~10), (b)
   add multi-symbol simulate support (each strategy's `evaluate(ctx)`
   loops over `ctx.watchlist`, so it's a natural extension), or (c)
   extend the default backtest window to 3-5 years. Suggested:
   option (b). The current single-symbol approach undercounts because
   each strategy is built to be a universe-wide responder, not a
   per-symbol entry generator.

2. **Event-overlay architecture.** The M-F trader's library-gap list
   is all event-overlay rules (WWDC window, NFP window, peer-earnings
   spillover, etc.) — not standalone strategies. These cannot be
   added via `propose-strategy` because they aren't backtestable in
   isolation. Is this in scope for the research agent, or should I
   keep flagging them for operator direction?

3. **Tiebreak semantics on head-to-head.** When both strategies have
   0 trades on a symbol, the current decision rule picks the one with
   smaller `max_drawdown` — but a 0-trade strategy's `max_drawdown` is
   always 0.00, so the strategy that fires *less* effectively wins by
   default. This is what drove the AVGO/MU/DELL recommendations.
   Suggestion: change the rule to "if both have 0 trades, return tie
   (`winner: null`) and let the operator decide."

4. **AAPL WWDC June 8-12 (already started Monday).** No event-window
   rule. Trader will not adjust posture. Carrying forward; cannot be
   addressed via addition battery without an overlay primitive.
