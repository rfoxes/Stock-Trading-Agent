# Tasks for the next run

This file is the focused to-do list for the next run (Tue 2026-06-23 — last full
session before the MU Wed 6/24 AMC print). Yesterday's Claude wrote it after the
6/22 run. Replace it (don't append) when you write the next version.

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
fails with `No module named 'requests'`. Confirmed still broken today (6/22).
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly.
NOT a "stop on ModuleNotFoundError" situation — complete the run via the venv and
document the drift.

## ⚠️ READ SECOND: NEWS BRIEF WAS STALE ON 6/22 — DATE-CHECK IT

On 6/22 the on-disk `news_brief.md` was still the **6/19 Juneteenth** brief — the
news pipeline skipped the Monday run. **Check `news_brief.md`'s `# News brief for
<date>` header matches today's date BEFORE trusting it.** If it doesn't match,
treat the brief as ABSENT (proceed without live news per the manual) and re-flag the
news-pipeline issue. Do NOT act on a stale brief.

## Status as of last update (2026-06-22, first live session post-Juneteenth)

- **Clean do-nothing day. `cli execute` → 0 intents** across all 7 strategies
  (0 submitted / 0 rejected / 0 errors). **Decision: Keep.** No rotations, no
  `.py`/`.md` edits, no manual changes.
- **MRVL did NOT fire** despite S&P 500 inclusion effective at today's open — the
  breakout volume gate was unmet (correct; do not override to chase index flow).
- **P0 = 0 unclaimed.** `cli list-active` → universe 23, **claimed 23,
  unclaimed_count 0, provisional_count 1**. No new unclaimed symbols → no triage.
- **SPCX = PROVISIONAL/UNVALIDATED claim on equity_trend_following_ema_cross,
  execution-quarantined, revalidate_by 2026-07-04** (auto-extended from 6/30 — still
  <60 bars). Execute confirmed it skips (`provisional_quarantined: ["SPCX"]`).
  Do NOT hand-promote.
- **News brief STALE (dated 6/19) — proceeded without live news per the manual.**
- **Account: equity $108,940.77; cash $15,518.15; buying power $323,655.93.**
  (Down $543 vs 6/19 $109,484.18 holiday last-close mark — first live repricing.)
- **Positions (6 longs, 5 green):** AAPL 72 (+8.85%), AVGO 26 (+4.06%),
  MU 7 (**+25.04%**, running into the 6/24 print), ORCL 38 (**-1.02%**, lone red),
  QQQ 28 (+13.58%), SPY 35 (+4.91%).
- **Regime: bull, conf 0.71, ADX 21.04** (further softening from 22.63 — trend
  weakening but still bull, price 8.1% above 200-SMA).

## To do next run (Tue 6/23 — last full session before MU print)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv interpreter
   (see warning #1). **Date-check the brief** (warning #2) — if it's not a fresh
   6/23 brief, proceed without it and re-flag the news pipeline.

2. **Snapshot + P0 check.** `cli list-active`. Expect `unclaimed_count: 0` and
   SPCX still PROVISIONAL (revalidate_by 7/04). If any NEW symbol shows as
   unclaimed, run `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT use
   `cli add-active`.

3. **Reconcile.** Confirm the 6 longs (AAPL/AVGO/MU/ORCL/QQQ/SPY) are still held.
   If any exited via a strategy's logic, `log-closed <strategy_id> <SYM>
   <pnl_fraction>`. No action if all still held.

4. **Position watch:**
   - **MU — Q3 FY26 print Wed 6/24 AMC. Tue 6/23 is the LAST full session before
     it.** Held and running **+25.04%**. `equity_event_driven_catalyst` window logic
     + trailing stop govern. **Watch the trailing stop into the print** — a +25%
     unrealized gain is exactly what the trailing stop protects. If the strategy
     trims/exits on its own rule, that's correct; do NOT discretionarily sell.
   - **ORCL — lone red (-1.02%).** Modest, no threshold breach. equity_event_driven_
     catalyst holds it. Watch but no action unless a rule fires.
   - **MRVL/INTC — breakout_volume claims both.** S&P-inclusion flow did NOT produce
     a volume-confirmed breakout Monday. Watch for a volume-confirmed entry; if the
     gate isn't met, no trade is correct. Don't override.
   - **QQQ — SPCX Nasdaq-100 fast-entry (~July 1) + Russell 6/26.** Soft awareness;
     no active rule reads rebalance flow (correct). SPCX's drawdown shrinks the flow.

5. **Run `cli execute` (via venv).** SPCX appears under `provisional_quarantined`/
   `skipped` — expected, not an error.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat)

- **SPCX validation (TOP PRIORITY, deadline 2026-07-04).** Provisional claim on
  equity_trend_following_ema_cross, execution-quarantined. Research must run a real
  backtest once SPCX has ≥60 bars and either VALIDATE (Sharpe ≥ 0.5 → promote to a
  trading claim) or ESCALATE. SPCX down 20%+ from its post-IPO high (Cursor-deal
  dilution). Likely also wants a vol-selling options strategy activated as a candidate
  responder (hyper-IV new listing; `volatility_regime` type). Recorded in
  `state/provisional_claims.md`.
- **`_load_news_brief()` staleness guard (NOW URGENT — bit in practice 6/22).** Parses
  `date_in_file` but never compares to today; on 6/22 the only on-disk brief was the
  stale 6/19 one, which would have been fed to strategies as live signal. Reject or
  down-weight a brief whose `date_in_file` != today. Top soft-signal item.
- **News-pipeline reliability / health-check.** The 6/22 Monday brief was never
  produced (regression after fresh 6/16–6/19). Add a health-check / alert on
  news-agent run failure so a missed brief is visible.
- **Scheduled index-rebalance / forced-flow overlay (MRVL/FLEX → S&P 500 6/22 [now
  effective, no breakout]; SPCX → Nasdaq-100 ~July 1; Russell 6/26; held QQQ).** No
  active rule reads a known index-rebalance schedule as a flow event. Suggested
  research: an index-rebalance/forced-flow overlay (anticipated add/drop dates +
  estimated flow) as a soft posture signal. Open Q: should index-inclusion become a
  6th Tier-B promotion trigger? gap_type: event_catalyst — responder: NONE.
- **US semiconductor industrial-policy / reshoring overlay (Intel foundry build-out).**
  Apple→Intel domestic-chip deal + the Lee (ex-SK Hynix CEO) EVP-Foundry hire — no
  rule maps a domestic-manufacturing policy/management catalyst to the affected names.
  INTC's only handle is breakout_volume (price). gap_type: event_catalyst — responder:
  NONE.
- **Event-window coverage on price-claimed names (INTC foundry-mgmt; META/GOOGL
  regulatory [Ohio under-16 law]; AMZN cost-curve; QQQ rebalance flow).**
  `event_catalyst` is declared only by equity_event_driven_catalyst, which claims
  AVGO/MU/ORCL — not these names. Broaden its claim set to event-prone large caps OR
  add a lightweight event-window co-claim overlay. gap_type: event_catalyst —
  responder: NONE.
- **Macro-event-window category (FOMC higher-for-longer; Citadel Sept-hike call).**
  No canonical gap_type covers a scheduled macro print. gap_type: NEW_CATEGORY_NEEDED
  — responder: NONE.
- **AI-capex financing / crowding overlay** (ORCL/DELL/hyperscalers/semis) — higher-
  for-longer + BofA "most-crowded-trade-in-history" compound into a cohort
  financing/leverage + crowding headwind with no rule flagging it. gap_type:
  NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX last reported close 16.40, sub-17). Registry hole
  CLOSED (volatility_regime declared by iron_condor_high_iv, calendar_spread,
  jade_lizard, long_straddle_earnings) but none active / none claim a universe symbol.
  Activate one vol-selling options strategy with a claim; doubles as SPCX candidate.
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
   Persisting across many runs.
2. **[NEW] News pipeline skipped the Monday 6/22 run — brief was STALE (6/19).**
   Fix the news-agent Monday run; add a health-check / alert on news-agent failure.
   Tue 6/23: confirm a fresh 6/23 brief is produced.
3. **SPCX is a PROVISIONAL, execution-quarantined claim** — Sat research owns
   validation by 2026-07-04 (needs ≥60 bars). Do NOT character-match / hand-promote.
4. **MU Q3 FY26 print CONFIRMED Wed 6/24 AMC** — pre-print window open, position
   running hard (+25.04%). Watch the trailing stop into the print. Tue 6/23 is the
   last full session before it.
5. **Higher-for-longer + AI-crowding is the standing macro backdrop** (~80% odds of
   ZERO 2026 cuts; Citadel Sept-hike call; BofA "most crowded trade in history").
   Whole book AI-cohort/rate-sensitive levered; regime ADX softening to 21.04. No
   rule pre-positions for it (correct). Watch for delayed de-rating.
6. **US-Iran Geneva signing was called off last-minute (NOT confirmed as of 6/19).**
   Brief is stale; re-confirm status when a fresh brief lands. Don't mistake an
   oil-sensitive treaty-fade for fundamental weakness.
