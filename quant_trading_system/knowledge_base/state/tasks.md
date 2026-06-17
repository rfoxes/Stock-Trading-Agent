# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude (Thu 2026-06-18, the
session AFTER FOMC). Yesterday's Claude wrote it after finishing today's work.
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
fails with `No module named 'requests'`. Confirmed still broken today (6/17).
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.
NOT a "stop on ModuleNotFoundError" situation — complete the run via the venv and
document the drift.

## Status as of last update (2026-06-17, FOMC decision day, post-close run)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no
  `.py`/`.md` edits, no manual changes.
- **P0 = 0 unclaimed.** `cli list-active` → universe 23, **claimed 23,
  unclaimed_count 0, provisional_count 1**. No new unclaimed symbols → no triage.
- **SPCX = PROVISIONAL/UNVALIDATED claim on equity_trend_following_ema_cross,
  execution-quarantined, revalidate_by 2026-06-30.** Execute confirmed it skips
  (`provisional_quarantined: ["SPCX"]`). Do NOT hand-promote.
- **MRVL did NOT fire** despite the Jensen $2B-alliance catalyst (+3%) — the
  breakout strategy's volume-confirmation gate wasn't met. Correct algorithmic
  outcome; no action.
- **Active set: 7 strategies, 23/23 claimed.** No changes.
- **Account: equity $108,164.35; cash $15,518.15; buying power $321,481.95.**
  (UP ~$200 vs 6/16 even on a -1.2% index day — AI-memory cohort closed green.)
- **Positions (6 longs, all green):** AAPL 72 (+9.38%), AVGO 26 (+5.47%),
  MU 7 (+9.31%), ORCL 38 (+3.53%), QQQ 28 (+12.41%), SPY 35 (+5.01%).
- **Regime: bull, conf 0.75, ADX 24.98** (unchanged).
- **FOMC done:** hawkish dot-plot pivot (median 2026 dot 3.8%, cuts→hikes);
  VIX +12% to 18.44 (sub-20). Fully in prices.

## To do next run (Thu 6/18)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter
   (see warning above). **Check the brief's date matches today** — verify it's
   fresh, not stale.

2. **Post-FOMC backdrop.** The decision is done and in prices. Higher-for-longer
   is now the standing macro (median 2026 dot 3.8%, cuts→hikes). The whole book is
   AI-cohort/rate-sensitive levered. No rule pre-positions for rates (correct) —
   **watch the execute output for delayed de-rating reaching trend/momentum rules**
   (any trend-exit or RSI-divergence fires on the AI cohort). Default standard
   execute otherwise; no discretionary hedges.

3. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and
   SPCX still PROVISIONAL (revalidate_by 6/30). If any NEW symbol shows as
   unclaimed, run `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT use
   `cli add-active`.

4. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held.
   If any exited via a strategy's logic, `log-closed <strategy_id> <SYM>
   <pnl_fraction>`. No action if all still held.

5. **Position watch:**
   - **MU pre-print window — Q3 FY26 = Tue 6/24 AMC.** Held +9.31%, 52-wk-high
     area, bullish flow + same-day Cook memory-cost tailwind. `equity_event_driven_catalyst`
     window logic + trailing stop govern.
   - **MRVL — S&P 500 inclusion pending ~6/22** (passive-flow window) + Jensen $2B
     alliance. Breakout strategy claims it; watch for a volume-confirmed entry.
   - **QQQ — SPCX Nasdaq-100 rebalance (~July 1) + Russell 6/26.** Soft awareness:
     ~$22-27B forced SPCX buy reweights existing QQQ constituents over ~2 weeks.
     No active rule reads it (correct). SPY insulated. Don't mistake rebalance
     pressure for fundamental weakness.

6. **Run `cli execute` (via venv).** SPCX appears under `provisional_quarantined`/
   `skipped` — expected, not an error.

7. **Library gaps — see list below (Saturday research owns them).**

8. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, hard deadline 2026-06-30).** Provisional claim
  on equity_trend_following_ema_cross, execution-quarantined. Research must run a
  real backtest once SPCX has ≥60 bars (had ~4-5 on 6/17) and either VALIDATE
  (Sharpe ≥ 0.5 → promote to a trading claim) or ESCALATE. Likely also wants a
  vol-selling options strategy activated as a candidate responder (hyper-IV new
  listing; `volatility_regime` type). Recorded in `state/provisional_claims.md`.
- **Macro-event-window category (FOMC dot plot + retail sales).** Today's hawkish
  pivot is the cleanest exemplar yet: no canonical gap_type covers a scheduled
  macro print, no rule lets the trader pre-position/re-size around FOMC/CPI/jobs
  (correct under the mandate, but the soft-signal handle is missing).
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Event-window coverage on price-claimed names (AAPL guidance "100-year flood"
  memory-cost / price-hike warning; HPE-NVIDIA-Vultr partnership +4%; META KOSA
  reversal; NVDA export-policy de-escalation).** `event_catalyst` is declared only
  by equity_event_driven_catalyst, which claims AVGO/MU/ORCL — not
  AAPL/HPE/META/NVDA. Broaden its claim set to event-prone large caps OR add a
  lightweight event-window co-claim overlay alongside the price strategy.
  gap_type: event_catalyst — responder: NONE.
- **`_load_news_brief()` has no staleness guard.** Parses `date_in_file` but never
  compares to today; a stale brief is fed to strategies as live signal. Top
  soft-signal item. Reject or down-weight a brief whose `date_in_file` != today.
- **`news_brief.has_positive_signal`/`has_negative_signal` keyword detector too
  coarse** (6/10 ORCL false NEGATIVE; 6/16 AVGO false POSITIVE). Rework keyword
  sets / add confidence or freshness gate; consider `has_asymmetric_signal()` +
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
- **Vol-regime activation** (VIX 18.44, +12% on the dots; still sub-20). Registry
  hole CLOSED (4 options strategies declare `volatility_regime`) but none active /
  none claim a universe symbol. Activate one vol-selling options strategy with a
  claim; doubles as the SPCX candidate responder.
- **Scheduled index-rebalance / forced-flow overlay** (SPCX → Nasdaq-100 ~July 1,
  Russell 6/26; QQQ reweight) — no rule reads a known rebalance schedule as a flow event.
- **AI-capex permitting / "$4.1T AI-debt" financing-risk overlay** (ORCL/DELL/
  hyperscalers) — a higher-for-longer Fed compounds the leverage/permitting
  headwind. NEW_CATEGORY_NEEDED; no responder.
- **AI-policy / export-control overlay** (Anthropic Fable/Mythos ban; DeepSeek-
  blacklist delay) — no rule responds to national-security/export events. Soft signal.
- **`underwriter_franchise_event` for JPM** (SpaceX IPO + record options debut
  ~1.8M contracts / ~$2.8B premium day one) — absent. NEW_CATEGORY_NEEDED.
- **`m_a_arbitrage_event` (NUVL/GSK)** — `pairs_arbitrage` responder
  (equity_pairs_trading_cointegration) not active; NUVL claimed by trend-following
  (price-driven). Activation gap.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew
   3.14.5 (no harness deps). Repoint the Cowork task / daily_prompt to
   `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Persisting across many runs. See last_handoff.md Open issue #1.
2. **News pipeline reliability.** Fresh 6/16 and 6/17 briefs (holding) after
   6/11–6/15 misses. Consider a health-check / alert on run failure.
3. **SPCX is a PROVISIONAL, execution-quarantined claim** — Sat research owns
   validation by 2026-06-30 (needs ≥60 bars). Do NOT character-match / hand-promote.
4. **MU Q3 FY26 print Tue 6/24 AMC** — pre-print window open, position green (+9.31%).
5. **Higher-for-longer is now the standing macro backdrop** post-FOMC (median 2026
   dot 3.8%, cuts→hikes). Whole book AI-cohort/rate-sensitive levered; no rule
   pre-positions for rates (correct). Watch for delayed de-rating in coming sessions.
