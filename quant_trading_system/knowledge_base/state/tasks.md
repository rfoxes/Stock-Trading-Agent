# Tasks for the next run

This file is the focused to-do list for the next run (**Thu 2026-06-25** — day after MU's
Q3 FY26 record blowout print). Yesterday's Claude wrote it after the 6/24 (MU print day) run.
Replace it (don't append) when you write the next version.

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
`No module named 'requests'`. Confirmed still broken 6/24. **RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a
"stop on ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF

The 6/22 Monday brief was SKIPPED earlier; 6/23 and 6/24 were present and on-date. **Always
check `news_brief.md`'s `# News brief for <date>` header matches today BEFORE trusting it.**
If it doesn't, treat the brief as ABSENT (proceed without live news per the manual) and
re-flag the news pipeline.

## Status as of last update (2026-06-24 MU print day, NOTABLE, clean do-nothing)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no `.py`/`.md`
  edits, no manual changes.
- **MU PRINT IS OUT — RECORD BLOWOUT, RESOLVED TO THE UPSIDE.** Q3 FY26 rev $41.46B (record),
  non-GAAP EPS $25.11 vs ~$20.20; Q4 guide ~$50B / ~86% GM / EPS ~$31, far above Street.
  Stock +12–15% AH. **Held MU re-rated +8.12% → +22.36%.** equity_event_driven_catalyst fired
  **0 intents** — held, trailing stop did NOT trip, no rule-driven exit to log. The print was
  NOT halt-worthy (favorable + fully known by run time); let the rule process it, it held.
- **P0 = 0 unclaimed.** `cli list-active` → universe 23, **claimed 23, unclaimed_count 0,
  provisional_count 1**. No new unclaimed symbols → no triage.
- **SPCX = PROVISIONAL/UNVALIDATED, execution-quarantined, revalidate_by 2026-07-04**
  (still <60 bars). Execute confirmed skip. Do NOT hand-promote.
- **Account: equity $107,169.58; cash $15,518.15; buying power $318,696.60.**
  (Up ~$1,212 vs 6/23 read $105,957.17 — MU re-rate + broad rebound.)
- **Positions (6 longs, 5 green):** AAPL 72 (+7.64%), AVGO 26 (+3.16%, Jalapeño tailwind),
  MU 7 (**+22.36%** — the mover, held through the print, trailing stop intact),
  ORCL 38 (**−10.10%**, only red, deepened on 21k job-cut digestion), QQQ 28 (+11.64%),
  SPY 35 (+3.93%).
- **Regime: bull, conf 0.71, ADX 21.04** (unchanged).

## To do next run (Thu 6/25)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter (warning #1).
   **Date-check the brief** (warning #2) — expect a fresh 6/25 brief covering MU's Day-1
   post-print follow-through and any IV crush.

2. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and SPCX still
   PROVISIONAL (revalidate_by 7/04). If any NEW symbol shows as unclaimed, run
   `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT use `cli add-active`.

3. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held. **MU is
   still the one to watch** — if equity_event_driven_catalyst's trailing stop or post-print
   window logic exits/trims MU on its own rule (e.g., on an IV-crush give-back of the AH pop),
   `log-closed equity_event_driven_catalyst MU <pnl_fraction>`. Do NOT discretionarily sell
   MU to "lock in" the blowout gain — forbidden. Let the rule decide.

4. **Position watch:**
   - **MU — print OUT, held +22.36%; trailing stop did NOT fire on the +22% pop.** Day-1
     follow-through is the watch: an IV-crush + give-back of the AH pop is the scenario where
     the trailing stop could finally engage. Reconcile any rule-driven exit. No discretionary
     action.
   - **ORCL — book's only red (−10.10%), deepened on 21k job-cut digestion** (worst month
     since 2001). No threshold breach, no rule fired, held. Restructuring event has no
     algorithmic handle — soft library gap. Watch but no action unless a rule fires.
   - **AVGO — Jalapeño/OpenAI custom-silicon win (held, +3.16%).** Tailwind with no
     algorithmic handle (event-driven models earnings, not product deals). No action.
   - **CBRS — debut-print Day-1 follow-through (−8% AH 6/23, slid further 6/24).** No
     earnings-window responder (claimed by trend-following only) — assignment gap for
     Saturday. No action.
   - **GOOGL — joins DJIA eff Mon 6/29 (forced flow) + Gemini 3.5 product.** No active rule
     reads an index-rebalance schedule. Watch the brief; no action.
   - **ARM/INTC/MRVL — breakout_volume claims all three;** rebounded with the tape, watch for
     a volume-confirmed breakout. If the gate isn't met, no trade is correct.

5. **Run `cli execute` (via venv).** SPCX appears under `provisional_quarantined`/`skipped`
   — expected, not an error. React to realized price, not the narrative — if a trend/momentum
   rule or a trailing stop fires, execute; if none fires, do-nothing is correct and
   non-curve-fit. Do NOT discretionarily de-risk or take profits on the AI-cohort book.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, deadline 2026-07-04).** Provisional claim on
  equity_trend_following_ema_cross, execution-quarantined. Research must backtest once SPCX
  has ≥60 bars and either VALIDATE (Sharpe ≥ 0.5 → trading claim) or ESCALATE. New data:
  $25B unsecured-notes raise (post-$86B IPO), $6.3B Reflection compute deal, Nasdaq-100 add
  ~July 1. Likely also wants a vol-selling options strategy activated as a candidate responder
  (hyper-IV new listing; volatility_regime).
- **Earnings-window assignment on CBRS (printed first public quarter 6/23 AMC, −8% AH, slid
  further 6/24).** CBRS is claimed by trend-following (price-driven); the earnings_window
  responder (equity_event_driven_catalyst) does NOT claim it. Assign CBRS to the event-driven
  responder via head-to-head vs trend-following. gap_type: earnings_window — responder: NONE.
- **Product/partnership sub-trigger on event-driven covered names — AVGO Jalapeño (6/24).**
  AVGO IS claimed by equity_event_driven_catalyst, but the strategy models earnings windows,
  not product/partnership-deal events — a material custom-silicon win has no handle even on a
  covered held name (same shape as ORCL restructuring). Decide whether a product/partnership/
  restructuring sub-trigger belongs in the event-driven strategy. gap_type: event_catalyst —
  responder: partial (claimed, unmodeled).
- **Index-rebalance / forced-flow overlay — live instances (GOOGL → DJIA 6/29; SPCX →
  Nasdaq-100 ~July 1; held QQQ).** No active rule reads a known index-rebalance schedule as a
  flow event. Open Q: should index-inclusion become a 6th Tier-B promotion trigger?
  gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction events (ORCL 21k job cuts).** ORCL is claimed by
  equity_event_driven_catalyst, but the strategy models earnings windows, not restructuring
  disclosures — no true handle even on a covered name. gap_type: event_catalyst — responder:
  partial (claimed, unmodeled).
- **Event-window coverage on price-claimed names (GOOGL index/product; TSLA Sunrun 16-GW pact
  + NHTSA probe; AMZN Nokia/AWS expansion; META federal-testing pressure; carry-forward
  GOOGL DeepMind, MSFT Chevron power deal, DELL launch, AAPL data leak).** `event_catalyst` is
  declared only by equity_event_driven_catalyst (claims AVGO/MU/ORCL). Broaden its claim set
  to event-prone large caps OR add a lightweight event-window co-claim overlay. gap_type:
  event_catalyst — responder: NONE.
- **AI-capex financing / crowding overlay — de-rating RECOVERED 6/24** (risk-on rebound,
  Russell 2000 record, MU blowout reaffirmed memory demand). Cohort financing/leverage +
  crowding still has no rule; the acute Mon–Tue unwind has paused. gap_type:
  NEW_CATEGORY_NEEDED — responder: NONE.
- **Macro-event-window category (FOMC higher-for-longer / hawkish dots; oil/Iran macro;
  Citadel Sept-hike call).** No canonical gap_type covers a scheduled macro print.
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX ~19.5, crossed >18 on the de-rating; MU post-print IV crush;
  CBRS first-print vol; SPCX hyper-IV). Registry hole CLOSED (volatility_regime declared by
  iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings) but none active /
  none claim a universe symbol. Activate one vol strategy with a claim (MU post-print IV crush
  is the textbook iron-condor/short-vol setup; doubles as SPCX candidate).
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
- **AI-policy / export-control overlay** (META federal AI-testing pressure; carry-forward
  Anthropic export ban, Sanders AI-equity-tax) — no rule responds to national-security/
  export/AI-tax/regulatory events. Soft signal. gap_type: event_catalyst — responder: NONE.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no
   harness deps). Repoint the Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall
   deps into 3.14, or recreate the venv. Persisting across many runs.
2. **News pipeline intermittent — 6/22 Monday run MISSED; 6/23 + 6/24 recovered.** Add a
   health-check / alert on news-agent run failure so a missed brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3).
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to
   today; bit in practice 6/22. Reject/down-weight a brief whose date != today.
4. **SPCX PROVISIONAL, execution-quarantined** — Sat research owns validation by 2026-07-04
   (needs ≥60 bars). Do NOT character-match / hand-promote.
5. **MU Q3 FY26 print resolved — record blowout, held +22.36%, trailing stop did NOT fire.**
   Watch Day-1 follow-through / IV crush for a give-back where the trailing stop could engage;
   reconcile any rule-driven exit. No discretionary action.
6. **Higher-for-longer-with-a-hike-bias backdrop; AI-crowding de-rating RECOVERED.** Hawkish
   June-17 dots; Citadel Sept-hike aligned. Whole book AI-cohort/rate-sensitive levered. No
   rule pre-positions (correct); watch for any renewed roll-over reaching trend/momentum rules.
