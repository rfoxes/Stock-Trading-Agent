# Tasks for the next run

This file is the focused to-do list for the next run (Mon 2026-06-22 — first cash
session after the Juneteenth holiday). Yesterday's Claude wrote it after finishing
the 6/19 (market-closed) run. Replace it (don't append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

**Every symbol in the universe MUST have a strategy attached — none is ever left
strategy-less.** See `manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED
RULE". Two grades of attachment:
- **(a) VALIDATED claim** — a library strategy cleared baseline Sharpe (0.5) in a
  `cli triage-symbol` backtest. Trades normally.
- **(b) PROVISIONAL claim** — nothing cleared baseline (or no price history), so
  triage attached the best-available strategy as an UNVALIDATED claim, recorded in
  `state/provisional_claims.md` with a `revalidate_by` deadline and
  **QUARANTINED from execution** (`cli execute` auto-skips it; see
  `provisional_quarantined`/`skipped` output). It never trades until Saturday
  research validates it.

After triage, `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM>
[--gap-type X]` for any NEW unclaimed symbol — it auto-claims OR provisionally
attaches. Character-match shortcuts and direct YAML edits to
`active_strategies.md` are FORBIDDEN. Never use `cli add-active` to bypass triage.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps
(requests/alpaca-py/dotenv).** Bare `python3 -m quant_trading_system.cli ...`
fails with `No module named 'requests'`. Confirmed still broken today (6/19).
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.
NOT a "stop on ModuleNotFoundError" situation — complete the run via the venv and
document the drift.

## Status as of last update (2026-06-19, Juneteenth — MARKET CLOSED, post-close run)

- **Today was Juneteenth: US markets CLOSED, no cash session.** Next open Mon 6/22.
  This run planned into Monday.
- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no
  `.py`/`.md` edits, no manual changes.
- **P0 = 0 unclaimed.** `cli list-active` → universe 23, **claimed 23,
  unclaimed_count 0, provisional_count 1**. No new unclaimed symbols → no triage.
- **SPCX = PROVISIONAL/UNVALIDATED claim on equity_trend_following_ema_cross,
  execution-quarantined, revalidate_by 2026-06-30.** Execute confirmed it skips
  (`provisional_quarantined: ["SPCX"]`). Now -20%+ from post-IPO high (Cursor-deal
  dilution) — research signal, not a trader action. Do NOT hand-promote.
- **Active set: 7 strategies, 23/23 claimed.** No changes.
- **Account: equity $109,484.18; cash $15,518.15; buying power $325,177.48.**
  (Flat vs 6/18 $109,459.46 — market closed; last-close marks.)
- **Positions (6 longs, all green):** AAPL 72 (+9.85%), AVGO 26 (+9.03%),
  MU 7 (**+15.37%**, running into the 6/24 print), ORCL 38 (+3.96%), QQQ 28 (+14.30%),
  SPY 35 (+5.35%).
- **Regime: bull, conf 0.73, ADX 22.63** (slight further softening from 23.38).
- **Macro:** higher-for-longer standing backdrop (~80% odds of ZERO 2026 cuts;
  Citadel Sept-hike call) + BofA "long-semis = most crowded trade in history."
  VIX last close 16.40 (sub-17 low-vol). US-Iran Geneva signing called off
  last-minute (NOT confirmed) — confirm over the weekend.

## To do next run (Mon 6/22 — first session post-holiday)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter
   (see warning above). **Check the brief's date matches Monday 6/22** — verify it's
   fresh, not the stale 6/19 holiday brief.

2. **MRVL is the most plausible firer Monday — let the volume gate decide.** Marvell's
   S&P 500 inclusion (with FLEX, replacing POOL/CPB) goes effective before Monday's
   open → potential passive-flow buy on a breakout-claimed name
   (equity_breakout_volume_confirmation). If the volume gate is met, executing is
   correct; if NOT met, no trade is correct. **Do NOT override the gate to chase the
   index-add flow.**

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and
   SPCX still PROVISIONAL (revalidate_by 6/30). If any NEW symbol shows as
   unclaimed, run `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT use
   `cli add-active`.

4. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held.
   If any exited via a strategy's logic, `log-closed <strategy_id> <SYM>
   <pnl_fraction>`. No action if all still held.

5. **Position watch:**
   - **MU pre-print window — Q3 FY26 CONFIRMED Wed 6/24 AMC.** Held and **running
     +15.37%**, riding the AI-memory demand stack. Monday is the last full session
     before the print. `equity_event_driven_catalyst` window logic + trailing stop
     govern. **Watch the trailing stop into the print** — a big unrealized gain is
     exactly what the trailing stop protects.
   - **INTC / MRVL — breakout_volume claims both.** Catalysts live (Intel foundry
     leadership hire; MRVL S&P add 6/22). Watch for a volume-confirmed entry; if the
     gate isn't met, no trade is correct. Don't override to chase.
   - **QQQ — SPCX Nasdaq-100 fast-entry (~July 1) + Russell 6/26.** Soft awareness:
     forced SPCX buy reweights existing QQQ constituents — but SPCX's -20% drawdown
     shrinks the dollar flow vs prior $22-27B estimate. No active rule reads it
     (correct). SPY insulated. Don't mistake rebalance pressure for fundamental weakness.

6. **Run `cli execute` (via venv).** SPCX appears under `provisional_quarantined`/
   `skipped` — expected, not an error.

7. **Library gaps — see list below (Saturday research owns them).**

8. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, hard deadline 2026-06-30).** Provisional claim
  on equity_trend_following_ema_cross, execution-quarantined. Research must run a
  real backtest once SPCX has ≥60 bars and either VALIDATE (Sharpe ≥ 0.5 → promote
  to a trading claim) or ESCALATE. Brief notes SPCX is now -20%+ from its high on the
  $60B Cursor-deal dilution (Grantham "could break the index"). Likely also wants a
  vol-selling options strategy activated as a candidate responder (hyper-IV new
  listing; `volatility_regime` type). Recorded in `state/provisional_claims.md`.
- **Scheduled index-rebalance / forced-flow overlay (MRVL/FLEX → S&P 500 6/22; SPCX →
  Nasdaq-100 ~July 1; Russell 6/26; held QQQ).** No active rule reads a known
  index-rebalance schedule as a flow event. MRVL's S&P add (Monday) and the QQQ
  reweight both qualify. Suggested research: an index-rebalance/forced-flow overlay
  (anticipated add/drop dates + estimated flow) as a soft posture signal. Open Q:
  should index-inclusion become a 6th Tier-B promotion trigger?
  gap_type: event_catalyst — responder: NONE.
- **US semiconductor industrial-policy / reshoring overlay (Intel foundry build-out).**
  Apple→Intel domestic-chip deal + the Lee (ex-SK Hynix CEO) EVP-Foundry hire — no
  rule maps a domestic-manufacturing policy/management catalyst to the affected names.
  INTC's only handle is breakout_volume (price); the policy/management event itself is
  unmodeled. gap_type: event_catalyst — responder: NONE.
- **Event-window coverage on price-claimed names (INTC foundry-mgmt; META/GOOGL
  regulatory [Ohio under-16 social-media law]; AMZN cost-curve commentary; QQQ
  rebalance flow).** `event_catalyst` is declared only by
  equity_event_driven_catalyst, which claims AVGO/MU/ORCL — not these names. Broaden
  its claim set to event-prone large caps OR add a lightweight event-window co-claim
  overlay alongside the price strategy. gap_type: event_catalyst — responder: NONE.
- **Macro-event-window category (FOMC higher-for-longer; Citadel Sept-hike call).**
  No canonical gap_type covers a scheduled macro print, no rule lets the trader
  pre-position/re-size around FOMC/CPI/jobs (correct under the mandate, but the
  soft-signal handle is missing). gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **AI-capex financing / crowding overlay** (ORCL/DELL/hyperscalers/semis) — the
  AI-trade-to-bond-market reframing + higher-for-longer + BofA's "most-crowded-trade-
  in-history" survey compound into a cohort financing/leverage + crowding headwind
  with no rule flagging it. gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX last close 16.40, sub-17). Registry hole CLOSED
  (volatility_regime declared by iron_condor_high_iv, calendar_spread, jade_lizard,
  long_straddle_earnings) but none active / none claim a universe symbol. Activate one
  vol-selling options strategy with a claim; doubles as the SPCX candidate responder.
- **`_load_news_brief()` has no staleness guard.** Parses `date_in_file` but never
  compares to today; a stale brief is fed to strategies as live signal. Top
  soft-signal item — especially relevant Monday (the 6/19 holiday brief must not be
  reused). Reject or down-weight a brief whose `date_in_file` != today.
- **`news_brief.has_positive_signal`/`has_negative_signal` keyword detector too
  coarse** (6/10 ORCL false NEGATIVE; 6/16 AVGO false POSITIVE). Rework keyword
  sets / add a confidence or freshness gate; consider `has_asymmetric_signal()` +
  a catalyst-strength threshold before `event_driven_catalyst` enters on a brief
  signal alone.
- **Validate the 5 first-pass + 3 provisional-placeholder assignments via
  head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` placeholders → CBRS, NUVL, TSM
- **AI-policy / export-control overlay** (Anthropic Fable 5/Mythos 5 export ban;
  Sanders AI-equity-tax bill) — no rule responds to national-security/export/AI-tax
  events. Soft signal. gap_type: event_catalyst — responder: NONE.
- **`m_a_arbitrage_event` (NUVL/GSK)** — `pairs_arbitrage` responder
  (equity_pairs_trading_cointegration) not active; NUVL claimed by trend-following
  (price-driven). Activation gap.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew
   3.14.5 (no harness deps). Repoint the Cowork task / daily_prompt to
   `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Persisting across many runs. See last_handoff.md Open issue #1.
2. **News pipeline reliability.** Fresh 6/16–6/19 briefs (holding) after 6/11–6/15
   misses. Consider a health-check / alert on run failure. Monday: confirm a fresh
   6/22 brief replaces the 6/19 holiday brief.
3. **SPCX is a PROVISIONAL, execution-quarantined claim** — Sat research owns
   validation by 2026-06-30 (needs ≥60 bars). Do NOT character-match / hand-promote.
4. **MU Q3 FY26 print CONFIRMED Wed 6/24 AMC** — pre-print window open, position
   running (+15.37%). Watch the trailing stop into the print. Monday is the last full
   session before it.
5. **Higher-for-longer + AI-crowding is the standing macro backdrop** (~80% odds of
   ZERO 2026 cuts; Citadel Sept-hike call; BofA "most crowded trade in history").
   Whole book AI-cohort/rate-sensitive levered; no rule pre-positions for it (correct).
   Watch for delayed de-rating as the AI-capex-financing reframing compounds.
6. **US-Iran Geneva signing called off last-minute (NOT confirmed).** Confirm over
   the weekend; don't mistake a treaty-fade in oil-sensitive names for fundamental
   weakness.
