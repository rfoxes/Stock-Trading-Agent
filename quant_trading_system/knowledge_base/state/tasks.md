# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude (Wed 2026-06-17,
**FOMC DECISION DAY**). Yesterday's Claude wrote it after finishing today's work.
Replace it (don't append) when you write the version for the next Claude.

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
fails with `No module named 'requests'`. Confirmed still broken today (6/16).
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.
NOT a "stop on ModuleNotFoundError" situation — complete the run via the venv and
document the drift.

## Status as of last update (2026-06-16, post-Option-3 scheduled run)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no
  `.py`/`.md` edits, no manual changes.
- **P0 = 0 unclaimed.** The news agent shipped the Option-3 / mandatory-attach
  doctrine earlier today, reconciling SPCX from `true_library_gap` into a
  PROVISIONAL claim. `cli list-active` → universe 23, **claimed 23,
  unclaimed_count 0, provisional_count 1**. No triage needed this run.
- **SPCX = PROVISIONAL/UNVALIDATED claim on equity_trend_following_ema_cross,
  execution-quarantined, revalidate_by 2026-06-30.** Execute confirmed it skips:
  `provisional_quarantined: ["SPCX"]`. It will NOT trade until Sat research
  validates. Do NOT promote it to a trading claim by hand.
- **Active set: 7 strategies, 23/23 claimed.** No changes.
- **Account: equity $107,963.82; cash $15,518.16; buying power $320,920.49.**
  (Down ~$49 — noise.)
- **Positions (6 longs, all green):** AAPL 72 (+10.19%), AVGO 26 (~flat, +0.008%),
  MU 7 (+5.38%), ORCL 38 (+5.60%), QQQ 28 (+12.80%), SPY 35 (+5.94%).
- **Regime: bull, conf 0.75, ADX 24.98** (unchanged).
- **News brief: FRESH today (6/16), NOTABLE.**

## To do next run (Wed 6/17 — FOMC DECISION DAY)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter
   (see warning above). **Check the brief's date matches today** — the pipeline
   has been flaky; verify it's fresh, not stale.

2. **FOMC DECISION DAY (Wed 6/17).** The dot plot + Warsh debut press conference
   land at 2:00/2:30 PM ET — DURING the session, before the post-close run. Hold
   ~97% priced; the dot plot is the surprise vector and the main risk to the
   AI-cohort multiple (whole book is AI-levered). No `macro_event_window` rule
   exists — you CANNOT pre-position (correct under the mandate). **Watch for
   dot-plot-driven price reactions that trip trend/momentum rules** in the execute
   output, and read the brief for a possible HALT-WORTHY flag if the print is a
   shock. Default standard execute otherwise.

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and
   SPCX still PROVISIONAL (revalidate_by 6/30). If any NEW symbol shows as
   unclaimed, run `cli triage-symbol <SYM> [--gap-type <type>]` (auto-claims or
   provisionally attaches). Do NOT use `cli add-active`.

4. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held.
   If any exited via a strategy's logic, `log-closed <strategy_id> <SYM>
   <pnl_fraction>`. No action if all still held (entries don't get log-closed).

5. **Position watch:**
   - **MU pre-print window — Q3 FY26 = Tue 6/24 AMC.** Held +5.38%. 52-wk high,
     bullish flow into the print. `equity_event_driven_catalyst` window logic +
     trailing stop govern.
   - **QQQ — SPCX Nasdaq-100 rebalance (~July 1).** Soft awareness only:
     ~$22-27B forced SPCX buy reweights existing QQQ constituents over ~2 weeks.
     No active rule reads index-rebalance flow (correct). SPY insulated. Don't
     mistake rebalance pressure for fundamental weakness.
   - **AVGO (~flat).** No fresh catalyst, next print September. Trust exit logic.

6. **Run `cli execute` (via venv).** SPCX will appear under
   `provisional_quarantined`/`skipped` — that's expected, not an error.

7. **Library gaps — see list below (Saturday research owns them).**

8. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, hard deadline 2026-06-30).** Provisional claim
  on equity_trend_following_ema_cross, execution-quarantined. Research must run a
  real backtest once SPCX has ≥60 bars (had 3 on 6/16) and either VALIDATE
  (Sharpe ≥ 0.5 → promote to a trading claim) or ESCALATE. Likely also wants a
  vol-selling options strategy activated as a candidate responder (hyper-IV new
  listing; `volatility_regime` type). Recorded in `state/provisional_claims.md`.
- **`_load_news_brief()` has no staleness guard.** Parses `date_in_file` but never
  compares to today; a stale brief is fed to strategies as live signal. Top
  soft-signal item. **Suggested:** reject or down-weight a brief whose
  `date_in_file` != today.
- **`news_brief.has_positive_signal`/`has_negative_signal` keyword detector too
  coarse** (6/10 ORCL false NEGATIVE; 6/16 AVGO false POSITIVE). **Suggested:**
  rework keyword sets / add confidence or freshness gate; consider
  `has_asymmetric_signal()` + a catalyst-strength threshold before
  `event_driven_catalyst` enters on a brief signal alone.
- **Validate the 5 first-pass + 3 provisional-placeholder assignments via
  head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` placeholders → CBRS, NUVL, TSM
- **Event-window coverage on price-claimed names** (META AI-Mode launch; NVDA
  ~$20-25B debt raise) — `event_catalyst` responder claims only AVGO/MU/ORCL, not
  META/NVDA. Broaden the claim set or add a lightweight event-window co-claim overlay.
- **`macro_event_window` overlay** (FOMC dot plot 6/16–17; import-price print) —
  NEW_CATEGORY_NEEDED; no canonical type covers scheduled macro events.
- **Vol-regime activation** (VIX 16.41, sub-20). Registry hole CLOSED (4 options
  strategies declare `volatility_regime`) but none active / none claim a universe
  symbol. Activate one vol-selling options strategy with a claim; doubles as the
  SPCX candidate responder.
- **Scheduled index-rebalance / forced-flow overlay** (SPCX → Nasdaq-100 ~July 1,
  Russell 6/26; QQQ reweight) — no rule reads a known rebalance schedule as a flow event.
- **AI-capex permitting / "$4.1T AI-debt" risk overlay** (ORCL/DELL/hyperscalers)
  — NEW_CATEGORY_NEEDED; structural policy/financing headwind, no responder.
- **AI-policy / export-control overlay** (Anthropic Fable/Mythos ban) — no rule
  responds to national-security/export events. Soft signal only.
- **`underwriter_franchise_event` for JPM** (SpaceX IPO + options debut) — absent.
- **`m_a_arbitrage_event` (NUVL/GSK)** — `pairs_arbitrage` responder not active;
  NUVL claimed by trend-following (price-driven). Activation gap.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew
   3.14.5 (no harness deps). Repoint the Cowork task / daily_prompt to
   `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Persisting across runs. See last_handoff.md Open issue #1.
2. **News pipeline reliability.** Recovered today (fresh 6/16 brief) after
   6/11–6/15 were missed. Likely the same interpreter outage. Consider a
   health-check / alert on run failure.
3. **SPCX is a PROVISIONAL, execution-quarantined claim** — Sat research owns
   validation by 2026-06-30 (needs ≥60 bars). Do NOT character-match / hand-promote.
4. **MU Q3 FY26 print Tue 6/24 AMC** — pre-print window open, position green.
