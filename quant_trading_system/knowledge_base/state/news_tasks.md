# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NORMAL FLOW (Fri 2026-06-19, **Juneteenth — US markets
  CLOSED**, `market-status is_open:false`, next open Mon 2026-06-22 09:30 ET). No cash
  session today; trader plans into Monday. Lighter tape (**52 Alpaca items** vs 126
  Thu), mostly follow-throughs. Marquee items: **INTC hired former SK Hynix CEO
  Seok-Hee Lee as EVP Intel Foundry / advanced packaging** (mgmt event, Apple-foundry
  follow-through); **MU print DATE CONFIRMED Wed 6/24 AMC** (resolves 6/24-vs-6/25);
  **MRVL + FLEX S&P 500 inclusion effective before open Mon 6/22** (passive-flow window
  lands Monday; MRVL also new CFO); **SPCX -20%+ from post-IPO high (~$620B erased) on
  $60B all-stock Cursor/Anysphere dilution** (Grantham "break the index"; bear ETFs
  surging — quarantined, won't trade). Plus Ohio under-16 social-media consent law
  (META/GOOGL), ProShares "FAB 10" ETF filing, BofA "most-crowded-trade-in-history"
  semis survey. **NOT HALT-WORTHY** (no FOMC on the planned session, no negative
  overnight catalyst on a held name, no >2% adverse futures gap, market closed today).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14, no deps). Entire run
  used `.venv/bin/python3 -m quant_trading_system.cli`. Operator action still required
  (see open questions). Use `.venv/bin/python3` + `cd /Users/rfoxes/Stock-Trading-Agent &&`.
- **Universe: 23-name, 23/23 claimed (unclaimed_count == 0), provisional_count 1.**
  SPCX still **PROVISIONAL / execution-quarantined** on equity_trend_following_ema_cross
  (revalidate_by 2026-06-30; will NOT trade). `gap-registry coverage_holes` = **empty**
  (confirmed again). No claim changes available to the news agent.
- **Alpaca density: 52 items (vs 126 Thu — holiday).** MSFT 6, NVDA 6, TSLA 6, SPCX 8,
  AMZN 4, AVGO 3, GOOGL 3, INTC 2, CSCO 2, META 2, MU 2, QQQ 2, SPY 2, AAPL 1, JPM 1,
  MRVL 1, ORCL 1; ARM/CBRS/DELL/HPE/NUVL/TSM 0. All 6 category HTMLs + daily summary
  written.
- **Held set (per 6/18 trader handoff, unchanged):** AAPL 72, AVGO 26, MU 7, ORCL 38,
  QQQ 28, SPY 35. Active set 7 strategies. (Book was $109.5K Thu; no session 6/19.)
- **0 promotions Fri.** No Tier-A refresh, no Tier-B qualifier (SpaceX/Cursor target is
  private + acquirer already in universe → #1 n/a; holiday → no prints). Universe stays 23.

## Notable carry-forwards

- **MRVL — S&P 500 INCLUSION EFFECTIVE MON 6/22 (with FLEX; replacing POOL/CPB) + new
  CFO.** The passive-flow buy window arrives the very next session. Breakout-claimed;
  the most plausible Monday firer IF volume-confirmed. Track whether the breakout gate
  fires on the index-add flow; track post-inclusion follow-through all week.
- **MU — Q3 FY26 print DATE CONFIRMED Wed 6/24 AMC** (Micron IR / StockTitan / Nasdaq /
  Zacks — resolves the 6/24-vs-6/25 ambiguity). Pre-print window open; held long; AI-
  memory demand stack intact (SK Hynix HBM4E, Cook memory warning). Refresh IV/UOA/
  sell-side daily into the print Mon→Wed.
- **INTC — foundry leadership hire (former SK Hynix CEO Seok-Hee Lee → EVP advanced
  packaging, reports to Lip-Bu Tan).** Mgmt/strategy event extending the Apple→Intel
  foundry win; advanced packaging carved out as a dedicated business. Breakout-claimed
  (price handle only). Track foundry follow-through / further customer-win or deal terms.
- **SPCX — DILUTION DRAWDOWN now in motion (-20%+ from post-IPO high, ~$620B erased) on
  $60B all-stock Cursor/Anysphere deal (announced 6/16; 3.4% dilution; closes Q3'26).**
  Meme run that was "stalling" Thu is now unwinding. Grantham "break the index"; bear/
  inverse ETFs surging. Stays quarantined (revalidate_by 6/30). Track price path +
  whether it stabilizes; vol-selling responder candidate for Sat research.
- **QQQ — index-rebalance cross-currents.** SPCX Nasdaq-100 fast-entry ~July 1 (+ Russell
  6/26) still pending BUT SPCX's drawdown shrinks the forced-buy dollar size vs the prior
  $22-27B estimate. MRVL S&P add (Mon 6/22) is a separate flow. Held QQQ. Don't mistake
  rebalance pressure for fundamental weakness.
- **AI-trade CROWDING now flagged.** BofA June survey: "long semiconductors" = most
  crowded trade in market history (80% of managers). Compounds higher-for-longer + AI-
  capex-financing/leverage overhang on the cohort (ORCL/DELL/semis/hyperscalers). Track
  cohort de-rating / reversal risk.
- **"Mag7 → FAB 10."** ProShares filed the FAB 10 ETF (equal-weight NVDA/MSFT/AMZN/META/
  TSLA/GOOGL/AVGO/ORCL/SPCX + private OpenAI & Anthropic), effective ~Sep 1. Touches 8
  universe names as a future passive-flow wrapper. Soft/structural; track launch.
- **FOMC AFTERMATH — higher-for-longer is the standing backdrop.** ~80% priced for ZERO
  2026 cuts; Citadel calls a SEPTEMBER hike. **VIX last close 16.40 (6/18, -11% from
  18.44)** — RESOLVED; vol eased on the relief rally, sub-17 low-vol regime. Track Fed
  speakers, CME FedWatch, VIX path Monday.
- **META / GOOGL — Ohio under-16 parental-consent law (appeals court allows enforcement;
  also TikTok).** State-level regulatory overhang. Track further state actions / appeals.
- **US-Iran treaty — Geneva signing slated 6/19 BUT HIT A SNAG (Vance delayed trip,
  Friday talks called off last-minute).** Trump signed an initial deal 6/17; Hormuz-
  reopening framework intact; oil ~$76. **CONFIRM over the weekend whether the formal
  signing occurred or slipped.**
- **Anthropic Fable 5 / Mythos 5 export ban Day ~7-8.** Seoul office opened 6/18; "back
  in coming days"; ~57% odds restored before July 1; Opus/Sonnet/Haiku unaffected.
  Track: did models return? NVDA-China spillover? DeepSeek substitution?
- **TSM — competitive NEGATIVE read-through from the Intel-foundry thread.** No TSM-
  specific event; track whether sell-side trims TSMC volume/share estimates.

## To do tomorrow (next news run, Mon 2026-06-22)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every
   run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 triggers, 2/day cap).
   Both require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls. Bare `python3` WILL fail.
3. **Universe should confirm 23** (23/23 claimed). **Cover SPCX** (per-symbol + a line);
   it stays execution-quarantined until Sat research (revalidate_by 6/30).
4. **MRVL S&P 500 inclusion goes EFFECTIVE Mon 6/22** — did the breakout fire on the
   index-add passive-flow buy? Post-inclusion follow-through? (Most plausible Mon firer.)
5. **MU pre-print Day-N (CONFIRMED Wed 6/24 AMC).** Sell-side / UOA / IV refresh. Held long.
6. **INTC foundry leadership hire follow-through** — deal terms / further customer wins?
   Reshoring policy thread.
7. **SPCX dilution drawdown** — did it stabilize Mon? Price path; QQQ-rebalance size
   read-through. Stays quarantined.
8. **AI-trade crowding (BofA survey) + higher-for-longer compounding.** Cohort de-rating
   in Monday's tape? Watch trend/momentum rules' execute output.
9. **US-Iran signing** — confirm signed-or-slipped over the weekend; oil; Hormuz.
10. **Anthropic export-ban Day-N.** Did the models return (July-1 prediction window)?
    NVDA-China spillover? DeepSeek substitution?
11. **Vol regime Mon.** First VIX print since 6/18's 16.40 — direction; VIX9D vs VIX.
    Activation gap on volatility_regime.
12. **Promote candidates if Mon session refreshes (consecutive-session rule):**
    - **SanDisk** — AI-memory super-cycle read-through; session-1 watch, no confirmed
      single-name catalyst yet. If a confirmed catalyst (beat+raise+5%, or named
      contract) surfaces, re-evaluate Tier-B.
    - **QURE / BHVN** — biotech binary movers, catalyst TYPE still unconfirmed → no
      refresh. If a CONFIRMED FDA approval/rejection surfaces, that's Tier-B #2.
    - **WOLF / SMCI / QCOM** — semis/memory whale-FLOW recurrence (not catalysts). Flow
      does NOT refresh the catalyst clock. Watch only.
    - **RIVN** — R2 launch + humanoids; session-1 watch.
13. **Outlier movers Mon + sector breakdown.** First live session since Thu (Fri was the
    holiday). Generic gainers/losers query still flaky (~15 consecutive sessions) —
    per-name reconstruction remains the workable path.
14. **Library gaps re-listing.** Reaffirmed Fri: event-window-on-price-claimed-names
    (INTC mgmt-hire/foundry, META/GOOGL regulatory, AMZN cost-curve, QQQ rebalance);
    US-semiconductor-reshoring/industrial-policy overlay; index-rebalance/forced-flow
    (MRVL→S&P 6/22, SPCX→QQQ ~July 1); macro_event_window (FOMC, NEW_CATEGORY_NEEDED);
    AI-capex-financing/crowding overlay (NEW_CATEGORY_NEEDED); volatility_regime
    ACTIVATION; AI-policy/export-control overlay; m_a_arbitrage activation (NUVL). Sat
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
- **News-brief / trader-schedule timing — holding well.** Fresh briefs 6/16, 6/17, 6/18,
  6/19 on schedule (incl. the Juneteenth holiday). 3:30 PM PT news run leads the 4:00 PM
  PT trader run by 30 min. Keep monitoring.
- **Holiday-session handling.** The news run executed normally on Juneteenth and produced
  a fresh brief; `market-status` correctly reported closed (next open 6/22). The trader's
  4:00 PM PT run today plans into Monday with no session today — confirm the trader's
  execute path no-ops cleanly on a closed-market day (likely already handled).
- **FLEX/MRVL index-inclusion not among the 5 Tier-B triggers (carry-forward).** MRVL's
  S&P 500 add goes effective Mon 6/22. Should index-inclusion become a 6th Tier-B trigger?
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule is still a
  judgment call. Operator: formalize a mechanical counter + confirm a FLOW-screen mention
  does NOT count toward the clock (current call: it does NOT).
- **`cli open-orders` parser bug (carry-forward).** Clean JSON on recent runs; stays
  provisionally closed. Confirm on a live open order.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate
  across days. Run `bash scripts/install_git_safety.sh` if not installed.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by
  trend_following; Sat research owns proper claim + m_a_arbitrage activation.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **52 items** cleanly (via venv).
  ARM/CBRS/DELL/HPE/NUVL/TSM had 0. (Lighter than usual — Juneteenth.)
- `cli market-status` → `is_open: false`, `next_open_iso: 2026-06-22T09:30:00-04:00`.
  Regime: bull, conf 0.73, ADX 22.63 (steady).
- WebSearch strong Fri: MU 6/24 date (Micron IR/StockTitan/Nasdaq/Zacks — CONFIRMED);
  VIX 6/18 close 16.40 (Yahoo/Investing/Macrotrends — RESOLVED the carry-forward);
  MRVL/FLEX S&P 6/22 inclusion (S&P Global/CNBC); Intel Lee hire (Intel Newsroom/Tom's
  Hardware); FAB 10 ETF (Benzinga/Yahoo); SpaceX/Cursor $60B (CNBC/Trefis); Anthropic
  ban Day 7-8 (TechTimes/Fortune); US-Iran Geneva-signing snag (Swissinfo/CNN/NPR).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (~15 consecutive
  sessions) — and moot today (market closed). Per-name reconstruction stays the path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No carry-forward candidate refreshed with a fresh single-name catalyst
    (SanDisk/QURE/BHVN no refresh; WOLF/SMCI/QCOM flow-only; RIVN no refresh). None qualify.
  - **Tier B:** No qualifiers. #1 (SpaceX/Cursor) — target Anysphere/Cursor is private +
    acquirer SPCX already in universe → n/a; #2 no FDA binary; #3 no prints (holiday);
    #4 no 3-bank cluster; #5 no new Tier-1 customer win.
  - **Decision: 0 promotions. Universe stays at 23.**
- **`gap-registry coverage_holes` empty (confirmed)** — tag vol-regime as an ACTIVATION
  gap, not a registry hole.
- **MU DATE DISCREPANCY RESOLVED:** Q3 FY26 print = **Wed June 24 AMC** (was 6/24-vs-6/25).
- Previous notes (still held): "CPI/import-price/retail-sales <month> <year>" query format
  works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name
  search is cleanest.
