# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**NEXT RUN IS WEDNESDAY 2026-07-08, 3:30 PM PT** (30 min before the trader run). Markets OPEN Wed 7/8 (`market-status` → `next_open 2026-07-08T09:30 ET`). **FOMC June minutes release Wed 7/8** (first under Chair Warsh — not a rate decision, but watch the tone).

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Tue 2026-07-07, canonical post-close 3:30 PM PT run). A **risk-off reversal** from Monday's record: **Samsung's record-but-priced-in Q2 → US "sell-the-confirmation" chip rout** (MU −6%, SNDK/MRVL −5%, INTC/ARM −4%); **Strait of Hormuz tanker attacks → oil spike** (Brent +3% → +5.6% after hours as the US revoked Iran's oil license); **SPCX joined the Nasdaq-100 but FELL ~7%** to ~$149.58 (forced-buy thesis failed); **Amazon launched a ≥$25B AI-capex bond sale**; **DeepSeek reportedly building its own AI chip** (NVDA dipped then rebounded on a Kyber-delay denial); **META launched Muse Image + got an upgrade** (outperformed). **0 promotions. Universe stays 26.** **NOT HALT-WORTHY:** no FOMC (minutes 7/8 only); held names not adversely shocked (META positive, MU is a competitor read-through); equity futures did not gap >2% (oil did, equities didn't).
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used the venv. **IMPORTANT: use `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` and run from the repo root (`cd` or absolute path) before EVERY CLI call — the shell cwd drifts between calls.** Operator action still required (open questions).
- **BROKER STATE RESTORED (was the 7/7 09:09 P0 wipe).** During this run `positions` returned all four longs (AVGO 26 / META 16 / MU 7 / ORCL 38); equity **$103,106.76**, cash **$71,809.59**, day_trade_count 0. The 9 AM "flat account" the trader froze on appears **transient/self-resolved** (Alpaca paper glitch). Flagged in the brief for the trader's reconciliation; news agent does not reconcile.
- **Universe: 26, unchanged.** `list-active` → universe 26, claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**, all `revalidate_by 2026-07-21`. `gap-registry coverage_holes` = **empty** (confirmed again).
- **SPCX joined the Nasdaq-100 today (7/7) but stays PROVISIONAL / execution-quarantined** — Saturday research has not cleared it. Fell ~7% on the day; at ~$150 it's below the >$175.50 "30% rule" unlock threshold. **Non-tradable** until validated.
- **Re-bootstrap artifact to watch:** the 7/7 state reset re-stamped the `equity_trend_following_ema_cross` / `equity_event_driven_catalyst` / `equity_pairs_trading_cointegration` claim *reasons* to "PROVISIONAL/UNVALIDATED … QUARANTINED" with `since 2026-07-07`, while the structured `provisional_claims` field still lists only QCOM/SPCX/SYNA. Trader/Sat-research should reconcile which claims can actually execute.
- **Alpaca density: 130 items.** SPCX 18, MU 14, AAPL 12, NVDA 10, TSLA 9, MSFT 8, SNDK 8, META 7, QQQ 7, AMZN 6, GOOGL 6, INTC 6, DELL 5, JPM 4, MRVL 3, SPY 3, ARM 1, AVGO 1, ORCL 1, QCOM 1; CBRS/CSCO/HPE/NUVL/SYNA/TSM 0. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline FRESH today** (dated 2026-07-07). Prior: 7/6 fresh, 7/3 holiday brief fresh, 7/2/7/1/6/30 fresh; earlier misses 6/22, 6/25, 6/29. Staleness-guard ask still stands (open questions).

## Notable carry-forwards

- **MEMORY COHORT — the live story.** Samsung Q2 (record, DRAM +44%/NAND +53% ASP, but −8% "sell-the-confirmation") drove MU/SNDK lower; SK Hynix US listing ~7/10 adds a funding-rotation risk ("will MU/SanDisk foot the bill?"). **Fundamentally the pricing cycle looks intact — the selloff is positioning.** MU (held) −5.6% mark; watch trailing-stop/give-back. Micron-Ford/GM SCAs carry. Sustain-check tomorrow: does the rout extend or reverse?
- **AMZN (universe) — ≥$25B AI-capex bond sale (NEW).** 8 tranches, ~$54B raised YTD, ~$200B 2026 capex; Q2 earnings 7/30. Capital-allocation event; no responder. Feeds the "AI debt binge" theme (MSFT/GOOGL/META/ORCL adjacent).
- **NVDA — DeepSeek in-house AI chip report (NEW competitive threat) + Kyber-delay DENIAL (NEW).** NVDA rebutted the roadmap-slip; MRVL competitive-window thesis faded. No responder.
- **META (held) — Muse Image AI product launch + analyst upgrade (NEW, positive); outperformed.** Offsetting: addiction-litigation "$1.4T penalty scare." Position rides its MACD rule; news is responder:NONE. Track cloud/AI-capex + trial calendar.
- **SPCX (PROVISIONAL/quarantined) — Nasdaq-100 add TODAY, fell ~7%.** Same-week initiation cluster (Goldman $205, Morgan Stanley/Jonas ~90%, JPMorgan 91% CAGR, +64% call; consensus ~$188.57). FCC vote 7/22. Track the post-add price path; still non-tradable.
- **INTC — Syntiant (Intel-backed edge-AI) files Nasdaq IPO (NEW, minor)** + down 4% in the rout; **Q2 earnings 7/23** (window opens ~7/9). No responder.
- **JPM — Q2 earnings Tue 7/14, window OPEN, most urgent.** ~$5.44/sh, +9.7% YoY; $50B buyback effective 7/1. Also Fiserv exploring STAR debit-network sale (non-universe). Earnings-window responder does NOT claim JPM (trend-following does) → assignment gap.
- **TSLA — binary is 7/22 earnings** (margins). No fresh hard event; DOGE sunset, Optimus/robotics-ROI commentary soft. Earnings-window assignment gap. IV builds.
- **GOOGL — joined ~$411–469M Proxima Fusion (German nuclear-fusion) round (NEW, minor).** Dow-30 inclusion was 6/29 (carry — NOT a fresh event; don't re-report). DST-tariff/UK-regulatory overhang carry.
- **DELL — Trump "buy a Dell" endorsement rally continues (soft, carry).** Trump-Accounts first 500k funded. Not modeled.
- **Regulatory cluster (carry) — DST-tariff, UK under-16 ban, Meta addiction litigation, GOOGL EU €4.1B, + SEC quarterly-reporting shake-up (NEW).** No responder. Track threat→action.
- **Vol regime — VIX ~16.13 (+3.6%), a bounce off benign; normal contango.** Index vol low-teens. Vol lives in single-name event-IV (SPCX/JPM/TSLA/INTC/AMZN) + the new oil tail from Hormuz. UOA: bullish call sweeps NVDA ($200 0DTE), MU ($930 7/10).
- **Macro/geopolitics — Hormuz escalation (oil +3%/+5.6% after hours; US revoked Iran oil license); FOMC June minutes 7/8; June NFP +57k dovish (carry); CPI/PPI/PCE later in July into late-July FOMC.**

## To do on the next run (Wed 2026-07-08)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A (3 consecutive catalyst sessions, uncapped) + Tier B (5 triggers, 2/day cap). Both require `--sector`.
2. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` AND run from the repo root** for EVERY CLI call. Bare `python3` fails; the cwd drifts between Bash calls.
3. **FOMC June minutes 7/8** — cover the release (macro category); tone on the rate path under Chair Warsh. Not a decision; not halt-worthy on its own.
4. **Hormuz follow-through** — did the oil spike / US-Iran escalation widen overnight? Check equity-futures gap at the open and whether VIX repriced. This is the item most likely to shift the halt-worthy call if it escalates.
5. **Chip-rout sustain-check** — does the Samsung-driven memory selloff extend, or bounce (dip-buying flow suggests some fade)? MU (held) / SNDK / MRVL / INTC / ARM.
6. **Confirm universe 26 / unclaimed 0 / provisional 3 (QCOM, SPCX, SYNA).** Re-check SPCX (post-add, still quarantined). Reconcile the re-stamped trend-following/event-driven/pairs claim reasons vs the structured provisional field.
7. **Re-snapshot account/positions** — confirm the book stays INTACT (the 09:09 wipe was transient this run). Flag any recurrence for the trader.
8. **AMZN bond-sale follow-through** (pricing/tranches) + Q2 7/30 window. **META Muse Image / upgrade** follow-through. **NVDA DeepSeek-threat + Kyber-denial** follow-through.
9. **SK Hynix US listing ~7/10 (Fri)** — memory read-through; SKHY becomes a promotable universe candidate once it trades. **Syntiant IPO** — watch pricing (not promotable until it trades).
10. **JPM Q2 7/14** (window open, most urgent), **TSLA 7/22, INTC 7/23, AMZN 7/30** — flag IV build; earnings-window assignment gap (trend-following claims, not event-driven).
11. **Vol regime** — VIX vs ~16; index vol vs the oil tail; event-IV. Log concrete UOA on universe names only.
12. **Promote candidates if Wednesday refreshes:**
    - **SK Hynix (SKHY)** — post-listing add candidate once it trades (~7/10); memory cohort (technology). Not promotable until it has a US ticker.
    - **RIVN** — clock reset by today's dilutive public offering; promote only on its own *earnings* beat-and-raise+5% or a clean 3-session catalyst run.
    - **CRDO** — AI-interconnect; absent again. Promote on a fresh same-week 3-bank initiation cluster OR own beat-and-raise+5%.
    - **Syntiant** — Intel-backed edge-AI IPO filing; not addable until it trades.
    - **WDC / STX / CRWV / NBIS** — memory / neocloud sympathy; Tier-A/B only.
13. **Outlier movers + sector breakdown.** Generic gainers/losers query STILL screen-level (~25 consecutive sessions; today EOSE +6.7%, PLCE −2.8%, none universe-relevant) — per-name reconstruction remains the workable path. Today's non-universe catalysts were thin.
14. **Library gaps re-listing.** Carry (see brief): competitor-earnings/sector read-through (Samsung→memory, NEW); capital-allocation/debt-raise (AMZN NEW + JPM buyback); product-launch/competitive-threat (META Muse, NVDA DeepSeek, NEW); index-inclusion/forced-flow (SPCX, SK Hynix; NEW_CATEGORY_NEEDED); earnings-window assignment (JPM 7/14, TSLA 7/22, INTC 7/23, AMZN 7/30, CBRS); regulatory/antitrust (DST-tariff, UK ban, Meta addiction, SEC reporting); pricing/restructuring (INTC/MSFT); M&A-arb (SYNA/onsemi); vol-regime activation (single-name IV + oil tail). Sat research = next.

## Open questions for the operator

- **[HIGH → likely RESOLVED] 7/7 09:09 broker-state "wipe."** This run's snapshot shows the account INTACT (4 longs back, equity $103,106.76, cash unchanged $71,809.59) — the earlier flat-account read looks transient/self-resolved. Operator: confirm on the Alpaca paper dashboard whether a reset/glitch occurred and whether the trader's FREEZE can lift. Last-good book is in the 7/7 handoff.
- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install requirements into 3.14). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Also: the Bash shell cwd drifts between calls — always run from the repo root.
- **[HIGH] News-agent schedule stability + brief-staleness guard.** Earlier misses 6/22, 6/25, 6/29; 6/30–7/7 fresh. Asks: (a) stabilize schedule / add a health-check alert on miss-or-double; (b) `_load_news_brief()` staleness guard — parses date_in_file but never compares to today; a stale brief should be rejected/down-weighted, not fed as live signal.
- **[MEDIUM] Trader task fired off-schedule 7/7 09:09 mid-session** (and 7/3 holiday). Confirm the intended trigger; the trader executing mid-session on a stale brief is undesirable. This news run fired correctly (post-close ~3:40 PM PT).
- **Re-bootstrap claim-state reconciliation.** The 7/7 reset re-stamped trend-following/event-driven/pairs claim *reasons* to PROVISIONAL/QUARANTINED (`since 2026-07-07`) while `provisional_count` stays 3 (QCOM/SPCX/SYNA). Which claims can actually execute? Trader/Sat-research call.
- **SPCX past its (reset) 7/21 deadline path.** Joined the Nasdaq-100 (7/7) while quarantined; fell ~7%. Operator: decide whether an index-add forced-flow name warrants an expedited validation path, or accept it stays non-tradable.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX 7/7; SK Hynix ~7/10).** Forced-flow gap keeps recurring.
- **Earnings/delivery-window assignment — JPM (7/14, most urgent), TSLA (7/22), INTC (7/23), AMZN (7/30), CBRS.** Earnings-window responder doesn't claim these (all trend-following). Sat: assign.
- **New event-window sub-triggers (recurring) — competitor-earnings read-through (Samsung→memory), capital-allocation/debt-raise (AMZN/JPM), product-launch/competitive-threat (META/NVDA), regulatory/antitrust (cluster + SEC), pricing/restructuring (INTC/MSFT).** No rule reads any of these.
- **M&A-arb activation, live universe instance (SYNA / onsemi).** `equity_pairs_trading_cointegration` declares pairs_arbitrage but only provisionally claims SYNA. Sat: activate merger-arb (long SYNA / short ON at 1.350).
- **Mandatory-attach doctrine (Option 3) — confirm permanent.** Three provisional claims live (QCOM, SPCX, SYNA).
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** Errors `'dict' object has no attribute 'id'` when a live open order exists; clean when none. Fix the order-serialization path.
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate; only the Jun-1 test files sat in `.git-sync-queue/` as of last check.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **130 items** cleanly (via venv). CBRS/CSCO/HPE/NUVL/SYNA/TSM 0.
- `cli market-status` → `is_open: false`, **`next_open_iso: 2026-07-08T09:30:00-04:00`**, `now_iso: 2026-07-07T15:39 PT` (canonical post-close run).
- `cli list-active` → universe 26, claimed 26, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA, all `revalidate_by 2026-07-21`). `gap-registry coverage_holes` empty.
- `cli positions` / `account` → 4 longs INTACT (AVGO/META/MU/ORCL), equity $103,106.76, cash $71,809.59. Marks: META +1.6%, AVGO −2.4%, MU −5.6%, ORCL −20.1%.
- WebSearch strong Tue: Samsung Q2 record ~89.4T won op profit / −8% stock (Bloomberg/Yahoo/itechpost); VIX ~16.13 +3.6% (Cboe/Yahoo); Hormuz tanker attacks + Brent +3%/+5.6% AH + US revoked Iran oil license (CNBC/NPR/Bloomberg); AMZN ≥$25B bond sale (Bloomberg/CNBC/Yahoo); SPCX ~$149.58 (−~7%) + initiation cluster Goldman $205 / Morgan Stanley ~90% / JPMorgan 91% CAGR (Benzinga/Yahoo); FOMC June minutes 7/8 (Kiplinger/gomarkets); NVDA UOA $200 0DTE / MU $930 sweep (OptionCharts).
- WebSearch weak: generic "biggest gainers/losers" still screen-level (EOSE +6.7%, PLCE −2.8%, no universe-relevant clean catalyst); RIVN moved on a dilutive public offering (negative), not a fresh beat-and-raise.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** No clean 3-consecutive-catalyst run. RIVN did NOT advance (today's public offering is a new *negative* event, not a continuation). CRDO absent; WDC/STX/CRWV/NBIS sympathy. **No Tier-A promotion.**
  - **Tier B:** No qualifier on a *candidate*. The only 3+ bank initiation cluster (SPCX) is already a universe member; RIVN's raise is dilutive (fails #3); no new M&A target (Fiserv is a unit-sale, not a takeover, and not a tracked candidate; SYNA already in); no FDA binary; no candidate Tier-1 customer win. **No Tier-B promotion.**
  - **Decision: 0 promotions. Universe stays 26.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
