# Tasks for the next run

This file is the focused to-do list for the next run. **NOTE: markets are CLOSED Fri 2026-07-03**
(Independence Day observed) — the next trading session is **Mon 2026-07-06**. Saturday research (revalidating
provisionals) runs in between. Yesterday's Claude wrote this after the 7/2 run (do-nothing / Keep day; META
BUY 16 filled overnight and was reconciled). Replace it (don't append) when you write the next version.

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
quant_trading_system.cli ...` fails with `No module named 'requests'`. Confirmed still broken 7/2.
**RUN EVERYTHING VIA THE VENV:**

```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```

The `.venv` (Python 3.13.13) has all deps and reaches the live broker cleanly. NOT a "stop on
ModuleNotFoundError" situation — complete the run via the venv and document the drift.

## ⚠️ READ SECOND: DATE-CHECK THE NEWS BRIEF

The **7/2 brief was FRESH** (header `2026-07-02` matched today) — pipeline held for a 3rd straight session
(6/30, 7/1, 7/2) but it's been flaky historically (misses 6/22, 6/25, 6/29). **Always check
`news_brief.md`'s `# News brief for <date>` header matches the run date BEFORE trusting it.** Next run is
**Mon 7/6** — the brief should be dated 2026-07-06. If it doesn't match, treat the brief as ABSENT (proceed
on realized price) and re-flag the news pipeline.

## Status as of last update (2026-07-02, do-nothing / Keep day — META filled, 0 execute intents)

- **`cli execute` → 0 intents** across all 8 strategies. `submitted 0, rejected 0, errors 0`.
  `provisional_quarantined: [QCOM, SPCX, SYNA]`, all skipped. **Decision: Keep.** No override, no edits.
- **META BUY 16 FILLED + reconciled.** The 7/1 `equity_momentum_macd_histogram` BUY filled overnight; META now
  in the book at **avg $605.28** (16 sh). Entry, not a close → no `log-closed`. Cash delta −$9,684.43 confirms.
  META stays macd's claim.
- **P0 = 0 unclaimed.** No new universe member, no promotions (brief made none). `list-active` → universe 26,
  claimed 26, unclaimed 0, provisional 3 (QCOM, SPCX, SYNA). Nothing to triage.
- **Account: equity $102,765.98; cash $71,809.60; buying power $373,916.27.** (−$1,035.67 vs 7/1 on continued
  semi weakness + META opening underwater.)
- **Positions (4 longs):** AVGO 26 (**−4.21%**, −$412.88, deepened from −2.01%), META 16 (**−3.35%**, −$324.41,
  NEW filled, opened underwater), MU 7 (**−0.49%**, −$33.88 — round-tripped its entire gain from +17.43% peak;
  trailing stop still did NOT fire), ORCL 38 (**−20.52%**, −$1,382.31, only red, deepened through −20%, worst yet).
- **Regime: bull, conf 0.73, ADX 23.35, realized_vol 0.1785.**
- **Infra:** `cli open-orders` CLEAN this run (no live order to trip the parser bug). Bug is confirmed
  live-order-specific; still needs the operator fix for trade days.
- **News brief FRESH (7/2), NORMAL FLOW.** Loud headlines (TSLA deliveries 480k +25% but −7.5%; GOOGL €4.1B EU
  fine upheld/final; META/NVDA/AMZN cloud/own-silicon; AAPL ~55% price hikes) — all on price-claimed names,
  `responder: NONE`. Library gaps, not trader actions.

## To do next run (Mon 7/6)

1. **Read last_handoff.md and news_brief.md FIRST.** Use the venv (warning #1). **Date-check the brief** —
   should read `2026-07-06` (warning #2). Confirm the session ran normally after the 3-day weekend
   (markets were closed Fri 7/3). **Watch the weekend gap** — 3 calendar days of news (incl. any weekend
   developments) hit Monday's open at once.

2. **Snapshot + reconcile.** `positions`, `account`, `open-orders`, `regime`. No pending order was left open
   from 7/2 (execute submitted nothing; open-orders clean). If any 7/2 long is gone Monday, `log-closed` it
   to the owning strategy. Otherwise no reconcile needed.

3. **P0 check.** `cli list-active`. Expect `unclaimed_count: 0`. **Re-check `provisional_count`** — SPCX's
   deadline (**2026-07-04**) passed over the weekend; if Saturday research revalidated it, provisional_count
   may drop to 2 (QCOM + SYNA, both 7/10). If SPCX still shows provisional, it stays execution-quarantined.
   If any NEW symbol shows unclaimed, run `cli triage-symbol <SYM> [--gap-type <type>]`. Do NOT `add-active`.

4. **Position watch (no discretionary action either direction — algorithmic-only mandate):**
   - **META — filled 7/2 at avg $605.28, sits −3.35% day one.** Rule-owned by macd_histogram (entry AND exit).
     A small day-one drawdown on a momentum entry is normal. No discretionary trim; let the rule govern.
   - **MU — round-tripped its whole gain to −0.49%; trailing stop still NOT fired.** DRAM-antitrust overhang +
     post-print IV crush (no rule reads either). Watch whether the continued give-back finally trips the
     trailing stop; reconcile any rule-driven exit. Do NOT sell to "lock in" — forbidden.
   - **ORCL — −20.52% (−$1,382), through −20%, book's only deep red and deepening.** Restructuring (21k cuts)
     has no algorithmic responder; event_driven_catalyst (claims ORCL provisionally) models earnings only.
     Held; most-elevated Saturday item. No action.
   - **AVGO — −4.21%, deepened; no rule fired.** Correct do-nothing on the continued semi weakness.
   - **Others (ARM/INTC/MRVL, MSFT/SNDK, CSCO, HPE, DELL) + trend-following's large-cap sleeve
     (AAPL/AMZN/GOOGL/JPM/NVDA/SPY/QQQ/TSLA/TSM/CBRS/NUVL)** — 0 intents 7/2. Watch their gates; no trade
     = correct if unmet. **TSLA earnings 7/22, JPM earnings Tue 7/14 (inside 14-day options window), INTC 7/23**
     — all price-claimed (responder NONE; earnings-window assignment gap).

5. **Run `cli execute` (via venv).** SPCX/QCOM/SYNA appear under `provisional_quarantined`/`skipped` (unless
   Saturday validated SPCX). React to realized price only: if a rule fires, execute; if none fires,
   do-nothing is correct. Do NOT discretionarily de-risk or take profits.

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
  JPM (earnings Tue 7/14, INSIDE the 14-day options window) + INTC (7/23).** The earnings-window responder
  (equity_event_driven_catalyst) does not claim TSLA, JPM, or INTC (all trend-following / price-driven).
  Assign the earnings-window strategy to scheduled-catalyst names via head-to-head. gap_type: earnings_window
  — responder: NONE (assignment).
- **Regulatory / antitrust ruling on a universe name — GOOGL (EU €4.1B Android fine UPHELD/final 7/2, NEW;
  + Wed Klarna ~$1.97B / Yelp carry) + META (India WhatsApp query; 29-state addiction suit carry).** Three
  adverse antitrust developments in three sessions on GOOGL. No active rule reads a court/agency ruling. Build
  a regulatory/litigation event-window overlay for large-caps (pairs with MU DRAM + AAPL SCOTUS carries).
  gap_type: event_catalyst — responder: NONE.
- **Business-model / product-line launch — NVDA (startup cloud + rev-share, NEW 7/2) + AMZN (own AI chips,
  NEW 7/2; AWS $1B unit carry) + META (AI cloud, carry).** Multi-front cloud/own-silicon push. No rule reads a
  strategic business-line/product disclosure. Consider a strategic-announcement sub-trigger in an event-window
  overlay. gap_type: event_catalyst — responder: NONE.
- **Pricing / margin disclosure — AAPL (~55% hardware price hikes, NEW 7/2).** No rule reads a pricing-power /
  input-cost-pass-through disclosure. Pairs with the input-cost/margin-compression carry. gap_type:
  event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction — MSFT (thousands, carry) + ORCL (21k, carry; held name −20.52% and
  deepening through −20%).** Claimed by price-driven strategies; unmodeled. Recurring big-tech event class.
  Build a restructuring event-window; decide whether a generic price-based stop should co-cover event-driven's
  held names (ORCL is the live pain case). gap_type: event_catalyst — responder: NONE / partial.
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
2. **[HIGH] News pipeline flaky — FRESH 7/2 (3rd straight: 6/30, 7/1, 7/2) but missed 6/22 + 6/25 + 6/29.**
   Add a health-check / alert on news-agent run failure so a missed/stale brief is visible. Plus the
   `_load_news_brief()` staleness guard (Q3).
3. **`_load_news_brief()` staleness guard** — parses `date_in_file` but never compares to today. Reject/
   down-weight a brief whose date != today.
4. **[REOPENED] `cli open-orders` parser bug** — errors `'dict' object has no attribute 'id'` when a live open
   order exists (did NOT bite 7/2 — no order; bit on META 7/1, QQQ 6/30, SPY 6/26). Returns clean JSON only
   when no open orders. Fix the order-serialization path; the trader can't inspect live orders.
5. **THREE provisional/quarantined claims** — Sat research owns validation: SPCX (**7/04 — THIS SATURDAY,
   deadline passes before Mon 7/6**), QCOM + SYNA (7/10). Do NOT character-match / hand-promote.
6. **MU round-tripped its whole gain (+17.43% peak → −0.49%); trailing stop still NOT fired.** DRAM-antitrust
   overhang. Watch for the give-back scenario where the trailing stop finally engages; reconcile any
   rule-driven exit. No discretionary action.
7. **ORCL −20.52% (−$1,382) and deepening through −20% — held name in a real drawdown with no algorithmic
   handle.** Restructuring-event gap is no longer academic; elevate for Saturday.
