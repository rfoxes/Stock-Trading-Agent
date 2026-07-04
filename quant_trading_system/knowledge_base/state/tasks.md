# Tasks for the next run

This file is the focused to-do list for the next run. **The next trading session is Mon 2026-07-06.**
Yesterday's Claude wrote a 7/3 version anticipating the holiday; today's run **actually fired on the holiday
Fri 7/3** (market closed, no session) and confirmed nothing drifted. This is the refreshed list for Mon 7/6.
Saturday research (revalidating provisionals, incl. the SPCX 7/04 deadline) runs in between. Replace it
(don't append) when you write the next version.

---

## STANDING POLICY (P0, do not ignore) — MANDATORY-ATTACH DOCTRINE (2026-06-16)

**Every symbol in the universe MUST have a strategy attached — none is ever left strategy-less.** See
`manual.md` "P0 — EVERY SYMBOL ALGORITHMICALLY EVALUATED RULE". Two grades:
- **(a) VALIDATED claim** — a library strategy cleared baseline Sharpe (0.5) in a `cli triage-symbol`
  backtest. Trades normally.
- **(b) PROVISIONAL claim** — nothing cleared baseline (or no price history), so triage attached the
  best-available strategy as an UNVALIDATED claim, recorded in `state/provisional_claims.md` with a
  `revalidate_by` deadline and **QUARANTINED from execution** (`cli execute` auto-skips). Never trades until
  Saturday research validates.

After triage, `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]` for any NEW
unclaimed symbol. Character-match shortcuts and direct YAML edits to `active_strategies.md` are FORBIDDEN.
Never use `cli add-active` to bypass triage.

---

## ⚠️ READ FIRST: BARE `python3` IS STILL BROKEN — USE THE VENV

**Homebrew `/opt/homebrew/bin/python3` is 3.14.5 and lacks the harness deps.** Bare `python3 -m
quant_trading_system.cli ...` fails with `No module named 'requests'`. Confirmed still broken 7/3.
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a "stop on
ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF + CHECK MARKET STATUS

The **7/3 brief was FRESH** (a purpose-built holiday brief, header `2026-07-03`) — the pipeline held for a 4th
straight session (6/30, 7/1, 7/2, 7/3) but it's been flaky historically (misses 6/22, 6/25, 6/29). **Always
check `news_brief.md`'s `# News brief for <date>` header matches the run date BEFORE trusting it.** Next run is
**Mon 7/6** — the brief should be dated 2026-07-06. If it doesn't match, treat the brief as ABSENT (proceed on
realized price) and re-flag the news pipeline. **Also run `cli market-status` early** — 7/3 taught us the task
can fire on a NYSE holiday; if `is_open: false`, do a read-only snapshot and do NOT execute. Monday 7/6 should
be `is_open: true`.

## Status as of last update (2026-07-03 HOLIDAY run — market CLOSED, no session, no execute)

- **Market was CLOSED (Independence Day observed).** `market-status` → `is_open: false`,
  `next_open 2026-07-06 09:30 ET`. **`cli execute` deliberately NOT run** — no session to trade into. Not a
  "fired 0 intents" day; execute was never called. Decision: no-execute holiday deferral.
- **Book frozen — no fills/closes over the holiday.** Cash $71,809.59 (= 7/2's $71,809.60, penny rounding).
  All four 7/2 longs present at identical quantities. No reconciliation needed.
- **P0 = 0 unclaimed.** No new universe member, no promotions (holiday brief made none). `list-active` →
  universe 26, claimed 26, unclaimed 0, provisional 3 (QCOM, SPCX, SYNA). Nothing to triage.
- **Account: equity $102,666.87; cash $71,809.59; buying power $373,638.74.** (−$99.11 vs 7/2 — just marks
  settling to the official 7/2 close, no trades.)
- **Positions (4 longs, marked to 7/2 close):** AVGO 26 (**−4.46%**, −$437.32), META 16 (**−3.70%**, −$358.01),
  MU 7 (**−0.75%**, −$51.38 — trailing stop still NOT fired), ORCL 38 (**−20.88%**, −$1,406.25 — fresh worst).
- **Regime: bull, conf 0.73, ADX 22.84, realized_vol 0.1783.**
- **Infra:** `cli open-orders` CLEAN (no live order). Parser bug did not bite.
- **News brief FRESH (7/3 holiday), NO MATERIAL NEWS.** Purpose-built to refresh the date so Monday doesn't
  fall back to the stale 7/2 brief. All 7/2 carry-forwards unchanged (no session altered them).

## To do next run (Mon 7/6)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv (warning #1). **Date-check the brief** —
   should read `2026-07-06` (warning #2). **Run `cli market-status`** — should be `is_open: true` Monday.
   **Watch the weekend gap** — 3+ calendar days of news (incl. any weekend developments) hit Monday's open at
   once, on top of the 7/2 close the book is currently marked to.

2. **Snapshot + reconcile.** `positions`, `account`, `open-orders`, `regime`. No pending order exists (open-
   orders clean 7/3). If any long is gone Monday, `log-closed` it to the owning strategy. Otherwise no
   reconcile needed. Book currently: AVGO 26, META 16, MU 7, ORCL 38.

3. **P0 check.** `cli list-active`. Expect `unclaimed_count: 0`. **Re-check `provisional_count`** — SPCX's
   deadline (**2026-07-04**) passed over the weekend; if Saturday research revalidated it, provisional_count
   may drop to 2 (QCOM + SYNA, both 7/10). If SPCX still shows provisional, it stays execution-quarantined.
   If any NEW symbol shows unclaimed, run `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT `add-active`.

4. **Position watch (no discretionary action either direction — algorithmic-only mandate):**
   - **META — filled 7/2 at avg $605.28, marked −3.70% into the 7/2 close.** Rule-owned by macd_histogram
     (entry AND exit). A small early drawdown on a momentum entry is normal. No discretionary trim; let the
     rule govern.
   - **MU — −0.75%, trailing stop still NOT fired.** DRAM-antitrust overhang + post-print IV crush (no rule
     reads either). Watch whether the continued give-back finally trips the trailing stop; reconcile any
     rule-driven exit. Do NOT sell to "lock in" — forbidden.
   - **ORCL — −20.88% (−$1,406), fresh worst.** Restructuring (21k cuts) has no algorithmic responder;
     event_driven_catalyst (claims ORCL provisionally) models earnings only. Held; most-elevated Saturday
     item. No action.
   - **AVGO — −4.46%; no rule fired.** Correct do-nothing on the continued semi weakness.
   - **Others (ARM/INTC/MRVL, MSFT/SNDK, CSCO, HPE, DELL) + trend-following's large-cap sleeve
     (AAPL/AMZN/GOOGL/JPM/NVDA/SPY/QQQ/TSLA/TSM/CBRS/NUVL)** — watch their gates; no trade = correct if unmet.
     **JPM earnings Tue 7/14 (inside the 14-day options window by Monday), TSLA earnings 7/22, INTC 7/23** —
     all price-claimed (responder NONE; earnings-window assignment gap).

5. **Run `cli execute` (via venv) — only if market is open.** SPCX/QCOM/SYNA appear under
   `provisional_quarantined`/`skipped` (unless Saturday validated SPCX). React to realized price only: if a
   rule fires, execute; if none fires, do-nothing is correct. Do NOT discretionarily de-risk or take profits.

6. **Library gaps — see list below (Saturday research owns them).**

7. **Run `cli git-sync --agent trader --message "..."` (via venv) as last action.**

## Library gaps + research items (carry to research_tasks.md Sat 7/4)

- **THREE provisional/quarantined validations (TOP PRIORITY):**
  - **SPCX** (trend-following, deadline **2026-07-04 — THIS SATURDAY**, needs ≥60 bars). Carry: Nasdaq-100 add
    **Tue 7/7** (~$4.3B forced passive buying), FCC satellite-licensing vote 7/22, elevated single-name IV,
    broke IPO price. Price history still thin (only joins the index 7/7) — may not clear baseline yet. Likely
    wants a vol-selling options responder.
  - **QCOM** (event-driven, deadline **2026-07-10**). Top candidate Sharpe 0.0.
  - **SYNA** (pairs-cointegration, deadline **2026-07-10**). **Live merger-arb:** onsemi $7B all-stock
    (1.350 ON/sh, ~19% premium, close mid-2027). Textbook long SYNA / short ON. The activation instance for
    the standing m_a_arbitrage gap — validate the pairs setup.
- **Delivery / earnings-window assignment — TSLA (Q2 deliveries 480k printed 7/2, +25%; earnings 7/22) +
  JPM (earnings Tue 7/14, INSIDE the 14-day options window by Mon 7/6) + INTC (7/23).** The earnings-window
  responder (equity_event_driven_catalyst) does not claim TSLA, JPM, or INTC (all trend-following /
  price-driven). Assign the earnings-window strategy to scheduled-catalyst names via head-to-head. gap_type:
  earnings_window — responder: NONE (assignment).
- **Regulatory / antitrust ruling on a universe name — GOOGL (EU €4.1B Android fine UPHELD/final 7/2;
  + Wed Klarna ~$1.97B / Yelp carry) + META (India WhatsApp query; 29-state addiction suit carry).** Three
  adverse antitrust developments in three sessions on GOOGL. No active rule reads a court/agency ruling. Build
  a regulatory/litigation event-window overlay for large-caps (pairs with MU DRAM + AAPL SCOTUS carries).
  gap_type: event_catalyst — responder: NONE.
- **Business-model / product-line launch — NVDA (startup cloud + rev-share) + AMZN (own AI chips; AWS $1B
  unit carry) + META (AI cloud, carry).** Multi-front cloud/own-silicon push. No rule reads a strategic
  business-line/product disclosure. Consider a strategic-announcement sub-trigger in an event-window overlay.
  gap_type: event_catalyst — responder: NONE.
- **Pricing / margin disclosure — AAPL (~55% hardware price hikes).** No rule reads a pricing-power /
  input-cost-pass-through disclosure. Pairs with the input-cost/margin-compression carry. gap_type:
  event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction — MSFT (thousands, carry) + ORCL (21k, carry; held name −20.88% and
  fresh worst).** Claimed by price-driven strategies; unmodeled. Recurring big-tech event class. Build a
  restructuring event-window; decide whether a generic price-based stop should co-cover event-driven's held
  names (ORCL is the live pain case). gap_type: event_catalyst — responder: NONE / partial.
- **Capital-allocation / capital-return — JPM ($50B buyback + dividend eff 7/1) + MU ($250M Trump Accounts,
  carry).** No rule reads a buyback/dividend/pricing disclosure. gap_type: event_catalyst — responder: NONE.
- **Short-interest / positioning disclosure — NVDA/TSLA (Burry AI-bear thesis "extends beyond," carry).** No
  rule reads a 13F/short disclosure. gap_type: event_catalyst — responder: NONE.
- **Index-rebalance / forced-flow window — SPCX→Nasdaq-100 (Tue 7/7, ~$4.3B); SK Hynix Nasdaq listing (~7/10).**
  No rule reads an index-rebalance schedule. Open Q: index-inclusion as a 6th Tier-B promotion trigger?
  gap_type: event_catalyst — responder: NONE.
- **Litigation / antitrust on a held name — MU (DRAM price-fixing class action, N.D. Cal., carry).** MU's
  provisional/quarantined claim models earnings windows only. gap_type: event_catalyst — responder: NONE.
- **Input-cost / margin-compression carry (AAPL memory pass-through → 55% hikes; Cook "extreme memory
  shortage"; SNDK Chinese-supply risk).** Price-claimed; no rule reads a cost/margin shock. Build an
  event-window overlay co-claiming large-caps for cost/margin events. gap_type: event_catalyst — responder: NONE.
- **Macro-event-window category (June NFP +57k big miss / dovish; Fed on hold; May core PCE 3.4%;
  US–Mexico–Canada trade-deal review window opened).** No canonical gap_type covers a scheduled macro/policy
  print or regime; no rule lets the trader pre-position (correct under the mandate, but the soft-signal handle
  is missing). gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation** (VIX ~16.6, index IV-rank below the >50 threshold; MU post-print IV crush =
  short-vol setup; SPCX event-IV into 7/7; TSLA event-IV into 7/22; JPM into 7/14). volatility_regime is
  declared (iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings) but none active / none
  claims a universe symbol. Activate one vol strategy with a claim (MU IV crush textbook short-vol; doubles as
  SPCX candidate). gap_type: volatility_regime — responder: NONE (active); activation pending.
- **Validate the first-pass + provisional assignments via head-to-head:**
  - `equity_breakout_volume_confirmation` vs `equity_trend_following_ema_cross` on ARM, MRVL, INTC
  - `equity_mean_reversion_bollinger` vs `equity_trend_following_ema_cross` on CSCO
  - `equity_rsi_divergence` vs `equity_trend_following_ema_cross` on HPE
  - `equity_event_driven_catalyst` vs `equity_trend_following_ema_cross` on AVGO, MU, ORCL
  - `equity_sector_rotation_momentum` vs `equity_trend_following_ema_cross` on DELL
  - `equity_momentum_macd_histogram` vs `equity_trend_following_ema_cross` on META, MSFT (SNDK already
    validated for macd, Sharpe 2.254 — no head-to-head needed; META now has a LIVE macd long, avg $605.28)
  - trend-following placeholders → AAPL, AMZN, CBRS, GOOGL, JPM, NUVL, NVDA, QQQ, SPY, TSLA, TSM
    (CBRS → event-driven; TSLA/JPM/INTC → event-driven for the earnings/delivery windows)
  - QCOM provisional (event-driven) + SYNA provisional (pairs-cointegration) → validate or escalate

## Open questions for the operator

1. **[HIGH] Repair the scheduled-task interpreter.** Bare `python3` → Homebrew 3.14.5 (no deps). Repoint the
   Cowork task / daily_prompt to `.venv/bin/python3`, or reinstall deps into 3.14, or recreate the venv.
   Persisting across many runs.
2. **[MEDIUM] Trader task fired on the 7/3 NYSE holiday.** Ran cleanly as read-only assess-and-stop
   (market-status guarded the execute step), but ideally short-circuit on `is_open: false` — or confirm the
   M-F schedule is intended to fire on holidays. Not harmful, just wasteful.
3. **[HIGH] News pipeline flaky — a purpose-built holiday brief fired FRESH 7/3 (4th straight: 6/30, 7/1, 7/2,
   7/3) but missed 6/22 + 6/25 + 6/29.** Add a health-check / alert on news-agent run failure so a
   missed/stale brief is visible. Plus the `_load_news_brief()` staleness guard (Q4).
4. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to today. Reject/
   down-weight a brief whose date != today.
5. **[REOPENED] `cli open-orders` parser bug** — errors `'dict' object has no attribute 'id'` when a live open
   order exists (did NOT bite 7/2 or 7/3 — no order; bit on META 7/1, QQQ 6/30, SPY 6/26). Returns clean JSON
   only when no open orders. Fix the order-serialization path; the trader can't inspect live orders.
6. **THREE provisional/quarantined claims** — Sat research owns validation: SPCX (**7/04 — THIS SATURDAY,
   deadline passes before Mon 7/6**), QCOM + SYNA (7/10). Do NOT character-match / hand-promote.
7. **MU round-tripped its whole gain (+17.43% peak → −0.75%); trailing stop still NOT fired.** DRAM-antitrust
   overhang. Watch for the give-back scenario where the trailing stop finally engages; reconcile any
   rule-driven exit. No discretionary action.
8. **ORCL −20.88% (−$1,406) — held name in a real drawdown with no algorithmic handle.** Restructuring-event
   gap is no longer academic; elevate for Saturday.
