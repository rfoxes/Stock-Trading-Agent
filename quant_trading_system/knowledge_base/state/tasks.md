# Tasks for the next run

**✅ 7/21 COMPLETE (single fire, canonical 16:03, Tuesday). FIRST COVERED SESSION SINCE 7/16.** KEEP day on a
constructive semi-led rebound. Book unchanged (**META only**, cash $94,690.29, no open orders, META **+5.84%** —
down from 7/16's +9.89% through the two un-covered down sessions, still green/trending). **Nothing closed → no
reconciliation.** News brief **FRESH & on-time** (correctly dated 7/21); **NOTABLE — a broad semiconductor-led relief
rally snapping a 3-session losing streak, constructive and NOT halt-worthy** (Nasdaq +1.29%, S&P +0.89%, SOX +5.2%,
VIX ~18.65, no >2% futures gap). Driver = strong Korea/Taiwan AI-export data + memory-price upturn (MU +12%, SNDK
+14%). Hard single-name catalysts (SMCI record >$60B backlog +18% AH, NVDA 9.3% Nebius stake, RKLB $266M defense
contract, INTC +5% Google Cloud deal, IREN raised >$4B AI-cloud guide) all `responder: NONE`. Universe grew **37 →
40**: news promoted **NBIS, IREN, AMD** (all Tier-0 news-subjects with hard discrete catalysts) → each `triage-symbol
--gap-type event_catalyst` → all `equity_event_driven_catalyst` below-baseline provisional (Sharpe 0.0/0 trades,
degenerate-0-trade = issue #5), quarantined, `revalidate_by 2026-08-04`. `provisional_count 9 → 12`. `cli execute` =
clean no-op 0/0/0. See `last_handoff.md`. Replace this file (don't append) when you write the next version.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.
Note: CLI prints a `safety_gate_initialized` structlog line to **stdout** before the JSON — pipe through
`grep '^{'` before parsing with python/jq.

## ⚠️ RUN-GAP CONTEXT (7/17, 7/20, Sat 7/18 all DROPPED — resolved this run, informational for you)
- The 7/21 run was the FIRST coverage since 7/16 (two trader/news days + Saturday research skipped). The book was
  frozen-in-amber (no execute ran in the gap → nothing closed, cash to the penny) and resumed cleanly. If you see
  another multi-day gap: it's NOT a wipe (book stays intact, not flat) and NOT a double-fire — resume normally,
  reconcile nothing, and note any provisional deadlines that lapsed in the gap are overdue-but-quarantined. Full
  doctrine now in manual.md "Recent feedback" (skipped-run bullet).
- **THREE overdue provisionals: QCOM / SPCX / SYNA** hit `revalidate_by 2026-07-21` with no Saturday research.
  Overdue but STAY quarantined — you do NOT validate (research's job). Flagged to operator.

## ⚠️ WED 7/22 CONTEXT (informational — TSLA prints, but none of it changes your run)
- **TSLA reports Q2 tonight (7/22 AMC), ~6% implied move** — record 480K deliveries (+25% YoY) but murky margins;
  raised Model 3 lease prices up to 15% ahead of the print. TSLA is on `equity_trend_following_ema_cross`, NOT an
  earnings-window responder → the print itself will be UNRESPONDED (the acute recurring earnings-window gap). This is
  informational; you have no earnings-window responder on TSLA to act on. If the news agent promotes any NEW name
  (e.g. off a TSLA reaction), triage it (do NOT `add-active`).
- **Next earnings cluster:** TSLA 7/22 AMC, INTC/ARM 7/23, MSFT 7/29, AMZN/AAPL 7/30. SMCI pre-announced 7/21
  (backlog, UNRESPONDED — it's on `mean_reversion_bollinger`; full report Aug 11).
- **Live tails:** (1) **AI-capex-doubt** is still the #1 named tail risk (BofA survey) even after today's chip
  re-rate — a dispersion regime (±12-14% single-name chip swings under VIX ~18.65), not a panic. (2) **US-Iran/Hormuz
  resumed** (Iran struck 3 vessels, ceasefire broke down), oil elevated (~$4 gasoline), but equities rallied through
  it. A >2% overnight equity-futures gap is the halt-worthy line — was NOT there 7/21. (3) **China chip-manufacturing
  curbs** (TSM/QCOM watch); USTR 25% Brazil tariff effective 7/22. Positions ride their own rules regardless.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5 in
triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED until
Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a below-baseline
trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]`
for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are FORBIDDEN. Never use
`cli add-active` to bypass triage.

## To do next run (Wed 7/22 — book stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-22; if
   not, treat as ABSENT, note the gap, fall back to the raw `news/daily_summary/2026-07-22.html` for a halt-worthy
   safety scan. **Run `cli market-status`** + `git log --oneline -5`; note the run TIME. If it double-fires (a 2nd
   fire same day — tell is a `[trader 2026-07-22]` commit already in git log + a handoff already narrating a completed
   7/22 run), take NO action: don't re-execute, don't re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$104-106k (moves only on META's mark).
     No resting orders. If instead FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe → FREEZE (see
     playbook). Nothing is currently pending to close, so a rising-cash vanish is not expected.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 12` (AMD/IREN/NBIS `2026-08-04`;
   GS `2026-07-28`; MS/PYPL `2026-07-29`; QCOM/SPCX/SYNA `2026-07-21 OVERDUE`; SKHY `2026-07-24`; RIVN `2026-07-27`;
   UNH `2026-07-30`). All twelve are ALREADY claimed/quarantined — do NOT re-triage them; research owns validation.
   Triage only any *new* unclaimed symbol. Do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's live
   claims (AVGO/MU/ORCL) are flat with no fresh *discrete single-name* entry catalyst → likely fires nothing.
   Provisionals stay quarantined/skipped.
5. **Library gaps — see list below (Saturday research owns them; the earnings-window assignment gap is the most
   acute, live again 7/21 with SMCI and again 7/22 with TSLA).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash unchanged
+ vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL `get_order`
fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson in manual.md). **Also distinguish a SKIPPED-RUN
gap** (book INTACT at prior qty/avg-entry + cash unchanged + no closes + a multi-day hole in git log) → NOT a wipe,
resume normally (7/21 skipped-run doctrine now in manual.md).

## Position watch

- **META (+5.84%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending). Rebounded green today; its 7/21 touchpoints (Ackman long/"cheap stock,"
  ARK added, "Meta Compute" neocloud push) are constructive positioning, NOT an adverse single-name shock — do NOT
  hand-manage on those or any capex/regulatory/positioning headline; all informational (no responder).
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. ORCL's ~4% 7/21 sector bounce (still near 52-wk
  lows) is not a directive to hand-manage.

## Library gaps + research items (carry to research_tasks.md — Saturday, if research runs)

All `responder: NONE` — informational, not tradable under the mandate. `gap-registry coverage_holes` is **empty**;
every item is an activation/assignment/taxonomy gap (a rule/event-type not mapped to the symbol that had the event):
- **Provisional/quarantined validations (TOP PRIORITY):** now **12** — all on `equity_event_driven_catalyst` except
  as noted: **AMD** (MS AI deal, `2026-08-04`), **IREN** ($2.8B contracts + >$4B guide, `2026-08-04`), **NBIS** (NVDA
  9.3% stake, `2026-08-04`), **GS** (`2026-07-28`), **MS** (`2026-07-29`), **PYPL** ($53B M&A target, `2026-07-29`),
  **QCOM** (`2026-07-21 OVERDUE`), **RIVN** (Q2 beat+raise, `2026-07-27`), **UNH** (Q2 blowout, `2026-07-30`) — all
  degenerate-0-trade Sharpe-0.0 below-baseline trading provisionals. Plus **SKHY** (`equity_watch_only`; no-history,
  `2026-07-24`), **SPCX** (`equity_trend_following_ema_cross`; no-history, `2026-07-21 OVERDUE`), **SYNA**
  (`equity_pairs_trading_cointegration`; onsemi merger-arb, `2026-07-21 OVERDUE`). Validate/upgrade or archive each.
  **QCOM/SPCX/SYNA are OVERDUE** (missed the 7/18 research run) — clear them first.
- **Earnings/print-window ASSIGNMENT gap (MOST ACUTE recurring — TWO fresh live examples this window: SMCI +18% AH
  pre-announcement 7/21 UNRESPONDED (on `mean_reversion_bollinger`); TSM 7/16 capex selloff UNRESPONDED (on
  `trend_following`)). Upcoming: TSLA 7/22 AMC (on `trend_following` — will be unresponded), INTC/ARM 7/23, MSFT 7/29,
  AMZN/AAPL 7/30; plus quarantined GS/MS/PYPL/QCOM/RIVN/UNH.** These prints are claimed by trend-following / breakout /
  mean-reversion / macd, NOT `equity_event_driven_catalyst` (unvalidated) / `long_straddle_earnings`. **Reassign /
  activate an earnings-window responder on the names actually printing.** Single strongest research priority.
- **Strategic-investment / stake / M&A event — NVDA's 9.3% Nebius stake; AMD's Microsoft AI deal; PYPL ($53B M&A
  target, quarantined); SYNA/onsemi.** No rule reads an equity-stake disclosure or a named partnership/M&A.
  *Research: an event/M&A/stake overlay; cointegration look for merger-arb.*
- **Contract-win event — RKLB's $266M defense contract (on `breakout_volume_confirmation`, reads price/volume not
  awards); IREN's $2.8B contracts.** No rule reads a contract award. *Research: a contract/award responder in the
  event overlay.*
- **Partnership / product-roadmap overlay — AAPL–Klarna leasing deal; GOOGL's new Gemini Flash models + Frozen v2
  chip; INTC's Google Cloud AI deal.** No rule reads a partnership or a product launch. *Research: a product/
  partnership-event overlay.*
- **Pricing-action / policy overlay — TSM's ~10% price-hike plan; China's chip-manufacturing curbs (TSM/QCOM); USTR
  25% Brazil tariff (eff. 7/22); TSLA's Model 3 lease-price hike.** No rule reads a pricing action or an
  export-control/tariff policy shift. *Research: a policy/pricing-event overlay.*
- **AI-capex re-rating + cohort momentum (BIDIRECTIONAL — de-rate 7/16, re-rate 7/21) — today's semi/memory rebound
  on Asia export data (MU +12%, SNDK +14%, SOX +5.2%); the AI-capex credit-event fear is still the #1 tail (BofA
  survey); ORCL bounced 4% but still near 52-wk lows.** No rule reads a cohort-wide capex re-rating in *either*
  direction (`sector_rotation_momentum` claims only DELL). *Research: a cohort / sector-risk overlay handling both
  the de-rate and the re-rate.*
- **Analyst-action / valuation-shock (event-scale) — BE (+ on a JPMorgan ~30% PT raise); SNDK/MU (analyst
  memory-price calls, MS 25% spike / BofA $1,550 Micron).** Recurring event-scale analyst reactions; normally
  dropped, but repeated scale argues for a filter that fires only on event-scale moves. *Research: a rating-action /
  valuation-shock filter.*
- **Index / forced-flow + ETF/float mechanics — SKHY (Korea leveraged-ETF margin; carry); SPCX (sub-IPO leveraged/
  inverse ETFs).** No `index_rebalance` gap_type exists. Argues for a 6th Tier-B trigger / forced-flow overlay
  (`NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`).
- **Geopolitical / energy-shock overlay — US-Iran/Hormuz (resumed, Iran struck 3 vessels), oil elevated,
  diesel/gasoline read-through.** No rule reads an oil/geopolitical shock or its inflation read-through. *Research: a
  macro/energy-shock risk overlay.*
- **Vol-regime / dispersion activation (persistent) — VIX ~18.65 with extreme single-name chip dispersion (±12-14%
  daily swings); dense event IV into TSLA 7/22, INTC/ARM 7/23, MSFT 7/29, AMZN/AAPL 7/30.** Options skeletons
  (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) exist but none active / none
  claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right? Backtest
  the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **Fallback-threshold question (issue #5, three fresh data points 7/21: NBIS/IREN/AMD)** — no-price-history routes
  to `equity_watch_only` correctly (SKHY/SPCX). The open case is the degenerate 0-trade Sharpe-0.0 backtest (NBIS/
  IREN/AMD today; UNH 7/16; GS 7/14; MS/PYPL 7/15; RIVN 7/13) routing to a below-baseline *trading* provisional.
  Decide whether a 0-trade score should also route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Healthcare breadth — still thin (UNH + NUVL).** Awareness only (not a trade directive).

## Open questions for the operator

1. **[HIGH — timing] Schedule reliability — BOTH failure modes now seen.** 7/7 & 7/8 double-fired; 7/9-7/16 clean;
   **7/17, 7/20, Sat 7/18 DROPPED** (this run was first coverage since 7/16). Confirm single-trigger + no-drop config.
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[HIGH — new] Overdue provisionals + skipped research.** QCOM/SPCX/SYNA overdue (`revalidate_by 7/21`, no Sat
   research). The provisional book (now 12) only shrinks when research validates/archives — if research keeps
   missing, add a trader escalation path.
4. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/21 (brief fresh & on-time), but the
   7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden brief-synthesis + git-sync.
5. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
6. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (NBIS/IREN/AMD are the newest instances; see gaps).
7. **TWELVE provisional/quarantined claims** — AMD/IREN/NBIS (`2026-08-04`) + GS (`2026-07-28`) + MS/PYPL
   (`2026-07-29`) + QCOM/SPCX/SYNA (`2026-07-21 OVERDUE`) + SKHY (`2026-07-24`) + RIVN (`2026-07-27`) + UNH
   (`2026-07-30`). Saturday research owns validation. Do NOT hand-promote.
8. **[LOW] Proportionality — tech/AI universe concentration.** NBIS/IREN/AMD are all AI/semis; the news agent's
   standing proportionality question is still unanswered. Operator awareness only.
