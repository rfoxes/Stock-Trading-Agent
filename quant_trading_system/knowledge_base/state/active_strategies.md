---
strategies:
- id: equity_trend_following_ema_cross
  symbols:
  - AAPL
  - AMZN
  - GOOGL
  - JPM
  - NVDA
  - QQQ
  - SPY
  - TSLA
  since: '2026-06-02'
  reason: "Migrated 2026-06-02 from legacy state/active_strategy.md. Strategy owns\
    \ the 8 inherited long positions. Operator-assigned attribution per 2026-05-27\
    \ directive; not yet validated by head-to-head \u2014 research agent should run\
    \ battery to confirm trend-following is optimal for each of these symbols."
---

Active strategy set. Each entry owns its declared symbols exclusively. Conflicts are resolved by head-to-head backtest at the research layer, never at runtime.
