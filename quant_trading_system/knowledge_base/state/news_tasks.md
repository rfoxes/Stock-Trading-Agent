# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Thu 2026-06-25, canonical post-close 3:30 PM PT run).
  **The day's twist: MU's record-blowout gap-up HELD in the cash session (+15%), but the
  same memory shortage became a cost shock for hardware makers** — **AAPL −6.1%** (single
  heaviest S&P weight) after **raising Mac/iPad prices 15–20%** (Cook: "Hundred-Year
  Flood"); **MSFT −3.2%** (52-wk low, Xbox price hike) — **Nasdaq down a 4th straight
  day**. Dow rose on a value rotation (CAT +5.8%, UNH +2.7%). Hot **May PCE** (core 3.4%,
  highest since Oct '23; headline 4.1%); **oil < $70** (4th down session, US-Iran de-esc).
  **2 universe promotions:** **QCOM** (Tier-B #5, Meta anchor customer for Dragonfly C1000)
  + **SNDK** (Tier-A session 3, memory supercycle). **NOT HALT-WORTHY:** no FOMC; MU
  resolved favorably (held); AAPL −6% is realized price on a cost narrative, not a guidance
  cut; oil/Iran risk-positive.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire run used
  `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3 -m quant_trading_system.cli`.
  Operator action still required (see open questions). Always `cd` back to repo root (or use
  the absolute venv path) before CLI calls — a `cd` into a news subdir breaks the relative
  venv path.
- **Universe: GREW 23 → 25.** QCOM + SNDK promoted today (both technology), both **UNCLAIMED**
  → trader P0 triage owns the claim (`triage-symbol QCOM --gap-type event_catalyst`,
  `triage-symbol SNDK --gap-type trending`). The prior 23 stay claimed. SPCX still
  **PROVISIONAL / execution-quarantined** (revalidate_by **2026-07-04**). `gap-registry
  coverage_holes` = **empty** (confirmed again).
- **Alpaca density: 162 items.** MU 40, META 13, NVDA 13, AMZN 11, AAPL 11, GOOGL 10,
  SPCX 10, MSFT 9, INTC 7, QQQ 6, SPY 5, DELL 4, MRVL 3, TSM 3, JPM 2, ORCL 2, AVGO 1;
  ARM/CBRS/CSCO/HPE/NUVL 0. All 6 category HTMLs + daily summary written.
- **2 promotions Thu (cap respected):** QCOM = 1 single-event (Tier-B #5, under the 2/day
  cap); SNDK = Tier-A (uncapped, 3-session recurrence).

## Notable carry-forwards

- **MU (held) — Day-1 cash reaction HELD (+15%); gap-up did NOT fade.** Rev $41.46B
  (~+346% YoY), Q4 guide ~$50B; ~$100B forward contracts; FY26 capex $27B + 100% excess-cash
  return; CEO: shortage tight beyond 2027, no "line of sight." equity_event_driven_catalyst
  claims MU (true responder); held → entry guard skips; post-print window + trailing stop
  govern. **The trailing-stop-on-give-back scenario did NOT trigger today (no fade).** Watch
  Fri for any delayed give-back / IV-crush mechanics. Drop analyst PT resets (BofA $1,550,
  Susquehanna $2,000 — opinions).
- **AAPL (held) — NEW negative held-name event: 15–20% Mac/iPad price hikes on memory costs,
  −6.1%.** First held-name NEGATIVE event with no responder (claimed by price-driven
  trend-following). Library gap: input-cost / margin-compression event-window. Track whether
  the price-hike narrative broadens to other hardware names / a demand read.
- **JPM (universe) — $50B buyback (eff Jul 1) + 10% dividend hike, post-stress-test;
  all-time high.** Capital-allocation event; price-claimed, no responder (NEW library gap).
  Track financials-rotation follow-through.
- **CBRS (universe) — Day-2 record two-session loss** (~$172 vs $182 prior close) on weak FY
  outlook / lower-margin guide. Assignment gap (claimed by trend-following, not the
  earnings-window responder). Track Day-3 stabilization.
- **INTC (universe) — Goldman initiated Neutral, $150 PT** (server-CPU + foundry tailwinds,
  "balanced" risk/reward); premarket MU-pop faded to red close. Single-bank init (below
  3-bank Tier-B cluster); no responder. Track for an initiation cluster.
- **QCOM (NEW universe) — Investor Day data-center pivot: $15B DC rev by FY29, Dragonfly
  C1000, Meta anchor customer, $40B FY29 non-handset; +7.4%.** Unclaimed → trader triage /
  Saturday research. Track DC follow-through + any further customer wins.
- **SNDK (NEW universe) — memory/NAND supercycle, MU-validated; +16%, ~600% YTD.** Unclaimed
  → trader triage / Saturday research. Track whether the cohort sustains.
- **AVGO (held) — Jalapeño/OpenAI follow-through quieted.** No fresh catalyst today; the
  product/partnership win stays claimed-but-unmodeled by event-driven (partial gap).
- **ORCL (held) — 21k job-cut digestion continues; book's only red.** Restructuring event
  unmodeled by event-driven (partial gap).
- **GOOGL → DJIA effective pre-open Mon 6/29** (replacing VZ). Forced-flow/index event on a
  price-claimed name; traded lower today; Google Finance exited beta (portfolios/AI tools).
  Track index-flow commentary 6/26 & into 6/29.
- **TSLA — NTSB probe opened + wrongful-death suit filed (Texas FSD crash).** Regulatory/legal
  escalation; price-claimed, no responder. Track probe scope + energy-business follow-through.
- **SPCX — bond-deal "bubble" warnings (Allianz: $70B "funny money"), FOMO-trap framing;
  +393% "SpaceX MSTR."** Stays quarantined (revalidate_by 7/04). Carry: $6.3B Reflection
  deal, Cathie Wood buying, Nasdaq-100 add ~July 1. Track price path + bond/equity divergence.
- **Memory-cost-inflation TWO-SIDED theme.** MU/SNDK/WDC/STX (makers) up; AAPL/MSFT (device
  makers) down on hardware price hikes. Track whether device-maker margin pressure broadens.
- **Hot PCE / higher-for-longer.** Core PCE 3.4% (highest since Oct '23). May seen as the
  2026 inflation peak; slowing expected from July. Track Fed speakers, CME FedWatch, next
  CPI/jobs.
- **Oil < $70 / US-Iran de-escalation.** Disinflationary, risk-positive. Track roadmap
  durability + waiver extension.
- **VIX ~18.6 (−5%) — eased back toward 18; contango, no inversion.** Track whether index vol
  holds >18 or reverts; MU post-print IV crush (short-vol setup).

## To do tomorrow (next news run, Fri 2026-06-26)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.**
   Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require
   `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3` FROM THE REPO ROOT** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 25** (QCOM + SNDK newly added). Check the trader claimed QCOM +
   SNDK (P0 triage); if still unclaimed, note it. SPCX stays quarantined (revalidate_by 7/04).
4. **MU Day-2 cash reaction** — does the +15% gap-up hold/extend/fade Fri; any delayed IV-crush
   give-back that could finally engage the trailing stop. Drop PT resets.
5. **AAPL price-hike follow-through** (held; −6.1% Thu). Track whether the memory-cost margin
   narrative broadens / any demand or guidance read. NEW input-cost library gap.
6. **CBRS Day-3** (record two-session loss). Assignment gap. Cover the cash reaction.
7. **JPM buyback follow-through + financials rotation** (all-time high on $50B + dividend).
8. **QCOM data-center follow-through** (Investor Day pivot; Meta anchor). **SNDK / memory
   cohort** (WDC/STX) — does the MU read-through sustain.
9. **GOOGL → DJIA (effective Mon 6/29).** Track index-flow commentary into 6/26 & 6/29.
10. **SPCX price path + bond/equity divergence + Nasdaq-100 rebalance (~July 1).** Quarantined.
11. **Macro: hot-PCE / higher-for-longer + oil/Iran threads.** Fed speakers, FedWatch; oil
    path, roadmap durability.
12. **Vol regime** — VIX vs 18; MU post-print IV crush; whether the de-rating vol bump reverts.
13. **Promote candidates if Fri refreshes:**
    - **WDC / STX** — memory cohort, rode MU (flow/sympathy). Watch; promote only on a clean
      3-consecutive run OR a Tier-B catalyst (own beat+raise+5%, named contract, FDA, 3-bank).
    - **CRDO** — AI interconnect; thematic watch.
    - **WOLF / SMCI** — flow-recurrence (not catalysts). Flow does NOT refresh the catalyst clock.
14. **Outlier movers + sector breakdown.** Generic gainers/losers query still flaky
    (~19 consecutive sessions) — per-name reconstruction remains the workable path.
15. **Library gaps re-listing.** NEW Thu: input-cost/margin-shock on a held name (AAPL —
    first held-name NEGATIVE event, no responder); capital-allocation event (JPM buyback/
    dividend, no responder). Carry: earnings-window ASSIGNMENT (CBRS); sell-side initiation
    (INTC Goldman, single-bank); product/partnership + restructuring sub-triggers on
    event-driven covered names (AVGO Jalapeño, ORCL); index-rebalance/forced-flow (GOOGL→DJIA
    6/29 + SPCX→Nasdaq-100 ~July 1 — TWO live); event-window on price-claimed names
    (TSLA/META/AMZN); macro_event_window (PCE/Fed, NEW_CATEGORY_NEEDED); vol_regime ACTIVATION
    (MU post-print IV crush); m_a_arbitrage activation (NUVL). Sat research = next opportunity.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Prior runs showed a miss
  (6/22 skipped) and a double (6/23). 6/24 + 6/25 appear to be single clean canonical 3:30 PT
  runs. Asks stand: (a) stabilize the schedule / add a health-check alert on miss-or-double;
  (b) the `_load_news_brief()` staleness-guard — a stale brief should be rejected/down-weighted,
  not fed to strategies as live signal.
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working
  interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the
  scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install
  requirements into 3.14 / rebuild the venv), and pin python@3.13. **daily_news_prompt.md
  line ~31 still says "There is no virtualenv" — stale, contradicts reality; please update.**
- **NEW — Input-cost / margin-shock event-window (AAPL).** AAPL fell 6.1% on a real corporate
  event (15–20% price hikes on memory-cost inflation) yet is claimed only by price-driven
  trend-following. First held-name NEGATIVE event with no responder. Sat research: should an
  event-window overlay co-claim large-caps for cost/margin-guidance events?
- **NEW — Capital-allocation event-window (JPM $50B buyback + dividend).** No rule reads a
  buyback/dividend authorization. Sat research: a capital-allocation sub-trigger?
- **Index-inclusion as a 6th Tier-B trigger? — TWO live (GOOGL→DJIA 6/29; SPCX→Nasdaq-100
  ~July 1).** Both in-universe so promotion moot, but the recurring forced-flow gap argues for
  a 6th Tier-B trigger or an index-rebalance overlay.
- **Event-driven strategy scope — product/partnership + restructuring sub-triggers.** AVGO
  (Jalapeño) + ORCL (21k cuts) claimed by event-driven yet neither event type is modeled.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** SPCX is the first live
  provisional claim (revalidate_by 2026-07-04). Confirm permanent.
- **CBRS earnings-window assignment.** CBRS (debut 6/23, record two-session loss through 6/25)
  claimed only by price-driven trend-following. Sat research: head-to-head vs
  equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is a judgment
  call; skipped/doubled sessions muddy the clock (SNDK's chain). A mechanical counter would
  clarify. (SNDK promoted Thu at session 3 of the rebuild.)
- **`cli open-orders` parser bug (carry-forward).** Clean JSON on recent runs; provisionally
  closed. Confirm on a live open order.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate across
  days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by
  trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **162 items** cleanly (via venv).
  ARM/CBRS/CSCO/HPE/NUVL had 0.
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-06-26T09:30:00-04:00`,
  `now_iso: 2026-06-25T15:37 PT` (post-close run).
- WebSearch strong Thu: MU Day-1 close +15% / cohort (TheStreet/Bloomberg/Benzinga); AAPL
  −6.1% on 15–20% Mac/iPad price hikes (TheStreet/Barchart); QCOM Investor Day ($15B DC rev,
  Meta anchor, +7.4% — CNBC/Bloomberg/ServeTheHome); JPM $50B buyback + dividend (CNBC/SEC
  8-K); INTC Goldman Neutral $150 (Investing.com); CBRS record two-session loss (Bloomberg/
  Yahoo); PCE core 3.4% (BEA/CBS); oil < $70 (Bloomberg/TradingEconomics); VIX 18.63 (Cboe).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (micro-cap noise
  INHD/CAST/SAGT) — per-name reconstruction stays the path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** SNDK reached session 3 of the post-skip rebuild (memory cohort, MU-validated)
    → **PROMOTED** (technology). WDC/STX/CRDO thematic/sympathy only — not yet 3 consecutive.
  - **Tier B:** **QCOM PROMOTED** under #5 (Tier-1 customer win — Meta named anchor for
    Dragonfly C1000, verifiable). No other qualifier (no NEW M&A target, FDA binary, clean
    beat+raise+5% NEW name, or 3-bank cluster). 1 of 2 single-event slots used.
  - **Decision: 2 promotions (QCOM, SNDK). Universe 23 → 25.**
- **`gap-registry coverage_holes` empty (confirmed)** — vol-regime + index-rebalance +
  input-cost + capital-allocation are ACTIVATION/assignment/taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works;
  per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search
  is cleanest.
