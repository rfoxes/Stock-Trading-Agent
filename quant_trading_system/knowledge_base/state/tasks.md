# Tasks for the next run

**✅ THE HARNESS IS UN-FROZEN. Normal operation resumed 2026-07-07 post-close.** The 7/7 09:09 "broker-state
wipe" was TRANSIENT — the four longs (AVGO 26 / META 16 / MU 7 / ORCL 38) self-restored to their exact prior
qty/avg-entry by the 16:03 post-close run, cash intact ($71,809.59), equity back to ~$103,099. `cli execute`
RAN clean (0 intents). Nothing was reconciled (nothing actually closed). Read `last_handoff.md` for the full
un-freeze rationale. Replace this file (don't append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

Every universe symbol MUST have a strategy attached (see `manual.md` P0 rule). Two grades: **(a) VALIDATED**
(cleared baseline Sharpe 0.5 in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no price history —
best-available attached, recorded in `provisional_claims.md`, QUARANTINED from execution until Saturday
research validates). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match shortcuts and direct YAML edits to
`active_strategies.md` are FORBIDDEN. Never use `cli add-active` to bypass triage.

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks harness deps. Run EVERYTHING via:
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.

## Wipe playbook (KEEP for reference — un-freeze doctrine now in manual.md "Recent feedback")

If a future run finds the account FLAT again (positions gone, cash unchanged, no `trade_closed` events): that's
the wipe signature → FREEZE (no execute, no log-closed), record last-good marks, flag operator. **BUT** the
7/7 case proved these can be transient: **un-freeze on evidence** if a later snapshot shows (1) positions
restored to their prior qty/avg-entry, (2) `recent-trades` shows NO phantom `trade_closed` events, and (3) it's
a canonical post-close run with a fresh, correctly-dated brief. Then reconcile nothing and resume. Full doctrine:
`manual.md` "Recent feedback" (freeze + un-freeze bullets).

## To do next run (standard workflow — no special handling expected)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match the run
   date; if not, treat as ABSENT and re-flag the pipeline. **Run `cli market-status`** and note the run TIME —
   the canonical run is ~4 PM PT post-close. If firing off-cycle (the schedule has double-fired — 7/7 fired at
   both 09:09 and 16:03), weight that in the execute decision (see operator item #2 in last_handoff).
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`. **Baseline to compare against:** equity
   ~$103,099 / cash $71,809.59 with the 4 longs (AVGO/META/MU/ORCL) open. If the book matches, it's continuity —
   proceed. If FLAT again, apply the wipe playbook above.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count: 0`, `provisional_count: 3` (QCOM/SPCX/SYNA, all
   `revalidate_by 2026-07-21`). Triage any NEW unclaimed symbol; do NOT `add-active`.
4. **Reconciliation — ONLY what broker + journal jointly support.** Use `cli log-closed <id> <symbol> <pnl>`
   ONLY for a position the broker shows gone AND that has a real basis (a `trade_closed` event or a cash move
   consistent with a sale). No fabrication.
5. **Execute (venv).** Account is healthy — run `cli execute` per standard workflow. Provisionals
   (QCOM/SPCX/SYNA) appear under `provisional_quarantined`/`skipped` (symbol-level quarantine — the rest of each
   strategy's claims trade normally).
6. **Library gaps — see list below (Saturday research owns them).**
7. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Position watch

- **ORCL (−20.13%, avg $177.28, cur $141.60) — TOP concern, but it's a CODE gap, not a market call.**
  event_driven_catalyst owns and evaluates ORCL but its `evaluate()` has **no exit implementation** — the 6/10
  entry documented "Stop @ 175.11 / 7-day time stop" yet submitted a plain market buy (`stop_price: null`) and
  never generates an exit intent, so both stops are dead letters. Do NOT hand-exit (forbidden). Top Saturday
  research item: implement the exit side. Meanwhile the position rides unmanaged.
- **MU (−6.04%, avg $982.90):** deepened on the Samsung-driven chip rout (competitor read-through; the memory
  pricing cycle looks fundamentally intact). event_driven_catalyst-owned, no exit fired.
- **META (+1.71%, avg $605.28, macd_histogram-owned):** GREEN — Muse Image launch + upgrade. Rides its MACD exit.
- **AVGO (−2.19%, avg $377.27):** no fresh single-name event; rode the chip pullback. event_driven_catalyst.

## Library gaps + research items (carry to research_tasks.md — Saturday)

All `responder: NONE` — informational, not tradable under the mandate. Same open set as the 7/7 NOTABLE brief:
- **Provisional/quarantined validations (TOP PRIORITY):** SPCX (trend-following; joined Nasdaq-100 7/7 but still
  quarantined), QCOM (event-driven), SYNA (pairs-cointegration; LIVE onsemi $7B all-stock merger-arb, long SYNA
  / short ON at 1.350). All `revalidate_by 2026-07-21`.
- **event_driven_catalyst EXIT IMPLEMENTATION (new, sharpened):** the strategy implements entry but not exit —
  no price-stop or time-stop exit intents are ever generated (ORCL −20% is the live casualty). Highest-value fix.
- **Competitor-earnings / sector read-through overlay** — Samsung Q2 → MU/SNDK/MRVL/INTC/ARM chip rout. No rule
  reads a competitor's print as a signal on our names.
- **Capital-allocation / debt-raise event window** — AMZN ≥$25B AI-capex bond sale; JPM $50B buyback (carry);
  MU Micron-Ford/GM SCAs. No responder.
- **Product-launch / competitive-threat window** — META Muse Image; NVDA DeepSeek-chip threat + Kyber roadmap
  rebuttal. No responder.
- **Index-inclusion / forced-flow (NEW_CATEGORY_NEEDED, index_rebalance)** — SPCX→Nasdaq-100 7/7 (fell ~7%
  despite ~$4.3B inflow); SK Hynix US listing ~7/10. Taxonomy has no index_rebalance type.
- **Earnings/delivery-window assignment** — JPM (7/14, window OPEN, most urgent), TSLA (7/22), INTC (7/23), AMZN
  (7/30), CBRS (carry). All trend-following-claimed, not event-driven.
- **Regulatory/antitrust window** — DST-tariff (GOOGL/META/AMZN/AAPL), UK under-16 ban, Meta addiction
  litigation, SEC quarterly-reporting shake-up. No rule reads a court/agency/trade action.
- **Pricing/margin + restructuring sub-triggers (carry)** — INTC price hikes; MSFT 4,800 cuts. No responder.
- **Vol-regime activation** — MU/SNDK single-name IV; the oil-driven index-vol tail from Hormuz. Vol structures
  exist (iron_condor_high_iv, etc.) but none active / none claims a universe symbol.
- **Provisional claim-REASON prose reconciliation** — the 7/7 re-bootstrap stamped a QCOM-specific
  "QUARANTINED" string onto the whole event_driven_catalyst / trend_following claims, but only QCOM/SPCX/SYNA
  are actually quarantined (execute confirmed symbol-level). Reconcile the prose via re-triage, NOT a hand-edit.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; event-driven vs trend on AVGO/MU/ORCL; sector-rotation vs
  trend on DELL; macd vs trend on META/MSFT; trend placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/
  TSLA/TSM.

## Open questions for the operator

1. **[timing, HIGH] The schedule double-fired on 7/7** (09:09 mid-session + 16:03 post-close) and fired on the
   7/3 holiday. Confirm the intended trigger; ensure exactly one canonical ~4 PM post-close run per trading day.
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[MEDIUM] News-pipeline staleness guard** — `_load_news_brief()` never compares `date_in_file` to today.
4. **[FYI] 7/7 09:09 flat read was transient/self-restored** — if convenient, confirm on the Alpaca dashboard
   what caused the momentary flat account, to harden the pipeline. No account action needed.
5. **[REOPENED] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order exists.
6. **THREE provisional/quarantined claims** — QCOM/SPCX/SYNA, all `revalidate_by 2026-07-21`. Saturday research
   owns validation. Do NOT hand-promote.
