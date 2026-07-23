# Handoff to tomorrow's Claude

(Run on the **2026-07-23 (Thursday) clock** — canonical post-close, snapshot read **2026-07-23 16:03 PT**,
`is_open false`, `next_open 2026-07-24 09:30 ET`. **SINGLE FIRE** — git log had no `[trader 2026-07-23]` commit
before this run (last trader commit was `[trader 2026-07-22]`; the only 7/23 commit was `[news 2026-07-23]`). Ran
everything via the venv. **NOT a KEEP no-op day — a real ALGORITHMIC EXIT fired:** META's MACD-histogram exit
triggered and `cli execute` **submitted a market DAY sell of the full 16-share META position** — it rests for the
7/24 open. Book was META-only and intact going in (not a wipe), no promotions-were-already-there but the news agent
promoted **NOW + STM** (universe 40→42) which I triaged to quarantined provisionals. Schedule holding — 7/21, 7/22,
7/23 all single-fired on time after the 7/17+7/20 drops.)

## 🔴 TL;DR — THE MACD EXIT FIRED. ONE SELL ORDER IS RESTING. TOMORROW MUST RECONCILE THE FILL.

Not a no-op. `equity_momentum_macd_histogram` finally tripped its exit on META (**"Exit: MACD hist -1.8108 flipped
negative"** — histogram crossed below zero after a three-session momentum rollover: +5.84% on 7/21 → +2.59% on 7/22 →
+0.35% today). `cli execute` **submitted 1 intent: SELL META 16 @ market, TIF day** — order
`db566584-d77f-4b10-982c-12839ab4867d`, status **accepted / filled_qty 0** (resting; a post-close DAY market order
will fill at the **7/24 open**). All safety checks passed (paper/restricted/position_size/daily_loss/max_positions).
I did **not** override it — this is the strategy doing exactly its job; the algorithmic-only mandate forbids me from
countermanding a strategy's own exit. Everything else fired 0 intents; all **14** provisionals were
quarantined/skipped.

**➡️ THE SINGLE MOST IMPORTANT THING FOR TOMORROW (7/24): reconcile the META fill from the ACTUAL fill price, not
today's mark.** See the "MANDATORY reconciliation" block below. This is the exact 7/9 MU sign-flip situation —
overnight the tape has Brent >$100 + a risk-off session + META's Lina-Khan item, so META could gap either way; today's
+0.35% mark is NOT the fill.

## NEWS BRIEF WAS FRESH & ON-TIME — NOTABLE, NOT HALT-WORTHY

`state/news_brief.md` header = **`2026-07-23`** — correctly dated, a genuine fresh Thursday run (one `[news
2026-07-23]` commit, 213 Alpaca items; GOOGL 35 / TSLA 29 / INTC 18 / SPCX 17 / NVDA 16). **Assessment: NOTABLE — a
genuine risk-off session (the Magnificent Seven's worst day since April 2025), NOT halt-worthy.** Nasdaq Composite
**−2.15%** (25,137.69), S&P 500 **−1.21%** (7,408.30), Dow **−0.97%** (51,711.65). What actually happened:
1. **The GOOGL/TSLA capex shock crystallized in the regular session.** **GOOGL −7%** as the market re-read Wed's print
   through capex: 2026 capex raised to **$195–205B**, a **33-quarter buyback streak ended**, and its **first negative
   FCF since the 2004 IPO** (despite record $112B profit / +24% rev / +82% cloud / $514B backlog). **TSLA −14%** (worst
   day in >1yr) on a Q2 EPS miss (~⅓ light), a non-cash SpaceX-stake gain = ~69% of GAAP profit. Mag7 ETF ~−4%.
   **Neither is a held name.**
2. **INTC printed a blowout AMC (a universe name).** Rev $16.1B (**+25% YoY, fastest in ~15 yrs**) vs $14.43B est; EPS
   $0.38 vs $0.21; **Data Center & AI +59% to $6.3B**; raised Q3 guide; **+7–13% AH**.
3. **Oil topped $100.** Houthis **struck two Saudi tankers** (Encelia, Layla) — the blockade turned kinetic. **Brent
   +6.45% to ~$101.10** (first >$100 since May; ~40% MTD); **10-yr yield to an 18-month high** (oil + a 1969-low 187K
   jobless print).

**No HALT trigger fires:** (1) no FOMC today (next **7/28–29**); (2) held name **META had no adverse major single-name
event** — only the modest, municipal Lina-Khan→NYC-EDC appointment (cross-listed AMZN); META reports **7/29**; (3) the
**oil shock did NOT gap equity futures >2%** — the S&P fell −1.21% *intraday*, and, tellingly, **VIX actually eased to
16.64 (−2.4%)** even as the index dropped. A −2.15% Nasdaq day led by two idiosyncratic mega-cap earnings reactions,
with vol falling, is NOTABLE — not a halt. NOTABLE does not gate execute → decision unaffected (and today execute
*did* act, but only because a strategy's own rule fired, not because of the brief).

## Snapshot (7/23 16:03 PT, via venv)

- **`market-status`:** `is_open false`, `now 2026-07-23T16:03:05 PT`, `next_open 2026-07-24 09:30 ET`. Canonical
  post-close slot, **single fire ✓** (no `[trader 2026-07-23]` commit pre-run; last was `[trader 2026-07-22]`, only
  `[news 2026-07-23]` between; prior handoff narrated 7/22 not 7/23).
- **Account:** equity **$104,406.45**, cash **$94,690.29** (UNCHANGED to the penny from 7/22/7/21/7/16/…),
  buying_power $94,690.29, day_trade_count 0.
- **Positions — META only (going in):** META 16 @ avg $605.28, cur **$607.37, +0.35% GREEN** (+$33.51 unreal, mv
  $9,717.92). `momentum_macd_histogram`-owned; **MACD exit TRIGGERED this run** (histogram −1.8108, flipped negative).
  Rolled over from +5.84% (7/21) → +2.59% (7/22) → +0.35% (today) — momentum decay, exactly what the histogram-negative
  exit is designed to catch.
- **Open orders:** **empty pre-execute**; **one resting sell post-execute** (the META exit, `db566584…`, confirmed
  client-direct — see below). NOTE: `cli open-orders` throws `'dict' object has no attribute 'id'` (the known parser
  bug) now that a live order exists — read open orders **client-direct** (`AlpacaClient(...).get_open_orders()` returns
  dicts; use `.get('id')` etc.).
- **Regime:** bull, conf 0.68, ADX 17.8, realized_vol 0.1168 (essentially identical to 7/22 — still clearly bull).

**NOT a wipe, NOTHING to reconcile at the START of this run.** Going in, the book was NOT flat — META persisted at its
exact prior qty/avg-entry, cash unchanged (expected: AVGO/MU/ORCL closed & reconciled 7/9; nothing was pending to
close before execute). NOT a double-fire (single `[news 2026-07-23]`, no prior `[trader 2026-07-23]`). The
reconciliation obligation is created BY this run's execute (the new resting sell), for TOMORROW to settle.

## P0 triage (mandatory-attach) — 2 promotions, both triaged to quarantined provisionals

The news agent promoted **NOW (ServiceNow)** and **STM (STMicroelectronics)** → universe **40 → 42**, both UNCLAIMED.
`list-active` going in: `unclaimed_count 2` (NOW, STM), claimed 40/42, `provisional_count 12`. Triaged both:
- **`triage-symbol NOW --gap-type earnings_window`** → `verdict: provisional_claim` on `equity_event_driven_catalyst`,
  **Sharpe 0.000 < 0.500** (degenerate 0-trade — issue #5), QUARANTINED, `revalidate_by 2026-08-06`.
- **`triage-symbol STM --gap-type earnings_window`** → same: `provisional_claim` on `equity_event_driven_catalyst`,
  **Sharpe 0.000**, QUARANTINED, `revalidate_by 2026-08-06`.

Re-ran `list-active`: **`unclaimed_count 0`, claimed 42/42, `provisional_count 14`.** P0 gate satisfied. Did NOT
re-triage the 12 existing provisionals (research owns validation). Did NOT `add-active` (forbidden).

The **14** quarantined provisionals now:
- `equity_event_driven_catalyst` (11, quarantined): **AMD `2026-08-04`, GS `2026-07-28`, IREN `2026-08-04`,
  MS `2026-07-29`, NBIS `2026-08-04`, NOW `2026-08-06` (NEW), PYPL `2026-07-29`, QCOM `2026-07-21 (OVERDUE)`,
  RIVN `2026-07-27`, STM `2026-08-06` (NEW), UNH `2026-07-30`**
- `equity_watch_only` (1): **SKHY `2026-07-24` (TOMORROW — will overdue if no Sat 7/25 research)** (no-history route)
- `equity_trend_following_ema_cross` (1): **SPCX `2026-07-21 (OVERDUE)`** (no-history route)
- `equity_pairs_trading_cointegration` (1): **SYNA `2026-07-21 (OVERDUE)`** (onsemi merger-arb)

**Three still OVERDUE (QCOM/SPCX/SYNA, `revalidate_by 7/21`)** — Saturday 7/18 research never ran. **SKHY hits `7/24`
tomorrow.** The trader cannot validate (research's job); logged for research + flagged to operator. `gap-registry
coverage_holes`: **empty**.

## `cli execute` — 1 SUBMITTED (the META exit), 0 rejected, 0 errors

`submitted_count 1, rejected_count 0, error_count 0`.
- **`equity_momentum_macd_histogram` fired 1 intent → SELL META 16 @ market (TIF day), SUBMITTED.** Order
  `db566584-d77f-4b10-982c-12839ab4867d`, status `accepted`, filled_qty 0 (resting for the 7/24 open). Exact reasoning
  (captured via a read-only `evaluate()` replay — no second submission): **"Exit: MACD hist -1.8108 flipped
  negative."** MSFT/SNDK (its other claims) fired nothing (not held).
- **`equity_event_driven_catalyst` fired 0 intents** — its non-quarantined claims are AVGO/MU/ORCL (flat since 7/9).
  **ORCL's $6.99B/10-yr Navy IDIQ ("Pentagon") contract was the ONE live-responder event today** (event_driven_catalyst
  validated-claims ORCL and declares `event_catalyst`), but its `evaluate()` generated **NO entry on the award** — same
  as the 7/15 ORCL Japan-cloud tag. So even the one event with a responder produced no trade. (Research question:
  does its `evaluate()` actually fire on a government-contract award, or only earnings-type catalysts?)
- **Every other hard catalyst was `responder: NONE`:** INTC's blowout (on `breakout_volume_confirmation` — reads
  price/volume, no earnings-window responder; note the +7–13% AH pop *could* trip the breakout rule on a confirmed
  session move tomorrow, the trader's call); GOOGL −7% & TSLA −14% (both on `trend_following`, earnings-window gap);
  SMCI (3rd straight session, on `mean_reversion_bollinger`); the memory cohort MU/SNDK/SKHY (no cohort responder).
- **Provisionals quarantined/skipped:** all 14 (`AMD, GS, IREN, MS, NBIS, NOW, PYPL, QCOM, RIVN, SKHY, SPCX, STM, SYNA,
  UNH`) — symbol-level quarantine working, incl. the two new ones.

Post-execute book: **META still 16 (sell is resting, not filled)**, cash still $94,690.29, **one open order**
(db566584). Nothing has settled yet — the reconciliation is tomorrow's.

## Decision: KEEP the strategy set (but a real exit fired)

No rotations, no strategy edits, no parameter changes, no manual bullet. The MACD-histogram exit firing is the
strategy set working as designed — a decision to KEEP it, not to change it. The day traced cleanly: intact book (not a
wipe) → 2 promotions triaged to quarantined provisionals → execute where exactly one strategy's own exit rule tripped
on its held name. I did not manufacture, block, or modify any order. (I did NOT re-add a manual bullet — the fill-
reconciliation discipline is already in the manual's "Recent feedback": the 7/9 MU `log-closed`-from-actual-fill
lesson covers this exact case.)

## ⏭️ MANDATORY reconciliation for TOMORROW (7/24) — read this first

The META sell (`db566584-d77f-4b10-982c-12839ab4867d`, market DAY) fills at the **7/24 open**. Tomorrow's run is
post-close 7/24, hours after the open, so under normal timing it WILL have filled. Steps, in order:

1. **Snapshot first.** `account`, `positions`, `open-orders` (use client-direct for open-orders — CLI parser bug).
   Expect: **META GONE (flat book), cash UP by ~the fill proceeds** (≈ filled_avg_price × 16 ≈ ~$9.7k), equity ~flat.
   This is a **"cash UP + position vanished" = legitimate fill/close — NOT a wipe.** (Wipe = flat book + cash
   *unchanged* + no `trade_closed`. Here cash RISES, so it's a fill.) Do NOT freeze.
2. **Pull the ACTUAL fill, client-direct:**
   `AlpacaClient(Settings(_env_file='.env')).get_order('db566584-d77f-4b10-982c-12839ab4867d')` → returns a dict; read
   `status` / `filled_avg_price` / `filled_qty` / `filled_at`.
3. **`log-closed` from the REAL fill, not today's mark (the 7/9 MU sign-flip lesson):**
   ```
   cli log-closed equity_momentum_macd_histogram META <pnl_fraction>
   ```
   where `pnl_fraction = (filled_avg_price − 605.275625) / 605.275625`. Today's +0.35% mark ($607.37) is NOT the fill —
   overnight risk-off + Brent >$100 + META's Lina-Khan item could move the open either way. Cross-check: cash rise
   should ≈ `filled_avg_price × 16` to the penny; if it matches, the close is confirmed legit AND arithmetically
   complete.
4. **If — anomalously — the order is STILL resting AND META still shows held at tomorrow's run:** do NOT run `cli
   execute` blindly. `equity_momentum_macd_histogram.evaluate()` will re-emit "sell META 16" (histogram still
   negative) → a SECOND resting sell → **oversell into a short** when both fill. First cancel the stale order (or wait
   for fill) and reconcile; only then execute. (Under normal fill timing this won't happen — the market order fills at
   the open — but guard it.)
5. After META closes, the book is **fully flat / all cash (~$104k)**. `equity_event_driven_catalyst` still claims
   AVGO/MU/ORCL (flat since 7/9) + provisionals; no held position to hand-manage. Then run the standard workflow
   (triage any NEW unclaimed name, `cli execute`).

## Summary of what I did today (7/23 post-close)

1. **Read context** — daily_prompt.md, manual.md, tasks.md (7/22-dated), last_handoff.md (7/22), news_brief.md.
   **Date-checked the brief: header `2026-07-23` = today → FRESH & on-time.** NOTABLE risk-off, not halt-worthy.
2. **Confirmed interpreter** — `.venv/bin/python3` (3.13.13) throughout (bare `python3` still Homebrew 3.14.5, no
   deps).
3. **`market-status` + git log** — 16:03 PT canonical post-close; **single fire** (last trader commit `[trader
   2026-07-22]`, only `[news 2026-07-23]` between). Schedule holding (7/21+7/22+7/23 all fired on time).
4. **Broker snapshot** — account/positions/open-orders/regime. Book = META only (+0.35%), cash unchanged to the penny,
   no open orders going in → healthy continuation, NOT a wipe (book intact), NOT a double-fire. Nothing pending to
   reconcile at the start.
5. **P0 triage** — `list-active` showed `unclaimed_count 2` (NOW + STM promoted, universe 40→42). Triaged both
   `--gap-type earnings_window` → both `provisional_claim` on `equity_event_driven_catalyst` (Sharpe 0.0,
   degenerate-0-trade issue #5), quarantined `revalidate_by 2026-08-06`. Re-ran `list-active`: `unclaimed_count 0`,
   claimed 42/42, `provisional_count 12→14`. Did NOT re-triage the 12 existing provisionals.
6. **`cli execute`** — **1 intent submitted: SELL META 16 @ market (MACD-histogram exit, "hist -1.8108 flipped
   negative")**, resting order `db566584…` for the 7/24 open; 0 rejected / 0 errors; 14 provisionals
   quarantined/skipped; event_driven_catalyst fired 0 (no entry on ORCL's contract award). Captured the exact exit
   reason via a read-only `evaluate()` replay (no duplicate submission — confirmed exactly ONE open order after).
7. **Decision: KEEP** — the exit is the strategy working as designed; no rotations/edits/params/manual bullet.
   Refreshed library gaps for Saturday research, flagged the 3 overdue provisionals (QCOM/SPCX/SYNA) + SKHY's 7/24
   deadline + the schedule question to the operator. git-sync last.

## Observations and reasoning

- **The book is turning over for the first time in weeks.** META has been the sole position and a persistent KEEP for
  the whole recent stretch; its MACD histogram finally flipped negative today (−1.8108) as the +5.84%→+2.59%→+0.35%
  slide rolled momentum over. The exit is textbook: the strategy is designed to ride momentum and step out when the
  histogram crosses zero, and it did. After tomorrow's fill the book goes flat/all-cash — the harness is back to a
  clean slate, waiting on the next strategy entry signal.
- **The one event with a responder still produced no trade.** ORCL's $7B Navy/Pentagon IDIQ is claimed by
  `equity_event_driven_catalyst` (validated) and is a discrete contract-award catalyst, but `evaluate()` emitted no
  entry — consistent with 7/15's ORCL Japan-cloud tag. Whether the strategy is *supposed* to fire on a government
  award (vs only earnings-type catalysts) is a live research question; logged. Every other hard catalyst
  (INTC blowout, GOOGL −7%, TSLA −14%, SMCI, memory cohort) was `responder: NONE` — the same acute earnings-window
  assignment gap, now with a **universe blowout (INTC)** in hand alongside GOOGL/TSLA.
- **The AI-capex bear thesis went from murmur to roar — and it's a library gap, not a book event.** GOOGL's $205B
  capex ceiling + halted buyback + first negative FCF since 2004 was the spark; a Nikkei study pegged Big Tech's
  off-balance-sheet AI debt at ~$1.65T; Burry warned of "$100 oil colliding with the AI-debt explosion." But the
  *demand* side still printed strong (GOOGL cloud +82%/$514B backlog; INTC DC&AI +59%) — the fight is over funding /
  margins / debt, not demand. No held name is exposed and no rule reads a cohort-wide capex re-rating; logged as a gap.
  This is the structural overhang into MSFT/META (7/29) and AMZN/AAPL (7/30).
- **A real energy/geopolitical escalation, but the halt line held.** The Houthi blockade turned kinetic (two Saudi
  tankers struck); Brent >$100 (+40% MTD), 10-yr yield to an 18-month high, a fresh inflation tail into the 7/28–29
  FOMC. Yet equities did NOT gap >2% and VIX *fell* to 16.64 — the market read it as an orderly, earnings-driven
  pullback, not a panic. No energy names in the universe; informational. **Escalation-watch persists:** a full
  Bab-el-Mandeb closure (~7% of global supply) + a >2% overnight futures gap would flip tomorrow's halt calculus.
- **META held constructively right up to the exit.** It stayed green (+0.35%) into the close; its only item today
  (Lina Khan → NYC EDC) is municipal and cross-listed (AMZN), not adverse-major. The exit was momentum-mechanical
  (histogram cross), not news-driven. META Q2 is 7/29 — moot for the position once tomorrow's sell fills.
- **Provisional book grew to 14 and still only research can shrink it.** NOW + STM added today (both degenerate-0-trade
  Sharpe-0.0 → below-baseline trading provisionals, issue #5). QCOM/SPCX/SYNA remain `revalidate_by 7/21` OVERDUE
  (Sat 7/18 research never ran); **SKHY hits 7/24 tomorrow.** If Sat 7/25 research also slips, five provisionals are
  overdue. The trader cannot validate — operator escalation path still open.
- **Schedule looks solid.** 7/21, 7/22, 7/23 all single-fired on time. The 7/17+7/20 drops appear to be behind us, but
  confirm the trigger config is stable.

## Final state at session end

- **Positions:** META 16 @ $605.28 (cur $607.37, +0.35%) — **but a market DAY sell of all 16 is RESTING**
  (`db566584-d77f-4b10-982c-12839ab4867d`), fills 7/24 open. Effectively exiting.
- **Open orders:** ONE — `db566584…` META sell 16 @ market, TIF day, status accepted.
- **Account:** equity $104,406.45, cash $94,690.29 (unchanged; the sell hasn't settled), day_trade_count 0.
- **Active set:** 9 strategies × **42/42 claimed** (`unclaimed_count 0`); **14 PROVISIONAL** (AMD/IREN/NBIS
  `2026-08-04`; NOW/STM `2026-08-06`; GS `2026-07-28`; MS/PYPL `2026-07-29`; QCOM/SPCX/SYNA `2026-07-21 OVERDUE`;
  SKHY `2026-07-24`; RIVN `2026-07-27`; UNH `2026-07-30`), all execution-quarantined.
- **Regime:** bull, conf 0.68, ADX 17.8, realized_vol 0.1168.
- **Reconciliation:** NONE done today (nothing had closed at snapshot time); **ONE created for tomorrow** (the resting
  META sell — see the MANDATORY block above). **`cli execute`: RAN, 1 submitted.**
- **Code/strategy changes:** none. **Manual:** no bullet appended.

## Open issues for the operator

1. **[HIGH — timing] Schedule reliability — apparently recovered.** 7/7 & 7/8 double-fired; 7/9–7/16 clean;
   **7/17, 7/20, Sat 7/18 DROPPED**; **7/21 + 7/22 + 7/23 all fired on time ✓.** Confirm the single-trigger,
   no-drop config is stable.
2. **[HIGH] Bare `python3` broken (Homebrew 3.14.5, no deps).** Everything runs via
   `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`. Repoint the task/daily_prompt or reinstall deps.
3. **[HIGH — carry] Overdue provisionals + skipped research.** QCOM/SPCX/SYNA overdue (`revalidate_by 7/21`, no Sat
   7/18 research); **SKHY hits `7/24` tomorrow** and overdues if Sat 7/25 also misses. The provisional book is now
   **14** and only shrinks when research validates/archives — if research keeps missing, add a trader escalation path.
4. **[MEDIUM — now ACTIVE, was dormant] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` fires
   whenever a live order rests, and there IS one now (the META sell). Read open orders client-direct until fixed
   (`AlpacaClient(...).get_open_orders()` → list of dicts, use `.get('id')`). Worth a real fix before the next resting
   exit.
5. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite 7/21–7/23 (all fresh & on-time), but the
   7/10 partial run is unfixed — add a `date_in_file == today` guard AND harden brief-synthesis + git-sync.
6. **[MEDIUM] Fallback-threshold question (issue #5).** The degenerate 0-trade Sharpe-0.0 case keeps recurring —
   AMD/IREN/NBIS/NOW/STM/UNH/GS/MS/PYPL/RIVN all routed to a below-baseline *trading* provisional instead of
   watch_only. Decide whether a 0-trade backtest should route to watch_only.
7. **FOURTEEN provisional/quarantined claims** — AMD/IREN/NBIS (`2026-08-04`), NOW/STM (`2026-08-06`), GS
   (`2026-07-28`), MS/PYPL (`2026-07-29`), QCOM/SPCX/SYNA (`2026-07-21 OVERDUE`), SKHY (`2026-07-24`), RIVN
   (`2026-07-27`), UNH (`2026-07-30`). Saturday research owns validation. Do NOT hand-promote.
8. **[LOW] Proportionality — universe tech/AI-concentration.** NOW/STM (both tech/semis) added today; the news agent's
   standing proportionality question (off-theme beats like BX/CMCSA noted but not added) is still unanswered.
   Awareness only.

## Git-sync status

Ran `cli git-sync --agent trader --message "..."` (via venv) as the last action. State files changed
(last_handoff.md, tasks.md; active_strategies.md + provisional_claims.md via the NOW/STM triage; journal updated with
the META sell order) plus any untracked news HTML from today's pipeline run. git-sync queues a JSON marker to
`.git-sync-queue/`; the operator's launchd LaunchAgent (`com.harness.gitrunner`) runs the actual push. Expect
`{"ok": true, "queued": ...}`. If markers pile up across runs, the LaunchAgent isn't installed — run
`bash scripts/install_git_safety.sh`.
