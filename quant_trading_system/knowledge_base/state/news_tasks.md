# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**⚠️ THIS RUN (2026-07-10) COMPLETED LATE — MONDAY 2026-07-13 ~09:52 PT (weekend session suspension).** The market clock has already rolled to **7/13 (is_open true, next_open 2026-07-14)**. If a fresh **Monday 2026-07-13** news run has NOT already fired, it should — the 7/10 brief is now 1 session stale. Markets are open 7/13; the next trader run is post-close 7/13 ~4 PM PT.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Fri 2026-07-10, fired ~15:35 PT; completed Mon 7/13 due to suspension). **Constructive, contained, NOT halt-worthy.** Marquee = **SK Hynix's $26.5B Nasdaq debut** (largest-ever US IPO by a foreign company; priced $149, opened ~$170 / +14–17%; chairman "demand is enormous"). It's **rotating liquidity within the memory/semis cohort** — AI-proximity winners (NVDA, SK Hynix) vs **MU "already cracking."** Held **META** caught a *fresh EU DSA "addictive features" action* (fines up to 6% of revenue at risk, preliminary) but closed **up ~6%** on a leaked AI-hardware capex memo. **AAPL sued OpenAI** (trade-secret theft, new). **No FOMC, no >2% geopolitical gap → not halt-worthy.**
- **UNIVERSE GREW 31 → 32 under Tier-0.** Promoted **SKHY (SK Hynix, technology)** on its 7/10 debut per the standing directive. **Promoted the PERMANENT ticker SKHY** (regular-way from Mon 7/13) — NOT the Friday-only when-issued line **SKHYV** (~$168–170, now frozen). **CONFIRMED: SKHY quotes live on Alpaca as of the 7/13 open** (mid ~$156.5, bid/ask 151/162, thin). It lands **UNCLAIMED** → trader mandatory-attach triage. Backtest history is minimal (1 session), so expect a no/low-history provisional/quarantined outcome initially.
- **Held book:** universe `by_source` still shows **positions = META only** (7/9 reconciliation stands — AVGO/MU/ORCL closed). No reconcile for the news agent.
- **Interpreter:** bare `python3` STILL BROKEN (Homebrew 3.14.5, no deps). Entire run used the venv. **Use `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` from repo root before EVERY CLI call.**
- **Pre-promotion state:** `list-active` → universe 31, claimed 31, **unclaimed 0**, **provisional 4 (QCOM, SPCX, SYNA `revalidate_by 2026-07-21`; WULF `revalidate_by 2026-07-23`)**. `gap-registry coverage_holes` **empty** (confirmed again). Post-promotion universe = 32 (SKHY unclaimed).
- **Alpaca density: 109 items** (vs 168 on 7/9). META 14, MU 12, NVDA 11, SPCX 10, MSFT 7, TSLA 7, AMZN 6, GOOGL/INTC/SPY 5, AAPL/AVGO/TSM 4, QQQ/SNDK 3, BE/ORCL/RKLB 2, ARM/DELL/WULF 1; CBRS/CSCO/HPE/IRDM/JPM/MRVL/NUVL/QCOM/SYNA 0. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline:** header dated 2026-07-10 (with a run-timing note flagging the Mon-7/13 completion). Prior: 7/9 fresh, 7/8 fresh, 7/7 fresh.

## Notable carry-forwards

- **SKHY (SK Hynix) — PROMOTED 7/10; regular-way live 7/13.** Debut STRONG (not "wonky"): +14–17% over the $149 offer, $26.5B, largest-ever foreign US IPO. Joins the **Nasdaq Composite Monday 7/13**. **Next-run checks:** (1) confirm the trader triaged SKHY (unclaimed → claimed/provisional); (2) track whether SKHY holds its debut level or fades (7/13 early book was thin, mid ~$156.5 < Friday's when-issued ~$168.6); (3) verify SKHYV (temp line) is retired and only SKHY persists — flag if SKHYV lingers as a phantom.
- **MEMORY COHORT — the live story is now IPO liquidity-drain + reshoring.** (1) SK Hynix's $26.5B listing draining AI-trade capital → **MU pressured**; (2) Commerce Sec. **Lutnick** pressuring Samsung/SK Hynix to build US fabs (MU-aligned reshoring); (3) MU $250B (carry). Sustain-check: does the MU-vs-SKHY "AI-proximity split" persist or reconverge?
- **META (held) — EU DSA "addictive features" action (NEW regulatory).** Preliminary "may breach," fines up to 6% of revenue at risk. Plus leaked multi-year AI-hardware capex memo + Muse Spark 1.1 + in-house "Iris" chip. Watch whether the EU finding hardens into a formal charge/fine. Rides its MACD rule.
- **AAPL — sued OpenAI for trade-secret theft (NEW litigation).** Watch for OpenAI response / escalation.
- **GOOGL — report: US AI models (OpenAI/Google) reached Pentagon-blacklisted Chinese firms via overseas subsidiaries (NEW, export-control).** Watch for any policy/agency follow-up.
- **INTC — JPMorgan named it a highest-conviction Q3 short** (after doubling YTD); Q2 earnings 7/23. Track whether the short thesis draws follow-on flow.
- **JPM — Q2 earnings Tue 7/14 (most urgent), window OPEN.** Same day as June CPI + Warsh testimony. $50B buyback effective 7/1. Earnings-window assignment gap.
- **Earnings run: JPM 7/14, TSLA 7/22, ARM 7/23, INTC 7/23, AMZN 7/30.** Event-IV building.
- **SPCX (PROVISIONAL/quarantined) — no new hard event.** SpaceX IPO aftermath (Musk "first trillionaire"), China's first reusable-booster landing (competitive), Starlink 10Gbps, FSPC + Ex-Elon ETFs (forced-flow). Stays non-tradable. FCC 100k-sat vote 7/22 carry.
- **RKLB — added to First Trust FSPC Space Economy ETF** (inclusion/forced-flow, mild). Iridium M&A follow-through quiet.
- **BE — Hunterbrook short-report pushback continues** (management defending supply-chain credibility). Thesis unresolved.
- **WULF — NO fresh event 7/10** (only a crypto-cohort roundup). Stays provisional/quarantined (`revalidate_by 2026-07-23`). Watch for Anthropic-lease / Abernathy-JV follow-through.
- **Vol regime — VIX ~15.84 (benign, contango).** Event-IV into the 7/14 cluster + 7/22–30 earnings run. Single-name tech dispersion elevated (carry).
- **Macro — no print 7/10; 7/14 is the pivot:** June CPI (headline ~3.9%, core ~2.9% forecast) + Warsh testimony (House Tue/Senate Wed) + PPI Wed + JPM earnings. Last inflation read before 7/28–29 FOMC. Funds 3.50–3.75%.

## To do on the next run

1. **CONFIRM the schedule.** This 7/10 run completed Monday 7/13 (suspension). Verify a fresh **7/13** run fires (or that this is it, re-based) so the trader doesn't act on a stale Friday brief. If it's already 7/13+, run the standard workflow for the CURRENT date and re-fetch.
2. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` from repo root** for EVERY CLI call. **Re-read `news_manual.md §9` every run** (Tier 0 = promote every US-tradable news-subject on first appearance, uncapped; Tier A recurrence = prioritization hint; Tier B still applies; all require `--sector`).
3. **SKHY follow-through** — confirm trader claim status (unclaimed → provisional/claimed), confirm SKHY (not SKHYV) is the live symbol, track debut hold-vs-fade. Note SKHYV should retire.
4. **Memory cohort** — MU-vs-SKHY AI-proximity split; Lutnick reshoring; WDC/SNDK/ARM read-through; MU $250B follow-through.
5. **META (held)** — does the EU DSA finding harden? Any capex-memo detail. Rides MACD.
6. **7/14 cluster** — June CPI + Warsh testimony + JPM earnings all Tuesday. Log the CPI print vs ~3.9%/2.9% forecast; event-IV.
7. **Confirm universe = 32 / provisional 4 (QCOM, SPCX, SYNA, WULF)** + SKHY claim status.
8. **Vol regime** — VIX vs ~15.84; event-IV into 7/14 + earnings run. Log concrete single-name UOA on universe names only (today's whale-alerts were scan rollups).
9. **Outlier movers + sector breakdown.** Per-name reconstruction from Alpaca remains the workable path. Today's clean promote (SKHY) done; tracked WDC/AMD/Samsung/DAL/CRCL (no clean US-tradable single-name hard catalyst).
10. **Library gaps re-listing** (see brief): regulatory/litigation (META EU DSA NEW, AAPL v OpenAI NEW, GOOGL export-control NEW); sector liquidity-rotation/IPO-drain (SK Hynix→MU, NEW); index-inclusion/forced-flow (SKHY→Nasdaq Comp, Ex-Elon + FSPC ETFs, SPCX; NEW_CATEGORY_NEEDED); earnings-window assignment (JPM/TSLA/ARM/INTC/AMZN); capex-window (MU $250B, META 14GW); activist-short (BE); vol-regime activation; new-listing no-history triage (SKHY). Sat research = next.

## Open questions for the operator

- **[HIGH — NEW/acute] News run completed 3 days late (weekend session suspension).** The 7/10 run fired at the correct Fri 15:35 PT slot but only finished Mon 7/13 ~09:52 PT. This is the schedule-stability + brief-staleness risk manifesting concretely: a 7/13 trader could read a 7/10-dated brief. Asks: (a) stabilize the scheduler / add a heartbeat that a run finished same-day; (b) implement the `_load_news_brief()` staleness guard (parses date_in_file but never compares to today — a >1-session-old brief should be rejected/down-weighted).
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Repoint the launcher + prompt to the venv (or pip-install requirements into 3.14). Bash cwd drifts — always run from repo root.
- **[MEDIUM] Trader off-schedule / double-fire (7/7, 7/8).** Confirmed recurring on order-submitting days. Fix the single-trigger config before a double-fire lands where the 2nd run could act twice.
- **[MEDIUM] Fallback-threshold question (carry, now with SKHY).** A no-price-history / 0-trade backtest attaches a below-baseline *trading* provisional rather than routing to `equity_watch_only` (bit SMCI/RKLB/IRDM/BE 7/8, WULF 7/9). SKHY is the next test case (minimal history on debut). Should a degenerate/empty backtest count as "rankable" or "no signal → watch_only"?
- **New-listing ticker lifecycle (NEW).** SK Hynix used a temporary when-issued ticker **SKHYV** (Fri 7/10 only) then the permanent **SKHY** (regular-way from 7/13). We promoted SKHY (correct — it persists). Generalize: when a promotable IPO/ADR lists, promote the PERMANENT regular-way ticker, not the when-issued line. Verify SKHYV is retired and doesn't linger as a phantom quote.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX; SK Hynix→Nasdaq Comp 7/13; Ex-Elon + FSPC ETFs).** Forced-flow gap keeps recurring.
- **Earnings-window assignment — JPM (7/14, most urgent), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** Earnings-window responders don't claim these. Sat: assign.
- **New event-window sub-triggers (recurring) — regulatory/litigation (META EU DSA, AAPL v OpenAI, GOOGL export-control, all NEW), capital-allocation/capex (MU $250B, META 14GW), activist-short (BE), product/vendor (MSFT in-house AI carry).** No rule reads any of these.
- **M&A-arb activation — RKLB (acquirer)/IRDM (target) + SYNA/onsemi.** `equity_pairs_trading_cointegration` claims only SYNA. Sat: activate merger-arb.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists. (Not re-checked — news agent doesn't pull broker state.)
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate in `.git-sync-queue/`.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **109 items** cleanly (via venv). Zeros: CBRS/CSCO/HPE/IRDM/JPM/MRVL/NUVL/QCOM/SYNA.
- `cli market-status` at run start → `is_open false`, `now 2026-07-10T15:35 PT`, `next_open 2026-07-13T09:30 ET`. At completion (post-suspension) → `is_open true`, `now 2026-07-13T09:52 PT`, `next_open 2026-07-14T09:30 ET`.
- `cli list-active` (pre-promotion) → universe 31, claimed 31, unclaimed 0, provisional 4 (QCOM/SPCX/SYNA/WULF). `gap-registry coverage_holes` empty. Post-promotion universe 32 (SKHY unclaimed).
- **SK Hynix ticker resolution (IMPORTANT):** SKHY (permanent, regular-way from 7/13) vs SKHYV (temporary when-issued, Fri only). At Fri run: SKHY = "no quote available", SKHYV = live ($168.6 mid). At Mon 7/13 completion: SKHY = live ($156.5 mid), SKHYV = frozen ($168.6). **Promoted SKHY — validated correct.**
- WebSearch strong Fri: SK Hynix $26.5B Nasdaq debut priced $149, opened ~$170 / +17% indicated (Bloomberg/CNBC/Yahoo/Motley Fool); VIX ~15.84 (−6.3%); June CPI 7/14 forecast headline ~3.9% / core ~2.9% + Warsh testimony (ActionForex/Kiplinger); Trump aircraft-tariff deferral; Lutnick US-fab pressure; Meta EU DSA fine risk; Apple v OpenAI lawsuit.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier 0 (news-subject inclusion, uncapped):** Promoted **SKHY** (own marquee coverage + US-listed as of 7/10 + standing directive). Foreign/not-US-tradable subjects (Samsung, Kioxia, Blue Origin) tracked. Sympathy/price-only (WDC, AMD) dropped from promotion. CRCL/cryptobank outside equity universe → tracked.
  - **Tier B:** SKHY is also index-inclusion-adjacent (joins Nasdaq Composite) but that's not one of the 5 codified triggers; promotion rests on Tier-0 + the standing directive. No other candidate met a Tier-B trigger.
  - **Decision: 1 promotion (SKHY, Tier-0 + directive). Universe 31 → 32.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
