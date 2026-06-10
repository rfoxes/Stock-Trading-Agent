---
strategies:
- id: equity_momentum_macd_histogram
  symbols:
  - META
  - MSFT
  since: '2026-06-04'
  reason: 'Operator directive 2026-06-04: every universe symbol must be claimed. Large-cap
    momentum tech names match MACD-histogram strategy character (trending/momentum
    regime). First-pass assignment without head-to-head per operator override; research
    agent should validate.'
- id: equity_breakout_volume_confirmation
  symbols:
  - ARM
  - INTC
  - MRVL
  since: '2026-06-04'
  reason: "Operator directive 2026-06-04: every universe symbol must be claimed. Volatile\
    \ chip names \u2014 breakout-confirmation suits MRVL (recent Jensen-anointment\
    \ momentum) and ARM (growth chip). First-pass assignment without head-to-head\
    \ per operator override; research agent should validate. INTC added 2026-06-09\
    \ per P0 zero-unclaimed rule (volatile chip with Google-foundry news catalyst)."
- id: equity_mean_reversion_bollinger
  symbols:
  - CSCO
  since: '2026-06-04'
  reason: "Operator directive 2026-06-04: every universe symbol must be claimed. CSCO\
    \ is a lower-vol large-cap with 11 PT raises in a week (extended) \u2014 Bollinger\
    \ mean reversion is a defensible first-pass match. Research agent should validate\
    \ via head-to-head."
- id: equity_rsi_divergence
  symbols:
  - HPE
  since: '2026-06-04'
  reason: "Operator directive 2026-06-04: every universe symbol must be claimed. HPE\
    \ RSI 87.56 per Thu news brief (historic AI-server rally, overbought) \u2014 RSI\
    \ divergence is the textbook setup for trend-exhaustion at extreme RSI. Research\
    \ agent should validate via head-to-head."
- id: equity_event_driven_catalyst
  symbols:
  - AVGO
  - MU
  - ORCL
  since: '2026-06-04'
  reason: "Operator directive 2026-06-04: every universe symbol must be claimed. AVGO\
    \ just printed Q2 (Wed AMC, -12.59% Day-1) and MU prints Q3 ~June 24. Event-driven\
    \ catalyst is the on-character match for earnings-window names. First-pass without\
    \ head-to-head per operator override. ORCL added 2026-06-09 per P0 zero-unclaimed\
    \ rule \u2014 Wed AMC Q4 FY26 print is exactly the strategy's on-character event."
- id: equity_sector_rotation_momentum
  symbols:
  - DELL
  since: '2026-06-04'
  reason: 'Operator directive 2026-06-04: every universe symbol must be claimed. DELL
    is an AI-server cohort name; sector-rotation-momentum matches the rotational regime
    that''s been live (tech-to-financials Thu, AI-cohort rotation broadly). First-pass
    without head-to-head.'
- id: equity_trend_following_ema_cross
  symbols:
  - AAPL
  - AMZN
  - CBRS
  - GOOGL
  - JPM
  - NUVL
  - NVDA
  - QQQ
  - SPY
  - TSLA
  - TSM
  since: '2026-06-10'
  reason: "Migrated 2026-06-02 from legacy state/active_strategy.md. Strategy owns\
    \ the inherited long positions. Operator-assigned attribution per 2026-05-27 directive;\
    \ not yet validated by head-to-head \u2014 research agent should run head-to-head\
    \ battery to confirm trend-following is optimal for each of these symbols. TSM/CBRS/NUVL\
    \ added 2026-06-09 per P0 zero-unclaimed rule (safe-default heuristic predating\
    \ triage; research agent owns proper claim, especially NUVL biotech M&A target\
    \ \u2014 library gap)."
---

Active strategy set. Each entry owns its declared symbols exclusively. Conflicts are resolved by head-to-head backtest at the research layer, never at runtime.
