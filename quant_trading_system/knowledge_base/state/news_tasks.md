# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NORMAL FLOW (Wed 2026-07-01, first H2 session, canonical post-close 3:30 PM PT run).
  **The day's shape: an AI-capex give-back rotation (semis −~4.5% inside the Nasdaq-100 vs a Dow record / software
  bid) — PRICE ACTION we drop — over a real cluster of legal/regulatory + big-tech-business events.** Genuine new
  events: **Swedish court ordered GOOGL to pay ~$1.97B to Klarna's PriceRunner** (comparison-shopping antitrust)
  + a **US judge barred Google from re-litigating search monopoly** (Yelp win) — two adverse antitrust items same
  day; **META building a cloud unit to sell excess AI compute** (hit neoclouds NBIS −12% / CRWV) **+ META lost its
  bid to dismiss a 29-state youth-addiction suit** (to trial); **MSFT cutting thousands** (sales/consulting/Xbox)
  **+ Haleon 5-yr AI deal**; **AWS launched a $1B AI-engineering unit**; **MU** CEO supply-tight-through-2027 +
  Cook "extreme shortage" + $250M Trump Accounts; **NVDA** Michael Burry short disclosure + Anthropic export
  controls lifted; **JPM** $50B buyback eff 7/1; **TSLA** Q2 delivery print due 7/2. **0 promotions. Universe
  stays 26.** **NOT HALT-WORTHY:** no FOMC (the jobs print is 7/2, not today; ADP already digested); legal items
  are on price-claimed names; geopolitics risk-positive.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used
  `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3 -m quant_trading_system.cli`. Operator action still
  required (open questions). Always `cd` to repo root (or use the absolute venv path) before EVERY CLI call — a
  bare `.venv/bin/python3` from the wrong cwd errors ("no such file or directory").
- **Universe: 26, unchanged.** No promotion (no Tier-A 3-session catalyst run; no clean Tier-B trigger; no operator
  directive). `list-active` → universe 26, claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**.
  `gap-registry coverage_holes` = **empty** (confirmed again).
- **Alpaca density: 155 items.** NVDA 18, TSLA 16, GOOGL 14, META 14, MU 15, MSFT 11, SPCX 9, AMZN 8, SNDK 8,
  INTC 7, ORCL 5, AAPL 5, MRVL 5, QQQ 5, SPY 4, AVGO 2, DELL 2, QCOM 2, TSM 2, ARM 1, CSCO 1, JPM 1;
  CBRS/HPE/NUVL/SYNA 0. All 6 category HTMLs + daily summary written.
- **Brief pipeline FRESH today** (6/30 was fresh too; misses still span 6/22, 6/25, 6/29). Staleness-guard ask
  still stands (open questions).

## Notable carry-forwards

- **GOOGL — antitrust double hit (NEW).** Sweden's Patent and Market Court awarded ~$1.97B ($1.5B + interest) to
  Klarna's PriceRunner (Shopping-abuse case; dismissed most of the SEK 80B claim → ~18% of the ask). Same day a
  US magistrate barred Google from re-litigating search-monopoly power (Yelp). Real cost + precedent overhang;
  price-claimed, no responder. Track for further antitrust developments (DOJ search remedies, EU DMA).
- **META — cloud-compute business (NEW strategy shift) + 29-state addiction suit to trial (NEW litigation).**
  Meta selling excess AI compute intrudes on AWS/Azure/GCP + neoclouds (NBIS/CRWV). Price-claimed, no responder.
  Track for official confirmation / capacity figures and the addiction-trial calendar.
- **MSFT — thousands-scale layoffs (NEW; 2nd big-tech restructuring after ORCL 21k) + Haleon 5-yr AI deal.**
  Price-claimed, no responder. Track whether the restructuring wave broadens (recurring event class).
- **AMZN — AWS $1B AI-engineering unit (NEW capital allocation) + ~20% GPU price hike (eff 7/1, carry) + ACCC
  suit (carry).** Price-claimed, no responder. Cloud-pricing/capital-allocation theme now multi-session.
- **MU (held) — supply-tight-through-2027 (CEO) + Cook "extreme shortage" + $250M Trump Accounts + DRAM antitrust
  suit (carry).** Provisional/quarantined event-driven claim models earnings windows only. Track docket + any
  cohort/guidance read-through + IV crush give-back (trailing-stop scenario).
- **NVDA — Michael Burry short disclosure ("beginning of the end") + Anthropic export controls lifted + SMCI
  Taiwan detentions (chip-smuggling probe).** Price-claimed, no responder. Track positioning + export-policy.
- **TSLA — Q2 delivery print due Thu 7/2 (IR consensus ~406k, Bloomberg ~396k); full Q2 earnings July 22.** The
  earnings-window responder does NOT claim TSLA (trend-following does) → assignment gap. Optimus on Model S/X
  line; CA EV-incentive snub. **COVER THE DELIVERY RESULT TOMORROW (7/2).**
- **INTC — Q2 earnings July 23** (outside 14-day window; flag as the date approaches).
- **JPM — $50B buyback + dividend effective 7/1 (consummated).** Capital-return reset; no responder.
- **ORCL (held) — 21k-cut restructuring still weighs; no new event; no responder (book's red name).**
- **QQQ (held) — EMA death-cross SELL 28 submitted 6/30, pending fill.** Trader reconciles at execute; track
  position state (trend-following has now exited SPY 6/26, AAPL 6/25, QQQ 6/30).
- **SPCX (PROVISIONAL/quarantined) — Nasdaq-100 add Tue July 7 (~$4.3B forced buying). revalidate_by 2026-07-04
  — THIS WEEK.** Track the price path into the add + whether research/head-to-head revalidates by 7/04.
- **SK Hynix — $29B Nasdaq listing ~July 10.** Memory-trade read-through (MU/SNDK). Post-listing universe-add
  candidate once it trades with a US ticker.
- **Memory cohort (MU, SNDK, WDC/STX) + SK Hynix build-up.** SNDK +BofA PT $2,500 (opinion). Demand confirmation
  (Cook shortage) vs the DRAM legal tail. Sustain check.
- **AI-capex repricing theme (NEW two-sided positioning).** Apollo's Sløk "painful repricing" warning vs Ackman
  bullish vs Burry shorts (NVDA/TSLA/AMAT/CAT). Recurring; no responder.
- **Input-cost / pricing-power theme (carry, two-sided).** Device makers passing memory cost (AAPL/MSFT) vs cloud
  raising AI-compute prices (AWS). Recurring; no responder.
- **Macro: jobs week + higher-for-longer.** ADP June +98k (miss, 7/1). **NFP Thu 7/2 8:30 ET (pulled early for
  July 4)** — THE headline print tomorrow. ISM Mfg 53.3. May core PCE 3.4%. Oil soft. Track the NFP + FedWatch.
- **Vol regime — VIX ~16.45 (−~1.2 vs 6/30), normal contango, no inversion, fresh multi-week low.** Dispersion
  single-name (semis rout; MU IV crush; SPCX/TSLA event-IV). Track whether index vol stays benign through NFP.

## To do tomorrow (next news run — Thu 2026-07-02)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A (3 consecutive
   catalyst sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require `--sector`.
2. **USE `.venv/bin/python3` AND `cd` TO THE REPO ROOT** for EVERY CLI call. Bare `python3` fails; a bare
   `.venv/bin/python3` from the wrong cwd also fails ("no such file or directory").
3. **Universe should confirm 26.** Check unclaimed 0 / provisional 3 (QCOM, SPCX, SYNA). **SPCX revalidate_by
   7/04 — this Saturday; if the trader/research hasn't revalidated, note it as a live checkpoint.**
4. **MACRO IS THE HEADLINE TOMORROW: nonfarm payrolls (June) Thu 7/2 8:30 ET** (pulled early for July 4). Cover
   the result; it's the week's marquee print into a half-day/holiday-shortened week (markets close early 7/3,
   shut 7/4). ADP was soft (+98k) — watch the beat/miss vs ~110k+ NFP consensus + unemployment rate.
5. **TSLA Q2 delivery print (due 7/2)** — cover the actual number vs ~406k IR / ~396k Bloomberg consensus. A
   real universe catalyst; assignment gap (earnings-window strategy doesn't claim TSLA).
6. **GOOGL antitrust follow-through** — Klarna appeal chatter, Yelp-suit next steps, any DOJ/EU read-through.
7. **META cloud-compute + addiction-suit** — official confirmation / capacity detail + trial scheduling.
8. **MSFT layoffs scope** + whether the big-tech restructuring wave broadens.
9. **MU DRAM antitrust suit** — docket + cohort read-through + IV-crush give-back (trailing-stop scenario).
10. **Index-rebalance cluster — SPCX→Nasdaq-100 Tue 7/7; SK Hynix listing ~7/10.** Track SPCX path into the add.
11. **Memory cohort** (MU, SNDK, WDC/STX) + **SK Hynix IPO build-up** — sustain check.
12. **Vol regime** — VIX vs ~16–17; whether index vol stays benign through the 7/2 NFP; MU IV crush; TSLA/SPCX
    event-IV.
13. **Promote candidates if Thu refreshes:**
    - **CRDO** — AI-interconnect; thematic carry, recurrence clock did NOT advance today (absent from feed).
      Promote on a *fresh* same-week 3-bank initiation cluster OR an own beat-and-raise+5%. Track recurrence.
    - **SK Hynix** — post-IPO add candidate once it trades (~July 10); not promotable until a US ticker.
    - **WDC / STX** — memory cohort, sympathy/flow. Promote only on a clean 3-consecutive catalyst run OR Tier-B.
    - **NBIS / CRWV** — neoclouds moved on Meta's cloud entry (sympathy, not own catalyst); watch only.
    - **AMAT / KLA / ALAB** — chip-equipment / AI-interconnect; price/flow; watch.
14. **Outlier movers + sector breakdown.** Generic gainers/losers query STILL screen-level (~22 consecutive
    sessions; today YTD MGRT/ANL/SNDK, no same-day catalyst names outside universe). Per-name reconstruction
    remains the workable path.
15. **Library gaps re-listing.** NEW Wed: regulatory/antitrust ruling (GOOGL Klarna+Yelp, META addiction suit);
    business-line launch (META cloud, AMZN AWS unit); restructuring (MSFT + ORCL carry); delivery/earnings-window
    assignment (TSLA 7/2, INTC 7/23); short-interest disclosure (NVDA Burry); capital-allocation (JPM buyback,
    AMZN pricing, MU Trump Accounts); partnership (MSFT-Haleon, NVDA carry). Carry/escalating: index-rebalance
    (SPCX 7/7, SK Hynix ~7/10); M&A-arb activation (SYNA + NUVL); MU DRAM litigation; macro_event_window (jobs
    week, NEW_CATEGORY_NEEDED); vol_regime activation (MU IV crush). Sat research = next.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Misses span 6/22, 6/25, 6/29; 6/30 + 7/1
  fresh. Asks stand: (a) stabilize the schedule / add a health-check alert on miss-or-double; (b) the
  `_load_news_brief()` staleness-guard — a stale brief should be rejected/down-weighted, not fed to strategies as
  live signal (parses date_in_file but never compares to today).
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher +
  daily_news_prompt.md to the venv python (or pip-install requirements into 3.14 / rebuild the venv), and pin
  python@3.13. **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.**
- **Regulatory/antitrust event-window — NEW live cluster (GOOGL Klarna+Yelp, META addiction suit; MU DRAM carry;
  AAPL SCOTUS carry).** No rule reads a court/agency ruling. Sat research: should an event-window overlay cover
  litigation/regulatory catalysts on large-caps?
- **Business-line-launch sub-trigger — META (AI cloud) + AMZN (AWS $1B unit).** No rule reads a strategic
  business-line announcement.
- **Restructuring/workforce-reduction event-window — MSFT (NEW) + ORCL (carry).** Recurring big-tech class; no
  responder.
- **Earnings/delivery-window assignment — TSLA (7/2 deliveries) + INTC (7/23) + CBRS (carry).** Earnings-window
  responder (equity_event_driven_catalyst) does not claim these names. Sat: assign it.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX→Nasdaq-100 7/7; SK Hynix ~7/10; GOOGL→DJIA done;
  FTSE Russell end-June).** Recurring forced-flow gap argues for a 6th trigger or an overlay.
- **M&A-arb activation, live universe instance (SYNA / onsemi).** equity_pairs_trading_cointegration declares
  pairs_arbitrage but only provisionally claims SYNA. Sat research: activate merger-arb (long SYNA / short ON at
  1.350). Pairs with the NUVL/GSK carry.
- **Capital-allocation / capital-return event-window (JPM $50B buyback; AMZN AWS pricing; MU Trump Accounts).**
  No rule reads a buyback/dividend/pricing disclosure.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Three provisional claims live (QCOM, SPCX, SYNA);
  SPCX revalidate_by 7/04 (Sat) is the first checkpoint this week.
- **CBRS earnings-window assignment.** CBRS claimed only by price-driven trend-following. Sat: head-to-head vs
  equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is a judgment call; a mechanical
  counter would clarify the clock (CRDO is the current ambiguous case; its clock did NOT advance today).
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** Errors `'dict' object has no attribute 'id'` when a
  live open order exists (bit on the QQQ order 6/30); clean when none. Fix the order-serialization path.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate across days. Run
  `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim +
  m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **155 items** cleanly (via venv). CBRS/HPE/NUVL/SYNA 0.
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-07-02T09:30:00-04:00`,
  `now_iso: 2026-07-01T15:39 PT` (post-close run).
- `cli list-active` → universe 26, claimed 26, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA). `gap-registry
  coverage_holes` empty.
- WebSearch strong Wed: ADP June +98k miss (CNBC/Fox/Yahoo); VIX ~16.45 (Cboe/Yahoo); ISM Mfg PMI June 53.3
  (ISM/PRNewswire); GOOGL ~$1.97B Klarna/PriceRunner ruling + Yelp win (Bloomberg/Benzinga/PYMNTS); TSLA Q2
  deliveries expected 7/2 ~406k (TechTimes/Electrek/Investing.com).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (YTD MGRT/ANL/SNDK, no same-day catalyst
  outside universe) — per-name reconstruction stays the path (~22 sessions).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No candidate reached a clean 3-consecutive-catalyst run (CRDO absent from today's feed → clock
    did not advance; WDC/STX sympathy; NBIS/CRWV sympathy to Meta's event). **No Tier-A promotion.**
  - **Tier B:** No qualifier — no NEW confirmed M&A target (SYNA already in), no FDA binary, no universe/candidate
    beat+raise+5% (PRGS beat but no thematic fit / no raise-confirmation cohort), no *fresh* same-week 3-bank
    initiation cluster, no candidate Tier-1 customer-win press release (Haleon/MSFT is on an existing member).
    **No Tier-B promotion.**
  - **Decision: 0 promotions. Universe stays 26.**
- **`gap-registry coverage_holes` empty (confirmed)** — regulatory, business-launch, restructuring, cloud-pricing,
  m_a_arbitrage, vol-regime, index-rebalance, capital-allocation, delivery-window are ACTIVATION/assignment/
  taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction
  beats generic gainers/losers; major-M&A → target per-name search is cleanest.
- **HOLIDAY NOTE:** July 3 is a shortened session (early close ~1 PM ET); markets closed July 4 (Sat). Next full
  cash session after Thu 7/2 is Mon 7/6. Factor the shortened week into scheduling.
