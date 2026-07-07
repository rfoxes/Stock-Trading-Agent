# Tasks for the next run

**⚠️ THE HARNESS IS FROZEN pending operator confirmation of a BROKER-STATE WIPE detected 2026-07-07.** Read
`last_handoff.md` in full before doing anything. The paper account came back FLAT on 7/7 (all four longs gone,
cash unchanged, equity −$31.6k, no `trade_closed` events, provisional claims re-stamped to today) — a suspected
Alpaca paper-account reset, NOT strategy exits. Last run did NOT execute, did NOT log-closed. Replace this file
(don't append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

Every universe symbol MUST have a strategy attached (see `manual.md` P0 rule). Two grades: **(a) VALIDATED**
(cleared baseline Sharpe 0.5 in triage — trades) / **(b) PROVISIONAL** (nothing cleared / no price history —
best-available attached, recorded in `provisional_claims.md`, QUARANTINED from execution until Saturday
research validates). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol. Character-match shortcuts and direct YAML edits to
`active_strategies.md` are FORBIDDEN. Never use `cli add-active` to bypass triage.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks harness deps. Run EVERYTHING via:
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.

## ⚠️ READ SECOND: THE 7/7 BROKER-STATE WIPE — DO NOT RESUME BLIND

On 7/7 the account was FLAT: `positions: []`, equity = cash = **$71,809.59** (cash unchanged to the penny from
7/6), all four longs (AVGO 26 / META 16 / MU 7 / ORCL 38, ~$31.6k MV) gone with **no cash credit** and **no
`trade_closed` journal events**. Provisional claims re-stamped `provisional_since: 2026-07-07`,
`revalidate_by 2026-07-21`. Leading hypothesis: **Alpaca paper-account reset / environment reinitialization.**
Last run FROZE (no execute, no log-closed) pending operator confirmation.

**Your first job: determine whether the operator has confirmed the cause.**
- **If the operator confirms the flat book is the NEW baseline** (reset intended / accepted): treat $71,809.59
  cash / 0 positions as the starting book. Do a normal snapshot, P0 check, then `cli execute` (the account is
  clean, strategies will evaluate against a flat book and may open fresh entries — that's fine). Do NOT
  `log-closed` the four old positions — they weren't sold; there's no realized P&L to attribute.
- **If the operator confirms the positions should be RESTORED / it was a glitch**: do NOT execute; wait for the
  restore. The last-good book + marks are in `last_handoff.md` "Last known-good book" for reconstruction.
- **If there is NO operator word yet AND the account is still flat/anomalous**: stay FROZEN. Do a read-only
  snapshot, confirm state, re-flag the operator, do NOT execute, do NOT log-closed. Document and stop.
- **If the account has visibly changed again** (positions restored, or a different equity): re-assess from the
  fresh broker state; reconcile only what the broker + journal jointly support.

## To do next run

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match the run
   date; if not, treat as ABSENT and re-flag the pipeline. **Run `cli market-status`** and note the run TIME —
   7/7 fired off-cycle at 09:09 mid-session; the canonical run is ~4 PM PT post-close. If firing off-cycle,
   weight that in the execute decision.
2. **Snapshot:** `account`, `positions`, `open-orders`, `regime`. **Compare equity AND cash to the 7/6
   last-good ($103,459.08 / $71,809.59) and the 7/7 flat ($71,809.59 / $71,809.59).** If positions reappear
   with cash moved, that's a real change — reconcile against the journal. If still flat, see the wipe playbook
   above.
3. **P0 check:** `cli list-active`. Expect `unclaimed_count: 0`, `provisional_count: 3` (QCOM/SPCX/SYNA, all
   `revalidate_by 2026-07-21`). Triage any NEW unclaimed symbol; do NOT `add-active`.
4. **Reconciliation — ONLY what's supported.** Use `cli log-closed <id> <symbol> <pnl>` ONLY for positions the
   broker shows gone AND that have a real basis (a `trade_closed` event or a cash move consistent with a sale).
   The four 7/7-vanished names have neither — do NOT log-closed them unless the operator directs a specific
   reconciliation.
5. **Execute (venv) — gated on the wipe playbook.** If the operator has cleared the flat book as baseline (or
   the account is confirmed healthy), run `cli execute`. Provisionals (QCOM/SPCX/SYNA) appear under
   `provisional_quarantined`/`skipped`. If still frozen, do NOT execute.
6. **Library gaps — see list below (Saturday research owns them).**
7. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Position watch (only relevant IF positions are restored)

If the operator restores the 7/6 book, the prior watch items resume: **META** (macd_histogram-owned, entry avg
$605.28); **MU** (trailing stop had NOT fired at −0.73%; DRAM-antitrust overhang); **ORCL** (−18.69%,
restructuring drawdown, no algorithmic responder — top Saturday item); **AVGO** (Broadcom-Apple-2031 positive,
responder NONE). If the flat book stands, these are moot until strategies re-enter organically.

## Library gaps + research items (carry to research_tasks.md — Saturday)

Same open gap set as 7/6 (the 7/6 brief was NOTABLE with several NEW instances). All `responder: NONE` —
informational, not tradable under the mandate:
- **Provisional/quarantined validations (TOP PRIORITY):** SPCX (trend-following; joined Nasdaq-100 7/7 but
  still quarantined; `revalidate_by 2026-07-21`), QCOM (event-driven, 7/21), SYNA (pairs-cointegration, 7/21 —
  LIVE onsemi $7B all-stock merger-arb, long SYNA / short ON at 1.350). Deadlines all reset to 7/21 by the 7/7
  state re-bootstrap.
- **Customer/supply-agreement event window** — MU Micron-Ford + Micron-GM SCAs; AVGO Broadcom-Apple-2031.
  event_driven_catalyst models earnings windows, not supply/partnership disclosures.
- **Product/roadmap-slip sub-trigger** — NVDA Kyber NVL144 delay; MRVL competitive-window read-through.
- **Restructuring/workforce-reduction event window** — MSFT (4,800 cuts) + ORCL (carry). No responder.
- **Pricing/margin-disclosure sub-trigger** — INTC price hikes up to $50 + AAPL ~55% hikes.
- **Regulatory/antitrust event window** — DST-tariff (GOOGL/META/AMZN/AAPL), UK under-16 ban, GOOGL EU €4.1B
  (carry). No rule reads a court/agency/trade action.
- **Index-inclusion/forced-flow (NEW_CATEGORY_NEEDED)** — SPCX→Nasdaq-100 7/7; SK Hynix Nasdaq listing 7/10.
- **Earnings/delivery-window assignment** — JPM (7/14, window open), TSLA (7/22), INTC (7/23), CBRS (carry);
  all trend-following-claimed, not event-driven. JPM most urgent.
- **Capital-allocation event window** — JPM $50B buyback (consummated); MU Trump-Accounts (carry).
- **Vol-regime activation** — MU post-print IV crush; SPCX/JPM/TSLA event-IV. Vol structures exist
  (iron_condor_high_iv, etc.) but none active / none claims a universe symbol.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on
  ARM/MRVL/INTC; bollinger vs trend on CSCO; rsi vs trend on HPE; event-driven vs trend on AVGO/MU/ORCL;
  sector-rotation vs trend on DELL; macd vs trend on META/MSFT; trend placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/
  NUVL/NVDA/QQQ/SPY/TSLA/TSM.

## Open questions for the operator

1. **[P0, BLOCKING] Confirm the 7/7 broker-state wipe.** Was the Alpaca paper account/positions reset? Is the
   flat $71,809.59 book the new baseline, or should the four longs be restored? The harness is frozen until you
   answer. Details + last-good marks in `last_handoff.md`.
2. **[HIGH] Scheduled task fired off-cycle at 09:09 PT mid-session (7/7).** Combined with the 7/3 holiday
   firing, the trigger is misbehaving. Confirm intended schedule; confirm whether a canonical 4 PM run also
   fires.
3. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
4. **[HIGH] News pipeline** — 7/7 brief absent at run time (header `2026-07-06`). Add a health-check/alert +
   the `_load_news_brief()` staleness guard.
5. **[REOPENED] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` when a live order
   exists (did NOT bite 7/7 — no order).
6. **THREE provisional/quarantined claims** — QCOM/SPCX/SYNA, all `revalidate_by 2026-07-21`. Saturday research
   owns validation. Do NOT hand-promote.
