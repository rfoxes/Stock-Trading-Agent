# Tasks for the next run

**⚠️ 3 EXITS SUBMITTED 7/8, FILLING AT THE 7/9 OPEN — RECONCILE THEM, DO NOT FREEZE.** The fixed
`equity_event_driven_catalyst` fired its now-enforced exits: SELLS for **AVGO 26** (time stop), **MU 7** (time
stop), **ORCL 38** (hard ATR stop). They were submitted but rest unfilled (market was closed) and should fill at
the 7/9 open. Read `last_handoff.md` for the full narrative. Replace this file (don't append) when you write the
next version.

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

## To do next run (7/9)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match the run date;
   if not, treat as ABSENT and note the gap. **Run `cli market-status`**; note the run TIME (canonical ~4 PM PT
   post-close). If the schedule double-fires again, weight that in the execute decision.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`.
   - **Expected book after the 7/9 open fills:** positions = **META 16 ONLY**; cash risen ~$22,080 to **~$93,891**;
     equity roughly unchanged (~$103k, moved only by META's mark + fill slippage). **This is a LEGITIMATE CLOSE
     (cash RISES by ~proceeds), NOT a wipe** (wipe = cash unchanged while positions vanish). Do NOT freeze.
   - `open-orders` will likely still ERROR with `'dict' object has no attribute 'id'` if any sell is still live
     (the reopened parser bug bites when a live order exists). Once all 3 fill, the error should clear.
3. **RECONCILE THE FILLS (the day's key task).** For each of AVGO/MU/ORCL that the broker now shows GONE, run
   `cli log-closed equity_event_driven_catalyst <SYM> <pnl_fraction>` using the **ACTUAL fill price** from Alpaca
   (approx targets below from 7/8 marks — REPLACE with real fills):
   - `log-closed equity_event_driven_catalyst AVGO +0.028`   (~$388 vs entry $377.27 — a WIN)
   - `log-closed equity_event_driven_catalyst MU   -0.0375`  (~$946 vs entry $982.90)
   - `log-closed equity_event_driven_catalyst ORCL -0.204`   (~$141 vs entry $177.28)
   Only log the ones that ACTUALLY closed. **Self-healing:** if a sell expired overnight and a position is still
   open, execute will simply re-emit it — no manual action; just reconcile whatever filled.
4. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 7` (QCOM/SPCX/SYNA
   `revalidate_by 2026-07-21`; SMCI/RKLB/IRDM/BE `revalidate_by 2026-07-22`). Triage any NEW unclaimed symbol; do
   NOT `add-active`. (SK Hynix's US ADR listing is due **7/10** — if the news agent promotes it, it'll need triage.)
5. **Execute (venv).** `cli execute` per standard workflow. event_driven_catalyst now has only META-less held names
   left (AVGO/MU/ORCL exited); it may fire nothing. Provisionals stay quarantined/skipped.
6. **Library gaps — see list below (Saturday research owns them).**
7. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Wipe playbook (KEEP for reference — full doctrine in manual.md "Recent feedback")
If a future run finds the account FLAT with **cash UNCHANGED** and **no `trade_closed` events** → wipe signature →
FREEZE (no execute, no log-closed), record last-good marks, flag operator. **Un-freeze on evidence** if a later
snapshot shows positions restored to prior qty/avg-entry + no phantom closes + canonical post-close + fresh brief.
**NOTE: the 7/9 fills are NOT this** — cash will RISE (real proceeds), positions gone because they legitimately
SOLD. Distinguish "cash unchanged + vanished" (wipe → freeze) from "cash up + vanished" (fills → reconcile).

## Position watch (after the 7/9 fills)

- **META (+/− small, avg $605.28) — the only remaining long.** `equity_momentum_macd_histogram`-owned; rides its
  MACD exit. DMA regulatory read-through is an overhang, not a shock; no responder (informational).
- **AVGO / MU / ORCL — EXITED 7/9** by event_driven_catalyst (time/time/hard-stop). Reconcile via log-closed
  (step 3). ORCL's −20% finally closed — the old missing-exit bug is fixed and enforced.

## Library gaps + research items (carry to research_tasks.md — Saturday)

All `responder: NONE` — informational, not tradable under the mandate. From the 7/8 NOTABLE brief:
- **Provisional/quarantined validations (TOP PRIORITY):** now **7** — QCOM (event-driven), SPCX (trend-following;
  Nasdaq-100 + FCC 100k-sat filing, still quarantined), SYNA (pairs; onsemi merger-arb), plus NEW 7/8:
  **SMCI** (event-driven, edge-AI appliance), **RKLB** (event-driven, $8B Iridium M&A), **IRDM** (pairs; the
  RKLB/IRDM merger-arb target @ $54/sh — a genuine live pair worth a real cointegration look), **BE** (event-
  driven, Hunterbrook short report). QCOM/SPCX/SYNA `revalidate_by 2026-07-21`; SMCI/RKLB/IRDM/BE `2026-07-22`.
- **event_driven_catalyst exit CALIBRATION (was: implementation — now DONE/enforced).** The exit side is now
  wired and fired live (AVGO/MU/ORCL 7/8). Remaining research: is `max_hold_days: 7` right? Backtest the time-stop
  horizon + the 2×ATR hard-stop multiple. Also: the strategy models only a name's OWN earnings window — no re-entry
  on a NEW catalyst (AVGO's Apple $30B deal fired the exit while a fresh bull catalyst landed same day).
- **Customer-win / capital-allocation overlay (NEW instance) — Apple↔AVGO/AAPL $30B Broadcom deal.** No rule reads
  an anchor-customer / supply-commitment win. Positive catalyst on a held name the library can't act on.
- **Competitor-earnings / sector read-through — Samsung $59B guide (bullish MU/SNDK/TSM) + China CXMT threat
  (bearish MU/SNDK, NEW).** event_driven_catalyst models only a name's own window, not a peer print.
- **Regulatory / antitrust window — EU DMA App Store ruling (AAPL/GOOGL/META, concrete action); SEC reporting
  shake-up; BE Hunterbrook short report.** No rule reads a court/agency/activist-short action.
- **Index-inclusion / forced-flow (NEW_CATEGORY_NEEDED, index_rebalance)** — SPCX Nasdaq-100 + FCC filing; **SK
  Hynix $29B Nasdaq ADR listing due 7/10**. Taxonomy has no index_rebalance type — recurring, argues for a 6th
  Tier-B trigger / forced-flow overlay.
- **M&A-arb activation — RKLB/IRDM ($54/sh confirmed, NOW in universe) + SYNA/onsemi (carry).** pairs_cointegration
  declares pairs_arbitrage; IRDM/SYNA both provisional. Validate the RKLB/IRDM and SYNA/ON pairs via head-to-head.
- **Earnings/delivery-window assignment — JPM (7/14, window OPEN, most urgent), TSLA (7/22), INTC (7/23), AMZN
  (7/30).** All trend-following-claimed, not event-driven.
- **Product-launch / competitive-threat — SMCI edge-AI appliance; OpenAI GPT-Live vs MSFT; NVDA Vera Rubin
  supply.** No rule reads a product launch / partner-competitor product event.
- **Vol-regime activation — single-name event-IV (JPM/TSLA/INTC/AMZN, SK-Hynix listing) + oil-driven index-vol
  tail (Iran).** Structures exist (iron_condor_high_iv, long_straddle_earnings) but none active / none claims a
  universe symbol.
- **Fallback-threshold question (NEW, minor)** — SMCI/RKLB/IRDM/BE each triaged to a below-baseline TRADING
  provisional (Sharpe 0.0 from 0 trades) rather than `equity_watch_only`, because a 0.0 score reads as "rankable
  candidate" not "no signal." Decide whether a 0-trade degenerate backtest should route to watch_only instead.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.

## Open questions for the operator

1. **[timing, HIGH] Confirm the single-trigger schedule** — 7/7 double-fired (09:09 + 16:03), 7/3 fired on a
   holiday. 7/8 fired once at the canonical ~16:02 ✓. A double-fire on an order-submitting day is the real risk.
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[REOPENED, BITING] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order
   exists. Bit 7/8 (3 live sells). Doesn't block trading; blinds the open-orders view until fills clear.
4. **[MEDIUM] News-pipeline staleness guard** — `_load_news_brief()` never compares `date_in_file` to today.
5. **[MEDIUM, NEW] Fallback threshold** — 0-trade Sharpe-0.0 → trading-provisional vs watch_only (see gaps list).
6. **SEVEN provisional/quarantined claims** — QCOM/SPCX/SYNA (`2026-07-21`), SMCI/RKLB/IRDM/BE (`2026-07-22`).
   Saturday research owns validation. Do NOT hand-promote.
