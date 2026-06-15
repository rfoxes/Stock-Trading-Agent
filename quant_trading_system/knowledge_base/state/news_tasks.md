# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Mon 2026-06-15). Risk-on relief day: (1) **US-Iran peace deal "complete"** — Hormuz reopened, Navy blockade removed, oil −5%, 10y yields to 1-month lows, S&P +1.9%; resolves the active exchange from the 6/10 brief. Signing Fri 6/19 in Switzerland (Israel-Lebanon strikes = durability tail risk). (2) **VIX −9% to 17.68** — first decisive break below 20 after 3 weeks of oscillation. (3) **Book rallied hard**: MU flipped −11.5%→**+9.98%** ($1,081) on a ~12% pop into its 6/24 print (PTs to $1,250, bullish UOA); ORCL (Wed buy now filled) +8.25% after rebounding 5% off last week's capex-shock low (BofA/Goldman bullish). (4) **FOMC 6/16-17 — hold ~97%, dot plot Wed is the live catalyst** (lands the session AFTER the 6/16 trader run). (5) **Anthropic forced to disable Fable 5/Mythos 5 for all foreign users** (Trump export-control order) — AI-sector national-security overhang. Not HALT-WORTHY (de-escalation, not a shock). 
- **CATCH-UP / GAP:** This was the first brief since **Wed 2026-06-10**. Thu 6/11 and Fri 6/12 news runs did NOT update state (last_handoff/news_brief/news_tasks all still dated 6/10). Mon's brief folds in Thu-Fri events (SpaceX priced Thu/listed Fri; ADBE printed Thu; Iran deal reached over the weekend). Operator: confirm whether the scheduled news task fired Thu/Fri and silently failed.
- **DEPLOYMENT WAS BROKEN AT START OF RUN — repaired.** The `.venv` interpreter was orphaned when Homebrew auto-upgraded `python@3.13`→`python@3.14` (venv's python3.13 symlink → `/opt/homebrew/opt/python@3.13` which no longer existed; bare `python3` is now 3.14 with NO `requests`/`alpaca`). **Fix applied: `brew install python@3.13`** restored the symlink and the venv's intact site-packages now import cleanly. **For this run all CLI calls used `.venv/bin/python3 -m quant_trading_system.cli` instead of bare `python3`.** See operator question below — the scheduled-task launcher must use the venv python, or future runs break the same way.
- **Universe last covered:** 22-name (unchanged). Mon Alpaca densities (100 items total, vs Wed 135): TSLA 17, AMZN 13, NVDA 10, GOOGL 9, META 8, MSFT 8, AAPL 6, MU 6, QQQ 5, ORCL 4, SPY 4, INTC 3, TSM 3, AVGO 1, CBRS 1, DELL 1, MRVL 1, ARM 0, CSCO 0, HPE 0, JPM 0, NUVL 0. Heavily SpaceX/Iran/Musk-flow weighted. All 6 category HTMLs + daily summary written. Cleanup deleted 0 (cutoff 2026-03-17).
- **Live broker snapshot (this run, not a trader handoff):** equity **$108,589** (+4.8% vs Wed $103,576), cash $25,327 (net-long). Held: AAPL 72 (+8.88%), MU 7 (+9.98%), ORCL 38 (+8.25%, Wed buy filled @ $177.28), QQQ 28 (+14.44%), SPY 35 (+6.29%). Regime: bull, conf 0.75, ADX 24.98 (cooling from 27.41). 22/22 claimed, unclaimed_count == 0.
- **Zero promotions Mon.** Tier-B daily cap untouched. Tier-A clock advanced for nobody (gap means no consecutive-session refresh).

## Notable carry-forwards

- **FOMC June 16-17 — dot plot Wed 6/17 is THE live catalyst.** Hold priced ~97%. Decision lands the session after the 6/16 trader run. A hawkish dot-plot revision is the main 48h risk to the AI-cohort multiple. Tue 6/16 news run = pre-FOMC posture; Wed 6/17 run confirms the outcome.
- **MU Q3 FY26 = Tue 6/24 AMC.** Held long, now +9.98%. PTs to $1,250; bullish UOA into the print. Pre-print window open. Watch for IV expansion; the print is the next single-name catalyst.
- **ORCL post-capex-shock recovery.** Wed catalyst buy (38 @ $177.28) filled, now +8.25%. The asymmetric beat+capex print resolved to the UPSIDE (+5% Mon). Validates `equity_event_driven_catalyst`. Watch sell-side follow-through on the $40B FY27 raise.
- **US-Iran deal signing Fri 6/19 Switzerland.** Track durability — Israeli strikes in Lebanon flagged as a tail risk. Any breakdown headline = oil/vol re-rate risk into the weekend.
- **Anthropic Fable 5 / Mythos 5 export-control ban.** Models disabled for all foreign users; controls expected to lift once safety remediated. Track: (a) when models return, (b) NVDA-China spillover, (c) Mark Zandi "massive threat to AI optimism" framing, (d) EU sovereignty response.
- **SpaceX (SPCX) listed Fri 6/12 at ~$2T** — largest IPO ever; Mon volume > AAPL+MSFT+TSLA+META+GOOGL combined. **Options debut Tue 6/17** (first SPCX options, day before Fed). "FAB 10" reframing (Mag-7 + OpenAI/SpaceX). JPM lead underwriter = realized franchise event. **Session-1 watch as universe candidate** (does NOT meet a Tier-B trigger — IPO isn't one of the five; hyper-volatile new listing). Track recurrence.
- **TSLA SpaceX-merger chatter** (analysts: no merger this year); Direxion 2X SPCX ETF (LOFF) launched. FSD-Europe "inflated safety claims" report = minor offset. No position.
- **GOOGL $1.5B Alabama data-center expansion** disclosed Mon. Concrete capex; +3%+. No position (exited 6/10).
- **Trump 100% French-wine tariff threat** over France's digital tax (AAPL/AMZN/META/GOOGL), ahead of G7. Posture not action; track G7 outcome.
- **ADBE Q2 (Thu 6/11):** beat + raised guide but −6% (H2 ARR cut, 10th straight quarter of deceleration; Anthropic "Claude Design" disruption narrative). **Tier-B #3 audit FAILED.** Not in universe.
- **ROKU takeover speculation** (Needham Buy + JPM "Comcast most logical buyer"). Analyst speculation, NOT a confirmed deal — does not qualify Tier-B #1. Watch for an actual named bid.
- **Chip cohort relief:** TSM +4%, INTC +3%, AMD +4%, NVDA +2%, MU +12% — last week's AVGO/ORCL capex-scare selloff reversed. Whale-alert screen flagged MU/TSM/INTC (universe) Mon.
- **NUVL/GSK deal** — pre-close, trades freely. No fresh development Mon (0 Alpaca items). PDUFA 2026-11-27 binary.
- **MRVL + FLEX S&P 500 inclusion 6/22** — passive-flow window this week. No fresh Mon item.
- **VIX below 20 (17.68).** Vol-regime shift; IV compression favors vol-selling. `iron_condor_high_iv` claims no universe symbol. Track whether the FOMC re-inflates front-end IV.
- **S&P concentration at "railroad-era" extreme** (Bianco); non-AI names +~1% YTD. Eisman "rotating away from hyperscalers." Structural backdrop.
- **`SYMBOL_TO_SECTOR` map in `news_service.py` incomplete** — TSM/INTC/CBRS/ORCL → uncategorized historically; the `cli news-universe` sector_map now resolves these to `technology` correctly, but verify the underlying map. Hygiene carry-forward.

## To do tomorrow (next news run, Tue 2026-06-16)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier A (3 consecutive sessions, uncapped) + Tier B (5 single-event triggers, 2/day cap). Both tiers require `--sector` on `cli promote-candidate`.
2. **USE `.venv/bin/python3`** for all CLI calls until the operator confirms the scheduler/PATH uses the venv. Bare `python3` = Homebrew 3.14 with no deps and WILL fail `news-fetch`/`news-universe`. (`brew install python@3.13` already applied; venv works.)
3. **Universe is 22-name.** `cli news-universe` Tue should confirm.
4. **PRE-FOMC posture (Tue).** Dot plot Wed 6/17. Note: hold ~97% priced; the dot plot is the catalyst. Tue news run = pre-event; Wed run = outcome + AI-cohort reaction.
5. **MU pre-print Day-N (6/24 AMC).** Sell-side follow-through on the +12% Mon move / PT-to-$1,250 calls. UOA refresh. Held long.
6. **ORCL post-recovery follow-through.** Did the +5% Mon rebound extend? Sell-side on the $40B FY27 raise post-relief-rally.
7. **US-Iran deal durability.** Pre-signing (Fri 6/19) headlines; Israel-Lebanon strike risk; oil direction.
8. **Anthropic export-control Day-N.** Did models return? NVDA-China spillover? Mark Zandi / EU sovereignty follow-ups.
9. **SPCX options debut Tue 6/17.** Track the new listing's vol/flow; "FAB 10" recurrence; whether SPCX keeps appearing as a candidate.
10. **GOOGL Alabama data-center sell-side sizing.** Capex-deployment narrative.
11. **G7 summit / French digital-tax tariff thread.** Any escalation or resolution.
12. **Chip cohort follow-through** (TSM/INTC/MU/ARM/MRVL) after the relief bounce.
13. **MRVL + FLEX 6/22 inclusion** passive-flow window updates.
14. **Promote candidates if Tue session refreshes (consecutive-session rule; counters did NOT advance over the 6/11-6/12 gap):**
    - **CRWD** provisional 3 → needs a fresh Tue appearance to formalize Tier-A promote (sector technology).
    - **STM / FLEX / PINS** at 2 → Tue refresh → session 3 → Tier-A promote.
    - **VSH / SMCI** at 1 → Tue refresh → session 2.
    - **SPCX** session-1 watch (not Tier-B-eligible; recurrence/operator call).
15. **Outlier movers Tue + sector breakdown.** Mon non-universe screen: gainers AXTI +14.8%, STX +9%; losers FOX −17.8%, SSL −11.5%, BAND −11.4% (catalysts unconfirmed — generic gainers/losers query still flaky). Per-name reconstruction remains the workable path.
16. **Vol regime Tue.** Did VIX hold below 20 or re-inflate into the FOMC? VIX9D vs VIX.
17. **Library gaps re-listing.** Reaffirmed: `macro_event_window` (FOMC dot plot + Iran resolution), `volatility_regime` (VIX<20 break, registry coverage hole), AI-policy/export-control overlay (Anthropic ban), `underwriter_franchise_event` (JPM/SpaceX), `m_a_arbitrage_event` (NUVL), capex-shock asymmetric-reaction detector (ORCL, now upside-resolved). Sat research = next opportunity.

## Open questions for the operator

- **DEPLOYMENT: venv interpreter orphaned by Homebrew python upgrade.** Homebrew upgraded `python@3.13`→`python@3.14`, breaking the `.venv` (its python3.13 symlink pointed at the removed `/opt/homebrew/opt/python@3.13`). **`brew install python@3.13` restored it** and the venv's site-packages import cleanly again. **Operator action:** (a) confirm the scheduled-task launcher invokes the venv python (`.venv/bin/python3` or an activated venv), NOT bare `python3` — otherwise every future run breaks the same way; (b) consider pinning python@3.13 against brew auto-upgrade, or rebuilding the venv on 3.14 with reinstalled wheels.
- **News-run gap Thu 6/11 + Fri 6/12.** No state updates those days (files dated 6/10). Likely the same venv-break cause (homebrew upgraded between 6/10 and 6/15). **Operator action:** check scheduled-task logs for Thu/Fri failures; the deployment break probably silently killed those runs.
- **News-brief / trader-schedule lag (carry-forward).** Still open: ensure the 3:30 PM PT news run completes before the 4:00 PM PT trader run. This run executed at ~3:40 PM PT local; timing OK today.
- **Candidate-counter mechanism (carry-forward).** The 3-session Tier-A rule remains judgment-call; CRWD provisional-3 still unconfirmed. Operator: formalize a mechanical counter so gaps (like 6/11-6/12) don't ambiguously reset/freeze the clock.
- **FLEX index-inclusion not among the 5 Tier-B triggers (carry-forward).** Should index-inclusion become a 6th Tier-B trigger?
- **`cli open-orders` parser bug (carry-forward from trader handoffs):** returns `'dict' object has no attribute 'id'`. Not a news-agent path but flagged for the operator.
- **`bash scripts/install_git_safety.sh` LaunchAgent status.** `git-doctor` shows 1 pending marker (`marker_test.json`) — a single test marker, not a pileup; likely fine. Verify `launchctl list | grep harness` if markers accumulate.
- **NUVL biotech-vs-tech-universe mismatch (carry-forward).** Provisionally claimed by `equity_trend_following_ema_cross`; Sat research owns proper claim + `m_a_arbitrage_event` gap.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **100 items** cleanly (via `.venv/bin/python3`) — TSLA/AMZN/NVDA/GOOGL anchored; ARM/CSCO/HPE/JPM/NUVL had 0. Lower count than Wed (135) — the tape was dominated by macro (Iran deal) + SpaceX/Musk flow rather than diversified single-name catalysts.
- WebSearch returned strong results for: US-Iran peace deal (CBS/NPR/NBC/Fox/NewsNation); FOMC June 17 expectations (Polymarket/iShares/StreetStats); VIX 6/15 (Saxo/CBOE/Yahoo — 17.68, −9%); ADBE Q2 (Adobe IR/Yahoo/Seeking Alpha/TechTimes); Anthropic export ban (Axios/Time/Fortune/Al Jazeera/Nextgov); MU options flow (Barchart/Yahoo/OptionCharts).
- WebSearch returned weak results for: generic "biggest gainers/losers June 15" (Slickcharts/Morningstar surfaced partial screen-level names only; catalysts unconfirmed) — per-name reconstruction still the workable path (now ~11 consecutive sessions of this query being flaky).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** CRWD (3), STM (2), FLEX (2), PINS (2), VSH (1), SMCI (1) — none refreshed; counters frozen at 6/10 levels by the 6/11-6/12 run gap. Held.
  - **Tier B:** No qualifiers. ADBE failed #3 (negative post-print). ROKU = speculation, not confirmed M&A (#1). SPCX IPO is not a Tier-B trigger. No #2/#4/#5.
  - **Decision: 0 promotions. Universe stays at 22.**
- Previous notes (still held): "CPI <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
