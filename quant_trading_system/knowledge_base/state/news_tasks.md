# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**✅ FRESH, ON-TIME Tuesday 2026-07-14 run** firing at the ~15:39 PT slot with 7/14 data (news-fetch stamped 7/14; quotes/WebSearch all 7/14). `market-status` at run: `is_open false`, `now 2026-07-14T15:39 PT`, `next_open 2026-07-15T09:30 ET`. Next trader run is post-close 7/14 ~4 PM PT; **next news run is Wed 7/15 ~3:30 PM PT.** The 7/14 event stack (the week's densest) is now BEHIND us and resolved constructively — see below.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Tue 2026-07-14). **Event-dense but constructive/orderly, NOT halt-worthy.** Four threads, all net market-friendly: (1) **June CPI cooler than expected** — headline -0.4% MoM / **3.5% YoY** (vs -0.2% / 3.8% consensus, from 4.2%), core **flat / 2.6% YoY** (vs +0.2% / 2.9%); biggest monthly headline drop since April 2020, energy-led; cut near-term rate-hike odds; last read before 7/28-29 FOMC. (2) **Bank blowouts** — JPM EPS $6.14 vs $5.85, rev $58.02B, **profit +41%**; **GS best quarter in history** (EPS $20.98, rev $20.34B +39%, +6.9%, IB fees SpaceX-IPO-boosted); BAC/C/WFC also strong. (3) **Warsh hawkish debut** — "no tolerance" for inflation, rejected "mission accomplished" → tempered the dovish print. (4) **US-Iran/Hormuz escalated a 3rd day** — port blockade reimposed, tankers hit, oil 1-month high (WTI $79.34, Brent $84.73), but **US equities closed GREEN (Nasdaq 100 +1.09%) — no >2% gap.** Memory cohort BOUNCED (hedge funds bought semis fastest in 3.5yr; SKHY +6% / MU +3% / SNDK +5% / NVDA +3%). VIX ~17 (flat/lower, orderly). **No HALT trigger:** no FOMC today, META no adverse catalyst, no >2% futures gap.
- **UNIVERSE GREW 33 → 34 under Tier-0.** Promoted **GS (Goldman Sachs, financials)** — news-subject (best quarter in its history, +6.9%, dedicated coverage); also fills the recurring financials-breadth gap (JPM had been the only bank). Lands **UNCLAIMED** → trader P0 triage (`triage-symbol GS --gap-type earnings_window`; GS has real history → expect a rankable backtest / trading claim or below-baseline provisional, NOT the no-history watch_only route).
- **Held book:** universe `by_source` still shows **positions = META only**. No reconcile for the news agent.
- **Interpreter:** bare `python3` STILL BROKEN (Homebrew 3.14.x, no harness deps). Use **`/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`** from repo root before EVERY CLI call. Bash cwd can drift between calls — `cd /Users/rfoxes/Stock-Trading-Agent &&` prefix if a bare-relative call fails. (This run: all CLI calls ran clean from repo root via the venv, no cwd drift hit.)
- **Pre/post-promotion state:** pre → universe 33, claimed 33, unclaimed 0, provisional 5 (QCOM/SPCX/SYNA 7/21, SKHY 7/24, RIVN 7/27). Post-GS → **universe 34, claimed 33, unclaimed 1 (GS), provisional 5 (unchanged)**. **WULF is validated** (`equity_rsi_divergence`), not provisional — don't relist. `gap-registry coverage_holes` **empty** (confirmed again).
- **Alpaca density: 144 items** (vs 129 on 7/13). NVDA 15, JPM 12, SKHY 11, MU 10, MSFT 9, AMZN/GOOGL 8, META/SNDK 7, AAPL/ORCL 6, SPY 5, AVGO/QQQ/TSLA/TSM 4, INTC 3, RIVN/WULF 2, ARM/BE/CBRS/CSCO/DELL/IRDM/MRVL/RKLB/SMCI 1; zeros: HPE/NUVL/QCOM/SYNA. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline:** header dated 2026-07-14 (fresh, on-time). Prior: 7/13 (fresh), 7/10 (late-completed Friday data), 7/9 fresh.

## Notable carry-forwards

- **AI-MEMORY COHORT — the story flipped BACK to constructive.** 7/13 = Samsung-guidance de-rate; **7/14 = sharp rebound** (hedge funds bought US semis fastest in 3.5yr, "selloff has run its course"; SKHY +6% / MU +3% / SNDK +5%). **Sustain-check for 7/15+:** does the bounce hold or was it a one-day reflex? Watch SK Hynix scarcity dynamics (ADR ~50% premium to Seoul; new 2×-leveraged HYNX ETF), Micron follow-through, and whether the momentum-factor "crash" (Goldman: worst 3-week factor draw-down on record) keeps rotating leadership.
- **7/14 EVENT STACK — RESOLVED, now carries.** June CPI cool (log actual 3.5%/2.6% ✓ done); Warsh hawkish (Senate testimony **Wed 7/15** — second read on tone); JPM/GS/BAC/C/WFC all printed strong (JPM +41% profit, GS best-ever). **7/15 checks:** Warsh Senate tone; June PPI + Empire State manufacturing (Wed 7/15); MS reports Wed 7/15.
- **US-IRAN / STRAIT OF HORMUZ (acute, escalating — 3rd day).** Port blockade reimposed, tankers hit, oil 1-month high; gasoline seen >$4/gal within 7-10 days. **7/15 checks:** did it escalate overnight? Any equity-futures >2% gap (the halt line — NOT there yet, tape green)? Oil follow-through + the inflation read-through (June CPI predates this spike). Live geopolitical/energy tail.
- **GS (newly promoted, UNCLAIMED) — confirm the trader triaged it.** Expect `earnings_window` triage; GS has real history so it should route to a trading claim or below-baseline provisional (NOT watch_only). Track post-earnings drift.
- **META (held) — quiet corporate day.** No fresh catalyst; only touchpoint = NY 50MW data-center freeze (capex/permitting headwind, shared with MSFT/AMZN/GOOGL). Prior constructive capex/pricing carries intact. Rides MACD.
- **TSM — Q2 earnings THU 7/16** (June sales +67.9% YoY; consensus ~59% profit jump; large implied move). Earnings-window assignment gap.
- **NVDA — cut >half of Asian AI-chip customers (China export screening); Vera Rubin roadmap slight delay.** Regulatory/product track. AAPL — record 20% smartphone share (+3% growth) vs a KeyBanc Underweight cut. RKLB — Neutron engine hot-fire test passed (milestone toward late-2026 debut).
- **AAPL — KeyBanc cut to Underweight (20% downside call); Epic + v OpenAI litigation carries.** Litigation/rating track.
- **SPCX (PROVISIONAL/quarantined) — Cathie Wood added $21.3M; SpaceXAI leasing idle Grok capacity to Anthropic; pundit bear takes (Schiff/Yusko).** Lockup/float "900% explosion" carry. Stays non-tradable.
- **Earnings run: JPM/GS 7/14 (done), MS 7/15, TSM 7/16, TSLA 7/22, ARM/INTC 7/23, AMZN 7/30.** Event-IV building.
- **Vol regime — VIX ~17, flat/lower, orderly.** Wide single-name dispersion (GS +6.9% / SNDK +5% vs ARM -6%) under a calm index; momentum-factor crash flagged by Goldman.

## To do on the next run (Wed 7/15)

1. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` from repo root** (cd-prefix if a bare call fails). Re-read `news_manual.md §9` (Tier 0 = promote every US-tradable news-subject on first appearance, uncapped; Tier A recurrence = prioritization; Tier B still applies; all require `--sector`).
2. **Warsh Senate testimony (Wed 7/15) tone** — second read; hawkish-consistent or softer? **June PPI + Empire State (Wed 7/15)** — log actuals vs consensus. **MS reports Wed 7/15** — single-name bank print (candidate follow-through).
3. **GS follow-through** — confirm the trader triaged GS (unclaimed → claimed/provisional; expect a rankable `earnings_window` outcome, NOT watch_only). Post-earnings drift.
4. **Memory cohort** — did the 7/14 bounce hold or fade? SKHY scarcity/ADR-premium/HYNX-ETF dynamics; MU follow-through; momentum-factor rotation.
5. **US-Iran / Hormuz** — escalation check; oil follow-through; equity-futures gap (halt-worthy only if >2%). Inflation read-through (gasoline >$4/gal forward).
6. **META (held)** — any capex/permitting follow-through (NY freeze); EU DSA status. Rides MACD.
7. **Confirm universe = 34 / claimed 33 (after GS triage → 34) / provisional 5 (QCOM/SPCX/SYNA 7/21, SKHY 7/24, RIVN 7/27).** WULF is validated — don't relist.
8. **Vol regime** — VIX vs ~17; event-IV into TSM 7/16. Log concrete single-name UOA on universe names ONLY (today's whale alerts were scanner rollups, not sized sweeps — same as prior runs).
9. **Outlier movers + sector breakdown.** Today: clean promote (GS). Tracked (not promoted): BAC/C/WFC (bank cohort, session 2), MS (reports 7/15), IBM (AI-spend-doubt), UMC (silicon-photonics mass production), WDC (memory sympathy, recurring).
10. **Library gaps re-listing** (see brief): earnings-window assignment (JPM/GS printed unresponded, TSM 7/16 URGENT, TSLA/ARM/INTC/AMZN); cohort sentiment-reversal bidirectional (AI-memory de-rate→rebound); regulatory/export-control (NVDA China screening, AAPL litigation, META EU DSA); policy/capex-headwind (NY data-center freeze); index/forced-flow + ETF/float (SKHY ADR-premium/HYNX, SPCX lockup, NEW_CATEGORY_NEEDED); product/engineering-milestone (RKLB Neutron, NVDA Vera Rubin, TSLA Optimus); geopolitical/energy-shock (US-Iran/oil); vol-regime activation; new-listing no-history triage (SKHY/RIVN).

## Open questions for the operator

- **[MEDIUM] Bare `python3` still broken.** Homebrew 3.14.x lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Repoint the launcher + prompt to the venv (or pip-install requirements into 3.14).
- **[MEDIUM] Trader schedule double-fire (7/7, 7/8).** 7/9–7/13 each fired once. Confirm the single-trigger config before a double-fire lands where the 2nd run could act twice.
- **[MEDIUM] News-brief staleness guard.** The 7/10-data-completed-late-Monday episode motivated a `_load_news_brief()` staleness check (parse date_in_file, reject/down-weight if >1 session old). Recent runs are fresh so it's not biting, but the guard is still unbuilt.
- **[MEDIUM] Fallback-threshold question (carry).** No/low-price-history or 0-trade backtest attaches a below-baseline *trading* provisional rather than routing to `equity_watch_only` (SKHY→watch_only when zero bars; RIVN/WULF degenerate-0-trade → trading provisional). GS (promoted today) has real history and should NOT hit this path — clean test of the "has-history → rankable" branch. Should a degenerate/empty backtest count as "rankable" or "no signal → watch_only"?
- **Financials breadth — GS now added (JPM+GS).** BAC/C/WFC/MS remain candidates (session 2). Consider whether a 2nd operator-approved bank peer is wanted, or whether GS+JPM is sufficient breadth.
- **Index-inclusion / float-mechanics as a 6th Tier-B trigger? — recurring** (SKHY ADR ~50% premium + 2×-leveraged HYNX ETF launch; SPCX lockup "900% float explosion"; leveraged single-stock/DRAM ETFs). Forced-flow gap keeps recurring.
- **Earnings-window assignment — JPM/GS (printed 7/14, unresponded), TSM (7/16), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** Earnings-window responders (`equity_event_driven_catalyst`/`long_straddle_earnings`) don't claim these. Sat research: assign. Two blowout prints just went unresponded.
- **New event-window sub-triggers (recurring) — cohort sentiment-reversal (bidirectional: AI-memory de-rate→rebound), regulatory/export-control (NVDA China, AAPL litigation, META EU DSA), policy/capex-headwind (NY data-center freeze), product/engineering-milestone (RKLB Neutron, NVDA Vera Rubin, TSLA Optimus), activist-short (BE), geopolitical/energy-shock (US-Iran/oil).** No rule reads any of these.
- **M&A-arb activation — RKLB (acquirer)/IRDM (target) + SYNA/onsemi.** `equity_pairs_trading_cointegration` claims only SYNA. Sat: activate merger-arb.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists. (Not re-checked — news agent doesn't pull broker state.)
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate in `.git-sync-queue/`.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim.
- **Sunset watch:** no universe symbol yet hit the 0-news-across-30-sessions + no-position sunset criterion; keep tracking (CBRS/IRDM/NUVL/QCOM/SYNA recurring zeros but recently added / claimed).

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **144 items** cleanly (via venv). Zeros: HPE/NUVL/QCOM/SYNA.
- `cli market-status` at run start → `is_open false`, `now 2026-07-14T15:39 PT`, `next_open 2026-07-15T09:30 ET`. Fresh on-time Tuesday run.
- `cli list-active` (pre-promotion) → universe 33, claimed 33, unclaimed 0, provisional 5 (QCOM/SPCX/SYNA 7/21, SKHY 7/24, RIVN 7/27). `gap-registry coverage_holes` empty. Post-promotion → universe 34, claimed 33, unclaimed 1 (GS).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier 0 (news-subject inclusion, uncapped):** Promoted **GS** (dedicated coverage "Goldman Sachs Posts Upbeat Q2 Earnings" + hard catalyst = best quarter in its history, +6.9%; US-tradable NYSE). Rationale progression: on 7/13 GS was a *cohort earnings preview* (correctly not promoted); on 7/14 it *reported* a single-name blowout with dedicated coverage → Tier-0 subject. Also resolves the recurring financials-breadth gap.
  - **NOT promoted:** BAC/C/WFC (cohort earnings coverage, not single-name subject), MS (reports 7/15, price-action framing), IBM (AI-spend-doubt sentiment peg, no hard catalyst), UMC (modest mid-tier-foundry milestone; semis over-represented), WDC (memory sympathy). All tracked as candidates.
  - **Decision: 1 promotion (GS, Tier-0). Universe 33 → 34.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE <month> <year>" query format works; per-name reconstruction beats generic gainers/losers (the "biggest gainers S&P 500" query returned Indian-market Nifty data — reconstruct from per-name Alpaca instead); major-M&A → target per-name search is cleanest; headlines+summaries only (don't WebFetch full articles). VIX exact-close quotes can diverge across aggregators on a busy day — report "~level, regime" not false precision.
