---
id: equity_event_driven_catalyst
name: Event-Driven Catalyst
type: equity
timeframe:
  - swing
indicators:
  - atr
  - news_signal
market_regime:
  - all_regimes
gap_types:
  - event_catalyst
  - earnings_window
parameters:
  risk_pct_per_trade: 0.01
  stop_atr_multiplier: 2.0
  atr_period: 14
  max_hold_days: 7
  min_negative_unreal_pct_for_news_exit: 0.0
status: active
---

# Event-Driven Catalyst

## Description

This strategy reads today's news brief (`state/news_brief.md`) and acts only
on concrete catalysts the news agent has surfaced — earnings beats with
raised guidance, regulatory approvals, confirmed M&A, lawsuit settlements,
buyback announcements, partnership deals with material revenue impact. It
does NOT trade on price action alone — every entry is justified by an event
in the brief.

It is also the ONLY strategy in the library that uses negative news as an
exit signal: held positions whose news brief entry contains negative
catalyst markers (guidance cut, downgrade, lawsuit, regulatory action) are
exited the next session regardless of technical state.

## Entry Rules

For each symbol in the strategy's universe that the news brief flags with
positive markers:
- Beat / raised guidance / upgrade / approval / acquisition target / buyback /
  partnership / record revenue.

AND we don't already hold the symbol AND we have buying power for at least a
1% risk position:
- Place a market buy.
- Stop = entry − 2 × ATR(14).
- Risk per trade = 1% of equity, sized via the standard share-count helper.

If the news brief headline assessment is HALT-WORTHY EVENT, skip entries.
NORMAL FLOW and NOTABLE both allow entries; NO MATERIAL NEWS allows entries
only if there are positive single-name catalysts (in practice rare).

## Exit Rules

- **Negative news exit:** if the news brief contains negative markers
  (guidance cut, downgrade, lawsuit, regulatory action, recall, warning,
  fraud, restate, going concern, bankruptcy) for a held symbol, exit at
  next session's open. Catalyst-driven exits take precedence over all other
  signals.
- **Hard stop:** exit if price ≤ entry × (1 − 2×ATR/entry) — the stop set
  at entry.
- **Time stop:** exit after 7 calendar days regardless of P&L. The catalyst
  edge decays fast; do not turn this into a long-term hold.
- **Take profit:** none explicit — let the strategy ride to the time stop
  unless the news flips negative.

## Risk Management

- 1% of equity risked per trade.
- Capped by `MAX_POSITION_SIZE_PCT` (default 10%).
- Maximum 3 concurrent positions opened by this strategy at any time.
- Skip entries on HALT-WORTHY EVENT days.
- Skip entries on symbols whose news brief contains negative markers
  (don't long a catalyst that's already turned negative).
