# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Wed 2026-06-24, **after-hours / 3:30 PM PT
  refresh** — the canonical post-close run leading the 4:00 PM PT trader run). **The
  marquee event landed: MU's Q3 FY26 print is OUT (AMC) and it is a record blowout** —
  rev **$41.46B**, non-GAAP EPS **$25.11** vs ~$20.20 (+24%); **Q4 guide ~$50.0B ±$1B at
  ~86% GM, EPS ~$31** (far above Street, sold-out HBM); stock **+12–15% AH. MU is a held
  long.** Two more held-name events: **AVGO** — Broadcom + OpenAI unveiled **"Jalapeño,"**
  OpenAI's first custom inference chip (built by Broadcom); **GOOGL** confirmed into the
  **DJIA effective Mon 6/29** + launched Gemini 3.5 Flash "Computer Use." Around them the
  two-day AI/semis de-rating **recovered** (risk-on; Russell 2000 record) and **oil fell
  below $70** on US-Iran de-escalation. **NOT HALT-WORTHY:** no FOMC; the held-name
  catalyst (MU) **resolved FAVORABLY** so there's nothing to halt for; the >2% move
  earlier in the week is recovering price action, not a geopolitical shock.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire run
  used `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3 -m quant_trading_system.cli`.
  Operator action still required (see open questions). **NB: `cd` into a news subdir
  earlier in the run broke the relative `.venv/bin/python3` path — always `cd` back to
  repo root (or use the absolute venv path) before CLI calls.**
- **Universe: 23-name, 23/23 claimed (unclaimed_count == 0), provisional_count 1.** SPCX
  still **PROVISIONAL / execution-quarantined** on equity_trend_following_ema_cross
  (revalidate_by **2026-07-04**; will NOT trade). `gap-registry coverage_holes` =
  **empty** (confirmed again). No claim changes available to the news agent.
- **Alpaca density: 182 items.** MU 24, NVDA 21, TSLA 21, AMZN 15, GOOGL 13, SPCX 13,
  CBRS 11, META 10, MSFT 10, INTC 7, AVGO 6, QQQ 6, AAPL 5, JPM 4, ORCL 4, MRVL 3, TSM 3,
  CSCO 1, SPY 3, NUVL 2; ARM/DELL/HPE 0. All 6 category HTMLs + daily summary written.
- **0 promotions Wed.** No Tier-A refresh (SNDK/CRDO/WDC/STX rode MU's coattails =
  theme/sympathy, not own catalysts; SNDK chain still rebuilding post-skip), no Tier-B
  qualifier (MU/CBRS in-universe; AVGO Jalapeño is on an in-universe name; KBH off-
  character; no FDA/M&A/3-bank cluster). Universe stays 23.

## Notable carry-forwards

- **MU — Q3 FY26 print OUT (6/24 AMC): RECORD BLOWOUT + big Q4 raise; +12–15% AH; held
  long.** Rev $41.46B, non-GAAP EPS $25.11 (+24% vs est), Q4 guide ~$50B/~86% GM/~$31 EPS.
  The pre-print ~14% implied + PUT hedging overwhelmed by upside. **THE trader task is the
  post-print reconciliation:** equity_event_driven_catalyst claims MU (true responder);
  held → entry guard skips; post-print window + trailing stop govern. **Thursday's run
  MUST cover Day-1 cash-session reaction** (does the gap-up hold? any analyst PT resets —
  drop those as opinions; cover only fresh events). Watch the trailing stop on a now-
  deeply-ITM position.
- **AVGO (held) — Broadcom + OpenAI "Jalapeño" custom inference chip.** OpenAI's first
  Intelligence Processor, built by AVGO; ~9-month design-to-tape-out; deploy end-2026,
  ramp 2027–28, gigawatt-scale. AVGO rose. Product/partnership event on a held name;
  equity_event_driven_catalyst claims AVGO but models earnings windows not product deals
  (partial gap). Track follow-through / any AVGO guidance read-through.
- **GOOGL → DJIA (effective pre-open Mon 6/29), replacing VZ.** Forced-flow/index event on
  an in-universe price-claimed name; Dow funds rebalance into GOOGL. Also launched Gemini
  3.5 Flash "Computer Use"; Reddit data-pricing talks. Index-rebalance library gap (joins
  SPCX→Nasdaq-100 ~July 1). Track index-flow commentary 6/26–6/29.
- **CBRS — debut-print Day-1 follow-through (−8% AH 6/23, slid again 6/24).** Needham
  reiterated Buy; analysts raised forecasts. No earnings-window strategy claims CBRS
  (assignment gap). Track Day-2 follow-through Thursday.
- **ORCL (held) — ~21,000 job cuts digestion; worst month since 2001.** Restructuring/cost
  event; event_driven claims ORCL but doesn't model restructuring (partial gap). Book's
  only red. Track any guidance read or stabilization.
- **AI memory supercycle — VALIDATED by MU.** MU's record print + ~86% GM guide rippled to
  SNDK/WDC/STX. Counter: SK Hynix targeting ~$29.4B Nasdaq ADR listing (supply +
  competing pure-play). Track whether the memory cohort sustains the MU read-through.
- **Custom-silicon arms race — Jalapeño (AVGO/OpenAI) + Anthropic/AWS Trainium.**
  Hyperscalers/labs diversifying off merchant GPUs → AVGO/AMZN tailwind, NVDA-moat
  question. Track further custom-ASIC / Trainium / Jalapeño-ramp news.
- **SPCX — $25B unsecured-notes raise (after $86B IPO); "battleground," analysts split
  (PROVISIONAL/quarantined).** Carry: $6.3B Reflection deal, Cathie Wood buying, Nasdaq-100
  add ~July 1. Stays quarantined (revalidate_by 7/04). Track price path + bond/equity
  divergence + Nasdaq-100 rebalance read-through.
- **TSLA — Sunrun/Renew Home 16-GW clean-energy pact (data-center power) + NHTSA FSD
  probe.** Partnership event + regulatory overhang. Track probe scope + energy-business
  follow-through.
- **AMZN — Nokia expands AWS collaboration (Autonomous Networks, L4); Anthropic-Trainium
  GPU-alternative framing.** Cloud-partnership cluster. Track further AWS/Trainium wins.
- **Oil < $70 / US-Iran de-escalation (60-day roadmap; Hormuz reopening).** Disinflationary,
  risk-positive. Track roadmap durability, oil path, whether the waiver is extended.
- **Hawkish Fed / higher-for-longer.** June 17 held 3.50–3.75% with hike-biased dots; Chair
  Warsh; Citadel Sept-hike call aligned; Fed stress-test results out 6/24. Track Fed
  speakers, CME FedWatch, next CPI/jobs.
- **VIX ~19.5 — crossed above 18 on the de-rating** (up from ~17.3 a week ago; first >3pt
  move this run), likely eased on the Wed rebound. Track whether index vol holds >18 or
  reverts; MU post-print IV crush.
- **INTC — foundry-turnaround leadership thread + Pelosi call-option disclosure (stale,
  5/29 fill).** No fresh discrete catalyst; rose ~3% on a technical signal. Track foundry
  customer wins.

## To do tomorrow (next news run, Thu 2026-06-25)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.**
   Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both
   require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3` FROM THE REPO ROOT** for all CLI calls. Bare `python3` WILL
   fail; a `cd` into a news subdir breaks the relative venv path.
3. **Universe should confirm 23** (23/23 claimed). **Cover SPCX** (per-symbol + a line);
   stays execution-quarantined until Sat research (revalidate_by 7/04).
4. **MU DAY-1 CASH REACTION — THE follow-up.** Printed Wed 6/24 AMC (record blowout +
   raise, +12–15% AH). Cover the Thursday cash-session move (does the gap-up hold/extend/
   fade) + held-position trailing-stop reconciliation. Drop analyst PT resets (opinions).
5. **AVGO Jalapeño follow-through** (held; OpenAI custom-chip win). Cover any analyst/
   guidance read-through; partial gap (event-driven claims AVGO but doesn't model product
   deals).
6. **CBRS Day-2 follow-through** (debut-print −8% AH 6/23, slid again 6/24). Assignment
   gap. Cover the cash-session reaction.
7. **GOOGL→DJIA (effective Mon 6/29).** Track index-flow commentary into 6/26–6/29; any
   further Gemini/product news.
8. **SPCX price path + bond/equity divergence + Nasdaq-100 rebalance (~July 1).** Stays
   quarantined. Cover any further notes/fundraise news.
9. **AI memory cohort** — does the MU read-through sustain SNDK/WDC/STX; SK Hynix listing
   progress. **Custom-silicon** — Jalapeño/Trainium follow-on.
10. **Oil/Iran + hawkish-Fed threads** — oil path, roadmap durability; Fed speakers,
    FedWatch, any CPI/jobs print.
11. **Vol regime** — VIX vs 18; MU post-print IV crush; whether the de-rating's vol bump
    persists or reverts.
12. **Promote candidates if Thu session refreshes (consecutive-session rule):**
    - **SNDK (SanDisk)** — strongest recurring candidate (memory/NAND supercycle). Rode
      MU's coattails Wed (sympathy, not own catalyst); chain still rebuilding post-skip
      (~session 2). Needs a clean 3-consecutive run OR a Tier-B catalyst (own beat+raise+5%,
      named contract, FDA, 3-bank cluster) to promote.
    - **CRDO (Credo)** — AI interconnect, $10B TAM; thematic watch.
    - **WDC / STX** — memory cohort, rode MU Wed (flow/sympathy). Watch only.
    - **WOLF / SMCI / QCOM** — flow-recurrence (not catalysts). Flow does NOT refresh the
      catalyst clock. Watch only.
13. **Outlier movers + sector breakdown.** Generic gainers/losers query still flaky
    (~18 consecutive sessions) — per-name reconstruction remains the workable path.
14. **Library gaps re-listing.** Reaffirmed Wed: earnings-window ASSIGNMENT on CBRS (now a
    Day-1 realized event); **product/partnership sub-trigger on event-driven covered names
    (AVGO Jalapeño — claimed-but-unmodeled, NEW this run; ORCL restructuring — partial)**;
    index-rebalance/forced-flow (GOOGL→DJIA 6/29 + SPCX→Nasdaq-100 ~July 1 — TWO live);
    event-window on price-claimed names (GOOGL/TSLA/AMZN/META); macro_event_window (FOMC/
    oil/Iran, NEW_CATEGORY_NEEDED); AI-capex-financing/crowding overlay (NEW_CATEGORY_NEEDED,
    de-rating now RECOVERING); volatility_regime ACTIVATION (MU post-print IV crush =
    iron-condor/short-vol setup; was the long-straddle setup pre-print); m_a_arbitrage
    activation (NUVL). Sat research = next opportunity.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Prior runs showed a
  miss (6/22 skipped) and a double (6/23 09:55 + 15:40). Today (6/24) appears to be a
  single clean canonical 3:30 PT run. Asks stand: (a) stabilize the schedule / add a
  health-check alert on miss-or-double; (b) the `_load_news_brief()` staleness-guard — a
  stale brief should be rejected/down-weighted, not fed to strategies as live signal.
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working
  interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the
  scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install
  requirements into 3.14 / rebuild the venv), and pin python@3.13. **daily_news_prompt.md
  line ~31 still says "There is no virtualenv" — stale, contradicts reality; please
  update.**
- **Index-inclusion as a 6th Tier-B trigger? — TWO live instances (GOOGL→DJIA 6/29;
  SPCX→Nasdaq-100 ~July 1).** Both in-universe so promotion is moot, but the recurring
  forced-flow gap argues for either a 6th Tier-B trigger or an index-rebalance overlay.
- **Event-driven strategy scope — product/partnership + restructuring sub-triggers.** AVGO
  (Jalapeño, 6/24) and ORCL (21k cuts) are BOTH claimed by equity_event_driven_catalyst
  yet neither event type is modeled (only earnings windows). Sat research: decide whether
  to broaden the event-driven strategy or add an event-window overlay.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** SPCX is the first live
  provisional claim (revalidate_by 2026-07-04). Confirm permanent.
- **CBRS earnings-window assignment.** CBRS (debut print 6/23, slid again 6/24) is claimed
  only by price-driven trend-following; no earnings-window strategy claims it. Sat
  research: head-to-head CBRS vs equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is a judgment
  call; the skipped Monday + the doubled 6/23 muddy SNDK's recurrence chain. A mechanical
  counter that handles skipped/duplicate sessions would clarify the clock.
- **`cli open-orders` parser bug (carry-forward).** Clean JSON on recent runs; stays
  provisionally closed. Confirm on a live open order.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate
  across days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by
  trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **182 items** cleanly (via venv).
  ARM/DELL/HPE had 0.
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-06-25T09:30:00-04:00`,
  `now_iso: 2026-06-24T15:39 PT` (post-close run).
- WebSearch strong Wed: MU Q3 results (StockTitan/Investing.com/Benzinga — rev $41.46B,
  EPS $25.11, Q4 guide ~$50B/~86% GM, +12–15% AH); Broadcom/OpenAI "Jalapeño" (CNBC/
  Broadcom IR/TechCrunch); oil < $70 + Iran 60-day roadmap (CNBC/TradingEconomics);
  rebound/Russell-2000 record (TheStreet/Schwab); VIX ~19.5 (CBOE/Yahoo).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (micro-cap noise
  INHD/CAST) — per-name reconstruction stays the path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** SNDK/CRDO/WDC/STX thematic or MU-sympathy only; SNDK chain still
    rebuilding. None qualify.
  - **Tier B:** No qualifiers. MU/CBRS in-universe; AVGO Jalapeño is an in-universe-name
    win (#5 n/a); no NEW M&A target (#1), no FDA binary (#2), no NEW beat+raise+5% (#3 —
    KBH off-character), no 3-bank cluster (#4).
  - **Decision: 0 promotions. Universe stays at 23.**
- **`gap-registry coverage_holes` empty (confirmed)** — vol-regime + index-rebalance are
  ACTIVATION/taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/import-price/retail-sales <month> <year>" query format
  works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name
  search is cleanest.
