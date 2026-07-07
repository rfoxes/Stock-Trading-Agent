# News brief for 2026-07-07

## Headline assessment

**NOTABLE — a genuine risk-off reversal (chip rout + Hormuz oil spike), but NOT halt-worthy.** After Monday's record risk-on tape, Tuesday flipped: **Samsung's record-but-priced-in Q2 print triggered a "sell-the-confirmation" chip rout** (MU −6%, SNDK −5%, MRVL −5%, INTC −4%, ARM −4% intraday), a **Strait of Hormuz tanker attack spiked oil** (Brent +3% to $74.16, then +5.6% to $76.04 after hours as the US revoked Iran's oil-sale license), **SpaceX joined the Nasdaq-100 but FELL ~7%** (forced-buy thesis didn't hold), and **Amazon launched a ≥$25B AI-capex bond sale**. `market-status`: `is_open false`, `next_open 2026-07-08 09:30 ET` — this is the canonical ~3:30 PM PT post-close run (today's cash session already closed). **None of the three HALT-WORTHY triggers fires:** (1) no FOMC — the Fed is on hold and only the June *minutes* release tomorrow (7/8, first under Chair Warsh); (2) no confirmed adverse overnight catalyst on a held name — META actually rose on a product launch + upgrade, and the MU weakness is a *competitor's* earnings read-through, not an MU-specific shock; (3) the Hormuz escalation moved **oil** >2% but **equity** indices/futures did not gap >2% (Nasdaq −1.2%, S&P −0.5%, Dow −0.2%). 130 Alpaca items; density SPCX 18 / MU 14 / AAPL 12 / NVDA 10 / TSLA 9. **Universe stays 26; 0 promotions.** `list-active`: claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**; `gap-registry coverage_holes` **empty**.

> **Broker-state note for the trader (relevant to the 7/7 09:09 handoff P0):** I snapshotted the account during this run — **it is INTACT, not flat.** `positions` shows all four longs back (AVGO 26, META 16, MU 7, ORCL 38); equity **$103,106.76**, cash **$71,809.59**, buying_power $374,870.44, day_trade_count 0. The 09:09 AM "wipe" that the trader froze on appears to have been **transient** (Alpaca paper glitch/reset that self-restored). Current marks: **META +1.6% (green), AVGO −2.4%, MU −5.6% (deepened on the chip rout), ORCL −20.1% (still the worst).** This is informational for your reconciliation — I do not trade or reconcile.

> **Provisional-claim note:** `provisional_count 3` (QCOM/SPCX/SYNA), all `revalidate_by 2026-07-21` after the 7/7 state re-bootstrap. **SPCX joined the Nasdaq-100 today but remains PROVISIONAL/execution-quarantined — it will NOT trade** regardless of the forced-flow. Separately, note the re-bootstrap re-stamped the `equity_trend_following_ema_cross` / `equity_event_driven_catalyst` / `equity_pairs_trading_cointegration` claim *reasons* to "PROVISIONAL/UNVALIDATED … QUARANTINED" with `since 2026-07-07`; the structured `provisional_claims` field still lists only the 3 symbols. Worth reconciling which claims can actually execute — trader/Saturday-research call, not mine.

## Watchlist + positions

Event-driven lines (a thing that *happened*), each tagged with a canonical `gap_type` + algorithmic responder. Price moves omitted — the trader has bars.

- **MU (held): Samsung's record Q2 drove a memory "sell-the-confirmation" selloff + SK Hynix US-listing (~7/10) funding-rotation concern.** The *fundamental* read is bullish — Samsung's DRAM ASPs +~44% / NAND +~53% confirm the memory pricing cycle — but positioning sold the news. Micron-Ford / Micron-GM SCAs are carry. No MU-specific corporate event today.
  - gap_type: event_catalyst (competitor-earnings read-through)
  - responder: NONE — library gap (MU's `equity_event_driven_catalyst` claim is provisional/quarantined and models MU's *own* earnings window, not a competitor's print; the position rides its rule)
- **META (held): launched "Muse Image," an AI visual-creation product, AND received an analyst upgrade** — META outperformed a down tape (+1%+, now green vs entry). Offsetting overhang: multiple social-media "addiction" court cases (a "$1.4T penalty scare" headline) + DST-tariff carry.
  - gap_type: event_catalyst (product launch + upgrade)
  - responder: NONE — library gap (META claimed by `equity_momentum_macd_histogram` (trending); a product launch/upgrade has no responder — the position rides its MACD exit)
- **AVGO (held): no fresh single-name event.** Rode the chip pullback (−2.4%); Broadcom-Apple-2031 extension is carry. A small bearish $375 call trade appeared in the flow (minor). Position rides its rule.
  - gap_type: event_catalyst
  - responder: NONE — library gap (`equity_event_driven_catalyst`, provisional/quarantined)
- **ORCL (held): no fresh event.** Only a tangential Musk healthcare-AI mention. Still the book's worst mark (−20.1%); that's price, for the trader's rule to handle.
  - gap_type: event_catalyst
  - responder: NONE — library gap (`equity_event_driven_catalyst`, provisional/quarantined)
- **NVDA: reports that China's DeepSeek is developing its own inference AI chip** pressured NVDA; separately NVDA **denied the Kyber NVL144 delay** report ("our roadmap remains intact"), and the stock rebounded ~1%. A competitive-threat event + a management roadmap rebuttal.
  - gap_type: event_catalyst (competitive threat / roadmap rebuttal)
  - responder: NONE — library gap (NVDA claimed by trend-following; no rule reads a competitor-chip report or a roadmap denial)
- **AMZN: launched a ≥$25B bond sale (8 tranches, 3–40yr) to fund AI-infrastructure capex** — ~$54B raised YTD, 2026 capex guided ~$200B (from $131B); demand 1.6x. Q2 earnings 7/30. A concrete capital-allocation / debt-raise event on a universe name.
  - gap_type: event_catalyst (capital-allocation / debt raise); earnings_window opens ~7/16
  - responder: NONE — library gap (AMZN claimed by trend-following; no capital-allocation or earnings-window responder claims AMZN)
- **INTC: Intel-backed Syntiant (edge-AI chips) filed for a Nasdaq IPO** (minor portfolio-company event); INTC itself fell ~4% in the chip rout. **Q2 earnings July 23** (14-day options window opens ~7/9).
  - gap_type: event_catalyst (portfolio-company IPO) + earnings_window (7/23)
  - responder: NONE — library gap (INTC claimed by `equity_breakout_volume_confirmation` (trending); no pricing/IPO or earnings-window responder claims INTC)
- **SPCX (PROVISIONAL / execution-quarantined): joined the Nasdaq-100 today but FELL ~7% to ~$149.58** — ~$4.3B passive inflow failed to lift it in the risk-off tape ("QQQ hype overdone"). It sits well below the >$175.50 "30% rule" unlock threshold, so the ~456M-share supply overhang is not in play at these levels. A same-week sell-side **initiation cluster** hit (Goldman Buy $205; Morgan Stanley/Jonas ~90% upside; JPMorgan 91% rev CAGR; +64% call; consensus avg PT ~$188.57). FCC vote 7/22.
  - gap_type: event_catalyst — index-inclusion forced-flow, which the canonical taxonomy does not cover → also **NEW_CATEGORY_NEEDED** (index_rebalance)
  - responder: NONE — library gap (SPCX's trend-following claim is provisional/quarantined AND no rule reads index-inclusion forced-flow)
- **MRVL / SNDK: fell ~5% as memory-cohort read-throughs of Samsung + DeepSeek.** The NVDA-Kyber "competitive window" thesis for MRVL faded as NVDA rebutted the delay; SNDK also carries the SK-Hynix funding-rotation concern.
  - gap_type: event_catalyst (sector/competitor read-through)
  - responder: NONE — library gap (MRVL claimed by breakout_volume — *may* catch momentum if volume/ADX-confirmed, but the event has no responder; SNDK by macd_histogram (trending))
- **JPM: firmed into its 7/14 Q2 print (window OPEN)** — ~$5.44/sh est, +9.7% YoY; $50B buyback effective 7/1. Bank season starts next week. No fresh single-name event today.
  - gap_type: earnings_window
  - responder: NONE — library gap (JPM claimed by trend-following, not the earnings-window strategy — assignment gap; most urgent)
- **TSLA: no fresh hard event.** Binary is the **7/22 earnings** call (margins); DOGE sunset (7/4) + Optimus/robotics-ROI commentary are soft. IV building.
  - gap_type: earnings_window
  - responder: NONE — library gap (TSLA claimed by trend-following, not earnings-window — assignment gap)
- **GOOGL: joined a ~$411–469M funding round for German fusion startup Proxima Fusion** (~$2.4B valuation) — a minor strategic AI-energy investment. Its Dow-30 inclusion was **6/29 (carry, not today)**; today's "who leaves the Dow next" piece is retrospective commentary. DST-tariff / UK-regulatory overhang carry.
  - gap_type: event_catalyst (minor investment)
  - responder: NONE — library gap (GOOGL claimed by trend-following; no partnership/investment responder)
- **DELL: Trump "buy a Dell" endorsement rally continued** (soft catalyst) + Trump-Accounts tie-in (first 500k funded).
  - gap_type: event_catalyst (soft/endorsement)
  - responder: NONE — library gap (DELL claimed by `equity_sector_rotation_momentum` (trending); endorsement not modeled)
- **AAPL: no hard corporate event** — used steep iPhone-17 discounts to regain the No. 2 spot in China's 618 festival (though sales still fell); a JPMorgan note argues Macs, not the iPhone, are Apple's AI growth driver. Soft demand/product framing.
  - gap_type: event_catalyst (demand signal, soft)
  - responder: NONE — library gap (AAPL claimed by trend-following)

**No fresh single-name news:** ARM (down in the rout, no company event), CBRS (0 items), CSCO (0), HPE (0), NUVL (0), ORCL/AVGO covered above, QCOM (index-cohort mention only; provisional), QQQ / SPY (chip-rout price only), SYNA (0 items; onsemi merger-arb carry), TSM (0 items; Samsung/foundry read-through only).

## Sector themes

- **Memory / semis — the day's dominant event.** Samsung's record Q2 (op profit +~1,810% YoY; DRAM ASP +~44%, NAND +~53%) *beat* but the stock fell ~8% after a ~150% YTD run — "buy the expectation, sell the confirmation." This dragged the whole US chip complex (MU/SNDK/MRVL/INTC/ARM −4–6%). Compounding: DeepSeek's reported in-house AI chip (NVDA) + the SK Hynix US listing (~7/10) rotation concern ("will MU/SanDisk foot the bill?"). **Net: the pricing cycle looks intact fundamentally; the move is positioning/sentiment.**
- **AI-capex "debt binge."** Amazon's ≥$25B bond sale (8 tranches; ~$54B YTD; ~$200B 2026 capex) is the marquee item in a broadening trend of hyperscalers funding AI infrastructure with debt — a structural capital-allocation theme that touches AMZN/MSFT/GOOGL/META/ORCL.
- **Energy / geopolitics.** The Hormuz tanker attacks + US revoking Iran's oil license lifted Brent 3% (5.6% after hours) and put energy/defensive sectors on top — a fresh oil-driven risk channel that had been dormant since last weekend's détente narrative.
- **Index-rebalance / forced-flow.** SPCX → Nasdaq-100 today (fell despite ~$4.3B inflow); SK Hynix US listing ~7/10. Recurring mechanical-flow theme the taxonomy still doesn't model.
- **Big-tech regulatory/trade overhang (carry).** DST-tariff threat (GOOGL/META/AMZN/AAPL), UK under-16 ban, Meta addiction litigation, SEC quarterly-reporting shake-up — a live cluster, no fresh imposition today.

## Candidates for the universe

**Promotion analysis (`news_manual.md §9`): 0 promotions. Universe stays 26.**
- **Tier A (3-session recurrence):** No candidate reached a clean 3-consecutive-catalyst run. **RIVN** did NOT advance — today it *fell on a dilutive public-offering announcement* (a new, negative event, not a continuation of the 7/2 delivery beat-and-raise), so its clean-catalyst clock stays ~1. CRDO absent again. WDC/STX/CRWV/NBIS are chip-rout sympathy / flow only. **No Tier-A promotion.**
- **Tier B (single-event triggers):** No qualifier on a *candidate*. The one clear 3+ bank initiation cluster (Tier-B #4) is **SPCX — already a universe member**, so no promotion. RIVN's public offering is dilutive (fails #3). No new confirmed M&A target (Fiserv is exploring a *unit* sale, not a takeover, and isn't a tracked candidate; SYNA/onsemi already in). No FDA binary; no candidate Tier-1 customer win. **No Tier-B promotion.**
- **No operator directive** to add a symbol this run.

Watch-list carried for tomorrow:
- **SK Hynix (SKHY)** — US listing ~**7/10 (Fri)**; promotable once it trades with a US ticker (memory cohort, technology). Not addable until then.
- **Syntiant** — Intel-backed edge-AI chipmaker filed for a Nasdaq IPO today; not trading yet, not promotable. Watch the pricing.
- **RIVN** — clock reset by today's dilutive raise; promote only on its own *earnings* beat-and-raise+5% or a clean 3-session catalyst run.
- **CRDO** — AI-interconnect; promote on a fresh same-week 3-bank initiation cluster or own beat-and-raise+5%.
- **WDC / STX / CRWV / NBIS** — memory / neocloud sympathy; Tier-A/B only.

## Macro / sector context

- **FOMC June minutes tomorrow (Wed 7/8)** — the first set under new Chair Warsh (a forecast-skeptic); the tone on the rate path is the watch item. Not a rate decision (Fed on hold at 3.50–3.75%). No first-tier US data today.
- **Geopolitics turned risk-off.** Iran's attacks on tankers near the Strait of Hormuz (Qatari LNG carrier Al-Rekayyat + a 2nd ship) and the US revoking Iran's oil-sale license sent Brent +3% ($74.16) intraday and +5.6% ($76.04) after hours — a sharp reversal of last weekend's US-Iran "great progress." **Equity indices fell only modestly (Nasdaq −1.2%); equity futures did not gap >2%, so this is escalation, not an equity shock — but watch the 7/8 open for oil/futures follow-through.**
- **Policy.** SEC weighing an end to mandatory quarterly reporting (investor pushback); DST-tariff / UK under-16 ban overhangs unchanged (no imposition); Trump-Accounts first 500k funded (soft).
- **Vol.** VIX ~16.13 (+0.56, +3.6%) — a bounce off benign, under the >3-pt regime threshold; normal contango. The vol lives in single-name event-IV (SPCX/JPM/TSLA/INTC/AMZN) and the new oil tail. Concrete UOA: bullish call sweeps buying the dip on NVDA ($200, 0DTE) and MU ($930, 7/10).

## Library gaps

`gap-registry coverage_holes` is **empty** — every item below is an **activation / assignment / taxonomy** gap (a rule exists in the library or an event type isn't modeled), not a registry hole. Re-listed for tomorrow's `tasks.md` → Saturday research:

- **Competitor-earnings / sector read-through event window — NEW instance (Samsung Q2 → MU/SNDK/MRVL/INTC/ARM chip rout).** No rule reads a *competitor's* earnings print as a signal on our names; `equity_event_driven_catalyst` models only a name's own window. *Research: a sector/peer-earnings read-through overlay.*
- **Capital-allocation / debt-raise event window — NEW instance (AMZN ≥$25B AI-capex bond sale) + JPM $50B buyback (carry) + MU Trump-Accounts (carry).** No rule reads a debt raise or buyback disclosure.
- **Product-launch / competitive-threat event window — META Muse Image (NEW); NVDA DeepSeek-chip threat + Kyber roadmap rebuttal (NEW).** No rule reads a product launch, a competitor-chip report, or a management roadmap denial.
- **Index-inclusion / forced-flow — SPCX → Nasdaq-100 today (NEW_CATEGORY_NEEDED, index_rebalance); SK Hynix ~7/10.** Taxonomy has no index_rebalance type; recurring — argues for a 6th Tier-B trigger or a forced-flow overlay. SPCX's own claim is provisional/quarantined.
- **Earnings/delivery-window assignment — JPM (7/14, window OPEN, most urgent), TSLA (7/22), INTC (7/23), AMZN (7/30), CBRS (carry).** All claimed by trend-following, not `equity_event_driven_catalyst`.
- **Regulatory / antitrust event window — DST-tariff (GOOGL/META/AMZN/AAPL), UK under-16 ban, Meta addiction litigation, SEC quarterly-reporting shake-up (NEW).** No rule reads a court / agency / trade action.
- **Pricing/margin + restructuring sub-triggers (carry) — INTC price hikes / MSFT 4,800 cuts.** No responder to a pricing-power or workforce-reduction disclosure.
- **M&A-arb activation — SYNA / onsemi (long SYNA / short ON at 1.350).** `equity_pairs_trading_cointegration` declares pairs_arbitrage but only provisionally claims SYNA.
- **Vol-regime activation — MU/SNDK selloff-driven single-name IV; the oil-driven index-vol tail from Hormuz.** Vol structures exist (`iron_condor_high_iv`, etc.) but aren't activated on single-name IV or an energy-shock channel.

## Recommendations for the trader

- **NOTABLE, not gating.** Weight this as a soft signal — nothing here requires deviation from the algorithmic-only mandate. The market is closed (`next_open 7/8`); positions ride their own rules.
- **First, confirm the account.** I observed the book INTACT this run (4 longs back, equity $103,106.76) — the 09:09 "wipe" looks transient/self-resolved. Re-snapshot `account`/`positions` yourself before any execute; if it re-confirms clean, the earlier P0 freeze rationale no longer applies. (Still your reconciliation call, not mine.)
- **SPCX stays quarantined.** It joined the Nasdaq-100 but fell ~7% and remains provisional/execution-quarantined — it will NOT trade regardless of the index tailwind. Confirm `unclaimed 0` / `provisional 3` and reconcile the re-stamped trend-following/event-driven/pairs claim reasons.
- **Held names are `responder: NONE`.** MU's chip-rout weakness is a *competitor's* earnings read-through (fundamentally the memory cycle looks intact), META's product launch/upgrade is positive, AVGO/ORCL had no fresh event — all informational, not entry/exit signals. Let the rules run.
- **Watch the overnight oil/geopolitics tail into 7/8** and the FOMC minutes (7/8). Neither makes today halt-worthy, but both could move the 7/8 open.
- **Options awareness:** IV is building into JPM (7/14), TSLA (7/22), INTC (7/23), AMZN (7/30); dip-buying call flow on NVDA/MU. The earnings-window strategy does not claim any of these (assignment gap; Saturday item).
- **Standard workflow otherwise.** The event cluster is real and two-sided (bearish rout vs. bullish memory pricing / dip-buying flow); don't manufacture action from it.
