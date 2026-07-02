# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**NEXT RUN IS MONDAY 2026-07-06, NOT Friday.** Markets are CLOSED Fri 7/3 (Independence Day observed; July 4 is a Saturday). The CLI `market-status` confirms `next_open 2026-07-06T09:30 ET`. There is **no shortened Friday session** this year — 7/3 is a full holiday. (This corrects the prior tasks.md note that called 7/3 "a shortened session.") The news agent may not run on the 7/3 holiday; if it does, it will find a stale tape — assess and stop.

---

## Status as of the last update

- **Last brief assessment:** NORMAL FLOW (Thu 2026-07-02, second H2 session, canonical post-close 3:30 PM PT run; last equity session before a 3-day weekend). **The day's shape: a dovish jobs miss + AI-chip give-back rotation** (Dow record vs SOXX's worst 2-day drop in over a year — PRICE ACTION we drop) over a real event cluster. Genuine new events: **June NFP +57k big miss** (UE fell to 4.2% on a participation slump to 61.5%, lowest since Mar 2021) — read dovishly; **TSLA Q2 deliveries 480,126 (+25%, blowout vs ~406k) but stock −7.5%** (worst day in ~a year; margins now the focus, July 22 earnings); **EU top court UPHELD GOOGL's €4.1B Android antitrust fine (final)**; **META cloud thesis broadened** (BofA/JPM $20B/Cramer); **NVDA launched its own startup cloud + rev-share**; **AMZN building its own AI chips (beyond QCOM)**; **AAPL ~55% hardware price hikes** (memory cost pass-through, +4%). **0 promotions. Universe stays 26.** **NOT HALT-WORTHY:** NFP digested (no FOMC; Fed on hold, Warsh no-signal at Sintra); TSLA/GOOGL/META events on price-claimed names; geopolitics risk-positive (US-Iran talks wrapped, oil 4-mo lows).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used
  `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3 -m quant_trading_system.cli`. Operator action still
  required (open questions). Always `cd` to repo root (or use the absolute venv path) before EVERY CLI call.
- **Universe: 26, unchanged.** No promotion (no Tier-A 3-session catalyst run; no clean Tier-B trigger; no operator
  directive). `list-active` → universe 26, claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**.
  `gap-registry coverage_holes` = **empty** (confirmed again).
- **Alpaca density: 141 items.** TSLA 19, META 17, NVDA 13, MU 11, AAPL 10, AMZN 10, MSFT 9, SPCX 9, GOOGL 6,
  SPY 6, INTC 5, JPM 5, QQQ 4, AVGO 3, QCOM 3, SNDK 3, ARM 2, ORCL 2, TSM 2, DELL 1, MRVL 1;
  CBRS/CSCO/HPE/NUVL/SYNA 0. All 6 category HTMLs + daily summary written.
- **Brief pipeline FRESH today** (7/1 + 6/30 were fresh too; earlier misses span 6/22, 6/25, 6/29). Staleness-guard
  ask still stands (open questions). **If the pipeline skips the 7/3 holiday and resumes 7/6, the 7/2 brief will be
  stale by Monday — the trader's staleness guard matters most across this long weekend.**

## Notable carry-forwards

- **TSLA — Q2 deliveries PRINTED (NEW): 480,126, +25% YoY, blowout vs ~406k, but stock −7.5%** (worst day in ~a
  year). Focus has shifted from volume to margins/per-unit economics → the binary is now the **July 22 earnings
  call** (full Q2 financials). NHTSA closed the 695k-vehicle braking probe (regulatory clear). Earnings-window
  responder does NOT claim TSLA (trend-following does) → assignment gap. **Track into the 7/22 print; IV builds.**
- **GOOGL — antitrust triple hit (NEW EU ruling).** EU's top court UPHELD the record €4.1B ($4.67B) Android fine,
  rejecting the final appeal — now a crystallized cost. Stacks on Wed's Klarna ~$1.97B + Yelp. Price-claimed, no
  responder. Track for DOJ search-remedy read-through / any further EU DMA action.
- **META — AI-cloud thesis broadened (NEW endorsements) + pending BUY 16 (7/1).** BofA Buy, JPMorgan ~$20B TAM,
  Cramer "worth $100/share"; stock +9% on 7/1. India raised WhatsApp-username cybercrime query (regulatory query,
  not action). The MACD-momentum BUY 16 (7/1) is a price entry, pending fill — trader reconciles. Track cloud
  capacity/capex confirmation + the 29-state addiction-trial calendar (carry).
- **NVDA — own startup cloud + revenue-sharing program (NEW business-line launch)** + NVDA/Corning ~3,000 jobs.
  Parallels Meta/AWS cloud pushes. Price-claimed, no responder. Track the cloud/compute-competition theme.
- **AMZN — building its own AI chips beyond Qualcomm (NEW vertical-integration signal)** + NJ employer Medicaid
  fees (minor policy). Price-claimed, no responder. QCOM competitive read-through (AMZN keeps using QCOM for now).
- **AAPL — ~55% hardware price hikes (NEW pricing/margin event)** as memory shortages pass through to consumers
  (inflation read-through); +4% bucking the chip rout. Price-claimed, no responder. Track whether other device
  makers follow + the margin/demand elasticity read at the next AAPL print.
- **JPM — Q2 earnings Tue July 14 (~$5.61/sh), now inside the 14-day options window.** Kicks off bank season.
  $50B buyback effective 7/1 (consummated). Earnings-window responder does NOT claim JPM (trend-following does)
  → assignment gap. **Flag IV build into 7/14.**
- **INTC — Q2 earnings July 23** (outside the 14-day window; flag as it approaches). Rebounded ~2%.
- **MU (held) — no fresh hard event; semi-rout IV crush continues; trailing stop still NOT fired (per 7/1 handoff).**
  $250M Trump Accounts + $200B US-investment (carry); two-sided options flow (bearish $1050 put sweep + neutral
  $1160 calls). Provisional/quarantined event-driven claim models earnings windows only. Watch trailing-stop scenario.
- **ORCL (held) — 21k-cut restructuring still weighs; no new event; no responder (book's deep-red name).**
- **AVGO (held) — no fresh single-name catalyst; semis 2-day rout (price).**
- **SPCX (PROVISIONAL/quarantined) — Nasdaq-100 add Tue July 7 (~$4.3B forced buying) + FCC satellite-licensing
  vote July 22 (tailwind). Musk denied a "SpaceX AI handheld" report ("utterly false"). revalidate_by 2026-07-04 —
  THIS SATURDAY.** If research/head-to-head hasn't revalidated by 7/04, it stays execution-quarantined. Track the
  price path into the 7/7 add.
- **SK Hynix — $29B Nasdaq listing ~July 10.** Memory-trade read-through (MU/SNDK). Post-listing universe-add
  candidate once it trades with a US ticker.
- **Memory cohort (MU, SNDK, WDC/STX) + SK Hynix build-up.** AAPL 55% price hikes = demand/pricing confirmation
  vs Chinese-supply risk (SNDK) + the DRAM legal tail (MU). Sustain check.
- **Cloud/compute-competition theme (NEW two-sided).** META cloud + NVDA startup cloud + AMZN own-chips + AWS $1B
  unit (carry) vs neoclouds (CRWV/NBIS, called oversold on the Meta threat). Recurring; no responder.
- **Input-cost / pricing-power theme (carry, two-sided).** AAPL passing memory cost (55% hikes) vs cloud raising
  AI-compute prices (AWS). Recurring; no responder.
- **Macro: dovish jobs miss + higher-for-longer paused.** June NFP +57k miss; UE 4.2% (participation-driven);
  Fed on hold (Warsh no-signal at Sintra). **US declined to renew the Mexico/Canada trade deal → review-period
  tariff risk (NEW policy watch).** Oil soft. Next major macro after the holiday: track the July CPI/PPI calendar
  + FedWatch into the late-July FOMC.
- **Vol regime — VIX ~16.59 (roughly flat vs 7/1's 16.45), normal contango, no inversion.** Index vol benign
  through NFP. Dispersion single-name (semis worst 2-day in a year; MU IV crush; TSLA event-IV into 7/22; SPCX
  into 7/7; JPM into 7/14). Track whether index vol stays benign across the long weekend.

## To do on the next run (Mon 2026-07-06 — or 7/3 if the pipeline fires on the holiday, in which case assess+stop)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A (3 consecutive
   catalyst sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require `--sector`.
2. **USE `.venv/bin/python3` AND `cd` TO THE REPO ROOT** for EVERY CLI call. Bare `python3` fails.
3. **Universe should confirm 26.** Check unclaimed 0 / provisional 3 (QCOM, SPCX, SYNA). **SPCX revalidate_by 7/04
   is THIS PAST SATURDAY by Monday — check whether Saturday research/head-to-head revalidated it or it's still
   execution-quarantined (and note SPCX joins the Nasdaq-100 Tue 7/7, the day after this run).**
4. **SPCX → Nasdaq-100 add is Tue 7/7** (~$4.3B forced passive buying) — Monday's run is the last news read before
   the add. Cover the price path + any last-minute index-methodology news.
5. **TSLA into the July 22 earnings call** — the delivery print is done; the margin/financials binary is 7/22.
   Track IV build; the earnings-window strategy doesn't claim TSLA (assignment gap).
6. **JPM Q2 earnings Tue 7/14** — inside the 14-day window by Monday; kicks off bank season. Flag IV build.
7. **GOOGL antitrust follow-through** — EU €4.1B upheld (final); watch DOJ search-remedy / EU DMA read-through +
   any Klarna appeal chatter.
8. **META cloud** — capacity/capex confirmation + the addiction-trial calendar; reconcile the 7/1 BUY 16 fill state.
9. **Memory cohort** (MU, SNDK, WDC/STX) + **SK Hynix listing ~7/10** — sustain check; AAPL price-hike read-through.
10. **US-Mexico-Canada trade-deal review (NEW policy watch)** — any tariff escalation over the long weekend.
11. **Vol regime** — VIX vs ~16–17 after the holiday; whether index vol stays benign; MU IV crush; event-IV
    (TSLA 7/22, SPCX 7/7, JPM 7/14).
12. **Promote candidates if Monday refreshes:**
    - **RIVN** — NEW session-1 candidate (Q2 delivery beat + raised FY26 guidance 65–70k + R2 launch, +8%). This is
      a DELIVERY beat-and-raise, NOT an earnings print → does not meet Tier-B #3 (earnings). Track recurrence;
      promote on its own earnings beat-and-raise+5% or a clean 3-session run. Consumer-discretionary sector.
    - **CRDO** — AI-interconnect; absent from today's feed → clock did NOT advance. Promote on a *fresh* same-week
      3-bank initiation cluster OR own beat-and-raise+5%.
    - **SK Hynix** — post-IPO add candidate once it trades (~7/10); not promotable until a US ticker.
    - **WDC / STX** — memory cohort, sympathy/flow. Promote only on a clean 3-consecutive catalyst run OR Tier-B.
    - **CRWV / NBIS** — neoclouds; sympathy to Meta's cloud entry (analysts call oversold), not own catalyst; watch.
    - **UHS / HCA** — hospital operators up on the CMS payment-rate proposal; outside the tech universe; operator note.
13. **Outlier movers + sector breakdown.** Generic gainers/losers query STILL screen-level (~23 consecutive
    sessions); per-name reconstruction remains the workable path. Today's clean non-universe catalysts: RIVN
    (delivery beat+raise), LCID (CFO change), UHS/HCA (CMS proposal), Nike (7/1 beat but China −12%).
14. **Library gaps re-listing.** Carry: delivery/earnings-window assignment (TSLA 7/22, JPM 7/14, INTC 7/23);
    regulatory/antitrust (GOOGL EU fine, META India/addiction); business-line launch (NVDA cloud, AMZN chips,
    META cloud); pricing/margin (AAPL hikes, NEW); capital-allocation (JPM buyback, MU Trump Accounts);
    restructuring (MSFT + ORCL); short-interest (NVDA/TSLA Burry); index-rebalance (SPCX 7/7, SK Hynix ~7/10);
    M&A-arb (SYNA/onsemi); macro/policy-event window (NFP, US-MX-CA trade-deal review; NEW_CATEGORY_NEEDED);
    vol-regime activation (MU IV crush). Sat research = next.

## Open questions for the operator

- **[HIGH] News-agent schedule stability + brief-staleness guard.** Earlier misses span 6/22, 6/25, 6/29; 6/30 +
  7/1 + 7/2 fresh. Asks stand: (a) stabilize the schedule / add a health-check alert on miss-or-double; (b) the
  `_load_news_brief()` staleness-guard — a stale brief should be rejected/down-weighted, not fed as live signal
  (parses date_in_file but never compares to today). **This matters most across the 7/3–7/6 long weekend, when the
  7/2 brief will be 4 calendar days old by the Monday trader run.**
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher +
  daily_news_prompt.md to the venv python (or pip-install requirements into 3.14 / rebuild the venv), and pin
  python@3.13. **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.**
- **Holiday-calendar note in prior tasks.md was WRONG.** It said "July 3 is a shortened session (early close)."
  In 2026, July 4 is a Saturday, so the holiday is observed Friday July 3 → NYSE is CLOSED July 3 (full holiday),
  confirmed by `market-status` next_open = 7/6. Fixed here. Consider adding a holiday-calendar sanity check.
- **Earnings/delivery-window assignment — TSLA (7/22), JPM (7/14, inside window), INTC (7/23), CBRS (carry).**
  Earnings-window responder (equity_event_driven_catalyst) does not claim these names (all price-driven). Sat:
  assign it. JPM is the most urgent (window opens by Monday).
- **Regulatory/antitrust event-window — live cluster (GOOGL EU €4.1B upheld + Klarna/Yelp; META India/addiction;
  MU DRAM carry; AAPL SCOTUS carry).** No rule reads a court/agency ruling. Sat research: litigation/regulatory
  event-window overlay for large-caps.
- **Business-line-launch sub-trigger — NVDA (startup cloud), AMZN (own chips), META (AI cloud), AWS ($1B unit).**
  No rule reads a strategic business-line announcement. Recurring; multi-name.
- **Pricing/margin-disclosure sub-trigger — AAPL (55% hikes).** No rule reads a pricing-power / input-cost event.
- **Restructuring/workforce-reduction event-window — MSFT + ORCL (carry).** Recurring big-tech class; no responder.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX→Nasdaq-100 7/7; SK Hynix ~7/10).** Recurring
  forced-flow gap argues for a 6th trigger or an overlay.
- **M&A-arb activation, live universe instance (SYNA / onsemi).** equity_pairs_trading_cointegration declares
  pairs_arbitrage but only provisionally claims SYNA. Sat: activate merger-arb (long SYNA / short ON at 1.350).
- **Capital-allocation / capital-return event-window (JPM $50B buyback; MU Trump Accounts).** No rule reads a
  buyback/dividend/pricing disclosure.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Three provisional claims live (QCOM, SPCX, SYNA);
  SPCX revalidate_by 7/04 (Sat) is this week's checkpoint.
- **CBRS earnings-window assignment.** CBRS claimed only by price-driven trend-following. Sat: head-to-head vs
  equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is a judgment call; a mechanical
  counter would clarify the clock (CRDO ambiguous case; RIVN new session-1; neither advanced/promoted).
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** Errors `'dict' object has no attribute 'id'` when a live
  open order exists (bit on the QQQ 6/30 + META 7/1 orders); clean when none. Fix the order-serialization path.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate across days. Run
  `bash scripts/install_git_safety.sh` if not installed. (Long weekend — watch for pile-up across 7/3–7/6.)
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim +
  m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **141 items** cleanly (via venv). CBRS/CSCO/HPE/NUVL/SYNA 0.
- `cli market-status` → `is_open: false`, **`next_open_iso: 2026-07-06T09:30:00-04:00`** (confirms 7/3 is a full
  holiday, not a shortened session), `now_iso: 2026-07-02T15:39 PT` (post-close run).
- `cli list-active` → universe 26, claimed 26, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA). `gap-registry
  coverage_holes` empty.
- WebSearch strong Thu: June NFP +57k / UE 4.2% / participation 61.5% (BLS/CNBC); VIX ~16.59 (Cboe/Yahoo); TSLA
  480,126 deliveries +25% / stock −7.5% (24-7 Wall St./CNBC); GOOGL EU €4.1B Android fine upheld (Benzinga);
  RIVN +8% delivery beat+raise (Motley Fool); CMS hospital-rate proposal → UHS/HCA (CNBC); US-MX-CA trade-deal
  non-renewal (TheStreet/CNBC).
- WebSearch weak: generic "biggest gainers/losers" still screen-level — per-name reconstruction stays the path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No candidate reached a clean 3-consecutive-catalyst run (CRDO absent → clock did not advance;
    RIVN is session 1; WDC/STX/CRWV/NBIS sympathy). **No Tier-A promotion.**
  - **Tier B:** No qualifier — no NEW confirmed M&A target (SYNA already in), no FDA binary, no *earnings*
    beat-and-raise+5% on a universe/candidate name (RIVN's is a DELIVERY beat-and-raise, not earnings; Nike beat
    but −3% / China −12%), no *fresh* same-week 3-bank initiation cluster, no candidate Tier-1 customer-win press
    release. **No Tier-B promotion.**
  - **Decision: 0 promotions. Universe stays 26.**
- **`gap-registry coverage_holes` empty (confirmed)** — regulatory, business-launch, pricing/margin, restructuring,
  cloud-competition, m_a_arbitrage, vol-regime, index-rebalance, capital-allocation, delivery/earnings-window are
  ACTIVATION/assignment/taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction
  beats generic gainers/losers; major-M&A → target per-name search is cleanest.
- **HOLIDAY NOTE (CORRECTED):** Fri July 3 is a FULL market holiday (Independence Day observed; July 4 = Saturday).
  NYSE closed 7/3; next full cash session Mon 7/6. There is NO shortened Friday session this year.
