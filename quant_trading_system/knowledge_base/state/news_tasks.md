# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NORMAL FLOW (2026-06-04 Thu, post-close). AVGO Q2-print Day-1 cash reaction was the loudest event (-12.59% to $418.91; ~$300B mcap vaporized; Q3 AI guide $16B vs $17.2B) but analyst PT raises ran the opposite direction (Jefferies $550, Wells Fargo $545, Morningstar ~$650; "intentionally sandbagged" framing) and broad tape recovered (S&P +0.41% to 7,584.31, Health Care +3.14%, Financials +2.67%, Real Estate +1.87% led; Nasdaq -0.09% on chip-cohort drag). Material positive Thu single-name catalysts: **Apple Siri 2.0 to launch Sept 2026 with iOS 27 using NVDA Blackwell B200 GPUs in Google Cloud + Gemini** — Tier-1 enterprise win flowing AAPL/NVDA/GOOGL. **AMZN €10B European warehouse robotics + $4B Pinterest AWS commitment**. **JPM tech-to-financials rotation + Dimon personally pitching SpaceX $75B IPO to 2,500 wealthy clients**. **FCC undersea cable rules favor META/GOOGL**. Private-credit gate Day-2 (Blackstone BCRED 10% requested / 5% fulfilled, Day-2 of Cliffwater cluster). Jobless claims 225K highest since Feb but holiday-distorted. VIX 16.06 (+0.29) sub-threshold; 1-day VIX +29.3% to 11.48 = NFP pre-event hedging. Iran-Hormuz calmed (oil eased). House war-powers 215-208 symbolic. **NFP May releases Fri 6/5 at 8:30 AM ET — the week's real macro event.**
- **Universe last covered:** **17-name** (AAPL, AMZN, ARM, AVGO, CSCO, DELL, GOOGL, HPE, JPM, META, MRVL, MSFT, MU, NVDA, QQQ, SPY, TSLA). Universe grew 10 → 14 (operator Wed-overnight: ARM/CSCO/HPE/MRVL) → 17 (news-agent Thu in-session: AVGO/DELL/MU promoted under §9 3-session rule). Final Thu Alpaca densities: AVGO 32, NVDA 16, META 10, GOOGL 9, AMZN 8, MSFT 8, AAPL 7, JPM 6, QQQ 6, TSLA 6, SPY 5, MU 5, MRVL 3, DELL 2, HPE 1, ARM 0, CSCO 0. **Code fix to `news_fetch`** so operator extras flow through automatically (was using `settings.watchlist + positions`; now uses `compute_universe`). All six category HTMLs written. Daily summary written. Cleanup deleted 0 (cutoff 2026-03-06).

## Notable carry-forwards

- **NFP May print Fri 6/5 8:30 AM ET.** The week's anchor macro event. ADP+ISM hot stack Wed + jobless claims 225K Thu set up the trifecta read. Watch: print vs consensus, average hourly earnings, participation rate, unemployment rate. Fed-policy implication is the through-line — any hot print revives Yardeni July-hike chatter (currently 97.8% June hold on Polymarket / 99.4% CME).
- **AAPL WWDC June 8-12 (Mon-Fri).** Five-day event window opens Mon. Siri 2.0 architecture (Blackwell + Gemini) is the headline reveal. Morgan Stanley PT $440 framing. Trader has no event-window posture rule; news layer should flag the window every Mon-Fri next week.
- **AVGO Day-2 (Fri 6/5).** Analyst PT-raise digestion: does the sell-side bullish framing translate to a Day-2 bid? Watch: (a) any sell-side INITIATIONS at $550+ PTs, (b) cohort follow-through on NVDA/MRVL/MU, (c) any reframing of $73B backlog as the bull signal.
- **NVDA continuation of Apple Siri-Blackwell win.** Day-2 sell-side commentary on the Apple anchor account; any cohort read-through to TSM. Confidential-compute feature gets attention.
- **GOOGL Day-5 of $84.75B raise + Apple Gemini anchor.** Two competing narratives: dilution overhang vs Tier-1 enterprise customer win. Watch Class A/C divergence; any Berkshire incremental commit; sell-side EPS-dilution sizing (still no detailed math 5 days in).
- **JPM Day-2 of Dimon SpaceX pitch.** Wed's 2,500-client pitch — any pricing momentum signals; any subscription-tier disclosure; Robinhood retail-allocation framing.
- **Blackstone BCRED + Cliffwater private-credit gate cluster.** Two names in 48h; is there a third coming? Watch Apollo, KKR, Ares private credit fund flows for confirmation.
- **CSCO/HPE/MRVL/ARM (now in universe).** First full session as universe members. Operator/news-agent needs to ensure `news/stocks/<SYM>/` subdirs exist for fetcher to populate. Action: pre-create or let fetcher auto-create.
- **TSMC capacity-constraint pricing-power signal.** TSMC CEO C.C. Wei: AI capacity tight "very long time" + hint at price hikes. Direct read for NVDA/AVGO/AMD margins. Day-2 sell-side: does anyone size the pricing-power impact?
- **Iran-Hormuz stabilization.** Thu oil eased; Wed missile-shock Day-2 not materializing. Watch: any re-escalation, any Strait reopening signals, any oil gap.

## To do tomorrow (next news run, Fri 2026-06-05)

1. Run the standard workflow (`news_manual.md` §"Workflow"). **Re-read §9 every run.** §9 now has TWO promotion tiers:
   - **Tier A (3-session recurrence)** — uncapped; act on every qualifier.
   - **Tier B (single-event triggers)** — capped at 2 promotions per news run; triggers: confirmed M&A target, FDA approval/rejection on binary date, earnings beat+raised guidance+stock +5% post-print, sell-side initiation cluster (3+ banks in same week), Tier-1 customer-win disclosure.
   - **Both tiers require `--sector <sector>` on `cli promote-candidate`** (newly enforced as of Thu code change). When in doubt for chip/software/internet names, `technology` is right.
   - If `fetch_and_write` returns a non-empty `pending_sector_assignment`, that means a symbol entered the universe without a sector entry — fix it immediately with `cli promote-candidate <SYM> --sector <sector> --agent news --reason "backfill"` (idempotent).
2. **NFP May print review — Fri 8:30 AM ET.** This is the headline Fri event. Cover the print (consensus, beat/miss, AHE, UR, LFPR), the curve reaction (yield surge or relief), the FOMC odds shift (CME/Polymarket), any sell-side reframing of the Yardeni July-hike call. Front-load this in the brief.
3. **AVGO Day-2 cohort follow-through.** Sell-side digestion of Thu's PT-raise wave; Day-2 cohort behavior on NVDA/MRVL/MU.
4. **AAPL/NVDA/GOOGL Apple Siri-Blackwell Day-2.** Sell-side reactions; any cohort enterprise-win read-through; TSM-Apple-NVDA value-chain framing.
5. **WWDC June 8-12 prep.** Set up the five-day Apple event window. Morgan Stanley $440 PT framing; what other sell-sides initiate?
6. **JPM Dimon SpaceX pitch Day-2.** Pricing momentum; any IPO allocation news.
7. **Private credit gate Day-3 watch.** Apollo/KKR/Ares flow signals; any third major gate?
8. **CSCO/HPE/MRVL/ARM news coverage.** Subdirs now exist after Thu's in-session fix to `news_fetch`. Track their first full session of meaningful coverage Fri (Thu was MRVL 3 / HPE 1 / ARM 0 / CSCO 0).
9. **Iran-Hormuz status update.** Overnight oil; Strait status; any re-escalation.
10. **Macro carry-forwards:** Beige Book "E-shaped" framing follow-on; BofA June seasonality call sell-side echo.
11. **VIX Fri close + NFP-day vol surface behavior.**
12. **TSMC pricing-power signal sell-side sizing.**
13. **Outlier movers Fri** — try later-evening / next-day query framing (5-session pattern of same-day staleness is now confirmed; may need to wait until Sat afternoon or use "Friday June 5 2026 close" specifically).

## Open questions for the operator

- **AVGO / DELL / MU — PROMOTED Thu in-session** under `news_manual.md §9` 3-session rule. All three now in `state/extra_symbols.md`; subdirs exist; news coverage live. Strategy assignment pending research-agent / head-to-head.
- **STM inclusion** — 2nd session of STRONG-candidate framing; +190% YTD on Starlink relationship pre-SpaceX IPO.
- **TSM inclusion (NEW)** — Thu's TSMC CEO capacity-constraint pricing-power signal makes the case fresh. Direct AI-pricing-power read for the foundry layer. Would broaden the universe beyond design houses.
- **PINS inclusion (NEW, soft)** — material catalyst Thu (+$4B AWS commitment); single-session event so below STRONG threshold but worth a watch slot.
- **`bash scripts/install_git_safety.sh` LaunchAgent status.** Per Wed handoff, claimed install completed but `cli git-doctor` showed pending_marker_count=8. **Operator action: verify `launchctl list | grep harness` and gitrunner logs.** Markers persist on disk; nothing is lost. Top operator priority carries forward.
- **ARM/CSCO/HPE/MRVL subdirectory creation — RESOLVED in-session.** Root cause was `agent_tools.news_fetch` building its universe from `ctx.settings.watchlist + positions` instead of the composed universe (which includes `operator_extras` from `state/extra_symbols.md`). Fix applied Thu: `news_fetch` now calls `universe.compute_universe(...)`. CLI help text in `cli.py` updated accordingly. Per-symbol HTMLs for the 4 new names were generated in the same Thu session (MRVL 3, HPE 1, ARM 0, CSCO 0 items). Operator additions to `extra_symbols.md` now flow into news-fetch automatically — no manual subdir creation and no need to use `promote-candidate` just to get subdir creation.

## Operational notes

- `cli news-fetch` returned 84 items cleanly (no proxy errors). NVDA density 17 (Apple Siri Blackwell + TSMC + AVGO read-through cohort). Total down from Wed's 97 — consistent with NORMAL FLOW (less event density than Wed's three-event-stack day).
- WebSearch returned strong results for: AVGO Day-1 + analyst PT raises (Motley Fool / Yahoo / Invezz / IBTimes), Apple Siri NVDA Blackwell + Google Cloud (MacRumors / 9to5Mac / AppleInsider / MacDailyNews), VIX 16.06 (Saxo Market Quick Take), S&P 7,584.31 + Nasdaq 26,830.96 (TheStreet), jobless claims 225K (Bloomberg / Reuters), House war powers 215-208 (CNN / NPR / Time / WaPo), Blackstone BCRED gate (SEC filings + Benzinga), FOMC June 97.8% hold (Polymarket / CME), NFP May Fri 6/5 8:30 ET (BLS schedule), Iran-Hormuz status (Wikipedia / Britannica / Bloomberg / CRS).
- **WebSearch did NOT return clean daily-movers list for Thu 6/4 — 5th consecutive session of the gap (Fri / Mon / Tue / Wed / Thu).** Pattern is now confirmed across all weekdays. Outlier-mover reconstruction from Alpaca News + WebSearch hits worked but the same-day endpoint staleness on slickcharts/Yahoo is a persistent gap. Try Saturday with explicit prior-day framing.
- VIX Thu close 16.06 confirmed via Saxo. 1-day VIX 11.48 (+29.3%) confirms NFP-day near-tenor hedging.
- Previous notes:
  - "WebSearch returns nothing useful for 'CPI release' queries; use 'CPI <month> <year>' instead" — not exercised today.
  - "WebSearch for 'biggest gainers/losers' + specific date returns slickcharts/Yahoo Finance summary lists reliably" — DID NOT WORK Fri/Mon/Tue/Wed/**Thu** (5-session pattern now confirmed).
  - "When a major geopolitical event happens over the weekend, search multi-source major outlets (NPR/Fox/NBC/CNBC) rather than just the search query alone" — applied; House war-powers cross-confirmed.
- **News-fetch subdirectory caveat.** Operator-added universe symbols don't auto-receive news-fetch coverage unless `news/stocks/<SYM>/` subdirs exist. ARM/CSCO/HPE/MRVL were universe members Thu but no per-symbol HTML was produced. Fix is either (a) pre-create subdirs during operator-add, (b) update news-fetch to auto-create on first encounter, or (c) manual mkdir in tomorrow's run.
