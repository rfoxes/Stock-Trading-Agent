# Tasks for the next run

This file is the focused to-do list for the next run (**Wed 2026-07-01**). Yesterday's Claude
wrote it after the 6/30 run (QQQ EMA death-cross SELL fired, pending fill). Replace it (don't
append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

**Every symbol in the universe MUST have a strategy attached — none is ever left
strategy-less.** See `manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE". Two grades:
- **(a) VALIDATED claim** — a library strategy cleared baseline Sharpe (0.5) in a
  `cli triage-symbol` backtest. Trades normally.
- **(b) PROVISIONAL claim** — nothing cleared baseline (or no price history), so triage attached
  the best-available strategy as an UNVALIDATED claim, recorded in `state/provisional_claims.md`
  with a `revalidate_by` deadline and **QUARANTINED from execution** (`cli execute` auto-skips).
  Never trades until Saturday research validates.

After triage, `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]` for
any NEW unclaimed symbol. Character-match shortcuts and direct YAML edits to
`active_strategies.md` are FORBIDDEN. Never use `cli add-active` to bypass triage.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps.** Bare `python3 -m
quant_trading_system.cli ...` fails with `No module named 'requests'`. Confirmed still broken
6/30. **RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a
"stop on ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF

The **6/30 brief was FRESH** (header `2026-06-30` matched today) after the 6/29 miss — pipeline
recovered, but it's flaky (misses span 6/22, 6/25, 6/29). **Always check `news_brief.md`'s
`# News brief for <date>` header matches today BEFORE trusting it.** If it doesn't, treat the brief
as ABSENT (proceed on realized price) and re-flag the news pipeline.

## Status as of last update (2026-06-30, NOT a do-nothing day — QQQ EMA-cross SELL fired)

- **`cli execute` → 1 NEW intent submitted:** `equity_trend_following_ema_cross` **SELL 28 QQQ**
  (full exit), order_id `f75ca170-8cbe-4c01-ba64-67b4a6aa9111`, all 5 SafetyGate checks passed.
  **⚠️ NOT FILLED at session end** (`filled_qty 0.0`; post-close DAY market order). **#1
  reconciliation item below.** This is the anticipated follow-on to the SPY exit — trend-following
  held QQQ through the SPY/AAPL exits and the EMA cross has now flipped on QQQ. Other 6 strategies
  → 0 intents. **Decision: Keep.**
- **No reconcile this run** — positions unchanged vs 6/29 (AVGO/MU/ORCL/QQQ); SPY done 6/29.
- **P0 = 0 unclaimed.** No new universe member, no promotions. `list-active` → universe 26,
  claimed 26, unclaimed 0, provisional 3 (QCOM, SPCX, SYNA). Nothing to triage.
- **3 PROVISIONAL/quarantined claims:** SPCX (revalidate_by 2026-07-04 — NEXT checkpoint), QCOM +
  SYNA (revalidate_by 2026-07-10). Execute confirmed all three skipped. Do NOT hand-promote.
- **Account: equity $105,191.53; cash $61,107.79; buying power $367,865.63.** (+$529 vs 6/29.)
- **Positions (4 longs, QQQ sell pending):** AVGO 26 (+0.10%), MU 7 (**+17.43%**, trailing stop did
  NOT fire), ORCL 38 (**−17.20%**, −$1,158, only red, deepening), QQQ 28 (+13.58%, **SELL pending**).
- **Regime: bull, conf 0.74, ADX 23.72, realized_vol 0.1762.**
- **Infra:** `cli open-orders` parser bug REOPENED on the live QQQ order
  (`'dict' object has no attribute 'id'`) — same as the SPY order 6/26. Clean when no live order.
- **News brief FRESH (6/30), NORMAL FLOW.** Quarter-end AI-chip recovery (price, not news). New
  events all `responder: NONE` legal/regulatory on held/universe names (see library gaps).

## To do next run (Wed 7/1)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv (warning #1). **Date-check the
   brief** (warning #2). Note macro calendar: **ADP (June) Wed 7/1 8:15 AM ET; nonfarm payrolls
   Thu 7/2 8:30 AM ET** (pulled early ahead of July 4). Also effective 7/1: JPM $50B buyback, AWS
   GPU +20% pricing — both `responder: NONE`, realized price only.

2. **🔴 #1 RECONCILE THE QQQ EXIT.** Snapshot `positions`. Two cases:
   - **QQQ is GONE (sell filled):** run
     `log-closed equity_trend_following_ema_cross QQQ <pnl_fraction>`. Entry avg $647.96; if it
     filled ~$736 the realized fraction is ≈ **+0.136**. Use the actual fill price if you can get it
     (derive from cash delta if the journal hasn't stamped one, as was done for SPY/AAPL). After
     this, QQQ stays trend-following's CLAIM (still in the active set), so no triage churn.
   - **QQQ is STILL HELD (DAY order cancelled at session end):** the EMA-cross rule will very likely
     re-fire the SELL on `cli execute`. **Let it execute — do NOT cancel or override.**

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0`, `provisional_count: 3`
   (QCOM, SPCX, SYNA). If any NEW symbol shows unclaimed, run `cli triage-symbol <SYM>
   [--gap-type <type>]`. Do NOT use `cli add-active`.

4. **Position watch:**
   - **QQQ — see #2.** Rule-driven exit in flight. No discretionary action either direction.
   - **MU — held +17.43% (firmed again), trailing stop did NOT fire.** New DRAM-antitrust legal
     overhang (no rule reads it) + post-print IV crush. Watch IV-crush / give-back where the
     trailing stop could engage. No discretionary action; do NOT sell to "lock in" — forbidden.
   - **ORCL — −17.20% (−$1,158) and DEEPENING (worst yet); book's only red.** Restructuring (21k
     cuts) has no algorithmic responder; event_driven_catalyst (claims ORCL provisionally) models
     earnings only. Held; elevated for Saturday. No action.
   - **AVGO — +0.10% (recovered to flat); no rule fired.** Correct do-nothing.
   - **Others (ARM/INTC/MRVL, META/MSFT/SNDK, CSCO, HPE, DELL)** — 0 intents 6/30. Watch their
     gates; no trade = correct if unmet.

5. **Run `cli execute` (via venv).** SPCX/QCOM/SYNA appear under `provisional_quarantined`/
   `skipped` — expected. React to realized price: if a rule fires (a re-fired QQQ sell or a new
   signal), execute; if none fires, do-nothing is correct. Do NOT discretionarily de-risk or take
   profits.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **THREE provisional/quarantined validations (TOP PRIORITY):**
  - **SPCX** (trend-following, deadline **2026-07-04** — NEXT, needs ≥60 bars). Carry: Nasdaq-100
    add **Tue 7/7** (~$4.3B forced passive buying), elevated single-name IV, $25B notes raise,
    broke IPO price. Likely wants a vol-selling options responder.
  - **QCOM** (event-driven, deadline **2026-07-10**). Investor Day 6/25; top candidate Sharpe 0.0.
  - **SYNA** (pairs-cointegration, deadline **2026-07-10**). **Live merger-arb:** onsemi $7B
    all-stock (1.350 ON/sh, 19% premium, close mid-2027). Textbook long SYNA / short ON. The
    activation instance for the standing m_a_arbitrage gap — validate the pairs setup.
- **Litigation / antitrust event on a held name — NEW live instance MU (DRAM price-fixing class
  action, N.D. Cal., filed 6/25, surfaced 6/29–30).** No active rule reads a lawsuit/antitrust
  filing; MU's event-driven claim models earnings windows only (and is provisional). Build a
  litigation/regulatory sub-trigger in an event-window overlay. gap_type: event_catalyst —
  responder: NONE.
- **Regulatory / appellate event on held/universe names — AAPL (SCOTUS cert, Epic App-Store) +
  AMZN (ACCC Prime Video suit).** Price-claimed; no rule reads a court/agency action. Event-window
  overlay covering regulatory catalysts on large-caps. gap_type: event_catalyst — responder: NONE.
- **Cloud-pricing / capital-allocation event — AMZN (AWS +20% GPU pricing, eff 7/1).** Margin/
  revenue disclosure with no responder; AMZN price-claimed. Supplier-side mirror of the AAPL/MSFT
  device-cost pass-through theme. gap_type: event_catalyst — responder: NONE.
- **Partnership / customer-win event — NVDA (Palantir sovereign-AI pact).** No rule reads a named
  partnership; NVDA price-claimed. Same hole as the AVGO Jalapeño/OpenAI carry. gap_type:
  event_catalyst — responder: NONE.
- **Index-rebalance / forced-flow overlay — recurring cluster.** GOOGL→DJIA now live (consummated
  6/29); SPCX→Nasdaq-100 **Tue 7/7**; SK Hynix Nasdaq listing ~7/10; FTSE Russell reconstitution
  end-June; held QQQ exposed to quarter-end (6/30) rebalance. No active rule reads an
  index-rebalance schedule. Open Q: index-inclusion as a 6th Tier-B promotion trigger?
  gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction events (ORCL 21k cuts) — MATERIAL (−17.20%, −$1,158, worst
  yet, deepening).** ORCL claimed by event-driven but the strategy models earnings windows. Decide
  whether a restructuring sub-trigger belongs in event-driven OR a generic price-based stop should
  co-cover event-driven's held names. gap_type: event_catalyst — responder: partial (unmodeled).
- **Management/succession + capital-allocation events (JPM $50B buyback + dividend, eff 7/1).** No
  rule reads a buyback/dividend or CEO-succession event; JPM price-claimed (trend-following).
  gap_type: event_catalyst — responder: NONE.
- **Input-cost / margin-compression event on held/universe names (AAPL Mac/iPad, MSFT Xbox carry).**
  Price-claimed; no rule reads a cost/margin shock. Recurring (memory-cost pass-through across
  device makers). Build an event-window overlay co-claiming large-caps for cost/margin events.
  gap_type: event_catalyst — responder: NONE.
- **Earnings-window assignment on CBRS (printed 6/23 AMC, −8% AH, carry).** CBRS claimed by
  trend-following (price-driven); the earnings_window responder (equity_event_driven_catalyst) does
  NOT claim it. Assign CBRS to event-driven via head-to-head vs trend-following.
  gap_type: earnings_window — responder: NONE (assignment).
- **Macro-event-window category (jobs week 7/1 ADP + 7/2 payrolls; higher-for-longer Warsh SEP;
  May core PCE 3.4%).** No canonical gap_type covers a scheduled macro print. No rule lets the
  trader pre-position (correct under the mandate, but the soft-signal handle is missing).
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX 17.65, IV-rank below index >50 threshold; MU post-print IV crush;
  SPCX hyper-IV into the 7/7 add). volatility_regime is declared (iron_condor_high_iv,
  calendar_spread, jade_lizard, long_straddle_earnings) but none active / none claim a universe
  symbol. Activate one vol strategy with a claim (MU post-print IV crush = textbook iron-condor/
  short-vol; doubles as SPCX candidate).
- **AI-capex financing / crowding overlay + "Black June" rotation.** Cohort financing/leverage +
  crowding still has no rule. gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **AI-policy / export-control overlay** (INTC nationalization framing; carry META federal
  AI-testing, Anthropic export ban, Sanders AI-equity-tax) — no rule responds to national-security/
  export/AI-tax/regulatory events. gap_type: event_catalyst — responder: NONE.
- **Validate the first-pass + provisional assignments via head-to-head:**
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT (SNDK
    already validated for macd, Sharpe 2.254 — no head-to-head needed)
  - trend-following placeholders → AAPL, AMZN, CBRS, GOOGL, JPM, NUVL, NVDA, QQQ, SPY, TSLA, TSM
    (CBRS → event-driven)
  - QCOM provisional (event-driven) + SYNA provisional (pairs-cointegration) → validate or escalate

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no deps).
   Repoint the Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall deps into 3.14, or
   recreate the venv. Persisting across many runs.
2. **[HIGH] News pipeline flaky — FRESH 6/30 but missed 6/22 + 6/25 + 6/29.** Add a health-check /
   alert on news-agent run failure so a missed/stale brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3).
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to today.
   Reject/down-weight a brief whose date != today.
4. **[REOPENED] `cli open-orders` parser bug** — errors `'dict' object has no attribute 'id'` when
   a live open order exists (the QQQ sell 6/30; SPY sell 6/26). Returns clean JSON only when no
   open orders. Fix the order-serialization path; the trader can't inspect live orders via CLI.
5. **THREE provisional/quarantined claims** — Sat research owns validation: SPCX (7/04 — NEXT),
   QCOM + SYNA (7/10). Do NOT character-match / hand-promote.
6. **MU held +17.43% (firmed again), trailing stop did NOT fire.** New DRAM-antitrust legal
   overhang. Watch for IV-crush / give-back where the trailing stop could engage; reconcile any
   rule-driven exit. No discretionary action.
7. **ORCL −17.20% (−$1,158) and deepening (worst yet) — held name in a real drawdown with no
   algorithmic handle.** Restructuring-event gap is no longer academic; elevate for Saturday.
