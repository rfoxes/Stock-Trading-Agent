---
provisional:
- symbol: QCOM
  strategy_id: equity_event_driven_catalyst
  gap_type: event_catalyst
  sharpe: 0.0
  baseline_sharpe: 0.5
  provisional_since: '2026-07-07'
  revalidate_by: '2026-07-21'
  reason: "top candidate 'equity_event_driven_catalyst' has Sharpe 0.000 < baseline\
    \ 0.500. No library strategy is good enough on this symbol \u2014 log for Saturday\
    \ research to build a new template."
- symbol: RIVN
  strategy_id: equity_event_driven_catalyst
  gap_type: event_catalyst
  sharpe: 0.0
  baseline_sharpe: 0.5
  provisional_since: '2026-07-13'
  revalidate_by: '2026-07-27'
  reason: "top candidate 'equity_event_driven_catalyst' has Sharpe 0.000 < baseline\
    \ 0.500. No library strategy is good enough on this symbol \u2014 log for Saturday\
    \ research to build a new template."
- symbol: SKHY
  strategy_id: equity_watch_only
  gap_type: event_catalyst
  sharpe: null
  baseline_sharpe: 0.5
  provisional_since: '2026-07-10'
  revalidate_by: '2026-07-24'
  reason: "every candidate backtest errored / no price history \u2014 cannot rank"
- symbol: SPCX
  strategy_id: equity_trend_following_ema_cross
  gap_type: volatility_regime
  sharpe: null
  baseline_sharpe: 0.5
  provisional_since: '2026-07-07'
  revalidate_by: '2026-07-21'
  reason: "every candidate backtest errored / no price history \u2014 cannot rank"
- symbol: SYNA
  strategy_id: equity_pairs_trading_cointegration
  gap_type: pairs_arbitrage
  sharpe: 0.0
  baseline_sharpe: 0.5
  provisional_since: '2026-07-07'
  revalidate_by: '2026-07-21'
  reason: "top candidate 'equity_pairs_trading_cointegration' has Sharpe 0.000 < baseline\
    \ 0.500. No library strategy is good enough on this symbol \u2014 log for Saturday\
    \ research to build a new template."
---

PROVISIONAL (unvalidated) strategy attachments — Option 3 / mandatory-attach doctrine (2026-06-16). Each symbol here HAS a strategy attached in active_strategies.md for coverage, but is QUARANTINED FROM EXECUTION (run_active_strategies skips it) until Saturday research re-triages it: clearing baseline Sharpe promotes it to a normal validated claim (clear_provisional_claim); a passed `revalidate_by` deadline is escalated to the operator. NEVER trades while listed here.
