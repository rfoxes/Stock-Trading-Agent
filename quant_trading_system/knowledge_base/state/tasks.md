# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

---

## STANDING POLICY (P0, do not ignore)

**Every symbol in the universe MUST be claimed by an active strategy.**
See `manual.md` "P0 — ZERO-UNCLAIMED RULE" at the top. `cli execute`
REFUSES to run if any symbol is unclaimed. If you hit unclaimed symbols
(operator extras, news promotes, new positions), claim them via
`cli add-active` using the character-match heuristic in `manual.md`
BEFORE attempting execute.

---

## Status as of last update (Mon 2026-06-08, post-close)

- **Active set unchanged: 7 strategies, 17/17 universe symbols claimed.**
  Verify with `cli list-active`. unclaimed_count == 0 at end of session.
- **Today's execute: 2 intents submitted, both queued for Tue open as
  market orders.**
  - NVDA sell 96 from `equity_trend_following_ema_cross` (ADX(14)=19.0 < 20
    exit). Order id `cc089442-a517-4710-8c26-7bd924de386f`. Est. P&L at
    mark +$802 (profit exit).
  - MU buy 7 from `equity_event_driven_catalyst` (catalyst entry on Sun
    brief's positive Micron Vera Rubin HBM4 certification flag). Order id
    `53cd8553-1f0a-49fa-b3d1-6a09ee6a42f0`. Stop @ $813.44, risk ~1% eq.
- **Reconciled Fri's queued sells:** AMZN sell 76 @ $247.16 → -0.000984.
  META sell 17 @ $584.00 → -0.007192. Both `log-closed` ✓.
- **Account: equity $106,202.11 (flat vs Fri close $106,275.64).**
- **Regime: bull, conf 0.77, ADX 27.41.** Marginal cool-down from Fri
  (0.81/30.98). Still firmly bull; ADX now ~7 points above EMA-cross
  exit threshold (20.0).
- **No code, manual, or strategy changes today.**

## To do Tuesday (2026-06-09)

1. **Read last_handoff.md and news_brief.md FIRST.** Tue is CPI eve
   (CPI Wed 6/10 8:30 ET). WWDC Day 2. Watch for macro-event posture
   discussion in brief — trader has no rule, but document expectations.

2. **Standard read-and-snapshot.** Run `cli list-active`. Confirm
   `unclaimed_count == 0`.

3. **If unclaimed_count > 0**, claim via `cli add-active` (character-match
   from `manual.md` heuristic table). Do NOT defer to research agent.

4. **Reconciliation.** Yesterday's NVDA sell 96 and MU buy 7 were queued
   Mon post-close. Both will fill at Tue open:
   - **NVDA sell 96** (was 96 long at $199.397 avg, sold near ~$207-208
     mark). Use actual fill from Alpaca. First-pass estimate:
     realized ≈ ($207.50 - $199.397) × 96 ≈ +$778 ≈ +0.00732 of equity.
     `cli log-closed equity_trend_following_ema_cross NVDA <pnl_fraction>`.
   - **MU buy 7** opens a new position at ~$938. No reconciliation —
     this is an opening, not a close. Will show in `cli positions`.

5. **Run `cli execute`.** Watch for:
   - **MU follow-on activity.** New long; strategy may add stops/exits
     in subsequent runs.
   - **Other names.** ADX continues to cool — if it drops below 20
     across more of the trend-following claims (AAPL/GOOGL/JPM/QQQ/SPY),
     EMA-cross may fire more exits. That's the rule firing — let it.
   - **AAPL WWDC Day 2.** Still no event-window rule. Price-driven only.
   - **HPE RSI:** still elevated per Sun brief; divergence has not
     formed yet.

6. **HALT-WORTHY check:** unchanged criteria.

7. **CPI prep — Wed 6/10 8:30 ET.** No macro-event-window rule active.
   Trader will NOT preemptively reduce. The library gap is logged; the
   research agent owns building the overlay.

8. **Library gaps — see list below.** One new soft-flag from today
   (NVDA exit on anchor-positive supply-chain news re-confirms the
   Tier-1-supply-chain overlay gap).

9. **Run `cli git-sync --agent trader --message "..."` as last action.**
   Then `cli git-doctor` once if any lock-file warnings appeared.

## Library gaps for the research agent (carry to research_tasks.md Sat)

These are EVENT-OVERLAY gaps, NOT unclaimed-symbol gaps. Every universe
symbol is claimed.

- **Validate the 6 first-pass strategy assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT *(META 1-day round-trip realized -$764 vs estimated -$659 is fresh data point #2 — research agent has 2 META round-trips' worth of evidence now)*
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU *(today's MU buy is fresh data on the event-driven side)*
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
- **Tier-1 supply-chain partnership overlay — RE-CONFIRMED today.** NVDA exited on ADX-cool despite Sun NVDA-SK Hynix anchor-positive Tier-1 supply-chain news. Suggested rule: when a held name announces multiyear partnership with a named upstream/downstream counterparty in a Tier-1 cohort, defer trend-exit signals through a 5-day repricing window OR scale long posture up 10-20%.
- **AAPL WWDC June 8-12 event-window posture rule.** **ACTIVE THROUGH FRI.**
- **NFP / CPI / FOMC macro-event-window rule.** **CPI Wed 6/10 8:30 ET.**
- **Tier-1 customer-win event overlay** (Apple-Gemini → GOOGL +4pp Thu; Siri 2.0 Gemini → AAPL/GOOGL Mon).
- **Peer-earnings cohort-spillover overlay** (AVGO → NVDA/MU/MRVL).
- **Geopolitical / oil-spike risk-off overlay.** **Iran-Hormuz Day-3 active.**
- **Rate-policy-shift sizing rule** (10Y yield breakout).
- **Credit-stress sector overlay** (Cliffwater + Blackstone gates → JPM).
- **Capital-allocation / dilution-gap overlay** (GOOGL $84B raise Day-6).
- **TSMC capacity-constraint supply-side pricing-power overlay.**
- **Trump AI EO policy-tailwind sizing rule.**
- **EU cloud procurement regulatory-headwind rule.**
- **Corporate-action handler** (CRWD 4-for-1 split style).
- **Underwriter-franchise-event overlay** (SpaceX IPO Thu/Fri → JPM franchise marker).
- **Vol-regime overlay** (VIX >20 sustained → size down trend strategies).
- **Pre-print cohort-cert overlay** (held/candidate receives major-customer qualification confirmation pre-own-print).

## Open questions for the operator

1. **`cli open-orders`** — bug still present; today worked at snapshot
   time when no orders pending, but untested when 2 orders are live.

2. **META MACD round-trip realized -$764 vs estimate -$659.** Single
   round-trip data point, but actual fill came worse than Sun-quoted
   mark suggested. Sat research agent has two data points to consider
   (one round-trip, one realized vs estimate slippage).

3. **MU buy stop @ $813.44 (-14.3% range) on $938 underlying.** Wide
   stop driven by ATR=67.77. Defensible for print-volatility name, but
   the position will be tested into the June 24 print. Watch.

4. **AAPL WWDC June 8-12 ongoing.** No event-window rule.

5. **CPI Wed 6/10, ORCL Wed AMC, ADBE/PPI/SpaceX-IPO-pricing Thu,
   SpaceX listing Fri.** Catalyst-stacked rest of week. No macro-event
   rule active.
