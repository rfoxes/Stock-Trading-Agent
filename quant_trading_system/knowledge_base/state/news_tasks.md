# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**✅ SCHEDULE RESTORED.** This was a genuine, fresh **Monday 2026-07-13** run firing at the ~15:35 PT slot with **7/13 data** (news-fetch stamped 7/13; quotes/WebSearch all 7/13). The prior 7/10 brief's staleness (Friday data completed late Monday) is now resolved. `market-status` at run: `is_open false`, `now 2026-07-13T15:39 PT`, `next_open 2026-07-14T09:30 ET`. Next trader run is post-close 7/13 ~4 PM PT; **next news run is Tue 7/14 ~3:30 PM PT — and 7/14 is the single most event-dense day of the week (see below).**

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Mon 2026-07-13). **Risk-off but contained, NOT halt-worthy.** Three threads: (1) **AI-memory / DRAM cohort selloff** — Samsung's *record* prelim Q2 (~$58.4B op profit, ≈19× YoY) disappointed on supercycle *sustainability* fears → shares -10.7% Seoul → dragged MU (-5%), SNDK (-5%), SK Hynix/SKHY (-15.4% Seoul), WDC; DRAM ETF ~-30%/month ("bear market"); (2) **fresh US-Iran airstrikes over the Strait of Hormuz** (container-ship attack trigger), oil +~5% (Brent ~$79.59), but US futures contained (S&P -0.3% / Nasdaq -0.8% — below the >2% halt bar); (3) **dense 7/14 stack** = June CPI + Warsh testimony + FIVE big-bank prints (JPM/GS/BAC/C/WFC BMO). VIX 17.16 (+14%, +2.13 pt — just under the 3-pt bar). Held **META** had *constructive* events (Hyperion $50B+ capex, AI-API priced 75% below OpenAI/Anthropic). **No FOMC today, no >2% futures gap, no adverse held-name catalyst → NOTABLE, not halt-worthy.**
- **UNIVERSE GREW 32 → 33 under Tier-0.** Promoted **RIVN (Rivian, consumer_discretionary)** — news-subject with a hard catalyst (discounted **75M-share public offering**, dilutive raise, own coverage line). Lands **UNCLAIMED** → trader mandatory-attach triage (expect thin/degenerate backtest → watch/provisional). EV peer to TSLA.
- **Held book:** universe `by_source` still shows **positions = META only**. No reconcile for the news agent.
- **Interpreter:** bare `python3` STILL BROKEN (Homebrew 3.14.x, no harness deps). Use **`/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`** from repo root before EVERY CLI call. **Bash cwd drifts between calls — `cd /Users/rfoxes/Stock-Trading-Agent &&` prefix each command** (hit this again today: a bare-relative `.venv/bin/python3` call failed "no such file or directory" mid-run).
- **Pre/post-promotion state:** pre → universe 32, claimed 32, unclaimed 0, provisional 4 (QCOM/SKHY/SPCX/SYNA). Post-RIVN → **universe 33, claimed 32, unclaimed 1 (RIVN), provisional 4 (QCOM/SKHY/SPCX/SYNA)**. **WULF is NO LONGER provisional** — research released it to validated `equity_rsi_divergence` (with HPE) on 7/11 (Sharpe 0.880/12tr). `gap-registry coverage_holes` **empty** (confirmed again).
- **Alpaca density: 129 items** (vs 109 on 7/10). NVDA 14, MU 12, SPCX 12, META 10, AAPL 9, TSLA 9, SNDK 8, AMZN 7, GOOGL/JPM/MSFT 6, SKHY 5, ORCL/TSM 4, QQQ 3, ARM/AVGO/BE/INTC/SPY 2, CSCO/MRVL/RKLB/WULF 1; zeros: CBRS/DELL/HPE/IRDM/NUVL/QCOM/SMCI/SYNA. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline:** header dated 2026-07-13 (fresh, on-time). Prior: 7/10 (late-completed Friday data), 7/9 fresh, 7/8 fresh.

## Notable carry-forwards

- **AI-MEMORY COHORT — the story flipped from euphoria to de-rate.** Friday = SK Hynix debut euphoria; Monday = Samsung's record-but-"disappointing" guidance triggered a full-cohort selloff (MU/SKHY/SNDK/WDC down mid-single-digits, DRAM ETF -30%/month). **Sustain-check for 7/14+:** does the AI-memory de-rate deepen (supercycle-pace repricing) or bounce? Watch MU into any oversold signal, SKHY hold-vs-fade, and whether Micron's $6.9B reshoring (Trump) / $250B capex narrative re-anchors it.
- **US-IRAN / STRAIT OF HORMUZ (NEW, acute geopolitical).** Active airstrike exchange over the Strait (container-ship attack trigger); oil +5%. **7/14 checks:** did it escalate overnight? Any equity-futures >2% gap (the halt-worthy line)? Oil follow-through (energy names, chips→energy rotation)? This is the live geopolitical tail.
- **7/14 EVENT STACK (MOST URGENT) — everything lands tomorrow morning:** June CPI 8:30 AM (consensus headline ~3.8% YoY / core ~2.8% / monthly ~-0.2%) → **log the actual print vs consensus**; Warsh first semi-annual testimony (House Tue / Senate Wed) → tone (patient vs hawkish); **five big banks BMO — JPM/GS/BAC/C/WFC** (implied moves GS 6.0 / C 5.5 / WFC 5.5 / BAC 4.5 / JPM 4.4%). Last inflation read before 7/28-29 FOMC.
- **META (held) — constructive day.** Hyperion data center → $50B+ (capex); AI API priced ~75% below OpenAI/Anthropic (JPMorgan: enterprise-adoption lever). Noted overbought/near resistance. EU DSA "addictive features" finding (Fri) still open, no fresh escalation. Rides MACD.
- **TSM — June revenue +67.9% YoY (real demand signal); Q2 report THIS WEEK** (large implied move). Earnings-window assignment gap.
- **TSLA — Model S/X production line closing at Fremont → repurposed for Optimus humanoid production** (product/manufacturing pivot). Q2 earnings 7/22.
- **AAPL — Epic v. Apple App Store-fee battle new phase; Apple v. OpenAI (7/10) still trending.** Litigation track. Watch for rulings/escalation.
- **SPCX (PROVISIONAL/quarantined) — IPO-aftermath selloff:** new 52-wk lows, ~-35% from record 1 month post-IPO; **George Noble "900% float explosion" as lockups expire** (float/forced-flow mechanics); Musk orbital data centers (Chanos skeptic). Stays non-tradable.
- **BE — Hunterbrook short-report saga continues** (management/analyst pushback). Thesis unresolved.
- **INTC — Q2 earnings 7/23**; JPM's Q3-short call (Fri) is a carry. Held ~$102.50 support today.
- **Earnings run: JPM/GS/BAC/C/WFC 7/14, TSM this week, TSLA 7/22, ARM/INTC 7/23, AMZN 7/30.** Event-IV building.
- **Vol regime — VIX 17.16 (+14%), off Friday's ~15.84.** Risk-off pop, still MID band. Event-IV into CPI + bank earnings + TSM. Single-name memory/IPO dispersion elevated.

## To do on the next run (Tue 7/14)

1. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` from repo root, `cd`-prefixed on EVERY CLI call.** Re-read `news_manual.md §9` (Tier 0 = promote every US-tradable news-subject on first appearance, uncapped; Tier A recurrence = prioritization; Tier B still applies; all require `--sector`).
2. **LOG THE 7/14 STACK AS IT PRINTS:** June CPI actual vs ~3.8%/2.8% consensus (headline + core + monthly); Warsh testimony tone; JPM/GS/BAC/C/WFC results + reactions. This is the highest-value output tomorrow. Same-day timing matters — the trader run is post-close 7/14.
3. **RIVN follow-through** — confirm the trader triaged RIVN (unclaimed → claimed/provisional; expect watch-grade on thin history). Track whether the 75M-share offering priced and any further dilution detail.
4. **Memory cohort** — de-rate deepen vs bounce? MU/SKHY/SNDK/WDC; Micron reshoring ($6.9B / $250B) re-anchor? Samsung read-through.
5. **US-Iran / Hormuz** — escalation check; oil follow-through; equity-futures gap (halt-worthy only if >2%). Energy vs chips rotation.
6. **META (held)** — any capex/pricing follow-through; EU DSA status. Rides MACD.
7. **Confirm universe = 33 / claimed 32 / unclaimed (RIVN until triaged) / provisional 4 (QCOM/SKHY/SPCX/SYNA).** WULF is validated (not provisional) — don't relist it.
8. **Vol regime** — VIX vs 17.16; event-IV into CPI + bank prints + TSM. Log concrete single-name UOA on universe names ONLY (today's whale alerts were scanner rollups, not sized sweeps).
9. **Outlier movers + sector breakdown.** Today: clean promote (RIVN). Tracked (not promoted): bank peers GS/BAC/C/WFC (financials under-represented — only JPM; consider a peer), WDC (memory sympathy, recurring), Samsung (foreign), NBIS (AI-neocloud, Meta-competition).
10. **Library gaps re-listing** (see brief): earnings-window assignment (JPM 7/14 URGENT / TSM / TSLA / ARM / INTC / AMZN); cohort-selloff/sentiment-reversal (AI-memory de-rate, NEW); regulatory/litigation (AAPL Epic + v OpenAI, META EU DSA); capex/capital-allocation (META Hyperion $50B, MU reshoring); index/forced-flow + lockup/float (SPCX "900% float explosion", NEW_CATEGORY_NEEDED); activist-short (BE); geopolitical/energy-shock overlay (US-Iran/oil, NEW); vol-regime activation; new-listing no-history triage (RIVN, SKHY).

## Open questions for the operator

- **[MEDIUM] Bare `python3` still broken.** Homebrew 3.14.x lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Repoint the launcher + prompt to the venv (or pip-install requirements into 3.14). Bash cwd drifts — `cd` repo-root prefix every call.
- **[MEDIUM] Trader schedule double-fire (7/7, 7/8).** Confirmed recurring on order-submitting days; 7/9/7/10 each fired once. Confirm the single-trigger config before a double-fire lands where the 2nd run could act twice.
- **[MEDIUM] News-brief staleness guard.** The 7/10-data-completed-late-Monday episode motivated a `_load_news_brief()` staleness check (parse date_in_file, reject/down-weight if >1 session old). Today's run is fresh so it's not biting, but the guard is still unbuilt.
- **[MEDIUM] Fallback-threshold question (carry, now with RIVN).** A no/low-price-history or 0-trade backtest attaches a below-baseline *trading* provisional rather than routing to `equity_watch_only`. SKHY correctly routed to watch_only (no history); WULF (had history, degenerate 0-trade) got a trading provisional then was validated 7/11. RIVN is the next test case (limited history + a fresh dilutive offering). Should a degenerate/empty backtest count as "rankable" or "no signal → watch_only"?
- **Index-inclusion / float-mechanics as a 6th Tier-B trigger? — recurring (SPCX lockup "900% float explosion"; leveraged single-stock/DRAM ETFs; SK Hynix→Nasdaq Comp carry).** Forced-flow gap keeps recurring.
- **Financials breadth — only JPM in the universe** while GS/BAC/C/WFC all report alongside it 7/14. Consider adding one bank peer for sector breadth (news agent left them as candidates, not auto-promoted, since it was a cohort earnings preview rather than single-name catalysts).
- **Earnings-window assignment — JPM (7/14 URGENT), TSM (this week), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** Earnings-window responders (`equity_event_driven_catalyst`/`long_straddle_earnings`) don't claim these. Sat research: assign.
- **New event-window sub-triggers (recurring) — cohort-selloff/sentiment-reversal (NEW: AI-memory de-rate), regulatory/litigation (AAPL Epic/OpenAI, META EU DSA), capex (META Hyperion, MU reshoring), activist-short (BE), geopolitical/energy-shock (NEW: US-Iran/oil), product/manufacturing (TSLA Optimus line).** No rule reads any of these.
- **M&A-arb activation — RKLB (acquirer)/IRDM (target) + SYNA/onsemi.** `equity_pairs_trading_cointegration` claims only SYNA. Sat: activate merger-arb.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists. (Not re-checked — news agent doesn't pull broker state.)
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate in `.git-sync-queue/`.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim.
- **Sunset watch:** no universe symbol yet hit the 0-news-across-30-sessions + no-position sunset criterion; keep tracking (CBRS/IRDM/NUVL/SYNA recurring zeros but recently added / claimed).

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **129 items** cleanly (via venv). Zeros: CBRS/DELL/HPE/IRDM/NUVL/QCOM/SMCI/SYNA.
- `cli market-status` at run start → `is_open false`, `now 2026-07-13T15:39 PT`, `next_open 2026-07-14T09:30 ET`. Fresh on-time Monday run.
- `cli list-active` (pre-promotion) → universe 32, claimed 32, unclaimed 0, provisional 4 (QCOM/SKHY/SPCX/SYNA). `gap-registry coverage_holes` empty. Post-promotion → universe 33, claimed 32, unclaimed 1 (RIVN).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier 0 (news-subject inclusion, uncapped):** Promoted **RIVN** (own coverage "Why Is Rivian Falling Monday?" + hard catalyst = discounted 75M-share public offering; US-tradable NASDAQ). Foreign/not-cleanly-US-tradable subjects (Samsung/SSNLF) tracked. Cohort/sympathy (WDC, NBIS) and pure price-explainers on existing universe names (MU/INTC/SNDK/ORCL/ARM "why is X falling") NOT promoted (already in-universe or no hard catalyst).
  - **Tier B:** RIVN's offering is a capital-raise, not one of the 5 codified Tier-B triggers; promotion rests on Tier-0. Bank peers (GS/BAC/C/WFC) had earnings-tomorrow catalysts but arrived as a cohort preview, not single-name subject coverage → left as candidates, not auto-promoted (financials-breadth question logged for operator).
  - **Decision: 1 promotion (RIVN, Tier-0). Universe 32 → 33.**
- **SKHY ticker lifecycle (resolved):** SKHY is now the live regular-way ticker on Alpaca (5 news items 7/13, quoting). The temporary when-issued line SKHYV appears only in a couple of stale Friday cross-tags — effectively retired; no phantom to chase. Promoted-ticker choice (SKHY over SKHYV) validated.
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest; headlines+summaries only (don't WebFetch full articles).
