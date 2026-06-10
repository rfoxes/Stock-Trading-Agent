# News brief for 2026-06-10

## Headline assessment

**NOTABLE.** Wednesday delivered a three-axis event day. (1) **May CPI hit 4.2% YoY headline / 2.9% core** (matched +4.2% consensus; hottest headline since April 2023) — energy +3.9% MoM (+23.5% YoY) driven by the Hormuz shock. Fed-hike-by-Dec odds re-priced from ~30% to **63-96%** across venues; FOMC June 17 hold base case unchanged but the dot plot is now the live catalyst and easing-bias language is at risk. (2) **The Iran ceasefire framing broke**: US strikes on Iranian air-defense / radar / surveillance sites near Hormuz late 6/9, Iran IRGC missile + drone retaliation 6/10 on US base in Jordan + Persian Gulf targets; Trump threatening additional strikes on Iranian power plants + bridges. Oil reversed Mon-Tue's -5% Iran-deal-proximity into a sharp bid. (3) **ORCL Q4 FY26 AMC double-beat** ($2.11 vs $1.89 / +11.6%; revenue $19.2B +21%; cloud $9.9B +47%; RPO +$85B to $638B) **was undermined by a $40B FY27 capital raise announcement** — capex overshoot drove ORCL down in extended hours despite the beat + raised guide. Single-name fallout: chip cohort sold off (ARM -4.46%, MU -4.7% premarket, MRVL down, INTC sliding, AVGO testing key MAs); GOOGL + NVDA got an offsetting WWDC Day-3 anchor-customer confirmation (Apple Foundation Models run on Google Cloud + NVDA chips); META announced a 168MW Reliance-built AI data center in Gujarat; TSM May sales +30.1% YoY. **Not HALT-WORTHY** — no active FOMC, no >5σ guidance shock on a held name, the Iran exchange did not move overnight futures >2% before close, and the CPI was in-line with consensus. Trader should treat the day as elevated-vol event-window posture; algorithmic-only mandate still governs.

## Watchlist + positions

(Entering Thu: held longs AAPL 72, MU 7, QQQ 28, SPY 35 per Wed trader handoff; book is net-cash $32,064. Active set: 7 strategies × 22 universe symbols claimed.)

- **ORCL — MAJOR EVENT (Q4 FY26 print Wed AMC).** Double-beat: EPS $2.11 vs $1.89 (+11.6%), revenue $19.2B (+21% YoY), Cloud $9.9B (+47%; IaaS +93%), RPO $553B → $638B (+$85B; OpenAI / Meta AI-infra commits), raised FY27 EPS guide to $8.05 (rev reaffirmed $90B). **Capex shock:** announced $40B FY27 capital raise — exceeded consensus capex expectations and drove ORCL down in extended hours. **Tier-B #3 (beat + raise + +5% post-print) will NOT clear at Thu open absent overnight reversal.** No retroactive Tier-B audit confirmation; ORCL stays Tier-A-promoted from Tue.
  - responder: `equity_event_driven_catalyst` (on-character post-print window; rule will fire on the strategy's print-window logic Thu)

- **MU — EVENT-WINDOW (pre-print, MU Q3 FY26 = 6/24 AMC; held long).** Caught in Wed chip-cohort selloff (-4.7% premarket on broad CPI + Iran selloff); whale-alert activity confirmed Wed. Pre-print window opens next week. Position -8.44% unrealized at Wed close per trader handoff; stop $813.44 ~9.6% away. No fresh single-name catalyst Wed; "Why Is Micron Falling" framing is price action.
  - responder: `equity_event_driven_catalyst` (pre-print window posture; rule respects stop)

- **AAPL — EVENT (WWDC Day-3 confirmed: Apple Foundation Models on NVDA chips + Google Cloud; held long).** Confirmed Wed via Benzinga: Apple's AI relies on NVDA chips + Google Cloud for heavy workloads — anchor-customer confirmation for both. Negative read for AAPL silicon-self-sufficiency narrative; sell-side reaction continues to be mixed (-1.0% Wed per handoff). Telegram returned to Apple Watch (native app) — minor product item. Inflation-above-4% ETF strategy piece flagged AAPL alongside quality/dividend tilt.
  - responder: `equity_trend_following_ema_cross` (price-driven; no event-window rule active — library gap)

- **GOOGL — POSITIVE EVENT (WWDC Day-3 + GitLab partnership + SpaceX context).** "Apple's AI Reveal Hands An Unexpected Win To Google, NVIDIA" — explicit anchor-customer confirmation Wed. GitLab expanded Google Cloud partnership (fully managed DevSecOps + Gemini 3.5 AI). Munster: GOOG is a "formidable rival" to SpaceX (but doesn't make rockets). SpaceX-IPO context pieces frequently mention GOOG as the AI-cloud counterweight. GOOGL was exited Wed open per trader (sell 56 ≈ $362.92; +$1,352 P&L); no current position.
  - responder: `equity_trend_following_ema_cross` (rule fired Wed open; no current position)

- **NVDA — POSITIVE EVENT (WWDC anchor-customer confirmation + TSM May +30% YoY + SpaceX TAM).** Apple AI on NVDA chips (anchor-customer confirmation); TSM May +30.1% YoY revenue (cohort-positive). Wedbush Dan Ives: SpaceX $28.5T TAM ties to NVDA-substrate AI. ServiceNow demand-resilient piece referenced NVDA. Counter: Burry NVDA short paying off; Jensen called the pullback a "discount" buying window; Jensen declined Senate hearing. Defense-tech and DOE-fusion-timeline pieces named NVDA. NVDA was exited Tue (sell 96 from Mon trend-following ADX exit); no current position. Stock down again Wed in chip selloff.
  - responder: `equity_trend_following_ema_cross` (rule exited Tue; no fresh entry signal)

- **META — POSITIVE EVENT (Reliance India 168MW AI data center deal Day-1; not held).** Meta announced first India AI infra: Reliance builds 168MW data center in Jamnagar, Gujarat; Meta leases capacity, covers energy/water costs. Extends 2020 $5.7B Jio investment. Two-year build, renewable + desalinated-seawater cooled. Concrete capex commitment + India entry-point. Wed trade choppy on broader macro.
  - responder: `equity_momentum_macd_histogram` (no current position; rule will pick up any fresh momentum signal)

- **TSM — POSITIVE EVENT (May 2026 sales +30.1% YoY = NT$416.98B).** Material AI-chip-demand confirmation. Cited in NVDA / TSLA / AMZN / GOOGL / INTC cross-references all day. Chris Miller "Chip War" Wed framing: China has underspent on AI for 4 years — TSM-as-incumbent narrative reinforced. TSM not held; new universe member from Mon's promotion remains unclaimed character-wise per operator question (Sat research owns proper claim).
  - responder: `equity_trend_following_ema_cross` (provisional claim; price-driven rule will fire if EMA cross)

- **MRVL — NO FRESH SINGLE-NAME EVENT (chip-cohort drag).** "Why Is Marvell Technology Falling Wednesday" + whale-alert list flagged MRVL; nothing new on inclusion (6/22) or business fundamentals. Wed weakness is part of broader chip selloff.
  - responder: `equity_breakout_volume_confirmation` (volume-confirmation rule may fire on inclusion-window flows; today is price action)

- **INTC — NO FRESH MATERIAL EVENT (Google-TPU narrative quiet Day-4).** "Why Is Intel Stock Sliding Wednesday" cites profit-taking + AVGO-guidance ripple + macroeconomic headwinds; no fresh Google-foundry verification disclosed Wed. Sliding with the cohort.
  - responder: `equity_breakout_volume_confirmation` (price-driven; provisional claim)

- **AVGO — NO FRESH SINGLE-NAME EVENT (Day-5 post-print).** "Why Is Broadcom Falling Wednesday" + cohort-mentions only; post-earnings profit-taking framing continues. Next AVGO print September.
  - responder: `equity_event_driven_catalyst` (calm posture; no fresh catalyst)

- **NUVL — NO FRESH MATERIAL EVENT Day-2 of GSK deal.** Only cited in "5 stocks on radar" cohort piece. No deal-close timeline update, no spread-narrowing flag. Pre-close, trades freely.
  - responder: `equity_trend_following_ema_cross` (provisional claim; price-driven rule applies — library gap on M&A-arb)

- **JPM — SECTOR/FRANCHISE CONTEXT (3 cohort items; OpenAI underwriter, SpaceX underwriter window live Thu).** No JPM-specific single-name event Wed. SpaceX pricing Thu AMC = underwriter franchise event live. Inflation-above-4% ETF piece flagged JPM in quality/dividend tilt. JPM was exited Wed open per trader (sell 64 ≈ $311.78; -$80 P&L); no current position.
  - responder: `equity_trend_following_ema_cross` (rule fired Wed open; franchise event not in any active rule — library gap re-affirmed)

- **TSLA — NEUTRAL EVENT (Musk SpaceX-payload bombast + Dutch FSD-crash data positive).** Musk: SpaceX could put 1M tons in orbit within 5 years. Dutch FSD crash data showed 3.5x fewer crashes (positive for FSD narrative). Mentioned in Burry-short coverage. No held position; no re-entry signal.
  - responder: `equity_trend_following_ema_cross` (no signal)

- **MSFT — NO FRESH SINGLE-NAME EVENT.** "What's Going On With Microsoft Wednesday" + SpaceX cohort + Meta-Reliance cross-mention; nothing material.
  - responder: `equity_momentum_macd_histogram` (price-driven)

- **ARM — DRAG SESSION (no fresh catalyst).** "What Is Going On With Arm Wednesday" — -4.46% to $310.79 on "routine wave of broad-market profit-taking." No fresh ARM-specific event.
  - responder: `equity_breakout_volume_confirmation` (price-driven)

- **CBRS — NO FRESH MATERIAL EVENT.** Cited in "CPI Saves Market" macro piece + one other cohort mention. Mon's 7-bank initiation cluster attention persists structurally; nothing fresh Wed.
  - responder: `equity_trend_following_ema_cross` (provisional claim)

- **HPE — NO FRESH SINGLE-NAME EVENT (single cohort item + whale alert).** Whale-alert flagged HPE among 10 IT names; no fresh single-name catalyst.
  - responder: `equity_rsi_divergence` (price-driven)

- **AMZN — NO FRESH SINGLE-NAME EVENT.** Meta-Reliance + TSM May-sales + SpaceX-context cross-mentions only. No held position.
  - responder: `equity_trend_following_ema_cross` (no signal)

- **DELL, CSCO — NO FRESH NEWS Wed (0 Alpaca items each).** No single-name event.
  - DELL responder: `equity_sector_rotation_momentum` (price-driven)
  - CSCO responder: `equity_mean_reversion_bollinger` (price-driven)

- **SPY / QQQ — INDEX TAPE Wed.** Indices fell on hot CPI + Iran exchange; "CPI Saves Market" framing flagged momo-buy-the-dip but session ended weaker. Trump-Iran posts moved markets lower mid-morning. AMD slipped on chip selloff. No index-level event beyond the macro reaction.
  - responder: `equity_trend_following_ema_cross` (price-driven)

- **No fresh single-name news (Wed Alpaca densities; 135 total items):** CSCO 0, DELL 0, ARM 1, HPE 1, CBRS 2, NUVL 2, MRVL 2, JPM 3, INTC 4, MU 4, AAPL 5, AVGO 5, META 5, TSM 5, MSFT 6, AMZN 8, TSLA 11, QQQ 11, GOOGL 13, ORCL 15, SPY 15, NVDA 17.

## Sector themes

- **Macro repricing back to "higher-for-longer" via CPI energy passthrough.** May CPI 4.2% (highest since April 2023) is driven almost entirely by the Hormuz energy shock; core 2.9% (sticky but not spiraling). Wall Street consensus: "too hot to cut, not enough to hike yet — June 17 = hold, dot plot tighter." Defensives (XLE, gold, dividend/quality ETFs) outperforming AI cohort intra-day.
- **AI capex commitment cycle continues despite multiple-compression pressure.** Wed events: ORCL announced $40B FY27 capital raise (capex overshoot), META announced 168MW India data center with Reliance, Apple confirmed running on Google Cloud + NVDA chips, TSM May +30%. Demand side keeps printing; supply side now visibly absorbing the cost. Burry NVDA/PLTR short paying off as multiple compression in the AI cohort starts to crystallize.
- **Chip cohort selloff is broad but undifferentiated.** ARM, MU, INTC, MRVL, AVGO, NVDA all weaker — not a single-name story; the macro tape and Burry/Saylor sentiment items drove the dispersion. TSM May sales +30.1% YoY is the on-thesis positive offset that didn't catch.
- **AI data-center NIMBY/permit pushback becomes a recurring narrative.** xAI + SpaceX sued in Mississippi over data-center noise; ORCL's $40B FY27 raise concentrates the capex story. The "infrastructure friction" theme will likely return.
- **Defense / energy / quality tilt firms as the structural counterweight.** LMT, NOC, RTX cited in Trump-Iran piece; XLE / XOP bid; SCHD / DGRO / VIG / QUAL noted in the ETF strategy piece. The trader's universe doesn't have direct exposure to these (no XLE, no LMT) — observation only.

## Candidates for the universe

**No promotions executed Wed. Universe stays at 22.**

- **Tier A (3-session recurrence):** CRWD (provisional 3), STM (2), FLEX (2), PINS (2), VSH (1) — none refreshed in Wed Alpaca pull or Wed WebSearches. All hold at current session counts. CRWD provisional-3 still awaits a fresh appearance to formalize; operator question on candidate-counter mechanism carries forward.
- **Tier B (single-event triggers, 5 categories, 2/day cap):**
  - **#1 confirmed M&A target:** none Wed.
  - **#2 FDA binary:** none Wed.
  - **#3 beat + raise + +5%:** ORCL is in-universe (already promoted Tue); the Tier-B #3 audit was the Wed-AMC test, and the print failed the +5% criterion (down in extended hours on $40B capex raise). No retroactive Tier-B audit added. Externally, no S&P 500 name reported a beat+raise+5% print Wed AMC.
  - **#4 sell-side initiation cluster (3+ banks same week):** none new Wed.
  - **#5 Tier-1 customer-win disclosure:** META + Reliance India data-center deal is META-internal (universe member), not a candidate trigger; the partnership benefits META, not Reliance/Indian-listed names accessible to us. Apple-on-Google Cloud + NVDA-chips confirmation similarly benefits universe members. **No promotion qualifier.**
- **SMCI** — recurring cohort mention (ORCL/AVGO/INTC selloff context) but no single-name catalyst. Carry-forward as session-1 watch but does not qualify yet.
- **PLTR** — Burry short paying off; defense/AI-government adjacency. Not a Tier-B trigger.
- **Net: 0 candidates promoted Wed.** Tier-B daily cap (2) untouched; Tier-A clock advances for CRWD/STM/FLEX/PINS/VSH only on fresh appearance.

## Macro / sector context

- **May CPI 4.2% YoY headline / 2.9% core / +0.5% MoM headline / +0.3% MoM core.** Matched +4.2% consensus. Energy +3.9% MoM (+23.5% YoY) drove the headline; Hormuz shock the proximate cause. Fed-hike-by-Dec odds 63-96% across venues. June 17 FOMC = hold base case; dot plot is the live catalyst; easing-bias language at risk.
- **US-Iran exchange Day-1.** US strikes Iranian air-defense / radar near Hormuz (late 6/9). IRGC missile + drone strikes on US base in Jordan + Persian Gulf 6/10. Trump threatening more strikes on Iranian infrastructure (power plants + bridges). Oil reversed Mon-Tue's -5% into a bid. Tue's "ceasefire two-three days" framing is broken; the geopolitical tape is now in active-exchange posture.
- **PPI May + initial jobless claims Thu 6/11 8:30 ET.** Compound stack with ADBE AMC + SpaceX IPO pricing AMC.
- **ADBE Q2 FY26 Thu 6/11 AMC.** Consensus $5.81 EPS / $6.45B rev. ADBE -32% YTD on AI cannibalization concern. Options imply ±9.45%. $25B buyback in place.
- **SpaceX (SPCX) IPO pricing Thu 6/11 AMC → Fri 6/12 listing.** Demand >4x oversubscribed (>$250B vs $75B raise). $135 × 555.55M / $1.8T valuation. Largest IPO ever. JPM in lead-underwriter group with Goldman + Morgan Stanley.
- **VIX 19.87 mid-afternoon (open 20.10, hi 20.46, lo 20.06).** Third session probing the 20 ELEVATED threshold without a decisive break. Realized 30-day still 13.51 = VIX trading rich-to-realized = typical event-window posture.
- **FOMC June 16-17.** Hold priced; dot plot is the catalyst.
- **OpenAI / SpaceX / Anthropic AI-IPO supply wave continues.** No new S-1 filings Wed; SpaceX pricing Thu is the live event.

## Library gaps

- **AAPL WWDC 5-day event-window Day-3 (mixed reaction)** — `event_window_posture` rule still absent. Re-affirmed Day-3. **Suggested research:** event-window overlay (defer entries / tighten exits inside named multi-day catalyst windows).
- **ORCL capex-shock post-print (down in extended hours despite beat+raise)** — no `capex_shock_negative_event` overlay; the `equity_event_driven_catalyst` strategy's print-window rule may or may not fire on the asymmetric reaction. **Suggested research:** capex-overshoot detection overlay (when a beat+raise print is paired with above-consensus capex disclosure, defer / size down the entry).
- **NUVL M&A-arb position** — `m_a_arbitrage_event` still absent. Re-affirmed.
- **OpenAI + SpaceX overlapping franchise event for JPM** — `underwriter_franchise_event` still absent (Day-2 of overlap window). Re-affirmed.
- **Hot CPI + macro repricing** — `macro_event_window` overlay still absent. Trader took no preemptive posture on CPI day (algorithmic-only) — that's correct but the soft-signal handle is missing. **Suggested research:** macro-print event-window overlay (pre-print position sizing + post-print posture re-eval).
- **Cross-sector defensive rotation (energy / dividend / quality bid vs AI cohort)** — `cross_sector_rotation_overlay` still absent. Re-affirmed Day-2.
- **AI-cohort multiple-compression (Burry short paying off + $40B ORCL capex raise + Anthropic token-pricing AI-bubble narrative continuation)** — `equity_multiple_compression_overlay` still absent. Re-affirmed.
- **VIX-threshold cross / regime-shift** — `vol_regime_shift_overlay` still absent; three sessions oscillating around 20 without confirmation either way.
- **Iran-exchange / oil-shock event overlay** — currently no rule fires on energy-shock pass-through, even though it's now visible in CPI. Soft signal only.
- **Hormuz / China-Taiwan / defense-name framing** — no defense-sector exposure in the universe; observation only.

## Recommendations for the trader

- **NOTABLE assessment. Standard workflow with elevated event-window awareness.** Three live event vectors stacked: hot CPI fallout, US-Iran active exchange, ORCL post-print fade. None individually breach HALT-WORTHY; combined they argue for letting rules govern rather than overriding.
- **ORCL post-print Thu (AVGO/MU/ORCL claimed by `equity_event_driven_catalyst`).** The print profile (beat+raise+ negative AH reaction on capex shock) is exactly the kind of asymmetric catalyst the rule should handle. **Consider: the strategy may fire an exit/avoid signal on ORCL Thu open; trust the rule.** The trader has no ORCL position to manage today.
- **MU pre-print window opens next week (Q3 6/24 AMC).** Held position, -8.44% unrealized, stop ~9.6% away. Pre-print event-driven posture: don't override the rule; let the stop or the print response govern.
- **AAPL held into WWDC Day-3 (negative cumulative reaction).** No event-window rule; trader is correctly relying on trend-following price action. Standard posture.
- **JPM no longer held (exited Wed open); franchise-event window (SpaceX pricing Thu AMC + OpenAI Q4 listing) is informational only.** Library gap on `underwriter_franchise_event` re-affirmed.
- **Fed June 17 dot plot is the live macro catalyst.** No `macro_event_window` rule; trader cannot pre-position. Soft caution: any held momentum/trend position has 1 week to FOMC; the print profile (likely hold + hawkish dot-plot lift + easing-bias language removal) skews adversely for AI-cohort multiples.
- **VIX at the 20 ELEVATED threshold.** No `vol_regime_shift_overlay` rule. Observation only; iron-condor strategy (`iron_condor_high_iv`) would find IV rank attractive if it claimed any universe symbols, but none are claimed for it.
- **AI-cohort multiple-compression risk is becoming concrete** (Burry short + ORCL capex overshoot + Anthropic Mythos-token-pricing carry-forward). No rule fires on multiple-compression. Observation only.
- **`cli execute` should run as scheduled.** No HALT-WORTHY trigger. Rules govern; if no rule fires, no trade is the correct outcome.
- **Algorithmic-only mandate.** If a rule fires, execute; if no rule fires, don't trade.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **135 items** across 22 symbols (vs Tue 176, Mon 136). NVDA 17, SPY 15, ORCL 15, GOOGL 13, QQQ 11, TSLA 11, AMZN 8, MSFT 6, AAPL 5, AVGO 5, META 5, TSM 5, INTC 4, MU 4, JPM 3, NUVL 2, MRVL 2, CBRS 2, ARM 1, HPE 1, CSCO 0, DELL 0. Sector aggregates: technology 53, financials 3, healthcare 2, index 16, consumer_discretionary 11. `pending_sector_assignment: []`. Zero-coverage Wed: CSCO, DELL.
- 135 items Wed vs 176 Tue (-23%) consistent with the day's coverage being concentrated on macro (CPI / Iran) + ORCL print + chip selloff rather than diversified single-name catalysts. NVDA/ORCL/SPY/GOOGL anchor the count.
- All 6 category HTMLs written (macro, earnings, geopolitics, policy, volatility, options_flow). Daily summary written.
- WebSearch returned strong results for: May CPI 2026 (Benzinga / CNBC / Kiplinger / CBS / Morningstar); ORCL Q4 FY26 (Stocktitan / Oracle IR / TheStreet / Benzinga); Trump Iran Hormuz strikes (RFE/RL / Britannica / Wikipedia); VIX June 10 (StreetStats / CBOE / Yahoo / Macrotrends); ADBE Q2 preview (Alphastreet / TipRanks / TIKR); SpaceX IPO pricing oversubscription (Bloomberg / FXStreet / Yahoo / Seeking Alpha); Meta-Reliance India data center (TechCrunch / CNBC / Bloomberg / Meta IR).
- WebSearch returned weak results for: same-day "biggest gainers/losers" S&P 500 query still flaky (top losers JNJ/HD/PG/KO/GLW/WSM/BLDR/PODD via ChartMill indirect — usable for cohort framing only); intraday UOA platforms still not freely searchable.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier A:** no fresh sessions added for CRWD / STM / FLEX / PINS / VSH. Holding at prior counts.
  - **Tier B:** no qualifiers Wed. ORCL post-print failed Tier-B #3 (+5% confirmation) due to capex-shock AH selloff. META-Reliance partnership benefits an in-universe member, not a new candidate.
  - **Decision: 0 promotions this run.** Universe stays at 22.
- `git-sync` LaunchAgent status remains in pending-marker state per recent handoffs; operator action still pending.
