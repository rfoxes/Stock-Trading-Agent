# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude (Wed 2026-06-17,
FOMC decision day). Yesterday's Claude wrote it after finishing today's work.
Replace it (don't append) when you write the version for the next Claude.

---

## STANDING POLICY (P0, do not ignore)

**Every symbol in the universe MUST be either (a) claimed by an active strategy
via algorithmic triage, or (b) flagged as a true library gap.** See `manual.md`
"P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE". `cli execute` REFUSES to run
if any symbol is unclaimed AND not in `state/library_gaps.md`. Use
`cli triage-symbol <SYM> [--gap-type X]` for every unclaimed symbol — auto-claims
if Sharpe ≥ 0.5, else auto-records a library gap. Character-match shortcuts and
direct YAML edits to `active_strategies.md` are FORBIDDEN.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps
(requests/alpaca-py/dotenv).** `python3 -m quant_trading_system.cli ...` fails with
`No module named 'requests'`. Confirmed still broken today (6/16).
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.
This is a known-good interpreter — it is NOT a "stop on ModuleNotFoundError"
situation; complete the run via the venv and document the drift.

## Status as of last update (2026-06-16, scheduled post-close run)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no
  `.py`/`.md` edits, no manual changes.
- **SPCX triaged → `true_library_gap`.** The operator-directed SPCX promotion
  (6/16 news run) made universe = 23 with SPCX unclaimed.
  `cli triage-symbol SPCX --gap-type volatility_regime` → no rankable winner
  (the only volatility_regime responders are options strategies the backtester
  can't score; SPCX is a 6/12 IPO with no price history). Auto-recorded in
  `state/library_gaps.md`; gate now tolerates it. **Saturday research owns the
  proper claim — do NOT character-match it.**
- **Active set: 7 strategies, 22/23 claimed; SPCX library-gap-flagged.** No changes.
- **Account: equity $108,012.46; cash $15,518.16; buying power $321,056.68.**
  (Down ~$391 on the chip-cohort intraday selloff; AVGO round-tripped to ~flat.)
- **Positions (6 longs, all green):** AAPL 72 (+10.25%), AVGO 26 (+0.11%),
  MU 7 (+5.59%), ORCL 38 (+5.66%), QQQ 28 (+12.83%), SPY 35 (+5.96%).
- **Regime: bull, conf 0.75, ADX 24.98** (unchanged).
- **News brief: FRESH today (6/16), NOTABLE.** First fresh brief in days
  (6/11–6/15 missed; prior 6/16 run saw a stale 6/15 brief).

## To do next run

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

3. **Snapshot + P0 triage.** `cli list-active`. SPCX should still show as the lone
   unclaimed symbol but library-gap-flagged (tolerated). If any NEW symbol is
   unclaimed and unflagged, run `cli triage-symbol <SYM> [--gap-type <type>]`. Do
   NOT use `cli add-active` for unclaimed symbols.

4. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held.
   If any exited via a strategy's logic, `log-closed <strategy_id> <SYM>
   <pnl_fraction>`. No action if all still held (entries don't get log-closed).

5. **Position watch:**
   - **MU pre-print window — Q3 FY26 = Tue 6/24 AMC.** Held +5.59%. 52-wk high,
     bullish flow into the print. `equity_event_driven_catalyst` window logic +
     trailing stop govern.
   - **QQX/QQQ — SPCX Nasdaq-100 rebalance (~July 1).** Soft awareness only:
     ~$22-27B forced SPCX buy reweights existing QQQ constituents over ~2 weeks.
     No active rule reads index-rebalance flow (correct). SPY insulated. Don't
     mistake rebalance pressure for fundamental weakness.
   - **AVGO (+0.11%, ~flat).** No fresh catalyst, next print September. Trust the
     rule's exit logic.

6. **Run `cli execute` (via venv).**

7. **Library gaps — see list below (Saturday research owns them).**

8. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps for the research agent (carry to research_tasks.md Sat)

- **SPCX claim (NEW, top-priority once it has bars).** Flagged `true_library_gap`
  6/16 — a 6/12 IPO with no price/indicator history whose only canonical responder
  type (`volatility_regime`) is served solely by options strategies the backtester
  can't score. Research owns the proper claim. Likely needs (a) a few sessions of
  bars before any equity strategy can backtest it, and/or (b) activating a
  vol-selling options strategy with backtester chain-data support.
- **`_load_news_brief()` has no staleness guard.** Parses `date_in_file` but never
  compares to today; a stale brief is fed to strategies as live signal. Top
  soft-signal item — the pipeline has been intermittently producing stale/no briefs.
  **Suggested research:** reject or down-weight a brief whose `date_in_file` != today.
- **`news_brief.has_positive_signal`/`has_negative_signal` keyword detector too
  coarse in both directions** (6/10 ORCL false NEGATIVE; 6/16 AVGO false POSITIVE,
  one-shot not compounding). **Suggested research:** rework keyword sets / add a
  confidence or freshness gate; consider `has_asymmetric_signal()` + a
  catalyst-strength threshold before `event_driven_catalyst` enters on a brief
  signal alone.
- **Validate the 5 first-pass + 3 provisional assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` vs ??? on CBRS, NUVL, TSM
- **Event-window coverage on price-claimed names** (META AI-Mode launch; NVDA
  ~$20-25B debt raise) — `event_catalyst` responder claims only AVGO/MU/ORCL, not
  META/NVDA. Broaden the claim set or add a lightweight event-window co-claim overlay.
- **`macro_event_window` overlay** (FOMC dot plot 6/16–17; import-price print) —
  NEW_CATEGORY_NEEDED; no canonical type covers scheduled macro events.
- **`vol_regime_shift` activation** (VIX 16.41, second day sub-20) — registry hole
  CLOSED (4 options strategies declare `volatility_regime`) but none active / none
  claim a universe symbol. Activate one vol-selling options strategy with a claim;
  this would also give SPCX a candidate responder.
- **Scheduled index-rebalance / forced-flow overlay** (SPCX → Nasdaq-100 ~July 1,
  Russell 6/26; QQQ reweight) — no rule reads a known rebalance schedule as a flow event.
- **AI-capex permitting / "$4.1T AI-debt" risk overlay** (ORCL/DELL/hyperscalers)
  — NEW_CATEGORY_NEEDED; structural policy/financing headwind, no responder.
- **AI-policy / export-control overlay** (Anthropic Fable/Mythos ban, Day 4-5) —
  no rule responds to national-security/export events. Soft signal only.
- **`underwriter_franchise_event` for JPM** (SpaceX IPO + options debut) — absent.
- **`m_a_arbitrage_event` (NUVL/GSK)** — `pairs_arbitrage` responder not active;
  NUVL claimed by trend-following (price-driven). Activation gap.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew
   3.14.5 (no harness deps). Repoint the Cowork task / daily_prompt to
   `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Persisting across runs. See last_handoff.md Open issue #1.
2. **News pipeline reliability.** Recovered today (fresh 6/16 brief) after 6/11–6/15
   were missed and the prior 6/16 run saw a stale 6/15 brief. Likely the same
   interpreter outage. Consider a health-check / alert on run failure.
3. **SPCX is a documented library gap, not a claim** — Sat research owns the proper
   head-to-head once SPCX has tradeable bars. Do NOT character-match it.
4. **NUVL/CBRS/TSM placeholder claims + 5 first-pass assignments** — Sat research priority.
5. **MU Q3 FY26 print Tue 6/24 AMC** — pre-print window open, position green.
