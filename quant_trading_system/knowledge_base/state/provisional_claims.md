---
provisional:
- symbol: SPCX
  strategy_id: equity_trend_following_ema_cross
  gap_type: volatility_regime
  sharpe: null
  baseline_sharpe: 0.5
  provisional_since: '2026-06-16'
  revalidate_by: '2026-06-30'
  reason: "every candidate backtest errored / no price history \u2014 cannot rank"
---

PROVISIONAL (unvalidated) strategy attachments — Option 3 / mandatory-attach doctrine (2026-06-16). Each symbol here HAS a strategy attached in active_strategies.md for coverage, but is QUARANTINED FROM EXECUTION (run_active_strategies skips it) until Saturday research re-triages it: clearing baseline Sharpe promotes it to a normal validated claim (clear_provisional_claim); a passed `revalidate_by` deadline is escalated to the operator. NEVER trades while listed here.
