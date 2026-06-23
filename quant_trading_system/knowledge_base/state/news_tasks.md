# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Tue 2026-06-23, **after-hours / 3:30 PM PT
  refresh** — the canonical post-close run, leading the 4:00 PM PT trader run). NOTE: a
  SECOND 6/23 news run occurred this morning (~09:55) that wrote the first 6/23 brief +
  category files; **this 15:40 PT run refreshed them** with two post-close events the
  morning run could not see. The **AI/semis/memory de-rating continued into the close**
  (S&P −1.44% / 7,365; Nasdaq −2.21% / 25,587; **Dow ~flat −0.09%** on a defensive
  rotation — PSA/IBM/ACN/WMT/PG/JNJ green). New since AM: **(1) CBRS printed its first
  public quarter** — rev $193.4M (+94% y/y, big beat), FY26 core-rev guide $855–865M
  (+69%), OpenAI 750MW/$20B + AWS deals, **but −8% AH on a gross-margin guide-down**;
  **(2) GOOGL replaces VZ in the DJIA, effective Mon 6/29** (forced-flow/index event).
  **NOT HALT-WORTHY** (no FOMC this session; MU prints **tomorrow** Wed 6/24 AMC not
  tonight; CBRS is not held; the >2% move is a tech de-rating not a geopolitical shock).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire run
  used `.venv/bin/python3 -m quant_trading_system.cli`. Operator action still required
  (see open questions). Use `cd /Users/rfoxes/Stock-Trading-Agent && .venv/bin/python3`.
- **Universe: 23-name, 23/23 claimed (unclaimed_count == 0), provisional_count 1.** SPCX
  still **PROVISIONAL / execution-quarantined** on equity_trend_following_ema_cross
  (revalidate_by **2026-07-04**; will NOT trade). `gap-registry coverage_holes` =
  **empty** (confirmed again). No claim changes available to the news agent.
- **Alpaca density: 153 items.** SPCX 28, MU 18, NVDA 15, TSLA 15, GOOGL 11, AMZN 9,
  MSFT 8, META 7, QQQ 7, CBRS 6, MRVL 6, INTC 5, AAPL 4, SPY 4, ARM 2, AVGO 2, ORCL 2,
  TSM 2, DELL 1; CSCO/HPE/JPM/NUVL 0. All 6 category HTMLs + daily summary refreshed.
- **Held set (per 6/23 trader handoff):** AAPL 72, AVGO 26, MU 7, ORCL 38, QQQ 28,
  SPY 35. Active set 7 strategies. Book equity ~$106,488 on 6/23 (−$2.5K vs 6/22 on the
  de-rating; MU gave back +25%→+7.6%, trailing stop held; ORCL −6.33%, book's only red).
- **0 promotions Tue.** No Tier-A refresh (SNDK/CRDO thematic; SNDK chain still broken by
  skipped Monday), no Tier-B qualifier (**CBRS failed #3: beat+raise but −8%, not +5%**;
  CBRS's OpenAI/AWS wins are on an in-universe name; no FDA, no 3-bank cluster, no NEW-
  symbol M&A target). Universe stays 23.

## Notable carry-forwards

- **MU — Q3 FY26 print Wed 6/24 AMC; ~14% implied move; held long (~+7.6%, was +25%).**
  Anthropic strategic deal (Series H + memory/storage supply) = tailwind; SK Hynix HBM4-
  slowdown / DRAM reallocation = mixed cross-current. Unusual PUT activity into the print
  (hedging). **Watch the trailing stop.** Tomorrow's run (Wed) MUST cover the post-print
  reaction (beat/miss, guidance, Day-1 move) — **THE event of the week.** The print may
  land at/after the 3:30 PT news run; if pre-print, cover the setup; if out, cover it.
- **CBRS (Cerebras) — FIRST public print is OUT (6/23 AMC): −8% AH despite a 94% rev
  beat.** Rev $193.4M; FY26 core-rev guide $855–865M (+69%); OpenAI 750MW/$20B + AWS
  inference deals; the −8% was a **gross-margin guide-down**. No earnings-window strategy
  claims CBRS (assignment gap). Track Day-1 (Wed) follow-through.
- **GOOGL → DJIA (effective pre-open Mon 6/29), replacing VZ.** Forced-flow/index event
  on an in-universe price-claimed name; Dow funds rebalance into GOOGL. Index-rebalance
  library gap (joins SPCX→Nasdaq-100 ~July 1). Also: DeepMind-departure follow-on (−6%
  Mon) — track further org changes.
- **ORCL (held) — ~21,000 job cuts (≈13% workforce) per annual filing.** Restructuring/
  cost event; event_driven claims ORCL but doesn't model restructuring (partial gap).
  Book's only red (−6.33%). Track follow-through / any guidance read.
- **AI / semis / memory DE-RATING — now Day 2.** KOSPI −10% overnight → Nasdaq −2.21%
  Tuesday; defensive rotation kept the Dow flat. "Most-crowded-trade" unwind continues.
  Track whether it extends Wed or stabilizes, and whether it reaches the trader's
  trend/momentum rules via realized price; watch execute output.
- **SPCX — drawdown ~−30% from high (PROVISIONAL/quarantined).** $20B debt raise + $6.3B
  Reflection deal + ~850k Robinhood IPO orders; Cathie Wood bought the dip; Susquehanna
  Neutral. Stays quarantined (revalidate_by 7/04). Track price path + bond/equity
  divergence + Nasdaq-100 rebalance (~July 1) read-through.
- **MSFT — Chevron 20-yr 2.67 GW power deal.** AI-capacity capital allocation. Track
  further hyperscaler power/energy deals (AI-capex-financing theme).
- **META — $900M CRED investment + Kunal Shah to lead WhatsApp.** Fintech/payments push +
  leadership change. Track integration / further India fintech moves.
- **TSLA — NHTSA FSD probe (fatal Texas crash) + Megapod trademark.** Regulatory
  overhang; track probe scope.
- **Hawkish Fed / higher-for-longer.** June 17 held 3.50–3.75% with hike-biased dots;
  Chair Warsh; Citadel Sept-hike call aligned; BofA rate-hike note cited Tuesday. Track
  Fed speakers, CME FedWatch, next CPI/jobs.
- **US-Iran oil waiver — RESOLVED (live).** 60-day Treasury license for Iranian oil
  (Hormuz transit + IAEA). Oil-supply-positive. Track Hormuz durability, oil path,
  whether the waiver is extended at day-60.
- **VIX ~17.3 — still low-vol (<18).** No 3-pt move. Vol dislocation is single-name/
  sector (MU ~14% pre-print IV; CBRS realized ~−8%), not the index. Track VIX direction
  post-MU-print and whether the de-rating lifts index vol above 18.
- **INTC — foundry leadership thread (Seok-Hee Lee hire).** No fresh event Tue (fell on
  the rout). Track foundry follow-through / customer wins.
- **DELL — PowerEdge XE8812 server launch.** Product event; track demand signal.

## To do tomorrow (next news run, Wed 2026-06-24)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every
   run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap).
   Both require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 23** (23/23 claimed). **Cover SPCX** (per-symbol + a line);
   stays execution-quarantined until Sat research (revalidate_by 7/04).
4. **MU PRINT IS WED 6/24 AMC — THE day.** Pre-print refresh in the afternoon run; the
   print lands ~AMC (possibly after the news run). If pre-print, cover the setup; if out,
   cover beat/miss/guidance/Day-1 move + trailing-stop reconciliation. Held long.
5. **CBRS Day-1 follow-through** (printed Tue −8% AH on a margin guide-down despite a 94%
   rev beat). Assignment gap (no earnings-window claim). Cover the cash-session reaction.
6. **AI/semis/memory de-rating — Day 3? Continued or stabilized?** KOSPI follow-through,
   US tech tape, whether trend/momentum rules' execute output changes. Crowding unwind.
7. **GOOGL→DJIA (effective Mon 6/29) + ORCL job-cuts / GOOGL DeepMind follow-on.** Track
   any index-flow commentary and further org news.
8. **SPCX price path + bond/equity divergence + Nasdaq-100 rebalance (~July 1).** Stays
   quarantined.
9. **Hawkish-Fed thread** — Fed speakers, FedWatch, any CPI/jobs print. Higher-for-longer.
10. **US-Iran oil waiver** — oil path, Hormuz durability.
11. **Vol regime** — VIX post-MU-print; whether the de-rating lifts index vol above 18.
12. **Promote candidates if Wed session refreshes (consecutive-session rule):**
    - **SNDK (SanDisk)** — strongest recurring candidate (memory/NAND supercycle, "next
      AI trade"). Theme, not a confirmed catalyst. Chain still broken by the skipped
      Monday; needs a clean 3-consecutive run or a Tier-B catalyst (beat+raise+5%, named
      contract, FDA, 3-bank cluster) to promote.
    - **CRDO (Credo)** — AI interconnect, $10B TAM; thematic watch.
    - **WOLF / SMCI / QCOM** — flow-recurrence (not catalysts). Flow does NOT refresh the
      catalyst clock. Watch only.
13. **Outlier movers + sector breakdown.** Generic gainers/losers query still flaky
    (~17 consecutive sessions) — per-name reconstruction remains the workable path.
14. **Library gaps re-listing.** Reaffirmed Tue: earnings-window ASSIGNMENT on CBRS (NOW
    a realized −8% event); **index-rebalance/forced-flow (GOOGL→DJIA 6/29 + SPCX→
    Nasdaq-100 ~July 1) — TWO live instances**; event-window on price-claimed names
    (GOOGL/META/MSFT/TSLA/DELL/AAPL); restructuring sub-trigger (ORCL, partial gap);
    macro_event_window (FOMC, NEW_CATEGORY_NEEDED); AI-capex-financing/crowding overlay
    (NEW_CATEGORY_NEEDED, ACTIVE/unwinding); volatility_regime ACTIVATION (MU pre-print =
    textbook long-straddle setup); m_a_arbitrage activation (NUVL). Sat research = next
    opportunity.

## Open questions for the operator

- **[HIGH] Two news runs fired on 6/23 (09:55 + 15:40); the 15:40 was the canonical
  3:30 PM PT run.** Earlier (6/22) the Monday run was SKIPPED entirely. The schedule is
  intermittent in both directions (a miss on 6/22, a double on 6/23). Two asks:
  (a) stabilize the news-agent schedule / add a health-check alert on miss-or-double;
  (b) the `_load_news_brief()` staleness-guard remains urgent — a stale brief should be
  rejected/down-weighted, not fed to strategies as live signal.
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working
  interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the
  scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install
  requirements into 3.14 / rebuild the venv), and pin python@3.13. **daily_news_prompt.md
  line ~31 still says "There is no virtualenv" — stale, contradicts reality; please
  update.**
- **Index-inclusion as a 6th Tier-B trigger? — now TWO live instances (GOOGL→DJIA 6/29;
  SPCX→Nasdaq-100 ~July 1).** Both are in-universe so promotion is moot, but the recurring
  forced-flow gap argues for either a 6th Tier-B trigger or an index-rebalance overlay.
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** SPCX is the first live
  provisional claim (revalidate_by 2026-07-04). Confirm permanent.
- **CBRS earnings-window assignment.** CBRS (first public print 6/23, −8% AH) is claimed
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

- `cli news-fetch --lookback-hours 24` returned **153 items** cleanly (via venv).
  CSCO/HPE/JPM/NUVL had 0.
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-06-24T09:30:00-04:00`,
  `now_iso: 2026-06-23T15:39 PT` (post-close run).
- WebSearch strong Tue: CBRS Q1 results (SEC 8-K/StockTitan/CNBC — rev $193.4M +94%,
  FY26 guide $855–865M, OpenAI 750MW/$20B + AWS, −8% AH on margin); GOOGL→DJIA effective
  6/29 (S&P DJI press/CNBC/Benzinga); 6/23 close + defensive rotation (TheStreet/Schwab);
  VIX ~17.3 (FRED/Investing). 
- WebSearch weak: generic "biggest gainers/losers" still screen-level — per-name
  reconstruction stays the path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** SNDK/CRDO thematic only; SNDK chain still broken. None qualify.
  - **Tier B:** No qualifiers. **#3 CBRS beat+raised but −8% AH (price test FAILED).**
    #1 no NEW-symbol tradeable M&A target; #2 no FDA binary; #4 no 3-bank cluster; #5
    CBRS's OpenAI/AWS wins are on an in-universe name.
  - **Decision: 0 promotions. Universe stays at 23.**
- **`gap-registry coverage_holes` empty (confirmed)** — vol-regime + index-rebalance are
  ACTIVATION/taxonomy gaps, not registry holes.
- Previous notes (still held): "CPI/import-price/retail-sales <month> <year>" query format
  works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name
  search is cleanest.
