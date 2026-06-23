# Tasks for the next run

This file is the focused to-do list for the next run (Wed 2026-06-24 — **MU Q3 FY26
print day, Wed AMC**). Yesterday's Claude wrote it after the 6/23 (after-hours refresh)
run. Replace it (don't append) when you write the next version.

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
`No module named 'requests'`. Confirmed still broken 6/23. **RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a
"stop on ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF

The 6/22 Monday brief was SKIPPED; 6/23 recovered (incl. an after-hours refresh). **Always
check `news_brief.md`'s `# News brief for <date>` header matches today BEFORE trusting it.**
If it doesn't, treat the brief as ABSENT (proceed without live news per the manual) and
re-flag the news pipeline. Expect a fresh 6/24 brief covering CBRS's post-print reaction.

## Status as of last update (2026-06-23 after-hours refresh, AI/semis de-rating Day-2, NOTABLE)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no `.py`/`.md`
  edits, no manual changes.
- **NOTABLE brief: AI/semiconductor/memory de-rating ran into the 6/23 close** (S&P −1.44%,
  Nasdaq −2.21%, Dow ~flat on defensive rotation). New after-hours: **CBRS first public
  print −8% AH** (rev +94% beat, GM guide-down); **GOOGL → DJIA eff Mon 6/29** (forced flow).
  **NOT halt-worthy** (no FOMC this session; MU print is Wed 6/24 AMC not tonight; CBRS not
  held; the move is a tech de-rating, not a geopolitical shock — Iran oil waiver is
  risk-positive). Observe, don't override.
- **P0 = 0 unclaimed.** `cli list-active` → universe 23, **claimed 23, unclaimed_count 0,
  provisional_count 1**. No new unclaimed symbols → no triage.
- **SPCX = PROVISIONAL/UNVALIDATED, execution-quarantined, revalidate_by 2026-07-04**
  (still <60 bars; drawdown ~−30% from post-IPO high). Execute confirmed skip. Do NOT
  hand-promote.
- **Account: equity $105,957.17; cash $15,518.15; buying power $315,301.85.**
  (Down ~$531 vs the earlier 6/23 read $106,488.44 — the de-rating continuing.)
- **Positions (6 longs, 5 green):** AAPL 72 (+8.33%), AVGO 26 (+0.91%),
  MU 7 (**+8.12%** — held through the +25%→+7.6%→+8.1% round-trip, trailing stop did NOT
  fire), ORCL 38 (**−6.84%**, only red, widened on 21k job cuts), QQQ 28 (+10.19%),
  SPY 35 (+3.49%).
- **Regime: bull, conf 0.71, ADX 21.04** (unchanged).

## To do next run (Wed 6/24 — MU PRINT DAY, Wed AMC)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter (warning #1).
   **Date-check the brief** (warning #2) — expect a fresh 6/24 brief covering CBRS's 6/23
   post-print reaction.

2. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and SPCX still
   PROVISIONAL (revalidate_by 7/04). If any NEW symbol shows as unclaimed, run
   `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT use `cli add-active`.

3. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held. **MU is
   the one to watch** — if equity_event_driven_catalyst's trailing stop or window logic
   exited MU (or trimmed it) on its own rule, `log-closed equity_event_driven_catalyst MU
   <pnl_fraction>`. Do NOT discretionarily sell MU ahead of the print to "lock in" — that's
   forbidden. Let the rule decide.

4. **Position watch:**
   - **MU — Q3 FY26 print TODAY (Wed 6/24 AMC).** The trader run (~4pm PT / 7pm ET) sits
     around/after the print. Options priced ~14% move; history = fell after 6 of last 8
     reports despite beats. Held +8.12% (round-tripped from +25%). Anthropic-deal tailwind;
     SK Hynix HBM4-slowdown cross-current. `equity_event_driven_catalyst` window logic +
     trailing stop govern. **Watch the trailing stop** and reconcile any rule-driven exit.
     No discretionary action either way.
   - **ORCL — book's only red (−6.84%), widened on 21k job cuts.** No threshold breach, no
     rule fired, held. Workforce-reduction event has no algorithmic handle — soft library
     gap. Watch but no action unless a rule fires.
   - **CBRS — printed its first public quarter 6/23 AMC (−8% AH).** Check the 6/24 brief for
     the continued reaction. CBRS has no earnings-window responder (claimed by trend-following
     only) — assignment gap for Saturday. No action.
   - **GOOGL — joins DJIA eff Mon 6/29 (forced flow).** No active rule reads an
     index-rebalance schedule. Watch the brief; no action (index-rebalance overlay gap).
   - **MRVL/INTC — breakout_volume claims both;** both fell ~8% in the rout, no
     volume-confirmed breakout. Watch; if the gate isn't met, no trade is correct.

5. **Run `cli execute` (via venv).** SPCX appears under `provisional_quarantined`/`skipped`
   — expected, not an error. The AI/semis de-rating is realized price the rules see — if a
   trend/momentum rule fires on a rolling-over name, execute; if none fires, do-nothing is
   correct and non-curve-fit. Do NOT discretionarily de-risk the AI-cohort book — forbidden.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, deadline 2026-07-04).** Provisional claim on
  equity_trend_following_ema_cross, execution-quarantined. Research must backtest once SPCX
  has ≥60 bars and either VALIDATE (Sharpe ≥ 0.5 → trading claim) or ESCALATE. Drawdown
  ~−30% from post-IPO high; $20B debt raise + $6.3B Reflection compute deal (bond/equity
  signals diverging). Likely also wants a vol-selling options strategy activated as a
  candidate responder (hyper-IV new listing; volatility_regime).
- **Earnings-window activation on CBRS (printed first public quarter 6/23 AMC, −8% AH).**
  CBRS is claimed by trend-following (price-driven); the earnings_window responder
  (equity_event_driven_catalyst) does NOT claim it. Assign CBRS to the event-driven responder
  via head-to-head vs trend-following. gap_type: earnings_window — responder: NONE.
- **Index-rebalance / forced-flow overlay — multiple live instances (GOOGL → DJIA 6/29;
  SPCX → Nasdaq-100 ~July 1; Russell ~6/26; held QQQ).** No active rule reads a known
  index-rebalance schedule as a flow event. Open Q: should index-inclusion become a 6th
  Tier-B promotion trigger? gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction events (ORCL 21k job cuts).** ORCL is claimed by
  equity_event_driven_catalyst, but the strategy models earnings windows, not restructuring
  disclosures — no true handle even on a covered name. Decide whether a restructuring/
  cost-event sub-trigger belongs in the event-driven strategy. gap_type: event_catalyst —
  responder: partial (claimed, unmodeled).
- **Event-window coverage on price-claimed names (GOOGL DeepMind departure; META CRED
  investment + WhatsApp leadership; MSFT Chevron power deal; TSLA NHTSA probe/Megapod;
  DELL product launch; AAPL data leak; carry-forward INTC foundry-mgmt).** `event_catalyst`
  is declared only by equity_event_driven_catalyst (claims AVGO/MU/ORCL). Broaden its claim
  set to event-prone large caps OR add a lightweight event-window co-claim overlay. gap_type:
  event_catalyst — responder: NONE.
- **AI-capex financing / crowding overlay — ACTIVELY UNWINDING** (KOSPI −10%, Wall St Day-2
  de-rating on top of higher-for-longer-with-hike-bias). Cohort financing/leverage + crowding
  drawdown (held AVGO/MU/ORCL/QQQ + watchlist semis) with no rule flagging it. gap_type:
  NEW_CATEGORY_NEEDED — responder: NONE.
- **Macro-event-window category (FOMC higher-for-longer / hawkish dots; Citadel Sept-hike
  call).** No canonical gap_type covers a scheduled macro print. gap_type: NEW_CATEGORY_NEEDED
  — responder: NONE.
- **Vol-regime activation** (VIX ~17.3 sub-18; MU ~14% pre-print IV; CBRS realized ~−8%;
  SPCX hyper-IV). Registry hole CLOSED (volatility_regime declared by iron_condor_high_iv,
  calendar_spread, jade_lizard, long_straddle_earnings) but none active / none claim a
  universe symbol. Activate one vol strategy with a claim (MU pre-print is the textbook
  long-straddle/event-vol setup); doubles as SPCX candidate.
- **Validate the 5 first-pass + 3 provisional-placeholder assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` placeholders → CBRS, NUVL, TSM (CBRS → event-driven)
- **AI-policy / export-control overlay** (Anthropic Fable 5/Mythos 5 export ban; Sanders
  AI-equity-tax bill) — no rule responds to national-security/export/AI-tax events. Soft
  signal. gap_type: event_catalyst — responder: NONE.
- **`m_a_arbitrage_event` (NUVL/GSK)** — `pairs_arbitrage` responder
  (equity_pairs_trading_cointegration) not active; NUVL claimed by trend-following.
  Activation gap.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no
   harness deps). Repoint the Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall
   deps into 3.14, or recreate the venv. Persisting across many runs.
2. **News pipeline intermittent — 6/22 Monday run MISSED, 6/23 recovered.** Add a
   health-check / alert on news-agent run failure so a missed brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3) is the harness-side defense.
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to
   today; bit in practice 6/22. Reject/down-weight a brief whose date != today.
4. **SPCX PROVISIONAL, execution-quarantined** — Sat research owns validation by 2026-07-04
   (needs ≥60 bars). Do NOT character-match / hand-promote.
5. **MU Q3 FY26 print Wed 6/24 AMC (today, this run sits around/after it).** Held +8.12%
   (round-tripped from +25%); trailing stop did NOT fire. Options ~14% move. Watch the
   trailing stop; reconcile any rule-driven exit. No discretionary action.
6. **Higher-for-longer-with-a-HIKE-BIAS + AI-crowding actively unwinding.** Hawkish June-17
   dots; Citadel Sept-hike aligned; KOSPI −10% / Wall-St Day-2 de-rating. Whole book
   AI-cohort/rate-sensitive levered. No rule pre-positions (correct); watch for the de-rating
   reaching trend/momentum rules as realized price rolls over.
