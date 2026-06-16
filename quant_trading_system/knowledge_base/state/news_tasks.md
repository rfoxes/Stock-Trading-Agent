# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Tue 2026-06-16). FOMC eve, multi-event
  day, no halt trigger. (1) **Warsh's first FOMC (6/16-17)** — hold ~97% priced;
  the **dot plot + Warsh's debut presser Wed 6/17 2:00/2:30 PM ET** is THE live
  catalyst (fractured-committee risk: residual cut camp vs. a hawkish minority
  floating a 2026 *hike*); lands the session after the 6/16 trader run. (2) **Hot
  import print** — May import prices +1.9% (~2x consensus), YoY +6.7% (highest
  since Aug 2022); fuel +12.5%, cap goods +1.3%. Hawkish into the dot plot. (3)
  **AI-capex narrative turned two-sided** — JPMorgan "$4.1T AI-debt" + NVDA's own
  ~$20-25B debt raise + a $130B data-center-permitting backlash; chip cohort
  (NVDA/AVGO/MU) led the Nasdaq lower intraday while the Dow hit a record. (4)
  **US-Iran deal signing Fri 6/19 Switzerland** confirmed; oil ~$77-81; VIX 16.41
  (second day sub-20). Not HALT-WORTHY (Fed decision is Wed, Iran de-escalation,
  no held-name negative overnight catalyst).
- **First proper post-FOMC-eve brief; 6/16 fully covered.** Unlike the 6/11-6/12
  gap, this run executed cleanly. Note: the trader ran TWICE on 6/16 (a repair-run
  that fired an AVGO false-positive buy, then a do-nothing follow-on); last_handoff
  is dated 6/16. The 6/16 news brief (this one) is fresh — resolves the "no fresh
  brief for 6/16" issue the trader flagged.
- **Interpreter:** bare `python3` still BROKEN (Homebrew 3.14, no deps). Entire
  run used `.venv/bin/python3 -m quant_trading_system.cli`. Operator action still
  required (see open questions). NOTE: cwd drifts if you `cd` into a news subdir
  mid-run — use absolute paths or `cd /Users/rfoxes/Stock-Trading-Agent &&` for CLI.
- **Universe:** 22-name (unchanged). Tue Alpaca densities (98 items total, vs Mon
  100): TSLA 16, AMZN 13, MSFT 11, GOOGL 10, NVDA 10, META 7, AAPL 6, MU 6, QQQ 4,
  SPY 4, DELL 3, MRVL 3, INTC 2, AVGO 1, ORCL 1, TSM 1; ARM/CBRS/CSCO/HPE/JPM/NUVL 0.
  Heavily SpaceX/Elon/AI-debt weighted. All 6 category HTMLs + daily summary
  written. Cleanup deleted 0 (cutoff 2026-03-18).
- **`gap-registry` change:** `coverage_holes` is now **EMPTY** — the Sat research
  run closed the `volatility_regime` hole by tagging the 4 options strategies
  (iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings).
  Remaining gaps are now **activation/assignment** gaps (responder declared in
  library but not active / claims no universe symbol) + **taxonomy** gaps
  (NEW_CATEGORY_NEEDED), not registry holes. Tag accordingly going forward.
- **Held set (per 6/16 trader handoff):** AAPL 72, AVGO 26, MU 7, ORCL 38, QQQ 28,
  SPY 35. Active set 7 strategies × 22/22 claimed, unclaimed_count == 0.
- **Zero promotions Tue.** Tier-B daily cap untouched. No Tier-A catalyst refresh.

## Notable carry-forwards

- **FOMC dot plot Wed 6/17 — THE live catalyst.** Warsh's debut. Hold priced
  ~97%; the dots + presser are the event. Wed 6/17 news run = the OUTCOME run:
  report the dot-plot revision (cuts vs. hike-camp), Warsh's tone, and the
  AI-cohort reaction. A hawkish revision (reinforced by the hot import print) is
  the main 48h risk to the cohort multiple.
- **MU Q3 FY26 = Tue 6/24 AMC.** Held long. New 52-wk high pre-print; PT raises on
  AI-memory demand; bullish call flow. Pre-print window open — track IV expansion,
  sell-side follow-through, UOA refresh daily into the print.
- **META AI-Mode search launch (Muse Spark).** ~$10B/yr revenue potential, direct
  Google-search challenge. Product-launch event with NO event responder (META
  claimed by momentum_macd, price-driven) — logged as a library gap. Track sell-
  side sizing of the AI-search opportunity + GOOGL competitive response.
- **NVDA ~$20-25B debt raise.** Capital-allocation event; anchors the "$4.1T
  AI-debt" reframing. No event responder on NVDA (trend-following claim). Track
  use-of-proceeds (buyback per Cramer?) and whether more cohort names lever up.
- **AI-capex backlash ($130B data-center projects blocked/delayed, 14-state
  moratorium bills) + "$4.1T AI-debt" story.** New structural HEADWIND lens to the
  infra-capex thesis (ORCL/DELL/hyperscalers). Track legislative escalation +
  whether the cohort de-rates on financing/permitting risk.
- **US-Iran deal signing Fri 6/19 Switzerland.** Track durability (Israel-Lebanon
  strikes), oil direction, 60-day nuclear/sanctions negotiation start. Any
  breakdown headline = oil/vol re-rate into the weekend.
- **Anthropic Fable 5 / Mythos 5 export ban (Day 4-5).** Amazon-triggered (Jassy
  flagged flaws); Anthropic negotiating in DC; Polymarket ~71% / Kalshi ~68% it
  returns by July 1. Track: (a) does the model return (the prediction-market date
  is July 1), (b) NVDA-China spillover, (c) EU sovereign-AI response.
- **DELL AI-server +757% + Goldman $1.24T TAM raise.** Demand datapoint; on IT
  whale screen. Track sell-side follow-through.
- **INTC / Mobileye robotaxi 2027.** Stake read-through; track MBLY follow-up.
- **SPCX (SpaceX).** Historic options debut 6/16 (3rd-most-traded single name
  behind TSLA/NVDA; gamma-squeeze talk). Also exercising $60B option to buy
  Anysphere (Cursor). NOT a Tier-B trigger (IPO). Session-2 watch; track recurrence
  + read-through to TSLA/NVDA vol surface.
- **MRVL + FLEX S&P 500 inclusion 6/22** — passive-flow window THIS week. No fresh
  6/16 catalyst (MRVL slipped post-Monday-surge = price action). Track into 6/22.
- **VIX sub-20 (16.41).** IV compression; `volatility_regime` now has library
  responders but none active / none claim a universe symbol (activation gap).
  Track whether the dot plot re-inflates front-end IV.
- **NUVL/GSK** — pre-close, trades freely. 0 Alpaca items Tue. PDUFA 2026-11-27.
- **Trump 100% French-wine tariff threat** (AAPL/AMZN/META/GOOGL) ahead of G7.
  Posture; track G7.
- **`SYMBOL_TO_SECTOR` map** — `cli news-universe` resolves all 22 correctly now;
  underlying map in `news_service.py` may still be incomplete. Hygiene carry-forward.

## To do tomorrow (next news run, Wed 2026-06-17)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every
   run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap).
   Both require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls. Bare `python3` = Homebrew 3.14,
   no deps, WILL fail. Use absolute paths / `cd /Users/rfoxes/Stock-Trading-Agent &&`.
3. **Universe is 22-name.** `cli news-universe` Wed should confirm.
4. **FOMC OUTCOME run (Wed is THE day).** Report the actual dot-plot revision
   (median 2026 dots; cut vs. hike camp), Warsh's debut presser tone, and the
   AI-cohort reaction. This is the highest-priority item for Wed. Decision drops
   2:00 PM ET / presser 2:30 PM ET — the 3:30 PM PT news run will have the result.
5. **MU pre-print Day-N (6/24 AMC).** Sell-side / UOA refresh. Held long.
6. **META AI-Mode sell-side sizing + GOOGL response.** Product-launch follow-through.
7. **NVDA debt-raise use-of-proceeds.** Buyback confirmation? More cohort issuance?
8. **AI-capex backlash + "$4.1T debt" follow-through.** Any de-rating on financing/
   permitting risk? Legislative escalation (state moratoriums)?
9. **US-Iran deal durability** into the Fri 6/19 signing; oil; Israel-Lebanon risk.
10. **Anthropic export-ban Day-N.** Did models return (July-1 prediction-market
    date)? NVDA-China spillover? EU sovereign-AI follow-up.
11. **MRVL + FLEX 6/22 inclusion** passive-flow window — track all week.
12. **Vol regime Wed.** Did the dot plot re-inflate VIX, or did sub-20 hold? VIX9D
    vs VIX. Activation gap on volatility_regime (responders exist, none active).
13. **Promote candidates if Wed session refreshes (consecutive-session rule):**
    - **CRWD** — did NOT refresh Tue (catalyst clock broke); needs a fresh Wed
      catalyst appearance to rebuild toward Tier-A.
    - **SMCI / WDC** — recurring on whale FLOW screens (not catalyst events);
      session-2-ish on flow recurrence. A flow screen does NOT refresh the
      catalyst clock — need a real single-name catalyst.
    - **STM / FLEX / PINS** — no fresh Tue appearance; held.
    - **QCOM** — 40+ AI devices + rumored $10B Tenstorrent deal (+4%). Rumor, not
      confirmed → no Tier-B. Session-1 catalyst watch.
    - **RIVN** — R2 launch + humanoid robots. Session-1 watch.
    - **SPCX** — session-2 watch (not Tier-B-eligible).
14. **Outlier movers Wed + sector breakdown.** Tue confirmed catalysts: Yum sells
    Pizza Hut $2.7B (YUM seller); SpaceX buys Anysphere/Cursor $60B; PLAY missed
    Q1. Generic gainers/losers query still flaky (~12 consecutive sessions) —
    per-name reconstruction remains the workable path.
15. **Library gaps re-listing.** Reaffirmed/updated: event-window-on-price-claimed-
    names (META launch / NVDA debt — event_catalyst responder doesn't claim them);
    macro_event_window (FOMC/import-prints, NEW_CATEGORY_NEEDED); volatility_regime
    ACTIVATION (registry hole now CLOSED, but no active strategy claims a universe
    symbol); AI-capex/permitting risk overlay (NEW_CATEGORY_NEEDED); AI-policy/
    export-control overlay (Anthropic); m_a_arbitrage activation (NUVL);
    underwriter_franchise (JPM/SpaceX). Sat research = next opportunity.

## Open questions for the operator

- **DEPLOYMENT: bare `python3` still broken (Homebrew 3.14, no harness deps).**
  Persists across every run since 6/16. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **Operator action:**
  repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or
  pip-install requirements into 3.14 / rebuild the venv), and pin python@3.13 against
  brew auto-upgrade. Until then every automated run that uses bare `python3` fails.
  (NOTE: daily_news_prompt.md still says "There is no virtualenv" at line ~31 —
  this is stale and contradicts reality; flag for the operator to update.)
- **News-brief / trader-schedule timing.** This run executed ~3:40 PM PT; the FOMC
  result Wed lands 2:00 PM ET (11 AM PT) so the 3:30 PM PT Wed run will have it.
  Confirm the 3:30 PM news run reliably precedes the 4:00 PM trader run.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is
  still a judgment call; CRWD's clock broke Tue (no fresh appearance). Operator:
  formalize a mechanical counter + define whether a FLOW-screen mention (vs. a
  catalyst event) counts toward the clock (current call: it does NOT).
- **FLEX index-inclusion not among the 5 Tier-B triggers (carry-forward).** Should
  index-inclusion (MRVL/FLEX 6/22) become a 6th Tier-B trigger?
- **`cli open-orders` parser bug (carry-forward).** Returned clean JSON on the 6/16
  trader run; stays provisionally closed. Confirm on a live open order.
- **git-sync LaunchAgent.** `git-doctor` previously showed 1 pending marker
  (marker_test.json). Verify `launchctl list | grep harness` if markers accumulate
  across days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed
  by trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **98 items** cleanly (via venv).
  TSLA/AMZN/MSFT/GOOGL/NVDA anchored; ARM/CBRS/CSCO/HPE/JPM/NUVL had 0. Tape
  dominated by macro (FOMC/import-prices), the SpaceX/Elon complex, and the
  AI-debt/capex-risk narrative.
- WebSearch strong: FOMC June-17 / Warsh (Yahoo/StockTitan/IndexBox/nnng); import
  prices May (BLS/TradingEconomics/Investing); VIX 6/16 16.41 (Yahoo/CBOE/CNBC);
  Iran signing 6/19 (CNBC/CNN/CBS/Al Jazeera/RT); Anthropic ban update (Benzinga/
  TechTimes/MLQ/Kalshi/Polymarket); data-center backlash (NBC/Tom's Hardware/
  Benzinga); SPCX options debut (Seeking Alpha/SpotGamma/Saxo); Yum-Pizza Hut M&A
  (Bloomberg/Fortune/TipRanks).
- WebSearch weak: generic "biggest gainers/losers June 16" (Morningstar/WallStreetZen
  screen-level only, catalysts unconfirmed) — ~12 consecutive sessions flaky;
  per-name reconstruction still the workable path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** CRWD (was 3, broke — no fresh catalyst), STM/FLEX/PINS (2, no
    refresh), VSH (1, no refresh), SMCI (flow-screen recurrence only, not a
    catalyst). None qualify.
  - **Tier B:** No qualifiers. Yum=seller not target (#1 fail); no FDA (#2); no
    beat+raise+5% (#3, PLAY missed); no 3-bank cluster (#4); QCOM/Tenstorrent is
    rumor not confirmed (#5 fail).
  - **Decision: 0 promotions. Universe stays at 22.**
- **`gap-registry coverage_holes` is now empty** — re-tag vol-regime as an
  activation gap, not a registry hole, going forward.
- Previous notes (still held): "CPI/import-price <month> <year>" query format works;
  per-name reconstruction beats generic gainers/losers; major-M&A → target per-name
  search is cleanest.
