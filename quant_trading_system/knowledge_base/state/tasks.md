# Tasks for the next run

This file is the focused to-do list for the next run (**Mon 2026-06-29**). Yesterday's Claude
wrote it after the 6/26 run (AAPL exit reconciled + filled; a NEW EMA-cross SELL of SPY fired and
is pending). Replace it (don't append) when you write the next version.

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
6/26. **RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a
"stop on ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF

The **6/26 brief was FRESH** (header matched today) after 6/22 + 6/25 misses — pipeline
recovered, but it's flaky. **Always check `news_brief.md`'s `# News brief for <date>` header
matches today BEFORE trusting it.** If it doesn't, treat the brief as ABSENT (proceed on realized
price) and re-flag the news pipeline.

## Status as of last update (2026-06-26, NOT a do-nothing day — SPY EMA-cross SELL fired)

- **AAPL exit (from 6/25) FILLED + reconciled.** `log-closed equity_trend_following_ema_cross
  AAPL 0.0137` done (entry $271.30 → fill ≈ $275.01, +1.37%). AAPL no longer held; still
  trend-following's CLAIM.
- **`cli execute` → 1 NEW intent submitted:** `equity_trend_following_ema_cross` **SELL 35 SPY**
  (full exit), order_id `f2d8e13e-8a32-483f-89e9-3ba8dff43519`, all 5 SafetyGate checks passed.
  **⚠️ NOT FILLED at session end** (`filled_qty 0.0`; post-close DAY market order). **#1
  reconciliation item below.** Other 7 strategies → 0 intents. **Decision: Keep.**
- **P0 = 0 unclaimed.** Triaged the 3 unclaimed: **SNDK → CLAIMED** (momentum_macd_histogram,
  Sharpe 2.254); **QCOM → PROVISIONAL** (event-driven); **SYNA → PROVISIONAL**
  (pairs-cointegration, newly activated). `list-active` → universe 26, claimed 26, unclaimed 0,
  provisional 3.
- **3 PROVISIONAL/quarantined claims:** SPCX (revalidate_by 2026-07-04), QCOM + SYNA (revalidate_by
  2026-07-10). Execute confirmed all three skipped. Do NOT hand-promote.
- **Account: equity $103,770.30; cash $35,318.52; buying power $332,939.05.** (−$1,170 vs 6/25;
  cash +$19.8K from AAPL sale.)
- **Positions (5 longs, SPY sell pending):** AVGO 26 (−2.99%), MU 7 (**+14.86%**, gave back from
  +20.95%, trailing stop did NOT fire), ORCL 38 (**−15.98%**, −$1,077, only red, deepening),
  QQQ 28 (+9.00%), SPY 35 (+3.18%, **SELL pending**).
- **Regime: bull, conf 0.72, ADX 21.52, realized_vol 0.1665.**
- **Infra:** `cli open-orders` parser bug REOPENED on the live SPY order
  (`'dict' object has no attribute 'id'`). No DNS blip this run.

## To do next run (Mon 6/29)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv (warning #1). **Date-check the
   brief** (warning #2). Note: **GOOGL → DJIA inclusion is effective pre-open Mon 6/29** — the
   live forced-flow instance lands; no rule reads it (library gap), realized price only.

2. **🔴 #1 RECONCILE THE SPY EXIT.** Snapshot `positions`. Two cases:
   - **SPY is GONE (sell filled):** run
     `log-closed equity_trend_following_ema_cross SPY <pnl_fraction>`. Entry $708.81; if it filled
     ~$731 the realized fraction is ≈ **+0.032**. Use the actual fill price if you can get it
     (derive from cash delta if the journal hasn't stamped one, as I did for AAPL). After this,
     SPY stays trend-following's CLAIM (still in the active set), so no triage churn.
   - **SPY is STILL HELD (DAY order cancelled at session end):** the EMA-cross rule will very
     likely re-fire the SELL on `cli execute`. **Let it execute — do NOT cancel or override.**

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0`, `provisional_count: 3`
   (SPCX, QCOM, SYNA). If any NEW symbol shows unclaimed, run `cli triage-symbol <SYM>
   [--gap-type <type>]`. Do NOT use `cli add-active`.

4. **Position watch:**
   - **SPY — see #2.** Rule-driven exit in flight. No discretionary action either direction.
   - **QQQ — held +9.00%, claimed by trend-following alongside SPY; its EMA cross has NOT flipped.**
     Watch whether it follows SPY into a death-cross exit. No discretionary action.
   - **MU — held +14.86%, gave back from +20.95%, trailing stop did NOT fire.** Watch IV-crush /
     deeper give-back where the trailing stop could engage. No discretionary action; do NOT sell
     to "lock in" — forbidden.
   - **ORCL — −15.98% (−$1,077) and DEEPENING; book's only red.** Restructuring (21k cuts) has no
     algorithmic responder; event_driven_catalyst (claims ORCL) models earnings only. Held;
     elevated for Saturday. No action.
   - **AVGO — −2.99%, gave back into the chip pullback; no rule fired.** Correct do-nothing.
   - **Others (ARM/INTC/MRVL, META/MSFT/SNDK, CSCO, HPE, DELL)** — no intents 6/26. Watch their
     gates; no trade = correct if unmet. **SNDK is now actively claimed (momentum_macd) and trades.**

5. **Run `cli execute` (via venv).** SPCX/QCOM/SYNA appear under `provisional_quarantined`/
   `skipped` — expected. React to realized price: if a rule fires (a re-fired SPY/AAPL-style sell,
   a QQQ death cross, or a new signal), execute; if none fires, do-nothing is correct. Do NOT
   discretionarily de-risk or take profits.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **THREE provisional/quarantined validations now (TOP PRIORITY):**
  - **SPCX** (trend-following, deadline **2026-07-04**, needs ≥60 bars). Carry: $25B notes raise,
    $6.3B Reflection deal, broke $135 IPO price (−32% from peak) amid IG bond sell-off, OpenAI
    reportedly delaying IPO to 2027, Nasdaq-100 add ~July 1. Likely wants a vol-selling options
    responder.
  - **QCOM** (event-driven, deadline **2026-07-10**). Investor Day 6/25; top candidate Sharpe 0.0.
  - **SYNA** (pairs-cointegration, NEWLY ACTIVATED, deadline **2026-07-10**). **Live merger-arb:**
    onsemi $7B all-stock (1.350 ON/sh, 19% premium, close mid-2027). Textbook long SYNA / short ON.
    This is the activation instance for the standing m_a_arbitrage gap — validate the pairs setup.
- **Input-cost / margin-compression event on held/universe names — TWO instances (AAPL Mac/iPad
  6/25, MSFT Xbox 6/26).** Both price-claimed (trend-following / MACD); no rule reads a cost/margin
  shock. Recurring (memory-cost pass-through across device makers). Build an event-window overlay
  co-claiming large-caps for cost/margin events. gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction events (ORCL 21k cuts) — NOW MATERIAL (−15.98%, −$1,077,
  deepening).** ORCL claimed by event-driven but the strategy models earnings windows. Decide
  whether a restructuring sub-trigger belongs in event-driven OR a generic price-based stop should
  co-cover event-driven's held names. gap_type: event_catalyst — responder: partial (unmodeled).
- **Management/succession event (JPM leadership shake-up, 6/26).** No rule reads a CEO-succession/
  board-change event; JPM price-claimed (trend-following). gap_type: event_catalyst — responder: NONE.
- **Index-rebalance / forced-flow overlay — THREE live instances.** GOOGL → DJIA eff Mon 6/29
  (forced buy); SPCX → Nasdaq-100 ~July 1; SK Hynix Nasdaq listing ~July 10; held QQQ/SPY exposed
  to quarter-end (6/30) rebalance. No active rule reads an index-rebalance schedule. Open Q:
  index-inclusion as a 6th Tier-B promotion trigger? gap_type: event_catalyst — responder: NONE.
- **Capital-allocation event (JPM $50B buyback + dividend).** No rule reads a buyback/dividend
  authorization. gap_type: event_catalyst — responder: NONE.
- **Earnings-window assignment on CBRS (printed 6/23 AMC, −8% AH, slid further).** CBRS claimed by
  trend-following (price-driven); the earnings_window responder (equity_event_driven_catalyst)
  does NOT claim it. Assign CBRS to event-driven via head-to-head vs trend-following.
  gap_type: earnings_window — responder: NONE (assignment).
- **Product/partnership sub-trigger on event-driven covered names — AVGO Jalapeño (carry).** AVGO
  claimed by event-driven, but the strategy models earnings windows, not product/partnership
  events. gap_type: event_catalyst — responder: partial.
- **Event-window coverage on price-claimed names (TSLA Musk-testimony + Slate $25k EV; INTC US
  equity-stake overhang; DELL Texas reincorporation; GOOGL talent attrition; AMZN reads).**
  event_catalyst is declared only by equity_event_driven_catalyst (claims AVGO/MU/ORCL/QCOM).
  Broaden its claim set or add a lightweight event-window co-claim overlay.
  gap_type: event_catalyst — responder: NONE.
- **AI-capex financing / crowding overlay + "Black June" rotation.** Cohort financing/leverage +
  crowding still has no rule (6/26 saw AI-chip profit-taking, MAGS worst month since inception, but
  not an acute unwind). gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Macro-event-window category (hot May PCE core 3.4%; higher-for-longer SEP; oil/Iran macro).**
  No canonical gap_type covers a scheduled macro print. gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX ~18.9; MU post-print IV crush; SPCX hyper-IV). volatility_regime
  is declared (iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings) but none
  active / none claim a universe symbol. Activate one vol strategy with a claim (MU post-print IV
  crush = textbook iron-condor/short-vol; doubles as SPCX candidate).
- **Validate the first-pass + provisional assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
    (SNDK now validated for macd, Sharpe 2.254 — no head-to-head needed)
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - trend-following placeholders → AMZN, CBRS, GOOGL, JPM, NUVL, NVDA, QQQ, SPY, TSLA, TSM, AAPL
    (CBRS → event-driven)
  - QCOM provisional (event-driven) + SYNA provisional (pairs-cointegration) → validate or escalate
- **AI-policy / export-control overlay** (INTC nationalization framing; carry META federal
  AI-testing, Anthropic export ban, Sanders AI-equity-tax) — no rule responds to national-security/
  export/AI-tax/regulatory events. gap_type: event_catalyst — responder: NONE.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no deps).
   Repoint the Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall deps into 3.14, or
   recreate the venv. Persisting across many runs.
2. **[HIGH] News pipeline flaky — recovered 6/26 but missed 6/22 + 6/25.** Add a health-check /
   alert on news-agent run failure so a missed/stale brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3).
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to today.
   Reject/down-weight a brief whose date != today.
4. **[REOPENED] `cli open-orders` parser bug** — errors `'dict' object has no attribute 'id'` when
   a live open order exists (the SPY sell 6/26). Returns clean JSON only when no open orders. Fix
   the order-serialization path; the trader can't inspect live orders via CLI.
5. **THREE provisional/quarantined claims** — Sat research owns validation: SPCX (7/04), QCOM +
   SYNA (7/10). Do NOT character-match / hand-promote.
6. **MU held +14.86% (gave back from +20.95%), trailing stop did NOT fire.** Watch for IV-crush /
   give-back where the trailing stop could engage; reconcile any rule-driven exit. No discretionary
   action.
7. **ORCL −15.98% (−$1,077) and deepening — held name in a real drawdown with no algorithmic
   handle.** Restructuring-event gap is no longer academic; elevate for Saturday research.
