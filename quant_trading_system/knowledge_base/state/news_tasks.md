# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Thu 2026-06-18, Day-1 after FOMC). Event-rich
  but constructive / risk-ON. Marquee item: **Trump confirmed Apple agreed to build
  chips with Intel** — Intel's 3rd foundry win (after NVDA + Tesla TerraFab),
  **INTC +6-10%** (claimed by equity_breakout_volume_confirmation). Plus AAPL
  price-hike follow-through (~$100 iPhone hike), MU pre-print heating up, MRVL photonic
  milestone + 6/22 S&P 500 inclusion, AMZN Trainium external push, GOOGL Gemini co-lead
  Shazeer → OpenAI. **Relief rally** (Nasdaq 100 +2.5%, S&P +0.78%, Russell +2.0%) on
  the **US-Iran treaty signing Fri 6/19** (WTI ~$75.83) + the Intel/Apple deal.
  **Not HALT-WORTHY** — no active/pending FOMC on the planned session, no negative
  overnight catalyst on a held name, no adverse futures gap >2% (the only >2% move is
  the Nasdaq's UP day).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire run
  used `.venv/bin/python3 -m quant_trading_system.cli`. Operator action still required
  (see open questions). Use `.venv/bin/python3` + absolute paths / `cd /Users/rfoxes/Stock-Trading-Agent &&`.
- **Universe: 23-name, 23/23 claimed (unclaimed_count == 0), provisional_count 1.**
  SPCX still **PROVISIONAL / execution-quarantined** on equity_trend_following_ema_cross
  (revalidate_by 2026-06-30; will NOT trade). `gap-registry coverage_holes` = **empty**
  (confirmed again). No claim changes available to the news agent.
- **Alpaca density: 126 items (vs 169 Wed).** AAPL 12, AMZN 13, NVDA 14, SPCX 12,
  TSLA 11, GOOGL 10, INTC 9, META 9, MU 9, MRVL 5, TSM 5, MSFT 3, ORCL 3, QQQ 3, SPY 3,
  AVGO 2, CBRS 1, DELL 1, JPM 1; ARM/CSCO/HPE/NUVL 0. Tape dominated by the Intel/Apple
  chip deal, AI-memory super-cycle, AI-capex-financing reframing, SpaceX, and the Iran
  relief rally. All 6 category HTMLs + daily summary written.
- **Held set (per 6/17 trader handoff, unchanged):** AAPL 72, AVGO 26, MU 7, ORCL 38,
  QQQ 28, SPY 35. Active set 7 strategies.
- **0 promotions Thu.** No Tier-A refresh, no Tier-B qualifier (the Apple→Intel win is
  between two ALREADY-in-universe names → #5 n/a). Universe stays 23.

## Notable carry-forwards

- **INTC — Apple foundry deal (3rd Intel customer win; +6-10%).** Real demand/contract
  catalyst on a breakout-claimed name. Track follow-through + whether the breakout
  volume gate triggers a fire. Govt 10% Intel stake now >$600B. Reshoring policy theme.
- **AAPL — Cook memory price-hike (now ~$100 iPhone-hike analyst call) + Intel foundry
  diversification (held).** Two real events on a held, trend-claimed name → library gap.
  Track sell-side margin/demand reaction + whether other hardware names echo it.
- **MU Q3 FY26 print — DATE NOW ~6/24-25 AMC.** Zacks preview (6/18) says **Wed 6/25**;
  prior notes said Tue 6/24 — RECONFIRM the exact date next run. Pre-print window open:
  ~44% upside roundup, SK Hynix HBM4E samples, Cook tailwind, UBS de-risk cross-current.
  Refresh IV/UOA/sell-side daily into the print. Held long.
- **MRVL — Tower Semi/Marvell 5M+ photonic chips for AI data centers (product
  milestone) + S&P 500 inclusion 6/22 (with FLEX).** On-character for
  equity_breakout_volume_confirmation IF volume-confirmed. Track the 6/22 passive-flow
  window all week.
- **AMZN — Trainium AI-chip strategy beyond AWS (challenge to NVIDIA) + Kyndryl AWS AI
  deal.** Product/strategy event on a trend-claimed name → library gap. Track external-
  chip-sales follow-through + NVDA competitive read-through.
- **GOOGL — Gemini co-lead Noam Shazeer departs for OpenAI.** AI-talent loss event on a
  trend-claimed name → library gap. Track any further Google DeepMind/Gemini departures.
- **AI-capex = financing/leverage story.** "AI trade moving from Nvidia to the bond
  market" (NVDA/ORCL/META debt-funding) + Goldman "$770B could backfire" + UBS "take
  chips off the table," COMPOUNDED by higher-for-longer rates. Track cohort de-rating
  on financing/leverage risk (ORCL/DELL/hyperscalers).
- **FOMC AFTERMATH — higher-for-longer is now the standing backdrop.** ~80% priced for
  ZERO 2026 cuts; Citadel calls a SEPTEMBER hike. Track Fed-speaker reactions, CME
  FedWatch repricing, AI-cohort multiple de-rating, VIX path.
- **TSM — competitive NEGATIVE read-through from Apple→Intel foundry deal.** Apple
  diversifying capacity away from TSMC. Track whether sell-side cuts TSMC volume/share
  estimates.
- **SPCX → QQQ Nasdaq-100 fast-entry (~July 1) + Russell (6/26).** ~$22-27B forced flow
  reweights held QQQ constituents through ~July 1. SPY excluded (GAAP). Meme run
  reportedly STALLING (Cramer/Gary Black/Tom Sosnoff). Aug IPO lock-up = next structural
  date. Don't bury the real QQQ rebalance read-through under the meme noise. SPCX stays
  quarantined (revalidate_by 6/30).
- **US-Iran treaty SIGNING Fri 6/19 Geneva.** Confirm signed; Hormuz traffic normalizing;
  oil direction into the weekend; Israel-Lebanon durability tail risk.
- **Anthropic Fable 5 / Mythos 5 export ban (Day 6-7).** G7 fragmentation debate
  (Amodei + Altman). Track: does it return (~70% by July 1), NVDA-China spillover,
  DeepSeek/Z.ai substitution.
- **VIX sub-20, no clean regime.** volatility_regime is an ACTIVATION gap (responders
  exist, none active / none claim a universe symbol). 6/18 close UNCONFIRMED (likely
  eased off 18.44 on the relief rally). Track whether higher-for-longer keeps IV
  elevated or it fades sub-17.

## To do tomorrow (next news run, Fri 2026-06-19)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every
   run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap).
   Both require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 23** (23/23 claimed). **Cover SPCX** (per-symbol + a line);
   it stays execution-quarantined until Sat research (revalidate_by 6/30).
4. **INTC Apple-foundry follow-through** — did the breakout fire? Any further detail on
   the deal terms / timeline? Reshoring policy thread.
5. **MU pre-print Day-N (~6/24-25 AMC) — RECONFIRM exact date.** Sell-side / UOA / IV
   refresh. Held long.
6. **AAPL Cook memory-price-hike + Intel foundry diversification** follow-through. Does
   the hardware cohort echo it? MU read-through.
7. **MRVL photonic milestone + 6/22 S&P 500 inclusion (with FLEX)** passive-flow window.
8. **AMZN Trainium external-chip push + GOOGL Shazeer departure** follow-through.
9. **AI-capex financing/leverage + higher-for-longer compounding.** Any cohort de-rating?
10. **US-Iran treaty signing Fri 6/19** — confirm signed; oil; Hormuz normalization;
    Israel-Lebanon durability.
11. **Anthropic export-ban Day-N.** Did models return (July-1 prediction date)?
    NVDA-China spillover? DeepSeek substitution?
12. **Vol regime Fri.** VIX direction; did it ease off 18.44 / hold sub-20? VIX9D vs VIX.
    Activation gap on volatility_regime. (Get a confirmed VIX close — 6/18 was flaky.)
13. **Promote candidates if Fri session refreshes (consecutive-session rule):**
    - **SanDisk** — AI-memory super-cycle surge Thu, no CONFIRMED single-name catalyst →
      session-1 watch (memory read-through alongside MU). If a confirmed catalyst
      (beat+raise+5%, or named contract) surfaces, re-evaluate Tier-B.
    - **QURE / BHVN** — biotech binary movers (Wed), catalyst TYPE still unconfirmed → no
      Thu refresh. If a CONFIRMED FDA approval/rejection surfaces, that's Tier-B #2.
    - **WOLF / SMCI** — semis/memory whale-FLOW recurrence (not catalysts). Flow does NOT
      refresh the catalyst clock. Watch only.
    - **QCOM** — only the IT whale screen Thu (flow, not a catalyst).
    - **RIVN** — R2 launch + humanoids; no Thu refresh; session-1 watch.
14. **Outlier movers Fri + sector breakdown.** Thu confirmed: INTC +6-10% (Apple-Intel
    deal — IN universe); SanDisk surge (memory); AMZN up (Trainium). Generic
    gainers/losers query still flaky (~14 consecutive sessions) — per-name reconstruction
    remains the workable path.
15. **Library gaps re-listing.** Reaffirmed/updated Thu: event-window-on-price-claimed-
    names (AAPL/AMZN/GOOGL/NVDA/TSM/TSLA); US-semiconductor-reshoring/industrial-policy
    overlay (Intel foundry wins, NEW); macro_event_window (FOMC higher-for-longer,
    NEW_CATEGORY_NEEDED); index-rebalance/forced-flow (SPCX→QQQ); AI-capex financing
    overlay (NEW_CATEGORY_NEEDED); volatility_regime ACTIVATION; AI-policy/export-control
    overlay; m_a_arbitrage activation (NUVL); underwriter_franchise (JPM/SpaceX). Sat
    research = next opportunity.

## Open questions for the operator

- **DEPLOYMENT: bare `python3` still broken (Homebrew 3.14, no harness deps).** Persists
  across every run since 6/16. Working interpreter:
  `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **Operator action:**
  repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or
  pip-install requirements into 3.14 / rebuild the venv), and pin python@3.13 against
  brew auto-upgrade. **NOTE: daily_news_prompt.md line ~31 still says "There is no
  virtualenv" — stale, contradicts reality; please update.**
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Shipped 2026-06-16. SPCX
  is the first live provisional claim (revalidate_by 2026-06-30). Confirm permanent.
- **News-brief / trader-schedule timing — holding well.** Fresh briefs 6/16, 6/17, 6/18
  on schedule. The 3:30 PM PT news run continues to lead the 4:00 PM PT trader run by
  30 min. Keep monitoring.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is still a
  judgment call. Operator: formalize a mechanical counter + confirm a FLOW-screen mention
  does NOT count toward the clock (current call: it does NOT).
- **FLEX/MRVL index-inclusion not among the 5 Tier-B triggers (carry-forward).** Should
  index-inclusion (MRVL/FLEX 6/22) become a 6th Tier-B trigger?
- **`cli open-orders` parser bug (carry-forward).** Clean JSON on recent runs; stays
  provisionally closed. Confirm on a live open order.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate
  across days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by
  trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **126 items** cleanly (via venv).
  ARM/CSCO/HPE/NUVL had 0.
- WebSearch strong Thu: Intel/Apple chip deal (CNBC/US News/Reuters/24-7WallSt);
  FOMC aftermath / rate-cut odds (Polymarket/Kalshi/Benzinga); Iran treaty 6/19 + oil
  (OilPrice/NBC/RFE-RL/TradingEconomics); MU/FDX/NKE earnings calendar (Zacks/Globe and
  Mail); relief-rally index levels (Schwab/Edward Jones).
- WebSearch weak: **VIX exact 6/18 close** (sources kept returning the stale 18.44 6/17
  print — could not confirm the 6/18 figure; flagged in the brief). Generic "biggest
  gainers/losers June 18" still screen-level/unconfirmed (~14 consecutive sessions
  flaky) — per-name reconstruction still the workable path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No carry-forward candidate refreshed with a fresh single-name catalyst
    (QURE/BHVN no refresh; WOLF/SMCI/QCOM flow-only; RIVN no refresh). None qualify.
  - **Tier B:** No qualifiers. No confirmed M&A target (#1); no confirmed FDA binary (#2);
    no in-scope beat+raise+5% (#3); no 3-bank cluster (#4); the Apple→Intel foundry win
    (#5 candidate) is between two ALREADY-in-universe names → n/a.
  - **Decision: 0 promotions. Universe stays at 23.**
- **`gap-registry coverage_holes` empty (confirmed)** — tag vol-regime as an ACTIVATION
  gap, not a registry hole.
- **DATE DISCREPANCY to resolve:** MU Q3 print — Zacks 6/18 preview = Wed 6/25 AMC; prior
  harness notes = Tue 6/24. Reconfirm next run.
- Previous notes (still held): "CPI/import-price/retail-sales <month> <year>" query format
  works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name
  search is cleanest.
