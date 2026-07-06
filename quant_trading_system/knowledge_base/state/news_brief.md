# News brief for 2026-07-06

## Headline assessment

**NOTABLE — real single-name corporate events cluster + SPCX joins the Nasdaq-100 tomorrow; NOT halt-worthy.** First full session after the July 4 holiday weekend (`market-status`: `is_open false`, `next_open 2026-07-07 09:30 ET` — today's cash session already closed; this is the canonical 3:30 PM PT post-close run). The tape was risk-on (Dow record close >53,000, Nasdaq +1.1% on a semi rebound — price action, dropped), but underneath it were several genuine events: **two customer/supply deals on names we hold or track (Micron-Ford, Broadcom-Apple-to-2031), a Microsoft 4,800-job restructuring, an NVDA product-roadmap slip (Kyber NVL144), and Intel joining Apple in raising chip prices** — plus a concrete near-term calendar: **SPCX is added to the Nasdaq-100 TOMORROW (Tue 7/7, ~$4.3B forced passive buying)**, Samsung Q2 prelim is 7/7, SK Hynix lists on Nasdaq 7/10, and JPM's earnings window (7/14) is now open. **None of the three HALT-WORTHY triggers fires:** no FOMC (Fed on hold, next meeting late July); no confirmed adverse overnight catalyst on a held position (Micron-Ford and Broadcom-Apple are *positive* supply/partnership news, not shocks); no geopolitical event moving futures >2% (US-Iran talks made "great progress" over the weekend — risk-positive). 144 Alpaca items; density NVDA 16 / TSLA 15 / MU 14 / SPCX 14 / AAPL 13. **Universe stays 26; 0 promotions.** `list-active`: claimed 26, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**; `gap-registry coverage_holes` **empty**.

> **Provisional-claim note for the trader:** **SPCX's `revalidate_by 2026-07-04` has now lapsed** (it was this past Saturday) and it is **still PROVISIONAL / execution-quarantined** — Saturday research did not clear it to baseline. It joins the Nasdaq-100 tomorrow but remains **non-tradable** until validated. QCOM and SYNA `revalidate_by 2026-07-10`.

## Watchlist + positions

Event-driven lines (a thing that *happened*), each tagged with a canonical `gap_type` + algorithmic responder. Price moves are omitted — the trader has bars.

- **MU (held): Micron-Ford long-term memory-supply agreement** (Strategic Customer Agreement) for next-gen vehicles, backed by expanded advanced-DRAM capacity at the Manassas, VA fab — days after a similar **Micron-GM** deal; one of 16 SCAs cited on the fiscal-Q3 call. A concrete automotive-memory **customer win + US-capex** event on the deepest-tracked memory name.
  - gap_type: event_catalyst
  - responder: NONE — library gap (MU's `equity_event_driven_catalyst` claim is PROVISIONAL/quarantined at Sharpe 0.0 and models earnings windows, not supply-agreement disclosures)
- **AVGO (held): Broadcom-Apple chip supply deal reportedly extended through 2031.** AVGO rose on the report — a multi-year **partnership/customer-win extension** on the book's semi name.
  - gap_type: event_catalyst
  - responder: NONE — library gap (AVGO's `equity_event_driven_catalyst` claim is PROVISIONAL/quarantined, Sharpe 0.0)
- **AAPL: Broadcom partnership extended to 2031 (positive) + sits under the DST-tariff overhang** (Meta/Alphabet/Amazon/Apple exposed if the EU levies a Digital Services Tax). Foldable iPhone may slip months past the iPhone 18 (Kuo) — product-timing, minor.
  - gap_type: event_catalyst
  - responder: NONE — library gap (AAPL claimed by `equity_trend_following_ema_cross` (trending), which does not read partnership/regulatory events)
- **NVDA: Kyber NVL144 roadmap DELAY** — a product/roadmap slip that opens a competitive window for alternative AI-hardware suppliers (MRVL benefited directly). Nemotron full-stack push is softer strategy commentary; Michael Burry short-thesis rebuttal is carry.
  - gap_type: event_catalyst
  - responder: NONE — library gap (NVDA claimed by trend-following; no rule reads a roadmap slip)
- **MRVL: surged as NVDA's Kyber delay opened a competitive window** for alt AI-hardware suppliers; also named in BofA's "chip selloff is a bear trap / $1.5T AI buildout" list.
  - gap_type: event_catalyst (competitor-delay read-through)
  - responder: `equity_breakout_volume_confirmation` *may* respond to the resulting momentum **if volume/ADX-confirmed**; the underlying *event* has no event-driven responder → effectively a library gap
- **MSFT: cutting 4,800 jobs**, primarily Xbox, restructuring toward AI spend. A workforce-reduction/restructuring event.
  - gap_type: event_catalyst
  - responder: NONE — library gap (MSFT claimed by `equity_momentum_macd_histogram` (trending); no restructuring responder)
- **INTC: raised chip prices up to $50** ("market dynamics") — following Apple's ~55% hardware hikes; extends the input-cost/pricing-power theme. Separately, **Q2 earnings July 23** (enters the 14-day options window ~7/9).
  - gap_type: event_catalyst (pricing/margin disclosure) + earnings_window (7/23)
  - responder: NONE — library gap (INTC claimed by `equity_breakout_volume_confirmation` (trending); no pricing-power or earnings-window responder claims INTC)
- **SPCX (PROVISIONAL / execution-quarantined): joins the Nasdaq-100 TOMORROW (Tue 7/7)**, ~$4.3B forced passive buying — Monday is the last news read before the add. Separately, a "hidden 30% rule" could unlock ~456M additional shares after earnings if the stock holds >$175.50 before Aug 3 (**supply overhang**). FCC satellite-licensing vote 7/22.
  - gap_type: event_catalyst — index-inclusion forced-flow, which the canonical taxonomy does not cover → also **NEW_CATEGORY_NEEDED** (index-rebalance)
  - responder: NONE — library gap (SPCX's trend-following claim is PROVISIONAL/quarantined AND no rule reads an index-inclusion forced-flow event)
- **GOOGL: DST-tariff overhang + UK child-safety pushback.** Trump's 100% DST-tariff threat and Britain's under-16 social-media ban both name GOOGL (regulatory/trade overhang). No *fresh* GOOGL-specific court ruling today (the EU €4.1B Android fine upheld 7/2 is carry).
  - gap_type: event_catalyst
  - responder: NONE — library gap (GOOGL claimed by trend-following; no litigation/regulatory event responder)
- **META (held; BUY 16 live, avg $605.28): DST-tariff + UK child-safety overhang.** No new META-specific event; the AI-cloud thesis is carry. The position is governed by its own `equity_momentum_macd_histogram` exit — the *news* is `responder: NONE`, not a fresh entry/exit signal.
  - gap_type: event_catalyst
  - responder: NONE — library gap (regulatory overhang has no responder; the position rides its MACD rule)
- **JPM: Q2 earnings Tue 7/14** (~7am ET release; ~$5.44/sh est, +9.7% YoY) — kicks off bank season, now ~6 trading days out and **inside the 14-day options window**. $50B buyback effective 7/1 (consummated). No fresh single-name event today.
  - gap_type: earnings_window
  - responder: NONE — library gap (JPM claimed by trend-following, not the earnings-window strategy — assignment gap)
- **TSLA: no fresh hard event** — delivery-beat digestion; the binary is the **July 22 earnings call** (margins the focus). Cybercab accessibility detail + Leapmotor Mexico entry are minor.
  - gap_type: earnings_window
  - responder: NONE — library gap (TSLA claimed by trend-following, not earnings-window — assignment gap)
- **DELL: rose after Trump told people to "buy a Dell computer"** in the Oval Office — soft endorsement catalyst; Michael Dell reaffirmed his $6.25B Trump-Accounts pledge.
  - gap_type: event_catalyst (soft/endorsement)
  - responder: NONE — library gap (DELL claimed by `equity_sector_rotation_momentum` (trending); endorsement not modeled)

**No fresh single-name news:** AMZN (DST overhang only — folded into policy), ARM, CBRS, CSCO, HPE, NUVL, ORCL (no new event; restructuring drawdown is carry, price-only), QCOM (options-scan mention only; provisional), QQQ, SNDK (memory-cohort read-through, no single-name event), SPY, SYNA (no items; live onsemi merger-arb is carry), TSM (Apple/Intel price-hike foundry read-through only).

## Sector themes

- **Memory supercycle — twin catalysts this week.** Samsung Q2 preliminary earnings **tomorrow (7/7)**, record profit expected on AI-memory demand; SK Hynix lists ADRs on Nasdaq **7/10 (ticker SKHY, ~$166/ADS)**. Direct read-through to MU / SNDK; Micron-Ford (+ Micron-GM) SCAs add an automotive-demand leg.
- **AI-capex / compute build-out.** BofA called the June semi selloff a "bear trap" tied to a $1.5T AI buildout (MU/MRVL named); US tech funds drew a **record $14.3B weekly inflow** (2nd-biggest ever) even as broad equity funds saw the biggest outflows since March — an AI-conviction rotation. NVDA's Kyber delay reshuffles the AI-hardware supplier map (MRVL beneficiary).
- **Input-cost / pricing-power (two-sided, extending).** After Apple's ~55% hardware hikes, **Intel raised chip prices up to $50** — memory/component cost pass-through is broadening across device and chip makers.
- **Big-tech regulatory/trade overhang.** DST-tariff threat (GOOGL/META/AMZN/AAPL) + UK under-16 social-media ban + the carried GOOGL EU €4.1B fine — a live regulatory cluster with no algorithmic responder.
- **Index-rebalance / forced-flow.** SPCX → Nasdaq-100 Tue 7/7 (~$4.3B); SK Hynix listing 7/10. Recurring mechanical-flow theme.

## Candidates for the universe

**Promotion analysis (`news_manual.md §9`): 0 promotions. Universe stays 26.**
- **Tier A (3-session recurrence):** No candidate reached a clean 3-consecutive-catalyst run. **RIVN** is at ~session 2 — but today's coverage merely restates the same Q2 delivery beat-and-raise from 7/2 (12,194 delivered vs 9-11k guide; FY raised to 65-70k); **no fresh catalyst → clock did not truly advance.** **CRDO** absent again (clock did not advance). WDC/STX/CRWV/NBIS are sympathy/flow only. **No Tier-A promotion.**
- **Tier B (single-event triggers):** No qualifier. No new confirmed M&A target (SYNA/onsemi already in universe); no FDA binary; **RIVN's beat-and-raise is a DELIVERY print, not an *earnings* print → fails Tier-B #3**; no fresh same-week 3-bank initiation cluster; no candidate Tier-1 customer-win press release (Micron-Ford and Broadcom-Apple are *universe* names, not candidates). **No Tier-B promotion.**
- **No operator directive** to add a symbol this run.

Watch-list carried for tomorrow:
- **RIVN** — session ~2, delivery beat-and-raise (consumer-discretionary). Promote on its own *earnings* beat-and-raise+5% or a clean 3-session catalyst run.
- **SK Hynix (SKHY)** — lists on Nasdaq **7/10**; promotable once it trades with a US ticker (memory cohort). Not addable until then.
- **CRDO** — AI-interconnect; promote on a fresh same-week 3-bank initiation cluster or own beat-and-raise+5%.
- **WDC / STX** — memory cohort, flow only; Tier-A/B only.
- **CRWV / NBIS** — neoclouds, sympathy to the cloud build-out; watch.
- **Samsung** — foreign-listed (SSNLF OTC), not addable; memory read-through only.

## Macro / sector context

- **No first-tier US data today** (light post-holiday Monday). Backdrop unchanged: **June NFP +57k big miss** (UE 4.2% on a 61.5% participation slump), read dovishly; **Fed on hold** (Warsh no-signal at Sintra); next macro is the **July CPI/PPI calendar** into the late-July FOMC.
- **Policy — Trump's 100% DST-tariff threat resurfaced** (originated June 26): any country levying a Digital Services Tax on US tech faces an immediate 100% tariff on all goods to the US. The US-EU deal caps most tariffs at 15% through 2029 but excluded DST; France/Italy/Spain/Austria/UK have national DSTs. Overhang, **no action imposed**. **UK under-16 social-media ban** drew US-tech pushback; **DOGE officially sunset July 4**. **US-Mexico-Canada trade-deal review window** (carry) — no escalation over the weekend.
- **Geopolitics risk-positive.** US-Iran made "great progress" in weekend Switzerland talks (Qatar/Pakistan mediating) — roadmap to a final deal within 60 days; Strait of Hormuz to reopen to commercial vessels. Oil firm but near ~4-month lows. No futures shock.
- **Vol — VIX ~15.8, sub-16, benign**; drifted lower from ~16.6 (7/2 close) on the risk-on session. Normal contango, no inversion. Dispersion is single-name/event-IV: SPCX into 7/7, JPM into 7/14, TSLA into 7/22, MU post-print IV crush.

## Library gaps

`gap-registry coverage_holes` is **empty** — every item below is an **activation / assignment / taxonomy** gap (a rule exists in the library or an event type isn't modeled), not a registry hole. Re-listed for tomorrow's `tasks.md` → Saturday research:

- **Customer / supply-agreement event window — NEW instance (MU Micron-Ford + Micron-GM; AVGO Broadcom-Apple-2031).** `equity_event_driven_catalyst` claims these names only provisionally (quarantined, Sharpe 0.0) and models earnings windows, not supply/partnership disclosures. *Research: extend/validate the event-driven template to read strategic customer-agreement and multi-year partnership disclosures.*
- **Product/roadmap-slip sub-trigger — NEW (NVDA Kyber NVL144 delay; MRVL competitive-window read-through).** No rule reads a product-roadmap slip or its competitor read-through. *Research: a supply-chain/roadmap-event overlay.*
- **Restructuring / workforce-reduction event window — MSFT (4,800 cuts, NEW) + ORCL (carry).** Recurring big-tech class; no responder.
- **Pricing/margin-disclosure sub-trigger — INTC price hikes (NEW) + AAPL 55% hikes (carry).** No rule reads a pricing-power / input-cost event.
- **Regulatory/antitrust event window — DST-tariff (GOOGL/META/AMZN/AAPL, NEW resurfacing), UK under-16 ban (GOOGL/META/MSFT, NEW), GOOGL EU €4.1B (carry), META India/addiction (carry).** No rule reads a court/agency/trade action.
- **Index-inclusion / forced-flow — SPCX → Nasdaq-100 7/7 (NEW_CATEGORY_NEEDED); SK Hynix 7/10.** The canonical taxonomy has no index_rebalance type; recurring — argues for a 6th Tier-B trigger or a forced-flow overlay. SPCX's own claim is provisional/quarantined.
- **Earnings/delivery-window assignment — JPM (7/14, window now open), TSLA (7/22), INTC (7/23), CBRS (carry).** All claimed by trend-following, not `equity_event_driven_catalyst`. JPM is the most urgent.
- **M&A-arb activation — SYNA / onsemi (long SYNA / short ON at 1.350).** `equity_pairs_trading_cointegration` declares pairs_arbitrage but only provisionally claims SYNA.
- **Capital-allocation event window — JPM $50B buyback (consummated); MU Trump-Accounts (carry).** No rule reads a buyback/return disclosure.
- **Vol-regime activation — MU post-print IV crush.** Vol-selling/buying structures exist (`iron_condor_high_iv`, etc.) but aren't activated on single-name IV moves.

## Recommendations for the trader

- **NOTABLE, not gating.** Weight this brief as a soft signal — nothing here requires deviation from the algorithmic-only mandate. There is no `execute` decision until after the news; the market is closed now (`next_open 7/7`).
- **Re-check `provisional_count` and SPCX specifically.** SPCX's `revalidate_by 7/04` has lapsed and it is still quarantined the day before its Nasdaq-100 add — it will **not** trade regardless of the forced-flow tailwind. Confirm P0 (`unclaimed 0`) after the weekend and that no new universe member appeared.
- **Held positions ride their own rules.** MU's Micron-Ford deal, AVGO's Broadcom-Apple extension, and META's regulatory overhang are all `responder: NONE` — informational, not entry/exit signals. **MU's trailing stop still had not fired** as of the 7/3 handoff after its round-trip; reconcile any rule-driven trim on today's session and watch the give-back scenario.
- **Consider the IV build into JPM (7/14, window now open) and TSLA (7/22)** when weighting any options posture — but the earnings-window strategy does not claim either name (assignment gap; Saturday item).
- **Standard workflow otherwise.** The event cluster is real but mostly positive/benign and largely `responder: NONE`; don't manufacture action from it.
