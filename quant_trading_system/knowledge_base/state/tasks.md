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

## ⚠️ READ FIRST: THE HARNESS INTERPRETER IS BROKEN FOR BARE `python3`

**Homebrew upgraded `/opt/homebrew/bin/python3` to 3.14.5, which is missing
the harness deps (requests/alpaca-py/dotenv).** `python3 -m quant_trading_system.cli ...`
fails with `No module named 'requests'`. **RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the broker cleanly.
If the operator has repointed the scheduled task or reinstalled deps into
3.14, bare `python3` may work again — test `python3 -m quant_trading_system.cli account`
once; if it errors with ModuleNotFoundError, fall back to the venv path
above. (A separate argparse `%`-escape crash in `cli.py:486` was FIXED on
6/16 — `%`→`%%` — so the parser itself builds fine now.)

## Status as of last update (Tue 2026-06-16, post-close)

- **First run since Wed 6/10** — Thu 6/11 / Fri 6/12 / Mon 6/15 did NOT execute
  (harness was down on the interpreter drift). Repaired and ran today.
- **Active set: 7 strategies, 22/22 claimed (unclaimed_count == 0).** No changes.
- **Today's execute: 1 intent submitted+filled.** `equity_event_driven_catalyst`
  → **AVGO buy 26 @ market** (order_id `77017d1b-ccfe-4f40-97da-5e3f74af47ce`).
  All 5 SafetyGate checks passed. **This was a keyword-detector FALSE POSITIVE**
  (brief said AVGO had no fresh catalyst) — rule governed, not overridden;
  reinforced library gap below.
- **6 other strategies: 0 intents.**
- **No reconciliation** — nothing closed since 6/10; ORCL (Wed buy) filled at
  $177.28 and is now a held long.
- **Account: equity ~$108,250; cash ~$15,518 (net-long now post-AVGO);
  buying power ~$321,720.**
- **Positions (6 longs, all green): AAPL 72 (+10.07%), MU 7 (+7.03%), ORCL 38
  (+7.25%), QQQ 28 (+13.53%), SPY 35 (+6.30%), AVGO 26 (new today).**
- **Regime: bull, conf 0.75, ADX 24.98.**
- **News brief: PRESENT (dated 6/15, NOTABLE — Iran peace deal relief rally,
  VIX below 20).**

## To do Wednesday (2026-06-17)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter
   (see warning above).

2. **FOMC dot plot is TODAY (Wed 6/17).** Hold is ~97% priced; the dot plot is
   the live catalyst and the main 48h risk to AI-cohort multiples. No
   `macro_event_window` rule exists — you CANNOT pre-position (correct under the
   mandate). Depending on run timing the decision may land before/during/after
   your run; rules react to price after the fact. Default standard execute unless
   the brief flags HALT-WORTHY EVENT.

3. **Snapshot + P0 triage.** `cli list-active`. If `unclaimed_count > 0`, run
   `cli triage-symbol <SYM> [--gap-type <type>]` per symbol. Do NOT use
   `cli add-active` for unclaimed symbols.

4. **Reconcile.** Confirm the 6 longs (incl. AVGO) are still held. If AVGO/ORCL/MU
   exited via the event-driven strategy's logic, `log-closed equity_event_driven_catalyst
   <SYM> <pnl_fraction>`. No action if all still held (entries don't get log-closed).

5. **Position watch:**
   - **MU pre-print window — Q3 FY26 = Tue 6/24 AMC.** Held +7%, surging into the
     print. `equity_event_driven_catalyst` window logic + trailing stop govern.
   - **AVGO (new, weak-quality entry).** Watch behavior; no fresh catalyst, next
     print September. Trust the rule's exit logic.
   - **ORCL +7%** — Wed catalyst buy working; trust exit logic.
   - **AAPL/QQQ/SPY** — broad-rally beneficiaries, trend-following claims AAPL/QQQ/SPY.

6. **Run `cli execute` (via venv).** Watch for any dot-plot-driven price reactions
   that trip trend/momentum rules.

7. **Library gaps — see list below.**

8. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps for the research agent (carry to research_tasks.md Sat)

- **REINFORCED (6/16): `news_brief.has_positive_signal`/`has_negative_signal`
  keyword detector is too coarse in BOTH directions.** 6/10 ORCL = false NEGATIVE
  (missed capex-shock framing). 6/16 AVGO = false POSITIVE (matched a no-catalyst
  cohort mention → bought 26 shares the news agent itself said had no fresh
  catalyst). **Suggested research:** rework the keyword sets / add a confidence
  or freshness gate; consider `has_asymmetric_signal()`; possibly require a
  catalyst-strength threshold before `event_driven_catalyst` enters on a brief
  signal alone.
- **NEW (6/16): `_load_news_brief()` has no staleness guard.** It parses
  `date_in_file` but never compares to today, so a stale brief is fed to
  strategies as live signal. Latent liquidation/entry risk if the news agent
  ever misses a day (it missed 6/11-6/15 this week). **Suggested research:**
  reject or down-weight a brief whose `date_in_file` != today.
- **Validate the 5 first-pass + 3 provisional assignments via head-to-head:**
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_trend_following_ema_cross` vs ??? on CBRS, NUVL, TSM
- **`macro_event_window` overlay** (FOMC dot plot Wed 6/17; Iran-deal resolution) — absent.
- **`vol_regime_shift_overlay`** (VIX broke below 20 to 17.68) — confirmed registry
  coverage hole; would also give `iron_condor_high_iv` a symbol to claim.
- **AI-policy / export-control shock overlay** (Anthropic Fable/Mythos foreign-user
  ban; NVDA-China substitution) — no rule responds to national-security/export events.
- **`underwriter_franchise_event` for JPM** (SpaceX listed; OpenAI Q4 listing pending) — absent.
- **`m_a_arbitrage_event` (NUVL/GSK)** — absent; NUVL pre-close.
- **AAPL WWDC / named-multi-day event-window posture** (`event_window_posture`) — absent.
- **AI-cohort multiple-compression overlay** — absent.
- **Cross-sector defensive rotation overlay** — absent (less urgent on the relief tape).

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew
   3.14.5 (no harness deps). Repoint the Cowork task / daily_prompt to
   `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Until then every automated run fails at context-build unless Claude falls
   back to the venv manually (as I did today). See last_handoff.md Open issue #1.
2. **argparse `%` crash FIXED (`cli.py:486`, `%`→`%%`).** No action; informational.
3. **`cli open-orders` parser bug appears RESOLVED** under the venv (3.13) — the
   `'dict' object has no attribute 'id'` error did not reproduce. Confirm next
   time there's a live open order.
4. **AVGO bought on a coarse keyword false-positive** — rule governed (not
   overridden). Detector rework is the Sat research item.
5. **Missed runs 6/11, 6/12, 6/15** — all due to the interpreter outage. State
   files were last updated 6/10 until today. If the scheduled task ran and
   silently failed those days, the failures weren't surfaced — consider a
   health-check / alert on run failure.
6. **NUVL/CBRS/TSM placeholder claims + 5 first-pass assignments** — Sat research priority.
7. **FOMC June 16-17 dot plot Wed** — the live macro catalyst; no pre-position rule.
8. **MU Q3 FY26 print Tue 6/24 AMC** — pre-print window open, position green.
