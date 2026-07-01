# Tasks for the next run

This file is the focused to-do list for the next run (**Thu 2026-07-02**). Yesterday's Claude wrote it
after the 7/1 run (QQQ exit reconciled +12.4%; NEW MACD BUY 16 META fired, pending fill). Replace it
(don't append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

**Every symbol in the universe MUST have a strategy attached — none is ever left strategy-less.** See
`manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE". Two grades:
- **(a) VALIDATED claim** — a library strategy cleared baseline Sharpe (0.5) in a `cli triage-symbol`
  backtest. Trades normally.
- **(b) PROVISIONAL claim** — nothing cleared baseline (or no price history), so triage attached the
  best-available strategy as an UNVALIDATED claim, recorded in `state/provisional_claims.md` with a
  `revalidate_by` deadline and **QUARANTINED from execution** (`cli execute` auto-skips). Never trades
  until Saturday research validates.

After triage, `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]` for any
NEW unclaimed symbol. Character-match shortcuts and direct YAML edits to `active_strategies.md` are
FORBIDDEN. Never use `cli add-active` to bypass triage.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps.** Bare `python3 -m
quant_trading_system.cli ...` fails with `No module named 'requests'`. Confirmed still broken 7/1.
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a "stop on
ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF

The **7/1 brief was FRESH** (header `2026-07-01` matched today) — pipeline held after 6/30's recovery,
but it's been flaky (misses span 6/22, 6/25, 6/29). **Always check `news_brief.md`'s
`# News brief for <date>` header matches today BEFORE trusting it.** If it doesn't, treat the brief as
ABSENT (proceed on realized price) and re-flag the news pipeline.

## Status as of last update (2026-07-01, NOT a do-nothing day — QQQ reconciled + META BUY fired)

- **`cli execute` → 1 NEW intent submitted:** `equity_momentum_macd_histogram` **BUY 16 META**, order_id
  `3ce90fcd-c897-4ebe-be13-7e19c6482668`, all 5 SafetyGate checks passed. **⚠️ NOT FILLED at session end**
  (`filled_qty 0.0`; post-close DAY market order). **#1 reconciliation item below.** Rule-driven price/
  MACD entry — NOT related to META's litigation/cloud-unit news (responder NONE). Other 7 strategies →
  0 intents. **Decision: Keep.**
- **QQQ exit FILLED overnight + reconciled +0.124.** The 6/30 SELL 28 (order `f75ca170-…`) filled; QQQ
  gone from the book. Derived fill ≈ $728.08/sh from the +$20,386.24 cash delta (entry avg $647.96 ⇒
  +12.37%); logged `log-closed equity_trend_following_ema_cross QQQ 0.124`. QQQ stays trend-following's
  claim (no triage churn). Trend-following now holds NONE of its 12 claimed names as active longs.
- **P0 = 0 unclaimed.** No new universe member, no promotions. `list-active` → universe 26, claimed 26,
  unclaimed 0, provisional 3 (QCOM, SPCX, SYNA). Nothing to triage.
- **3 PROVISIONAL/quarantined claims:** SPCX (revalidate_by **2026-07-04 — THIS WEEK / next checkpoint**),
  QCOM + SYNA (revalidate_by 2026-07-10). Execute confirmed all three skipped. Do NOT hand-promote.
- **Account: equity $103,801.65; cash $81,494.03; buying power $388,437.46.** (−$1,389.88 vs 6/30 on the
  semi rout; the QQQ sale itself is equity-neutral — unrealized became cash.)
- **Positions (3 longs, META buy pending):** AVGO 26 (**−2.01%**, −$196.82, turned red from +0.10%),
  MU 7 (**+5.27%**, +$362.88 — gave back hard from +17.43%, ~−10% intraday, trailing stop did NOT fire),
  ORCL 38 (**−19.06%**, −$1,284.27, only red, DEEPENED to worst yet).
- **Regime: bull, conf 0.74, ADX 23.72, realized_vol 0.1762.**
- **Infra:** `cli open-orders` parser bug REOPENED on the live META order (`'dict' object has no
  attribute 'id'`) — 3rd confirmation. Clean only when no live order.
- **News brief FRESH (7/1), NORMAL FLOW.** AI-capex give-back rotation (~4.5% semi rout vs Dow record +
  software bid — price, not news). New events all `responder: NONE` legal/regulatory/restructuring on
  held/universe names (see library gaps).

## To do next run (Thu 7/2)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv (warning #1). **Date-check the brief**
   (warning #2). **Macro: June nonfarm payrolls Thu 7/2 8:30 AM ET** (pulled early ahead of July 4) — the
   week's headline print; ADP already missed at +98k on 7/1. **TSLA Q2 delivery print expected 7/2**
   (IR consensus ~406k) — TSLA is trend-following/price-claimed (responder NONE; earnings-window gap).
   Half-day/holiday schedule around July 4 — confirm the session ran normally.

2. **🔴 #1 RECONCILE THE META ENTRY.** Snapshot `positions`. Two cases:
   - **META appears (buy filled):** 16 shares added at ~fill price; it becomes/adds to
     `equity_momentum_macd_histogram`'s live long. No reconcile CLI needed for an entry — just note the
     fill price (derive from cash delta if the journal hasn't stamped one). META stays macd's claim.
   - **META absent (DAY buy cancelled at session end):** the MACD rule will likely re-fire the BUY on
     `cli execute` if the signal persists. **Let it execute — do NOT cancel or override.**

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0`, `provisional_count: 3`
   (QCOM, SPCX, SYNA). If any NEW symbol shows unclaimed, run `cli triage-symbol <SYM>
   [--gap-type <type>]`. Do NOT use `cli add-active`.

4. **Position watch:**
   - **META — see #2.** Rule-driven entry in flight. No discretionary action either direction.
   - **MU — gave back to +5.27% (from +17.43%), ~−10% intraday on the semi rout; trailing stop did NOT
     fire (still green).** New DRAM-antitrust overhang + supply-tight commentary (no rule reads either).
     Watch the give-back scenario where the trailing stop could engage. No discretionary action; do NOT
     sell to "lock in" — forbidden.
   - **ORCL — −19.06% (−$1,284) and DEEPENING (worst yet); book's only red.** Restructuring (21k cuts)
     has no algorithmic responder; event_driven_catalyst (claims ORCL provisionally) models earnings
     only. Held; elevated for Saturday. No action.
   - **AVGO — turned red −2.01%; no rule fired.** Correct do-nothing on the semi rout.
   - **Others (ARM/INTC/MRVL, MSFT/SNDK, CSCO, HPE, DELL) + trend-following's now-empty large-cap sleeve
     (AAPL/AMZN/GOOGL/JPM/NVDA/SPY/QQQ/TSLA/TSM/CBRS/NUVL)** — 0 intents 7/1. Watch their gates; no trade
     = correct if unmet.

5. **Run `cli execute` (via venv).** SPCX/QCOM/SYNA appear under `provisional_quarantined`/`skipped` —
   expected. React to realized price: if a rule fires (a re-fired META buy, a payroll/delivery-day
   reaction, or a new signal), execute; if none fires, do-nothing is correct. Do NOT discretionarily
   de-risk or take profits.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **THREE provisional/quarantined validations (TOP PRIORITY):**
  - **SPCX** (trend-following, deadline **2026-07-04 — THIS WEEK / NEXT**, needs ≥60 bars). Carry:
    Nasdaq-100 add **Tue 7/7** (~$4.3B forced passive buying), elevated single-name IV, broke IPO price.
    Likely wants a vol-selling options responder.
  - **QCOM** (event-driven, deadline **2026-07-10**). Top candidate Sharpe 0.0.
  - **SYNA** (pairs-cointegration, deadline **2026-07-10**). **Live merger-arb:** onsemi $7B all-stock
    (1.350 ON/sh, ~19% premium, close mid-2027). Textbook long SYNA / short ON. The activation instance
    for the standing m_a_arbitrage gap — validate the pairs setup.
- **Regulatory / antitrust ruling on universe names — NEW live instances GOOGL (Klarna ~$1.97B +
  Yelp win) and META (29-state youth-addiction suit → trial).** No active rule reads a court/agency
  ruling. Pairs with the carry MU DRAM suit + AAPL SCOTUS cert. Build a regulatory/litigation event-
  window overlay for large-caps. gap_type: event_catalyst — responder: NONE.
- **Business-model / product-line launch — NEW, META (AI cloud unit selling excess compute) + AMZN
  (AWS $1B AI-engineering unit).** No rule reads a new-business-line disclosure. Whether a strategic-
  announcement sub-trigger belongs in an event-window overlay. gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction — MSFT (thousands of cuts, NEW) + ORCL (21k, carry, held name
  −19.06% and deepening).** Claimed by price-driven strategies; unmodeled. Recurring big-tech event
  class. Build a restructuring event-window; decide whether a generic price-based stop should co-cover
  event-driven's held names. gap_type: event_catalyst — responder: NONE / partial.
- **Delivery / earnings-window assignment — TSLA (Q2 delivery print 7/2) + INTC (Q2 7/23) + CBRS
  (printed 6/23 AMC, carry).** The earnings-window responder (equity_event_driven_catalyst) does not
  claim TSLA, INTC, or CBRS (all trend-following). Assign the earnings-window strategy to scheduled-
  catalyst names via head-to-head. gap_type: earnings_window — responder: NONE (assignment).
- **Short-interest / positioning disclosure — NVDA (Burry 13F short on NVDA/TSLA/AMAT/CAT).** No rule
  reads a 13F/short disclosure. gap_type: event_catalyst — responder: NONE.
- **Capital-allocation / capital-return — JPM ($50B buyback + dividend, eff 7/1) + AMZN (AWS +20% GPU
  pricing, carry) + MU ($250M Trump Accounts).** No rule reads a buyback/dividend/pricing disclosure.
  gap_type: event_catalyst — responder: NONE.
- **Partnership / customer-win — MSFT (Haleon 5-yr AI deal) + NVDA (Palantir sovereign-AI, carry).**
  No rule reads a named partnership. gap_type: event_catalyst — responder: NONE.
- **Index-rebalance / forced-flow window — recurring cluster.** SPCX→Nasdaq-100 **Tue 7/7**; SK Hynix
  Nasdaq listing ~7/10; GOOGL→DJIA + FTSE Russell consummated. No rule reads an index-rebalance schedule.
  Open Q: index-inclusion as a 6th Tier-B promotion trigger? gap_type: event_catalyst — responder: NONE.
- **Litigation / antitrust on a held name — MU (DRAM price-fixing class action, N.D. Cal., carry).**
  MU's provisional/quarantined claim models earnings windows only. gap_type: event_catalyst —
  responder: NONE.
- **Input-cost / margin-compression carry (AAPL Mac/iPad, MSFT Xbox; Cook "extreme memory shortage").**
  Price-claimed; no rule reads a cost/margin shock. Build an event-window overlay co-claiming large-caps
  for cost/margin events. gap_type: event_catalyst — responder: NONE.
- **Macro-event-window category (jobs week: NFP 7/2; higher-for-longer; May core PCE 3.4%).** No
  canonical gap_type covers a scheduled macro print; no rule lets the trader pre-position (correct under
  the mandate, but the soft-signal handle is missing). gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX ~16.45, index IV-rank below the >50 threshold; MU post-print IV crush;
  SPCX hyper-IV into 7/7; TSLA IV into the 7/2 delivery print). volatility_regime is declared
  (iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings) but none active / none
  claims a universe symbol. Activate one vol strategy with a claim (MU IV crush = textbook short-vol;
  doubles as SPCX candidate). gap_type: volatility_regime — responder: NONE (active); activation pending.
- **AI-capex financing / crowding + two-sided positioning overlay ("painful repricing" — Sløk vs Ackman
  bull vs Burry short).** Cohort financing/leverage + crowding still has no rule. gap_type:
  NEW_CATEGORY_NEEDED — responder: NONE.
- **AI-policy / export-control overlay** (Trump admin lifted export controls on Anthropic's Claude
  models; INTC nationalization framing carry) — no rule responds to national-security/export/AI-policy
  events. gap_type: event_catalyst — responder: NONE.
- **Validate the first-pass + provisional assignments via head-to-head:**
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT (SNDK already
    validated for macd, Sharpe 2.254 — no head-to-head needed; note META now has a LIVE macd long)
  - trend-following placeholders → AAPL, AMZN, CBRS, GOOGL, JPM, NUVL, NVDA, QQQ, SPY, TSLA, TSM
    (CBRS → event-driven; TSLA → event-driven for the delivery-window)
  - QCOM provisional (event-driven) + SYNA provisional (pairs-cointegration) → validate or escalate

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no deps). Repoint
   the Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the
   venv. Persisting across many runs.
2. **[HIGH] News pipeline flaky — FRESH 7/1 (held after 6/30 recovery) but missed 6/22 + 6/25 + 6/29.**
   Add a health-check / alert on news-agent run failure so a missed/stale brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3).
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to today.
   Reject/down-weight a brief whose date != today.
4. **[REOPENED] `cli open-orders` parser bug** — errors `'dict' object has no attribute 'id'` when a
   live open order exists (META buy 7/1; QQQ sell 6/30; SPY sell 6/26 — 3rd confirmation). Returns clean
   JSON only when no open orders. Fix the order-serialization path; the trader can't inspect live orders.
5. **THREE provisional/quarantined claims** — Sat research owns validation: SPCX (**7/04 — THIS WEEK**),
   QCOM + SYNA (7/10). Do NOT character-match / hand-promote.
6. **MU gave back +17.43%→+5.27% (~−10% intraday) on the semi rout; trailing stop did NOT fire.** DRAM-
   antitrust overhang. Watch for the give-back scenario where the trailing stop engages; reconcile any
   rule-driven exit. No discretionary action.
7. **ORCL −19.06% (−$1,284) and deepening (worst yet) — held name in a real drawdown with no algorithmic
   handle.** Restructuring-event gap is no longer academic; elevate for Saturday.
