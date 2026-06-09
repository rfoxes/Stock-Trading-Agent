# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

---

## STANDING POLICY (P0, do not ignore)

**Every symbol in the universe MUST be claimed by an active strategy.**
See `manual.md` "P0 — ZERO-UNCLAIMED RULE" at the top. `cli execute`
REFUSES to run if any symbol is unclaimed. Claim via direct edit of
`state/active_strategies.md` (see Open Issue #1 below — `cli add-active`
is buggy and replaces existing claims).

---

## Status as of last update (Tue 2026-06-09, post-close)

- **Active set: 7 strategies, 22/22 universe symbols claimed (unclaimed_count == 0).**
  CBRS/INTC/NUVL/ORCL/TSM added today per P0 heuristic. Verify with `cli list-active`.
- **Today's execute: 2 intents submitted, both queued for Wed open as market sells.**
  - GOOGL sell 56 from `equity_trend_following_ema_cross` (EMA12 death-cross EMA26 exit). Order id `b7232cef-2130-4a92-b858-5799a9b8673c`. Est. P&L +$1,367 (profit exit).
  - JPM sell 64 from `equity_trend_following_ema_cross` (ADX(14)=20.0 at exit threshold; implementation treats as inclusive). Order id `311fc65b-1a94-4575-9bd2-724d311546bb`. Est. P&L -$22 (~flat).
- **Reconciled Mon's queued orders:** NVDA sell 96 filled ~$210.68 → +0.01020 of equity. MU buy 7 filled at $982.90 avg (opening fill; no reconciliation; now -$445.83 unrealized vs $813.44 stop).
- **Account: equity $105,122.24 (-1.02% vs Mon $106,202.11; chip-selloff drag).**
- **Regime: bull, conf 0.77, ADX 27.41.** Unchanged from Mon. ADX now ~7 above 20.0 EMA-cross exit threshold; further cool-down would fire more EMA-cross exits.
- **CLI bug discovered: `add-active` REPLACES the strategy's symbol claims rather than appending.** Recovered today via direct YAML edit. Workaround: edit `state/active_strategies.md` directly when adding claims.

## To do Wednesday (2026-06-10)

1. **Read last_handoff.md and news_brief.md FIRST.** Wed is CPI day
   (BLS release 8:30 ET; consensus +0.5% MoM / +4.2% YoY headline,
   +0.3% MoM / +2.9% YoY core). ORCL Q4 FY26 prints AMC. Anticipate
   the brief will be NOTABLE or higher.

2. **Standard read-and-snapshot.** Run `cli list-active`. Confirm
   `unclaimed_count == 0`. If a new universe entry appeared (Wed news
   promotion), claim via DIRECT YAML EDIT (see Open Issue #1) — do NOT
   trust `cli add-active`.

3. **Reconciliation.** Mon's GOOGL sell 56 and JPM sell 64 are queued
   Tue post-close and will fill Wed open:
   - **GOOGL sell 56** (was 56 long at $338.79 avg; Tue mark $364.00).
     Expected fill near Wed open price. Use actual fill from Alpaca
     positions delta. First-pass estimate: realized ≈
     ($364 - $338.79) × 56 ≈ +$1,412 ≈ +0.01343 of equity. Actual fill
     could come in different post-Tue-selloff Wed open.
     `cli log-closed equity_trend_following_ema_cross GOOGL <pnl_fraction>`.
   - **JPM sell 64** (was 64 long at $313.04 avg; Tue mark $312.70).
     Estimate ~flat to slightly negative. Use actual fill.
     `cli log-closed equity_trend_following_ema_cross JPM <pnl_fraction>`.

   Compute fills via cash-delta arithmetic if needed: (cash_change +
   GOOGL_outflow + JPM_outflow) = -(GOOGL_proceeds + JPM_proceeds).
   No buys queued Mon overnight; cash change should be pure sells inflow.

4. **Run `cli execute`.** Watch for:
   - **MU follow-on activity.** -$445.83 unrealized at Tue close;
     stop $813.44 still ~13% away. Watch for time-stop or stop-loss
     trigger if Wed continues chip-cohort weakness.
   - **ORCL pre-print posture.** event-driven-catalyst strategy now
     claims ORCL. Prints Wed AMC. Strategy may or may not fire entry
     pre-print (didn't fire today; the rule keys off catalyst-flag).
     If brief flags ORCL positive pre-print, expect possible entry.
   - **CPI reaction.** No macro-event-window rule. Strategies will fire
     on whatever technical signal forms in the post-CPI tape.
   - **Other names.** ADX continues to govern trend-following exits.
     With JPM gone after Wed open, claimed-but-no-position trend-following
     names = AAPL, NVDA (gone), QQQ, SPY, AMZN (gone), TSLA (gone),
     CBRS, NUVL, TSM. Held among them: AAPL, QQQ, SPY. Plus MU.

5. **HALT-WORTHY check.** Pre-CPI tape can be volatile. If brief flags
   HALT-WORTHY (e.g., CPI prints >2σ off consensus), use discretion to
   skip `cli execute`. Standard threshold: only skip if brief explicitly
   says HALT-WORTHY EVENT, not on intraday vol alone.

6. **Library gaps — see list below.** Two soft-flag re-confirmations
   today (GOOGL/JPM exits on event-positive days) re-affirm existing
   gaps. No new gap categories.

7. **Run `cli git-sync --agent trader --message "..."` as last action.**
   Then `cli git-doctor` once if any lock-file warnings appeared.

## Library gaps for the research agent (carry to research_tasks.md Sat)

These are EVENT-OVERLAY gaps + the 5 new first-pass assignments. Every universe symbol is claimed.

- **Validate the now-5-strategy first-pass assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT *(META 1-day round-trip realized -$764 unchanged data point)*
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC *(INTC added 2026-06-09)*
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL *(ORCL added 2026-06-09, Wed AMC print is fresh data; today's MU print prep is ongoing)*
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` vs ??? on CBRS, NUVL, TSM *(safe-default placeholders, especially NUVL biotech)*
- **Tier-1 supply-chain / customer-win partnership overlay — RE-CONFIRMED Day-3 in a row.** NVDA exited Mon despite NVDA-SK Hynix Sun positive; GOOGL exited Tue despite Google-SpaceX cloud deal + BNP Gemini share-gain Tue positive. Suggested rule: when a held name announces multiyear partnership with a named upstream/downstream counterparty OR receives a named-Tier-1-customer win, defer trend-exit signals through a 5-day repricing window OR scale long posture up 10-20%.
- **Underwriter-franchise-event overlay — extended.** OpenAI confidential S-1 Tue named JPM as lead underwriter (alongside Goldman, Morgan Stanley) on top of the SpaceX Thu/Fri pricing-listing window. JPM exit on ADX-cool fires regardless. Suggested rule: when JPM (or any underwriter) is named lead on a flagship IPO with >$500B target valuation, defer trend-exit signals through the listing window.
- **M&A target post-announcement (biotech / cross-sector) overlay — NEW Tue.** NUVL entered universe Tue as confirmed GSK $10.6B M&A target at $124/share. Stock will pin near $124 barring break. No M&A-arb strategy exists. Suggested rule: post-announcement entry on confirmed M&A target with stop at announced deal price minus 5%; exit on deal close or termination news. This is the priority claim swap from `equity_trend_following_ema_cross` for NUVL.
- **AAPL WWDC June 8-12 event-window posture rule. ACTIVE THROUGH FRI.** Day-2 Tue punished AAPL on monetization questions. Day-3-5 reactions Wed-Fri.
- **NFP / CPI / FOMC macro-event-window rule. CPI WED 6/10 8:30 ET, FOMC Jun 16-17.**
- **Peer-earnings cohort-spillover overlay** (AVGO → NVDA/MU/MRVL; ORCL → cloud cohort Wed).
- **Geopolitical / oil-spike risk-off overlay** (Iran-Israel ceasefire fragile, oil -5% Tue).
- **Rate-policy-shift sizing rule** (10Y yield around CPI / FOMC).
- **Credit-stress sector overlay** (Cliffwater + Blackstone gates → JPM).
- **TSMC capacity-constraint supply-side pricing-power overlay.**
- **Trump AI EO policy-tailwind sizing rule.**
- **EU cloud procurement regulatory-headwind rule.**
- **Corporate-action handler** (CRWD 4-for-1 split style).
- **Vol-regime overlay** (VIX intraday Tue 18.92 → 20.45 +8% — ELEVATED >20 tag back live).
- **AI-cohort multiple-compression overlay** (Anthropic Fable 5 token-pricing AI-bubble + $3.6T IPO supply with SpaceX/OpenAI/Anthropic concentration).
- **Cross-sector defensive rotation overlay** (Tue REIT/staples/utilities bid vs AI-cohort sold).
- **Pre-print cohort-cert overlay** (held/candidate receives major-customer qualification confirmation pre-own-print).

## Open questions for the operator

1. **`cli add-active` REPLACES rather than APPENDS** — HIGH PRIORITY. Hit
   today claiming 5 unclaimed symbols. Each `add-active` call wiped the
   strategy's prior symbol list. Recovered via direct YAML edit. Until
   fixed, the workflow for claiming a new symbol on a strategy that
   already owns symbols MUST go through direct file edit, not the CLI.
   Suggested fix: append by default; require `--replace` to overwrite.

2. **`cli open-orders` parsing bug** — carry-forward. Untested today
   when orders are live (Mon's 2 cleared at Tue open; Tue's 2 just
   submitted at end-of-run).

3. **NUVL claim placeholder via trend-following.** NUVL is a deal-pinned
   biotech M&A target; trend-following won't generate meaningful signals.
   Need M&A-arb strategy. Sat research agent priority.

4. **CBRS, TSM claim placeholders** — safe-default trend-following.
   Validate via head-to-head Sat.

5. **GOOGL exit on Google-SpaceX positive — Day-3 consecutive event-positive
   exit pattern.** NVDA Mon, GOOGL Tue. Library gap doubly confirmed.

6. **JPM exit at ADX=20.0 exactly + OpenAI underwriter franchise event
   Tue.** Borderline ADX firing + no franchise-event rule = exit on a
   franchise-tailwind day.

7. **MU buy stop at $813.44 → -6.5% unrealized after Tue chip selloff.**
   Stop still ~13% buffer. Position into Jun 24 print.

8. **CPI Wed 6/10 8:30 ET, ORCL Wed AMC, ADBE/PPI/SpaceX-IPO Thu,
   SpaceX listing Fri.** Catalyst stack continues. No macro-event-window
   rule active.

9. **NUVL universe membership terminates on GSK deal close.** While the
   deal is pending the symbol stays in the universe and the harness
   tracks it; on close, remove from `extra_symbols.md` (operator action
   when the time comes).
