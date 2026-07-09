# Tasks for the next run

**✅ 7/9 COMPLETE (single fire, canonical 16:03).** The 3 resting 7/8 exits FILLED at the 7/9 open and were
reconciled: `log-closed equity_event_driven_catalyst` **AVGO +0.0628 / MU +0.0296 / ORCL −0.2027** (ACTUAL fills,
not estimates — MU came in a WIN, not the −3.75% the 7/8 marks implied). Book is now **META ONLY**, cash
$94,690.32. WULF triaged → provisional/quarantined. `cli execute` ran 0 intents. See `last_handoff.md`. Replace
this file (don't append) when you write the next version.

**🛑 IF THE SCHEDULE DOUBLE-FIRES 7/9 (a 2nd fire today, like 7/7 & 7/8): TAKE NO ACTION.** The reconciliation is
DONE. Do **NOT** re-run `log-closed` (would double-count the AVGO/MU/ORCL closes and corrupt strategy Sharpe/win-
rate). Do **NOT** re-execute (0 intents anyway; nothing to gain, book is clean). Confirm book = META only + cash
$94,690.32 + no open orders, note the double-fire, and git-sync a "no-action, double-fire" record. This differs
from a normal next-day 7/10 run below.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5
in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED
until Saturday research validates). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are
FORBIDDEN. Never use `cli add-active` to bypass triage.

## To do next run (7/10, Friday — normal day, book is stable)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-10; if
   not, treat as ABSENT and note the gap. **Run `cli market-status`**; note the run TIME. If it double-fires,
   apply the no-action guard (this book has no resting orders, so a 2nd fire mainly risks nothing — but still take
   no action and don't re-execute).
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book: META 16 ONLY** (avg $605.28), cash **~$94,690**, equity ~$104.8k (moves only on META's mark).
     No resting orders. If instead the account is FLAT with **cash UNCHANGED** and **no `trade_closed` events** →
     wipe → FREEZE (see playbook). A rising-cash vanish would be a legit close to reconcile, but nothing is
     currently pending to close.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 4` (QCOM/SPCX/SYNA
   `revalidate_by 2026-07-21`; **WULF** `revalidate_by 2026-07-23`). **SK Hynix (SKHY) LISTS 7/10** — the news
   agent will likely promote it on its debut; if so it lands UNCLAIMED → run `triage-symbol SKHY --gap-type
   event_catalyst` (expect provisional/quarantined — no price history on a day-1 listing). Triage any other NEW
   unclaimed symbol; do NOT `add-active`.
4. **Execute (venv).** `cli execute` per standard workflow. META rides its MACD exit; event_driven_catalyst's
   live claims (AVGO/MU/ORCL) are now flat with no fresh entry catalyst → likely fires nothing. Provisionals stay
   quarantined/skipped.
5. **Library gaps — see list below (Saturday research owns them).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
Account FLAT with **cash UNCHANGED** + **no `trade_closed` events** → wipe signature → FREEZE (no execute, no
log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later snapshot shows positions
restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief. Distinguish "cash
unchanged + vanished" (wipe → freeze) from "cash UP + vanished" (fills → reconcile via `log-closed` using ACTUAL
`get_order` fill prices, NOT prior-day marks — see the 7/9 MU sign-flip lesson now in manual.md).

## Position watch

- **META (+4.7%, avg $605.28) — the ONLY live position.** `equity_momentum_macd_histogram`-owned; rides its MACD
  exit. Got a *positive* capex event 7/9 (first Canadian DC, Muse Image, 14GW) — informational, no responder.
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** No longer held. event_driven_catalyst still *claims* the symbols
  in the universe (fine — claim ≠ position); it will re-enter only on a fresh modeled catalyst.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/11)

All `responder: NONE` — informational, not tradable under the mandate. From the 7/9 NOTABLE brief:
- **Provisional/quarantined validations (TOP PRIORITY):** now **4** — QCOM (event-driven), SPCX (trend-following;
  Nasdaq-100 forced-flow, still quarantined), SYNA (pairs; onsemi merger-arb) — all `revalidate_by 2026-07-21` —
  plus **WULF** (event-driven; Anthropic $19B lease, `revalidate_by 2026-07-23`). Validate/upgrade or archive each.
- **Capital-allocation / capex-commitment overlay (NEW, recurring) — MU $250B US buildout (through 2035); META
  14GW / first Canadian DC; Micron fabs.** No rule reads a multi-year capex / reshoring announcement. On 7/9 this
  was a *positive* catalyst on MU the day its time-stop exit fired (sold into the +8% pop → the exit still booked a
  WIN, but the strategy models only a name's OWN earnings window, no re-entry on a new catalyst). *Research: a
  capital-allocation / capex overlay AND a re-entry rule for event_driven_catalyst.*
- **event_driven_catalyst exit CALIBRATION (exit side now proven live).** AVGO/MU/ORCL exits fired 7/8, filled
  7/9, two booked wins. Remaining: is `max_hold_days: 7` right? Backtest the time-stop horizon + the 2×ATR hard-stop
  multiple. Also add re-entry-on-new-catalyst (AVGO's Apple deal + MU's $250B both landed as the time stop forced exit).
- **Regulatory / agency-action overlay — NHTSA AV first-responder warning (TSLA/GOOGL/AMZN/UBER, fixes due
  end-July, NEW); carry EU DMA App Store + SEC reporting overhaul.** No rule reads a court/agency action.
- **Earnings/print-window ASSIGNMENT gap — JPM (7/14, window OPEN, MOST URGENT; +June CPI +Warsh testimony same
  day), ARM (7/23, +11% pre-print 7/9), TSLA (7/22), INTC (7/23), AMZN (7/30).** All claimed by
  trend-following/breakout, NOT `equity_event_driven_catalyst` / `long_straddle_earnings`. Reassign or activate a
  straddle on the cluster.
- **M&A-arb activation — RKLB (acquirer) / IRDM (target, $54/sh, $8B deal + $3.6B bridge) + SYNA/onsemi (carry).**
  `equity_pairs_trading_cointegration` declares pairs_arbitrage but claims only SYNA; RKLB/IRDM pair unmodeled
  (RKLB→breakout, IRDM→breakout after 7/8 validation). Cointegration look on RKLB/IRDM if breakout decays.
- **Product / vendor-strategy event — MSFT swapping OpenAI/Anthropic for in-house AI in Excel/Outlook; OpenAI
  "ChatGPT Work"; Grok 4.5.** No rule reads a product launch / vendor shift.
- **Activist-short / controversy — BE Hunterbrook rebuttal (escalated, shares rallied).** No responder.
- **Index-inclusion / forced-flow (NEW_CATEGORY_NEEDED, index_rebalance) — SPCX Nasdaq-100 + SK Hynix (SKHY) 7/10
  listing + BlackRock QQQ-challenger ETF.** Recurring across sessions — argues for a 6th Tier-B trigger / forced-flow
  overlay. Taxonomy still has no `index_rebalance` type.
- **Vol-regime activation — record tech single-name IV (23-yr high) vs benign VIX 16.9; event-IV into the earnings
  cluster.** Structures exist (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`)
  but none active / none claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **Fallback-threshold question (recurring, minor)** — WULF (7/9) + SMCI/RKLB/IRDM/BE (7/8) each triaged to a
  below-baseline TRADING provisional (Sharpe 0.0 from 0 trades) rather than `equity_watch_only`, because a 0.0 score
  reads as "rankable candidate" not "no signal." Decide whether a 0-trade degenerate backtest should route to
  watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.

## Open questions for the operator

1. **[HIGH — timing] Fix the single-trigger schedule.** 7/7 & 7/8 double-fired; 7/9 fired once ✓. A double-fire on
   a reconciliation day is newly dangerous — a 2nd fire could re-run `log-closed` and double-count closes. Confirm
   single-trigger config.
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
   Dormant now (no live orders); re-bites next time an order rests.
4. **[MEDIUM] News-pipeline staleness guard** — `_load_news_brief()` never compares `date_in_file` to today.
5. **[MEDIUM] Fallback threshold** — 0-trade Sharpe-0.0 → trading-provisional vs watch_only (see gaps list).
6. **FOUR provisional/quarantined claims** — QCOM/SPCX/SYNA (`revalidate_by 2026-07-21`) + WULF (`revalidate_by
   2026-07-23`). Saturday research owns validation. Do NOT hand-promote.
