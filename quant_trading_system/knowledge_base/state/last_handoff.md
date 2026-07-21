# Handoff to tomorrow's Claude

(Run on the **2026-07-21 (Tuesday) clock** — canonical post-close, snapshot read **2026-07-21 16:03 PT**,
`is_open false`, `next_open 2026-07-22 09:30 ET`. **SINGLE FIRE** — git log had no `[trader 2026-07-21]` commit
before this run (last trader commit was `[trader 2026-07-16]`; between them: only one `[news 2026-07-21]`). Ran
everything via the venv. **KEEP day on a constructive semi-led rebound:** book unchanged (META only, +5.84%,
pulled back from 7/16's +9.89% through the two skipped/down sessions but green/trending), 3 new names promoted &
triaged to quarantined provisionals, `cli execute` a clean no-op. **⚠️ FIRST COVERED SESSION SINCE 7/16 — see the
run-gap note.**)

## ✅ TL;DR — KEEP. BOOK STILL META-ONLY, NOTHING TO RECONCILE, EXECUTE A CLEAN NO-OP

No trades, no rotations, no edits. The book stayed **META only** (+5.84%, down from 7/16's +9.89% through the two
un-covered down sessions before today's rebound, but still green and above its MACD exit). The P0 action was
triaging the **three newly-promoted names** — **NBIS (Nebius), IREN, AMD** — all of which landed as below-baseline
**provisionals** on `equity_event_driven_catalyst` (Sharpe 0.0 / 0 trades each), execution-quarantined,
`revalidate_by 2026-08-04`. `cli execute` fired 0 intents. Today's event stack (a broad semi-led relief rally on
strong Korea/Taiwan export data + a memory-price upturn; hard single-name catalysts: SMCI record >$60B backlog
+18% AH, NVDA's 9.3% Nebius stake, RKLB's $266M defense contract, INTC +5% on a Google Cloud deal, IREN's raised
>$4B AI-cloud guidance) was event-dense but **constructive and orderly** (VIX ~18.65, no >2% futures gap), and
every material single-name item was `responder: NONE` (informational under the mandate), so nothing traded and
nothing should have.

## ⚠️ RUN-GAP: FIRST COVERED SESSION SINCE 2026-07-16 (two trader/news days + Sat research DROPPED)

The scheduled runs for **Fri 7/17 and Mon 7/20 did NOT fire** (no `[news]`/`[trader]` commits for either day), and
**Saturday 7/18 research did NOT run** (no research commit). This run is the first coverage since Thursday 7/16.
Consequences handled this run:
- **The book ran un-triaged for two trading days.** Reconciled carefully: it is **NOT a wipe** (see snapshot) — the
  book is intact (META at exact prior qty/avg-entry), cash unchanged to the penny, no `trade_closed` events. Because
  no `execute` fired on 7/17 or 7/20, META simply rode its own MACD rule with no algorithmic action; nothing closed,
  nothing to `log-closed`. A multi-day skipped-run gap leaves the book frozen-in-amber, safe to resume from.
- **Three overdue provisionals: QCOM / SPCX / SYNA hit `revalidate_by 2026-07-21` with no Saturday research to
  revalidate them.** They are now **overdue but stay quarantined** — the trader does NOT validate (that's research's
  job); logged for research + flagged to the operator. No action beyond keeping them quarantined.
- **Two days of promotions arrived at once:** the 7/21 news agent promoted NBIS/IREN/AMD (universe 37 → 40); all
  three triaged this run.

## NEWS BRIEF WAS FRESH & ON-TIME — NOTABLE, NOT HALT-WORTHY

`state/news_brief.md` header = **`2026-07-21`** — correctly dated, a genuine fresh Tuesday run (one `[news
2026-07-21]` commit, 197 Alpaca items; NVDA 26 / MU 18 / MSFT 14). **Assessment: NOTABLE — an event-dense but
constructive session that snapped a three-session losing streak; NOT halt-worthy.** Nasdaq +1.29% (25,837), S&P
+0.89% (7,509), Dow +0.74%, SOX +5.2%, VIX ~18.65 (−0.6%). The threads that landed:
1. **A broad semiconductor/memory relief rally with a fundamental driver, not just flow** — strong South Korea +
   Taiwan export data confirmed AI/semiconductor demand; memory prices turned up (Micron +12%, Sandisk +14%, DRAM
   ETF +11-12%, SOX +5.2%). A near-exact mirror-reversal of last Thursday's chip de-rate.
2. **SMCI pre-announced a blowout Q4** — record >$60B new-order backlog, gross margin 15-17% vs an 8.2-8.4% guide →
   +18% AH. A hard earnings-window pre-announcement (full report Aug 11).
3. **NVDA disclosed a 9.3% equity stake in Nebius (NBIS)** — a strategic-investment event that re-rated the neocloud
   cohort.
4. **RKLB won a $266M defense contract; INTC +5% on a Google Cloud AI deal; IREN raised AI-cloud guidance >$4B on
   $2.8B of new contracts.**

**No HALT trigger fires:** (1) no FOMC today (next 7/28-29); (2) held name **META had no adverse single-name event**
— quite the opposite (Ackman long/"cheap stock," ARK added, "Meta Compute" neocloud push continues); (3)
Iran/Hormuz (conflict resumed) did **not** gap equity futures >2% — equities in fact rallied through it. The
AI-capex-doubt tail is still the market's #1 named fear (BofA fund-manager survey) even on an up day, but the tape
rallied around it. NOTABLE does not gate execute → decision unaffected.

## Snapshot (7/21 16:03 PT, via venv)

- **`market-status`:** `is_open false`, `now 2026-07-21T16:03:05 PT`, `next_open 2026-07-22 09:30 ET`. Canonical
  post-close slot, **single fire ✓** (no `[trader 2026-07-21]` commit existed pre-run; last was `[trader 2026-07-16]`,
  only one `[news 2026-07-21]` between).
- **Account:** equity **$104,940.05**, cash **$94,690.29** (UNCHANGED to the penny from 7/16/7/15/7/14/7/13),
  buying_power $407,460.49, day_trade_count 0.
- **Positions — META only:** META 16 @ avg $605.28, cur **$640.61, +5.84% GREEN** (+$565.35 unreal, mv $10,249.76).
  `momentum_macd_histogram`-owned; MACD exit NOT triggered (still trending). Gave back part of the run (7/16's +9.89%
  at $665.11) through the two un-covered down sessions, then held green into today's rebound.
- **Open orders:** **empty** (confirmed pre- and post-execute).
- **Regime:** bull, conf 0.68, ADX 17.88, realized_vol 0.1136 (a touch softer than 7/16's 0.69/19.38/0.1354 —
  consistent with the intervening chop, still clearly bull).

**NOT a wipe, NOTHING to reconcile.** Wipe signature = *flat* book + unchanged cash + no `trade_closed` events. Here
the book is NOT flat — META persists at its exact prior qty/avg-entry. Cash unchanged is *expected* (AVGO/MU/ORCL
closed & reconciled 7/9; META still held; nothing pending to close; no execute ran during the 7/17-7/20 gap). No
freeze, no `log-closed`.

## P0 triage (mandatory-attach) — NBIS/IREN/AMD promoted → 3 quarantined provisionals

The news pipeline promoted **three names** (universe **37 → 40**), all landing unclaimed. Each is a Tier-0
news-subject with a hard discrete catalyst; each triaged with `--gap-type event_catalyst`:
- **NBIS (Nebius)** — NVDA disclosed a 9.3% equity stake. → `triage-symbol NBIS --gap-type event_catalyst`
- **IREN** — raised AI-cloud revenue guidance >$4B on $2.8B of new contracts. → `triage-symbol IREN --gap-type event_catalyst`
- **AMD** — Microsoft AI deal (7/20) + Advancing AI 2026 event (7/21), +8%. → `triage-symbol AMD --gap-type event_catalyst`

**All three verdict `provisional_claim` → `equity_event_driven_catalyst`**, execution-quarantined,
**`revalidate_by 2026-08-04`**. Each scored **Sharpe 0.000 on 0 trades** (< baseline 0.50) → below-baseline
**trading** provisional. Same **degenerate-0-trade** case (issue #5) as UNH (7/16), GS (7/14), MS + PYPL (7/15),
RIVN (7/13): these are established names WITH deep price history (real backtests ran), but
`equity_event_driven_catalyst` fired 0 trades in-window → Sharpe 0.0 → read as a rankable candidate → routed to a
below-baseline *trading* provisional (NOT the no-history watch_only route). No new durable lesson — reconfirms
issue #5.

After triage: `unclaimed_count 0`, claimed **40/40**, `provisional_count 9 → 12`:
- `equity_event_driven_catalyst` (9, quarantined): **AMD `2026-08-04`, GS `2026-07-28`, IREN `2026-08-04`,
  MS `2026-07-29`, NBIS `2026-08-04`, PYPL `2026-07-29`, QCOM `2026-07-21 (OVERDUE)`, RIVN `2026-07-27`,
  UNH `2026-07-30`**
- `equity_watch_only` (1): **SKHY `2026-07-24`** (no-history route)
- `equity_trend_following_ema_cross` (1): **SPCX `2026-07-21 (OVERDUE)`** (no-history route)
- `equity_pairs_trading_cointegration` (1): **SYNA `2026-07-21 (OVERDUE)`**

Did NOT re-triage any of the pre-existing 9 (research owns validation). The three OVERDUE (QCOM/SPCX/SYNA) stay
quarantined — the trader cannot validate; logged for research + operator. `gap-registry coverage_holes` per the
brief: **empty**.

## `cli execute` — clean no-op

`submitted_count 0, rejected_count 0, error_count 0`. Every executing strategy returned 0 intents:
- **META** (macd_histogram) held — MACD exit not triggered (still green/trending, +5.84%).
- **event_driven_catalyst did NOT re-enter AVGO/MU/ORCL** — its non-quarantined claims (flat since the 7/9 close).
  No fresh *discrete single-name* entry catalyst fired for its `evaluate()`. ORCL bounced ~4% with the sector but is
  still near 52-wk lows and last week's cash-burn story did not advance — a cohort bounce is not a responder event.
- **Every hard catalyst today was `responder: NONE`** — each hit a symbol whose claiming strategy doesn't read that
  event type: **SMCI's +18% backlog pre-announcement** went unresponded (SMCI on `mean_reversion_bollinger`, not an
  earnings-window responder — the acute recurring gap, live again like TSM 7/16); **NVDA's Nebius stake / AMD's MS
  deal** (no strategic-investment responder); **RKLB's contract win** (on `breakout_volume_confirmation`, reads
  price/volume not awards); **INTC's Google Cloud deal** (partnership, unassigned).
- **Provisionals quarantined/skipped:** all 12 (`AMD, GS, IREN, MS, NBIS, PYPL, QCOM, RIVN, SKHY, SPCX, SYNA, UNH`)
  — symbol-level quarantine working, incl. the three new NBIS/IREN/AMD.

Book confirmed unchanged post-execute (META 16 only, cash $94,690.29, no open orders, equity $104,940.05).

## Decision: KEEP

No rotations, no strategy edits, no parameter changes. **One manual bullet added** (skipped-run doctrine — see
below), because a multi-day dropped-runs gap is a distinct operational anomaly from a wipe or a double-fire and the
manual had no explicit handling for it. The day traced cleanly: healthy book (META only) → 3 names promoted →
triaged/quarantined → execute clean no-op. Nothing fired and nothing should have on a constructive rebound where
every single-name event was `responder: NONE`.

## Summary of what I did today (7/21 post-close)

1. **Read context** — daily_prompt.md, manual.md, tasks.md (7/17-dated — two runs were skipped), last_handoff.md
   (7/16), news_brief.md. **Date-checked the brief: header `2026-07-21` = today → FRESH & on-time.** NOTABLE
   (constructive rebound), not halt-worthy.
2. **Confirmed interpreter** — `.venv/bin/python3` throughout (bare `python3` still Homebrew 3.14.5, no deps).
3. **`market-status` + git log** — 16:03 PT canonical post-close; **single fire** (last trader commit `[trader
   2026-07-16]`, only `[news 2026-07-21]` between; handoff narrated 7/16 not 7/21). Detected the **run-gap**: no
   7/17, 7/20, or Sat 7/18 commits.
4. **Broker snapshot** — account/positions/open-orders/regime. Book = META only (+5.84%), cash unchanged, no open
   orders → healthy continuation, NOT a wipe (book intact, not flat). Nothing pending to reconcile.
5. **P0 triage** — `list-active` showed unclaimed 3 (NBIS/IREN/AMD, newly promoted). Triaged each with `--gap-type
   event_catalyst` → all `provisional_claim` / `equity_event_driven_catalyst` (Sharpe 0.0/0 trades →
   below-baseline trading provisional), quarantined, `revalidate_by 2026-08-04`. Re-checked: `unclaimed_count 0`,
   claimed 40/40, `provisional_count 12`.
6. **`cli execute`** — 0 intents / 0 submitted / 0 rejected / 0 errors; 12 provisionals quarantined/skipped. No
   re-entry into the just-exited names. Confirmed positions (META only) + cash (unchanged) post-execute.
7. **Decision: KEEP** — refreshed library gaps for Saturday research, flagged the 3 overdue provisionals + the
   dropped-runs schedule issue to the operator, added one manual bullet (skipped-run doctrine). git-sync last.

## Observations and reasoning

- **Two skipped sessions, then a clean resume — the book was frozen-in-amber.** Because no `execute` ran on 7/17 or
  7/20, nothing algorithmic happened: META rode its MACD rule, no closes, cash to the penny. This is the third
  distinct operational anomaly the harness has produced (after the double-fire on 7/7-7/8 and the transient wipe on
  7/7), and it is the *benign* one — the correct response is simply to resume normally, reconcile nothing, and note
  that any provisional `revalidate_by` deadlines that lapsed during the gap (QCOM/SPCX/SYNA, all 7/21) are now
  overdue-but-still-quarantined. The wipe/freeze doctrine does NOT trigger here because its signature requires a
  *flat* book — ours is intact. (Captured as a durable manual bullet this run.)
- **Last Thursday's chip de-rate reversed almost exactly.** The same semiconductor/memory complex that sold off
  ~6% on 7/16's TSM-capex fear rallied hard today (SOX +5.2%, MU +12%, SNDK +14%) on strong Korea/Taiwan export
  data and a memory-price upturn — a real, event-driven regime turn, not just a bounce. But the structural tension
  didn't resolve: an AI-capex-driven credit event is still the #1 named tail risk in the BofA survey, above Iran and
  tariffs. "Who funds the buildout, at what margin" persists; the tape simply rallied around it. Nothing in the
  library reads a cohort-wide capex re-rating in *either* direction — logged (again) as a gap.
- **The neocloud / "compute is the new oil" cohort re-rated on hard catalysts, and it drove today's promotions.**
  NVDA's 9.3% Nebius stake and IREN's $2.8B-contract guidance raise are concrete strategic events, not sentiment —
  which is exactly why the news agent promoted NBIS and IREN (plus AMD on its Microsoft deal). All three land
  quarantined; Saturday research owns whether any clears baseline. Note the proportionality tension the news agent
  flagged: all three are AI/semis, continuing the universe's tech concentration — an open operator question.
- **The earnings-window assignment gap got its cleanest live example yet.** SMCI pre-announced a blowout (+18% AH on
  a record >$60B backlog) and nothing responded because SMCI is on `mean_reversion_bollinger`, not an earnings-window
  strategy — a carbon copy of TSM on 7/16. With TSLA printing tomorrow AMC (7/22, ~6% implied, on a trend-following
  claim), INTC/ARM 7/23, MSFT 7/29, AMZN/AAPL 7/30, this is the single most acute recurring gap and the top Saturday
  research priority.
- **META held constructively.** It gave back part of its run through the two un-covered down days but rebounded green
  today; its MACD rule stayed long and untriggered. Today's META touchpoints (Ackman long, ARK buying, Meta-Compute
  momentum) are constructive/positioning, not an adverse single-name shock — no basis to override the rule.
- **Book is clean and cash-heavy.** $94.7k cash / $104.9k equity = ~90% cash, one live position (META, +5.84%).
  Active set intact (9 strategies incl. watch_only, 40/40 claimed); **12 provisionals quarantined** (9 → 12 with
  NBIS/IREN/AMD); everything else awaiting an entry signal its strategy hasn't fired.
- **Live tails to watch:** (1) the **AI-capex-doubt** structural fear persists even after today's re-rate — a
  dispersion regime (single-name chip swings of ±12-14% under VIX ~18.65), not a panic; (2) **Iran/Hormuz resumed**
  (Iran struck three vessels; ceasefire framework broke down), oil elevated (gasoline ~$4), but equities rallied
  through it — a >2% futures gap is the halt line and it is NOT there; (3) **China chip-manufacturing curbs**
  (TSM/QCOM exposure) under consideration; USTR 25% Brazil tariff effective 7/22. **TSLA prints 7/22 AMC.** Positions
  still ride their own rules.

## Final state at session end

- **Positions:** META 16 @ $605.28 (cur $640.61, +5.84%) — the only live position.
- **Open orders:** none.
- **Account:** equity $104,940.05, cash $94,690.29, day_trade_count 0.
- **Active set:** 9 strategies × **40/40 claimed** (`unclaimed_count 0`); **12 PROVISIONAL** (AMD/IREN/NBIS
  `2026-08-04`; GS `2026-07-28`; MS/PYPL `2026-07-29`; QCOM/SPCX/SYNA `2026-07-21 OVERDUE`; SKHY `2026-07-24`;
  RIVN `2026-07-27`; UNH `2026-07-30`), all execution-quarantined.
- **Regime:** bull, conf 0.68, ADX 17.88, realized_vol 0.1136.
- **Reconciliation:** none needed (nothing closed). **`cli execute`: RAN, 0 submitted.**
- **Code/strategy changes:** none. **Manual:** one bullet appended (skipped-run doctrine).

## Open issues for the operator

1. **[HIGH — timing] Schedule reliability — now BOTH failure modes seen.** 7/7 & 7/8 **double-fired**; 7/9-7/16 each
   fired once ✓; then **7/17, 7/20 (trader/news) and Sat 7/18 (research) DROPPED entirely** — this run is the first
   coverage since 7/16. The schedule has now produced both extra fires and missed fires. Confirm the trigger config.
2. **[HIGH] Bare `python3` broken (Homebrew 3.14.5, no deps).** Everything runs via
   `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`. Repoint the task/daily_prompt or reinstall deps.
3. **[HIGH — new] THREE overdue provisionals with no research to revalidate.** QCOM/SPCX/SYNA all hit
   `revalidate_by 2026-07-21` and Saturday 7/18 research did not run, so they are overdue and stay quarantined. If
   research keeps missing, these (and the growing provisional book, now 12) never get validated or archived —
   consider an escalation path when research is skipped.
4. **[MEDIUM] News-pipeline staleness / partial-run (issue #4).** Did NOT bite today (brief fresh & on-time), but the
   7/10 partial run is unfixed — still add the `date_in_file == today` guard AND harden the news agent's
   brief-synthesis/commit step.
5. **[MEDIUM] `cli open-orders` parser bug** — `'dict' object has no attribute 'id'` whenever a live order rests.
   Dormant now (no live orders). Worth a real fix before the next resting exit.
6. **[MEDIUM] Fallback-threshold question (issue #5).** The degenerate 0-trade Sharpe-0.0 case keeps recurring —
   NBIS/IREN/AMD today (established names, deep history, 0 trades in-window → below-baseline *trading* provisional
   instead of watch_only), joining UNH/GS/MS/PYPL/RIVN. Decide whether a 0-trade backtest should route to watch_only.
7. **TWELVE provisional/quarantined claims** — AMD/IREN/NBIS (`2026-08-04`), GS (`2026-07-28`), MS/PYPL
   (`2026-07-29`), QCOM/SPCX/SYNA (`2026-07-21 OVERDUE`), SKHY (`2026-07-24`), RIVN (`2026-07-27`), UNH
   (`2026-07-30`). Saturday research owns validation. Do NOT hand-promote.
8. **[LOW] Proportionality — universe tech/AI-concentration.** The news agent again flagged its standing question:
   NBIS/IREN/AMD are all AI/semis. The operator's proportionality directive is still unanswered. Awareness only.

## Git-sync status

Ran `cli git-sync --agent trader --message "..."` (via venv) as the last action. State files changed
(last_handoff.md, tasks.md, active_strategies.md, provisional_claims.md, manual.md, journal) plus any untracked news
HTML from today's pipeline run. git-sync queues a JSON marker to `.git-sync-queue/`; the operator's launchd
LaunchAgent (`com.harness.gitrunner`) runs the actual push. Expect `{"ok": true, "queued": ...}`. If markers pile up
across runs, the LaunchAgent isn't installed — run `bash scripts/install_git_safety.sh`.
