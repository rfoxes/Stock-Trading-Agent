# Handoff to tomorrow's Claude

## State

- **Date written:** 2026-05-13 (post-close run; fifth scheduled tick of the
  harness; first day with the broker actually reachable).
- **Active strategy:** still **none**. `state/active_strategy.md` is unchanged
  from its seed unset state. I did not call `set-active` — `regime` still
  returns `unknown` because the Alpaca subscription does not permit recent
  SIP bars, so a strategy pick today would be a guess.
- **Broker positions (unexpected, manual override — DO NOT close without
  operator confirmation):** 10 long positions totalling ~$208,455 market
  value, ~+$11,925 unrealized P&L: AAPL 72@271.30 (now 298.63, +10.1%),
  AMZN 76@248.53 (270.40, +8.8%), GOOGL 56@338.79 (403.48, +19.1%),
  JPM 64@313.04 (301.00, -3.8%), META 28@681.55 (616.10, -9.6%),
  MSFT 44@421.24 (404.65, -3.9%), NVDA 96@199.40 (227.39, +14.0%),
  QQQ 28@647.96 (718.25, +10.8%), SPY 35@708.81 (743.64, +4.9%),
  TSLA 48@403.98 (448.36, +11.0%). **The journal has zero events** so
  these are not attributable to any harness-side strategy.
- **Open orders:** none.
- **Account snapshot:** equity $111,924.00, cash -$96,531.22 (margin),
  buying power $15,392.78, day_trade_count 0.
- **Queued for tomorrow's session:** nothing. No `submit` calls were made
  today, same as days 1–4.
- **Strategy library on disk:** 18 active (10 equity, 8 options), 0 archived.
  Unchanged from days 1–4.
- **Outage status:** network back as of today. The 4-day proxy outage
  appears resolved. New blocker is the data subscription, not the network.
- **Operator alert:** I replaced `ATTENTION.md` with a fresh notice that
  describes both new anomalies (unexplained portfolio + bars-feed
  subscription) and the minimal fixes for each.

## Recommendations for tomorrow's Claude

1. **First, check whether the operator has acted on `ATTENTION.md`.**
   `cat ATTENTION.md` and `python3 -m quant_trading_system.cli positions`.
   If the 10 positions are still there *and* there's no operator note
   anywhere (look in the repo root and in `knowledge_base/state/` for any
   new files), treat them the same way I did today: don't close them,
   don't tag them, document and stop. The risk profile of flattening
   someone's intentional book is much worse than letting it sit one
   more day.

2. **Check whether the bars feed is fixed.** Run
   `python3 -m quant_trading_system.cli regime`. If it now returns a
   real classification (not `unknown` with `confidence=0.0`), the data
   subscription was either upgraded or the source was patched to use
   IEX. From that point you can run the *real* day-1 workflow: read
   2–3 strategies whose `market_regime` matches, optionally backtest
   one with `backtest <strategy_id> SPY 2023-01-01 2025-01-01`, and
   call `set-active` with a real reason. Be conservative on the first
   real run — small size, clear stop and target in `--reasoning`, or
   trade nothing if no setup actually fires.

3. **If the operator has assigned the existing positions to a strategy,**
   you'll see a note in `ATTENTION.md` or in a new file under
   `state/`. That note should give you a `strategy_id` to attribute
   them under. In that case you can call `set-active <id>` *and* you
   are now responsible for managing those positions — meaning you
   need to defend a stop and target for each one in tomorrow's
   conclusion (or in a follow-up that documents the per-symbol
   exit plan). Do *not* invent stop/target levels without checking
   the strategy's rules.

4. **If the operator has flat-closed the positions,** the journal
   should now contain real entries (Alpaca's order history will be
   the source of truth). Run `recent-trades` and `portfolio-health
   --days 30` to confirm, then proceed as a real day 1 (cold pick of
   active strategy, conservative entries only if a setup fires).

5. **The `health` / `portfolio-health` id mismatch for equity
   strategies is real.** `list-strategies` reports
   `equity_breakout_volume_confirmation` etc.; `health <id>` and
   `portfolio-health` return `strategy_not_found` for those exact
   ids. Options ids (no prefix) work fine. If you're picking an
   equity strategy and want its health snapshot, this will currently
   not work — that's a code bug, not a transient issue. Flag in
   tomorrow's conclusion if it bites you; don't fix it inline.

6. **Don't re-derive the full audit if everything is still stuck.**
   If `ATTENTION.md` is unchanged and `regime` still returns
   `unknown`, the minimum useful probe is: `account` (broker live?),
   `positions` (any change?), `regime` (feed unblocked?),
   `ls knowledge_base/journal/` (any new attribution?). If all four
   say "same as yesterday," that's your conclusion — keep it short,
   point at this handoff, stop.

7. **One small market-data note for context.** After-hours `quote SPY`
   today returned `bid=742.16, ask=0.0`. The zero ask is probably a
   feed/hours interaction (the bid worked), but if you see the same
   thing intraday tomorrow it's a real issue — the harness uses mid
   for some sizing, and `mid` will collapse to 0 if `ask` is 0.
