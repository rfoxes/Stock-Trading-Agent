# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

---

## STANDING POLICY (P0, do not ignore)

**Every symbol in the universe MUST be either (a) claimed by an active
strategy via algorithmic triage, or (b) flagged as a true library gap.**
See `manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE" (the
top of `manual.md`, refined 2026-06-10). `cli execute` REFUSES to run
if any symbol is unclaimed AND not in `state/library_gaps.md`.

**Use `cli triage-symbol <SYM> [--gap-type X]`** for every unclaimed
universe symbol — it auto-claims if Sharpe ≥ 0.5 on a library
candidate, else auto-records to `state/library_gaps.md`. Character-match
shortcuts and direct YAML edits to `active_strategies.md` are NOW
FORBIDDEN (operator directive 2026-06-10). The old "cli add-active is
buggy" footgun is also fixed — it UNIONs by default now; pass
`--replace` for the old overwrite behaviour.

---

## Status as of last update (Wed 2026-06-10, post-close)

- **Active set: 7 strategies, 22/22 universe symbols claimed (unclaimed_count == 0).**
  No claim changes today; Tue's work still standing. Verify with `cli list-active`.
- **Today's execute: 0 intents.** All 7 strategies returned empty. No submissions, no rejections, no errors.
- **Reconciled Tue's queued exits (both filled Wed open):**
  - GOOGL sell 56 ≈ $362.92 fill → realized +0.01286 of equity (P&L +$1,352).
  - JPM sell 64 ≈ $311.78 fill → realized -0.00076 of equity (P&L -$80).
  - Logged via `cli log-closed equity_trend_following_ema_cross GOOGL 0.01286` and `... JPM -0.00076`.
- **Account: equity $104,506.85 (-0.59% vs Tue $105,122.24); cash $32,063.73 (positive, net-cash posture).**
- **Positions: 4 longs — AAPL 72 (+7.73%), MU 7 (-8.44%), QQQ 28 (+7.72%), SPY 35 (+3.01%).**
- **Regime: bull, conf 0.77, ADX 27.41.** Unchanged from Mon/Tue.
- **NEWS BRIEF GAP: today's `news_brief.md` was not written by the news agent — file header still reads 2026-06-09.** Proceeded without news context per manual §1. Operator awareness needed.

## To do Thursday (2026-06-11)

1. **Read last_handoff.md and news_brief.md FIRST.** Thu has a heavy catalyst stack:
   - PPI May + initial jobless claims 8:30 ET (consensus PPI +0.3% MoM; claims ~220K).
   - ADBE Q2 prints AMC.
   - SpaceX IPO pricing AMC ($135 × 555.6M target, $1.75T valuation).
   - **ORCL prints Wed AMC (tonight); Thu's tape will react.**
   - If the news brief is again missing/stale, note it again and proceed.

2. **Standard read-and-snapshot.** Run `cli list-active`. Note `unclaimed_count`.
   If `unclaimed_count > 0` (Thu news promotion — likely SPCX post-listing? but SPCX lists Fri, not Thu, so probably 0), for each unclaimed symbol run:
   ```
   cli triage-symbol <SYM> [--gap-type <type from news brief>]
   ```
   This auto-claims (Sharpe ≥ 0.5 on a library candidate) OR auto-flags as `true_library_gap` in `state/library_gaps.md`. Either outcome lets `cli execute` proceed. **Do NOT use direct YAML edits or `cli add-active` for unclaimed symbols** — triage is the only sanctioned path. (`cli add-active` itself is now safe: UNIONs by default. But triage is what the doctrine requires for claim decisions.)

3. **Reconciliation.** No orders queued Wed overnight. No fill expected Thu open from yesterday's `execute`. Quick `cli positions` diff vs handoff:
   - Confirm 4 longs unchanged (AAPL 72, MU 7, QQQ 28, SPY 35) — no surprise overnight fills.
   - If anything changed (Alpaca margin call, surprise close, etc.), reconcile before execute.

4. **Run `cli execute`.** Watch for:
   - **ORCL post-print reaction.** `equity_event_driven_catalyst` claims ORCL. The strategy's print-response rule may fire on Thu tape depending on print outcome. If ORCL gaps materially, the strategy could attempt entry.
   - **MU stop watch.** -8.44% unrealized Wed; $813.44 stop is ~9.6% away (current $899.92). If chip cohort weakens further Thu, stop could come into play. The event-driven strategy holds through 6/24 print barring stop trigger.
   - **AAPL WWDC Day-4.** Penultimate WWDC reaction day. Trend-following claims AAPL; price-driven rules will fire if signal forms.
   - **ADBE post-print Thu AMC.** ADBE not in universe; not actionable for the trader.
   - **PPI reaction.** Same as CPI Wed — no macro-event-window rule; strategies react to price.
   - **SpaceX IPO pricing AMC.** Listing Fri. No SPCX in universe yet (won't be tradable until Fri at earliest). JPM franchise-event tailwind continues but JPM was exited Wed — no position to defend.

5. **HALT-WORTHY check.** Multiple catalysts. If brief flags HALT-WORTHY (e.g., PPI prints >2σ off consensus + ORCL gaps -10%+), use discretion to skip `cli execute`. Standard threshold: only skip if brief explicitly says HALT-WORTHY EVENT.

6. **Library gaps — see list below.** No new gap categories Wed (no intents fired = no new exit-on-positive-news data points).

7. **Run `cli git-sync --agent trader --message "..."` as last action.** Then `cli git-doctor` once if any lock-file warnings appeared.

## Library gaps for the research agent (carry to research_tasks.md Sat)

These are EVENT-OVERLAY gaps + the 5 still-unvalidated first-pass assignments. Every universe symbol is claimed; head-to-head validation remains the Sat research priority.

- **Validate the now-5-strategy first-pass assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL *(ORCL Wed AMC print is fresh data)*
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` vs ??? on CBRS, NUVL, TSM *(safe-default placeholders, especially NUVL biotech)*
- **Tier-1 supply-chain / customer-win partnership overlay — re-confirmed Tue (Day-3).** NVDA/GOOGL exits on event-positive days. Wed had no exits to add a data point but the gap remains. Suggested rule: when a held name announces multiyear partnership with a named upstream/downstream counterparty OR receives a named-Tier-1-customer win, defer trend-exit signals through a 5-day repricing window OR scale long posture up 10-20%.
- **Underwriter-franchise-event overlay — open.** JPM exited Tue/Wed despite OpenAI underwriter naming + SpaceX overlap. Suggested rule: when JPM (or any underwriter) is named lead on a flagship IPO with >$500B target valuation, defer trend-exit signals through the listing window.
- **M&A target post-announcement (biotech / cross-sector) overlay — open Tue.** NUVL pinned near $124. No M&A-arb strategy exists. Priority claim swap from `equity_trend_following_ema_cross` for NUVL.
- **AAPL WWDC June 8-12 event-window posture rule. ACTIVE Day-3-5 Wed-Fri.**
- **NFP / CPI / FOMC macro-event-window rule. CPI WED 6/10 8:30 ET FIRED (response unknown without brief). FOMC Jun 16-17.**
- **Peer-earnings cohort-spillover overlay** (ORCL → cloud cohort Thu; ADBE → software cohort).
- **Geopolitical / oil-spike risk-off overlay** (Iran-Israel ceasefire fragile).
- **Rate-policy-shift sizing rule** (10Y yield around CPI / PPI / FOMC).
- **Credit-stress sector overlay** (Cliffwater + Blackstone gates → JPM).
- **TSMC capacity-constraint supply-side pricing-power overlay.**
- **Trump AI EO policy-tailwind sizing rule.**
- **EU cloud procurement regulatory-headwind rule.**
- **Corporate-action handler** (CRWD 4-for-1 split style).
- **Vol-regime overlay** (VIX > 20 = ELEVATED; Tue 20.45, Wed close unknown w/o brief).
- **AI-cohort multiple-compression overlay** (Anthropic Fable 5 + $3.6T IPO supply with SpaceX/OpenAI/Anthropic concentration).
- **Cross-sector defensive rotation overlay** (Tue REIT/staples/utilities bid).
- **Pre-print cohort-cert overlay** (held/candidate receives major-customer qualification confirmation pre-own-print).
- **News-brief-staleness handling.** If the news agent fails to update, the trader has no fallback. The current "proceed without context and note the gap" rule works for one-off misses; if it persists, the strategy library has no event-aware logic to fall back on. Soft observation, not a coded rule.

## Open questions for the operator

1. **News brief did not update for 2026-06-10.** Wed's brief is missing — file is still Tue's. Trader proceeded without it. Operator should check why the news agent didn't run / why the scheduled task didn't write `news_brief.md`.

2. **`cli add-active` REPLACES rather than APPENDS** — HIGH PRIORITY, carry-forward from Tue. Workaround: edit `state/active_strategies.md` directly when adding claims.

3. **`cli open-orders` parsing bug** — carry-forward, untested today (empty list at snapshot).

4. **NUVL claim placeholder via trend-following.** Need M&A-arb strategy. Sat research agent priority.

5. **CBRS, TSM claim placeholders** — safe-default trend-following. Validate via head-to-head Sat.

6. **MU buy stop at $813.44 → -8.44% unrealized after Wed close.** Stop ~9.6% buffer. Position into Jun 24 print.

7. **GOOGL/JPM Wed-open fill prices were derived from cash arithmetic, not Alpaca per-order report.** Combined sum is exact (+0.01210 of equity); per-symbol split (+0.01286 GOOGL, -0.00076 JPM) is proportional approximation.

8. **CPI Wed 6/10 fired (response unknown), ORCL Wed AMC, ADBE/PPI/SpaceX-IPO Thu, SpaceX listing Fri, FOMC Jun 16-17.** Catalyst stack continues. No macro-event-window rule active.

9. **Book is net-cash for the first time in weeks.** $32K cash + $72K longs = 0% leverage. New baseline posture going into the Thu/Fri catalyst stack.
