# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**NEXT RUN IS TUESDAY 2026-07-07, 3:30 PM PT** (30 min before the trader run). Markets OPEN Tue 7/7 (`market-status` → `next_open 2026-07-07T09:30 ET`). **SPCX joins the Nasdaq-100 at Tuesday's open** — the add happens on the day of the next run.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Mon 2026-07-06, canonical post-close 3:30 PM PT run; first full session after the July 4 holiday weekend). Risk-on tape (Dow record >53,000 — price, dropped) over a real event cluster: **Micron-Ford long-term memory-supply SCA** (+ Micron-GM; Manassas VA DRAM capex); **Broadcom-Apple chip deal extended to 2031** (AVGO up); **MSFT cutting 4,800 jobs** (Xbox restructuring); **NVDA Kyber NVL144 roadmap DELAY** (MRVL benefits); **INTC raised chip prices up to $50** (after Apple). Plus a hard calendar: **SPCX → Nasdaq-100 Tue 7/7**, Samsung Q2 prelim 7/7, SK Hynix Nasdaq listing 7/10, JPM earnings 7/14 (window open). **0 promotions. Universe stays 26.** **NOT HALT-WORTHY:** no FOMC; the two held-name deals are positive; US-Iran risk-positive (weekend "great progress," Hormuz reopening); no >2% futures shock.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used the venv. **IMPORTANT: `cd` to the repo root (or use the absolute path) before EVERY CLI call — the shell cwd drifts between calls.** Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`. Operator action still required (open questions).
- **Universe: 26, unchanged.** `list-active` → universe 26, claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**. `gap-registry coverage_holes` = **empty** (confirmed again).
- **SPCX PROVISIONAL DEADLINE LAPSED.** SPCX `revalidate_by 2026-07-04` is now **past** and SPCX is **still PROVISIONAL / execution-quarantined** — Saturday research did NOT clear it. It joins the Nasdaq-100 Tue 7/7 but stays **non-tradable** until validated. QCOM/SYNA `revalidate_by 2026-07-10`.
- **Alpaca density: 144 items.** NVDA 16, TSLA 15, MU 14, SPCX 14, AAPL 13, GOOGL 9, MSFT 9, AVGO 7, SPY 6, AMZN 5, DELL 5, META 5, INTC 4, QQQ 4, SNDK 4, MRVL 3, TSM 3, ARM 2, JPM 2, ORCL 2, QCOM 2; CBRS/CSCO/HPE/NUVL/SYNA 0. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline FRESH today** (dated 2026-07-06). Prior: 7/3 holiday brief FRESH, 7/2/7/1/6/30 fresh; earlier misses 6/22, 6/25, 6/29. Staleness-guard ask still stands (open questions).

## Notable carry-forwards

- **MU (held) — Micron-Ford long-term memory-supply SCA (NEW), + Micron-GM (days prior).** Automotive-memory customer win + Manassas VA DRAM capex; one of 16 SCAs from the fiscal-Q3 call. event_catalyst; no true responder (event-driven claim quarantined, models earnings only). **MU trailing stop still NOT fired as of 7/3 handoff** after the +17.4%→~flat round-trip — watch the give-back/stop scenario. Post-print IV crush continues.
- **AVGO (held) — Broadcom-Apple chip deal extended to 2031 (NEW).** Multi-year partnership/customer-win extension; AVGO up. event_catalyst; event-driven claim quarantined → no responder.
- **AAPL — Broadcom-2031 partnership (positive) + DST-tariff overhang + foldable-iPhone slip past iPhone 18 (Kuo, minor).** Price-claimed (trend-following); regulatory/partnership events have no responder.
- **NVDA — Kyber NVL144 roadmap DELAY (NEW product-slip).** Opens a competitive window for alt AI-hardware suppliers (MRVL beneficiary). Nemotron full-stack push (softer); Burry short-thesis rebuttal (carry). No responder.
- **MRVL — surging on the NVDA Kyber delay competitive window (NEW read-through)** + BofA "bear trap / $1.5T buildout" list. Claimed by breakout-volume (may catch momentum if volume-confirmed); the event itself has no responder.
- **MSFT — 4,800 job cuts / Xbox restructuring (NEW).** Restructuring event; claimed by MACD-momentum (trending) → no restructuring responder. Recurring big-tech class with ORCL.
- **INTC — raised chip prices up to $50 (NEW pricing/margin event)** after Apple; **Q2 earnings July 23** (enters 14-day window ~7/9). Pricing-power + earnings-window, both no responder (breakout-volume claims INTC).
- **SPCX (PROVISIONAL/quarantined) — Nasdaq-100 add TUE 7/7 (~$4.3B forced buying); Monday was the last read before the add.** "30% rule" could unlock ~456M shares after earnings if it holds >$175.50 before Aug 3 (supply overhang). FCC vote 7/22. revalidate_by 7/04 LAPSED, still quarantined → **will not trade** into the add. Track the price path Tue.
- **GOOGL — DST-tariff overhang + UK under-16 social-media ban pushback (NEW policy), + EU €4.1B (carry).** Regulatory cluster; no responder. Track DOJ search-remedy / EU DMA read-through.
- **META (held; BUY 16 live, avg $605.28) — DST-tariff + UK child-safety overhang; AI-cloud thesis carry.** Position rides its own MACD exit; the news is responder:NONE. Track cloud capex confirmation + addiction-trial calendar.
- **JPM — Q2 earnings Tue 7/14 (~$5.44/sh, +9.7% YoY), window NOW OPEN.** Kicks off bank season. $50B buyback consummated 7/1. Earnings-window responder does NOT claim JPM (trend-following does) → assignment gap. Most urgent.
- **TSLA — no fresh hard event; binary is the 7/22 earnings call** (margins the focus). Delivery-beat digestion; Cybercab accessibility + Leapmotor Mexico (minor). Earnings-window assignment gap. IV builds.
- **DELL — up on Trump "buy a Dell" endorsement (NEW soft catalyst)** + Michael Dell $6.25B Trump-Accounts pledge. Endorsement not modeled.
- **Memory cohort (MU, SNDK, WDC/STX) + Samsung 7/7 + SK Hynix 7/10.** Samsung record-profit print tomorrow; SK Hynix lists as SKHY (~$166) Friday. Micron-Ford/GM add an automotive-demand leg. Sustain check + AAPL/INTC price-hike read-through.
- **AI-capex / fund-flow theme.** Record $14.3B weekly tech-fund inflow (2nd-biggest ever) vs broad-equity outflows; BofA "bear trap." Recurring; no responder.
- **Macro/policy:** June NFP +57k dovish miss (carry); Fed on hold; DST-tariff threat (resurfaced, originated 6/26); UK under-16 ban; US-MX-CA trade-deal review (carry). Next macro: July CPI/PPI into late-July FOMC.
- **Vol regime — VIX ~15.8 (sub-16, down from ~16.6 on 7/2), normal contango, no inversion.** Index vol benign; dispersion single-name (SPCX 7/7, JPM 7/14, TSLA 7/22, MU IV crush).

## To do on the next run (Tue 2026-07-07)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A (3 consecutive catalyst sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require `--sector`.
2. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` AND `cd` TO THE REPO ROOT** for EVERY CLI call. Bare `python3` fails; the cwd drifts between Bash calls.
3. **Universe should confirm 26.** Check unclaimed 0 / provisional 3 (QCOM, SPCX, SYNA). **Re-check SPCX** — revalidate_by 7/04 lapsed; see if Saturday research finally cleared it (still quarantined as of Mon 7/6). **SPCX joins the Nasdaq-100 at Tue's open** — cover the price path + any index-methodology news; note it still can't trade if quarantined.
4. **Samsung Q2 prelim (7/7) + SK Hynix listing (7/10)** — memory read-through to MU/SNDK; SKHY becomes a promotable universe candidate once it trades (Friday).
5. **JPM Q2 earnings Tue 7/14** — inside the 14-day window; flag IV build; assignment gap (trend-following claims, not event-driven).
6. **TSLA into 7/22 earnings** — track IV build; assignment gap.
7. **MU (held) — reconcile any trailing-stop/rule-driven trim** after the round-trip; Micron-Ford/GM demand leg. **AVGO — Broadcom-Apple 2031** follow-through.
8. **NVDA Kyber delay follow-through / MRVL competitive window** — track whether the roadmap-slip theme sustains.
9. **MSFT restructuring** (4,800 cuts) + **INTC price hikes** — restructuring + pricing/margin themes; both no responder.
10. **Regulatory cluster** — DST-tariff, UK under-16 ban, GOOGL EU/DOJ — any escalation from threat to action.
11. **Vol regime** — VIX vs ~15-16; whether index vol stays benign; event-IV (SPCX 7/7, JPM 7/14, TSLA 7/22); MU IV crush.
12. **Promote candidates if Tuesday refreshes:**
    - **RIVN** — session ~2, DELIVERY beat-and-raise (not earnings → no Tier-B #3). Consumer-discretionary. Promote on its own *earnings* beat-and-raise+5% or a clean 3-session catalyst run. Today merely restated the 7/2 print (clock did not truly advance).
    - **SK Hynix (SKHY)** — post-IPO add candidate once it trades (~7/10); not promotable until it has a US ticker. Memory cohort (technology).
    - **CRDO** — AI-interconnect; absent again (clock not advanced). Promote on a fresh same-week 3-bank initiation cluster OR own beat-and-raise+5%.
    - **WDC / STX** — memory cohort, flow only. Tier-A/B only.
    - **CRWV / NBIS** — neoclouds; sympathy to the cloud build-out; watch.
    - **Samsung** — foreign-listed (SSNLF OTC); not addable; memory read-through only.
13. **Outlier movers + sector breakdown.** Generic gainers/losers query STILL screen-level (~24 consecutive sessions; today's top gainer CLRO +109% had no identifiable catalyst) — per-name reconstruction remains the workable path. Today's clean non-universe catalysts were thin (RIVN restated delivery beat).
14. **Library gaps re-listing.** Carry (see brief): customer/supply-agreement event window (MU/AVGO, NEW); product/roadmap-slip (NVDA/MRVL, NEW); restructuring (MSFT NEW + ORCL); pricing/margin (INTC NEW + AAPL); regulatory/antitrust (DST-tariff, UK ban, GOOGL EU); index-inclusion/forced-flow (SPCX 7/7, SK Hynix 7/10; NEW_CATEGORY_NEEDED); earnings/delivery-window assignment (JPM 7/14, TSLA 7/22, INTC 7/23, CBRS); M&A-arb (SYNA/onsemi); capital-allocation (JPM buyback, MU Trump-Accounts); vol-regime activation (MU IV crush). Sat research = next.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Earlier misses span 6/22, 6/25, 6/29; 6/30-7/6 fresh (incl. the 7/3 holiday brief). Asks stand: (a) stabilize the schedule / add a health-check alert on miss-or-double; (b) the `_load_news_brief()` staleness guard — a stale brief should be rejected/down-weighted, not fed as live signal (parses date_in_file but never compares to today).
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install requirements into 3.14 / rebuild the venv), and pin python@3.13. **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Also: **the Bash shell cwd drifts between calls** — always `cd` to the repo root or use the absolute venv path.
- **[MEDIUM] Trader scheduled task fired on the 7/3 market holiday** (ran clean as assess-and-stop). Ideally short-circuit on `is_open:false` before broker snapshots, or confirm the M-F schedule is intended to fire on NYSE holidays.
- **SPCX provisional past its 7/04 deadline and joining the Nasdaq-100 (7/7) while still quarantined.** Saturday research did not clear it. Operator: decide whether an index-add forced-flow name warrants an expedited validation path, or accept it stays non-tradable through the add.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX 7/7; SK Hynix ~7/10).** The forced-flow gap keeps recurring; argues for a 6th trigger or a forced-flow overlay.
- **Earnings/delivery-window assignment — JPM (7/14, window open, most urgent), TSLA (7/22), INTC (7/23), CBRS (carry).** Earnings-window responder does not claim these (all trend-following). Sat: assign.
- **Customer/supply-agreement + product-roadmap-slip sub-triggers (NEW) — MU/AVGO (SCAs/partnership) + NVDA/MRVL (Kyber delay).** No rule reads a strategic customer agreement, a multi-year partnership extension, or a product-roadmap slip. Multi-name, recurring.
- **Regulatory/antitrust event window — live cluster (DST-tariff, UK under-16 ban, GOOGL EU €4.1B, META India/addiction, MU DRAM).** No rule reads a court/agency/trade action.
- **Restructuring/workforce-reduction event window — MSFT (4,800, NEW) + ORCL (carry).** Recurring big-tech class; no responder.
- **Pricing/margin-disclosure sub-trigger — INTC (NEW) + AAPL (carry).** No rule reads a pricing-power / input-cost event.
- **M&A-arb activation, live universe instance (SYNA / onsemi).** `equity_pairs_trading_cointegration` declares pairs_arbitrage but only provisionally claims SYNA. Sat: activate merger-arb (long SYNA / short ON at 1.350).
- **Capital-allocation / capital-return event window (JPM $50B buyback; MU Trump-Accounts).** No rule reads a buyback/return disclosure.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Three provisional claims live (QCOM, SPCX, SYNA); SPCX's checkpoint lapsed.
- **CBRS earnings-window assignment.** CBRS claimed only by price-driven trend-following. Sat: head-to-head vs `equity_event_driven_catalyst`.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** Errors `'dict' object has no attribute 'id'` when a live open order exists; clean when none. Fix the order-serialization path.
- **git-sync LaunchAgent.** Only the Jun-1 test files (`marker_test.json`, `test.txt`) sit in `.git-sync-queue/` — no real pile-up, LaunchAgent processing normally. Verify `launchctl list | grep harness` if markers accumulate.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **144 items** cleanly (via venv). CBRS/CSCO/HPE/NUVL/SYNA 0.
- `cli market-status` → `is_open: false`, **`next_open_iso: 2026-07-07T09:30:00-04:00`**, `now_iso: 2026-07-06T15:39 PT` (post-close run; today's session already closed).
- `cli list-active` → universe 26, claimed 26, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA). `gap-registry coverage_holes` empty.
- WebSearch strong Mon: Dow 53,055.91 record close / S&P 7,537.43 / Nasdaq 26,121.16 (TheStreet/Motley Fool); VIX ~15.8 (Cboe/Yahoo); Micron-Ford SCA + Manassas VA DRAM (GlobeNewswire/StockTitan/Benzinga); JPM Q2 7/14 ~$5.44/sh (JPMorgan IR/StockTitan); Samsung Q2 prelim 7/7 + SK Hynix SKHY listing 7/10 ~$166 (Korea Herald/Bloomingbit); US-Iran weekend "great progress"/Hormuz reopening (CNBC/Al Jazeera); DST-tariff threat originated 6/26 (CNBC/CBS).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (CLRO +109% no catalyst); RIVN search restated the 7/2 delivery print (no fresh catalyst).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No candidate reached a clean 3-consecutive-catalyst run (RIVN ~session 2 but today restated 7/2's delivery print; CRDO absent; WDC/STX/CRWV/NBIS sympathy). **No Tier-A promotion.**
  - **Tier B:** No qualifier — no NEW confirmed M&A target (SYNA already in), no FDA binary, no *earnings* beat-and-raise+5% on a universe/candidate name (RIVN's is a DELIVERY beat-and-raise), no *fresh* same-week 3-bank initiation cluster, no candidate Tier-1 customer-win press release (Micron-Ford/Broadcom-Apple are universe names). **No Tier-B promotion.**
  - **Decision: 0 promotions. Universe stays 26.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
