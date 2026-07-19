# Tasks for the next run

## ⚡ OPERATOR DIRECTIVE (2026-07-19) — SHORT-TERM TRANSITION IS LIVE

The harness has transitioned from holding longs to trading on a shorter
timeline (days to a few weeks — typically ~2-15 trading days; swing, not
day trading). **Read `manual.md` §"P1 — SHORT-TERM TRADING DOCTRINE"
before this run's workflow.** For you:
(1) do NOT sell META or anything else because of this — exits stay with the
owning strategy's rules, no calendar liquidations, ever; (2) weight the
brief's new `## Near-term catalyst calendar` section in meta-decisions;
(3) expect faster turnover ahead — reconcile every close from ACTUAL fill
prices; (4) rotation toward short-horizon strategies goes only through
triage/head-to-head (research owns the migration — log candidates, don't
re-claim). New prompt files (`daily_prompt_short_term.md` etc.) exist for
the operator to paste into the scheduled tasks; until that happens, this
note + the manuals carry the directive. Keep this block in `tasks.md`
until the operator confirms the new prompts are pasted, then drop it.

**✅ 7/16 COMPLETE (single fire, canonical 16:03, Thursday).** KEEP day on a real-but-orderly risk-off tape. Book
unchanged (**META only**, cash $94,690.29, no open orders, META **+9.89%** — gave back part of Wed's +12.43% with
the broad chip de-rate but still green/trending). **Nothing closed → no reconciliation.** News brief **FRESH &
on-time** (correctly dated 7/16); **NOTABLE — a genuine risk-off chip/semiconductor selloff, but orderly and NOT
halt-worthy** (Nasdaq -1.47%, S&P -0.51%, VIX +3.66% to 16.24, no >2% futures gap). The 7/16 stack (TSM "insanely
good" print that sold off ~6% on a $60-64B capex guide → broad chip de-rate; GOOGL -4% on a Gemini 3.5 Pro delay;
4th-session AI-hardware/memory give-back; 6th-day Iran/Hormuz) was a real down day but every material item was
`responder: NONE`. Cutting the other way: UNH blowout lifted the Dow, AAPL record high, firm macro (Philly Fed
41.4, claims 208K). Universe grew **36 → 37**: news promoted **UNH** (UnitedHealth Q2 blowout + raised FY26 guide;
a deliberate healthcare diversifier). UNH → `triage-symbol --gap-type earnings_window` → `equity_event_driven_
catalyst` below-baseline provisional (Sharpe 0.0/0 trades, degenerate-0-trade = issue #5), quarantined,
`revalidate_by 2026-07-30`. `cli execute` = clean no-op 0/0/0. See `last_handoff.md`. Replace this file (don't
append) when you write the next version.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.
Note: CLI prints a `safety_gate_initialized` structlog line to **stdout** before the JSON — pipe through
`grep '^{'` before parsing with python/jq.

## ⚠️ FRI 7/17 CONTEXT (informational — none of it makes the run different)
- **NFLX reported Q2 last night (7/16 AMC).** The news agent said it would promote NFLX today **on a confirmed
  beat-and-raise** (not on preview coverage). If NFLX (or any NEW name) shows up unclaimed, triage it (do NOT
  `add-active`).
- **No fresh earnings today.** Next cluster: TSLA 7/22, ARM/INTC 7/23, MSFT 7/29, AMZN 7/30. TSM printed 7/16
  (capex selloff, UNRESPONDED — it's on trend-following, not an earnings-window strategy).
- **Live tails:** (1) **AI-capex-doubt / chip de-rate** is now broad (foundry TSM + hardware DELL/SMCI/HPE + memory
  MU/SNDK + Oracle cash-burn 52-wk low) under a still-calm index (VIX 16.24) — a dispersion regime, not a panic.
  (2) **US-Iran/Hormuz is on its 6th day**, oil/yields up, forward gasoline pressure; both June inflation prints
  predate the oil spike. An overnight equity-futures gap **>2%** is the halt-worthy line — was NOT there 7/16
  (Nasdaq -1.47%, VIX 16.24). Positions ride their own rules regardless.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5
in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED
until Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a
below-baseline trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are
FORBIDDEN. Never use `cli add-active` to bypass triage.

## To do next run (Fri 7/17 — book stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-17; if
   not, treat as ABSENT, note the gap, fall back to the raw `news/daily_summary/2026-07-17.html` for a halt-worthy
   safety scan. **Run `cli market-status`**; note the run TIME. If it double-fires (a 2nd fire same day — the tell
   is a `[trader 2026-07-17]` commit already in git log + a handoff already narrating a completed 7/17 run), take
   NO action: don't re-execute, don't re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$105-106k (moves only on META's
     mark). No resting orders. If instead FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe →
     FREEZE (see playbook). Nothing is currently pending to close, so a rising-cash vanish is not expected.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 9` (GS `2026-07-28`;
   MS/PYPL `2026-07-29`; QCOM/SPCX/SYNA `2026-07-21`; SKHY `2026-07-24`; RIVN `2026-07-27`; **UNH `2026-07-30`**).
   All nine are ALREADY claimed/quarantined — do NOT re-triage them; research owns validation. Triage only any
   *new* unclaimed symbol (news agent may promote NFLX or another name). Do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's live
   claims (AVGO/MU/ORCL) are flat with no fresh *discrete single-name* entry catalyst → likely fires nothing.
   (ORCL made a 52-wk low 7/16 on cash-burn — a valuation move its rule doesn't read; its Japan-cloud story did NOT
   advance. A cohort de-rate/bounce is NOT a responder event.) Provisionals stay quarantined/skipped.
5. **Library gaps — see list below (Saturday 7/18 research owns them; TSM/UNH/MS/PYPL/RIVN/GS earnings/M&A already
   printed unresponded).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash
unchanged + vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL
`get_order` fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson in manual.md).

## Position watch

- **META (+9.89%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending). Gave back part of Wed's +12.43% run with the broad chip/tech de-rate but
  stayed green. Its 7/16 touchpoints ("Meta Compute" enterprise-cloud push + AI-debt-cohort mention + incidental
  Brazil-tariff cross-tag) are competitive/positioning noise, NOT an adverse single-name shock — do NOT hand-manage
  on those or any capex/regulatory/litigation headline; all informational (no responder).
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. ORCL's 7/16 52-wk low (cash-burn) is a
  valuation/sentiment move its rule doesn't read — not a directive to hand-manage.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/18)

All `responder: NONE` — informational, not tradable under the mandate. `gap-registry coverage_holes` is **empty**;
every item is an activation/assignment/taxonomy gap (a rule/event-type not mapped to the symbol that had the event):
- **Provisional/quarantined validations (TOP PRIORITY):** now **9** — on `equity_event_driven_catalyst`:
  **GS** (best-quarter print, `2026-07-28`), **MS** (record Q2, `2026-07-29`), **PYPL** ($53B M&A target,
  `2026-07-29`), **QCOM** (`2026-07-21`), **RIVN** (Q2 beat+raise, `2026-07-27`), **UNH** (Q2 blowout + raised
  guide, `2026-07-30`) — all degenerate-0-trade Sharpe-0.0 below-baseline trading provisionals. Plus **SKHY**
  (`equity_watch_only`; ADR premium + leveraged HYNX ETFs, no-history, `2026-07-24`), **SPCX**
  (`equity_trend_following_ema_cross`; no-history, sub-IPO-price, `2026-07-21`), **SYNA**
  (`equity_pairs_trading_cointegration`; onsemi merger-arb, `2026-07-21`). Validate/upgrade or archive each.
- **Earnings/print-window ASSIGNMENT gap (MOST ACUTE recurring — live example 7/16) — TSM (printed 7/16,
  capex-driven ~6% selloff, UNRESPONDED because it's on `equity_trend_following_ema_cross`), UNH (blowout,
  quarantined), MS/PYPL/RIVN/GS (quarantined), MSFT (7/29), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** These are
  claimed by trend-following / breakout / macd, NOT `equity_event_driven_catalyst` (unvalidated) /
  `long_straddle_earnings`. **TSM is the single most concrete live case** that an earnings-window print gets no
  responder when the name is on a trend-following claim. Reassign / activate an earnings-window responder on the
  names actually printing.
- **AI-capex / cash-burn re-rating + cohort sentiment reversal (DOMINANT theme 7/16) — TSM capex selloff (foundry
  layer), ORCL cash-burn 52-wk low, DELL/SMCI/HPE server give-back, MU/SNDK memory de-rate (4th session, now a
  sustained downtrend not a whipsaw); the $182B Big-Tech AI-debt-spree story (CDS spreads reportedly doubled).**
  No rule reads a cohort-wide capex-doubt/overbuild re-rating or a sustained cohort flow reversal. *Research: a
  cohort / sector-risk overlay that handles the capex-doubt regime.* (DELL is on `equity_sector_rotation_momentum`
  — may mechanically react, but nothing reads the overcapacity/capex-doubt narrative itself.)
- **Product / roadmap-event overlay — GOOGL Gemini 3.5 Pro delay (-4%); AAPL AI-chip-acquisition intent + record
  high; TSLA FSD legal clearance.** No rule reads a product launch/delay or a legal/regulatory clearance.
  *Research: a product/regulatory-event overlay.*
- **Analyst-action / valuation-downgrade shock (event-scale) — ARM -5% on a downgrade** (recurring: DELL -13% 7/15,
  ARM/HSBC -6% 7/14). Normally analyst opinion is dropped, but repeated event-scale single-name reactions argue for
  a filter that fires only when the move is event-scale. *Research: a rating-action / valuation-shock filter.*
- **M&A-target / merger-arb activation — PYPL ($53B Stripe/Advent offer, quarantined, no dev 7/16); AAPL
  chip-acquisition intent; RKLB(acquirer)/IRDM(target, $8B); SYNA/onsemi.** `equity_pairs_trading_cointegration`
  claims only SYNA; no merger-arb active. *Research: activate merger-arb / event-target handling; cointegration
  look on RKLB/IRDM.*
- **Short-seller / allegation event — BE short-seller allegations (7/16), despite a $1.7B AI-infra investment.** No
  rule reads a short-seller report or allegation disclosure. *Research: fold into the event/regulatory overlay.*
- **Index / forced-flow + ETF/float mechanics (recurring) — SKHY (Korea tripled leveraged-ETF cash margin after 24
  emergency halts in 9 weeks); Lucid 2x ETF delisted (NAV negative); SPCX sub-IPO-price with leveraged/inverse
  ETFs.** No `index_rebalance` gap_type exists. Argues for a 6th Tier-B trigger / forced-flow overlay
  (`NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`).
- **Binary-launch / space-catalyst — SPCX Starship Flight 13 (7/16 night, Starlink V3 payload).** No rule reads a
  binary launch outcome (SPCX is quarantined regardless). *Research: fold into the event-catalyst overlay.*
- **Vol-regime / dispersion activation (SHARP 7/16) — VIX 16.24 (low index vol) but extreme single-name dispersion
  (SOXX -13%/4wk, its Nasdaq-100 premium erased; SNDK -40% from peak; INTC ~-31% July); event-IV into NFLX
  (tonight), TSLA/ARM/INTC/MSFT/AMZN.** Options skeletons (`iron_condor_high_iv`, `long_straddle_earnings`,
  `jade_lizard`, `calendar_spread`) exist but none active / none claims a universe symbol. Dispersion, not index
  vol — screen single-name / event-IV.
- **Geopolitical / energy-shock overlay — US-Iran/Hormuz (6th day), oil/yields up, forward gasoline pressure; both
  cool June prints predate the oil spike; USTR 25% Section 301 tariff on Brazilian goods (eff. 7/22, payments-name
  watch item).** No rule reads an oil/geopolitical shock or a tariff action or its inflation/payments read-through.
  *Research: a macro/energy/policy-shock risk overlay.*
- **Tokenization / market-structure (carry from 7/15) — DTCC first live tokenized stocks & Treasurys.** Novel event
  type, no responder. `NEW_CATEGORY_NEEDED (market-structure / tokenization)`.
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right?
  Backtest the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **Fallback-threshold question (issue #5, fresh data point 7/16: UNH)** — no-price-history routes to
  `equity_watch_only` correctly (SKHY/SPCX). The open case is only the degenerate 0-trade Sharpe-0.0 backtest
  (UNH today; GS 7/14; MS/PYPL 7/15; RIVN 7/13; WULF/SMCI/RKLB/IRDM/BE historically) routing to a below-baseline
  *trading* provisional. Decide whether a 0-trade score should also route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Healthcare breadth — improved via UNH (7/16), still thin.** Universe healthcare is now UNH + NUVL. Awareness
  only (not a trade directive).

## Open questions for the operator

1. **[HIGH — timing] Confirm single-trigger schedule.** 7/7 & 7/8 double-fired; **7/9–7/16 fired once ✓** (six
   clean days running).
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/13-7/16 (briefs fresh & on-time),
   but the 7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden the news agent's
   brief-synthesis + git-sync so a weekend/late run can't leave a stale brief.
4. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
5. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (UNH is the newest instance; see gaps).
6. **NINE provisional/quarantined claims** — GS (`2026-07-28`) + MS/PYPL (`2026-07-29`) + QCOM/SPCX/SYNA
   (`2026-07-21`) + SKHY (`2026-07-24`) + RIVN (`2026-07-27`) + UNH (`2026-07-30`). Saturday research owns
   validation. Do NOT hand-promote.
7. **[LOW] BLK + ASML** still tracked, not promoted (neither recurred with a fresh hard catalyst 7/16). **NFLX**
   reported 7/16 AMC — news agent to promote 7/17 on a confirmed beat-and-raise. Operator awareness only.
