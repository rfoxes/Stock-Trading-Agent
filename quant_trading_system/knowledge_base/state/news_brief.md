# News brief for 2026-06-30 (post-close / 3:30 PM PT)

## Headline assessment

**NORMAL FLOW.** Post-close 3:30 PM PT run, leading the 4:00 PM PT trader run, on quarter-end
(the best quarter for the S&P 500 and Nasdaq in six years). **The day's tape was an AI-chip
*recovery* — semis bounced, the Nasdaq firmed, VIX eased to 17.65 — but that is price action the
trader already sees, not the news.** The genuine *new* events were a cluster of **legal/regulatory
items on held names**: a **US DRAM price-fixing class action naming Micron** (MU, held), the
**Supreme Court agreeing to hear Apple's Epic App-Store appeal** (AAPL, held), and **Australia's
ACCC suing Amazon** over Prime Video ads — plus an **AWS ~20% GPU price hike effective July 1**
(AMZN revenue tailwind), **Alphabet's now-live Dow membership** (GOOGL, effective 6/29), and a
**Palantir–Nvidia sovereign-AI deal** (NVDA). None changes the algorithmic picture on a held name;
the two held-name legal items are slow-moving civil/appellate processes, not guidance surprises.

**NOT HALT-WORTHY:** none of the manual's three triggers fire. (1) No FOMC on the next cash session
(June 17 hold 3.50–3.75% is in prices; no scheduled US print today — ADP is tomorrow 7/1, nonfarm
payrolls Thu 7/2). (2) No held-name confirmed overnight catalyst with a >5σ guidance change — the
MU antitrust suit is early-stage litigation, not an earnings/guidance event. (3) Geopolitics is
risk-positive (US-Iran framework holding; best quarter in six years "despite the Iran war"). **Observe;
let rules ride.**

## Watchlist + positions

(Held longs per the 2026-06-29 trader handoff: **AVGO 26, MU 7, ORCL 38, QQQ 28** — SPY was sold
6/29 (+3.95%, reconciled). Active set **8** strategies. **Universe 26**, **claimed 26**, **unclaimed
0**. Three **PROVISIONAL / execution-quarantined** claims: **SPCX** (trend-following, revalidate_by
**2026-07-04**), **QCOM** (event-driven, revalidate_by **2026-07-10**), **SYNA** (pairs-cointegration,
revalidate_by **2026-07-10**). `gap-registry coverage_holes` confirmed **empty** again this run.
**No promotions today — universe stays 26.**)

- **MU — EVENT (legal / antitrust; held long, provisionally claimed).** Micron, Samsung and SK Hynix
  were named in a **US DRAM price-fixing class action** (N.D. Cal., 17 plaintiffs, filed 6/25, surfaced
  6/29–30): the suit alleges the ~90%-share memory trio used the HBM transition as cover to curtail
  DDR3/DDR4 output and inflate DRAM prices (+~700% over four years). Allegations are unproven; defendants
  have not responded. A new legal overhang, but early civil litigation — not a guidance event. Post-print
  IV crush also continuing (short-vol micro-setup).
  - gap_type: event_catalyst
  - responder: NONE — library gap. MU is claimed (PROVISIONAL) by equity_event_driven_catalyst, which
    models earnings windows, not litigation; held → entry guard skips; post-print window + trailing stop
    govern. No active rule reads an antitrust/litigation event. Realized price only.

- **AAPL — EVENT (regulatory / Supreme Court; held long).** The **US Supreme Court granted cert** on
  Apple's appeal of the 2025 Epic App-Store contempt finding (the 27% external-link fee). Oral arguments
  ~October; ruling not due until ~June 2027 — distant, but real optionality on the App-Store fee model.
  - gap_type: event_catalyst
  - responder: NONE — library gap. AAPL is claimed by equity_trend_following_ema_cross (price-driven);
    no active rule reads a regulatory/appellate event. (Note: Friday's EMA-cross full exit on AAPL filled
    +1.37% and was reconciled 6/27 — AAPL is no longer a held long per the 6/29 handoff's position set;
    treat the SCOTUS item as universe-level news.)

- **AMZN — EVENT (pricing power + regulatory; universe, price-claimed).** **AWS raised GPU/ML
  capacity-block prices ~20%, effective July 1** (3rd straight quarter of hikes after a 15% Jan move);
  BofA estimates +1–2pp to H2 AWS growth, citing OpenAI/Anthropic commitments — a revenue-tailwind /
  pricing-power event (the *supplier* side of the AI cost wave). Separately, **Australia's ACCC sued
  Amazon** over Prime Video ad bundling.
  - gap_type: event_catalyst
  - responder: NONE — library gap. AMZN is claimed by equity_trend_following_ema_cross (price-driven);
    no rule reads a pricing/capital-allocation or regulatory disclosure.

- **GOOGL — EVENT (index inclusion now live; universe, price-claimed).** Alphabet's **DJIA membership is
  effective** (replaced Verizon 6/29; the Dow closed above 52,000 on the debut). The forced-flow event is
  now complete — the buy-in is in the tape.
  - gap_type: event_catalyst
  - responder: NONE — library gap. GOOGL is claimed by equity_trend_following_ema_cross; no rule reads an
    index-rebalance schedule. Now realized price only (event consummated).

- **NVDA — EVENT (partnership; universe, price-claimed).** Palantir struck a **sovereign-AI pact with
  Nvidia for US agencies** (plus a Surf Air commercial deal on PLTR's side). Real partnership news. (Also:
  Taiwan authorities raided Super Micro over an alleged $2.5B Nvidia chip-smuggling scheme — SMCI is
  outside the universe; enforcement item, not an NVDA action.)
  - gap_type: event_catalyst
  - responder: NONE — library gap. NVDA is claimed by equity_trend_following_ema_cross (price-driven);
    no rule reads a partnership/customer-win disclosure.

- **SPCX — EVENT (index inclusion scheduled; PROVISIONAL / execution-quarantined).** SpaceX **joins the
  Nasdaq-100 before the open Tue July 7** (fast-track, ~$4.3B forced passive buying) — **corrected date:
  July 7, not the ~July 1 carried in prior notes.** Elevated single-name IV into the add. SPCX also drew
  Trump-Accounts-donation and capital-raise headlines.
  - gap_type: volatility_regime
  - responder: equity_trend_following_ema_cross (PROVISIONAL/UNVALIDATED, execution-quarantined; revalidate_by
    2026-07-04). **Will NOT trade.**

- **MU / AVGO / ORCL / QQQ (held) — reconcile, don't act.** MU: legal overhang above, no rule-driven action
  beyond post-print window / trailing stop. **AVGO** — no fresh single-name catalyst (semis bounced; Jefferies
  Buy reiteration is opinion). **ORCL** — no fresh event (21k-cut restructuring still weighs, no responder).
  **QQQ** — index; held, EMA cross has not flipped (watch for a death-cross exit like SPY's; if it fires, let it).

- **No fresh single-name news** (tape / theme / opinion / flow only): **MSFT** (no real corporate event —
  the Buffett/Gates-Foundation story is not MSFT-specific), **META** (AI-scam report + Kalshi/Polymarket
  takeover-risk mentions — not a META event), **JPM** (capital-return-reset digestion after record highs;
  crypto-framework commentary — no new action; $50B buyback effective 7/1 is the carry), **DELL** (only
  peripheral Trump-Accounts mentions; reincorporation already done), **TSLA** (Robotaxi/Waymo competitive
  chatter, X Money app details — no hard event), **INTC** (Cantor PT bump + ongoing nationalization
  overhang — opinion/carry), **TSM / ARM / MRVL** (PT raises + sector-rally commentary — opinion),
  **SNDK** (Bernstein PT-to-$3,000 boost — opinion, but a notable memory-cohort signal), **QCOM, SYNA,
  CBRS, CSCO, HPE, NUVL** (0 Alpaca items, no catalyst), **QQQ, SPY** (index).

## Sector themes

- **AI-memory supercycle — now with a legal overhang.** The DRAM price-fixing class action (MU/Samsung/SK
  Hynix, ~90% share) is the first litigation aimed squarely at the memory re-rating; it alleges the HBM
  transition was cover to curtail DDR3/DDR4 and inflate prices (+~700% / 4 yrs). Unproven and slow, but it
  puts a regulatory tail on the cohort's pricing power. SK Hynix's $29B Nasdaq listing still tracks for ~7/10.
- **AI cloud pricing power: AWS GPU prices +~20% (eff 7/1), third straight quarterly hike.** Amazon is leaning
  into AI demand with pricing discipline (BofA: +1–2pp to H2 AWS growth). A real margin/revenue event in cloud
  — the supplier-side mirror of the device-maker cost pass-through (AAPL/MSFT) theme.
- **Semiconductor / AI-interconnect strength broadening.** Chip-equipment (AMAT +~10%, KLA +~12%) and
  AI-interconnect names (Astera Labs +~16%, Credo) led the turnaround; the AI-infrastructure trade is
  widening past GPUs into memory, optical, packaging and cooling (thematic, mostly price/flow).
- **Index-rebalance / forced-flow cluster.** GOOGL→DJIA now live (6/29); FTSE Russell 2026 reconstitution
  effective end-June (CRDO into Russell 1000, SPCX into Russell 1000/Top 200); SPCX→Nasdaq-100 Tue 7/7;
  SK Hynix Nasdaq listing ~7/10. Mechanical buying, not a fundamental catalyst.
- **Bank capital returns.** JPMorgan's post-stress-test $50B buyback + dividend takes effect July 1; financials
  remain a relative-strength pocket after the record-high reset.

## Candidates for the universe

**No promotions this run. Universe stays 26.**

- **Watch (NOT promoted):**
  - **CRDO (Credo)** — AI-interconnect; extended its run on a Russell 1000 reclassification + a lingering
    multi-bank PT cluster (Evercore initiation $325; Needham/Roth/BofA/Jefferies/Mizuho/Susquehanna/JPM PT
    raises). **Recurrence: session ~2–3 as a thematic carry.** The PT cluster timing is the prior two weeks
    (around its early-June print), and today's move is sector-rally + reiterated upgrades — *opinion-driven,
    not a fresh single-event catalyst today*, so no clean Tier-B trigger. Holding to avoid promoting on PT
    noise; if a *fresh* same-week 3-bank initiation cluster or an own beat-and-raise lands, it qualifies.
  - **SK Hynix** — $29B Nasdaq listing ~7/10; no US-traded ticker yet → track for a post-listing add.
  - **WDC / STX** — memory cohort, sympathy/flow only (no own catalyst); flow does not refresh the clock.
  - **AMAT / KLA / Astera Labs (ALAB)** — chip-equipment / AI-interconnect strength today on the turnaround;
    price/flow, no single-event catalyst. Logged for the operator's awareness, not promotable.
  - **CMCSA (Comcast)** — announced a split into two public companies (media vs tech, ~1 yr). A real corporate
    event but a spinoff, not one of the five Tier-B triggers (and not a target acquisition); operator note only.

## Macro / sector context

- **No FOMC this session; no scheduled US macro print today.** **ADP (June) releases Wed 7/1, 8:15 AM ET;
  the June Employment Situation / nonfarm payrolls releases Thu 7/2, 8:30 AM ET** (pulled a day early ahead
  of July 4). First labor reads into the Warsh higher-for-longer framework (June 17 hold 3.50–3.75%, hawkish
  SEP). May core PCE 3.4% (6/25) remains the freshest inflation print.
- **Quarter-end (6/30): best quarter for the S&P 500 and Nasdaq in six years; Dow's best since 2022.** Brings
  index-rebalance flow (above). Mechanical.
- **Geopolitics risk-positive.** US-Iran framework holding; Hormuz flows uninterrupted; oil soft. No new shock.
- **VIX 17.65 (–~1.2 vs Friday's 18.89).** Sub-3-point move; normal contango, no inversion. Index vol benign;
  dispersion single-name (MU post-print IV crush; SPCX hyper-IV into the 7/7 add). IV-rank below the >50
  vol-selling threshold at the index level.

## Library gaps

Every `responder: NONE` (or partial) item above, re-listed for the trader's tasks.md → Saturday research.
`gap-registry coverage_holes` is **empty**; these are **activation/assignment/taxonomy** gaps (a responder
exists but isn't active / claims no universe symbol, or no canonical gap_type fits).

- **Litigation / antitrust event on a held name — NEW, live instance MU (DRAM class action).** No active rule
  reads a lawsuit/antitrust filing; MU's event-driven claim models earnings windows only (and is provisional).
  **Suggested research:** whether a litigation/regulatory sub-trigger belongs in an event-window overlay.
  gap_type: event_catalyst — responder: NONE.
- **Regulatory / appellate event on a held/universe name — AAPL (SCOTUS cert, Epic) + AMZN (ACCC suit).**
  Price-claimed; no rule reads a court/agency action. **Suggested research:** event-window overlay covering
  regulatory catalysts on large-caps. gap_type: event_catalyst — responder: NONE.
- **Cloud-pricing / capital-allocation event — AMZN (AWS +20% GPU pricing).** A margin/revenue disclosure with
  no responder; AMZN is price-claimed. **Suggested research:** a pricing-power / capital-allocation sub-trigger.
  gap_type: event_catalyst — responder: NONE.
- **Partnership / customer-win event — NVDA (Palantir sovereign-AI deal).** No rule reads a named partnership;
  NVDA is price-claimed. Same hole as the AVGO Jalapeño/OpenAI carry. gap_type: event_catalyst — responder: NONE.
- **Index-rebalance / forced-flow window — recurring cluster.** GOOGL→DJIA (now live), SPCX→Nasdaq-100 (7/7),
  SK Hynix (~7/10), FTSE Russell reconstitution (end-June); held QQQ/SPY exposed to quarter-end rebalance. No
  rule reads an index-rebalance schedule. **Suggested research:** an index-rebalance/forced-flow overlay (and
  the standing operator Q: index-inclusion as a 6th Tier-B trigger). gap_type: event_catalyst — responder: NONE.
- **M&A-arb activation — live instance SYNA (onsemi target, carry).** equity_pairs_trading_cointegration
  declares pairs_arbitrage but is not active beyond the provisional SYNA claim; long SYNA / short ON at 1.350 is
  the textbook setup. Pairs with the NUVL/GSK carry. gap_type: pairs_arbitrage — responder: NONE (active).
- **Management/succession + capital-allocation events — JPM (carry: $50B buyback eff 7/1).** No rule reads a
  buyback/dividend or succession event. gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction events — ORCL (21k cuts, carry).** Claimed by event-driven but unmodeled.
  gap_type: event_catalyst — responder: partial.
- **Earnings-window assignment on CBRS (carry).** CBRS is claimed by trend-following (price-driven); the
  earnings-window responder (equity_event_driven_catalyst) does not claim it. gap_type: earnings_window —
  responder: NONE (assignment).
- **Macro-event window (jobs week 7/1–7/2; higher-for-longer).** No canonical gap_type covers a scheduled macro
  print/regime; no rule lets the trader pre-position (correct under the mandate, but the soft-signal handle is
  missing). gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation (MU post-print IV crush = short-vol setup, carry).** volatility_regime is declared
  (iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings) but none are active / claim a
  universe symbol. MU post-print is the textbook iron-condor setup. gap_type: volatility_regime — responder:
  NONE (active); activation pending.

## Recommendations for the trader

- **NORMAL FLOW, not halt-worthy — standard workflow; let rules ride.** No HALT-WORTHY trigger: no FOMC
  (ADP 7/1, payrolls 7/2 are ahead, not today); no held-name overnight guidance surprise (the MU antitrust
  suit and AAPL SCOTUS cert are slow legal processes); geopolitics risk-positive. **Observe, don't override** —
  discretionary hedges and discretionary profit-taking are both forbidden by the algorithmic-only mandate.
- **P0 triage — `unclaimed_count` should already be 0; no new universe member (no promotions).** Re-confirm
  `cli list-active` shows universe 26 / claimed 26 / unclaimed 0 / provisional 3 (QCOM, SPCX, SYNA). Nothing
  to triage this run unless the count drifts. SPCX revalidate_by 7/04 is the next provisional checkpoint.
- **MU (held) — reconcile, don't act.** New legal overhang but no rule fires on it; post-print IV crush in
  progress. Let equity_event_driven_catalyst's post-print window + the trailing stop govern; log any rule-driven
  trim at execute. No discretionary action on the antitrust headline.
- **QQQ (held) — watch for a follow-on EMA death-cross exit (as SPY fired 6/26).** Trend-following claims both;
  it exited SPY but is holding QQQ (EMA cross has not flipped). If the cross flips and the rule fires, let it.
- **MSFT / AAPL / AMZN / GOOGL / NVDA / JPM / TSLA / INTC — events with no responder; react to realized price
  only.** DRAM-suit read-through, AAPL SCOTUS, AWS pricing + ACCC suit, GOOGL Dow (done), NVDA-Palantir,
  JPM buyback, TSLA competitive chatter, INTC overhang all reach the book only as price; logged as library
  gaps for Saturday.
- **SPCX stays execution-quarantined.** The Nasdaq-100 add (now **Tue 7/7**, corrected) is research signal,
  not a trader action (revalidate_by 2026-07-04).
- **`cli execute` should run as scheduled.** Standard post-close quarter-end run; the algorithmic-only mandate
  governs. No fresh single-name catalyst demands a deviation from the rules.
