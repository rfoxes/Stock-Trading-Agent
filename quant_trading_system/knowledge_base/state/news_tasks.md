# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NORMAL FLOW (Fri 2026-06-26, canonical post-close 3:30 PM PT run).
  **The day's shape: an AI-chip "profit-taking" rout (Nasdaq's 5th straight down day; MU −5% /
  AVGO −4% / SNDK −5% premarket) — PRICE ACTION we drop — over a thinner layer of real events.**
  Genuine new events, mostly outside the held book: **onsemi (ON) → Synaptics (SYNA) $7B all-stock
  M&A** (confirmed target → promoted); **SK Hynix $29.4B Nasdaq IPO filing** (~July 10, memory-trade
  read-through); **MSFT Xbox price hike + memory-cost-doubling-by-2027** (input-cost event, mirrors
  AAPL Thu); **JPM leadership/succession shake-up**; **DELL Texas reincorporation**; **GOOGL AI-talent
  departures**; **SPCX broke below its $135 IPO price (−32% from peak)** on an IG bond sell-off +
  OpenAI-IPO-delay read-through. **1 promotion: SYNA (Tier-B #1, M&A target). Universe 25 → 26.**
  **NOT HALT-WORTHY:** no FOMC; no held-name overnight catalyst; oil/Iran risk-positive.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire run used
  `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3 -m quant_trading_system.cli`. Operator
  action still required (open questions). Always `cd` to repo root (or use the absolute venv path)
  before CLI calls.
- **Universe: GREW 25 → 26.** SYNA promoted today (technology, M&A target), **UNCLAIMED**. **Unclaimed
  now = 3: QCOM + SNDK (from Thu, still not triaged by the trader) + SYNA (today).** The prior 23 stay
  claimed. SPCX still **PROVISIONAL / execution-quarantined** (revalidate_by **2026-07-04**).
  `gap-registry coverage_holes` = **empty** (confirmed again).
- **Alpaca density: 128 items.** SPCX 18, MU 17, AAPL 15, MSFT 13, TSLA 10, NVDA 9, AMZN 8, GOOGL 6,
  META 6, INTC 4, JPM 3, AVGO 3, QQQ 3, SNDK 3, QCOM 2, CBRS 1, DELL 1, MRVL 1, ORCL 1, TSM 1;
  ARM/CSCO/HPE/NUVL 0. All 6 category HTMLs + daily summary written.
- **1 promotion Fri (cap respected):** SYNA = 1 single-event (Tier-B #1 M&A target, under the 2/day
  cap). No Tier-A qualifier reached a clean 3-consecutive-catalyst run.

## Notable carry-forwards

- **SYNA (NEW universe, UNCLAIMED) — onsemi $7B all-stock M&A target.** 1.350 ON/sh, 19% premium,
  definitive agreement + SEC 8-K/425 filed 6/25, close mid-2027. Price tracks ON at the ratio → live
  merger-arb instance (feeds the m_a_arbitrage activation gap; long SYNA / short ON). Trader P0 triage
  (`triage-symbol SYNA --gap-type pairs_arbitrage`). Track deal progress / any regulatory friction.
- **QCOM + SNDK (universe, STILL UNCLAIMED from Thu).** Trader had not run P0 triage on either by the
  6/25 handoff (handoff predates the promotions taking effect). Re-confirm whether the trader claims
  them this run; if still unclaimed, note it. QCOM: data-center pivot (Meta anchor). SNDK: memory cohort.
- **AAPL (held) — EMA-cross SELL 72 (full exit) submitted 6/25, PENDING FILL.** #1 trader reconciliation
  item: fill-or-cancel. If filled → `log-closed`; if cancelled → rule likely re-fires. No new AAPL
  corporate event today (Thu's price hikes were the event; today is oversold/profit-taking + punditry).
- **Input-cost / margin-shock theme — NOW TWO held/universe instances (AAPL Mac/iPad 6/25, MSFT Xbox
  today; memory costs to double by fall 2027).** Both price-claimed, no responder. Recurring memory-cost
  pass-through across device makers. NEW library gap escalating. Track whether it broadens (Sony/Nintendo
  named) + any demand/guidance read.
- **SK Hynix $29.4B Nasdaq IPO (~July 10).** World's top HBM supplier (>50% share), Q1 rev +198% YoY,
  2nd-largest US IPO ever after SPCX. Memory-trade read-through (MU/SNDK). **Watch for a post-listing
  universe add** (like SPCX pre-operator-directive) once it trades with a US ticker.
- **SPCX (PROVISIONAL/quarantined) — broke below $135 IPO price (−32% from peak); IG bond sell-off
  ($305M lost in days); OpenAI reportedly delaying its IPO to 2027 citing SpaceX.** Spillover: ILLR +127%
  ($411M SpaceX-exposure treasury), QUCY board OKs SpaceX equity stake. Stays quarantined (revalidate 7/04).
  Carry: Nasdaq-100 add ~July 1. Track price path + bond/equity divergence.
- **JPM (held? no — universe) — succession shake-up surfaces CEO field; Dimon stays ~3 yrs.** Management
  event, price-claimed, no responder. Carry: $50B buyback (eff Jul 1) + 10% dividend. Track financials.
- **GOOGL (universe) — AI-talent departures + → DJIA pre-open Mon 6/29.** Forced-flow index event on a
  price-claimed name. Track index-flow commentary into 6/29.
- **DELL (universe) — shareholders approved Texas reincorporation.** Governance event, no responder.
- **INTC (universe) — US-government-stake "nationalization" political debate (ongoing overhang, no new
  action).** Carry: Goldman Neutral $150 init (single-bank). Track for an initiation cluster.
- **MU (held) — post-print window; ~5% profit-taking breather, no new catalyst.** IV crush in progress
  (short-vol setup). equity_event_driven_catalyst claims MU; held → entry guard skips; trailing stop +
  post-print window govern. Watch for any sharper give-back that engages the trailing stop.
- **AVGO (held) — no fresh catalyst (profit-taking only).** Jalapeño/OpenAI win stays claimed-but-unmodeled
  (partial gap).
- **ORCL (held) — restructuring (21k cuts) digestion continues; no new catalyst.** Partial gap.
- **TSLA (universe) — Musk ordered to testify (America PAC $1M suit) + Slate Auto $25k truck reveal.**
  Legal/competitive, price-claimed, no responder. Carry: NTSB/FSD overhang.
- **Memory-cost-inflation TWO-SIDED theme.** Makers (MU/SK Hynix/SNDK/WDC/STX) vs device makers
  (AAPL/MSFT) passing cost via price hikes. Track whether margin pressure broadens.
- **Macro: hot PCE / higher-for-longer + oil/Iran.** Core PCE 3.4% (Thu). Oil < ~$71 (5th down session),
  framework holding. Track Fed speakers, FedWatch, jobs report (first week of July), oil path.
- **Vol regime — VIX 18.89 (+1.4%), mid-18s, contango/no inversion.** Track whether index vol holds; MU
  post-print IV crush (short-vol setup).

## To do tomorrow (next news run — Mon 2026-06-29)

NOTE: Next weekday run is **Mon 6/29** (no run over the weekend; Sat is the research agent).

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A
   (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require `--sector`.
2. **USE `.venv/bin/python3` FROM THE REPO ROOT** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 26** (SYNA newly added). Check the trader claimed QCOM + SNDK + SYNA (P0
   triage); if still unclaimed, note it. SPCX stays quarantined (revalidate_by 7/04).
4. **AAPL fill reconciliation** — did the 6/25 EMA-cross SELL fill or cancel? (Trader's item, but track
   the position state.) No new AAPL event expected unless price-hike narrative produces a demand read.
5. **GOOGL → DJIA EFFECTIVE pre-open Mon 6/29** — index-flow / forced-buy commentary; cover the cash
   reaction.
6. **Quarter-end Tue 6/30 rebalance flow** + **SPCX → Nasdaq-100 ~July 1** + **SK Hynix listing ~July 10.**
   Three live index-rebalance/forced-flow instances.
7. **Input-cost theme follow-through** (AAPL + MSFT price hikes). Track whether it broadens / any demand
   or guidance read. NEW recurring input-cost library gap (now 2 instances).
8. **SYNA / onsemi M&A** — deal progress, any antitrust/regulatory friction; ON price (SYNA tracks it).
9. **Memory cohort** (MU post-print, SNDK, WDC/STX) + **SK Hynix IPO build-up** — does the read-through
   sustain after Friday's profit-taking.
10. **SPCX price path + bond/equity divergence + OpenAI-IPO-delay read-through.** Quarantined.
11. **JPM succession + financials rotation; buyback effective Jul 1.**
12. **Macro: hot-PCE / higher-for-longer + oil/Iran.** Fed speakers, FedWatch; jobs report (first week
    of July); oil path.
13. **Vol regime** — VIX vs 18; MU post-print IV crush; whether the de-rating vol bump reverts.
14. **Promote candidates if Mon refreshes:**
    - **SK Hynix** — post-IPO add candidate once it trades (~July 10); not promotable until a US ticker.
    - **WDC / STX** — memory cohort, flow/sympathy. Promote only on a clean 3-consecutive run OR a Tier-B
      catalyst (own beat+raise+5%, named contract, FDA, 3-bank).
    - **CRDO** — AI interconnect; thematic watch. **WOLF / SMCI** — flow-recurrence (not catalysts).
15. **Outlier movers + sector breakdown.** Generic gainers/losers query still flaky (~20 consecutive
    sessions; Fri surfaced micro-cap noise INHD/CAST + biotech MRNA/SLS/ACAD with no clear catalyst) —
    per-name reconstruction remains the workable path.
16. **Library gaps re-listing.** NEW Fri: M&A-arb activation (SYNA live instance); management/succession
    (JPM). Escalating: input-cost/margin-shock (NOW 2 — AAPL + MSFT). Carry: capital-allocation (JPM
    buyback); earnings-window ASSIGNMENT (CBRS); product/partnership + restructuring sub-triggers (AVGO,
    ORCL); index-rebalance/forced-flow (NOW THREE — GOOGL→DJIA 6/29, SPCX→Nasdaq-100 ~7/1, SK Hynix ~7/10);
    event-window on price-claimed names (TSLA/INTC/DELL/GOOGL/AMZN); macro_event_window (PCE/Fed,
    NEW_CATEGORY_NEEDED); vol_regime ACTIVATION (MU IV crush); m_a_arbitrage activation (SYNA + NUVL carry).
    Sat research = next opportunity.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Prior runs showed a miss (6/22) and a
  double (6/23); 6/24, 6/25, 6/26 appear single clean canonical 3:30 PT runs. **NB the 6/25 trader handoff
  flagged the 6/25 brief as STALE/ABSENT (header read 6/24)** — second pipeline miss that week. Asks stand:
  (a) stabilize the schedule / add a health-check alert on miss-or-double; (b) the `_load_news_brief()`
  staleness-guard — a stale brief should be rejected/down-weighted, not fed to strategies as live signal.
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher +
  daily_news_prompt.md to the venv python (or pip-install requirements into 3.14 / rebuild the venv), and
  pin python@3.13. **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts
  reality; please update.**
- **NEW — M&A-arb activation, live universe instance (SYNA / onsemi).** SYNA promoted as an M&A target;
  equity_pairs_trading_cointegration declares pairs_arbitrage but is inactive and claims no universe symbol.
  Sat research: activate a merger-arb/pairs strategy and claim SYNA (long SYNA / short ON at 1.350). Pairs
  with the NUVL/GSK m_a_arbitrage carry.
- **Input-cost / margin-shock event-window — NOW TWO instances (AAPL 6/25, MSFT 6/26).** Both price-claimed,
  no responder; recurring. Sat research: should an event-window overlay co-claim large-caps for cost/margin
  events?
- **Management/succession event-window (JPM shake-up) + capital-allocation (JPM buyback/dividend).** No rule
  reads either. Sat research: management-change + capital-allocation sub-triggers?
- **Index-inclusion as a 6th Tier-B trigger? — THREE live (GOOGL→DJIA 6/29; SPCX→Nasdaq-100 ~7/1; SK Hynix
  listing ~7/10).** Recurring forced-flow gap argues for a 6th Tier-B trigger or an index-rebalance overlay.
- **Event-driven strategy scope — product/partnership + restructuring sub-triggers.** AVGO (Jalapeño) + ORCL
  (21k cuts) claimed by event-driven yet neither event type is modeled.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** SPCX is the first live provisional claim
  (revalidate_by 2026-07-04). Confirm permanent.
- **CBRS earnings-window assignment.** CBRS claimed only by price-driven trend-following. Sat research:
  head-to-head vs equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is a judgment call; a mechanical
  counter would clarify the clock.
- **`cli open-orders` parser bug (REOPENED 6/25).** Errors `'dict' object has no attribute 'id'` on a live
  open order (the AAPL sell). Returns clean JSON only when no open orders exist. Fix the order-serialization
  path. Doesn't block execute.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate across days. Run
  `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by trend_following; Sat
  research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **128 items** cleanly (via venv). ARM/CSCO/HPE/NUVL had 0.
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-06-29T09:30:00-04:00`,
  `now_iso: 2026-06-26T15:39 PT` (post-close run).
- `cli list-active` → universe 25→26 (after SYNA promote), claimed 23, **unclaimed 3 (QCOM, SNDK, SYNA)**,
  provisional 1 (SPCX, revalidate_by 2026-07-04). `gap-registry coverage_holes` empty.
- WebSearch strong Fri: VIX 18.89 +1.4% / Nasdaq 5th down day (Yahoo/CNBC); onsemi→Synaptics $7B all-stock
  (SEC 8-K/425, StockTitan/Yahoo/TipRanks); SK Hynix $29.4B Nasdaq IPO ~July 10 (Bloomberg/SiliconANGLE/CNBC);
  MSFT Xbox price hike / memory costs double by 2027 (Benzinga); oil < ~$71 (TradingEconomics/CNBC); US-Iran
  60-day license (CNBC/Al Jazeera).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (INHD/CAST micro-cap noise; biotech
  MRNA/SLS/ACAD movers without surfaced catalysts) — per-name reconstruction stays the path (~20 sessions).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No candidate reached a clean 3-consecutive-catalyst run (WDC/STX/CRDO thematic/sympathy only;
    flow does not refresh the catalyst clock). **No Tier-A promotion.**
  - **Tier B:** **SYNA PROMOTED** under #1 (confirmed M&A target — onsemi $7B all-stock, definitive
    agreement + SEC filings, verifiable). 1 of 2 single-event slots used. No other qualifier (no NEW FDA
    binary, beat+raise+5% new name, 3-bank cluster, or Tier-1 customer win). SK Hynix is an IPO filing — not
    one of the 5 Tier-B triggers and no US-traded ticker yet → watch, not promote.
  - **Decision: 1 promotion (SYNA). Universe 25 → 26.**
- **`gap-registry coverage_holes` empty (confirmed)** — m_a_arbitrage, vol-regime, index-rebalance,
  input-cost, capital-allocation, management-change are ACTIVATION/assignment/taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name
  reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
