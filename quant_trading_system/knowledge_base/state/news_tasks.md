# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**✅ FRESH, ON-TIME Wednesday 2026-07-22 run** firing at the ~15:39 PT slot with 7/22 data (news-fetch stamped 7/22; quotes/WebSearch all 7/22). `market-status` at run: `is_open false`, `now 2026-07-22T15:39 PT`, `next_open 2026-07-23T09:30 ET`. Next trader run is post-close 7/22 ~4 PM PT; **next news run is Thu 7/23 ~3:30 PM PT.**

**✅ SCHEDULE APPEARS RECOVERED.** 7/17 + 7/20 dropped, but **7/21 (news+trader) AND 7/22 both fired on time.** Git log tops out at `[trader 2026-07-21]`; no double-fire. **BUT the run-gap residue is still live: QCOM/SPCX/SYNA `revalidate_by 2026-07-21` remain OVERDUE** — Saturday 7/18 research never ran and there's been no research since. Flagged HIGH (open questions). **Thu 7/23: confirm `[news 2026-07-23]`/`[trader]` fire; watch whether Sat 7/25 research runs to clear the overdue three.**

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Wed 2026-07-22) — **event-dense but the equity tape held; NOT halt-worthy.** A mild, oil-pressured risk-off session (**Nasdaq −0.6% / 25,690.90, S&P ~flat / ~7,499, Dow ~flat / ~52,219**), chips cooling after Tue's +5.2% SOX day. Two things happened: (1) **two mega-cap Q2 prints AMC** — **GOOGL beat** (rev $119.8B +24%, **Google Cloud +82% to $24.77B**, EPS $9.11, CFO "demand still outpaces capacity" → IREN/NBIS/WULF/CRWV up AH) and **TSLA mixed** (record rev $28.24B +26% BEAT, but EPS $0.32/$0.33 MISS, net income −57%; Cybercab in production, Optimus "soon"); (2) **Houthi Red Sea / Bab el-Mandeb naval blockade on Saudi Arabia** (11th night of Iran war) → **oil spiked (Brent +3.4% ~$94, WTI +3% ~$87)**. **No HALT trigger:** no FOMC (7/28–29), META (held) only a modest France under-15 ban (cross SNAP/RDDT/X), oil did NOT gap equity futures >2% (S&P flat).
- **UNIVERSE UNCHANGED at 40 — NO promotions this run.** No non-universe name had a discrete hard catalyst meeting the subject test; the theme-relevant mover (CoreWeave/CRWV) rode analyst + GOOGL read-through, not its own event → tracked, not promoted (same discipline as WDC on 7/21). Off-theme beats (AT&T/COF/MCO/CME) noted, not candidates.
- **Held book:** universe `by_source` still shows **positions = META only**. No reconcile for the news agent.
- **Interpreter:** bare `python3` STILL BROKEN (Homebrew 3.14.5, no harness deps). Use **`/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`** from repo root before EVERY CLI call. (This run: all CLI calls ran clean via the venv. NOTE: `cd` into a news subdir breaks the *relative* `.venv/bin/python3` path — either cd back to repo root or use the absolute venv path.)
- **State:** universe 40, claimed 40, unclaimed 0, provisional 12 (unchanged by news agent). Provisionals: **QCOM/SPCX/SYNA 7/21 (OVERDUE)**, **SKHY 7/24**, **RIVN 7/27**, **GS 7/28**, **MS/PYPL 7/29**, **UNH 7/30**, **AMD/IREN/NBIS 8/4**. `gap-registry coverage_holes` **empty** (confirmed again).
- **Alpaca density: 197 items.** NVDA 18, GOOGL 17, TSLA 17, SMCI 14, AMZN/META/MSFT/MU/SPCX 10, SPY 9, DELL/INTC 7, AMD/ORCL/QQQ 6, AAPL/SKHY/SNDK 4, TSM 3, AVGO/CBRS/GS/JPM/NBIS/RKLB 2, ARM/CSCO/HPE/IRDM/IREN/MRVL/MS/QCOM/UNH/WULF 1; zeros: BE/NUVL/PYPL/RIVN/SYNA. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline:** header dated 2026-07-22 (fresh, on-time Wednesday). Prior: 7/21 (fresh), 7/16 (fresh). **7/17 + 7/20 MISSING (no runs).**

## Notable carry-forwards

- **EARNINGS SEASON IS LIVE — the top recurring library gap, now with prints in hand.** **GOOGL (beat) + TSLA (mixed) went unresponded today** (both on `equity_trend_following_ema_cross`, no earnings-window responder). **INTC + ARM print tomorrow 7/23 AMC** — LOG ACTUALS 7/23 (INTC has beaten rev 7 straight qtrs; watch the Lip-Bu Tan turnaround). Then MSFT/META 7/29, AMZN/AAPL 7/30, AMD/SPCX 8/4. **SMCI's +26% backlog reaction unresponded a 2nd session** (on `mean_reversion_bollinger`; full audited report Aug 11). This is the #1 Saturday-research priority.
- **GOOGL Q2 (held-adjacent, big):** rev $119.8B +24%, Cloud +82%, EPS $9.11, CFO "demand outpaces capacity." Lifted the neocloud/AI-infra cohort (IREN/NBIS/WULF/CRWV) AH. **7/23: watch the regular-session reaction + read-through to the AI-infra universe names.**
- **TSLA Q2 (universe):** record rev beat / EPS miss / net income −57%. Cybercab in production, Optimus "soon." **7/23: watch the reaction + margin/Robotaxi/FSD commentary; promote NOTHING (already in universe).**
- **Houthi Red Sea / Bab el-Mandeb blockade — the fresh macro/energy shock.** Iran-backed; threatens ~7% of global oil supply if Bab el-Mandeb fully closes (Yanbu ~2.5M bpd). Not yet fully enforced; ships turning around; oil +3–3.4%. **7/23 checks: escalation overnight? oil follow-through? equity-futures >2% gap (halt line — NOT there today)?** Inflation risk into 7/28–29 FOMC.
- **SMCI (universe) — record >$60B backlog + margin pre-announcement (+26% today).** Lifted DELL/HPE (+3%). Full audited report/call Aug 11. Live earnings-window-gap example (on `mean_reversion_bollinger`, unresponded).
- **RKLB (universe) — confirmed $266M US Space Force contract** (suborbital launches; clarifies Tue's "defense contract"). Watch contract cadence.
- **CBRS (Cerebras, universe) — CrowdStrike AI-security partnership** (discrete partnership on a usually-zero-news name). Watch for more Cerebras customer wins.
- **SPCX (PROVISIONAL/quarantined, revalidate_by 7/21 OVERDUE) — real corporate developments now:** first-ever PUBLIC earnings set for **Aug 4**; exploring a 1-GW Texas AI data center; Musk denied a $52B Foxconn AI-server deal ("fake news"); **share unlock ahead** (forced-flow watch). Stays non-tradable until research handles the overdue revalidation.
- **META (held) — France approved Europe's toughest under-15 social-media ban** (also SNAP/RDDT/X). Modest, single-market; not adverse-major. Q2 7/29. Rides MACD.
- **INTC — Q2 tomorrow 7/23; SK Hynix denied an Intel-Ohio-campus buyout report** (M&A rumor). On `breakout_volume_confirmation`.
- **NVDA / TSM — Taiwan June export orders record +59.4% ($95.26B)** reaffirming the AI supercycle; Bessent floated Chinese-AI sanctions (Jensen pushback); TSM ~10% 2027 price-hike plan + China chip-curb exposure (carry).
- **ORCL — data-center-cost / OpenAI-exposure pressure** (commentary, carry from last week's cash-burn story; no fresh discrete event). On `equity_event_driven_catalyst` (validated).
- **CoreWeave (CRWV) — TRACKING** (recurring neocloud cohort; rose on analyst + GOOGL read-through, no discrete event). Promote on its own hard catalyst (earnings/contract/M&A).
- **Vol regime — VIX ~17** (7/21 close 17.05; roughly unchanged 7/22 despite the oil move). **NOTE: this refines DOWN the prior brief's ~18.65 estimate — 7/21's true close was 17.05.** Dispersion persists (SMCI +26% vs SNDK down). Options skeletons not activated.

## To do on the next run (Thu 7/23)

1. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` from repo root** (don't `cd` into a news subdir and then call the relative path — it breaks). Re-read `news_manual.md §9` (Tier 0 = promote every US-tradable news-subject with a discrete catalyst on first appearance, uncapped; Tier A recurrence = prioritization; Tier B still applies; all require `--sector`).
2. **CONFIRM THE SCHEDULE FIRES** (`[news 2026-07-23]`/`[trader]`). 7/21+7/22 both fired; confirm the recovery holds. If runs drop again, flag HIGH.
3. **INTC + ARM Q2 results (print 7/23 AMC)** — log actuals vs consensus. **GOOGL/TSLA reaction** (regular-session move + AI-infra read-through). **SMCI** audited-print watch (Aug 11).
4. **Houthi Red Sea blockade / oil** — escalation? oil follow-through? equity-futures >2% gap? Inflation read-through into FOMC.
5. **AI-infra cohort (IREN/NBIS/WULF, CRWV-track)** — did GOOGL's "demand outpaces capacity" read-through hold? **AMD** — into its 8/4 print.
6. **META (held)** — any adverse single-name development beyond the France ban; Q2 7/29 setup. Rides MACD.
7. **Confirm universe = 40 / claimed 40 / provisional 12** (QCOM/SPCX/SYNA 7/21 OVERDUE, SKHY 7/24, RIVN 7/27, GS 7/28, MS/PYPL 7/29, UNH 7/30, AMD/IREN/NBIS 8/4).
8. **CoreWeave (CRWV)** — promote if a discrete hard catalyst lands (earnings/contract/M&A). **WDC/ASTS/ALAB** — promote if they recur with a fresh hard catalyst (tracked, not promoted). Off-theme beats (T/COF/MCO/GEV) not candidates.
9. **Vol regime** — VIX vs ~17; event IV into INTC/ARM 7/23, MSFT/META 7/29, AMZN/AAPL 7/30, AMD/SPCX 8/4. Log concrete single-name UOA on universe names ONLY (today's whale alerts were scanner rollups again — IT/comm-services/financials — not sized sweeps).
10. **Library gaps re-listing** (see brief): earnings-window assignment (**GOOGL/TSLA printed today unresponded; SMCI unresponded 2nd session; INTC/ARM 7/23; MSFT/META 7/29; AMZN/AAPL 7/30; AMD/SPCX 8/4**; GS/MS/PYPL/QCOM/RIVN/UNH quarantined); contract-win (RKLB $266M); partnership/product (CBRS-CrowdStrike, GOOGL AI-infra); strategic-corporate/capex/M&A-rumor (SPCX Aug-4/1-GW/Foxconn-denial, INTC Ohio-buyout denial); regulatory/policy (France under-15 ban, Warren oversight, Bessent Chinese-AI sanctions, China chip curbs); cohort/sector-momentum (Taiwan exports record, chip cooldown); analyst/valuation-shock (BlackRock memory-rout call, BofA $170B server-CPU); index/forced-flow (SPCX unlock, SKHY); geopolitical/energy-shock (Houthi/oil); vol-regime/dispersion activation.

## Open questions for the operator

- **[HIGH — carry] QCOM/SPCX/SYNA `revalidate_by 2026-07-21` STILL OVERDUE.** Saturday 7/18 research never ran; there's been no research since. They stay quarantined until research (or the trader's escalation path) handles them. **Does a missed-research-window auto-extend `revalidate_by` or force escalation?** The provisional book is now 12 and growing; if research keeps missing, none get validated or archived.
- **[MEDIUM — improving] Schedule reliability.** After 7/17+7/20 drops, 7/21 and 7/22 both fired on time — the schedule looks recovered, but confirm 7/23 fires and that Sat 7/25 research runs (to clear the overdue three). Both failure modes (double-fire 7/7–7/8, dropped runs 7/17/7/20) have now been seen.
- **[proportionality — RECURRING, still unanswered] How aggressively to apply UNCAPPED Tier-0?** This run promoted ZERO (no discrete-catalyst non-universe subject; CRWV rode read-through → tracked). Prior runs promoted 3 (7/21) and 1 (7/16), all AI/semis. The strict "discrete hard catalyst" subject test keeps the universe from ballooning on cohort moves, but tech concentration remains ~26/40. Preferred posture: promote every hard-catalyst news-subject, or cap per-day / weight toward diversification? (Removal is operator-only, so I still err toward hard-catalyst-only inclusion.)
- **[MEDIUM] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Repoint the launcher + prompt to the venv (or pip-install requirements into 3.14).
- **[MEDIUM] News-brief staleness guard.** The `_load_news_brief()` staleness check (parse date_in_file, reject/down-weight if >1 session old) is still unbuilt — matters more given the 7/17/7/20 drops (the trader could read a stale brief as "today" if a run drops again). Build it.
- **[MEDIUM] Fallback-threshold question (carry).** Degenerate 0-trade backtest attaches a below-baseline *trading* provisional rather than routing to `equity_watch_only` (GS/MS/PYPL/RIVN/UNH/AMD/IREN/NBIS → trading provisional; SKHY/SPCX no-history → watch_only/trend provisional). Should a degenerate/empty backtest count as "rankable" or "no signal → watch_only"?
- **Index-inclusion / float-mechanics as a 6th Tier-B trigger? — recurring** (SPCX share unlock ahead; SKHY Korea ETF margin). Forced-flow gap keeps recurring.
- **Product/roadmap + strategic-investment/partnership as event sub-triggers? — recurring & growing** (CBRS-CrowdStrike, GOOGL AI-infra, SPCX capex, NVDA-Nebius/AMD-Microsoft carry, RKLB contract). No rule reads any of these.
- **Earnings-window assignment — GOOGL/TSLA printed unresponded today; SMCI unresponded 2nd session; INTC/ARM 7/23; MSFT/AMZN/AAPL/META/AMD/SPCX upcoming; GS/MS/PYPL/QCOM/RIVN/UNH quarantined.** Earnings-window responders don't claim the names actually printing. Sat research: assign.
- **M&A-arb / merger activation — PYPL (Stripe/Advent target, no dev), AAPL (chip-acquisition intent, carry), RKLB(acquirer)/IRDM(target), SYNA/onsemi.** `equity_pairs_trading_cointegration` claims only SYNA. Sat: activate merger-arb.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists. (Not re-checked — news agent doesn't pull broker state.)
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate in `.git-sync-queue/`.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim. (UNH is a 2nd healthcare name.)
- **Sunset watch:** no universe symbol yet hit the 0-news-across-30-sessions + no-position sunset criterion; keep tracking (BE/NUVL/PYPL/RIVN/SYNA recurring zeros but recently added / claimed).

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **197 items** cleanly (via venv). Zeros: BE/NUVL/PYPL/RIVN/SYNA.
- `cli market-status` at run start → `is_open false`, `now 2026-07-22T15:39 PT`, `next_open 2026-07-23T09:30 ET`. Fresh on-time Wednesday run; 7/21+7/22 both fired (schedule recovering).
- `cli list-active` → universe 40, claimed 40, unclaimed 0, provisional 12. `gap-registry coverage_holes` empty. **No promotions this run** (universe unchanged 40).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier 0 (news-subject inclusion, uncapped):** NO qualifying non-universe subject with a discrete hard catalyst today. **CoreWeave (CRWV)** had a dedicated coverage line but the driver was analyst backing + GOOGL "demand outpaces capacity" read-through, not a discrete CRWV corporate event → tracked (same call as WDC on 7/21). Off-theme earnings beats (**AT&T/COF/MCO/CME** beat, **GEV** fell) are not theme-relevant candidates. Denied M&A rumors (SK Hynix/Intel-Ohio; Foxconn/SpaceX) are non-events.
  - **Decision: 0 promotions. Universe stays 40.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- **Number hygiene:** the "Stock Market News for July 22" recap articles (Yahoo/Globe&Mail) report the **7/21** close (S&P 7,509 / VIX 17.05) — do NOT mistake them for the 7/22 session. The 7/22 close (Nasdaq 25,690.90 / S&P ~7,499) came from the ABC News "how indexes fared Wednesday 7/22" wire + the 7/22 live blog. Same-day-dated recap articles lag one session.
- Previous notes (still held): "CPI/PPI <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest; headlines+summaries only (don't WebFetch full articles); VIX/index exact quotes diverge across aggregators on a busy day — report "~level, regime" not false precision.
