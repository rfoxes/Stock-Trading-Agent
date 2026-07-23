# Tasks for the next run

**🔴 7/23 COMPLETE (single fire, canonical 16:03, Thursday). NOT a KEEP no-op — the META MACD EXIT FIRED.**
`equity_momentum_macd_histogram` tripped its exit ("hist −1.8108 flipped negative") and `cli execute` **submitted a
market DAY sell of the full 16-share META position** — order **`db566584-d77f-4b10-982c-12839ab4867d`**, status
`accepted`/filled_qty 0, **rests for the 7/24 open.** Book was META-only + intact going in (cash $94,690.29 unchanged;
NOT a wipe), news agent promoted **NOW + STM** (universe 40→42) → I triaged both to quarantined provisionals
(`equity_event_driven_catalyst`, Sharpe 0.0, `revalidate_by 2026-08-06`). `unclaimed_count 0`, `provisional_count
12→14`. Brief FRESH & on-time (2026-07-23), NOTABLE risk-off (Mag7 worst day since Apr 2025, Nasdaq −2.15%), NOT
halt-worthy (VIX *eased* to 16.64, oil didn't gap futures >2%). See `last_handoff.md`. Replace this file (don't
append) when you write the next version.

## ⚠️ READ FIRST — RUN EVERYTHING VIA THE VENV
```
/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3 -m quant_trading_system.cli <cmd>
```
Bare `python3` = Homebrew 3.14.5, no deps. The `.venv` (3.13.13) has deps + reaches the live broker.
Note: CLI prints a `safety_gate_initialized` structlog line to **stdout** before the JSON — pipe through
`grep '^{'` before parsing with python/jq. **`cli open-orders` is BROKEN whenever a live order exists**
(`'dict' object has no attribute 'id'`) — and there IS one now (the META sell). Read open orders **client-direct**:
`AlpacaClient(Settings(_env_file='.env')).get_open_orders()` → list of dicts, use `.get('id')`/`.get('status')`.

## 🔴🔴 TOP PRIORITY (Fri 7/24) — RECONCILE THE META FILL FROM THE ACTUAL FILL PRICE

The resting META sell (`db566584-d77f-4b10-982c-12839ab4867d`, market DAY) fills at the **7/24 open**. Your run is
post-close 7/24, hours after the open → under normal timing it WILL have filled. Do this, in order:

1. **Snapshot first** (`account`, `positions`, open-orders client-direct). **Expected: META GONE (flat book), cash UP
   by ~fill proceeds (≈ filled_avg_price × 16 ≈ ~$9.7k), equity ~flat.** This is **"cash UP + position vanished" =
   legitimate fill/close — NOT a wipe** (a wipe is flat book + cash *UNCHANGED* + no `trade_closed`; here cash RISES).
   Do NOT freeze.
2. **Pull the ACTUAL fill client-direct:**
   `AlpacaClient(Settings(_env_file='.env')).get_order('db566584-d77f-4b10-982c-12839ab4867d')` → dict; read
   `status`/`filled_avg_price`/`filled_qty`/`filled_at`.
3. **`log-closed` from the REAL fill, NOT today's +0.35% mark (the 7/9 MU sign-flip lesson):**
   ```
   cli log-closed equity_momentum_macd_histogram META <pnl_fraction>
   ```
   `pnl_fraction = (filled_avg_price − 605.275625) / 605.275625`. Overnight risk-off + Brent >$100 + META's Lina-Khan
   item can move the open either way — the +0.35% mark ($607.37) is NOT the fill. **Cross-check:** cash rise should
   ≈ `filled_avg_price × 16` to the penny → confirms a legit close AND a complete reconciliation.
4. **GUARD — if the order is STILL resting AND META still shows held:** do NOT run `cli execute` blindly.
   `equity_momentum_macd_histogram.evaluate()` will re-emit "sell META 16" (histogram still negative) → a SECOND
   resting sell → **oversell into a short** when both fill. First cancel the stale order (or wait for the fill) and
   reconcile; only then execute. (Normal market-order-at-open timing avoids this — but guard it.)
5. After META closes, the book is **flat / all-cash (~$104k)**. No held position to manage; `event_driven_catalyst`
   still claims AVGO/MU/ORCL (flat since 7/9) + provisionals.

## STANDING POLICY (P0) — MANDATORY-ATTACH DOCTRINE
Every universe symbol MUST have a strategy (manual.md P0). Grades: **(a) VALIDATED** (cleared baseline Sharpe 0.5 in
triage — trades) / **(b) PROVISIONAL** (nothing cleared / no history — best-available attached, QUARANTINED until
Saturday research validates; no-history routes to `equity_watch_only`, degenerate-0-trade routes to a below-baseline
trading provisional). After triage `unclaimed_count` should be **0**. Run `cli triage-symbol <SYM> [--gap-type X]`
for any NEW unclaimed symbol. Character-match / direct YAML edits to `active_strategies.md` are FORBIDDEN. Never use
`cli add-active` to bypass triage.

## To do next run (Fri 7/24 — book turning over)

1. **Read `last_handoff.md` + `news_brief.md` FIRST** (venv). **Date-check the brief** — must match 2026-07-24; if
   not, treat as ABSENT, note the gap, fall back to raw `news/daily_summary/2026-07-24.html` for a halt-worthy safety
   scan (esp. Houthi/oil escalation into a >2% overnight futures gap — Brent was >$100 on actual tanker strikes). Run
   `cli market-status` + `git log --oneline -5`; note the run TIME. **Double-fire check:** if a `[trader 2026-07-24]`
   commit is already in git log + a handoff already narrates a completed 7/24 run, take NO action (don't re-execute,
   don't re-triage, don't re-log-closed).
2. **Snapshot:** `account`, `positions`, open-orders (client-direct). **Then RECONCILE THE META FILL** — the whole
   TOP-PRIORITY block above. Expected post-fill: flat book, cash ~$104k, day_trade_count possibly +1 if the sell and
   any same-day buy paired (unlikely — no buy pending).
3. **P0 check:** `cli list-active`. Expect `unclaimed_count 0`, `provisional_count 14` (AMD/IREN/NBIS `2026-08-04`;
   NOW/STM `2026-08-06`; GS `2026-07-28`; MS/PYPL `2026-07-29`; QCOM/SPCX/SYNA `2026-07-21 OVERDUE`; SKHY `2026-07-24`
   — overdue after today if no Sat 7/25 research; RIVN `2026-07-27`; UNH `2026-07-30`). All 14 ALREADY
   claimed/quarantined — do NOT re-triage; research owns validation. Triage only any *new* unclaimed symbol. Do NOT
   `add-active`.
4. **Execute (venv).** After the META reconciliation, `cli execute` per standard workflow. With META closed, the MACD
   strategy sees no META position → no re-emit. `event_driven_catalyst`'s live claims (AVGO/MU/ORCL) are flat with no
   fresh *discrete single-name* entry catalyst → likely fires nothing. **Watch INTC:** its +7–13% AH pop on the
   blowout *could* trip `equity_breakout_volume_confirmation` (reads price/volume) on a confirmed 7/24 session
   breakout — that's within its mandate, let it fire or not on its own rule. Provisionals stay quarantined/skipped.
5. **Library gaps — see list below (Saturday research owns them; the earnings-window assignment gap is the most acute,
   now with a universe blowout (INTC) alongside GOOGL/TSLA/SMCI).**
6. **`cli git-sync --agent trader --message "..."` (venv) as last action.**

## Position watch

- **META (avg $605.28) — EXITING.** `equity_momentum_macd_histogram` fired its histogram-negative exit; a market DAY
  sell of all 16 (`db566584…`) rests for the 7/24 open. Reconcile the fill (TOP-PRIORITY block). After it fills the
  book is flat/all-cash. META Q2 is 7/29 — moot once the position is closed.
- **AVGO / MU / ORCL — CLOSED & reconciled 7/9.** Not held. `event_driven_catalyst` still *claims* them (claim ≠
  position); re-enters only on a fresh modeled discrete catalyst. **ORCL won a $6.99B/10-yr Navy/Pentagon IDIQ 7/23 —
  event_driven_catalyst (which claims ORCL) fired NO entry on the award** (same as the 7/15 ORCL Japan-cloud tag).
  Whether its `evaluate()` should fire on a contract award is a research question, not a hand-manage directive.

## Library gaps + research items (carry to research_tasks.md — Saturday 7/25, if research runs)

All `responder: NONE` except ORCL (which had a responder but fired no trade) — informational, not tradable under the
mandate. `gap-registry coverage_holes` is **empty**; every item is an activation/assignment gap (a rule/event-type not
mapped to the symbol that had the event):
- **Provisional/quarantined validations (TOP PRIORITY):** **14** — all on `equity_event_driven_catalyst` except as
  noted: **AMD** (`2026-08-04`), **IREN** (`2026-08-04`), **NBIS** (`2026-08-04`), **NOW** (ServiceNow Q2 beat+raise
  +7%, `2026-08-06` NEW), **STM** (STMicro Q2 beat/soft-guide −14→−18%, `2026-08-06` NEW), **GS** (`2026-07-28`),
  **MS** (`2026-07-29`), **PYPL** (`2026-07-29`), **QCOM** (`2026-07-21 OVERDUE`), **RIVN** (`2026-07-27`),
  **UNH** (`2026-07-30`) — all degenerate-0-trade Sharpe-0.0 below-baseline trading provisionals. Plus **SKHY**
  (`equity_watch_only`; no-history, `2026-07-24` — overdue after today if Sat 7/25 misses), **SPCX**
  (`equity_trend_following_ema_cross`; no-history, `2026-07-21 OVERDUE`; SpaceX first public earnings Aug 4), **SYNA**
  (`equity_pairs_trading_cointegration`; onsemi merger-arb, `2026-07-21 OVERDUE`). Validate/upgrade or archive each.
  **QCOM/SPCX/SYNA are OVERDUE** (missed the dropped 7/18 research) — clear them first; **SKHY overdues today.**
- **Earnings/print-window ASSIGNMENT gap (MOST ACUTE recurring — now with a UNIVERSE BLOWOUT in hand): INTC blowout
  7/23 AMC (rev +25%/DC&AI +59%/+7–13% AH) UNRESPONDED (on `breakout_volume_confirmation`, reads price/volume);
  GOOGL −7% + TSLA −14% both UNRESPONDED (both on `trend_following`); SMCI UNRESPONDED a 3rd straight session (on
  `mean_reversion_bollinger`). Upcoming: MSFT/META 7/29, AMZN/AAPL 7/30, AMD/SPCX 8/4; plus quarantined
  GS/MS/PYPL/QCOM/RIVN/UNH.** Claimed by trend/breakout/mean-reversion/macd, NOT `equity_event_driven_catalyst`
  (unvalidated) / `long_straddle_earnings`. **Reassign / activate an earnings-window responder on the names actually
  printing.** Single strongest research priority.
- **Contract / award events — ORCL's $6.99B Navy/Pentagon IDIQ DID hit a responder (`equity_event_driven_catalyst`
  claims ORCL) but fired NO entry.** *Research: does its `evaluate()` actually fire on a government-contract award, or
  only earnings-type catalysts? (RKLB's $266M Space Force award 7/22 hit `breakout_volume`, price-only — still a gap
  for award-type events on non-ORCL names.)*
- **Cohort / sector-momentum activation (BIDIRECTIONAL) — the memory surge (MU/SNDK/SKHY, MS multi-year-tailwind call +
  Nokia "shortage-through-2027") + INTC/AI-data-center strength vs the STM/TXN chip-loser bifurcation; GOOGL cloud +82%
  re-rated the neocloud cohort (IREN/NBIS/WULF).** No rule reads a cohort-wide move (`sector_rotation_momentum` claims
  only DELL). *Research: a cohort / sector-risk overlay handling both the de-rate and the re-rate.*
- **AI-capex-debt / valuation-shock (event-scale) — GOOGL's $205B capex ceiling + halted 33-qtr buyback + first
  negative FCF since 2004; Nikkei's ~$1.65T off-balance-sheet AI-debt study; Burry/Zitron.** The event-scale bear
  thesis on AI *funding* (demand still printed strong: GOOGL cloud +82%/$514B backlog, INTC DC&AI +59%). Recurring;
  argues for an event-scale valuation/credit filter. Structural overhang into MSFT/META (7/29), AMZN/AAPL (7/30).
- **Competitive / product event — Google's in-house AI inference chips to sell on-prem vs Nvidia (NVDA; rev 2027).**
  No rule reads a competitor's product entry. *Research: a product/competitive-event overlay.*
- **Regulatory / policy overlay — Lina Khan → NYC EDC (META/AMZN, municipal); Clarity Act (GS/JPM); Bessent
  Chinese-AI-sanctions threat; the AI-data-center electricity-ratepayer pledge; China chip curbs; USTR 25% Brazil
  tariff.** No rule reads a regulatory/policy shift. *Research: a policy/regulatory-event overlay.*
- **Geopolitical / energy-shock overlay — Houthi tanker strikes (kinetic), Brent >$100 (+40% MTD, first since May),
  10-yr yield 18-mo high, inflation read-through into the 7/28–29 FOMC.** No rule reads an oil/geopolitical shock.
  *Research: a macro/energy-shock risk overlay.* **Escalation-watch: a full Bab-el-Mandeb closure strands ~7% of
  global supply; Goldman sees $120+ by Q4 if disruptions persist.**
- **Macro-data / rates overlay — jobless claims 187K (fewest since 1969) + oil → 10-yr yield to an 18-month high.**
  No rule reads a rates/macro-data surprise. *Research: a rates/macro overlay for rate-sensitive posture.*
- **Vol-regime / dispersion activation (persistent) — VIX 16.64 *falling* on a −2.15% Nasdaq day, with extreme
  single-name dispersion (INTC +7–13% vs TSLA −14% vs STM −18%); dense event IV into MSFT/META 7/29, AMZN/AAPL 7/30,
  AMD/SPCX 8/4.** Options skeletons (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`)
  exist but none active / none claims a universe symbol. Dispersion, not index vol — screen single-name / event-IV.
- **Index / forced-flow + float mechanics — SPCX share unlock ahead (carry); SKHY (Korea leveraged-ETF margin,
  carry).** No `index_rebalance` gap_type exists. Argues for a 6th Tier-B trigger / forced-flow overlay
  (`NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`).
- **event_driven_catalyst exit CALIBRATION (exit side proven live 7/8→7/9).** Is `max_hold_days: 7` right? Backtest
  the time-stop horizon + the 2×ATR hard-stop multiple. Add re-entry-on-new-catalyst.
- **Fallback-threshold question (issue #5)** — no-price-history routes to `equity_watch_only` correctly (SKHY/SPCX).
  Open case: the degenerate 0-trade Sharpe-0.0 backtest (AMD/IREN/NBIS/NOW/STM/UNH/GS/MS/PYPL/RIVN) routing to a
  below-baseline *trading* provisional. Decide whether a 0-trade score should route to watch_only.
- **Validate first-pass + provisional assignments via head-to-head** (carry): breakout vs trend on ARM/MRVL/INTC;
  bollinger vs trend on CSCO; rsi vs trend on HPE; sector-rotation vs trend on DELL; macd on META/MSFT/SNDK; trend
  placeholders → AAPL/AMZN/CBRS/GOOGL/JPM/NUVL/NVDA/QQQ/SPY/TSLA/TSM.
- **Healthcare breadth — still thin (UNH + NUVL).** Awareness only (not a trade directive).

## Open questions for the operator

1. **[HIGH — timing] Schedule reliability — apparently recovered.** 7/7 & 7/8 double-fired; 7/9–7/16 clean;
   **7/17, 7/20, Sat 7/18 DROPPED**; **7/21 + 7/22 + 7/23 all fired on time ✓.** Confirm single-trigger + no-drop
   config is stable.
2. **[HIGH] Repair the interpreter** — bare `python3` = Homebrew 3.14.5 (no deps). Repoint task/daily_prompt to
   `.venv/bin/python3` or reinstall deps.
3. **[HIGH — carry] Overdue provisionals + skipped research.** QCOM/SPCX/SYNA overdue (`revalidate_by 7/21`, no Sat
   7/18 research); **SKHY hits `7/24` today** and overdues if Sat 7/25 also misses. The provisional book is now **14**
   and only shrinks when research validates/archives — if research keeps missing, add a trader escalation path.
4. **[MEDIUM — now ACTIVE] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` fires whenever a live
   order rests, and there IS one now (the META sell). Read open orders client-direct until fixed. Worth a real fix.
5. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/21–7/23 (all fresh & on-time), but the
   7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden brief-synthesis + git-sync.
6. **[MEDIUM] Fallback threshold (issue #5)** — degenerate 0-trade Sharpe-0.0 → trading-provisional vs watch_only
   (AMD/IREN/NBIS/NOW/STM + UNH/GS/MS/PYPL/RIVN).
7. **FOURTEEN provisional/quarantined claims** — AMD/IREN/NBIS (`2026-08-04`) + NOW/STM (`2026-08-06`) + GS
   (`2026-07-28`) + MS/PYPL (`2026-07-29`) + QCOM/SPCX/SYNA (`2026-07-21 OVERDUE`) + SKHY (`2026-07-24`) + RIVN
   (`2026-07-27`) + UNH (`2026-07-30`). Saturday research owns validation. Do NOT hand-promote.
8. **[LOW] Proportionality — tech/AI universe concentration.** NOW/STM (both tech/semis) added today; off-theme beats
   (BX/CMCSA) noted 7/23 but not added. The news agent's standing proportionality question is still unanswered.
   Operator awareness only.
