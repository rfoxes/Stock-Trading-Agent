---
id: equity_watch_only
name: Watch Only (passive coverage)
type: equity
role: watch
timeframe:
  - swing
indicators: []
market_regime:
  - all_regimes
gap_types: []
parameters: {}
status: active
---

# Watch Only

## Description

The library's passive fallback strategy. It provides **coverage without
trading**: `evaluate()` always returns an empty list, so it never submits an
order.

Its purpose is the operator's mandatory-attach doctrine (2026-06-16, extended
2026-07-08): every symbol in the composed universe must have a strategy
attached, but that attachment does **not** have to trade. When the news layer
brings a new symbol into the universe and no library strategy has a *validated*
edge on it (no price history to backtest, or nothing clears baseline Sharpe),
triage attaches **watch_only** — an honest "we are watching this, not trading
it" state.

Watching is a legitimate resting state, not a failure. The symbol stays under
full news coverage. Saturday research periodically re-triages watched names and
upgrades any that develop a backtestable edge to a real trading strategy via
`triage-symbol` / `head-to-head`; until then, the name is simply monitored.

This strategy is excluded from being scored as a triage *candidate* (via
`role: watch`) — it is the fallback, never a competitor to real strategies.

## Entry Rules

None. This strategy never enters.

## Exit Rules

None. This strategy never exits. It should therefore only ever be attached to
symbols with **no open position** — a held position must be owned by a trading
strategy that actually manages its exits.

## Risk Management

Zero market exposure by construction: it places no orders, so there is nothing
to size, stop, or cap.
