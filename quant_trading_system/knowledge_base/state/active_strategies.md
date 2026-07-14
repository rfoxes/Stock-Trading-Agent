---
strategies:
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
  - SYNA
  since: '2026-07-08'
  reason: 'research 2026-07-08: released IRDM to validated breakout claim (triage
    winner breakout_volume_confirmation Sharpe 0.832 on 9 trades >= baseline); pairs
    retains SYNA provisional (held, thin 4-trade sample)'
- id: equity_mean_reversion_bollinger
  symbols:
  - CSCO
  - SMCI
  since: '2026-07-08'
  reason: 'triage-symbol 2026-07-08: equity_mean_reversion_bollinger beat 10 other
    candidate(s) on SMCI with Sharpe 0.814 (vs baseline 0.50)'
- id: equity_breakout_volume_confirmation
  symbols:
  - ARM
  - BE
  - INTC
  - IRDM
  - MRVL
  - RKLB
  since: '2026-07-08'
  reason: 'triage-symbol 2026-07-08: equity_breakout_volume_confirmation beat 10 other
    candidate(s) on IRDM with Sharpe 0.832 (vs baseline 0.50)'
- id: equity_watch_only
  symbols:
  - SKHY
  since: '2026-07-10'
  reason: "PROVISIONAL/UNVALIDATED triage 2026-07-10: every candidate backtest errored\
    \ / no price history \u2014 cannot rank Attached best-available equity_watch_only\
    \ for coverage; QUARANTINED from execution until Saturday research validates (clears\
    \ baseline 0.50) or escalates."
- id: equity_rsi_divergence
  symbols:
  - HPE
  - WULF
  since: '2026-07-11'
  reason: 'triage-symbol 2026-07-11: equity_rsi_divergence beat 10 other candidate(s)
    on WULF with Sharpe 0.880 (vs baseline 0.50)'
- id: equity_event_driven_catalyst
  symbols:
  - AVGO
  - GS
  - MU
  - ORCL
  - QCOM
  - RIVN
  since: '2026-07-14'
  reason: "PROVISIONAL/UNVALIDATED triage 2026-07-14: top candidate 'equity_event_driven_catalyst'\
    \ has Sharpe 0.000 < baseline 0.500. No library strategy is good enough on this\
    \ symbol \u2014 log for Saturday research to build a new template. Attached best-available\
    \ equity_event_driven_catalyst for coverage; QUARANTINED from execution until\
    \ Saturday research validates (clears baseline 0.50) or escalates."
---

Active strategy set. Each entry owns its declared symbols exclusively. Conflicts are resolved by head-to-head backtest at the research layer, never at runtime.
