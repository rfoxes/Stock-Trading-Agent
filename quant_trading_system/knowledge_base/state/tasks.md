# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

---

## STANDING POLICY (P0, do not ignore)

**Every symbol in the universe MUST be either (a) claimed by an active
strategy via algorithmic triage, or (b) flagged as a true library gap.**
See `manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE" (top
of `manual.md`, refined 2026-06-10). `cli execute` REFUSES to run if any
symbol is unclaimed AND not in `state/library_gaps.md`.

**Use `cli triage-symbol <SYM> [--gap-type X]`** for every unclaimed
universe symbol — auto-claims if Sharpe ≥ 0.5 on a library candidate,
else auto-records to `state/library_gaps.md`. Character-match shortcuts
and direct YAML edits to `active_strategies.md` are FORBIDDEN. The
`cli add-active` UNION fix landed today (commit 3daff8d); pass
`--replace` for the old overwrite behaviour.

---

## Status as of last update (Wed 2026-06-10, true post-close)

- **Active set: 7 strategies, 22/22 universe symbols claimed (unclaimed_count == 0).**
  No claim changes today.
- **Today's execute: 1 intent submitted.** `equity_event_driven_catalyst`
  → **ORCL buy 38 shares market day** (order_id `3d56fcac-a86f-412c-8918-c8ccb6bead45`).
  All 5 SafetyGate checks passed. Will fill Thu open.
- **6 other strategies: 0 intents each.**
- **No reconciliation needed today** (Tue's GOOGL/JPM exits already logged in earlier-in-day handoff via commit e6d0b26).
- **Account: equity $103,575.68 (down from earlier $104,506.85 snapshot — intraday mark drift); cash $32,063.73 (unchanged, ORCL not yet filled); buying power $321,605.61 (down from $328,681 due to ORCL reservation).**
- **Positions: 4 longs unchanged from earlier-in-day handoff but marks moved — AAPL 72 (+6.93%), MU 7 (**-11.49%** ← from -8.44%), QQQ 28 (+6.21%), SPY 35 (+1.84%). ORCL 38 pending fill.**
- **Regime: bull, conf 0.77, ADX 27.41.** Unchanged.
- **News brief: PRESENT today (NOTABLE).** Earlier-in-day handoff's "missing brief" issue resolved by commit 617846d.

## To do Thursday (2026-06-11)

1. **Read last_handoff.md and news_brief.md FIRST.** Heavy Thu stack continues:
   - PPI May + initial jobless claims 8:30 ET (consensus PPI +0.3% MoM; claims ~220K).
   - ADBE Q2 prints AMC.
   - SpaceX IPO pricing AMC (lists Fri).
   - **ORCL fill expected at Thu open** — see step 3.

2. **Snapshot + P0 triage.** Standard `cli list-active`. If `unclaimed_count > 0`, run `cli triage-symbol <SYM> [--gap-type <type>]` per symbol — auto-claim or auto-flag as library gap. **Do NOT use `cli add-active` for unclaimed symbols** (triage is the only sanctioned path).

3. **RECONCILE THE ORCL FILL (priority).** ORCL buy 38 should fill at Thu open. Check `cli positions`:
   - If ORCL appears as a long position: note avg fill price, market value, unrealized P&L. The strategy's ATR stop was set at submit time; verify it's still in place. NO `log-closed` call (this is an entry, not exit).
   - If ORCL did NOT fill (broker rejection, halt, etc.): document in handoff and flag for operator. The `cli open-orders` parser is currently broken (`'dict' object has no attribute 'id'`), so you may need to infer from `account` cash + buying-power deltas.
   - Compare ORCL Thu open to Wed AH close. AH was down on capex shock; if gap-down is severe (>5%), the ATR stop may fire same-day. **Trust the rule** — algorithmic-only mandate. Do not override.

4. **Other position watch:**
   - **MU stop buffer ~6.5%.** Position -11.49% Wed close; $813.44 stop is ~$56 below $870 current. If chip cohort continues lower Thu, stop may trigger. Pre-print window through 6/24.
   - **AAPL WWDC Day-4.** Penultimate WWDC reaction day. Trend-following claims AAPL; rule respects price action.
   - **ADBE post-print Thu AMC.** ADBE not in universe; not actionable.
   - **PPI reaction.** No macro-event-window rule; price action only.
   - **SpaceX pricing AMC.** Listing Fri. JPM exited Tue/Wed so no franchise event to defend.

5. **Run `cli execute`.** Watch for:
   - **Possible ORCL exit** if the ATR stop fires intraday on a hard gap-down.
   - **MU stop trigger** if MU breaks $813.44.
   - **Trend-following entries** on any of the 6 non-held universe names if Wed price action set up signals.

6. **HALT-WORTHY check.** Multiple catalysts. Default standard execute unless brief explicitly says HALT-WORTHY EVENT.

7. **Library gaps — see list below.** Wed added ONE new soft-signal gap (news-brief keyword detector cannot distinguish asymmetric reactions).

8. **Run `cli git-sync --agent trader --message "..."` as last action.**

## Library gaps for the research agent (carry to research_tasks.md Sat)

These are EVENT-OVERLAY gaps + the 5 still-unvalidated first-pass assignments. Every universe symbol is claimed; head-to-head validation remains the Sat research priority.

- **NEW (Wed 2026-06-10): news-brief keyword detector cannot distinguish asymmetric reactions.** The `event_driven_catalyst` strategy uses `news_brief.has_positive_signal(sym)` and `has_negative_signal(sym)` as keyword-match gates. Wed's ORCL bullet contained BOTH a beat+raise positive headline AND a capex-shock + AH-selloff negative framing — but `has_negative_signal` did not match the asymmetric-reaction keywords (capex, AH selloff, after-hours drop, negative reaction to beat). The strategy entered ORCL on positive-only signal. **Suggested research:** extend `_news_brief.py` keyword sets with asymmetric-reaction terms, OR add a `has_asymmetric_signal()` shortcut that returns true when positive AND negative both match — strategies can then choose to skip entry. This is the mirror of the brief's `capex_shock_negative_event` overlay request.
- **Validate the now-5-strategy first-pass assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL *(ORCL now has a real entry to validate against)*
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` vs ??? on CBRS, NUVL, TSM
- **Tier-1 supply-chain / customer-win partnership overlay.** NVDA/GOOGL anchor-customer confirmation Wed (Apple Foundation Models on Google Cloud + NVDA chips) didn't trigger any defer-exit logic. Suggested rule unchanged.
- **Underwriter-franchise-event overlay — open Day-2.** JPM exited Tue/Wed despite OpenAI underwriter naming + SpaceX overlap.
- **M&A target post-announcement (biotech / cross-sector) overlay — open.** NUVL pinned. No M&A-arb strategy exists.
- **AAPL WWDC June 8-12 event-window posture rule. ACTIVE Day-3-5 Wed-Fri.**
- **NFP / CPI / FOMC macro-event-window rule. CPI fired Wed in-line; FOMC Jun 16-17.**
- **Peer-earnings cohort-spillover overlay** (ADBE → software cohort Thu).
- **`capex_shock_negative_event` overlay** (ORCL Wed AMC: beat+raise but $40B FY27 capital raise drove down in AH).
- **Geopolitical / oil-spike risk-off overlay** (Iran-Israel active exchange Day-1; oil reversed Mon-Tue weakness).
- **Rate-policy-shift sizing rule** (10Y yield around CPI / PPI / FOMC).
- **Credit-stress sector overlay** (Cliffwater + Blackstone gates → JPM).
- **TSMC capacity-constraint supply-side pricing-power overlay** (TSM May +30% YoY).
- **Trump AI EO policy-tailwind sizing rule.**
- **EU cloud procurement regulatory-headwind rule.**
- **Corporate-action handler** (CRWD 4-for-1 split style).
- **Vol-regime overlay** (VIX 19.87 Wed mid-afternoon; third probe at 20 ELEVATED threshold).
- **AI-cohort multiple-compression overlay** (Burry short paying off + ORCL capex overshoot + Anthropic token-pricing).
- **Cross-sector defensive rotation overlay** (energy / dividend / quality bid vs AI cohort).
- **Pre-print cohort-cert overlay.**
- **News-brief-staleness handling.** Earlier-in-day Wed brief was missing for the first trader run; resolved later in the day. If staleness persists across runs the strategy library has no event-aware fallback.

## Open questions for the operator

1. **Two trader runs on Wed 6/10.** The earlier-in-day "do-nothing" run (commit e6d0b26) executed before the news brief was written. The scheduled task then fired again later in the day (this run), and the brief-using `event_driven_catalyst` rule fired the ORCL entry. Is the scheduled task firing more than once per day intentional? If not, the trigger setup may need review.

2. **`cli open-orders` parser bug remains.** `'dict' object has no attribute 'id'`. Now actively blocking — Wed has a live submitted order (ORCL) that can't be inspected from the CLI. HIGH PRIORITY operator fix.

3. **News-brief keyword detector lacks asymmetric-reaction nuance.** Sat research gap above; operator should also be aware that the gate is keyword-based and coarse.

4. **MU buy stop at $813.44 → -11.49% unrealized after Wed close.** Stop buffer ~6.5%. One chip-cohort red day away from triggering. Pre-print window through 6/24.

5. **NUVL/CBRS/TSM claim placeholders** — Sat research priority. NUVL especially (biotech M&A target with no M&A-arb strategy).

6. **GOOGL/JPM Wed-open fill prices were proportional cash-arithmetic, not Alpaca per-fill report.** Combined sum exact (+0.01210 of equity); per-symbol approximate. Carry-forward.

7. **CPI Wed in-line (4.2% headline matched consensus); PPI Thu; ADBE Thu AMC; SpaceX IPO pricing Thu AMC → list Fri.** Catalyst stack continues. No macro-event-window rule.

8. **Book is net-cash $32K cash vs $72K longs (0% leverage) — will become slightly less net-cash post-ORCL-fill Thu.** ORCL ~38 × $215 = ~$8,170 = ~8% of equity at entry.

9. **FOMC June 16-17.** Hold base case; dot plot is the catalyst. One week out.
