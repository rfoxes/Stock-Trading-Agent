# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

---

## STANDING POLICY (P0, do not ignore)

**Every symbol in the universe MUST be either (a) claimed by an active
strategy via algorithmic triage, or (b) flagged as a true library gap.**
See `manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE".
`cli execute` REFUSES to run if any symbol is unclaimed AND not in
`state/library_gaps.md`. Use `cli triage-symbol <SYM> [--gap-type X]` for
every unclaimed symbol — auto-claims if Sharpe ≥ 0.5, else auto-records a
library gap. Character-match shortcuts and direct YAML edits to
`active_strategies.md` are FORBIDDEN.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps
(requests/alpaca-py/dotenv).** `python3 -m quant_trading_system.cli ...` fails
with `No module named 'requests'`. Confirmed still broken today (6/16).
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the broker cleanly.
Test `python3 -m quant_trading_system.cli account` once; if it ModuleNotFounds,
use the venv path. (The argparse `%`-escape crash in `cli.py:486` was fixed
6/16 — parser builds fine now.) This is a known-good interpreter reaching the
LIVE broker — it is NOT a "stop on ModuleNotFoundError" situation; complete
the run via the venv and document the drift.

## Status as of last update (2026-06-16, follow-on run)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no
  `.py`/`.md` edits, no manual changes.
- **Active set: 7 strategies, 22/22 claimed (unclaimed_count == 0).** No changes.
- **AVGO did NOT re-fire** despite the same stale 6/15 brief — it's now held,
  so the entry guard skips it. Confirms yesterday's keyword false-positive is a
  **one-shot entry, not a compounding buy loop**.
- **No reconciliation** — all 6 longs still held since the 6/16 run.
- **Account: equity $108,403.81; cash $15,518.16; buying power $322,152.46.**
- **Positions (6 longs, all green):** AAPL 72 (+10.23%), AVGO 26 (+0.54%),
  MU 7 (+6.87%), ORCL 38 (+6.91%), QQQ 28 (+13.40%), SPY 35 (+6.24%).
- **Regime: bull, conf 0.75, ADX 24.98** (unchanged).
- **News brief: STALE — dated 6/15, broker clock 6/16. No fresh brief for
  today.** Treated as soft/absent context; verified no held name has a negative
  signal (no stale-news exit risk).

## To do next run

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter
   (see warning above). **Check the brief's date matches today** — it was stale
   today and no fresh brief was produced.

2. **FOMC dot plot (June 16–17).** The live macro catalyst. Hold ~97% priced;
   the dot plot is the surprise vector and the main 48h risk to AI-cohort
   multiples. No `macro_event_window` rule exists — you CANNOT pre-position
   (correct under the mandate). Default standard execute unless the brief flags
   HALT-WORTHY EVENT. Watch for dot-plot-driven price reactions that trip
   trend/momentum rules.

3. **Snapshot + P0 triage.** `cli list-active`. If `unclaimed_count > 0`, run
   `cli triage-symbol <SYM> [--gap-type <type>]` per symbol. Do NOT use
   `cli add-active` for unclaimed symbols.

4. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still
   held. If any exited via a strategy's logic, `log-closed <strategy_id> <SYM>
   <pnl_fraction>`. No action if all still held (entries don't get log-closed).

5. **Position watch:**
   - **MU pre-print window — Q3 FY26 = Tue 6/24 AMC.** Held +6.87%.
     `equity_event_driven_catalyst` window logic + trailing stop govern.
   - **AVGO (weak-quality entry, +0.54%).** No fresh catalyst, next print Sept.
     Trust the rule's exit logic; it has not re-fired.
   - **ORCL +6.91%, AAPL/QQQ/SPY** — relief-rally beneficiaries; trust rules.

6. **Run `cli execute` (via venv).**

7. **Library gaps — see list below (unchanged; Saturday research owns them).**

8. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps for the research agent (carry to research_tasks.md Sat)

- **`_load_news_brief()` has no staleness guard.** It parses `date_in_file` but
  never compares to today, so a stale brief is fed to strategies as live signal.
  **This is now the TOP soft-signal item** — the news pipeline missed 6/11–6/15
  AND produced no fresh 6/16 brief, so stale-brief feeds are happening in
  practice. **Suggested research:** reject or down-weight a brief whose
  `date_in_file` != today.
- **`news_brief.has_positive_signal`/`has_negative_signal` keyword detector is
  too coarse in BOTH directions.** 6/10 ORCL = false NEGATIVE (missed capex-shock
  framing). 6/16 AVGO = false POSITIVE (matched a no-catalyst cohort mention →
  bought 26 sh). NOTE: confirmed 6/16 the false-positive is ONE-SHOT (held names
  skip entry), not compounding. **Suggested research:** rework keyword sets /
  add confidence or freshness gate; consider `has_asymmetric_signal()` and a
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
- **`macro_event_window` overlay** (FOMC dot plot June 16–17; Iran-deal resolution) — absent.
- **`vol_regime_shift_overlay`** (VIX broke below 20 to 17.68) — confirmed registry
  coverage hole; would also give `iron_condor_high_iv` a symbol to claim.
- **AI-policy / export-control shock overlay** (Anthropic Fable/Mythos foreign-user
  ban; NVDA-China substitution) — no rule responds to national-security/export events.
- **`underwriter_franchise_event` for JPM** (SpaceX listed; OpenAI Q4 listing pending) — absent.
- **`m_a_arbitrage_event` (NUVL/GSK)** — absent; NUVL pre-close.
- **AAPL WWDC / named-multi-day event-window posture** (`event_window_posture`) — absent.
- **AI-cohort multiple-compression overlay** — absent.

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew
   3.14.5 (no harness deps). Repoint the Cowork task / daily_prompt to
   `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Persisting across runs (6/16 and today). See last_handoff.md Open issue #1.
2. **News pipeline reliability.** No fresh brief was produced for today (6/16);
   the brief is dated 6/15. The news agent missed 6/11–6/15 too. Likely the same
   interpreter outage. Consider a health-check / alert on run failure.
3. **`cli open-orders` parser bug** appears RESOLVED under the venv (3.13).
   Confirm next time there's a live open order.
4. **AVGO keyword false-positive is one-shot, not compounding** — confirmed
   6/16 it did not re-fire (held → entry guard skips). Detector rework is the
   Sat research item.
5. **NUVL/CBRS/TSM placeholder claims + 5 first-pass assignments** — Sat research priority.
6. **MU Q3 FY26 print Tue 6/24 AMC** — pre-print window open, position green.
