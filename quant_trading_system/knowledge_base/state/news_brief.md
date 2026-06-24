# News brief for 2026-06-24 (after-hours / 3:30 PM PT)

## Headline assessment

**NOTABLE.** This is the post-close 3:30 PM PT run, leading the 4:00 PM PT trader run.
**The marquee event landed: MU's Q3 FY26 print is OUT (AMC) and it is a record
blowout** — revenue $41.46B, non-GAAP EPS **$25.11** vs ~$20.20 est (+24%), and a
**Q4 guide of ~$50.0B ±$1.0B revenue at ~86% gross margin** (EPS ~$31), far above
Street; stock **+12–15% after-hours. MU is a held long.** Two more events on held
names: **AVGO** — Broadcom and OpenAI unveiled **"Jalapeño,"** OpenAI's first custom
inference chip (built by Broadcom), and **GOOGL** was confirmed as the Dow's newest
member (effective Mon 6/29) and launched Gemini 3.5 Flash "Computer Use." Around them,
**the two-day AI/semis de-rating recovered** (risk-on rebound; Russell 2000 at a
record) and **oil fell below $70** on US-Iran de-escalation.

**NOT HALT-WORTHY:** none of the manual's three triggers fire in a way that argues for
skipping execute. (1) No FOMC on the next cash session (the June 17 decision is in
prices). (2) The held-name catalyst that landed overnight — **MU's print — RESOLVED
FAVORABLY** (a blowout beat + raise on a long we already hold). The halt-worthy lever
exists so the trader can *skip execute to avoid trading into an adverse surprise*;
here the binary resolved to the upside, with the result now fully known, so there is
nothing to halt for — the trader should let the event-driven strategy process the
post-print window with full information. (3) The >2% move earlier in the week was a
tech de-rating (realized price the rules already see), now **recovering**, not a
geopolitical shock — today's actual geopolitics (Iran de-escalation, oil < $70) is
risk-positive. **Observe; don't override.** A do-nothing `execute` remains the likely
outcome unless a rule fires on realized price — but **MU's post-print reconciliation
is the one thing the trader must actively check** (trailing stop on a now-deeply-ITM
position; any event-driven window action).

## Watchlist + positions

(Held longs per the 6/23 trader handoff: **AAPL 72, AVGO 26, MU 7, ORCL 38, QQQ 28,
SPY 35**; book equity ~$106.0K. Active set 7 strategies; universe **23, 23/23 claimed,
unclaimed_count == 0**, `provisional_count: 1`. SPCX remains the lone **PROVISIONAL,
execution-quarantined** claim on equity_trend_following_ema_cross — revalidate_by
**2026-07-04**. `gap-registry coverage_holes` confirmed **empty** again this run.)

- **MU — EVENT (Q3 FY26 print OUT; record blowout + big raise; +12–15% AH; held long).**
  Revenue **$41.46B (record)**, non-GAAP EPS **$25.11** vs ~$20.20 (+24%); GAAP net
  income $28.24B. **Q4 FY26 guide ~$50.0B ±$1B revenue, GM ~86%, non-GAAP EPS ~$31** —
  far above Street, driven by sold-out HBM and AI-memory demand. CEO expected to detail
  the Anthropic strategic deal on the call. The pre-print ~14% implied move and PUT
  hedging were overwhelmed by the upside. **Held position (7 @ $982.90, was +8.12% at
  ~$1,063 on 6/23); a +12–15% AH pop puts it sharply further in the money.**
  - gap_type: earnings_window
  - responder: equity_event_driven_catalyst (claims MU — a TRUE responder match). Held,
    so the entry guard skips; the post-print window posture + trailing stop govern.
    **The trader must reconcile any rule-driven exit and confirm the trailing-stop level
    against the post-print mark.** No discretionary action.

- **AVGO — EVENT (custom-silicon win; held long).** Broadcom and OpenAI unveiled
  **"Jalapeño,"** OpenAI's first custom Intelligence Processor, built by Broadcom —
  design-to-tape-out in ~9 months, initial deployment end-2026, ramping 2027–28 at
  gigawatt scale. AVGO shares rose. A material product/partnership win on a held name.
  - gap_type: event_catalyst
  - responder: equity_event_driven_catalyst (claims AVGO) — **but the strategy models
    earnings windows, not product/partnership deals**, so there is no true algorithmic
    handle on *this* event type. Partial gap (claimed, unmodeled; see Library gaps). The
    win reaches the position only as realized price. No action.

- **GOOGL — EVENT (index membership / forced flow + product; price-claimed).** S&P DJI
  confirmed **Alphabet joins the DJIA effective pre-open Mon 6/29** (replacing VZ); DIA
  and Dow-tracking funds rebalance into GOOGL, and the stock rose on the news. Also
  launched **Gemini 3.5 Flash "Computer Use,"** and Reddit may charge Google/OpenAI more
  for training data.
  - gap_type: event_catalyst (index-rebalance/forced-flow + product launch)
  - responder: NONE — library gap. GOOGL is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads an index-rebalance schedule or a product event.

- **ORCL — EVENT (restructuring digestion; held long).** Oracle fell again Wednesday as
  investors digest the **~21,000-job (~13%) workforce cut** tied to AI build-out/
  adoption (cited by Sen. Warren). On track for its worst month since 2001 despite a
  record AI backlog. The book's only red.
  - gap_type: event_catalyst
  - responder: equity_event_driven_catalyst (claims ORCL) — **but models earnings
    windows, not workforce-reduction disclosures**; no true handle on this event type.
    Soft/partial gap. Position held; no rule fired; no action.

- **CBRS — EVENT (debut-print Day-1 follow-through; −8% AH on 6/23, slid further today).**
  After its first public quarter (rev $193.4M +94% beat, FY26 core-rev guide $855–865M,
  OpenAI 750MW/$20B + AWS deals, −8% AH on a gross-margin guide-down), shares fell again
  Wednesday. Needham reiterated Buy; analysts raised forecasts. CEO: data-center
  capacity, not chips/demand, is the AI bottleneck.
  - gap_type: earnings_window
  - responder: NONE — library gap (assignment). CBRS is claimed by
    equity_trend_following_ema_cross (price-driven); the earnings-window responder
    (equity_event_driven_catalyst) does NOT claim CBRS. The move reaches trend-following
    only as realized price.

- **TSLA — EVENT (partnership + regulatory overhang; price-claimed).** Tesla, Sunrun and
  Renew Home announced a **16-GW clean-energy pact** (home batteries/solar/smart devices)
  to power AI data centers + utilities. NHTSA FSD probe (fatal Texas crash) carries
  forward.
  - gap_type: event_catalyst
  - responder: NONE — library gap. TSLA is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads a partnership/regulatory event.

- **AMZN — EVENT (partnership; price-claimed).** **Nokia expanded its AWS collaboration**
  to run its Autonomous Networks Fabric on AWS (Level-4 autonomy). Separately, JPM's
  Cembalest called Anthropic's Amazon-Trainium pact the "strongest third-party"
  endorsement of non-NVDA AI silicon (read-through positive for AWS custom chips).
  - gap_type: event_catalyst
  - responder: NONE — library gap. AMZN is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads a cloud-partnership event.

- **META — EVENT (policy; price-claimed).** The Trump administration is reportedly
  pressing Meta to submit frontier AI models for voluntary federal testing. Low
  fundamental weight; logged for completeness.
  - gap_type: event_catalyst
  - responder: NONE — library gap. META is claimed by equity_momentum_macd_histogram
    (price-driven); no active rule reads a policy event.

- **No fresh single-name news** (tape / theme / screen mentions only): **AAPL, ARM,
  CSCO, DELL, HPE, INTC, JPM, MRVL, NVDA, NUVL, QQQ, SPY, TSM.** INTC rose ~3% on a
  technical signal (+ a month-old Pelosi call-option disclosure) — flow/price, no fresh
  corporate catalyst; foundry-turnaround thread carries. NVDA traded on the
  Trainium/SK-Hynix narrative (analyst framing, not an NVDA event). CSCO/DELL/HPE had 0–1
  items.

- **SPCX — EVENT (capital allocation; PROVISIONAL / execution-quarantined).** SpaceX
  **raised $25B in unsecured notes** weeks after its $86B IPO; a "battleground" stock
  with analysts split on valuation. Carry: $6.3B Reflection deal, Cathie Wood buying,
  Nasdaq-100 add ~July 1.
  - gap_type: volatility_regime (hyper-IV new listing; no price/earnings history)
  - responder: equity_trend_following_ema_cross (PROVISIONAL/UNVALIDATED,
    execution-quarantined; Saturday research revalidates by 2026-07-04). Will NOT trade.

## Sector themes

- **AI-memory supercycle validated by MU's print.** Record revenue + a ~86% gross-margin
  Q4 guide reaffirmed the HBM/DRAM cycle; the read rippled to **SanDisk (SNDK), Western
  Digital (WDC), Seagate (STX)** in sympathy. Counter-signal: **SK Hynix targeting a
  ~$29.4B Nasdaq ADR listing** — incremental supply and a competing memory pure-play.
- **Custom-silicon arms race accelerates.** Two fresh data points that hyperscalers and
  model labs are diversifying off merchant GPUs: **OpenAI/Broadcom "Jalapeño"** (AVGO
  beneficiary) and **Anthropic/AWS Trainium** (framed as the strongest GPU-alternative
  endorsement yet). An AVGO/AMZN tailwind and a standing NVDA-moat question.
- **AI-capex / FCF debate.** Chamath argued hyperscaler free-cash-flow declines
  (GOOGL/META/MSFT) are moat-building, not cash burn — a counter to the "crowded-trade"
  de-rating narrative that drove Mon–Tue.
- **Energy / macro: oil below $70 on Iran de-escalation.** A 60-day roadmap to a US-Iran
  deal + Hormuz reopening pushed crude ~40% off its wartime peak — disinflationary;
  cruise lines/transports rallied. Risk-positive.
- **Rotation / vol:** risk-on rebound from the two-day chip de-rating; Russell 2000 at a
  record; **VIX crossed above 18 (~19.5) during the de-rating** — the first >3pt move in
  this run, though it likely eased on Wednesday's bounce.

## Candidates for the universe

**0 promotions this run. Universe stays at 23.** No automated trigger fired.

- **Tier A (3-session recurrence):** **SNDK (SanDisk)** recurs again — it rallied in
  sympathy with MU's blowout (memory/NAND supercycle, "next AI trade") — but as a
  *theme / coattail move*, not a confirmed single-name catalyst, and its
  3-consecutive-session chain is **still being rebuilt** after the skipped Monday 6/22
  (this is ~session 2 of the rebuild, not yet 3). **CRDO (Credo)** recurs thematically
  (AI interconnect). Neither advances.
- **Tier B (single-event triggers, 5 categories, 2/day cap):**
  - **#1 M&A target:** none tradeable/new.
  - **#2 FDA binary:** none (TG Therapeutics had a clinical-update move, not an
    approval/rejection).
  - **#3 beat + raise + +5%:** **no qualifying NEW symbol.** KB Home beat (+16%) but is a
    homebuilder off-character for this tech universe and the raise wasn't confirmed; PAYX
    beat without a confirmed +5%/raise. MU and CBRS are already in-universe.
  - **#4 sell-side initiation cluster (3+ banks/week):** none.
  - **#5 Tier-1 customer win:** the OpenAI/Broadcom "Jalapeño" win is on **AVGO, already
    in-universe**; SK Hynix is not yet listed. No NEW symbol qualifies.
- **Watches for the operator / Saturday research (NOT promoted):** **SNDK** (strongest
  recurring; promote on a confirmed own beat+raise+5% or a named contract — not on MU
  coattails), **CRDO** (AI interconnect), **WDC / STX** (memory cohort, rode MU today —
  flow/sympathy, not own catalysts), and the standing **WOLF / SMCI / QCOM**
  flow-recurrence names (flow does not refresh the catalyst clock).

## Macro / sector context

- **MU's blowout is the day's dominant macro signal for the AI cohort** — a hard
  fundamental data point (record rev, ~86% GM guide) that cuts against the
  "most-crowded-trade unwind" thesis of Mon–Tue. Memory demand is intact.
- **Fed bank stress-test results released Wednesday; June 17 FOMC in prices.** No FOMC
  this session; higher-for-longer with a hike-biased dot-plot (first meeting under Chair
  Warsh) is the standing rate backdrop for the rate-sensitive AI cohort. Citadel's
  Sept-hike call aligns with the dots.
- **Oil < $70 (toward $72), lowest since late February**, on Strait-of-Hormuz reopening +
  a 60-day US-Iran roadmap; the US waiver for Iranian crude is in force. Disinflationary,
  risk-positive — not a shock.
- **GOOGL → DJIA effective 6/29** (replacing VZ) — scheduled index-membership change /
  forced flow.
- **VIX ~19.5** — crossed above 18 on the de-rating (up from ~17.3 a week ago), the first
  >3pt move in this run; likely eased on Wednesday's rebound. No confirmed term-structure
  inversion.

## Library gaps

Every `responder: NONE` (or partial) item above, re-listed for the trader's tasks.md →
Saturday research. `gap-registry coverage_holes` is **empty**; these are
**activation/assignment** gaps (responder exists but isn't active / claims no universe
symbol) plus **taxonomy** gaps (NEW_CATEGORY_NEEDED).

- **Earnings-window assignment on CBRS — realized, now Day-1 follow-through.** CBRS
  printed 6/23 AMC (−8% AH) and slid again 6/24, with no algorithmic handle: claimed by
  trend-following (price-driven); the earnings-window responder
  (equity_event_driven_catalyst) does NOT claim it. **Suggested research:** head-to-head
  CBRS vs equity_event_driven_catalyst; assign to the event-driven responder.
  gap_type: earnings_window — responder: NONE (assignment).
- **Product/partnership sub-trigger on event-driven covered names — AVGO Jalapeño.**
  AVGO *is* claimed by equity_event_driven_catalyst, but the strategy models earnings
  windows, not product/partnership-deal events, so a material custom-silicon win has no
  handle even on a covered held name (same shape as ORCL restructuring). **Suggested
  research:** decide whether a product/partnership/restructuring sub-trigger belongs in
  the event-driven strategy. gap_type: event_catalyst — responder: partial (claimed,
  unmodeled).
- **Index-rebalance / forced-flow window — TWO live instances.** GOOGL joins the DJIA
  6/29 (forced buy by Dow funds); SPCX → Nasdaq-100 ~July 1; held QQQ. No active rule
  reads a known index-rebalance schedule as a flow event. **Suggested research:** an
  index-rebalance/forced-flow overlay (anticipated add/drop dates + estimated flow) as a
  soft posture signal. NB carry-forward operator Q: should index-inclusion become a 6th
  Tier-B promotion trigger? gap_type: event_catalyst — responder: NONE.
- **Event-window coverage on price-claimed names (GOOGL index/product; TSLA Sunrun pact +
  NHTSA probe; AMZN Nokia/AWS; META federal-testing pressure).** `event_catalyst` is
  declared only by equity_event_driven_catalyst, which claims AVGO/MU/ORCL — not these
  names. Partnership, regulatory, product and policy events on price-claimed large caps
  have no algorithmic responder. **Suggested research:** broaden
  equity_event_driven_catalyst's claim set, or add a lightweight event-window overlay
  that co-claims alongside the price strategy. gap_type: event_catalyst — responder: NONE.
- **Restructuring / workforce-reduction events (ORCL 21k cuts).** Claimed by
  equity_event_driven_catalyst but unmodeled — no handle on this event type even on a
  covered name. gap_type: event_catalyst — responder: partial (claimed, unmodeled).
- **Macro-event window (Fed higher-for-longer / hawkish dots; oil/Iran macro).** No
  canonical gap_type covers a scheduled macro print/regime; no rule lets the trader
  pre-position around FOMC/CPI/jobs (correct under the mandate — but the soft-signal
  handle is missing). **Suggested research:** a `macro_event_window` category.
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **AI-capex financing / crowding overlay — now RECOVERING.** The two-day "most-crowded-
  trade" unwind reversed Wednesday (risk-on rebound; MU blowout reaffirmed demand). The
  crowding/leverage overlay still has no rule, but the acute de-rating has paused.
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation.** Registry hole CLOSED (volatility_regime declared by
  iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings), but none
  are active and none claim a universe symbol — so no active strategy reads the VIX
  regime (now > 18), MU's post-print IV crush, CBRS's first-print vol, or SPCX's hyper-IV.
  **Suggested research:** activate one vol strategy and give it a universe claim (MU
  pre-print was the textbook long-straddle setup; post-print IV crush is the iron-condor/
  short-vol setup). gap_type: volatility_regime — responder: NONE (active); activation
  pending.
- **M&A-arb (NUVL/GSK).** `pairs_arbitrage` declared by
  equity_pairs_trading_cointegration (not active); NUVL claimed by trend-following
  (price-driven). Activation gap re-affirmed. gap_type: pairs_arbitrage — responder:
  NONE (active).

## Recommendations for the trader

- **NOTABLE, not halt-worthy — standard workflow; let rules ride.** No HALT-WORTHY
  trigger argues for skipping execute: no FOMC on the next session; the held-name
  catalyst that landed (MU) **resolved FAVORABLY** (a blowout beat+raise on a long), so
  there's nothing to halt for; the >2% move earlier in the week is recovering price
  action, not a geopolitical shock. **Observe, don't override** — discretionary hedges
  and discretionary profit-taking are both forbidden by the algorithmic-only mandate.
- **MU (held) is THE reconciliation item.** The print is OUT and it's a record blowout
  (+12–15% AH); the position is now sharply further in the money on top of a +8% base.
  **Let equity_event_driven_catalyst's post-print window logic + the trailing stop
  govern, and reconcile any rule-driven exit against the post-print mark.** Do not act
  discretionarily on the good news — but DO confirm the trailing-stop level updated and
  log any rule-driven trim/exit at the next `execute`.
- **AVGO (held) — Jalapeño is a tailwind with no algorithmic handle.** The OpenAI/
  Broadcom custom-silicon win reaches the position only as realized price; logged as a
  product/partnership library gap (claimed-but-unmodeled). No action.
- **ORCL (held) — 21k job cuts is a cost event, not a position action.** Held by the
  event-driven strategy; the restructuring disclosure is a soft/partial library gap, not
  a trade trigger. Book's only red; no rule fired.
- **The AI/semis de-rating recovered — react to realized price, not the narrative.** If a
  rule fires on a name (e.g., MU's gap-up reaching a trend/momentum rule, or a trailing
  stop), execute; if none fires, the do-nothing is the correct, non-curve-fit outcome.
- **SPCX stays execution-quarantined.** The $25B notes raise + Nasdaq-100 add (~July 1)
  are research signal, not a trader action; validation owned by Saturday research
  (revalidate_by 2026-07-04).
- **`cli execute` should run as scheduled.** Standard post-close run; the
  algorithmic-only mandate governs. The one active task is the MU post-print
  reconciliation above.
