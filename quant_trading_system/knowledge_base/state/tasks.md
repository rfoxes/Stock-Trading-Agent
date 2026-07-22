# Tasks for the next run

**✅ 7/22 COMPLETE (single fire, canonical 16:03, Wednesday).** KEEP day on a mild, oil-pressured risk-off tape.
Book unchanged (**META only**, cash $94,690.29, no open orders, META **+2.59%** — down from 7/21's +5.84% on the
pullback, still green/trending). **Nothing closed → no reconciliation.** News brief **FRESH & on-time** (correctly
dated 7/22); **NOTABLE — an event-dense but orderly, oil-pressured risk-off session, NOT halt-worthy** (Nasdaq
−0.6%, S&P ~flat, VIX ~17, no >2% futures gap). Drivers: **GOOGL beat AMC** (Cloud +82%, "demand outpaces capacity")
+ **TSLA mixed AMC** (rev beat, EPS miss, net income −57%) — **neither a held name**; fresh **Houthi Red Sea /
Bab-el-Mandeb blockade → oil +3–3.4%** (Brent ~$94). Universe **unchanged at 40 — NO promotions** → **no triage this
run**. `unclaimed_count 0`, `provisional_count 12` (unchanged, all quarantined). `cli execute` = clean no-op 0/0/0,
all 12 provisionals skipped. See `last_handoff.md`. Replace this file (don't append) when you write the next version.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.
Note: CLI prints a `safety_gate_initialized` structlog line to **stdout** before the JSON — pipe through
`grep '^{'` before parsing with python/jq.

## ⚠️ THU 7/23 CONTEXT (informational — INTC/ARM print, but none of it changes your run)
- **INTC + ARM report Q2 tonight (7/23 AMC).** INTC is on `equity_breakout_volume_confirmation` (7 straight rev beats;
  fresh Data-Center/AI layoffs; SK-Hynix denied buying its Ohio campus); ARM is claimed too — **neither is an
  earnings-window responder** → both prints will be UNRESPONDED (the acute recurring earnings-window gap). This is
  informational; you have no earnings-window responder to act on. If the news agent promotes any NEW name off a
  reaction, triage it (do NOT `add-active`).
- **Earnings cluster ahead:** INTC/ARM 7/23 AMC, **MSFT + META 7/29**, AMZN/AAPL 7/30, AMD/SPCX 8/4. GOOGL/TSLA
  printed 7/22 AMC (both UNRESPONDED, both on `trend_following`). SMCI full audited report Aug 11.
- **Live tails:** (1) **Houthi Red Sea blockade** — oil elevated (Brent +3.4% ~$94, WTI +3% ~$87); a >2% overnight
  equity-futures gap is the halt-worthy line — was NOT there 7/22. Watch for escalation (full Bab-el-Mandeb closure =
  ~7% of global supply). (2) **AI-capex-doubt** persists even after GOOGL's strong print — a dispersion regime (SMCI
  +26% vs SNDK down under VIX ~17), not a panic. (3) **China chip-manufacturing curbs** (TSM/QCOM); USTR 25% Brazil
  tariff (eff. 7/22); Bessent Chinese-AI-sanctions threat. Positions ride their own rules regardless.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5 in
triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED until
Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a below-baseline
trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]`
for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are FORBIDDEN. Never use
`cli add-active` to bypass triage.

## To do next run (Thu 7/23 — book stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-23; if
   not, treat as ABSENT, note the gap, fall back to the raw `news/daily_summary/2026-07-23.html` for a halt-worthy
   safety scan (esp. any escalation of the Houthi/oil shock into a >2% futures gap). **Run `cli market-status`** +
   `git log --oneline -5`; note the run TIME. If it double-fires (a 2nd fire same day — tell is a `[trader
   2026-07-23]` commit already in git log + a handoff already narrating a completed 7/23 run), take NO action: don't
   re-execute, don't re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$104k (moves only on META's mark).
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
   acute, live again 7/22 with real GOOGL+TSLA prints and again 7/23 with INTC/ARM).**
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

- **META (+2.59%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending green). Gave back part of its run on the 7/22 oil-pressured pullback but held
  green. Its only 7/22 item — France's under-15 social-media ban (cross-listed SNAP/RDDT/X) — is modest/not
  adverse-major → do NOT hand-manage on it or any capex/regulatory/positioning headline; all informational (no
  responder). **META Q2 is 7/29** (on `momentum_macd`, not an earnings-window responder → the print itself will be
  unresponded).
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. ORCL's continued data-center-cost/OpenAI-exposure
  pressure (commentary, carry from the cash-burn story) is not a directive to hand-manage.

## Library gaps + research items (carry to research_tasks.md — Saturday, if research runs)

All `responder: NONE` — informational, not tradable under the mandate. `gap-registry coverage_holes` is **empty**;
every item is an activation/assignment/taxonomy gap (a rule/event-type not mapped to the symbol that had the event):
- **Provisional/quarantined validations (TOP PRIORITY):** **12** — all on `equity_event_driven_catalyst` except as
  noted: **AMD** (MS AI deal, `2026-08-04`), **IREN** ($2.8B contracts + >$4B guide, `2026-08-04`), **NBIS** (NVDA
  9.3% stake, `2026-08-04`), **GS** (`2026-07-28`), **MS** (`2026-07-29`), **PYPL** ($53B M&A target, `2026-07-29`),
  **QCOM** (`2026-07-21 OVERDUE`), **RIVN** (Q2 beat+raise, `2026-07-27`), **UNH** (Q2 blowout, `2026-07-30`) — all
  degenerate-0-trade Sharpe-0.0 below-baseline trading provisionals. Plus **SKHY** (`equity_watch_only`; no-history,
  `2026-07-24` — Friday, will overdue if Sat 7/25 research misses), **SPCX** (`equity_trend_following_ema_cross`;
  no-history, `2026-07-21 OVERDUE`; SpaceX set first public earnings Aug 4), **SYNA** (`equity_pairs_trading_
  cointegration`; onsemi merger-arb, `2026-07-21 OVERDUE`). Validate/upgrade or archive each. **QCOM/SPCX/SYNA are
  OVERDUE** (missed the dropped 7/18 research run) — clear them first.
- **Earnings/print-window ASSIGNMENT gap (MOST ACUTE recurring — now with REAL PRINTS in hand: GOOGL beat 7/22 AMC +
  TSLA mixed 7/22 AMC both UNRESPONDED (both on `trend_following`); SMCI +26% 7/22 second-session UNRESPONDED (on
  `mean_reversion_bollinger`); TSM 7/16 capex selloff UNRESPONDED). Upcoming: INTC/ARM 7/23 AMC, MSFT/META 7/29,
  AMZN/AAPL 7/30, AMD/SPCX 8/4; plus quarantined GS/MS/PYPL/QCOM/RIVN/UNH.** These prints are claimed by
  trend-following / breakout / mean-reversion / macd, NOT `equity_event_driven_catalyst` (unvalidated) /
  `long_straddle_earnings`. **Reassign / activate an earnings-window responder on the names actually printing.**
  Single strongest research priority.
- **Cohort / sector-momentum activation (BIDIRECTIONAL) — GOOGL Cloud +82% "demand outpaces capacity" re-rated the
  neocloud cohort (IREN/NBIS/WULF/CoreWeave AH); Taiwan June export orders +59.4% record ($95.26B) reaffirmed the
  AI-supercycle vs the same-day chip cooldown; the AI-capex credit-event fear is still the #1 tail (Cuban/Burry/
  Warren).** No rule reads a cohort-wide capex re-rating in *either* direction (`sector_rotation_momentum` claims only
  DELL). *Research: a cohort / sector-risk overlay handling both the de-rate and the re-rate.*
- **Contract-win event — RKLB's confirmed $266M Space Force contract (on `breakout_volume_confirmation`, reads
  price/volume not awards).** No rule reads a contract award. *Research: a contract/award responder.*
- **Partnership / product event — CBRS–CrowdStrike AI-security partnership; GOOGL/AI-infra read-through.** No rule
  reads a named partnership/product launch. *Research: a partnership/product-event overlay.*
- **Strategic-corporate / capex / M&A-rumor events — NVDA's 9.3% Nebius stake; AMD's Microsoft AI deal; PYPL ($53B M&A
  target, quarantined); SYNA/onsemi; SPCX (Aug-4 first public earnings, 1-GW data-center plan, $52B Foxconn-deal
  denial); INTC (SK-Hynix Ohio-buyout denial).** No rule reads an equity stake, capex plan, earnings-date set, or
  M&A-rumor denial. *Research: an event/M&A/stake overlay; cointegration look for merger-arb.*
- **Regulatory / policy overlay — France under-15 social-media ban (META); Warren data-center-oversight push; Bessent
  Chinese-AI-sanctions threat; China chip-manufacturing curbs (TSM/QCOM); USTR 25% Brazil tariff; TSM ~10% price
  hike.** No rule reads a regulatory/export-control/tariff/pricing shift. *Research: a policy/regulatory-event
  overlay.*
- **Geopolitical / energy-shock overlay — Houthi Red Sea / Bab-el-Mandeb blockade (oil +3–3.4%, Brent ~$94),
  inflation read-through into the 7/28–29 FOMC.** No rule reads an oil/geopolitical shock. *Research: a macro/
  energy-shock risk overlay.* **Escalation-watch: a full Bab-el-Mandeb closure strands ~7% of global supply.**
- **Analyst / valuation-shock (event-scale) — BlackRock "memory rout overdone" (MU/SNDK); BofA Nvidia-vs-AMD $170B
  server-CPU note; BE JPMorgan PT raise (carry).** Recurring event-scale analyst reactions; normally dropped, but
  repeated scale argues for a filter that fires only on event-scale moves. *Research: a rating-action / valuation-
  shock filter.*
- **Index / forced-flow + ETF/float mechanics — SPCX share unlock ahead; SKHY (Korea leveraged-ETF margin, carry).**
  No `index_rebalance` gap_type exists. Argues for a 6th Tier-B trigger / forced-flow overlay (`NEW_CATEGORY_NEEDED
  (index_rebalance / float mechanics)`).
- **Vol-regime / dispersion activation (persistent) — VIX ~17 with extreme single-name dispersion (SMCI +26% vs SNDK
  down); dense event IV into INTC/ARM 7/23, MSFT/META 7/29, AMZN/AAPL 7/30, AMD/SPCX 8/4.** Options skeletons
  (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) exist but none active / none
  claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right? Backtest
  the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **Fallback-threshold question (issue #5)** — no-price-history routes to `equity_watch_only` correctly (SKHY/SPCX).
  The open case is the degenerate 0-trade Sharpe-0.0 backtest (AMD/IREN/NBIS 7/21; UNH 7/16; GS 7/14; MS/PYPL 7/15;
  RIVN 7/13) routing to a below-baseline *trading* provisional. Decide whether a 0-trade score should route to
  watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Healthcare breadth — still thin (UNH + NUVL).** Awareness only (not a trade directive).

## Open questions for the operator

1. **[HIGH — timing] Schedule reliability — both failure modes seen, now apparently recovered.** 7/7 & 7/8
   double-fired; 7/9–7/16 clean; **7/17, 7/20, Sat 7/18 DROPPED**; **7/21 + 7/22 both fired on time ✓**. Schedule
   appears recovered — confirm single-trigger + no-drop config is stable.
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[HIGH — carry] Overdue provisionals + skipped research.** QCOM/SPCX/SYNA overdue (`revalidate_by 7/21`, no Sat
   7/18 research); **SKHY hits `7/24` this Friday** and overdues if Sat 7/25 also misses. The provisional book (12)
   only shrinks when research validates/archives — if research keeps missing, add a trader escalation path.
4. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/21 or 7/22 (both fresh & on-time),
   but the 7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden brief-synthesis + git-sync.
5. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
6. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (AMD/IREN/NBIS + UNH/GS/MS/PYPL/RIVN; see gaps).
7. **TWELVE provisional/quarantined claims** — AMD/IREN/NBIS (`2026-08-04`) + GS (`2026-07-28`) + MS/PYPL
   (`2026-07-29`) + QCOM/SPCX/SYNA (`2026-07-21 OVERDUE`) + SKHY (`2026-07-24`) + RIVN (`2026-07-27`) + UNH
   (`2026-07-30`). Saturday research owns validation. Do NOT hand-promote.
8. **[LOW] Proportionality — tech/AI universe concentration.** NBIS/IREN/AMD all AI/semis; off-theme beats
   (T/COF/MCO/CME) noted 7/22 but not added. The news agent's standing proportionality question is still unanswered.
   Operator awareness only.
