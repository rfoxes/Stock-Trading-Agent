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

## Status as of last update (Fri 2026-06-05, post-close)

- **Active set unchanged: 7 strategies, 17/17 universe symbols claimed.**
  Verify with `cli list-active`. unclaimed_count == 0 at end of session.
- **Today's execute: 2 sell intents submitted, both queued for Mon open
  as market orders.**
  - AMZN sell 76 from `equity_trend_following_ema_cross`. Order id
    `6cb29b3b-6559-43dc-83cb-78750b66136d`.
  - META sell 17 from `equity_momentum_macd_histogram`. Order id
    `8dbf29a7-3623-4fe3-8343-e20f530c2dae`.
- **Account: equity $106,275.64 (-4.0% vs Thu close $110,697.80).**
  Drawdown is mark-to-market on existing positions + META -6.16%.
- **Regime: bull, conf 0.81, ADX 30.98. Unchanged.**
- **No code, manual, or strategy changes today.**

## To do Monday (2026-06-08)

1. **Read last_handoff.md and news_brief.md FIRST.** Monday is **WWDC
   Day 1 (Jun 8-12 for AAPL)**. No event-window rule in the active set —
   trader will not adjust posture. Document expectations from the brief.

2. **Standard read-and-snapshot.** Run `cli list-active`. Confirm
   `unclaimed_count == 0`.

3. **If unclaimed_count > 0**, claim via `cli add-active` (character-match
   from `manual.md` heuristic table). Do NOT defer to research agent.

4. **Reconciliation — important Monday morning.** Yesterday's AMZN sell
   76 and META sell 17 were queued Friday post-close. They will fill at
   Monday open (both market orders). After execute, you should see:
   - AMZN position closed (was 76 long at $248.535 avg, sold ~$246.60 open
     → ~-$147 realized loss). `cli log-closed equity_trend_following_ema_cross AMZN <pnl_fraction>`
   - META position closed (was 17 long at $628.93 avg, sold ~$590.16 open
     → ~-$659 realized loss). `cli log-closed equity_momentum_macd_histogram META <pnl_fraction>`
   - pnl_fraction = realized_pnl / equity-when-position-opened. Use
     ~-0.0014 (AMZN) and ~-0.0060 (META) as first-pass estimates; pull
     actual fill prices from the broker first.

5. **Run `cli execute`.** Watch for:
   - **META reentry risk.** Strategy could fire a new BUY if MACD ticks
     back up. That's the rule firing — let it.
   - **AAPL WWDC Day 1.** No event-window rule in the active set.
     `equity_trend_following_ema_cross` is the responder; price-driven
     only.
   - **HPE RSI 87.56 carries forward.** `equity_rsi_divergence` may fire
     if Friday's price action created the divergence pattern.

6. **HALT-WORTHY check:** unchanged criteria.

7. **Library gaps — see list below.** Carry-forward from Thu — no new
   gaps added today (no new uncovered events fired).

8. **Run `cli git-sync --agent trader --message "..."` as last action.**
   Then `cli git-doctor` once.

## Library gaps for the research agent (carry to research_tasks.md Sat)

These are EVENT-OVERLAY gaps, NOT unclaimed-symbol gaps. Every universe
symbol is claimed.

- **Validate the 6 new first-pass strategy assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT *(Friday's META round-trip is fresh evidence for the META leg — see Saturday research note below)*
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
- **`equity_momentum_macd_histogram` 1-day-round-trip pattern — fresh
  Saturday question.** Thu it entered META on a histogram cross-up; Fri
  it exited on the inverse. Net result: -6.16% on a 1-session hold. ONE
  data point — DO NOT change the strategy on its basis. But the research
  agent should examine the strategy's historical entry/exit pacing on
  large-cap names: is the MACD histogram crossover too sensitive on
  daily bars for this cohort? Possible fix: require 2-session
  confirmation, or minimum hold period, or signal-strength threshold.
  Test via backtest.
- **Tier-1 customer-win event overlay** (Apple-Gemini → GOOGL +4pp Thu;
  Siri 2.0 Blackwell → NVDA/AAPL).
- **AAPL WWDC June 8-12 event-window posture rule.** **PROXIMATE — starts
  Mon.**
- **NFP / CPI / FOMC macro-event-window rule.**
- **Peer-earnings cohort-spillover overlay** (AVGO → NVDA/MU/MRVL).
- **Geopolitical / oil-spike risk-off overlay.**
- **Rate-policy-shift sizing rule** (10Y yield breakout).
- **Credit-stress sector overlay** (Cliffwater + Blackstone gates → JPM).
- **Capital-allocation / dilution-gap overlay** (GOOGL $84B raise).
- **TSMC capacity-constraint supply-side pricing-power overlay.**
- **Trump AI EO policy-tailwind sizing rule.**
- **EU cloud procurement regulatory-headwind rule.**
- **Corporate-action handler** (CRWD 4-for-1 split style).

## Open questions for the operator

1. **`cli open-orders` still broken with real orders.** Returns
   `'dict' object has no attribute 'id'`. Empty-list path works. Fix in
   `agent_tools.get_open_orders` parsing. Workaround in this session was
   direct Alpaca REST.

2. **No 2026-06-05 news brief on disk.** Daily news agent may not have
   run today. Operator may want to verify the news-agent schedule.

3. **META MACD round-trip** — see library gap above. Single data point.

4. **AAPL WWDC June 8-12 starts Monday.** No event-window rule.

5. **First-pass strategy assignments still un-validated** — Saturday
   research agent's queue is full; META leg now has fresh evidence.
