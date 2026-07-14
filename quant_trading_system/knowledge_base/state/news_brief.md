# News brief for 2026-07-14

## Headline assessment

**NOTABLE — the week's most event-dense day, but it resolved CONSTRUCTIVELY and is NOT halt-worthy.** Four threads landed together and, on net, were market-friendly:

1. **June CPI came in COOLER than expected — the day's dominant macro event.** Headline **-0.4% MoM** (vs -0.2% consensus) → **3.5% YoY** (vs 3.8% expected, down from 4.2% in May), the biggest monthly headline drop since April 2020; core **flat MoM** (vs +0.2%) → **2.6% YoY** (vs 2.9%). Energy-led (energy -5.7% MoM). It slashed near-term rate-hike odds. Last inflation read before the 7/28-29 FOMC. (Caveat: this June print PRE-dates the current oil spike.)
2. **Bank-season kickoff — blowouts across the board.** **JPM** (watchlist): EPS $6.14 vs $5.85, revenue $58.02B vs $50.19B, **profit +41% YoY** on surging IB fees ("extremely risk-on"; Dimon "market risks mounting"). **GS**: **best quarter in its history** — EPS $20.98 (~2× YoY), revenue $20.34B +39%, **+6.9%** (IB fees boosted by the SpaceX IPO). BAC/C/WFC also reported strong.
3. **Warsh's hawkish congressional debut partly offset the dovish CPI.** "No tolerance for persistently elevated inflation"; on the print: "'mission accomplished'… that is not my view." No forward-guidance signal. Senate testimony Wed 7/15.
4. **US-Iran / Strait of Hormuz escalated for a THIRD day** — US reimposed a port blockade, tankers hit, oil to a one-month high (WTI +1.5% $79.34, Brent +1.72% $84.73). **But US equities closed GREEN** (S&P +0.32%, Nasdaq 100 +1.09%, Russell +0.61%) — the premarket dip reversed on cool CPI + bank beats.

Alongside: the **AI-memory cohort bounced hard** (hedge funds bought US semis at the fastest pace in 3.5 years, "selloff has run its course"; SKHY +6%, MU +3%, SNDK +5%, NVDA +3%), reversing Monday's de-rate. VIX ~17 (roughly flat/lower) — orderly. `market-status`: `is_open false`, `now 2026-07-14 15:39 PT`, `next_open 2026-07-15 09:30 ET` — canonical post-close run, single fire. 144 Alpaca items (NVDA 15 / JPM 12 / SKHY 11 / MU 10). **Fresh, on-time Tuesday run.**

**None of the three HALT-WORTHY triggers fires:** (1) **no FOMC today** — CPI/Warsh today, FOMC is 7/28-29; (2) held name **META** had **no adverse catalyst** (its only touchpoint was the NY data-center-freeze policy item, a mild/cross-name capex headwind, not a >5σ single-name shock); (3) the geopolitical escalation **did not gap equity futures >2%** — the tape closed green. Oil-sensitive and fluid → caution flag, not a halt.

> **For the trader (P0 triage):** universe **33 → 34** — promoted **GS (Goldman Sachs, financials)** under Tier-0 (news-subject: best quarter in its history, +6.9%, dedicated coverage; also fills the long-flagged financials-breadth gap — JPM had been the only bank). It lands **UNCLAIMED**; run `triage-symbol GS --gap-type earnings_window` (GS has real price history, so expect a rankable backtest → a trading claim or a below-baseline provisional, NOT the no-history watch_only route). Provisional 5 unchanged: **QCOM/SPCX/SYNA** (`revalidate_by 2026-07-21`), **SKHY** (`2026-07-24`), **RIVN** (`2026-07-27`). WULF is validated (`equity_rsi_divergence`) — not provisional. `gap-registry coverage_holes` **empty**.

> **On the held book:** universe `by_source` still shows **positions = META only**. META had no fresh corporate catalyst today (the "+21% in 3 weeks / market's darling" framing is price/opinion — dropped); its one real touchpoint is the NY 50MW data-center freeze (a capex/permitting headwind shared with MSFT/AMZN/GOOGL). It rides its `equity_momentum_macd_histogram` exit — I do not and cannot advise overriding an algorithmic rule.

## Watchlist + positions

Event-driven lines (a thing that *happened*), each tagged with a canonical `gap_type` + algorithmic responder. Price moves omitted — the trader has bars.

- **JPM (watchlist): Q2 earnings BLOWOUT** — EPS $6.14 vs $5.85, revenue $58.02B vs $50.19B, profit +41% YoY on surging IB fees; full call transcript out. Dimon flagged "mounting market risks" even as the desk called markets "extremely risk-on." The marquee earnings event of the day.
  - gap_type: earnings_window
  - responder: NONE — library gap (JPM claimed by `equity_trend_following_ema_cross`, NOT `equity_event_driven_catalyst`/`long_straddle_earnings` — earnings-window assignment gap; the print is now OUT, post-earnings drift is the only remaining window)
- **GS (universe as of today, UNCLAIMED): Q2 — best quarter in Goldman's history** — EPS $20.98 (~2× YoY), revenue $20.34B +39% YoY, shares +6.9%; IB fees lifted by the SpaceX IPO. Newly promoted (Tier-0), awaiting P0 triage.
  - gap_type: earnings_window
  - responder: NONE — library gap (GS unclaimed pending `triage-symbol GS --gap-type earnings_window`; no earnings-window responder is active on it yet)
- **TSM (watchlist): Q2 earnings Thu 7/16** — June revenue +67.9% YoY already disclosed (hard AI-demand signal); consensus models ~59% Q2 profit growth; large options-implied move building.
  - gap_type: earnings_window (+ event_catalyst for the June revenue disclosure)
  - responder: NONE — library gap (TSM claimed by `equity_trend_following_ema_cross`; earnings-window assignment gap; window opens 7/16)
- **NVDA (watchlist): cut more than half of its Asian AI-chip customers** to comply with tighter US export screening on China; separately, Vera Rubin hardware rollout reportedly slightly delayed (analysts see limited financial impact).
  - gap_type: event_catalyst (regulatory/export-control commercial action + product-roadmap)
  - responder: NONE — library gap (NVDA claimed by `equity_trend_following_ema_cross`; no regulatory/export-control or product-roadmap responder)
- **AAPL (watchlist): record 20% Q2 smartphone market share, +3% unit growth** even as memory shortages hit rivals (a real demand/share disclosure). Separately KeyBanc cut AAPL to Underweight (analyst opinion — not an event).
  - gap_type: event_catalyst (demand/market-share data)
  - responder: NONE — library gap (AAPL claimed by `equity_trend_following_ema_cross`; no demand/share responder)
- **RKLB (watchlist): Neutron AVac engine passed a critical full-duration hot-fire test** — a key qualification milestone toward the Neutron rocket's planned late-2026 debut (product/engineering catalyst).
  - gap_type: event_catalyst (product/engineering milestone)
  - responder: NONE — library gap (RKLB claimed by `equity_breakout_volume_confirmation`; no product-milestone responder. If the milestone triggers a volume-confirmed breakout, the existing claim would mechanically respond — but nothing reads the milestone itself)
- **MU / SNDK / SKHY (memory cohort): sharp REBOUND, reversing Monday's de-rate** — hedge funds bought US semis at the fastest pace in 3.5 years, betting the selloff has "run its course." SK Hynix's US ADR trades ~50% premium to Seoul on scarcity; first 2×-leveraged SK Hynix ETF (HYNX) launched.
  - gap_type: event_catalyst (sector/cohort sentiment reversal; forced-flow/ETF mechanics for SKHY)
  - responder: NONE — library gap (MU/SNDK claimed by `equity_event_driven_catalyst`/`equity_momentum_macd_histogram`, which model discrete single-name catalysts, not a cohort-wide flow reversal; SKHY is on `equity_watch_only` — never trades. No cohort-reversal or float/ETF-mechanics responder)
- **META (held): NY to freeze new 50MW+ AI data centers for up to a year** (grid strain) — a permitting/capex headwind to the hyperscaler buildout (shared with MSFT/AMZN/GOOGL). No META-specific corporate catalyst today; prior constructive capex/pricing items are carries.
  - gap_type: event_catalyst (policy/capex headwind)
  - responder: NONE — library gap (META claimed by `equity_momentum_macd_histogram` (trending); no policy/capex responder — position rides its MACD exit)

**No fresh single-name news** (price/analyst/cohort only — nothing that *happened*): **ARM** (-6% on an HSBC valuation-downgrade — analyst opinion; earnings 7/23 carry), **MRVL** (KeyBanc PT raise citing AMZN/GOOGL custom-silicon design wins — analyst framing), **MSFT** (NY data-center freeze cross-tag; AI-spend commentary), **AMZN** (cohort/AI-datacenter mentions; Q2 earnings 7/30 carry), **GOOGL** (Marvell/Evercore cross-tags; AI-"tsunami" op-ed — opinion), **AVGO** (semis-cohort rebound; lot exited 7/9), **ORCL** (radar/cohort mentions), **INTC** (whale-alert rollup; UMC-peer photonics; earnings 7/23), **SPCX** (Cathie Wood added $21.3M; pundit bear takes; SpaceXAI leasing Grok capacity to Anthropic — provisional/quarantined), **CSCO / DELL / QCOM / SYNA / SMCI / HPE / NUVL / CBRS / IRDM / WULF** (0 or price/cohort-only items), **QQQ / SPY** (index/macro — trader has bars).

## Sector themes

- **AI-memory de-rate REVERSED — Monday's cohort selloff bounced.** Hedge funds bought US semiconductors at the fastest pace in at least 3.5 years last week, reversing two weeks of heavy selling on a bet the selloff has "run its course" (Goldman). SKHY +6%, MU +3%, SNDK +5%, NVDA +3%. A concrete positioning/flow reversal, not just price: the supercycle-pace-repricing scare from Samsung's guidance (7/13) did not stick. SK Hynix scarcity is acute — its US ADR trades a ~50% premium to Seoul and the first 2×-leveraged SK Hynix ETF (HYNX) launched today.
- **Bank earnings signal a strong economy.** Five big banks (JPM/GS/BAC/C/WFC) reported Q2 blowouts on surging IB (SpaceX-IPO-driven) and trading revenue (~$39B combined); JPM +41% profit, GS its best quarter ever. The sector narrative has fully shifted from rate-sensitivity to trading/IB/IPO-activity growth engines. Financials breadth improves with the GS promotion.
- **Momentum-factor "crash."** Goldman flags one of the worst three-week S&P 500 momentum-factor draw-downs on record — a factor rotation/dispersion signal. Wide single-name dispersion today (GS +6.9% / SNDK +5% vs ARM -6%) under a calm index VIX.
- **AI-datacenter capex meets a permitting brake.** New York is reportedly freezing new 50MW+ AI data centers for up to a year on grid strain — the first state-level siting brake, touching every hyperscaler (META/MSFT/AMZN/GOOGL). Buildout demand intact; the binding constraint shifts toward grid/permitting. Some AI-spend skepticism surfaced (Chamath: "wheels come off"; IBM lower dragging software).
- **Vol regime orderly.** VIX ~17 despite CPI + five bank prints + Warsh + live Iran/oil escalation — the market absorbed a very dense day without a vol spike. Event-IV building into TSM (7/16) and the 7/22-30 earnings run.

## Candidates for the universe

**PROMOTED today (universe 33 → 34):**
- **GS (Goldman Sachs, financials)** — Tier-0 news-subject: reported the **best quarter in its history** (EPS $20.98, revenue $20.34B +39% YoY, +6.9%), with dedicated single-name coverage. Also resolves the recurring financials-breadth gap (JPM had been the only bank). Lands unclaimed → P0 triage (`earnings_window`; has real history, expect a rankable backtest).

**Tracking (NOT promoted — cohort mentions, thematic, or modest single-name catalysts):**
- **BAC / C / WFC** — reported Q2 alongside JPM/GS but arrived in cohort coverage (earnings-scheduled lists, "banks to watch," whale-alert rollups), not dedicated single-name catalyst articles. **MS** — reports Wed 7/15; today's coverage was price-action framing. Financials-breadth *partly* addressed via GS; these stay candidates. (Recurrence: session 2.)
- **IBM** — dropped, "dragging software," on AI-spend skepticism (Chamath). A thematic/sentiment peg (no hard IBM corporate catalyst), so tracked, not promoted. Recurring "AI-capex-doubt" name.
- **UMC (United Microelectronics)** — silicon-photonics mass production milestone + expanding AI-DC roadmap (July earnings). A real but modest single-name catalyst from a mid-tier foundry; semis are already heavily represented → tracked, not promoted.
- **WDC** — memory-cohort name; participated in today's bounce but no WDC-specific event. Recurring memory-cohort track.

## Macro / sector context

- **June CPI (released 7/14, 8:30 AM ET):** headline **-0.4% MoM / 3.5% YoY** (vs -0.2% / 3.8% consensus, from 4.2% May) — biggest monthly headline drop since April 2020; core **flat / 2.6% YoY** (vs +0.2% / 2.9%). Energy index -5.7% MoM (biggest since April 2020) but +15.7% YoY. Cooler than expected on both lines → cut near-term rate-hike odds. Last inflation read before the **7/28-29 FOMC**. **Important:** the June data predates the current Iran-driven oil spike, so it understates forward energy/inflation pressure (gasoline seen >$4/gal within 7-10 days).
- **Fed Chair Warsh, first semi-annual testimony (House 7/14, Senate 7/15):** hawkish-measured — "no tolerance for persistently elevated inflation," "resolute commitment to restoring price stability"; explicitly rejected reading the cool CPI as "mission accomplished." No guidance on whether hikes come. Fed funds held 3.50-3.75% at the June meeting. Net: tempered the dovish print.
- **Geopolitics (fresh, material, escalating):** US-Iran hostilities entered a third day — the US reimposed a blockade on Iran's ports (4 PM ET), tankers were hit in the Strait (one mariner killed), transits fell >50%. Oil to a one-month high (WTI $79.34 +1.5%, Brent $84.73 +1.72%); Trump dropped his 20% Hormuz-toll demand. **US equities absorbed it and closed green — no >2% futures gap.** Live overnight tail.
- **Policy:** NY freezing new 50MW+ AI data centers (grid strain) — hyperscaler capex/permitting headwind. NVDA cut >half its Asian AI-chip customers on China export screening. California's $3,500 first-time-buyer EV rebate — modest EV tailwind (TSLA/RIVN).
- **Vol:** VIX ~17, roughly flat/lower; orderly despite the event stack. Wide single-name dispersion; event-IV building into TSM 7/16.

## Library gaps

`gap-registry coverage_holes` is **empty** — every item below is an **activation / assignment / taxonomy** gap (a rule/event-type isn't mapped to the symbol that had the event), not a registry hole. Re-listed for tomorrow's `tasks.md` → Saturday research:

- **Earnings/print-window assignment — JPM (printed 7/14), GS (printed 7/14, newly promoted), TSM (7/16), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** All claimed by trend-following / breakout, not `equity_event_driven_catalyst` / `long_straddle_earnings`. The most acute recurring gap; two blowout prints just went unresponded (JPM/GS) and TSM opens 7/16.
- **Sector / cohort sentiment reversal (bidirectional) — the AI-memory de-rate (7/13) → rebound (7/14).** No rule reads a cohort-wide flow/sentiment swing (Samsung guidance down-leg, then hedge-fund-buying up-leg). *Research: a cohort/sector risk overlay that handles both directions.*
- **Regulatory / export-control commercial action — NVDA cut >half of Asian AI-chip customers on China screening.** No rule reads an export-control-driven demand action. *Research: a regulatory/policy-event overlay (also covers AAPL litigation carry, META EU DSA carry).*
- **Policy / capex-headwind — NY 50MW data-center freeze (META/MSFT/AMZN/GOOGL).** No rule reads a permitting/grid brake on the capex thesis. *Research: a capex/policy overlay (pairs with the prior META Hyperion / MU reshoring capex gap).*
- **Index / forced-flow + ETF/float mechanics — SKHY ADR 50% premium + 2×-leveraged HYNX ETF launch; SPCX lockup/float carry.** Recurring across sessions → argues for a 6th Tier-B trigger or a forced-flow overlay. `NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`.
- **Product/engineering-milestone — RKLB Neutron engine hot-fire test; NVDA Vera Rubin roadmap; TSLA Optimus line carry.** No rule reads an engineering/qualification milestone. *Research: a product-catalyst overlay.*
- **Geopolitical / energy-shock overlay — US-Iran Hormuz (3rd day), oil at 1-month high, gasoline >$4/gal forward.** No rule reads an oil/geopolitical shock or its inflation read-through. *Research: a macro/energy-shock risk overlay.*
- **Vol-regime activation — orderly VIX ~17 but wide single-name dispersion; event-IV into TSM/TSLA/ARM/INTC/AMZN.** Options structures (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) exist but aren't activated on an earnings-IV / dispersion screen.
- **New-listing no-history triage — SKHY (still `equity_watch_only`), RIVN (degenerate-0-trade provisional).** Feeds the recurring fallback-threshold question (no-history / 0-trade → watch_only vs below-baseline trading provisional). GS (promoted today) has real history and should NOT hit this path.

## Recommendations for the trader

- **NOTABLE, not gating.** Weight this as a soft signal — nothing here requires deviation from the algorithmic-only mandate. The cool CPI, bank blowouts, memory rebound, and Warsh's hawkish tone are all informational; positions ride their own rules.
- **GS triage (new):** run `triage-symbol GS --gap-type earnings_window`. GS has real price history, so expect a rankable backtest — a trading claim if it clears baseline, else a below-baseline trading provisional (NOT the no-history watch_only route). Don't force a claim beyond what the score supports.
- **Provisionals unchanged:** QCOM/SPCX/SYNA stay quarantined (`revalidate_by 7/21`); SKHY (`7/24`); RIVN (`7/27`). Do NOT re-triage claimed symbols. SKHY's ADR-premium / leveraged-ETF activity does not change its watch_only quarantine.
- **Held name META:** no adverse catalyst today; the NY data-center freeze is a mild, shared policy headwind, not a basis to override its MACD rule. Soft note only.
- **JPM / GS printed today; TSM prints 7/16.** Two blowouts already out; TSM's window opens Thursday with a large implied move. None makes *today* halt-worthy, but earnings-window IV is live — informational for any options posture.
- **Watch the geopolitical + inflation-path tail.** The Iran/Hormuz escalation is live and oil-sensitive; the cool June CPI predates the oil spike, and Warsh is explicitly not declaring victory. If the situation gaps equity futures >2% overnight, that would be the halt-worthy line — it is not there today (equities closed green).
- **Standard workflow otherwise.** The event cluster is real but the market reaction was orderly and constructive (green tape, VIX ~17) — don't manufacture action from it.
