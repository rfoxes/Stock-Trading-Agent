# Tasks for the next run

**✅ 7/15 COMPLETE (single fire, canonical 16:03, Wednesday).** Quiet KEEP day. Book unchanged (**META only**,
cash $94,690.29, no open orders, META **+12.43%**). **Nothing closed → no reconciliation.** News brief **FRESH &
on-time** (correctly dated 7/15); NOTABLE-not-halt-worthy — the 7/15 stack (cool June PPI -0.3% MoM/5.5% YoY below
consensus + Empire State beat 15.6 + MS record Q2 + BLK beat + DTCC tokenization go-live + AAPL China/NVDA H200
regulatory unlocks) resolved CONSTRUCTIVELY, tape closed green, VIX fell to ~15.67. A sharp AI-hardware/memory
give-back ran underneath (DELL -13%, memory -3-8%) but index stayed calm. Universe grew **34 → 36**: news promoted
**MS** (Morgan Stanley record Q2; completes JPM+GS+MS bulge-bracket cohort) + **PYPL** (PayPal $53B Stripe/Advent
M&A target). Both → `triage-symbol` → `equity_event_driven_catalyst` below-baseline provisionals (Sharpe 0.0/0
trades each, degenerate-0-trade = issue #5), quarantined, both `revalidate_by 2026-07-29`. `cli execute` = 0
intents. See `last_handoff.md`. Replace this file (don't append) when you write the next version.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.

## ⚠️ THU 7/16 CONTEXT (informational — none of it makes the run different)
- **TSM earnings Thu 7/16** — window OPENS today; large options-implied move; June revenue +67.9% YoY already
  disclosed. Earnings-window IV is live (informational for any options posture). TSM is claimed by
  `equity_trend_following_ema_cross`, NOT an event/straddle strategy → likely no responder (recurring assignment gap).
- **Bank/broker season is DONE** (MS/BLK capped it 7/15). Next earnings cluster: TSLA 7/22, ARM/INTC 7/23, AMZN 7/30.
- **Live tails:** (1) US-Iran/Hormuz is fluid & oil-sensitive; BOTH cool June prints (CPI 7/14, PPI 7/15) predate
  the oil spike (forward gasoline pressure). An overnight equity-futures gap **>2%** would be the halt-worthy line —
  was NOT there 7/15 (green tape, VIX 15.67). (2) AI-hardware/memory dispersion is sharp under a calm index (third
  memory direction-change in three sessions). Positions ride their own rules regardless.
- **BLK + ASML** were flagged Tier-0-eligible but held by the news agent for proportionality 7/15 — the news agent
  may promote one/both next run. If a NEW unclaimed symbol appears, triage it (do NOT `add-active`).

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5
in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED
until Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a
below-baseline trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are
FORBIDDEN. Never use `cli add-active` to bypass triage.

## To do next run (Thu 7/16 — book stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-16; if
   not, treat as ABSENT, note the gap, fall back to the raw `news/daily_summary/2026-07-16.html` for a halt-worthy
   safety scan. **Run `cli market-status`**; note the run TIME. If it double-fires (a 2nd fire same day — the tell
   is a `[trader 2026-07-16]` commit already in git log + a handoff already narrating a completed 7/16 run), take
   NO action: don't re-execute, don't re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$105-106k (moves only on META's
     mark). No resting orders. If instead FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe →
     FREEZE (see playbook). Nothing is currently pending to close, so a rising-cash vanish is not expected.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 8` (GS `revalidate_by
   2026-07-28`; **MS/PYPL `2026-07-29`**; QCOM/SPCX/SYNA `2026-07-21`; SKHY `2026-07-24`; RIVN `2026-07-27`). All
   eight are ALREADY claimed/quarantined — do NOT re-triage them; research owns validation. Triage only any *new*
   unclaimed symbol (news agent may promote BLK/ASML or another name). Do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's live
   claims (AVGO/MU/ORCL) are flat with no fresh *discrete single-name* entry catalyst → likely fires nothing.
   (Watch ORCL — the 7/15 brief tagged its Japan-gov cloud contract as the one "clean responder" IF the strategy
   fires an entry; it did NOT fire 7/15. A cohort give-back/bounce is NOT a responder event.) Provisionals stay
   quarantined/skipped.
5. **Library gaps — see list below (Saturday 7/18 research owns them; MS/PYPL/RIVN/GS earnings/M&A already printed
   unresponded; TSM opens 7/16).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash
unchanged + vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL
`get_order` fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson in manual.md).

## Position watch

- **META (+12.43%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending). Extended with the 7/15 mega-cap platform rally. Its 7/15 touchpoints (an
  AI-layoff-discrimination lawsuit + a surplus-AI-capacity-leasing report) are litigation/monetization noise, NOT
  an adverse single-name shock — do NOT hand-manage on those or any capex/regulatory/litigation headline; all
  informational (no responder).
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. ORCL's 7/15 Japan-gov-cloud contract was tagged a
  potential responder but the strategy fired no entry — not a directive to hand-manage.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/18)

All `responder: NONE` — informational, not tradable under the mandate. `gap-registry coverage_holes` is **empty**;
every item is an activation/assignment/taxonomy gap (a rule/event-type not mapped to the symbol that had the event):
- **Provisional/quarantined validations (TOP PRIORITY):** now **8** — on `equity_event_driven_catalyst`:
  **GS** (best-quarter print, `2026-07-28`), **MS** (record Q2, `2026-07-29`), **PYPL** ($53B M&A target,
  `2026-07-29`), **QCOM** (`2026-07-21`), **RIVN** (Q2 beat+raise, `2026-07-27`) — all degenerate-0-trade Sharpe-0.0
  below-baseline trading provisionals. Plus **SKHY** (`equity_watch_only`; ADR premium + leveraged HYNX ETFs,
  no-history, `2026-07-24`), **SPCX** (`equity_trend_following_ema_cross`; no-history, sub-IPO-price, `2026-07-21`),
  **SYNA** (`equity_pairs_trading_cointegration`; onsemi merger-arb, `2026-07-21`). Validate/upgrade or archive each.
- **Earnings/print-window ASSIGNMENT gap (MOST ACUTE recurring) — MS (record Q2, UNRESPONDED), PYPL (M&A target,
  UNRESPONDED), RIVN (Q2 beat+raise 7/15, UNRESPONDED — quarantined), GS (52-wk high follow-through, quarantined),
  TSM (opens 7/16), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** These are claimed by trend-following / breakout,
  NOT `equity_event_driven_catalyst` (unvalidated) / `long_straddle_earnings`. **RIVN's beat-and-raise went
  unresponded specifically because its event-strategy claim is execution-quarantined — a concrete case that a
  quarantined event-strategy still leaves the earnings-window uncovered.** Reassign or activate a straddle on the
  cluster.
- **M&A-target / merger-arb activation (refreshed 7/15) — PYPL ($53B Stripe/Advent offer, unclaimed→provisional);
  RKLB(acquirer)/IRDM(target, $8B); SYNA/onsemi (carry).** `equity_pairs_trading_cointegration` claims only SYNA;
  no merger-arb active. *Research: activate merger-arb / event-target handling; cointegration look on RKLB/IRDM.*
- **Regulatory approval / export-control commercial action (refreshed 7/15) — AAPL China Apple-Intelligence
  approval (+4% record high); NVDA H200-to-China clearance (+4%).** No rule reads a regulatory approval/export
  action. *Research: a regulatory/policy-event overlay (also covers AAPL/META litigation carry, NVDA China).*
- **Sector/cohort sentiment reversal (bidirectional) + AI-hardware overcapacity (SHARP 7/15) — memory whipsaw
  (3 direction-changes in 3 sessions: Mon down/Tue up/Wed down); AI-hardware give-back (DELL -13%, HPE/SMCI
  sympathy, memory -3-8%).** No rule reads a cohort-wide flow/sentiment swing or an overcapacity/margin re-rate in
  EITHER direction. *Research: a cohort/sector risk overlay that handles both directions.*
- **Analyst-action / valuation-downgrade shock (NEW 7/15) — DELL GF Securities cut → -13% (a downgrade producing an
  event-scale move); recurring (ARM HSBC -6% on 7/14).** Normally analyst opinion is dropped, but a 13% single-name
  reaction is event-scale. *Research: a rating-action / valuation-shock filter (only when the move is event-scale).*
- **Tokenization / market-structure (NEW 7/15) — DTCC first live tokenized stocks & Treasurys (JPM/GS/BLK/Vanguard
  +~40 institutions).** Novel event type, no responder. `NEW_CATEGORY_NEEDED (market-structure / tokenization)`.
- **Product/engineering-milestone (refreshed 7/15) — INTC first to deploy ASML High-NA EUV; NVDA Vera Rubin
  roadmap (delay dismissed); RKLB Neutron hot-fire carry.** No rule reads an engineering/qualification milestone.
  *Research: a product-catalyst overlay.* (INTC is on breakout — responds only IF the milestone drives a
  volume-confirmed breakout, but nothing reads the milestone itself.)
- **Index / forced-flow + ETF/float mechanics (recurring) — SKHY thin-float ADR whipsawed by 4 leveraged SK Hynix
  ETFs; SPCX sub-IPO-price with leveraged/inverse/covered-call ETFs.** No `index_rebalance` gap_type exists.
  Argues for a 6th Tier-B trigger / forced-flow overlay (`NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`).
- **Policy / capex-headwind (refreshed 7/15) — NY 50MW data-center freeze (carry); Meta surplus-AI-capacity leasing
  report (overcapacity signal that spooked server integrators).** No rule reads a permitting/grid brake or an
  overcapacity policy signal on the capex thesis. *Research: a capex/policy overlay.*
- **Geopolitical / energy-shock overlay — US-Iran/Hormuz (3rd night), oil near one-month highs, forward gasoline
  pressure; both cool June prints predate the oil spike.** No rule reads an oil/geopolitical shock or its inflation
  read-through. *Research: a macro/energy-shock risk overlay.*
- **Vol-regime activation (SHARP 7/15) — VIX ~15.67 (low index vol) but WIDE single-name dispersion (mega-cap
  platforms +3-4% vs DELL -13% / memory -3-8%); event-IV into TSM (7/16) + 7/22-30 run (TSLA/ARM/INTC/AMZN).**
  Options skeletons (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) exist but
  none active / none claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **Activist-short / short-call — BE Hunterbrook reports (ongoing, contested); INTC JPMorgan Q3 short-call
  (carry).** No responder reads a short report or its rebuttal.
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right?
  Backtest the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **Fallback-threshold question (issue #5, TWO fresh data points 7/15)** — no-price-history routes to
  `equity_watch_only` correctly (SKHY/SPCX). The open case is only the degenerate 0-trade Sharpe-0.0 backtest
  (MS + PYPL today; GS 7/14; RIVN 7/13; WULF/SMCI/RKLB/IRDM/BE historically) routing to a below-baseline *trading*
  provisional. Decide whether a 0-trade score should also route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Financials breadth — now GOOD via JPM+GS+MS (full bulge-bracket cohort as of 7/15); PYPL adds fintech/M&A.**
  BLK flagged Tier-0-eligible (Q2 beat + DTCC settlement) but held for proportionality 7/15 — news agent may
  promote next run. Operator/news awareness only (not auto-promoted).

## Open questions for the operator

1. **[HIGH — timing] Confirm single-trigger schedule.** 7/7 & 7/8 double-fired; **7/9, 7/10, 7/13, 7/14, 7/15
   fired once ✓** (five clean days running).
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/13-7/15 (briefs fresh & on-time),
   but the 7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden the news agent's
   brief-synthesis + git-sync so a weekend/late run can't leave a stale brief.
4. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
5. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (MS + PYPL are the newest instances; see gaps).
6. **EIGHT provisional/quarantined claims** — GS (`2026-07-28`) + MS/PYPL (`2026-07-29`) + QCOM/SPCX/SYNA
   (`2026-07-21`) + SKHY (`2026-07-24`) + RIVN (`2026-07-27`). Saturday research owns validation. Do NOT
   hand-promote.
7. **[LOW] BLK + ASML** flagged Tier-0-eligible but held by the news agent 7/15 for proportionality — awareness
   only; news agent may promote next run.
