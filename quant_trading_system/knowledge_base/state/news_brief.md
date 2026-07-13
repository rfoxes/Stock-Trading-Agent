# News brief for 2026-07-13

## Headline assessment

**NOTABLE — event-rich and risk-off, but NOT halt-worthy.** Three live threads today, none of which trips a halt trigger:

1. **A memory / DRAM cohort selloff — the day's dominant *event*.** Samsung posted a *record* preliminary Q2 (operating profit ~89.4T won / ~$58.4B, ≈19× YoY on AI memory/HBM), yet its shares fell ~10.7% in Seoul as investors punished anything short of perfection on AI-supercycle *sustainability*. That triggered profit-taking across AI-memory names — **MU -~5%, SNDK -~5%, SK Hynix (SKHY) -15.4% in Seoul, WDC**; the DRAM ETF is now ~-30% in under a month ("bear market"). This is a genuine sentiment reversal from Friday's SK-Hynix-debut euphoria.
2. **Fresh US-Iran airstrikes over the Strait of Hormuz.** The US struck Iran after an Iranian attack on a container ship in the Strait; oil surged ~5% (Brent ~$79.59, WTI ~$74.85). **But US equity futures were contained — S&P -0.3%, Nasdaq -0.8%, Dow ~flat — well below the >2% halt trigger.** Energy names (XOM/COP/CVX) +~1%.
3. **A dense 7/14 event stack (tomorrow).** June CPI (8:30 AM; consensus headline ~3.8% YoY / core ~2.8%) + Fed Chair Warsh's first semi-annual testimony (House Tue, Senate Wed) + **five big banks reporting BMO simultaneously (JPM/GS/BAC/C/WFC)**. Last inflation read before the 7/28-29 FOMC.

VIX 17.16 (+2.13 pt / +14% — a real risk-off pop, just below the 3-pt "notable" bar, still MID band). `market-status`: `is_open false`, `now 2026-07-13 15:39 PT`, `next_open 2026-07-14 09:30 ET` — canonical post-close run, single fire. **This is a genuine, fresh Monday 7/13 run** (the prior brief was Friday 7/10 data completed late Monday; that staleness is now resolved). 129 Alpaca items (NVDA 14 / MU 12 / SPCX 12 / META 10).

**None of the three HALT-WORTHY triggers fires:** (1) **no FOMC decision today** — CPI/Warsh is *tomorrow*, FOMC is 7/28-29; (2) the held name **META** had *constructive* events (Hyperion $50B+ capex, AI-API price cut) — no adverse >5σ catalyst; (3) the geopolitical escalation **did not gap equity futures >2%** (Nasdaq -0.8%). Situation is fluid/oil-sensitive → flagged as caution, not a halt.

> **For the trader (P0 triage):** universe **32 → 33** — promoted **RIVN** (Tier-0 news-subject: discounted 75M-share public offering, its own coverage). It lands **UNCLAIMED**; expect `triage-symbol RIVN --gap-type event_catalyst` to route to a watch/provisional grade (limited/again-degenerate backtest likely). **SKHY** is already in-universe on **`equity_watch_only`** (provisional/quarantined, `revalidate_by 2026-07-24`) — do not re-triage a claimed symbol; it's simply caught in today's memory selloff. Provisional 4 unchanged: **QCOM, SKHY, SPCX, SYNA** (WULF was released to validated `equity_rsi_divergence` on 7/11). `gap-registry coverage_holes` **empty**.

> **On the held book:** universe `by_source` still shows **positions = META only**. META's day was *constructive* (capex + product/pricing), though the stock is noted overbought/near resistance and is caught in the broad tech risk-off. It rides its `equity_momentum_macd_histogram` exit — I do not and cannot advise overriding an algorithmic rule.

## Watchlist + positions

Event-driven lines (a thing that *happened*), each tagged with a canonical `gap_type` + algorithmic responder. Price moves omitted — the trader has bars.

- **META (held): expanded its Hyperion AI data center into a $50B+ project** (Louisiana tax incentives); separately, **JPMorgan flagged Meta's AI API priced ~75% below OpenAI/Anthropic** frontier models — a potential enterprise-adoption / new-revenue lever. Both constructive (capex + product/pricing) on the one held name.
  - gap_type: event_catalyst (capex + product/pricing)
  - responder: NONE — library gap (META claimed by `equity_momentum_macd_histogram` (trending); no capex or product/pricing responder — position rides its MACD exit)
- **JPM: Q2 earnings BMO tomorrow (Tue 7/14)** — bank-season opener, reporting simultaneously with GS/BAC/C/WFC; ~$5.59 EPS / ~$51.09B rev est, implied move ~4.4%; NIM the key metric; $50B buyback effective 7/1 (carry). Same morning as June CPI + Warsh.
  - gap_type: earnings_window
  - responder: NONE — library gap (JPM claimed by `equity_trend_following_ema_cross`, NOT `equity_event_driven_catalyst`/`long_straddle_earnings` — earnings-window assignment gap; MOST URGENT, window opens tomorrow)
- **TSM: June revenue +67.9% YoY** (AI-infrastructure demand signal — a monthly disclosure); **Q2 report this week** (large options-implied move).
  - gap_type: earnings_window (+ event_catalyst for the revenue print)
  - responder: NONE — library gap (TSM claimed by `equity_trend_following_ema_cross`; earnings-window assignment gap)
- **TSLA: closing the Model S/X production line at Fremont to repurpose the facility for Optimus humanoid-robot production** (product/manufacturing pivot, per AI chief Ashok Elluswamy). Q2 earnings 7/22.
  - gap_type: event_catalyst (product/manufacturing) + earnings_window (7/22)
  - responder: NONE — library gap (TSLA claimed by `equity_trend_following_ema_cross`; no product/manufacturing responder; earnings-window assignment gap)
- **MU: epicenter of the memory/DRAM cohort selloff** — Samsung's record-but-"only"-19× profit guidance sparked AI-memory profit-taking (DRAM ETF ~-30%/month); **+ Trump touted Micron in a fresh $6.9B US-manufacturing/reshoring commitment** (adds to the $250B capex plan, carry).
  - gap_type: event_catalyst (sector/cohort selloff + sentiment reversal; policy/capex)
  - responder: NONE — library gap (MU claimed by `equity_event_driven_catalyst`, which models discrete single-name catalysts, NOT a cohort de-rate / forced-flow rotation; MU lot already exited 7/9. No cohort-selloff or capex/reshoring responder)
- **SKHY (universe, `equity_watch_only`, provisional/quarantined): caught in the memory selloff** — SK Hynix -15.4% Seoul; "SK Hynix vs. Micron: AI-memory battle just got real." Now quoting regular-way on Alpaca.
  - gap_type: event_catalyst (cohort selloff)
  - responder: NONE — library gap (SKHY on `equity_watch_only` — never trades; research owns validation by 7/24)
- **AAPL: Epic v. Apple App Store-fee battle enters a new phase** (fight over Apple delaying the court process); the **Apple v. OpenAI trade-secret suit** (filed 7/10) still trending. Litigation track.
  - gap_type: event_catalyst (litigation)
  - responder: NONE — library gap (AAPL claimed by `equity_trend_following_ema_cross`; no litigation responder)
- **BE: Bloom Energy still "in the spotlight" after a week of short-seller (Hunterbrook) reports + analyst commentary** — thesis contested, unresolved. (Watched carry.)
  - gap_type: event_catalyst (activist short / controversy)
  - responder: NONE — library gap (BE claimed by `equity_breakout_volume_confirmation`; no short-report responder)
- **SPCX (PROVISIONAL / execution-quarantined): IPO-aftermath selloff** — new 52-week lows, ~-35% from its record one month post-IPO; **George Noble warns of a "900% float explosion" as lockups expire** (float/forced-flow mechanics); Musk touts orbital data centers (Chanos skeptical). No hard corporate catalyst.
  - gap_type: event_catalyst — lockup-expiry / float-increase / forced-flow → **NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)**
  - responder: NONE — library gap (SPCX's trend-following claim is provisional/quarantined; no rule reads float/lockup/forced-flow mechanics)

**No fresh single-name news** (price/analyst/cohort only — nothing that *happened*): **NVDA** (Q2 outlook + Meta/xAI "reinforce NVDA moat" opinion + quantum showcase Tue — cohort/context), **SNDK** (-5% memory-cohort sympathy; no SNDK event), **MSFT** (Nadella AI-ownership commentary — opinion), **AMZN** (cohort; Q2 earnings 7/30 carry), **GOOGL** (Meta cross-tags; Fri export-control story is a carry), **AVGO** (in the "$430B FCF" cohort piece; lot exited 7/9), **ORCL** (near 52-wk lows — price), **INTC** (-3%, earnings 7/23 — price/calendar), **ARM** (price + earnings 7/23), **MRVL** (-6% on chips→energy rotation — price/rotation, no corporate event), **CSCO** (president's AI-jobs op-ed), **WULF** (only an IT whale-alert scan; now on validated `equity_rsi_divergence`), **DELL / QCOM / SYNA / SMCI / HPE / NUVL / CBRS / IRDM / RKLB** (0 or price-only items; RKLB support-test technical), **QQQ / SPY** (index/geopolitics — trader has bars).

## Sector themes

- **AI-memory de-rate — the day's dominant structural event.** Samsung's record Q2 (~$58.4B op profit, ≈19× YoY) *disappointed* on sustainability fears and touched off a broad AI-memory selloff: MU, SNDK, SKHY, WDC all down mid-single-digits, the DRAM ETF ~-30% in under a month. The "AI-proximity winners vs pressured memory" split from Friday has flipped into a **full-cohort risk-off** — the market is now questioning whether the AI-memory supercycle's *pace* is priced too richly. Not price action alone: a concrete guidance event (Samsung) is the trigger.
- **Energy shock + chips→energy rotation.** The US-Iran Strait-of-Hormuz strikes pushed oil +~5%; energy shares rose ~2.1% while tech fell ~1.2%, and Wall Street was described as rotating out of high-flying chip names (MRVL -6%) into energy/defensives. A real macro-driven sector rotation.
- **AI-datacenter capex intact despite the memory wobble.** Meta expanded Hyperion to $50B+; NVDA/MU/AVGO/AMAT framed as set to generate ~$430B combined FCF even as hyperscalers "bleed cash" on AI infra. The buildout thesis is unbroken even as memory *pricing/valuation* repriced.
- **Financials into bank-earnings kickoff.** Five big banks (JPM/GS/BAC/C/WFC) report BMO 7/14; the sector narrative is shifting from rate-sensitivity to trading/IB/IPO-activity/commercial-lending growth engines. JPM is our only financials name.
- **Vol regime firming.** VIX 17.16 (+14%), off Friday's benign ~15.84, on the geopolitical + memory-selloff combination. Still MID-band/orderly; event-IV building into CPI + bank earnings + TSM.

## Candidates for the universe

**PROMOTED today (universe 32 → 33):**
- **RIVN (Rivian, consumer_discretionary)** — Tier-0 news-subject: launched a **discounted 75-million-share public offering** (dilutive capital raise), its own coverage line ("Why Is Rivian Falling Monday?" with the offering as the attributed catalyst). US-tradable (NASDAQ), EV peer to TSLA. Lands unclaimed → trader triage (watch-grade expected).

**Tracking (NOT promoted — foreign, cohort-sympathy, or no clean US-tradable single-name catalyst):**
- **Bank peers GS / BAC / C / WFC** — all report Q2 BMO tomorrow with JPM; **financials is under-represented in the universe (only JPM).** Worth the operator considering one bank peer for breadth. (Cohort earnings preview, so not auto-promoted today.)
- **WDC (Western Digital)** — memory-cohort sympathy in today's selloff; no WDC-specific event (recurring memory-cohort track).
- **Samsung (SSNLF)** — record Q2 but Seoul-listed / thin US ADR; not cleanly US-tradable. Track (recurring memory cohort).
- **NBIS (Nebius)** — fell on Meta-competition + AI-valuation anxiety; AI-neocloud/datacenter name (recurring AI-infra mention). Track.

## Macro / sector context

- **No US macro print today (Mon 7/13). The week's pivot is Tue 7/14:** June CPI (8:30 AM; consensus headline ~3.8% YoY down from 4.2%, core ~2.8%, monthly ~-0.2% — energy-led, *pre* today's oil spike) lands ~90 min before **Warsh's first semi-annual testimony** (House Tue, Senate Wed). Last inflation read before the **7/28-29 FOMC**. June PPI + Empire State Wed 7/15; retail sales Thu. Fed funds 3.50-3.75%; June minutes (7/8) read hawkish. Framing: soft CPI + patient Warsh keeps the AI/Mag7 bid; hot CPI + hawkish Warsh risks a rate-scare reversal.
- **Geopolitics (fresh, material):** the US and Iran exchanged airstrikes contesting the **Strait of Hormuz** (triggered by an Iranian attack on a container ship over the weekend). Oil +~5% to multi-week highs; Asian equities fell (SK Hynix -15.4%, Samsung -10.7% Seoul); US futures contained (S&P -0.3%, Nasdaq -0.8%). Fluid and oil-sensitive — a caution flag, not a halt trigger.
- **Policy:** Trump touted Toyota/Micron/GM committing a further **$6.9B to US manufacturing** (reshoring, MU-aligned). Meta's EU DSA "addictive features" preliminary finding (up to 6% of revenue) remains open from Friday; no fresh escalation today.
- **Vol:** VIX 17.16 (+2.13 pt / +14%) — risk-off pop, MID band; single-name memory/IPO (SPCX) dispersion elevated well above index vol.

## Library gaps

`gap-registry coverage_holes` is **empty** — every item below is an **activation / assignment / taxonomy** gap (a rule/event-type isn't mapped to the symbol that had the event), not a registry hole. Re-listed for tomorrow's `tasks.md` → Saturday research:

- **Earnings/print-window assignment — JPM (7/14, window OPEN, MOST URGENT), TSM (this week), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** All claimed by trend-following / breakout, not `equity_event_driven_catalyst` / `long_straddle_earnings`. Recurring; the JPM case is now imminent.
- **Sector / cohort selloff + sentiment-reversal — the AI-memory de-rate (Samsung guidance → MU/SKHY/SNDK/WDC).** No rule reads a cohort-wide sentiment reversal or a peer's guidance read-through. *Research: a cohort/sector risk-off overlay (overlaps with liquidity-rotation from prior briefs).*
- **Regulatory / litigation — AAPL (Epic new phase + v. OpenAI); META EU DSA (carry).** No rule reads a lawsuit or agency action. *Research: a regulatory/litigation-event overlay.*
- **Capital-allocation / capex — META Hyperion $50B+, Meta AI-API pricing; MU/Micron $6.9B reshoring (+ $250B carry).** No rule reads a multi-year capex plan or a pricing move. *Research: a capex/capital-allocation overlay.*
- **Index / forced-flow + lockup/float mechanics — SPCX "900% float explosion" (lockup expiry); leveraged single-stock/DRAM ETFs.** Recurring across sessions → argues for a **6th Tier-B trigger** or a forced-flow overlay. `NEW_CATEGORY_NEEDED (index_rebalance / float mechanics)`.
- **Activist-short / controversy — BE Hunterbrook reports (ongoing).** No rule reads a short report or its rebuttal.
- **Geopolitical / energy-shock overlay — US-Iran Strait-of-Hormuz strikes, oil +5%, chips→energy rotation.** No rule reads an oil/geopolitical shock or its cross-sector read-through. *Research: a macro/energy-shock risk overlay.*
- **Vol-regime activation — VIX +14% spike, event-IV into CPI + five bank prints + TSM this week.** Structures exist (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) but aren't activated on an earnings-IV / dispersion screen.
- **New-listing no-history triage — RIVN (just promoted; likely thin/degenerate backtest) and SKHY (still on `equity_watch_only` until bars accrue).** Feeds the recurring fallback-threshold question (does a no-history / 0-trade score route to `equity_watch_only` vs a below-baseline trading provisional?).

## Recommendations for the trader

- **NOTABLE, not gating.** Weight this as a soft signal — nothing here requires deviation from the algorithmic-only mandate. The memory-cohort selloff, the oil/geopolitical shock, and META's constructive capex/pricing news are all informational; positions ride their own rules.
- **RIVN triage (new):** run `triage-symbol RIVN --gap-type event_catalyst`. Expect a limited-history / degenerate-backtest outcome → watch/provisional grade. Don't force a trading claim. **SKHY:** already claimed (`equity_watch_only`, quarantined, revalidate 7/24) — do NOT re-triage; it's just caught in the memory selloff.
- **Held name META:** the day's events were *positive* (Hyperion $50B capex, AI-API price cut). It's noted overbought/near resistance and is in the broad tech risk-off, but there's no adverse catalyst — no basis to override its MACD rule. Soft note only.
- **Provisionals unchanged:** QCOM/SPCX/SYNA stay quarantined (`revalidate_by 7/21`); SKHY (`7/24`). SPCX's lockup/float-mechanics warning does not change its quarantine.
- **Digest the 7/14 stack** — June CPI (~3.8%/2.8% consensus) + Warsh testimony + five big-bank prints (JPM most relevant, implied move ~4.4%) all tomorrow BMO, plus TSM this week. Rate/vol-sensitive and event-heavy; none makes *today* halt-worthy, but tomorrow is the risk-dense session.
- **Watch the geopolitical tail.** The US-Iran Strait-of-Hormuz exchange is live and oil-sensitive; if it escalates and gaps equity futures >2% overnight, that would be the halt-worthy line — it is not there today (Nasdaq futures -0.8%).
- **Standard workflow otherwise.** The event cluster is real but the market reaction is orderly (VIX 17, futures <1% down) — don't manufacture action from it.
