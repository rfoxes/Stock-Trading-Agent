# Tasks for the next run

**✅ 7/13 COMPLETE (single fire, canonical 16:03, Monday).** Quiet KEEP day. Book unchanged (**META only**, cash
$94,690.29, no open orders, META +8.4%). **Nothing closed → no reconciliation.** News brief was **FRESH & on-time**
(correctly dated 7/13 — Friday's staleness resolved); NOTABLE-not-halt-worthy (AI-memory cohort selloff + US-Iran
Hormuz oil shock + dense 7/14 stack). Universe grew **32 → 33**: news promoted **RIVN** (75M-share dilutive
offering) → `triage-symbol RIVN` → `equity_event_driven_catalyst`, quarantined, `revalidate_by 2026-07-27`.
`cli execute` = 0 intents. See `last_handoff.md`. Replace this file (don't append) when you write the next version.

## ⚠️ NEXT RUN IS TUESDAY 7/14 — THE RISK-DENSE SESSION
Tomorrow BMO: **June CPI** (8:30 AM, consensus ~3.8% headline / ~2.8% core) + **Warsh's first semi-annual
testimony** + **five big banks report simultaneously (JPM/GS/BAC/C/WFC)**. Last inflation read before the 7/28-29
FOMC. **None of this makes today's run different** — but the 7/14 news brief will carry the actual CPI/bank-print
reactions. Read the brief's headline assessment carefully; a hot CPI + hawkish Warsh, or an overnight Hormuz
escalation gapping futures >2%, would be the halt-worthy lines. Positions still ride their own rules regardless.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5
in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED
until Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a
below-baseline trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are
FORBIDDEN. Never use `cli add-active` to bypass triage.

## To do next run (Tue 7/14 — event-dense day; book stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-14; if
   not, treat as ABSENT, note the gap, fall back to the raw `news/daily_summary/2026-07-14.html` for a halt-worthy
   safety scan. **Run `cli market-status`**; note the run TIME. If it double-fires (a 2nd fire same day — the tell
   is a `[trader 2026-07-14]` commit already in git log + a handoff already narrating a completed 7/14 run), take
   NO action: don't re-execute, don't re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$105k (moves only on META's mark).
     No resting orders. If instead FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe → FREEZE
     (see playbook). Nothing is currently pending to close, so a rising-cash vanish is not expected.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 5` (QCOM/SPCX/SYNA
   `revalidate_by 2026-07-21`; SKHY `2026-07-24`; **RIVN** `equity_event_driven_catalyst` `2026-07-27`). All five
   are ALREADY claimed/quarantined — do NOT re-triage them; research owns validation. Triage only any *new*
   unclaimed symbol (the news agent may promote a bank peer / memory-cohort / IPO name). Do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's live
   claims (AVGO/MU/ORCL) are flat with no fresh *discrete single-name* entry catalyst → likely fires nothing (a
   cohort de-rate is NOT a responder event). Provisionals stay quarantined/skipped.
5. **Library gaps — see list below (Saturday 7/18 research owns them; some are now imminent — JPM earnings 7/14).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash
unchanged + vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL
`get_order` fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson in manual.md).

## Position watch

- **META (+8.4%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending). Gave back ~2 pts of unreal in the 7/13 tech risk-off but its own news was
  *constructive* (Hyperion → $50B+ capex, AI-API priced ~75% below OpenAI/Anthropic). Noted overbought/near
  resistance + caught in the cohort selloff — do NOT hand-manage on the cohort move or the capex/regulatory
  headlines; all are informational (no responder).
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. MU's 7/13 cohort selloff is NOT such a catalyst.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/18)

All `responder: NONE` — informational, not tradable under the mandate. Carried + refreshed for 7/13:
- **Provisional/quarantined validations (TOP PRIORITY):** now **5** — QCOM (event-driven), SPCX (trend-following,
  lockup/float "900% explosion"), SYNA (pairs, onsemi merger-arb) — all `revalidate_by 2026-07-21` — **SKHY**
  (`equity_watch_only`; now quoting regular-way, real bars accruing → first backtestable window, `2026-07-24`) —
  plus **RIVN** (event-driven; 75M-share dilutive offering, degenerate 0-trade backtest, `2026-07-27`).
  Validate/upgrade or archive each.
- **Earnings/print-window ASSIGNMENT gap — JPM (7/14, window OPEN, MOST URGENT; +June CPI +Warsh same morning),
  TSM (this week), TSLA (7/22), ARM/INTC (7/23; INTC a JPMorgan Q3 short-call), AMZN (7/30).** All claimed by
  trend-following/breakout, NOT `equity_event_driven_catalyst` / `long_straddle_earnings`. Reassign or activate a
  straddle on the cluster. JPM is now imminent.
- **Sector / cohort selloff + sentiment-reversal — the AI-memory de-rate (Samsung record-but-"only"-19× guidance →
  MU/SKHY/SNDK/WDC; DRAM ETF -30%/mo).** No rule reads a cohort-wide sentiment reversal or a peer's guidance
  read-through. *Research: a cohort/sector risk-off overlay (overlaps with liquidity-rotation from prior briefs).*
- **Geopolitical / energy-shock overlay (NEW) — US-Iran Strait-of-Hormuz strikes, oil +5%, chips→energy rotation
  (MRVL -6%).** No rule reads an oil/geopolitical shock or its cross-sector read-through. *Research: a macro/
  energy-shock risk overlay.*
- **Index / forced-flow + lockup/float mechanics (recurring) — SPCX "900% float explosion" (lockup expiry);
  leveraged single-stock/DRAM ETFs; prior SKHY/SK-Hynix IPO-rotation.** No `index_rebalance` gap_type exists.
  Argues for a 6th Tier-B trigger / forced-flow overlay.
- **Regulatory / litigation overlay — AAPL (Epic new phase + v. OpenAI trade-secret suit); META EU DSA (carry,
  preliminary, up to 6% of rev).** No rule reads a court/agency action.
- **Capital-allocation / capex overlay (recurring) — META Hyperion $50B+ + AI-API pricing; MU/Micron $6.9B
  reshoring (+ $250B carry); Lutnick pressing Samsung/SK Hynix on US fabs.** No rule reads a multi-year capex /
  reshoring / pricing move. *Research: a capex/capital-allocation overlay AND a re-entry rule for
  event_driven_catalyst.*
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right?
  Backtest the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **M&A-arb activation — RKLB (acquirer) / IRDM (target, $54/sh, $8B deal) + SYNA/onsemi (carry).**
  `equity_pairs_trading_cointegration` declares pairs_arbitrage but claims only SYNA; RKLB/IRDM pair unmodeled
  (both currently breakout). Cointegration look on RKLB/IRDM if breakout decays.
- **Activist-short / short-call — BE Hunterbrook reports (ongoing, contested); INTC JPMorgan Q3 short-call
  (carry).** No responder reads a short report or its rebuttal.
- **Vol-regime activation — VIX +14% to 17.16; record single-name / event-IV into CPI + five bank prints + TSM
  this week.** Structures exist (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`)
  but none active / none claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **Litigation / product / vendor-strategy events — AAPL v. OpenAI; TSLA closing Fremont Model S/X line for Optimus
  robots; MSFT AI-ownership commentary; export-control report.** No rule reads a lawsuit / product launch / vendor
  shift.
- **Fallback-threshold question (issue #5, fresh RIVN data point 7/13)** — no-price-history routes to
  `equity_watch_only` correctly (SKHY). The open case is only the degenerate 0-trade Sharpe-0.0 backtest
  (RIVN today; WULF/SMCI/RKLB/IRDM/BE historically) routing to a below-baseline *trading* provisional. Decide
  whether a 0-trade score should also route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Financials under-represented (news-agent note)** — only JPM in the universe; GS/BAC/C/WFC all report 7/14.
  Operator may consider promoting one bank peer for breadth (not auto-promoted — cohort earnings preview).

## Open questions for the operator

1. **[HIGH — timing] Confirm single-trigger schedule.** 7/7 & 7/8 double-fired; **7/9, 7/10, 7/13 fired once ✓.**
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/13 (brief fresh & on-time), but
   the 7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden the news agent's
   brief-synthesis + git-sync so a weekend/late run can't leave a stale brief.
4. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
5. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (RIVN is the newest instance; see gaps).
6. **FIVE provisional/quarantined claims** — QCOM/SPCX/SYNA (`2026-07-21`) + SKHY (`2026-07-24`) + RIVN
   (`2026-07-27`). Saturday research owns validation. Do NOT hand-promote.
