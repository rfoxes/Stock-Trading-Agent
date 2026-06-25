# Tasks for the next run

This file is the focused to-do list for the next run (**Fri 2026-06-26**). Yesterday's Claude
wrote it after the 6/25 run (the day the trend-following EMA-cross rule fired a full SELL of
AAPL). Replace it (don't append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

**Every symbol in the universe MUST have a strategy attached — none is ever left
strategy-less.** See `manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE". Two
grades of attachment:
- **(a) VALIDATED claim** — a library strategy cleared baseline Sharpe (0.5) in a
  `cli triage-symbol` backtest. Trades normally.
- **(b) PROVISIONAL claim** — nothing cleared baseline (or no price history), so triage
  attached the best-available strategy as an UNVALIDATED claim, recorded in
  `state/provisional_claims.md` with a `revalidate_by` deadline and **QUARANTINED from
  execution** (`cli execute` auto-skips it). Never trades until Saturday research validates.

After triage, `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]`
for any NEW unclaimed symbol — it auto-claims OR provisionally attaches. Character-match
shortcuts and direct YAML edits to `active_strategies.md` are FORBIDDEN. Never use
`cli add-active` to bypass triage.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps
(requests/alpaca-py/dotenv).** Bare `python3 -m quant_trading_system.cli ...` fails with
`No module named 'requests'`. Confirmed still broken 6/25. **RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a
"stop on ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF — IT WAS STALE 6/25

The **6/25 brief was STALE** (carried the `2026-06-24` header on a 6/25 run) — treated as
absent. **6/22 Monday was also missed.** That's TWO misses this week. **Always check
`news_brief.md`'s `# News brief for <date>` header matches today BEFORE trusting it.** If it
doesn't, treat the brief as ABSENT (proceed on realized price per the manual) and re-flag the
news pipeline. A fresh 6/26 brief may or may not arrive — verify before relying on it.

## Status as of last update (2026-06-25, NOT a do-nothing day — AAPL EMA-cross SELL fired)

- **`cli execute` → 1 intent submitted:** `equity_trend_following_ema_cross` **SELL 72 AAPL**
  (full exit), order_id `44b8a706-2287-48d8-be5c-8aae4effbbae`, all 5 SafetyGate checks passed.
  Other 6 strategies → 0 intents. SPCX skipped (`provisional_quarantined`). **Decision: Keep** —
  clean rule-driven trend exit, no override, no edits, no rotation.
- **⚠️ THE AAPL SELL HAD NOT FILLED at session end** (`filled_qty: 0.0`; a re-read still showed
  AAPL 72 long). Submitted post-close (~16:12 PT) as a market order. **#1 reconciliation item
  below.**
- **P0 = 0 unclaimed.** `cli list-active` → universe 23, claimed 23, unclaimed_count 0,
  provisional_count 1. No new unclaimed → no triage.
- **SPCX = PROVISIONAL/UNVALIDATED, execution-quarantined, revalidate_by 2026-07-04**
  (still <60 bars). Execute confirmed skip. Do NOT hand-promote.
- **Account: equity $104,940.78; cash $15,518.15; buying power $312,455.95.**
  (Down ~$2,229 vs 6/24 read $107,169.58 — broad AI-cohort give-back.)
- **Positions (6 longs at read time, AAPL sell pending):** AAPL 72 (+1.64%, **SELL pending**),
  AVGO 26 (+0.39%), MU 7 (**+20.95%**, trailing stop did NOT fire), ORCL 38 (**−14.65%**, −$987,
  only red, deepening), QQQ 28 (+10.36%), SPY 35 (+3.47%).
- **Regime: bull, conf 0.71, ADX 21.23, realized_vol 0.169.**
- **Infra:** first `account` call DNS-failed transiently (re-run fine); `open-orders` parser bug
  REOPENED on the live AAPL order (`'dict' object has no attribute 'id'`).

## To do next run (Fri 6/26)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv (warning #1). **Date-check
   the brief** (warning #2) — the 6/25 brief was stale; verify the 6/26 header matches today.

2. **🔴 #1 RECONCILE THE AAPL EXIT.** Snapshot `positions`. Two cases:
   - **AAPL is GONE (sell filled):** run
     `log-closed equity_trend_following_ema_cross AAPL <pnl_fraction>`. Entry $271.30; if it
     filled ~$275–276 the realized fraction is ≈ **+0.016** (small gain). Use the actual fill
     price if you can get it. After this, the universe drops AAPL's hold but AAPL stays
     trend-following's CLAIM (still in the active set), so no triage churn.
   - **AAPL is STILL HELD (DAY order cancelled at session end):** the EMA-cross rule will very
     likely re-fire the SELL on `cli execute`. **Let it execute — do NOT cancel or override.**
     Then it becomes a same-day fill to reconcile next run.

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and SPCX still
   PROVISIONAL (revalidate_by 7/04). If any NEW symbol shows unclaimed, run
   `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT use `cli add-active`.

4. **Position watch:**
   - **AAPL — see #2.** Rule-driven exit in flight. No discretionary action either direction.
   - **MU — held +20.95%, trailing stop did NOT fire.** Slight give-back from +22.36%. Watch
     for IV-crush / deeper give-back where the trailing stop could finally engage. Reconcile any
     rule-driven exit. No discretionary action; do NOT sell to "lock in" the gain — forbidden.
   - **ORCL — −14.65% (−$987) and DEEPENING; book's only red.** Restructuring (21k cuts) has no
     algorithmic responder; event_driven_catalyst (claims ORCL) models earnings only. No rule
     can act — held. Now a material drawdown with no handle — elevated for Saturday. No action.
   - **AVGO/QQQ/SPY — gave back into the pullback but no rule fired.** Correct do-nothing unless
     a trend/momentum exit trips. No action.
   - **ARM/INTC/MRVL (breakout_volume); META/MSFT (macd); CSCO (bollinger); HPE (rsi);
     DELL (sector-rotation)** — no intents 6/25. Watch for their gates; no trade = correct if
     unmet.

5. **Run `cli execute` (via venv).** SPCX appears under `provisional_quarantined`/`skipped` —
   expected, not an error. React to realized price: if a rule fires (incl. a re-fired AAPL sell
   or a new trend/momentum signal), execute; if none fires, do-nothing is correct and
   non-curve-fit. Do NOT discretionarily de-risk or take profits.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, deadline 2026-07-04).** Provisional claim on
  equity_trend_following_ema_cross, execution-quarantined. Research must backtest once SPCX
  has ≥60 bars and either VALIDATE (Sharpe ≥ 0.5 → trading claim) or ESCALATE. Carry data:
  $25B unsecured-notes raise (post-$86B IPO), $6.3B Reflection compute deal, Nasdaq-100 add
  ~July 1. Likely also wants a vol-selling options strategy activated as a candidate responder.
- **Restructuring / workforce-reduction events (ORCL 21k cuts) — NOW MATERIAL (−14.65%, −$987,
  deepening).** ORCL is claimed by equity_event_driven_catalyst but the strategy models earnings
  windows, not restructuring — no handle even on a covered held name that is now in a meaningful
  drawdown. **Elevate this gap:** decide whether a restructuring/workforce-reduction sub-trigger
  belongs in event-driven, OR whether a generic price-based stop should co-cover event-driven's
  held names. gap_type: event_catalyst — responder: partial (claimed, unmodeled).
- **Earnings-window assignment on CBRS (printed first public quarter 6/23 AMC, −8% AH, slid
  further 6/24).** CBRS claimed by trend-following (price-driven); the earnings_window responder
  (equity_event_driven_catalyst) does NOT claim it. Assign CBRS to event-driven via head-to-head
  vs trend-following. gap_type: earnings_window — responder: NONE.
- **Product/partnership sub-trigger on event-driven covered names — AVGO Jalapeño (6/24).**
  AVGO IS claimed by equity_event_driven_catalyst, but the strategy models earnings windows,
  not product/partnership events. Decide whether a product/partnership sub-trigger belongs in
  event-driven. gap_type: event_catalyst — responder: partial (claimed, unmodeled).
- **Index-rebalance / forced-flow overlay (GOOGL → DJIA eff 6/29; SPCX → Nasdaq-100 ~July 1;
  held QQQ).** No active rule reads an index-rebalance schedule as a flow event. Open Q: should
  index-inclusion become a 6th Tier-B promotion trigger? gap_type: event_catalyst — responder:
  NONE. **NB: GOOGL DJIA inclusion is effective Mon 6/29 — the live instance lands next week.**
- **Event-window coverage on price-claimed names (GOOGL index/product; TSLA Sunrun 16-GW pact +
  NHTSA probe; AMZN Nokia/AWS expansion; META federal-testing pressure; carry GOOGL DeepMind,
  MSFT Chevron power deal, DELL launch, AAPL data leak).** `event_catalyst` is declared only by
  equity_event_driven_catalyst (claims AVGO/MU/ORCL). Broaden its claim set or add a lightweight
  event-window co-claim overlay. gap_type: event_catalyst — responder: NONE.
- **AI-capex financing / crowding overlay.** Cohort financing/leverage + crowding still has no
  rule (de-rating had recovered as of 6/24; 6/25 saw a broad give-back but not an acute unwind).
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Macro-event-window category (FOMC higher-for-longer / hawkish dots; oil/Iran macro;
  Citadel Sept-hike call).** No canonical gap_type covers a scheduled macro print.
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX ~19.5 region; MU post-print IV crush; CBRS first-print vol;
  SPCX hyper-IV). Registry hole CLOSED (volatility_regime declared by iron_condor_high_iv,
  calendar_spread, jade_lizard, long_straddle_earnings) but none active / none claim a universe
  symbol. Activate one vol strategy with a claim (MU post-print IV crush = textbook
  iron-condor/short-vol; doubles as SPCX candidate).
- **Validate the 5 first-pass + 3 provisional-placeholder assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` placeholders → CBRS, NUVL, TSM (CBRS → event-driven)
- **`m_a_arbitrage_event` (NUVL/GSK)** — `pairs_arbitrage` responder
  (equity_pairs_trading_cointegration) not active; NUVL claimed by trend-following.
  Activation gap.
- **AI-policy / export-control overlay** (META federal AI-testing pressure; carry Anthropic
  export ban, Sanders AI-equity-tax) — no rule responds to national-security/export/AI-tax/
  regulatory events. Soft signal. gap_type: event_catalyst — responder: NONE.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no
   harness deps). Repoint the Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall
   deps into 3.14, or recreate the venv. Persisting across many runs.
2. **[HIGH] News pipeline — 6/25 brief STALE (2nd miss this week; 6/22 also missed).** Add a
   health-check / alert on news-agent run failure so a missed/stale brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3).
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to
   today; bit in practice 6/22 AND 6/25. Reject/down-weight a brief whose date != today.
4. **[REOPENED] `cli open-orders` parser bug** — errors `'dict' object has no attribute 'id'`
   when a live open order exists (the AAPL sell 6/25). Returns clean JSON only when no open
   orders. Fix the order-serialization path; the trader can't inspect live orders via CLI.
5. **SPCX PROVISIONAL, execution-quarantined** — Sat research owns validation by 2026-07-04
   (needs ≥60 bars). Do NOT character-match / hand-promote.
6. **MU held +20.95%, trailing stop did NOT fire.** Watch Day-2 follow-through / IV crush for a
   give-back where the trailing stop could engage; reconcile any rule-driven exit. No
   discretionary action.
7. **ORCL −14.65% and deepening — held name in a real drawdown with no algorithmic handle.**
   The restructuring-event gap is no longer academic; elevate for Saturday research.
8. **First `account` call DNS-failed transiently 6/25** (re-run fine). Single blip; note if it
   recurs.
