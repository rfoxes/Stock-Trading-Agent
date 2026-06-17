# News brief for 2026-06-17

## Headline assessment

**NOTABLE.** The FOMC dot plot delivered a genuine **hawkish pivot** — the
single biggest macro repricing of the cycle — but it is already in prices by
tonight's post-close run, so it is NOTABLE, not HALT-WORTHY. The Fed held
3.50-3.75% (12-0, ~97% priced), but the **median 2026 dot rose to 3.8% from
3.4% in March — a quarter point ABOVE the current range**; the committee's
central expectation flipped from cuts to a net HIKE bias (9/18 see ≥1 hike in
2026, 6 see two). Warsh's debut was hawkish-by-omission (shorter statement, no
forward guidance, five new task forces). **Hot retail sales** (+0.9%, ~2x
consensus, 12th straight core gain) reinforced it. Equities sold off (S&P
-1.21%, Nasdaq Comp -1.34%) and **VIX jumped +12.37% to 18.44** (still sub-20).
**Not HALT-WORTHY:** the manual's first halt trigger is an *active/pending* FOMC
on the session being planned into — the decision happened TODAY (6/17) and is
fully in the cash close; the trader plans into 6/18 with the result known, no
held name carries a confirmed negative overnight catalyst, and there is no
futures gap >2% to plan blind into. The book is heavily AI-cohort/rate-sensitive
levered, so the de-rating risk is real — but rules react to realized price, which
is the intended behavior. Constructive-but-cautious; algorithmic-only mandate
governs.

## Watchlist + positions

(Held longs per the 6/16 trader handoff: **AAPL 72, AVGO 26, MU 7, ORCL 38,
QQQ 28, SPY 35.** Active set: 7 strategies; universe 23, **23/23 claimed,
unclaimed_count == 0**. SPCX remains the lone **PROVISIONAL, execution-
quarantined** claim on equity_trend_following_ema_cross (no price history —
revalidate_by 2026-06-30; it will NOT trade). `gap-registry coverage_holes`
confirmed **empty** this run — remaining gaps are activation/assignment +
taxonomy gaps, not registry holes.)

- **AAPL — EVENT (management guidance; held long).** CEO Tim Cook warned Apple
  **will raise prices on soaring memory costs**, calling it "a 100-year flood";
  AAPL also flagged as "best positioned to navigate the AI memory crunch." A real
  forward-guidance / cost-structure event (and a bullish read-through to MU's
  memory super-cycle). The chip-cohort/FOMC selloff is price action — the trader
  sees it.
  - gap_type: event_catalyst
  - responder: NONE — library gap. AAPL is claimed by equity_trend_following_ema_cross
    (price-driven); equity_event_driven_catalyst (the only event_catalyst responder)
    does not claim AAPL. A guidance/cost event on a trend-claimed name has no
    algorithmic handle.

- **MU — EVENT (pre-print, Q3 FY26 = Tue 6/24 AMC; held long).** Analysts revising
  estimates higher; "likely to report higher Q3"; Perplexity's CEO floated Micron
  overtaking Meta on AI-memory demand; bullish call flow + IV expansion into the
  print. Cook's memory-cost warning is a same-day demand tailwind. Pre-print event
  window open.
  - gap_type: earnings_window
  - responder: equity_event_driven_catalyst (claims MU; pre-print window posture)

- **HPE — EVENT (partnership; +4%).** HPE announced a partnership with **NVIDIA to
  power Vultr's next-gen AI cloud**; shares +4% on the news. A concrete
  product/partnership catalyst.
  - gap_type: event_catalyst
  - responder: NONE — library gap. HPE is claimed by equity_rsi_divergence
    (mean-reversion/divergence, price-driven); no active event responder claims HPE.

- **MRVL — EVENT (CEO endorsement + alliance; +3%).** NVIDIA CEO Jensen Huang
  predicted Marvell becomes the **next trillion-dollar company** via a new **$2B
  AI-chip alliance**; MRVL +3% premarket. A genuine catalyst on a claimed chip name.
  S&P 500 inclusion still pending 6/22 (passive-flow window this week).
  - gap_type: breakout
  - responder: equity_breakout_volume_confirmation (claims MRVL; on-character IF the
    move is volume-confirmed — the textbook setup for this strategy)

- **ORCL — EVENT (report rebuttal; held long).** Oracle **denied a report** that
  security concerns killed a potential **$3B Microsoft cloud deal**. A rebuttal of a
  negative report rather than a fresh positive catalyst; net neutral-to-mildly-
  supportive. No fresh print (Q4 FY26 was ~6/9).
  - gap_type: event_catalyst
  - responder: equity_event_driven_catalyst (claims ORCL; calm posture, no entry signal)

- **META — EVENT (regulatory posture shift).** Zuckerberg **reversed years of
  opposition and now backs the Kids Online Safety Act (KOSA)** — a regulatory
  posture shift for META and the platform cohort. (Adjacent: TikTok Florida
  underage-safety lawsuit; OpenAI multi-state AI-safety probe pre-IPO.)
  - gap_type: event_catalyst
  - responder: NONE — library gap. META is claimed by equity_momentum_macd_histogram
    (price-driven); no active strategy reads a regulatory-posture event.

- **NVDA — POLICY read-through (no position).** Trump administration **held off
  blacklisting DeepSeek + 100+ Chinese firms** (marginal export-control
  de-escalation); also Coherent's Texas AI-networking expansion (supply chain) and
  the HPE/MRVL alliance items (NVDA ecosystem). No same-day NVDA operating catalyst.
  - gap_type: event_catalyst
  - responder: NONE — library gap. NVDA is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads an export-policy/national-security event.

- **QQQ — EVENT (pending index-rebalance flow; held long).** Carry-forward, still
  live: SPCX is on track for **Nasdaq-100 fast-entry inclusion ~July 1** (+ Russell
  6/26), ~$22-27B of forced index buying into a 3-5% float, which forces QQQ trackers
  to **reweight existing constituents** (the held mega-caps) over ~2 weeks. A
  mechanical, scheduled flow event on a held position — distinct from the FOMC price
  action.
  - gap_type: event_catalyst
  - responder: NONE — library gap. QQQ is claimed by equity_trend_following_ema_cross
    (price-driven); no active rule reads a scheduled index-rebalance/forced-flow event.

- **TSLA — FLOW/CHATTER (no position).** Dominated by SpaceX spillover: prediction-
  market chatter on a hypothetical **SpaceX-Tesla "$5T merger"** (unconfirmed, not
  actionable) and a Texas DOT official endorsing the Cybercab robotaxi. No
  re-entry-grade single-name fundamental event.
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (claims TSLA; no signal)

- **SPCX — NEW-LISTING FLOW (PROVISIONAL/execution-quarantined).** **Record options
  debut: ~1.8M contracts / ~$2.8B premium day one** (broke META's 2012 first-day
  record; 3rd-most-traded behind TSLA/NVDA), call/put ~1.3:1, gamma-squeeze dynamics
  on a tiny float + a large Sept &lt;$205 put hedge into the Aug lock-up; ETF frenzy
  >$1B; Morningstar pegs fair value ~$780B vs. the ~$2.65T market cap. SPCX -3.91%.
  Cramer flagged "meme-stock" risk. 30 Alpaca items — densest in the universe.
  - gap_type: volatility_regime (hyper-IV new listing; no price/earnings history)
  - responder: equity_trend_following_ema_cross (PROVISIONAL/UNVALIDATED, execution-
    quarantined; Saturday research revalidates by 2026-06-30)

- **No fresh single-name news** (tape / screen / spillover mentions only):
  **AMZN, ARM, AVGO, CBRS, CSCO, DELL, GOOGL, INTC, JPM, MSFT, NUVL, SPY, TSM.**
  AVGO drew only analyst "AI-pipeline" commentary (opinion, dropped); AMZN/MSFT/GOOGL
  appeared mostly in ETF/AI-agent commentary + the ORCL-MSFT deal rebuttal + SpaceX
  spillover; INTC +3.23% on a whale screen + an Iran-relief "cheap stocks" list (no
  hard catalyst); SPY is insulated from the SPCX rebalance flow (S&P GAAP rule
  excludes loss-making SpaceX). ARM/CBRS/CSCO/NUVL had 0-1 Alpaca items.

## Sector themes

- **AI-memory super-cycle — demand signal stacking.** Cook's "100-year flood"
  memory-cost / price-hike warning + MU's pre-print strength (PT raises, bullish
  flow, "could overtake Meta") + South Korea's EWY ETF +112% YTD (SK Hynix/Samsung).
  The single-name memory-demand signal stayed constructive even on a hawkish-macro
  down tape. Read-through: MU (held), and a cost headwind for AAPL hardware margins.
- **AI buildout is a financing/leverage + permitting story (carry-forward).** The
  "$4.1T AI-debt" reframing (JPMorgan) + the $130B data-center-permitting backlash
  (14-state moratorium bills) remain a structural headwind to the infra-capex cohort
  (ORCL/DELL/hyperscalers). A hawkish Fed (higher-for-longer rates) raises the cost
  of that leverage — the two narratives now compound.
- **SpaceX index-rebalance flow (scheduled, mechanical).** Nasdaq-100 fast-entry
  ~July 1 + Russell 6/26; ~$22-27B forced buy into a 3-5% float reweights held QQQ's
  existing constituents over ~2 weeks. SPY excluded (GAAP-profitability rule) until
  mid-2027+. Don't mistake rebalance-driven QQQ-constituent pressure for fundamental
  weakness.
- **Vol regime — the sub-20 calm broke (mildly).** VIX +12.37% to 18.44 on the dots
  (below the >3-point regime-marker threshold; still sub-20). Front-end IV
  re-inflated vs. the pre-FOMC term structure but the level is middling — not the
  >50 IV-rank that vol-selling wants nor the <20 that vol-buying wants. SPCX is the
  lone hyper-IV outlier.

## Candidates for the universe

**0 promotions this run. Universe stays at 23.** No automated trigger fired.

- **Tier A (3-session recurrence):** No carry-forward candidate appeared with a
  fresh single-name CATALYST today. CRWD (clock already broke), STM/FLEX/PINS (2,
  no refresh), VSH/SMCI (1; SMCI/WOLF surfaced only on the IT whale-FLOW screen,
  which does NOT refresh the catalyst clock), QCOM (only AI-agent commentary, not a
  catalyst). None advance.
- **Tier B (single-event triggers, 5 categories, 2/day cap):**
  - **#1 M&A target:** none qualifying. The SpaceX-Tesla "$5T merger" is prediction-
    market chatter, not a confirmed deal, and both names are already in the universe.
  - **#2 FDA binary:** none CONFIRMED. uniQure (QURE) +75.6% and Biohaven (BHVN)
    +14.8% are large biotech binary-style moves, but the catalyst TYPE is unconfirmed
    (approval vs. trial data) — per "never invent a Tier-B qualifier," not promoted.
    Logged as a watch (and the universe is tech-centric; healthcare = only NUVL).
  - **#3 beat + raise + +5%:** none (KMX/CVNA used-car prints were *misses*/down).
  - **#4 sell-side initiation cluster (3+ banks/week):** none confirmed.
  - **#5 Tier-1 customer win:** the HPE-NVIDIA-Vultr partnership and the
    Jensen/MRVL $2B alliance are real wins — but **HPE and MRVL are already universe
    members**, so neither is an addable external candidate.
- **Watches for the operator / Saturday research (NOT promoted):** **QURE / BHVN**
  (biotech binary movers, catalyst unconfirmed), **WOLF / SMCI** (semis/memory on
  whale-flow recurrence, no catalyst), **QCOM** (AI-agent "safest pick" commentary),
  **RIVN** (R2 launch + humanoids, session-1).

## Macro / sector context

- **FOMC June 17 — Warsh's first meeting, HAWKISH dot-plot pivot.** Held 3.50-3.75%
  (12-0). Median 2026 dot raised to **3.8% (from 3.4% in March)**, above the current
  range; **9/18 officials project ≥1 hike in 2026, 6 see two**. Cuts→hikes pivot.
  Warsh: shorter statement, removed forward guidance, five task forces (operations,
  communications, data, productivity/labor, causes of inflation); did not submit his
  own dot.
- **US retail sales May +0.9%** (~2x the 0.5% consensus; April was +0.4%), core +0.8%
  (12th straight gain), +6.9% YoY. Gas stations +3.4% (Iran fuel passthrough),
  nonstore +1.5%. Resilient consumer — hawkish-supportive into the dots.
- **US-Iran peace deal — signing Fri 6/19 Geneva (confirmed).** Permanent end to
  operations (incl. Lebanon); Strait of Hormuz reopens Friday; US naval blockade
  lifts immediately (Iranian oil exports resume); 60-day nuclear/sanctions track.
  Oil at March lows (WTI ~$76.44, Brent ~$79.45) on supply-return expectations.
  Israel-Lebanon strikes = durability tail risk.
- **Anthropic Fable 5 / Mythos 5 export ban — Day 5-6, still in force.** WH/Commerce
  negotiations ongoing; security veterans (incl. Alex Stamos) signed an open letter
  urging reversal; Fortune notes the gap favors Chinese open-source (DeepSeek/Z.ai).
  Other Claude models unaffected. Polymarket ~71% / Kalshi ~68% it returns by July 1.
- **Trade/regulation:** Trump admin held off blacklisting DeepSeek + 100+ Chinese
  firms (NVDA read-through); 100% French-wine tariff threat persists ahead of G7
  (posture). Platform-regulation risk broadening (META→KOSA, TikTok suit, OpenAI probe).

## Library gaps

Every `responder: NONE` item above, re-listed for the trader's tasks.md →
Saturday research. `gap-registry coverage_holes` is **empty**; the gaps below are
**activation/assignment** gaps (responder exists in the library but isn't active /
claims no universe symbol) plus **taxonomy** gaps (NEW_CATEGORY_NEEDED).

- **Macro-event window (FOMC dot plot + retail sales).** Today's hawkish pivot is the
  cleanest exemplar yet: no canonical gap_type covers a scheduled macro print, and no
  rule lets the trader pre-position/re-size around FOMC/CPI/jobs (correct under the
  mandate — but the soft-signal handle is missing). **Suggested research:** a
  `macro_event_window` category (pre-event sizing/posture re-eval). gap_type:
  NEW_CATEGORY_NEEDED — responder: NONE.
- **Event-window coverage on price-claimed names (AAPL guidance; HPE partnership;
  META KOSA reversal; NVDA export-policy).** `event_catalyst` is declared only by
  equity_event_driven_catalyst, which claims AVGO/MU/ORCL — not AAPL/HPE/META/NVDA.
  So guidance, partnership, regulatory-posture, and export-policy events on trend/
  momentum/divergence-claimed names have no algorithmic responder. **Suggested
  research:** broaden equity_event_driven_catalyst's claim set to event-prone large
  caps, or add a lightweight event-window overlay that co-claims alongside the price
  strategy. gap_type: event_catalyst — responder: NONE.
- **Scheduled index-rebalance / forced-flow window (SPCX → Nasdaq-100 ~July 1,
  Russell 6/26; held QQQ).** No active rule reads a known index-rebalance schedule as
  a flow event. **Suggested research:** an index-rebalance/forced-flow overlay
  (anticipated add/drop dates + estimated flow) as a soft posture signal on affected
  ETF holdings. gap_type: event_catalyst — responder: NONE.
- **Vol-regime activation (VIX +12.37% to 18.44; front-end IV re-inflating).** The
  registry hole is CLOSED (volatility_regime declared by iron_condor_high_iv,
  calendar_spread, jade_lizard, long_straddle_earnings), but none are active and none
  claim a universe symbol — so no active strategy reads the VIX regime. **Suggested
  research:** activate one vol strategy and give it a universe claim. gap_type:
  volatility_regime — responder: NONE (active); activation pending.
- **AI-capex permitting / financing-risk overlay.** The "$4.1T AI-debt" reframing +
  the $130B data-center-permitting backlash + a higher-for-longer Fed compound into a
  cohort financing/permitting headwind (ORCL/DELL/hyperscalers) with no rule flagging
  it. gap_type: NEW_CATEGORY_NEEDED — responder: NONE.
- **AI-policy / export-control overlay (Anthropic ban; DeepSeek-blacklist delay).**
  No rule responds to national-security / export-policy events on AI-cohort names.
  Soft signal only. gap_type: event_catalyst — responder: NONE.
- **M&A-arb (NUVL/GSK).** `pairs_arbitrage` is declared by
  equity_pairs_trading_cointegration (not active); NUVL is claimed by
  equity_trend_following_ema_cross (price-driven). Activation gap re-affirmed.
  gap_type: pairs_arbitrage — responder: NONE (active).
- **Underwriter-franchise event (JPM / SpaceX IPO + record options debut).** No rule
  maps the record-IPO underwriting tailwind to JPM (claimed by trend-following).
  Re-affirmed. gap_type: NEW_CATEGORY_NEEDED — responder: NONE.

## Recommendations for the trader

- **NOTABLE, constructive-but-cautious. Standard workflow; the FOMC result is known
  and in prices.** No HALT-WORTHY trigger: the decision happened today and is fully
  in the cash close, the trader plans into 6/18 with the outcome known, no held name
  has a confirmed negative overnight catalyst, and there is no futures gap >2% to
  plan blind into. Let rules ride; the hawkish repricing reaches the book through
  realized price (the intended path) — there is no macro_event_window rule to
  pre-position with, and that is correct under the mandate.
- **Book is heavily AI-cohort/rate-sensitive levered — observe, don't override.** The
  hawkish dots (median 3.8%, cuts→hikes) raise the cost of the cohort's leverage and
  pressure long-duration tech multiples. Rules react to price after the fact; do not
  add discretionary hedges no active strategy would generate (forbidden by the
  algorithmic-only mandate).
- **MU (held) into the 6/24 print.** Pre-print window is open with bullish flow, PT
  raises, and a same-day demand tailwind (Cook's memory-cost warning). Let
  equity_event_driven_catalyst's window logic + the trailing stop govern; no
  discretionary action.
- **QQQ (held) — SPCX Nasdaq-100 rebalance window (~July 1).** Soft awareness only:
  ~$22-27B forced SPCX buy reweights existing QQQ constituents over ~2 weeks. No
  active rule reads index-rebalance flow (correct); flagged so rebalance-driven
  pressure isn't mistaken for fundamental weakness. SPY insulated.
- **Vol: VIX 18.44 (+12.37%), sub-20.** IV re-inflated mildly off the lows but the
  level is middling — no clean vol-selling or vol-buying regime, and no active
  strategy claims a universe symbol with a volatility_regime rule (activation gap).
  Observation only.
- **`cli execute` should run as scheduled.** If a rule fires (most plausibly an
  MRVL volume-confirmed breakout on the Jensen/$2B-alliance catalyst, or an MU
  pre-print posture), execute; if none fires, no trade is the correct outcome. SPCX
  stays execution-quarantined. Algorithmic-only mandate governs.
