# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Wed 2026-06-17, FOMC OUTCOME day). The
  **dot plot delivered a hawkish pivot** — Fed held 3.50-3.75% (12-0, ~97%
  priced) but the **median 2026 dot rose to 3.8% from 3.4% in March** (above the
  current range); **9/18 officials see ≥1 hike in 2026, 6 see two** — cuts→hikes.
  Warsh debut hawkish-by-omission (shorter statement, no forward guidance, 5 task
  forces, no own dot). **Retail sales +0.9%** (~2x consensus) reinforced it.
  Equities sold off (S&P -1.21%, Nasdaq Comp -1.34%); **VIX +12.37% to 18.44**
  (still sub-20). **Not HALT-WORTHY** — the decision is already in prices by the
  post-close run; the trader plans into 6/18 with the outcome known; no held name
  has a confirmed negative overnight catalyst; no futures gap >2%.
- **Interpreter:** bare `python3` still **BROKEN** (Homebrew 3.14, no deps). Entire
  run used `.venv/bin/python3 -m quant_trading_system.cli`. Operator action still
  required (see open questions). Use absolute paths / `cd /Users/rfoxes/Stock-Trading-Agent &&`.
- **Universe: 23-name, 23/23 claimed (unclaimed_count == 0), provisional_count 1.**
  SPCX confirmed still **PROVISIONAL / execution-quarantined** on
  equity_trend_following_ema_cross (revalidate_by 2026-06-30; it will NOT trade) —
  `list-active` Wed showed provisional_claims = [SPCX], sharpe null. Trader did NOT
  hand-promote it (correct). `gap-registry coverage_holes` = **empty** (confirmed).
- **Alpaca density (169 items total, vs 98 Tue):** SPCX 30, NVDA 18, META 16,
  GOOGL 14, AMZN 12, AAPL 9, MU 9, TSLA 9, MSFT 11, SPY 11, TSM 6, AVGO 5, QQQ 5,
  INTC 4, HPE 2, JPM 2, MRVL 2, ORCL 2, ARM 1, DELL 1; CBRS/CSCO/NUVL 0. Tape
  dominated by FOMC, the SpaceX/Elon complex, AI-memory demand, and AI-agent/
  ETF commentary. All 6 category HTMLs + daily summary written.
- **Held set (per 6/16 trader handoff, unchanged):** AAPL 72, AVGO 26, MU 7,
  ORCL 38, QQQ 28, SPY 35. Active set 7 strategies.
- **0 promotions Wed.** No Tier-A refresh, no Tier-B qualifier. Universe stays 23.

## Notable carry-forwards

- **FOMC AFTERMATH (Thu is Day-1 of the hawkish repricing).** Watch the AI-cohort
  multiple de-rate vs. the higher-for-longer dots; whether VIX holds sub-20 or
  pushes through; any Fed-speaker walk-back/clarification of the dot plot. The hot
  retail print + import print reinforce the hawkish read.
- **AAPL — Cook "100-year flood" memory-cost price-hike warning (held).** Real
  guidance/cost event; bullish read-through to MU, margin headwind for AAPL
  hardware. Track sell-side reaction + whether other hardware names echo it. Event
  on a price-claimed name → library gap.
- **MU Q3 FY26 = Tue 6/24 AMC (held long).** Pre-print window open: PT raises,
  bullish call flow, "could overtake Meta," same-day Cook-memory tailwind. Refresh
  IV expansion / UOA / sell-side daily into the print.
- **MRVL — Jensen "$2B AI-chip alliance" + "next trillion-dollar company" call
  (+3%); S&P 500 inclusion 6/22.** On-character for equity_breakout_volume_confirmation
  IF volume-confirmed. Track follow-through + the 6/22 passive-flow window (with FLEX).
- **HPE — NVIDIA/Vultr AI-cloud partnership (+4%).** Partnership event on a
  divergence-claimed name → library gap. Track follow-through.
- **META — Zuckerberg now backs KOSA (regulatory reversal); TikTok FL suit; OpenAI
  multi-state probe.** Platform-regulation risk broadening. Event on a momentum-
  claimed name → library gap. Track legislative movement.
- **NVDA — Trump admin held off blacklisting DeepSeek + 100+ Chinese firms.**
  Marginal export-control de-escalation; track whether it firms or reverses +
  China-substitution thread.
- **AI-capex = financing/leverage + permitting story.** "$4.1T AI-debt" + $130B
  data-center-permitting backlash, now COMPOUNDED by a higher-for-longer Fed
  (costlier leverage). Track cohort de-rating on financing/permitting risk.
- **SPCX → QQQ Nasdaq-100 fast-entry inclusion (~July 1) + Russell (6/26).** Track
  the confirmed add date + estimated $22-27B forced flow reweighting held QQQ's
  constituents daily through ~July 1. SPY excluded (S&P GAAP rule). Don't bury this
  real universe read-through under the Musk-flow/meme noise. SPCX options debut set
  a record (1.8M contracts/$2.8B premium); Aug IPO lock-up release is the next
  structural date (Sept &lt;$205 hedge already on).
- **US-Iran deal signing Fri 6/19 Geneva.** Hormuz reopens Fri; oil ~$76 (March
  lows). Track durability (Israel-Lebanon), oil direction into the weekend.
- **Anthropic Fable 5 / Mythos 5 export ban (Day 5-6).** WH/Commerce negotiations +
  security-veteran open letter. Track: (a) does it return (Polymarket ~71% /
  Kalshi ~68% by July 1), (b) NVDA-China spillover, (c) EU sovereign-AI response.
- **VIX 18.44 (+12.37%), sub-20.** volatility_regime is an ACTIVATION gap
  (responders exist, none active / none claim a universe symbol). Track whether the
  hawkish dots keep IV elevated or it fades back sub-17.

## To do tomorrow (next news run, Thu 2026-06-18)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every
   run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap).
   Both require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 23** (23/23 claimed). **Cover SPCX** (per-symbol + a
   line); it stays execution-quarantined until Sat research (revalidate_by 6/30).
4. **FOMC AFTERMATH — Day-1 of the hawkish repricing.** Report Fed-speaker
   reactions/walk-backs, AI-cohort multiple de-rating, VIX path, rate-cut-odds
   repricing (CME FedWatch). Highest-priority macro item.
5. **MU pre-print Day-N (6/24 AMC).** Sell-side / UOA / IV refresh. Held long.
6. **AAPL Cook memory-price-hike follow-through.** Sell-side margin/demand reaction;
   does the hardware cohort echo it? MU read-through.
7. **MRVL Jensen-alliance follow-through + 6/22 S&P 500 inclusion (with FLEX)**
   passive-flow window — track all week.
8. **HPE/NVIDIA partnership + META KOSA reversal** follow-through.
9. **AI-capex financing/permitting + higher-for-longer compounding.** Any de-rating?
10. **US-Iran signing Fri 6/19** durability; oil; Hormuz reopening; Israel-Lebanon.
11. **Anthropic export-ban Day-N.** Did models return (July-1 prediction date)?
    NVDA-China spillover? DeepSeek-blacklist-delay firming or reversing?
12. **Vol regime Thu.** Did VIX hold above 18 / push sub-17? VIX9D vs VIX.
    Activation gap on volatility_regime.
13. **Promote candidates if Thu session refreshes (consecutive-session rule):**
    - **QURE / BHVN** — biotech binary movers Wed (QURE +75.6%, BHVN +14.8%);
      catalyst TYPE unconfirmed (approval vs. trial) → not promoted. If a CONFIRMED
      FDA approval/rejection surfaces, that's Tier-B #2 (single-event). Session-1 watch.
    - **WOLF / SMCI** — semis/memory on whale-FLOW recurrence (not catalysts). Flow
      does NOT refresh the catalyst clock. Watch only.
    - **QCOM** — only AI-agent "safest pick" commentary Wed (not a catalyst).
    - **RIVN** — R2 launch + humanoids; session-1 watch.
    - **CRWD / STM / FLEX / PINS / VSH** — no fresh Wed catalyst; held/stale.
14. **Outlier movers Thu + sector breakdown.** Wed confirmed: QURE +75.6% / BHVN
    +14.8% (biotech binary, type unconfirmed); WOLF +13.8% (semis flow); KMX -7.6%
    / CVNA -7.7% (used-car retail soft prints); SATS -8.0%. Generic gainers/losers
    query still flaky (~13 consecutive sessions) — per-name reconstruction remains
    the workable path.
15. **Library gaps re-listing.** Reaffirmed/updated Wed: macro_event_window (FOMC
    dot plot, NEW_CATEGORY_NEEDED); event-window-on-price-claimed-names (AAPL/HPE/
    META/NVDA); index-rebalance/forced-flow (SPCX→QQQ); volatility_regime
    ACTIVATION; AI-capex permitting/financing overlay (NEW_CATEGORY_NEEDED);
    AI-policy/export-control overlay (Anthropic/DeepSeek); m_a_arbitrage activation
    (NUVL); underwriter_franchise (JPM/SpaceX). Sat research = next opportunity.

## Open questions for the operator

- **DEPLOYMENT: bare `python3` still broken (Homebrew 3.14, no harness deps).**
  Persists across every run since 6/16. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **Operator action:**
  repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or
  pip-install requirements into 3.14 / rebuild the venv), and pin python@3.13 against
  brew auto-upgrade. **NOTE: daily_news_prompt.md line ~31 still says "There is no
  virtualenv" — stale, contradicts reality; please update.**
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Shipped 2026-06-16
  on the operator's "3" instruction. SPCX is the first live provisional claim
  (revalidate_by 2026-06-30). Confirm you want it permanent. (Carry-forward from 6/16.)
- **News-brief / trader-schedule timing — CONFIRMED working Wed.** The 3:30 PM PT
  news run captured the 2:00 PM ET FOMC result cleanly, 30 min before the 4:00 PM PT
  trader run. The intended cadence held on the highest-stakes day. Keep monitoring.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is still
  a judgment call. Operator: formalize a mechanical counter + confirm a FLOW-screen
  mention does NOT count toward the clock (current call: it does NOT).
- **FLEX/MRVL index-inclusion not among the 5 Tier-B triggers (carry-forward).**
  Should index-inclusion (MRVL/FLEX 6/22) become a 6th Tier-B trigger?
- **`cli open-orders` parser bug (carry-forward).** Clean JSON on recent runs; stays
  provisionally closed. Confirm on a live open order.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers
  accumulate across days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed
  by trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **169 items** cleanly (via venv) —
  highest density in recent memory (SpaceX options debut + FOMC + AI-memory tape).
  CBRS/CSCO/NUVL had 0.
- WebSearch strong Wed: FOMC June-17 outcome / dot plot (CNBC/Fox/NPR/TradingKey/
  TheStreet); retail sales May (Census/NRF/TheStreet); VIX 18.44 +12.37% (Investing/
  CBOE/TheStreet); Iran signing 6/19 Geneva + oil (CNBC/Al Jazeera/SWI/TradingEconomics/
  Fortune); Anthropic ban update (Anthropic/Fortune/Axios); SPCX options record
  (Benzinga/TradingKey/Reuters).
- WebSearch weak: generic "biggest gainers/losers June 17" (Morningstar/WallStreetZen
  screen-level, catalysts unconfirmed) — ~13 consecutive sessions flaky; per-name
  reconstruction still the workable path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No carry-forward candidate refreshed with a fresh single-name
    catalyst (CRWD broke; STM/FLEX/PINS no refresh; SMCI/WOLF flow-only; QCOM
    commentary-only). None qualify.
  - **Tier B:** No qualifiers. SpaceX-Tesla merger = chatter not confirmed (#1);
    QURE/BHVN biotech catalyst TYPE unconfirmed (#2 not met); KMX/CVNA missed (#3);
    no 3-bank cluster (#4); HPE/MRVL wins are on names ALREADY in-universe (#5 n/a).
  - **Decision: 0 promotions. Universe stays at 23.**
- **`gap-registry coverage_holes` empty (confirmed)** — tag vol-regime as an
  ACTIVATION gap, not a registry hole.
- Previous notes (still held): "CPI/import-price/retail-sales <month> <year>" query
  format works; per-name reconstruction beats generic gainers/losers; major-M&A →
  target per-name search is cleanest.
