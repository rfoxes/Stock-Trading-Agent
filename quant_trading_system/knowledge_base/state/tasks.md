# Tasks for the next run

**✅ 7/10 COMPLETE (single fire, canonical 16:03).** Quiet KEEP day. Book unchanged (**META only**, cash
$94,690.29, no open orders). **Nothing closed → no reconciliation.** News pipeline half-ran (raw HTML written, but
`state/news_brief.md` stayed dated 7/9 + no `[news 2026-07-10]` commit) → treated the brief as ABSENT, fell back
to raw `daily_summary/2026-07-10.html` (NOTABLE-not-halt-worthy). Universe grew **31 → 32**: news promoted **SKHY**
(SK Hynix debut) → `triage-symbol SKHY` → `equity_watch_only`, quarantined, `revalidate_by 2026-07-24`.
`cli execute` = 0 intents. See `last_handoff.md`. Replace this file (don't append) when you write the next version.

**NOTE: next trader run is MONDAY 7/13** (7/10 was Friday; Sat 7/11 = research agent). No trader run Sat/Sun.

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

## To do next run (Mon 7/13 — normal day, book stable; JPM earnings 7/14 is the near catalyst)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-13; if
   not (as happened 7/10), treat as ABSENT, note the gap, and fall back to the raw `news/daily_summary/2026-07-13.html`
   for a halt-worthy safety scan. **Run `cli market-status`**; note the run TIME. If it double-fires (a 2nd fire
   same day), take NO action — this book has no resting orders, so re-execute risks little, but still don't
   re-execute or re-triage.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$105k (moves only on META's mark).
     No resting orders. If instead FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe → FREEZE
     (see playbook). Nothing is currently pending to close, so a rising-cash vanish is not expected.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 5` (QCOM/SPCX/SYNA
   `revalidate_by 2026-07-21`; WULF `2026-07-23`; **SKHY** `equity_watch_only` `2026-07-24`). **SKHY begins
   regular-way trading Mon 7/13** under its permanent ticker — it's ALREADY claimed (watch_only/quarantined), so do
   NOT re-triage it; research owns validation by 7/24. Triage only any *new* unclaimed symbol (the news agent may
   promote more memory-cohort / IPO names). Do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's live
   claims (AVGO/MU/ORCL) are flat with no fresh entry catalyst → likely fires nothing. Provisionals stay
   quarantined/skipped.
5. **Library gaps — see list below (Saturday 7/11 research owns them).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash
unchanged + vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL
`get_order` fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson in manual.md).

## Position watch

- **META (+10.4%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit (not triggered — still trending). Got BOTH a *positive* AI-capex memo (Muse Spark 1.1, in-house "Iris" chip)
  AND a *preliminary* EU DSA action (fines up to 6% of rev, "may breach") on 7/10 — stock closed up; both are
  informational (no responder). Do not hand-manage on the regulatory headline.
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. event_driven_catalyst still *claims* them (claim ≠
  position); re-enters only on a fresh modeled catalyst.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/11)

All `responder: NONE` — informational, not tradable under the mandate. Carried from 7/9 + new 7/10 items:
- **Provisional/quarantined validations (TOP PRIORITY):** now **5** — QCOM (event-driven), SPCX (trend-following,
  Nasdaq-100 forced-flow), SYNA (pairs, onsemi merger-arb) — all `revalidate_by 2026-07-21` — **WULF** (event-driven;
  Anthropic $19B lease, `2026-07-23`) — plus **SKHY** (`equity_watch_only`; SK Hynix, `2026-07-24`; will have real
  bars from 7/13 onward — first backtestable window). Validate/upgrade or archive each.
- **Index-inclusion / forced-flow / IPO liquidity-rotation (NEW instance, recurring) — SK Hynix (SKHY) $26.5B
  Nasdaq debut (largest-ever foreign US IPO); "IPO liquidity drain from US memory names, Micron cracking"; carry
  SPCX Nasdaq-100 + BlackRock QQQ-challenger ETF.** No rule reads index-inclusion / forced-flow / IPO-rotation
  mechanics. Taxonomy still has no `index_rebalance` type. Argues for a 6th Tier-B trigger / forced-flow overlay.
- **Regulatory / agency-action overlay — META EU DSA (Instagram/Facebook "addictive features", fines up to 6% of
  rev, PRELIMINARY, NEW on the held name); carry NHTSA AV first-responder warning (TSLA/GOOGL/AMZN/UBER, fixes due
  end-July), EU DMA App Store, SEC reporting overhaul.** No rule reads a court/agency action.
- **Capital-allocation / capex-commitment overlay (recurring) — MU $250B US buildout (through 2035); META 14GW /
  Muse Spark / in-house "Iris" chip; Lutnick telling Samsung/SK Hynix they have "no choice" but to build US fabs.**
  No rule reads a multi-year capex / reshoring announcement. *Research: a capex/capital-allocation overlay AND a
  re-entry rule for event_driven_catalyst.*
- **Earnings/print-window ASSIGNMENT gap — JPM (7/14, window OPEN, MOST URGENT; +June CPI +Warsh testimony +PPI
  same week), TSLA (7/22), ARM (7/23), INTC (7/23; JPMorgan named it a highest-conviction Q3 SHORT), AMZN (7/30).**
  All claimed by trend-following/breakout, NOT `equity_event_driven_catalyst` / `long_straddle_earnings`. Reassign
  or activate a straddle on the cluster.
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right?
  Backtest the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **M&A-arb activation — RKLB (acquirer) / IRDM (target, $54/sh, $8B deal) + SYNA/onsemi (carry).**
  `equity_pairs_trading_cointegration` declares pairs_arbitrage but claims only SYNA; RKLB/IRDM pair unmodeled
  (both currently breakout). Cointegration look on RKLB/IRDM if breakout decays.
- **Litigation / product / vendor-strategy events — AAPL sued OpenAI (trade-secret theft, NEW); MSFT in-house AI
  swap (dropping OpenAI/Anthropic in Excel/Outlook); OpenAI "ChatGPT Work"; Grok 4.5; export-control report
  (OpenAI/GOOGL models reaching blacklisted Chinese firms).** No rule reads a lawsuit / product launch / vendor shift.
- **Activist-short / short-call — BE Hunterbrook rebuttal (carry); INTC JPMorgan Q3 short-call (NEW).** No responder.
- **Vol-regime activation — record tech single-name IV (23-yr high) vs benign VIX ~17; event-IV into the earnings
  cluster.** Structures exist (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`)
  but none active / none claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **Fallback-threshold question (issue #5, clarified 7/10)** — no-price-history now routes to `equity_watch_only`
  correctly (SKHY today). The open case is only the degenerate 0-trade Sharpe-0.0 backtest (WULF/SMCI/RKLB/IRDM/BE)
  routing to a below-baseline *trading* provisional. Decide whether a 0-trade score should also route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.

## Open questions for the operator

1. **[HIGH — timing] Confirm single-trigger schedule.** 7/7 & 7/8 double-fired; **7/9 & 7/10 fired once ✓.**
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] News-pipeline staleness / partial-run (BIT 7/10).** Raw HTML + daily_summary written ~15:44 but
   `state/news_brief.md` stayed 7/9 + no `[news 2026-07-10]` commit. Add a `date_in_file == today` guard AND check
   why the news agent's brief-synthesis + git-sync didn't complete.
4. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders).
5. **[MEDIUM] Fallback threshold** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only (see gaps).
6. **FIVE provisional/quarantined claims** — QCOM/SPCX/SYNA (`2026-07-21`) + WULF (`2026-07-23`) + SKHY
   (`2026-07-24`). Saturday research owns validation. Do NOT hand-promote.
