# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NORMAL FLOW (Tue 2026-06-30, quarter-end, canonical post-close 3:30 PM PT run).
  **The day's shape: an AI-chip *recovery* (semis bounced, Nasdaq firmed, VIX → 17.65) — PRICE ACTION we
  drop — over a real cluster of legal/regulatory events on held/universe names.** Genuine new events:
  **US DRAM price-fixing class action naming Micron** (MU, held — N.D. Cal., 17 plaintiffs, filed 6/25,
  surfaced 6/29–30); **Supreme Court granted cert on Apple's Epic App-Store appeal** (AAPL — orals ~Oct,
  ruling ~June 2027); **Australia's ACCC sued Amazon** over Prime Video ads; **AWS GPU prices +~20% eff
  July 1** (AMZN revenue tailwind, 3rd straight quarterly hike, BofA +1–2pp H2 AWS growth); **GOOGL's DJIA
  membership now LIVE** (eff 6/29, Dow > 52,000); **Palantir–Nvidia sovereign-AI deal** (NVDA). **0 promotions.
  Universe stays 26.** **NOT HALT-WORTHY:** no FOMC (ADP 7/1, payrolls 7/2 ahead); held-name legal items are
  slow processes; oil/Iran risk-positive.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used
  `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3 -m quant_trading_system.cli`. Operator action
  still required (open questions). Always `cd` to repo root (or use the absolute venv path) before CLI calls.
- **Universe: 26, unchanged.** No promotion (no Tier-A 3-session catalyst run; no clean Tier-B trigger).
  `list-active` → universe 26, claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**.
  `gap-registry coverage_holes` = **empty** (confirmed again).
- **Alpaca density: 126 items.** NVDA 19, GOOGL 13, MU 12, TSLA 11, AAPL 9, SPCX 9, AMZN 8, MSFT 6, JPM 5,
  QQQ 5, SPY 5, AVGO 4, META 4, SNDK 4, DELL 3, INTC 3, MRVL 2, TSM 2, ARM 1, ORCL 1; CBRS/CSCO/HPE/NUVL/
  QCOM/SYNA 0. All 6 category HTMLs + daily summary written.
- **Brief pipeline RECOVERED for today.** The 6/29 trader handoff flagged the 6/26 brief as STALE; today's
  6/30 brief is fresh and dated correctly. (Staleness-guard ask still stands — open questions.)

## Notable carry-forwards

- **MU (held) — DRAM price-fixing class action (NEW legal overhang).** Micron/Samsung/SK Hynix, ~90% DRAM
  share, alleged to have used the HBM transition as cover to curtail DDR3/DDR4 and inflate prices (+~700%/4yr).
  N.D. Cal., Judge Noel Wise, unproven, defendants not yet responded. Slow civil litigation — no responder
  (event-driven models earnings windows only; MU claim is provisional). Track docket / any cohort read-through.
- **AAPL — SCOTUS granted cert on the Epic App-Store contempt appeal.** 27% external-link fee at issue; orals
  ~October, ruling ~June 2027. Distant but real optionality on the fee model. (Note: AAPL's EMA-cross full exit
  filled 6/27 +1.37% — AAPL is universe-level news now, not a held long.) No responder.
- **AMZN — AWS GPU/ML capacity-block prices +~20%, effective July 1** (3rd straight quarter; BofA +1–2pp H2 AWS
  growth). Pricing-power/revenue event, price-claimed, no responder. **+ ACCC (Australia) suit** over Prime
  Video ads. Track whether AWS pricing recurs / any cloud-demand read.
- **GOOGL — DJIA membership LIVE (eff 6/29; Dow > 52,000).** Forced-flow event CONSUMMATED; now realized price.
  Index-rebalance gap stands as a theme, not a fresh GOOGL action.
- **NVDA — Palantir sovereign-AI deal for US agencies (partnership).** Price-claimed, no responder. Same hole
  as AVGO Jalapeño/OpenAI. (Also: Taiwan raid of Super Micro over alleged $2.5B Nvidia chip-smuggling — SMCI
  out of universe.)
- **SPCX (PROVISIONAL/quarantined) — Nasdaq-100 add CORRECTED to Tue July 7** (fast-track, ~$4.3B forced
  buying; NOT ~July 1 as prior notes carried). Also joined Russell 1000/Top 200 (FTSE Russell end-June).
  Revalidate_by **2026-07-04** — next provisional checkpoint, falls THIS week. Track price path into the add.
- **SK Hynix — $29B Nasdaq listing ~July 10.** Memory-trade read-through (MU/SNDK). Watch for a post-listing
  universe add once it trades with a US ticker.
- **Input-cost / pricing-power theme — now TWO-SIDED and broadening.** Device makers passing memory cost via
  price hikes (AAPL/MSFT, carry) vs cloud raising AI compute prices (AMZN AWS +20%). Recurring; no responder.
- **JPM — $50B buyback + dividend effective July 1 (carry); capital-return reset digestion.** No responder.
- **ORCL (held) — 21k-cut restructuring still weighs; no new event; no responder (book's red name, ~ -16%).**
- **QQQ (held) — watch for an EMA death-cross exit (as SPY fired 6/26).** Trend-following holds QQQ; cross not
  flipped. Trader item, but track position state.
- **Memory cohort (MU post-print, SNDK, WDC/STX) + SK Hynix build-up.** SNDK +6% on Bernstein PT-$3,000 boost
  (opinion). Does the read-through sustain after the legal-suit headline.
- **Macro: higher-for-longer + jobs week.** ADP 7/1, nonfarm payrolls Thu 7/2 (pulled early for July 4). May
  core PCE 3.4%. Oil soft / Iran framework holding. Track the prints + FedWatch.
- **Vol regime — VIX 17.65 (–~1.2 vs Fri), normal contango, no inversion.** MU post-print IV crush (short-vol);
  SPCX hyper-IV into the 7/7 add. Track whether index vol stays benign.

## To do tomorrow (next news run — Wed 2026-07-01)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A (3 consecutive
   catalyst sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require `--sector`.
2. **USE `.venv/bin/python3` FROM THE REPO ROOT** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 26.** Check unclaimed 0 / provisional 3 (QCOM, SPCX, SYNA). **SPCX revalidate_by
   7/04 — this week; if the trader/research hasn't revalidated, note it.**
4. **MACRO IS THE HEADLINE TOMORROW: ADP (June) Wed 7/1 8:15 ET, then nonfarm payrolls Thu 7/2 8:30 ET.** Cover
   the ADP result Wed; flag the NFP print as the next-day catalyst into the holiday-shortened week.
5. **MU DRAM antitrust suit** — track docket developments + any cohort/guidance read-through.
6. **AAPL SCOTUS Epic** — track for scheduling/commentary; distant ruling, low near-term weight.
7. **AMZN AWS pricing follow-through** (eff 7/1) + ACCC suit. Does cloud-pricing recur as a theme.
8. **Index-rebalance cluster — SPCX→Nasdaq-100 Tue 7/7; SK Hynix listing ~7/10.** Two live forced-flow instances
   into next week (GOOGL→DJIA now done). Track the SPCX path into the add.
9. **Input-cost / pricing-power theme** — device-maker cost pass-through (AAPL/MSFT) vs AWS price hikes. Recurring
   library gap (now both sides).
10. **Memory cohort** (MU post-print + legal suit, SNDK, WDC/STX) + **SK Hynix IPO build-up** — sustain check.
11. **JPM buyback effective 7/1; financials rotation.**
12. **Vol regime** — VIX vs 17–18; MU IV crush; whether quarter-end-low vol holds into the jobs prints.
13. **Promote candidates if Wed refreshes:**
    - **CRDO** — AI-interconnect; **recurrence ~session 2–3 (thematic)**. NOT promoted today (PT-cluster timing
      is prior weeks; today's move is sector-rally + reiterated upgrades = opinion). Promote on a *fresh*
      same-week 3-bank initiation cluster OR an own beat-and-raise+5%. **Track the recurrence count.**
    - **SK Hynix** — post-IPO add candidate once it trades (~July 10); not promotable until a US ticker.
    - **WDC / STX** — memory cohort, flow/sympathy. Promote only on a clean 3-consecutive catalyst run OR a
      Tier-B catalyst.
    - **AMAT / KLA / ALAB (Astera Labs)** — chip-equipment / AI-interconnect strength (price/flow today); watch.
    - **CMCSA** — media/tech split announced (spinoff, ~1yr) — not a Tier-B trigger; operator note only.
14. **Outlier movers + sector breakdown.** Generic gainers/losers query still flaky (~21 consecutive sessions;
    today INHD +2,892% MTD micro-cap noise). Per-name reconstruction remains the workable path.
15. **Library gaps re-listing.** NEW Tue: litigation/antitrust (MU); regulatory/appellate (AAPL SCOTUS, AMZN
    ACCC); cloud-pricing/capital-allocation (AMZN AWS). Carry/escalating: index-rebalance (SPCX 7/7, SK Hynix
    ~7/10); input-cost/pricing-power (now two-sided); partnership (NVDA, AVGO); M&A-arb activation (SYNA + NUVL);
    management/succession + capital-allocation (JPM); restructuring (ORCL); earnings-window assignment (CBRS);
    macro_event_window (jobs week, NEW_CATEGORY_NEEDED); vol_regime activation (MU IV crush). Sat research = next.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Misses span 6/22, 6/25, (6/26 recovered),
  6/29 (trader flagged 6/26 brief STALE); 6/30 recovered. Asks stand: (a) stabilize the schedule / add a
  health-check alert on miss-or-double; (b) the `_load_news_brief()` staleness-guard — a stale brief should be
  rejected/down-weighted, not fed to strategies as live signal (it parses date_in_file but never compares to today).
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher +
  daily_news_prompt.md to the venv python (or pip-install requirements into 3.14 / rebuild the venv), and pin
  python@3.13. **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.**
- **Litigation/antitrust event-window — NEW live instance (MU DRAM suit).** No rule reads a lawsuit/antitrust
  filing. Sat research: should an event-window overlay cover litigation/regulatory catalysts on large-caps?
- **Cloud-pricing / capital-allocation sub-trigger — AMZN AWS +20%.** No rule reads a pricing/capital-allocation
  disclosure. Pairs with the input-cost (AAPL/MSFT) carry as a two-sided pricing-power theme.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (GOOGL→DJIA done; SPCX→Nasdaq-100 7/7; SK Hynix ~7/10;
    FTSE Russell reconstitution end-June).** Recurring forced-flow gap argues for a 6th trigger or an overlay.
- **M&A-arb activation, live universe instance (SYNA / onsemi).** equity_pairs_trading_cointegration declares
  pairs_arbitrage but only provisionally claims SYNA. Sat research: activate merger-arb (long SYNA / short ON at
  1.350). Pairs with the NUVL/GSK carry.
- **Management/succession + capital-allocation event-window (JPM).** No rule reads a buyback/dividend/succession.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Three provisional claims live (QCOM, SPCX, SYNA);
  SPCX revalidate_by 7/04 is the first checkpoint this week.
- **CBRS earnings-window assignment.** CBRS claimed only by price-driven trend-following. Sat: head-to-head vs
  equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is a judgment call; a mechanical
  counter would clarify the clock (CRDO is the current ambiguous case).
- **`cli open-orders` parser bug (QUIESCENT).** Errors `'dict' object has no attribute 'id'` only when a live
  open order exists; clean when none. Fix the order-serialization path.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate across days. Run
  `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim +
  m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **126 items** cleanly (via venv). CBRS/CSCO/HPE/NUVL/QCOM/SYNA 0.
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-07-01T09:30:00-04:00`,
  `now_iso: 2026-06-30T15:39 PT` (post-close run).
- `cli list-active` → universe 26, claimed 26, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA). `gap-registry
  coverage_holes` empty.
- WebSearch strong Tue: VIX 17.65 (Yahoo/TradingEconomics); MU/Samsung/SK Hynix DRAM class action (Tom's
  Hardware/Seeking Alpha/Benzinga, filed 6/25 N.D. Cal); AAPL SCOTUS cert on Epic (Bloomberg/MacRumors);
  AWS +20% GPU pricing eff 7/1 (Benzinga/TheStreet/BofA); SPCX→Nasdaq-100 **July 7** fast-track (Seeking
  Alpha/CNBC) — corrected from prior ~7/1; ADP 7/1 / NFP 7/2 (BLS schedule); quarter-end best-in-6-yrs (Schwab/Yahoo).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (INHD +2,892% MTD micro-cap noise) —
  per-name reconstruction stays the path (~21 sessions).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No candidate reached a clean 3-consecutive-catalyst run (CRDO thematic/PT-driven; WDC/STX
    sympathy; flow does not refresh the catalyst clock). **No Tier-A promotion.**
  - **Tier B:** No qualifier — no NEW confirmed M&A target (SYNA already in; CMCSA is a spinoff, not a target;
    Kalshi/Polymarket takeover-risk speculative), no FDA binary, no new beat+raise+5% name, no *fresh* same-week
    3-bank initiation cluster (CRDO's PT cluster is prior weeks + opinion-driven), no Tier-1 customer-win press
    release. **No Tier-B promotion.**
  - **Decision: 0 promotions. Universe stays 26.**
- **`gap-registry coverage_holes` empty (confirmed)** — litigation, regulatory, cloud-pricing, m_a_arbitrage,
  vol-regime, index-rebalance, input-cost, capital-allocation, management-change are ACTIVATION/assignment/
  taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction
  beats generic gainers/losers; major-M&A → target per-name search is cleanest.
