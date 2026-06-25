# News brief for 2026-06-25 (post-close / 3:30 PM PT)

## Headline assessment

**NOTABLE.** Post-close 3:30 PM PT run, leading the 4:00 PM PT trader run. **The day's
twist: MU's record-blowout gap-up HELD in the cash session (+15%), but the same memory
shortage that powered MU became a cost shock for hardware makers** — **AAPL fell 6.1%
(the single heaviest weight on the S&P 500) after raising Mac/iPad prices 15–20%** (CEO
Cook: a "Hundred-Year Flood"), and **MSFT fell 3.2%** (52-week low, also raising Xbox
prices), **dragging the Nasdaq down a 4th straight day**. The Dow rose modestly on a
rotation into value (healthcare/financials/industrials; CAT +5.8%, UNH +2.7%). Macro
added a hot **May PCE** (core **3.4%**, highest since Oct 2023; headline 4.1%) reinforcing
higher-for-longer, while **oil extended below $70** (4th down session) on US-Iran
de-escalation. Two universe promotions today: **QCOM** (Investor Day data-center pivot,
Meta anchor customer — Tier-B #5) and **SNDK** (memory supercycle, Tier-A session 3).

**NOT HALT-WORTHY:** none of the manual's three triggers fire. (1) No FOMC on the next
cash session (June 17 decision is in prices; PCE is a scheduled print the tape already
digested — S&P closed flat). (2) The held-name binary that landed overnight — **MU's
print — RESOLVED FAVORABLY** (a blowout beat+raise on a long we already hold); there is
nothing to halt for. **AAPL's −6.1% is realized price on a cost narrative, not an AAPL
guidance cut or a >5σ overnight surprise** — the trend rule already sees the move. (3)
Geopolitics (oil < $70, Iran de-escalation) is risk-positive, no futures dislocation.
**Observe; don't override.** A do-nothing `execute` remains the likely outcome unless a
rule fires on realized price.

## Watchlist + positions

(Held longs per the 6/24 trader handoff: **AAPL 72, AVGO 26, MU 7, ORCL 38, QQQ 28,
SPY 35**; book equity ~$107.2K. Active set 7 strategies. **Universe is now 25** after
today's QCOM + SNDK promotions — **23 of the prior 23 remain claimed; QCOM and SNDK are
UNCLAIMED** and feed the trader's P0 triage / Saturday research. SPCX remains the lone
**PROVISIONAL, execution-quarantined** claim on equity_trend_following_ema_cross
— revalidate_by **2026-07-04**. `gap-registry coverage_holes` confirmed **empty** again
this run.)

- **MU — EVENT (Q3 record blowout; Day-1 cash reaction HELD, +15%; held long).** The
  marquee print reconciled to the upside: rev **$41.46B** (~+346% YoY; vs ~$36B est),
  non-GAAP EPS $25.11, Q4 guide ~$50B; CEO Mehrotra sees the AI-memory shortage with no
  "line of sight" to supply catching up, tight beyond 2027, improving only gradually in
  2028; ~$100B forward customer contracts; FY26 capex $27B with 100% excess-cash return.
  **The gap-up held the full cash session — no give-back, no IV-driven fade.** Held
  position re-rated further into the money (was +22.36% on the 6/24 close).
  - gap_type: earnings_window
  - responder: equity_event_driven_catalyst (claims MU — TRUE responder). Held → entry
    guard skips; the post-print window posture + trailing stop govern. **Reconcile: the
    gap-up held, so the trailing-stop-engages-on-give-back scenario did NOT trigger
    today; confirm the trailing-stop level updated against the post-print mark and log
    any rule-driven trim.** No discretionary action on the good news.

- **AAPL — EVENT (input-cost / margin shock; held long, −6.1%).** Apple **raised Mac and
  iPad prices 15–20%**, confirming AI-driven memory/storage shortages are squeezing
  hardware costs; CEO Cook called the memory-price spike a "Hundred-Year Flood." The
  stock was the **single heaviest weight on the S&P 500** on the day. This is the bear
  side of MU's bull story — the memory supercycle as a device-maker cost headwind.
  - gap_type: event_catalyst
  - responder: NONE — library gap. AAPL is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads an input-cost / margin-compression event. The
    move reaches the held position only as realized price. **(Notable: a held-name event
    that's a NEGATIVE, unlike MU/AVGO — but still no algorithmic handle beyond price.)**

- **AVGO — no fresh single-name catalyst (held long).** Jalapeño/OpenAI custom-silicon
  follow-through has quieted; only thematic/portfolio-tracker mentions today. Carry: the
  product/partnership win remains claimed-but-unmodeled by event-driven (partial gap).
  - gap_type: event_catalyst — responder: equity_event_driven_catalyst (claimed, the
    *prior* event unmodeled; nothing new today). No action.

- **ORCL — EVENT (restructuring digestion continues; held long).** No fresh ORCL-specific
  catalyst; the ~21,000-job cut still weighs and ORCL stays the book's only red.
  - gap_type: event_catalyst
  - responder: equity_event_driven_catalyst (claims ORCL) — models earnings windows, not
    workforce-reduction; soft/partial gap. No rule fired; held; no action.

- **JPM — EVENT (capital allocation; universe, price-claimed).** JPMorgan authorized a
  **$50B buyback (effective Jul 1)** and intends to **raise the dividend to $1.65 (+10%)**
  after clearing the Fed stress test; the stock hit an all-time high.
  - gap_type: event_catalyst
  - responder: NONE — library gap. JPM is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads a buyback/dividend authorization. Realized price
    only.

- **INTC — EVENT (sell-side initiation; universe, price-claimed).** Goldman Sachs
  **initiated coverage at Neutral, $150 PT**, citing server-CPU + foundry tailwinds but
  "balanced" risk/reward (prefers NVDA/AVGO/AMD). The premarket MU-sympathy pop faded to
  a red close.
  - gap_type: event_catalyst
  - responder: NONE — library gap. INTC is claimed by equity_breakout_volume_confirmation
    (price-driven); a single-bank initiation is not a 3-bank cluster and has no responder.

- **CBRS — EVENT (Day-2 follow-through; universe, record two-session loss).** Cerebras
  fell again (~$172 vs $182 prior close), on track for a **record two-session loss** after
  its disappointing annual sales / lower-margin guide (renting back data-center capacity
  in its AI-cloud shift).
  - gap_type: earnings_window
  - responder: NONE — library gap (assignment). CBRS is claimed by
    equity_trend_following_ema_cross (price-driven); the earnings-window responder
    (equity_event_driven_catalyst) does NOT claim CBRS. Realized price only.

- **TSLA — EVENT (regulatory/legal escalation; universe, price-claimed).** The **NTSB
  opened a probe** and the victim's family **filed a wrongful-death lawsuit** over the
  fatal Texas FSD crash, escalating the existing NHTSA overhang. (Optimus-as-memory-
  customer is a thematic read-through, not a TSLA event.)
  - gap_type: event_catalyst
  - responder: NONE — library gap. TSLA is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads a regulatory/legal event.

- **META — EVENT (policy; price-claimed).** Zuckerberg (and Alphabet's Pichai) reportedly
  spared a child-safety Senate hearing as the White House intervened; AI-model-review
  standoff + surging capex in focus. Low fundamental weight.
  - gap_type: event_catalyst
  - responder: NONE — library gap. META is claimed by equity_momentum_macd_histogram
    (price-driven); no active rule reads a policy event.

- **SPCX — EVENT (capital-markets/sentiment; PROVISIONAL / execution-quarantined).** The
  $25B notes raise drew an Allianz "bubble / $70B of funny money" warning and FOMO-trap
  commentary; "SpaceX MSTR" +393% framing. Carry: $6.3B Reflection deal, Nasdaq-100 add
  ~July 1.
  - gap_type: volatility_regime
  - responder: equity_trend_following_ema_cross (PROVISIONAL/UNVALIDATED, execution-
    quarantined; Saturday research revalidates by 2026-07-04). Will NOT trade.

- **No fresh single-name news** (tape / theme / sympathy only): **AMZN** (Nokia/AWS
  read-through, Zoox-vs-Tesla framing), **ARM, CSCO, DELL** (fell Thursday, no catalyst),
  **HPE, MRVL** (memory-cohort sympathy), **MSFT** (52-week low + Xbox price hike — same
  memory-cost theme as AAPL, price-driven), **NVDA** (MU read-through, no NVDA event),
  **NUVL, TSM** (MU sympathy +4%), **QQQ, SPY** (index).

## Sector themes

- **AI-memory supercycle — hard-validated by MU, now a two-sided story.** MU's record
  print + Q4 ~$50B guide rippled to the NAND/DRAM cohort (**WDC +13%, STX, SNDK +16%**);
  Defiance launched a 2x DRAM ETF (DRAL). **The same shortage is a device-maker cost
  headwind** — AAPL (+15–20% Mac/iPad), MSFT (Xbox) raising consumer-hardware prices. Bull
  (memory makers) and bear (device makers) of one story on the same tape.
- **Compute / custom-silicon race widens — QCOM enters.** Qualcomm's Investor Day pivot
  ($15B data-center revenue by FY29; Dragonfly C1000 CPU; **Meta as anchor customer**,
  2028 production; $40B FY29 non-handset target) adds another merchant-GPU alternative
  alongside AVGO/OpenAI (Jalapeño) and AWS/Trainium. QCOM +7.4%.
- **Bank capital returns unlocked post-stress-test.** JPMorgan ($50B buyback + 10%
  dividend) and Goldman (dividend raise) led financials; a Dow-rotation tailwind.
- **Macro rotation: value over growth on a hot-inflation day.** Hot PCE + Mag-7
  memory-cost weakness drove a rotation into healthcare/financials/industrials (CAT, UNH);
  Nasdaq down a 4th day while the Dow rose.
- **Energy: oil < $70 (4th down session).** Mideast risk premium nearly unwound on
  US-Iran de-escalation + Hormuz reopening + US waiver. Disinflationary, risk-positive.

## Candidates for the universe

**2 promotions this run (both technology). Universe → 25.**

- **QCOM (PROMOTED — Tier-B #5, Tier-1 customer win).** Qualcomm's Investor Day named
  **Meta as anchor customer for the Dragonfly C1000 data-center CPU** (2028 production)
  and roughly doubled its FY2029 non-handset target to $40B (incl. $15B data-center);
  stock +7.4%. A named-hyperscaler anchor commit, verifiable (CNBC/Bloomberg/ServeTheHome)
  → meets Tier-B #5. Now in-universe and **UNCLAIMED** — trader P0 triage / Saturday
  research owns the strategy claim.
- **SNDK (PROMOTED — Tier-A, 3-session recurrence).** SanDisk recurred a 3rd consecutive
  session in the memory cohort, now **hard-validated by MU's record print** (SNDK +16% on
  the day, ~600% YTD, Defiance DRAM-ETF launch, sustained sell-side cohort framing). Per
  the 2026-06-04 "act, don't defer" discipline, promoted at session 3. Now in-universe and
  **UNCLAIMED**.
- **Still watches (NOT promoted):** **WDC / STX** (memory cohort, rode MU — flow/sympathy,
  not own catalysts; WDC +13%), **CRDO** (AI interconnect, thematic), and the standing
  **WOLF / SMCI** flow-recurrence names (flow does not refresh the catalyst clock).

## Macro / sector context

- **May PCE printed HOT (released 6/25): core PCE 3.4% YoY** (highest since Oct 2023),
  +0.3% m/m; headline 4.1% (highest since Apr 2023), +0.4% m/m; energy +3.9% m/m. Above
  the Fed's 2% target; reinforces higher-for-longer. Economists still expect May to mark
  the 2026 inflation peak, with slowing from July as gasoline falls. **No FOMC this
  session.**
- **Fed bank stress-test results (6/24) cleared large-bank capital returns** → JPMorgan
  $50B buyback + dividend, Goldman dividend raise.
- **Oil < $70 (WTI ~$70.7 / Brent ~$73.4), 4th consecutive down session**, lowest since
  late February, on US-Iran de-escalation, Strait-of-Hormuz reopening, and the US waiver
  for already-loaded Iranian crude. Disinflationary, risk-positive — not a shock.
- **GOOGL → DJIA effective pre-open Mon 6/29** (replacing VZ) — scheduled index-membership
  change / forced flow; Dow funds rebalance into GOOGL. (GOOGL traded lower today; Google
  Finance exited beta with portfolios/AI tools.)
- **VIX ~18.6 (−5% on the day)** — eased back toward 18 after the early-week de-rating;
  term structure in normal contango, no inversion. Dispersion is single-name (MU IV crush;
  AAPL/CBRS realized), not systemic.

## Library gaps

Every `responder: NONE` (or partial) item above, re-listed for the trader's tasks.md →
Saturday research. `gap-registry coverage_holes` is **empty**; these are
**activation/assignment** gaps (responder exists but isn't active / claims no universe
symbol) plus **taxonomy** gaps (NEW_CATEGORY_NEEDED).

- **NEW — Input-cost / margin-compression event on a held name (AAPL price hikes).** A
  held long fell 6.1% on a genuine corporate event (15–20% Mac/iPad price hikes driven by
  memory-cost inflation), but AAPL is claimed only by price-driven trend-following — no
  rule reads a cost/margin-shock disclosure. **First held-name NEGATIVE event of the
  recent run with no responder.** **Suggested research:** whether an event-window overlay
  should co-claim AAPL (and peers) for cost-input / margin-guidance events.
  gap_type: event_catalyst — responder: NONE.
- **NEW — Capital-allocation event (JPM $50B buyback + dividend).** No active rule reads a
  buyback/dividend authorization; JPM is price-claimed. **Suggested research:** a
  capital-allocation sub-trigger or event-window overlay for buyback/dividend
  announcements. gap_type: event_catalyst — responder: NONE.
- **Earnings-window assignment on CBRS — Day-2 realized (record two-session loss).** CBRS
  is claimed by trend-following (price-driven); the earnings-window responder
  (equity_event_driven_catalyst) does NOT claim it. **Suggested research:** head-to-head
  CBRS vs equity_event_driven_catalyst; assign to the event-driven responder.
  gap_type: earnings_window — responder: NONE (assignment).
- **Sell-side initiation event (INTC Goldman Neutral $150).** Single-bank initiation, no
  responder (and below the Tier-B 3-bank cluster threshold). gap_type: event_catalyst —
  responder: NONE.
- **Product/partnership sub-trigger on event-driven covered names — AVGO Jalapeño
  (carry).** AVGO is claimed by equity_event_driven_catalyst but the strategy models
  earnings windows, not product/partnership deals. gap_type: event_catalyst — responder:
  partial (claimed, unmodeled).
- **Restructuring / workforce-reduction events (ORCL 21k cuts, carry).** Claimed by
  event-driven but unmodeled. gap_type: event_catalyst — responder: partial.
- **Index-rebalance / forced-flow window — TWO live instances (carry).** GOOGL → DJIA 6/29
  (forced buy); SPCX → Nasdaq-100 ~July 1; held QQQ. No active rule reads an index-
  rebalance schedule. **Suggested research:** an index-rebalance/forced-flow overlay. NB
  carry-forward operator Q: should index-inclusion become a 6th Tier-B trigger?
  gap_type: event_catalyst — responder: NONE.
- **Event-window coverage on price-claimed names (TSLA NTSB probe + wrongful-death suit;
  META federal-testing pressure; AMZN cloud reads).** `event_catalyst` is declared only by
  equity_event_driven_catalyst, which claims AVGO/MU/ORCL — not these names. **Suggested
  research:** broaden the event-driven claim set or add a lightweight event-window overlay.
  gap_type: event_catalyst — responder: NONE.
- **Macro-event window (hot PCE / higher-for-longer; oil/Iran macro).** No canonical
  gap_type covers a scheduled macro print/regime; no rule lets the trader pre-position
  around PCE/FOMC/jobs (correct under the mandate — but the soft-signal handle is missing).
  gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **Vol-regime activation (MU post-print IV crush = short-vol setup).** volatility_regime
  is declared (iron_condor_high_iv, calendar_spread, jade_lizard, long_straddle_earnings)
  but none are active and none claim a universe symbol — so no active strategy reads the
  VIX regime, MU's IV crush, CBRS's first-print vol, or SPCX's hyper-IV. **Suggested
  research:** activate one vol strategy with a universe claim (MU post-print is the
  textbook iron-condor / short-vol setup). gap_type: volatility_regime — responder: NONE
  (active); activation pending.
- **M&A-arb activation (NUVL/GSK, carry).** `pairs_arbitrage` declared by
  equity_pairs_trading_cointegration (not active); NUVL claimed by trend-following.
  gap_type: pairs_arbitrage — responder: NONE (active).

## Recommendations for the trader

- **NOTABLE, not halt-worthy — standard workflow; let rules ride.** No HALT-WORTHY trigger
  argues for skipping execute: no FOMC; MU (held) **resolved FAVORABLY**; AAPL's −6.1% is
  realized price on a cost narrative (not a guidance cut); oil/Iran is risk-positive.
  **Observe, don't override** — discretionary hedges and discretionary profit-taking are
  both forbidden by the algorithmic-only mandate.
- **MU (held) — the gap-up HELD; reconcile, don't act.** The print is out and the +15%
  cash-session move did not fade. Let equity_event_driven_catalyst's post-print window +
  the trailing stop govern; confirm the trailing-stop level updated against the post-print
  mark and log any rule-driven trim/exit at `execute`. No discretionary action on the good
  news.
- **AAPL (held) — a −6.1% cost-event day with no algorithmic handle.** The 15–20% Mac/iPad
  price hike is a fundamental margin signal, but it reaches the position only as realized
  price (logged as a NEW held-name input-cost library gap). If AAPL's drop reaches a
  trend/momentum rule, execute; otherwise no action. Do not discretionarily hedge.
- **P0 triage — TWO new unclaimed symbols (QCOM, SNDK).** Both were promoted by the news
  agent today and are **UNCLAIMED**. Per the mandatory-attach doctrine, run
  `triage-symbol QCOM --gap-type event_catalyst` and `triage-symbol SNDK --gap-type
  trending` (memory-cohort momentum) to restore `unclaimed_count == 0` (provisional/
  quarantined is acceptable if backtests can't rank). News agent cannot attach strategies.
- **JPM / INTC / TSLA / CBRS — events with no responder; react to realized price only.**
  Buyback (JPM), Goldman init (INTC), NTSB probe (TSLA), Day-2 slide (CBRS) all reach the
  book only as price; logged as library gaps for Saturday.
- **SPCX stays execution-quarantined.** Bond-deal "bubble" commentary + Nasdaq-100 add
  (~July 1) are research signal, not a trader action (revalidate_by 2026-07-04).
- **`cli execute` should run as scheduled.** Standard post-close run; the algorithmic-only
  mandate governs. The active tasks are the MU post-print reconciliation and the QCOM/SNDK
  P0 triage above.
