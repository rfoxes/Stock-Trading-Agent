---
strategies:
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
- id: equity_sector_rotation_momentum
  symbols:
  - DELL
  since: '2026-06-04'
  reason: 'Operator directive 2026-06-04: every universe symbol must be claimed. DELL
    is an AI-server cohort name; sector-rotation-momentum matches the rotational regime
    that''s been live (tech-to-financials Thu, AI-cohort rotation broadly). First-pass
    without head-to-head.'
- id: equity_momentum_macd_histogram
  symbols:
  - META
  - MSFT
  - SNDK
  since: '2026-06-26'
  reason: 'triage-symbol 2026-06-26: equity_momentum_macd_histogram beat 3 other candidate(s)
    on SNDK with Sharpe 2.254 (vs baseline 0.50)'
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
  - SPCX
  - SPY
  - TSLA
  - TSM
  since: '2026-07-07'
  reason: "PROVISIONAL/UNVALIDATED triage 2026-07-07: every candidate backtest errored\
    \ / no price history \u2014 cannot rank Attached best-available equity_trend_following_ema_cross\
    \ for coverage; QUARANTINED from execution until Saturday research validates (clears\
    \ baseline 0.50) or escalates."
- id: equity_pairs_trading_cointegration
  symbols:
  - IRDM
  - SYNA
  since: '2026-07-08'
  reason: "PROVISIONAL/UNVALIDATED triage 2026-07-08: top candidate 'equity_pairs_trading_cointegration'\
    \ has Sharpe 0.000 < baseline 0.500. No library strategy is good enough on this\
    \ symbol \u2014 log for Saturday research to build a new template. Attached best-available\
    \ equity_pairs_trading_cointegration for coverage; QUARANTINED from execution\
    \ until Saturday research validates (clears baseline 0.50) or escalates."
- id: equity_event_driven_catalyst
  symbols:
  - AVGO
  - BE
  - MU
  - ORCL
  - QCOM
  - RKLB
  - SMCI
  since: '2026-07-08'
  reason: "PROVISIONAL/UNVALIDATED triage 2026-07-08: top candidate 'equity_event_driven_catalyst'\
    \ has Sharpe 0.000 < baseline 0.500. No library strategy is good enough on this\
    \ symbol \u2014 log for Saturday research to build a new template. Attached best-available\
    \ equity_event_driven_catalyst for coverage; QUARANTINED from execution until\
    \ Saturday research validates (clears baseline 0.50) or escalates."
---

Active strategy set. Each entry owns its declared symbols exclusively. Conflicts are resolved by head-to-head backtest at the research layer, never at runtime.
