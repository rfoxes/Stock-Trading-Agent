# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Tue 2026-06-23, live session, `market-status
  is_open:true`, next open Wed 6/24 09:30 ET). **First fresh brief since 6/19 — the
  Monday 6/22 news run was SKIPPED** (trader flagged a stale 6/19 brief and ran on
  broker state only; see open questions). Heavy, risk-off tape (**161 Alpaca items**
  vs 52 holiday Fri). Dominant story: **AI / semiconductor / memory DE-RATING in
  motion** — KOSPI −10% (circuit breakers x2; SK Hynix & Samsung −12%, Kioxia −15%);
  Wall Street tech −1.3% Mon; Nasdaq futures −2.4% Tue. Marquee held/watch items:
  **MU prints Wed 6/24 AMC (~14% implied move)** + announced a **strategic Anthropic
  deal** (Series H investment + memory supply); **ORCL disclosed ~21,000 job cuts**;
  **GOOGL −6% on a DeepMind departure**; **CBRS (Cerebras) first-ever public earnings
  Tue 6/23 AMC**; **MSFT–Chevron 20-yr 2.67 GW power deal**; **META $900M CRED
  investment + new WhatsApp head**; **TSLA NHTSA FSD probe**; **SPCX −30% from high +
  $20B debt raise + $6.3B Reflection deal**. **NOT HALT-WORTHY** (no FOMC this
  session; MU prints tomorrow not tonight; the >2% futures move is a tech de-rating
  not a geopolitical shock).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire
  run used `.venv/bin/python3 -m quant_trading_system.cli`. Operator action still
  required (see open questions). Use `.venv/bin/python3` + `cd /Users/rfoxes/Stock-Trading-Agent &&`.
- **Universe: 23-name, 23/23 claimed (unclaimed_count == 0), provisional_count 1.**
  SPCX still **PROVISIONAL / execution-quarantined** on equity_trend_following_ema_cross
  (revalidate_by **2026-07-04**; will NOT trade). `gap-registry coverage_holes` =
  **empty** (confirmed again). No claim changes available to the news agent.
- **Alpaca density: 161 items.** SPCX 30, MU 16, NVDA 15, TSLA 15, AMZN 14, GOOGL 12,
  META 12, MSFT 12, QQQ 6, AAPL 5, SPY 5, INTC 4, CBRS 3, TSM 3, AVGO 2, DELL 2,
  MRVL 2, ORCL 2, ARM 1; CSCO/HPE/JPM/NUVL 0. All 6 category HTMLs + daily summary
  written.
- **Held set (per 6/22 trader handoff, unchanged):** AAPL 72, AVGO 26, MU 7, ORCL 38,
  QQQ 28, SPY 35. Active set 7 strategies. (Book $108,940.77 on 6/22; MU running ~+25%.)
- **0 promotions Tue.** No Tier-A refresh (SNDK chain broken by skipped Monday; CRDO
  thematic only), no Tier-B qualifier (no FDA, no beat+raise+5% yet, no 3-bank
  cluster, no NEW-symbol M&A target or Tier-1 win). Universe stays 23.

## Notable carry-forwards

- **MU — Q3 FY26 print Wed 6/24 AMC; ~14% implied move; held long (~+25%).** Fresh
  **Anthropic strategic deal** (Series H investment + memory/storage supply, enterprise
  Claude) announced 6/22 — tailwind. Cross-current: **SK Hynix slowing HBM4 / shifting
  to conventional DRAM** (DRAM margins > HBM) — mixed memory read-through. Unusual PUT
  activity into the print (hedging). **Watch the trailing stop.** Tomorrow's run MUST
  cover the post-print reaction (beat/miss, guidance, Day-1 move) — this is THE event.
- **CBRS (Cerebras) — first-ever public earnings Tue 6/23 AMC.** No earnings-window
  strategy claims CBRS (assignment gap). Cover the post-print reaction Wed.
- **ORCL (held) — ~21,000 job cuts (≈13% workforce) per annual filing.** Restructuring/
  cost event; event_driven claims ORCL but doesn't model restructuring (partial gap).
  Track follow-through / any guidance read.
- **GOOGL — DeepMind departure (−6% Mon).** Senior-talent exit, proximate hyperscaler
  selloff driver. Track whether more departures / org changes follow.
- **AI / semis / memory DE-RATING.** KOSPI −10%, global chip rout, AI-capex
  profitability fears (Dan Niles cutting Mag7), hawkish Fed. The "most-crowded-trade"
  is unwinding. Track whether the de-rating reaches the trader's trend/momentum rules
  via realized price; watch execute output.
- **SPCX — drawdown deepens (−30% from post-IPO high).** New: **$20B debt raise**
  (bond investors lent despite equity rout) + **$6.3B Reflection AI-compute deal**
  (Colossus tenant); Cathie Wood bought the dip; 14-month unlock chatter. Stays
  quarantined (revalidate_by 7/04). Track price path + bond/equity divergence.
- **MSFT — Chevron 20-yr 2.67 GW power deal.** AI-capacity capital allocation. Track
  further power/energy deals across hyperscalers (AI-capex-financing theme).
- **META — $900M CRED investment + Kunal Shah to lead WhatsApp.** Fintech/payments
  push + leadership change. Track integration / further India fintech moves.
- **TSLA — NHTSA FSD probe (fatal Texas crash) + Megapod trademark.** Regulatory
  overhang; track probe scope. Megapod = modular AI infra (soft).
- **Hawkish Fed / higher-for-longer.** June 17 held 3.50–3.75% with hike-biased dots
  (9 see ≥1 hike, 6 see ≥2; PCE 3.6% YE; May CPI 4.2%); Chair Warsh; Citadel Sept-hike
  call now aligned. Track Fed speakers, CME FedWatch, next CPI/jobs.
- **US-Iran oil waiver — RESOLVED (live).** 60-day Treasury license for Iranian oil
  (Hormuz transit + IAEA in return); oil-supply-positive. Track Hormuz durability,
  oil path, whether the waiver is extended at day-60.
- **VIX ~17.3 — still low-vol (<18).** Up ~0.9 pt from 6/18's 16.40; no 3-pt move.
  Vol dislocation is single-name/sector (MU ~14% pre-print IV), not the index. Track
  VIX direction post-MU-print and whether the de-rating lifts the index VIX.
- **INTC — foundry leadership thread (Seok-Hee Lee hire).** No fresh event Tue (−8% on
  the broad rout). Track foundry follow-through / customer wins.
- **DELL — PowerEdge XE8812 server launch.** Product event; track demand signal.

## To do tomorrow (next news run, Wed 2026-06-24)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every
   run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap).
   Both require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 23** (23/23 claimed). **Cover SPCX** (per-symbol + a line);
   it stays execution-quarantined until Sat research (revalidate_by 7/04).
4. **MU PRINT IS WED 6/24 AMC — this is the day.** Pre-print refresh in the afternoon
   run (the print lands ~AMC, possibly after the news run; if pre-print, cover the
   setup; if results are out, cover beat/miss/guidance/Day-1 move). Held long. THE event.
5. **CBRS post-print reaction (printed Tue 6/23 AMC).** First public result — beat/miss,
   guidance, reaction. Assignment gap (no earnings-window claim).
6. **AI/semis/memory de-rating — did it continue or stabilize?** KOSPI follow-through,
   US tech tape, whether trend/momentum rules' execute output changes. Crowding unwind.
7. **ORCL job-cuts follow-through / GOOGL DeepMind-departure follow-on.** Any guidance
   or further org news.
8. **SPCX price path + bond/equity divergence** ($20B debt raise vs −30% equity). Stays
   quarantined. QQQ-rebalance size read-through (Nasdaq-100 ~July 1).
9. **Hawkish-Fed thread** — Fed speakers, FedWatch, any CPI/jobs print. Higher-for-longer.
10. **US-Iran oil waiver** — oil path, Hormuz durability.
11. **Vol regime** — VIX post-MU-print; whether the de-rating lifts index vol above 18.
12. **Promote candidates if Wed session refreshes (consecutive-session rule):**
    - **SNDK (SanDisk)** — strongest recurring candidate (memory/NAND supercycle, "next
      AI trade"). Theme, not a confirmed catalyst. **Recurrence: Fri (watch) + Tue
      (watch) = 2, NON-consecutive (Mon brief skipped).** If it refreshes Wed = 2
      consecutive; needs 3 for Tier A. Promote immediately on a confirmed Tier-B
      catalyst (beat+raise+5%, named contract, FDA, or 3-bank cluster).
    - **CRDO (Credo)** — AI interconnect, $10B TAM; session-1 thematic watch.
    - **WOLF / SMCI / QCOM** — flow-recurrence (not catalysts). Flow does NOT refresh
      the catalyst clock. Watch only.
13. **Outlier movers + sector breakdown.** Generic gainers/losers query still flaky
    (~16 consecutive sessions) — per-name reconstruction remains the workable path.
14. **Library gaps re-listing.** Reaffirmed Tue: event-window on price-claimed names
    (GOOGL/META/MSFT/TSLA/DELL/AAPL); earnings-window ASSIGNMENT on CBRS; restructuring
    sub-trigger (ORCL job cuts, partial gap); index-rebalance/forced-flow (SPCX→QQQ
    ~July 1); macro_event_window (FOMC, NEW_CATEGORY_NEEDED); **AI-capex-financing/
    crowding overlay (NEW_CATEGORY_NEEDED) — now ACTIVE/unwinding**; volatility_regime
    ACTIVATION (MU pre-print = textbook long-straddle setup); m_a_arbitrage activation
    (NUVL). Sat research = next opportunity.

## Open questions for the operator

- **[HIGH] News pipeline SKIPPED the Monday 6/22 run — and bare `python3` still broken.**
  No fresh 6/22 brief was produced; the trader ran on the stale 6/19 brief (caught it
  by date-check, proceeded without live signal per the manual). This run (6/23)
  restored a fresh brief. Two asks: (a) fix the news-agent Monday run / add a
  health-check alert on news-agent failure; (b) the `_load_news_brief()` staleness-
  guard is now urgent — a stale brief should be rejected/down-weighted, not fed to
  strategies as live signal. **Root cause likely the interpreter:** bare `python3` =
  Homebrew 3.14.5, lacks harness deps. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-
  task launcher + daily_news_prompt.md to the venv python (or pip-install requirements
  into 3.14 / rebuild the venv), and pin python@3.13. **daily_news_prompt.md line ~31
  still says "There is no virtualenv" — stale, contradicts reality; please update.**
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** SPCX is the first live
  provisional claim (revalidate_by 2026-07-04). Confirm permanent.
- **News-brief / trader-schedule timing.** Fresh briefs 6/16–6/19 on schedule, **6/22
  MISSED**, 6/23 restored. 3:30 PM PT news run should lead the 4:00 PM PT trader run by
  30 min. Monitor whether the Monday miss recurs.
- **FLEX/MRVL index-inclusion not among the 5 Tier-B triggers (carry-forward).** Should
  index-inclusion become a 6th Tier-B trigger?
- **CBRS earnings-window assignment.** CBRS (first public print 6/23) is claimed only by
  price-driven trend-following; no earnings-window strategy claims it. Sat research:
  head-to-head CBRS vs equity_event_driven_catalyst.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is still a
  judgment call. Note: the skipped Monday brief broke SNDK's recurrence chain — a
  mechanical counter would clarify whether a skipped session breaks or pauses the clock.
- **`cli open-orders` parser bug (carry-forward).** Clean JSON on recent runs; stays
  provisionally closed. Confirm on a live open order.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers
  accumulate across days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by
  trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **161 items** cleanly (via venv).
  CSCO/HPE/JPM/NUVL had 0. (Heavy — live risk-off session.)
- `cli market-status` → `is_open: true`, `next_open_iso: 2026-06-24T09:30:00-04:00`.
- WebSearch strong Tue: VIX ~17.3 (Yahoo/Macrotrends); KOSPI −10% cause + SK Hynix
  HBM4-slowdown (IndexBox/TradingKey/HDFCSky); Fed June-17 hold + hawkish dots
  (Federal Reserve/Advisor Perspectives/Schwab); Iran 60-day oil waiver (Treasury/NPR/
  Wash Examiner); Micron-Anthropic Series H + supply (Micron IR/GlobeNewswire/
  StockTitan); MU ~14% expected move + unusual puts (Benzinga/Barchart).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (~16 consecutive
  sessions) — per-name reconstruction stays the path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** SNDK recurs (theme, not catalyst) but chain broken by skipped Monday
    (Fri + Tue = 2, non-consecutive); CRDO session-1. None qualify.
  - **Tier B:** No qualifiers. #1 no NEW-symbol tradeable M&A target (CRED/Anysphere/
    Reflection private; Micron/Meta/SpaceX acquirers or in-universe); #2 no FDA binary;
    #3 no beat+raise+5% yet (MU/CBRS print Wed/tonight); #4 no 3-bank cluster; #5 the
    Anthropic/Reflection deals are on in-universe names.
  - **Decision: 0 promotions. Universe stays at 23.**
- **`gap-registry coverage_holes` empty (confirmed)** — tag vol-regime as an ACTIVATION
  gap, not a registry hole.
- Previous notes (still held): "CPI/import-price/retail-sales <month> <year>" query
  format works; per-name reconstruction beats generic gainers/losers; major-M&A →
  target per-name search is cleanest.
