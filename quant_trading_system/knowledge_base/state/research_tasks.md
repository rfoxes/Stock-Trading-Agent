# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update

- **Library size:** 19 strategies on disk (11 equity, 8 options).
  18 `active`, 1 `testing` (`equity_event_driven_catalyst`). 0 archived.
- **Last week's additions:** none.
- **Last week's updates/archives:** none — the addition battery was
  broken (see below), and the only archive-eligible strategy returned
  KEEP for lack of journal evidence.
- **Open candidates from last week:** none.
- **Blocker:** `cli simulate`, `cli propose-strategy`, `cli evaluate-add`,
  `cli evaluate-update` all fail with `StrategyContext.__init__() missing
  1 required positional argument: 'universe'`. Root cause: the
  `StrategyContext(...)` call in `quant_trading_system/strategy_backtest.py`
  (around line 333) does not pass `universe=...`. Operator was notified;
  fix may or may not have landed before this run.

## To do this Saturday

1. **First, verify the backtester is fixed:**

   ```
   python3 -m quant_trading_system.cli simulate equity_trend_following_ema_cross --symbol SPY
   python3 -m quant_trading_system.cli simulate equity_mean_reversion_bollinger --symbol SPY
   ```

   If both return `ok: true` with a sensible result, proceed. If either
   still raises the `universe` error, document in this Saturday's log
   and stop — the research path is still down.

2. **(Gated on #1.) Resume the deferred first-run calibration.** Per
   the original first-run task, pick 2 existing strategies that look
   thin or dated, build `<id>_v2` variants, and run
   `cli evaluate-update <existing> <id>_v2` on each. Candidates worth
   a first look (subjective — the battery decides):
   - `equity_vwap_reversion`: pure intraday mean-reversion is a known
     low-edge regime; check whether a volatility filter improves things.
   - `equity_rsi_divergence`: classic technical pattern with a lot of
     published parameter-sensitivity research; worth a parameter sweep.

3. **(Gated on #1.) OPERATOR REQUEST 2026-06-03: run head-to-head
   battery and propose claims for unclaimed + flagged candidates.**
   Specifically:
   - **Unclaimed in current universe:** META, MSFT. Run
     `cli head-to-head equity_trend_following_ema_cross <other>` on
     each — at minimum vs. `equity_mean_reversion_bollinger`,
     `equity_momentum_macd_histogram`, `equity_breakout_volume_confirmation`.
     Winner gets the claim via `cli add-active`.
   - **News-flagged candidates (5+ session recurrence):** MRVL, CSCO,
     HPE, DELL, MU, NTAP, OKTA, NOW, TEAM, SNOW, ARM, STM. These
     need to enter the universe first (add to `state/extra_symbols.md`)
     and then go through the same head-to-head battery to pick a claimant.
   - **Existing claims worth validating:** the 7 still-held names
     (AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY) were operator-assigned
     to trend-following at migration and were never validated by
     head-to-head per the original 2026-05-27 directive. If time
     permits, run h2h on at least one of them to validate the claim.
   - Document each winner/loser with Sharpe deltas in this Saturday's
     research log.

4. **Archive sweep.** `cli evaluate-archive` works regardless of the
   backtester. Run it on `equity_trend_following_ema_cross` (the only
   strategy with meaningful journal history). Almost certainly KEEP
   for at least a few more weeks given the small N, but worth a
   one-line check.

5. Write `knowledge_base/research_log/<today>.md` and replace this
   file with next Saturday's task list.

## Open questions for the operator

1. **One-line fix to `strategy_backtest.py`** is the critical-path item
   for the research agent. Detail in last Saturday's log
   (`research_log/2026-05-30.md`).

2. **Universe expansion candidates** (DELL, NTAP, OKTA, NOW, TEAM,
   MU, AVGO, SNOW) — if any are wanted in the M-F watchlist sooner
   than the research path can land them, drop into
   `state/extra_symbols.md`.
