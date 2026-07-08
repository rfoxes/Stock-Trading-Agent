# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**NEXT RUN IS THURSDAY 2026-07-09, 3:30 PM PT** (30 min before the trader run). Markets OPEN Thu 7/9 (`market-status` → `next_open 2026-07-09T09:30 ET`). **SK Hynix $29B Nasdaq ADR listing FRIDAY 7/10** — promote it once it has a live US ticker.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Wed 2026-07-08, canonical post-close ~3:40 PM PT run). A **rich two-sided day**: marquee positive = **Apple's $30B+ Broadcom chip deal through 2031** (lifted held **AVGO**); **Samsung ~$59B op-profit guide** confirmed the memory up-cycle (+ NVDA Vera Rubin SSD). Risk-off overlay: **Trump declared the Iran ceasefire "over"** (Brent +5.43%/$78.19), **hawkish June FOMC minutes** (9 hike / 8 hold / 1 cut; median 2026 rate up to ~3.8%; Warsh abstained from the dot), **EU DMA App Store loss for Apple** (gatekeeper read-through GOOGL/META), **China CXMT memory threat** (Citi + Apple testing). **NOT halt-worthy:** no FOMC decision (minutes only); no adverse held-name shock (AVGO positive, META regulatory overhang, MU competitor read-through, ORCL no event); equities did NOT gap >2% (S&P −0.28%, Nasdaq +0.2%, Dow −1.09%) — oil moved, equities didn't.
- **UNIVERSE GREW 26 → 30 under the NEW Tier-0 directive.** Promoted **SMCI** (edge-AI appliance launch, technology), **RKLB** ($8B Iridium M&A, industrials), **IRDM** (confirmed M&A target $54/sh, communication_services), **BE** (Hunterbrook short report, industrials). All 4 are **UNCLAIMED** → trader mandatory-attach triage assigns each `equity_watch_only` or a validated strategy. **This is the first Tier-0 run** (7/7 was still the old recurrence-gate regime).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used the venv. **Use `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` and run from the repo root before EVERY CLI call** — the shell cwd drifts between Bash calls. Operator action still required (open questions).
- **Pre-promotion state:** `list-active` → universe 26, claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**, all `revalidate_by 2026-07-21`. `gap-registry coverage_holes` = **empty** (confirmed again). Post-promotion universe = 30 (SMCI/RKLB/IRDM/BE unclaimed until trader triage).
- **Broker snapshot:** NOT re-pulled this run (news agent doesn't reconcile). The 7/7 09:09 "wipe" self-restored per the 7/7 handoff; positions were AVGO 26 / META 16 / MU 7 / ORCL 38, equity ~$103.1k. **The 7/8 handoff says the next `cli execute` will SELL AVGO (time) / MU (time) / ORCL (hard)** via the newly-fixed `equity_event_driven_catalyst` stops — expected, not an anomaly. Trader owns this.
- **Alpaca density: 106 items.** NVDA 14, SPCX 11, MU 9, TSLA 9, AAPL 9, META 8, MSFT 7, QQQ 6, SPY 6, GOOGL 5, SNDK 4, AMZN 3, AVGO 3, DELL 3, INTC 3, ORCL 3, JPM 2, CBRS 1; ARM/CSCO/HPE/MRVL/NUVL/QCOM/SYNA/TSM 0. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline FRESH today** (dated 2026-07-08). Prior: 7/7 fresh, 7/6 fresh, 7/3 holiday fresh; earlier misses 6/22, 6/25, 6/29. Staleness-guard ask still stands (open questions).

## Notable carry-forwards

- **AVGO (held) — Apple $30B+ Broadcom deal through 2031 (NEW, positive).** Custom ASIC + wireless (FBAR filters), >15B US-made chips, $1.5B Fort Collins capex, inside Apple's $600B US pledge. Fresh anchor-customer catalyst; no responder. Note the tension with the pending event_driven_catalyst time-stop exit (trader's call).
- **MEMORY COHORT — still the live story, now 3-sided.** (1) Samsung $59B guide confirms the up-cycle (bullish); (2) NEW China **CXMT** threat (Citi; Apple testing CXMT) = competitive risk to MU/SNDK/WDC; (3) **SK Hynix $29B Nasdaq listing 7/10** = funding rotation. MU (held) rides its rule. Sustain-check: does CXMT/China-threat framing build?
- **AAPL — triple event: $30B Broadcom deal + EU DMA App Store loss + testing China CXMT memory.** Regulatory (DMA) is a concrete action, gatekeeper read-through to GOOGL/META. No responder.
- **NVDA — Samsung mass-producing PCIe 6.0 SSD for NVDA Vera Rubin (NEW, supply/partnership).** Strengthens NVDA AI-memory stack. No responder.
- **META (held) — EU DMA gatekeeper read-through (NEW regulatory overhang).** Muse Image carry. Position rides MACD rule.
- **SPCX (PROVISIONAL/quarantined) — FCC filing for 100,000 Gen3 Starlink satellites (NEW) + Nasdaq-100 ETF passive inclusion + Starlink Aviation price doubling.** Real regulatory/forced-flow, but stays non-tradable. FCC vote 7/22 carry.
- **RKLB / IRDM (NEW to universe) — $8B Rocket Lab–Iridium deal ($54/sh, closes ~mid-2027).** IRDM = live merger-arb target; RKLB = space-consolidation leader. Both unclaimed; watch attach pending.
- **SMCI (NEW to universe) — edge-AI Kubernetes appliance launch (Red Hat/Everpure), surging.** AI-server cohort. Unclaimed; watch pending.
- **BE (NEW to universe) — Hunterbrook short report (Chinese scandium supply).** AI-datacenter power. Unclaimed; watch pending. Track whether the short thesis develops.
- **JPM — Q2 earnings Tue 7/14, window OPEN, most urgent.** Est ~$5.61/sh, $49.56B rev; $50B buyback effective 7/1. Earnings-window responder doesn't claim JPM (trend-following does) → assignment gap.
- **INTC 7/23, TSLA 7/22, AMZN 7/30 earnings** — IV builds; earnings-window assignment gap (all trend-following).
- **MSFT — OpenAI GPT-Live voice models (NEW, minor partner event).** No responder.
- **Regulatory cluster (carry + NEW) — EU DMA App Store ruling (NEW concrete action), SEC quarterly-reporting shake-up, DST-tariff/UK under-16/Meta addiction litigation.** No responder.
- **Vol regime — VIX ~16.13 (+4.77%), oil-bid but sub-regime; normal contango.** Vol in single-name event-IV (JPM/TSLA/INTC/AMZN, SK-Hynix-listing) + the oil tail from Iran.
- **Macro/geopolitics — Iran ceasefire "over" (Brent +5.43%/$78.19; equities contained); hawkish June FOMC minutes 7/8; June NFP +57k dovish (carry); CPI/PPI/PCE later in July into late-July FOMC.**

## To do on the next run (Thu 2026-07-09)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** **Tier 0 (promote EVERY US-tradable news-subject on first appearance — uncapped; watch attach makes it harmless)** is now the primary inclusion rule; Tier A (recurrence) is a prioritization hint; Tier B still applies. All require `--sector` (allowed: communication_services, consumer_discretionary, consumer_staples, crypto, energy, financials, healthcare, index, industrials, materials, real_estate, technology, utilities).
2. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` AND run from the repo root** for EVERY CLI call.
3. **SK Hynix listing FRIDAY 7/10** — once it has a live US ADR ticker, **promote it** (Tier-0 news-subject; memory cohort, technology). Not addable until it trades. Watch for the ticker symbol Thu/Fri.
4. **Iran follow-through** — did the oil spike / US-Iran escalation widen overnight? Check the 7/9 equity-futures gap and whether VIX repriced. Most likely item to shift the halt-worthy call if it escalates.
5. **Fed-minutes digestion** — any rate-path repricing after the hawkish June minutes (median 2026 up to 3.8%). Watch Treasury yields / rate-sensitive tone. Not halt-worthy on its own.
6. **Confirm universe = 30 / provisional 3 (QCOM, SPCX, SYNA).** Check whether the trader's triage attached watch_only (or a validated strategy) to SMCI/RKLB/IRDM/BE, and whether they moved from unclaimed → claimed.
7. **Memory sustain-check** — does the China CXMT threat build? Samsung/SK-Hynix cohort. MU (held) / SNDK / MRVL / INTC / ARM.
8. **AVGO $30B Broadcom deal follow-through** (any AVGO reaction / analyst notes). **NVDA Vera Rubin SSD** supply follow-through. **EU DMA ruling** fallout (Apple appeal? GOOGL/META read-through).
9. **New-symbol news follow-through** — SMCI (product adoption), RKLB/IRDM (deal-spread / regulatory), BE (short-report rebuttal or escalation).
10. **Vol regime** — VIX vs ~16; index vol vs the oil tail; event-IV into JPM 7/14. Log concrete UOA on universe names only (today's whale-alerts were scan rollups, no clean single strike).
11. **Outlier movers + sector breakdown.** Generic gainers/losers query STILL screen-level (~26 consecutive sessions; today returned Indian markets) — per-name reconstruction from Alpaca remains the workable path. Today's clean non-universe catalysts (SMCI/RKLB/IRDM/BE) were promoted; foreign names (Samsung/SK Hynix/CXMT/Momenta) tracked.
12. **Promotion watch for Thu/Fri:**
    - **SK Hynix (ticker TBD)** — promote on its US listing (~7/10); memory cohort (technology).
    - **Samsung (SSNLF)** — foreign OTC gray-market; the memory driver but no clean US line. Track, don't promote (MU/SNDK/TSM carry it).
    - **CXMT** — China, pre-IPO. Not US-tradable. Track (competitive threat).
    - **NBIS / WULF** — neocloud/AI-infra; promote only on a hard catalyst (beat-and-raise+5%, 3-bank cluster, or M&A), not price framing.
    - **Momenta** — HK-listed. Track.
13. **Library gaps re-listing** (see brief): customer-win/capital-allocation (Apple↔AVGO/AAPL $30B, NEW); competitor-earnings/sector read-through (Samsung + CXMT); regulatory/antitrust (EU DMA NEW, SEC, short reports); index-inclusion/forced-flow (SPCX FCC + Nasdaq-100, SK Hynix; NEW_CATEGORY_NEEDED); M&A-arb (RKLB/IRDM NEW + SYNA/onsemi); earnings-window assignment (JPM 7/14, TSLA 7/22, INTC 7/23, AMZN 7/30); product-launch/competitive-threat (SMCI, OpenAI GPT-Live, NVDA Vera Rubin); vol-regime activation. Sat research = next.

## Open questions for the operator

- **[NEW — Tier-0 volume] First Tier-0 run promoted 4 names in one session (SMCI/RKLB/IRDM/BE).** This is the intended behavior (uncapped, watch-attach makes over-inclusion harmless), but flagging the pace so the operator can confirm the universe-growth rate is acceptable. Universe 26 → 30 in one run; could accelerate on rich M&A/product days.
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install requirements into 3.14). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Also: the Bash shell cwd drifts between calls — always run from the repo root.
- **[HIGH] News-agent schedule stability + brief-staleness guard.** Earlier misses 6/22, 6/25, 6/29; 6/30–7/8 fresh. Asks: (a) stabilize schedule / add a health-check alert on miss-or-double; (b) `_load_news_brief()` staleness guard — parses date_in_file but never compares to today; a stale brief should be rejected/down-weighted.
- **[MEDIUM] Trader off-schedule firing (7/7 09:09, 7/3 holiday).** Confirm the intended trigger; the trader executing mid-session on a stale brief is undesirable. This news run fired correctly (post-close ~3:40 PM PT).
- **Provisional claim-REASON prose drift (carry).** The 7/7 reset re-stamped trend-following/event-driven/pairs claim *reasons* to PROVISIONAL/QUARANTINED while only QCOM/SPCX/SYNA are actually quarantined (structured `provisional_claims`). Reconcile via re-triage, not a hand-edit.
- **SPCX past its (reset) 7/21 deadline path.** Joined the Nasdaq-100 while quarantined; now filed FCC 100k-satellite plan. Operator: expedited validation for an index-add forced-flow name, or accept it stays non-tradable?
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX 7/7-7/8; SK Hynix 7/10).** Forced-flow gap keeps recurring.
- **Earnings-window assignment — JPM (7/14, most urgent), TSLA (7/22), INTC (7/23), AMZN (7/30).** Earnings-window responder doesn't claim these (all trend-following). Sat: assign.
- **New event-window sub-triggers (recurring) — customer-win/capital-allocation (Apple↔AVGO $30B, NEW), competitor-earnings read-through (Samsung/CXMT), regulatory/antitrust (EU DMA NEW + SEC), product-launch/competitive-threat (SMCI/OpenAI/NVDA).** No rule reads any of these.
- **M&A-arb activation — RKLB/IRDM (NEW, $54/sh target) + SYNA/onsemi.** `equity_pairs_trading_cointegration` declares pairs_arbitrage but claims only SYNA. Sat: activate merger-arb on IRDM/SYNA.
- **Mandatory-attach for 4 new symbols (SMCI/RKLB/IRDM/BE)** — confirm the trader's triage assigns watch/validated; Sat research validates whether any deserves a trading strategy.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists; clean when none.
- **git-sync LaunchAgent.** Queue clean this run (only Jun-1 test files). Verify `launchctl list | grep harness` if markers ever accumulate.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **106 items** cleanly (via venv). ARM/CSCO/HPE/MRVL/NUVL/QCOM/SYNA/TSM 0.
- `cli market-status` → `is_open: false`, **`next_open_iso: 2026-07-09T09:30:00-04:00`**, `now_iso: 2026-07-08T15:39 PT` (canonical post-close run).
- `cli list-active` (pre-promotion) → universe 26, claimed 26, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA, all `revalidate_by 2026-07-21`). `gap-registry coverage_holes` empty. Post-promotion universe 30.
- WebSearch strong Wed: Apple $30B Broadcom deal through 2031 (Bloomberg/MacRumors/NBC/Yahoo); Fed June minutes hawkish — 9 hikes, median 3.8%, Warsh abstained (Reuters/TradingKey/TechTimes); Trump Iran ceasefire "over" — S&P −0.28%, Nasdaq +0.2%, Dow −1.09%, Brent +5.43%/$78.19 (Bloomberg/CNBC/TheStreet); VIX 16.13 +4.77% (Cboe/Yahoo); Samsung ~$59B op-profit guide + Vera Rubin SSD (Benzinga/Goldman); SK Hynix $29B Nasdaq ADR listing 7/10 (CNBC/Fortune/Bloomberg); Rocket Lab–Iridium $8B at $54/sh (SEC 8-K/evertiq/Motley Fool); EU DMA App Store ruling (Benzinga).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (returned Indian markets/Nifty 50). Per-name reconstruction from Alpaca is the workable path.
- **Promotion analysis (`news_manual.md §9` — FIRST Tier-0 run):**
  - **Tier 0 (news-subject inclusion, uncapped):** Promoted **SMCI** (product launch), **RKLB** (own $8B M&A), **IRDM** (confirmed M&A target), **BE** (short report). All 4 = own coverage line + hard catalyst + US-tradable + in-theme. Foreign/not-yet-tradable subjects (Samsung/SK Hynix/CXMT/Momenta) tracked, not promoted. Off-theme incidental (KRUS sushi, PEP/KO) dropped.
  - **Tier B:** IRDM also satisfies #1 (confirmed M&A target). No other candidate met a Tier-B trigger.
  - **Decision: 4 promotions (all Tier-0). Universe 26 → 30.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
