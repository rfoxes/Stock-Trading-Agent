# Tasks for the next run

**✅ 7/14 COMPLETE (single fire, canonical 16:03, Tuesday — the week's most event-dense day).** Quiet KEEP day. Book
unchanged (**META only**, cash $94,690.29, no open orders, META +8.88%). **Nothing closed → no reconciliation.**
News brief **FRESH & on-time** (correctly dated 7/14); NOTABLE-not-halt-worthy — the 7/14 stack (cool June CPI
3.5%/2.6% YoY both below consensus + JPM/GS bank blowouts + Warsh hawkish debut + US-Iran/Hormuz 3rd day) resolved
CONSTRUCTIVELY, tape closed green, VIX ~17. AI-memory cohort BOUNCED (reversed Mon's de-rate). Universe grew
**33 → 34**: news promoted **GS** (Goldman — best quarter ever, +6.9%; fills financials-breadth gap) →
`triage-symbol GS --gap-type earnings_window` → `equity_event_driven_catalyst` below-baseline provisional
(Sharpe 0.0/0 trades, degenerate-0-trade case = issue #5), quarantined, `revalidate_by 2026-07-28`. `cli execute` =
0 intents. See `last_handoff.md`. Replace this file (don't append) when you write the next version.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.

## ⚠️ WED 7/15 CONTEXT (informational — none of it makes the run different)
- **Warsh Senate testimony (7/15)** — the second half of his semi-annual (House was 7/14). Hawkish-measured tone
  last time; watch the brief for any forward-guidance shift.
- **TSM earnings Thu 7/16** — large options-implied move building; June revenue +67.9% YoY already disclosed.
  Window opens Thursday; earnings-window IV is live (informational for any options posture).
- **MS reports Wed 7/15** — a financials-breadth candidate (session 2 tracking; not promoted).
- **Live tail:** US-Iran/Hormuz is fluid & oil-sensitive; June CPI predates the oil spike (gasoline >$4/gal
  forward). An overnight equity-futures gap **>2%** would be the halt-worthy line — was NOT there 7/14 (green tape).
  Positions ride their own rules regardless.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5
in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED
until Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a
below-baseline trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are
FORBIDDEN. Never use `cli add-active` to bypass triage.

## To do next run (Wed 7/15 — book stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-15; if
   not, treat as ABSENT, note the gap, fall back to the raw `news/daily_summary/2026-07-15.html` for a halt-worthy
   safety scan. **Run `cli market-status`**; note the run TIME. If it double-fires (a 2nd fire same day — the tell
   is a `[trader 2026-07-15]` commit already in git log + a handoff already narrating a completed 7/15 run), take
   NO action: don't re-execute, don't re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$105k (moves only on META's mark).
     No resting orders. If instead FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe → FREEZE
     (see playbook). Nothing is currently pending to close, so a rising-cash vanish is not expected.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 6` (GS `revalidate_by
   2026-07-28`; QCOM/SPCX/SYNA `2026-07-21`; SKHY `2026-07-24`; RIVN `2026-07-27`). All six are ALREADY
   claimed/quarantined — do NOT re-triage them; research owns validation. Triage only any *new* unclaimed symbol
   (the news agent may promote a bank peer like MS, a memory-cohort/IPO name). Do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's live
   claims (AVGO/MU/ORCL) are flat with no fresh *discrete single-name* entry catalyst → likely fires nothing (a
   cohort bounce/de-rate is NOT a responder event). Provisionals stay quarantined/skipped.
5. **Library gaps — see list below (Saturday 7/18 research owns them; JPM & GS earnings already printed
   unresponded; TSM opens 7/16).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash
unchanged + vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL
`get_order` fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson in manual.md).

## Position watch

- **META (+8.88%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending). Ticked up with the 7/14 semis-cohort bounce. Its only 7/14 touchpoint was
  the NY 50MW data-center freeze (a mild, SHARED capex/permitting headwind, also hitting MSFT/AMZN/GOOGL) — do NOT
  hand-manage on that or any capex/regulatory headline; all informational (no responder).
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. The 7/14 cohort bounce is NOT such a catalyst.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/18)

All `responder: NONE` — informational, not tradable under the mandate. `gap-registry coverage_holes` is **empty**;
every item is an activation/assignment/taxonomy gap (a rule/event-type not mapped to the symbol that had the event):
- **Provisional/quarantined validations (TOP PRIORITY):** now **6** — GS (event-driven; best-quarter-ever print,
  degenerate 0-trade backtest, `revalidate_by 2026-07-28`) — QCOM (event-driven), SPCX (trend-following,
  lockup/float), SYNA (pairs, onsemi merger-arb) — all `2026-07-21` — SKHY (`equity_watch_only`; ADR ~50% premium
  to Seoul + 2×-leveraged HYNX ETF launched 7/14, real bars accruing, `2026-07-24`) — RIVN (event-driven; 75M-share
  dilutive offering, degenerate 0-trade, `2026-07-27`). Validate/upgrade or archive each.
- **Earnings/print-window ASSIGNMENT gap (MOST ACUTE recurring) — JPM (printed 7/14, +41%, UNRESPONDED), GS
  (printed 7/14, best-ever, UNRESPONDED), TSM (opens 7/16), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** All
  claimed by trend-following / breakout, NOT `equity_event_driven_catalyst` / `long_straddle_earnings`. TWO
  blowout prints just went unresponded; TSM's large-implied-move window opens Thursday. Reassign or activate a
  straddle on the cluster.
- **Sector / cohort sentiment reversal (BIDIRECTIONAL, refreshed 7/14) — the AI-memory de-rate (7/13) → REBOUND
  (7/14; hedge funds bought US semis fastest in 3.5yr).** No rule reads a cohort-wide flow/sentiment swing in
  EITHER direction (Samsung guidance down-leg, then hedge-fund-buying up-leg). *Research: a cohort/sector risk
  overlay that handles both directions.*
- **Regulatory / export-control commercial action (NEW) — NVDA cut >half its Asian AI-chip customers on tighter
  China export screening.** No rule reads an export-control-driven demand action. *Research: a regulatory/policy
  overlay (also covers AAPL litigation carry, META EU DSA carry).*
- **Policy / capex-headwind (refreshed 7/14) — NY freezing new 50MW+ AI data centers up to a year (grid strain;
  META/MSFT/AMZN/GOOGL).** First state-level siting brake. No rule reads a permitting/grid brake on the capex
  thesis. *Research: a capex/policy overlay (pairs with prior META Hyperion / MU reshoring capex gap).*
- **Index / forced-flow + ETF/float mechanics (recurring) — SKHY ADR ~50% premium + 2×-leveraged HYNX ETF launch
  (7/14); SPCX lockup/float carry.** No `index_rebalance` gap_type exists. Argues for a 6th Tier-B trigger /
  forced-flow overlay (`NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`).
- **Product/engineering-milestone (NEW) — RKLB Neutron AVac engine full-duration hot-fire test passed; NVDA Vera
  Rubin roadmap slip; TSLA Optimus line carry.** No rule reads an engineering/qualification milestone. *Research:
  a product-catalyst overlay.* (RKLB is on breakout — would mechanically respond only IF the milestone triggers a
  volume-confirmed breakout, but nothing reads the milestone itself.)
- **Geopolitical / energy-shock overlay — US-Iran Hormuz (3rd day), oil at 1-month high, gasoline >$4/gal
  forward.** No rule reads an oil/geopolitical shock or its inflation read-through. *Research: a macro/energy-shock
  risk overlay.*
- **Capital-allocation / capex overlay (recurring) — META Hyperion $50B+ + AI-API pricing; MU/Micron $6.9B
  reshoring; Lutnick pressing Samsung/SK Hynix on US fabs.** No rule reads a multi-year capex/reshoring/pricing
  move. *Research: a capex/capital-allocation overlay AND a re-entry rule for event_driven_catalyst.*
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right?
  Backtest the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **M&A-arb activation — RKLB (acquirer) / IRDM (target, $54/sh, $8B deal) + SYNA/onsemi (carry).**
  `equity_pairs_trading_cointegration` declares pairs_arbitrage but claims only SYNA; RKLB/IRDM pair unmodeled
  (both currently breakout). Cointegration look on RKLB/IRDM if breakout decays.
- **Vol-regime activation — orderly VIX ~17 but WIDE single-name dispersion (GS +6.9% / SNDK +5% vs ARM -6%);
  Goldman flags one of the worst 3-week S&P momentum-factor drawdowns on record; event-IV into TSM (7/16) +
  7/22-30 run.** Options structures (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`,
  `calendar_spread`) exist but none active / none claims a universe symbol. Dispersion, not index vol — screen
  single-name / event-IV.
- **Activist-short / short-call — BE Hunterbrook reports (ongoing, contested); INTC JPMorgan Q3 short-call
  (carry).** No responder reads a short report or its rebuttal.
- **Fallback-threshold question (issue #5, fresh GS data point 7/14)** — no-price-history routes to
  `equity_watch_only` correctly (SKHY). The open case is only the degenerate 0-trade Sharpe-0.0 backtest
  (GS today; RIVN 7/13; WULF/SMCI/RKLB/IRDM/BE historically) routing to a below-baseline *trading* provisional.
  Decide whether a 0-trade score should also route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Financials breadth — improved via GS (7/14) but still thin.** GS + JPM now in the universe; BAC/C/WFC reported
  7/14 in cohort coverage, MS reports 7/15. Operator/news may consider promoting a bank peer for further breadth
  (not auto-promoted — cohort earnings, not dedicated single-name catalysts yet).

## Open questions for the operator

1. **[HIGH — timing] Confirm single-trigger schedule.** 7/7 & 7/8 double-fired; **7/9, 7/10, 7/13, 7/14 fired once ✓.**
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/13 or 7/14 (briefs fresh &
   on-time), but the 7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden the news agent's
   brief-synthesis + git-sync so a weekend/late run can't leave a stale brief.
4. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
5. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (GS is the newest instance; see gaps).
6. **SIX provisional/quarantined claims** — GS (`2026-07-28`) + QCOM/SPCX/SYNA (`2026-07-21`) + SKHY (`2026-07-24`)
   + RIVN (`2026-07-27`). Saturday research owns validation. Do NOT hand-promote.
