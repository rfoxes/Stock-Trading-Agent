# News brief for 2026-06-15

## Headline assessment

**NOTABLE.** Risk-on relief day. (1) **US-Iran peace deal announced** — Trump declared the deal "complete," reopened the Strait of Hormuz and removed the Navy blockade; oil −5%, 10y yields to one-month lows, S&P +1.9%. This RESOLVES the active US-Iran exchange that was live in the last brief (Wed 6/10). Signing ceremony Fri 6/19 in Switzerland (Israel-Lebanon strikes a tail risk to durability). (2) **VIX crushed ~9% to 17.68** (from ~19.87) — the first decisive break below 20 after three weeks of oscillation, as the geopolitical event premium drained. (3) **The whole book rallied**: MU flipped from −11.5% (Wed) to **+10%** at $1,081 on a ~12% pop into its June 24 print; ORCL (the Wed buy, now filled) +8% after rebounding 5% off last week's capex-shock low. (4) **FOMC June 16-17 — hold priced ~97%, but the new dot plot Wednesday is the live catalyst** and lands the session AFTER tomorrow's trader run. (5) Policy overhang: **the Trump admin forced Anthropic to disable Fable 5 / Mythos 5 for all foreign users** (export-control order) — an AI-sector national-security thread under the rally. **Not HALT-WORTHY** — the Iran move is a de-escalation (risk-on, not a shock), no active FOMC on tomorrow's session, no held-name overnight surprise. Treat as a constructive event-window day; algorithmic-only mandate governs.

> **Catch-up note:** This is the first brief since Wed 2026-06-10 — the Thu 6/11 and Fri 6/12 news runs did not update state (last_handoff/news_brief/news_tasks all still dated 6/10). Items below fold in what happened Thu-Fri (SpaceX priced Thu / listed Fri; ADBE printed Thu; Iran deal reached over the weekend). Deployment was also broken at the start of this run (venv interpreter orphaned by a Homebrew python 3.13→3.14 upgrade) — repaired before fetch; see operational notes.

## Watchlist + positions

(Held longs per live broker snapshot: **AAPL 72 (+8.88%), MU 7 (+9.98%), ORCL 38 (+8.25%), QQQ 28 (+14.44%), SPY 35 (+6.29%)**. Equity $108,589, cash $25,327 — net-long now, up +4.8% vs Wed close. Regime: bull, conf 0.75, ADX 24.98. 7 strategies × 22/22 claimed, unclaimed_count == 0.)

- **MU — EVENT (pre-print, Q3 FY26 = Tue 6/24 AMC; held long, now +9.98%).** Surged ~12% Monday; analysts lifting PTs as high as $1,250; "Broadcom-driven drop never made sense, dip buyers up 40%." Confirmed unusual options flow (calls > puts in $ terms) reads as bullish pre-print positioning. The Wed stop-risk concern (-11.5%, ~6.5% buffer) is fully resolved — position is green and the print is the next catalyst.
  - gap_type: earnings_window
  - responder: equity_event_driven_catalyst (claims MU; pre-print window posture)

- **ORCL — EVENT (post-capex-shock recovery; Wed buy now filled, +8.25% at $191.9).** Rebounded +5% Monday after its worst weekly drop since 2002; BofA and Goldman reiterated bullish on the AI-cloud-infra thesis. The Wed `equity_event_driven_catalyst` buy (38 sh @ $177.28) filled and is now in the money — the asymmetric beat-but-capex print has resolved to the upside on the relief tape.
  - gap_type: event_catalyst
  - responder: equity_event_driven_catalyst (claims ORCL; on-character post-print window)

- **GOOGL — EVENT (capex: $1.5B Alabama data-center expansion disclosed; +3%+).** Concrete AI-infra capex commitment on the risk-on tape. Also: a congressional-purchase disclosure (Rep. Taylor) and Eisman "rotating away from hyperscalers" commentary (opinion, dropped). No current position (exited 6/10).
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (claims GOOGL; price-driven rule re-engages on a fresh EMA cross)

- **AAPL — POLICY TAG only (held long, +8.88%).** No single-name fundamental event. Named in the Trump French-digital-tax tariff threat (AAPL/AMZN/META/GOOGL) — a negotiating posture, not an action. Otherwise caught the broad tech bid.
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (claims AAPL; price-driven; no event-window rule — library gap re-affirmed)

- **NVDA — POLICY/CHINA (no position).** +2% on the cohort bid. Negative structural thread: ByteDance reportedly evaluating domestic AI chips (Iluvatar CoreX, Baidu); Box CEO warns US restrictions accelerate the open-weight/sovereign-AI shift. Sequoia's Maguire drew an "early-NVIDIA" comparison to SpaceX. China-TAM erosion is a slow headwind, not a same-day catalyst.
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (claims NVDA; no fresh entry signal)

- **META — POLICY/EARNINGS-CONTEXT (no position).** +4.47% premarket on the relief rally; cohort pieces cite a projected ~$60B summer earnings print (weeks out). Named in the French digital-tax threat. No fresh single-name catalyst.
  - gap_type: trending
  - responder: equity_momentum_macd_histogram (claims META; price-driven)

- **MSFT — EARNINGS-CONTEXT (no position).** +1.92% premarket; ~$87B summer print referenced (weeks out). Eisman "hesitant on MSFT" (opinion, dropped). No fresh single-name event.
  - gap_type: trending
  - responder: equity_momentum_macd_histogram (claims MSFT; price-driven)

- **TSM — COHORT (no position).** +4% premarket; on the IT whale-alert screen. AI-chip demand thesis intact; no fresh single-name disclosure today.
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (provisional claim; price-driven)

- **INTC — COHORT (no position).** +3% premarket on the broad chip rally; on the IT whale-alert screen. No fresh Google-foundry verification. Price action, not event.
  - gap_type: breakout
  - responder: equity_breakout_volume_confirmation (provisional claim; no volume-confirmed breakout)

- **TSLA — FLOW/NEUTRAL (no position).** Surging on SpaceX-merger chatter (analysts: no merger this year) and the "all things Elon" trade (Direxion 2X SPCX ETF launched). Offset: a report flags "inflated" FSD-Europe safety claims. No re-entry-grade single-name fundamental event.
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (claims TSLA; no signal)

- **AVGO — COHORT (no position).** Single item: "Micron's Broadcom-driven drop never made sense" — references last week's AVGO-print-driven chip selloff, now unwinding. No fresh AVGO catalyst (next print September).
  - gap_type: event_catalyst
  - responder: equity_event_driven_catalyst (claims AVGO; calm posture, no fresh catalyst)

- **AMZN — POLICY TAG (no position).** Climbed on falling oil / easing tensions; named in the French digital-tax threat and the Anthropic-AI-policy pieces. No single-name fundamental event.
  - gap_type: trending
  - responder: equity_trend_following_ema_cross (claims AMZN; no signal)

- **No fresh single-name news** (caught the broad rally / screen mentions only): **ARM, AVGO, CBRS, CSCO, DELL, HPE, JPM, MRVL, NUVL.** JPM benefits indirectly as a SpaceX lead-underwriter (franchise event, see library gaps) but had no single-name disclosure. CBRS appeared once in a "5 stocks from most-accurate analysts" piece (no fresh initiation). ARM/CSCO/HPE/JPM/NUVL had 0 Alpaca items.

## Sector themes

- **Geopolitical de-risking drives a broad, oil-down/tech-up relief rally.** The US-Iran deal reopened Hormuz (~20% of global oil flow), oil −5%, yields to one-month lows. The energy-passthrough that drove May's 4.2% CPI is now reversing — a tailwind to the forward inflation read even though the June FOMC is already a lock for hold.
- **AI-sector risk is increasingly policy/national-security, not just fundamental.** The Trump-admin order forcing Anthropic to disable Fable 5 / Mythos 5 for all foreign users, plus ByteDance's pivot toward domestic chips, frames an export-control overhang sitting under the cohort even on an up day. Watch for spillover into NVDA-China sentiment.
- **"FAB 10" reframing — AI-cohort leadership broadening to include private-turned-public names.** SpaceX's ~$2T listing and the FAB-10 (Mag-7 + OpenAI/SpaceX) framing signal the market is re-rating frontier-AI/space names. Concentration remains extreme: non-AI S&P names up just ~1% YTD (Bianco).
- **Chip cohort (financials/tech split):** TSM +4%, INTC +3%, AMD +4%, NVDA +2%, MU +12% — the chip selloff from last week's AVGO/ORCL capex scare reversed hard on the risk-on bid. Financials (JPM): the SpaceX IPO is a realized underwriter-franchise event.
- **Vol regime shift:** VIX broke below 20 (17.68, −9%) — the multi-week event-premium-rich posture has unwound. IV compression favors vol-selling structures for high-IV-rank names; the FOMC dot plot Wed is the one near-term event the term structure hasn't fully discounted.

## Candidates for the universe

**0 promotions this run. Universe stays at 22.** (No Tier-A clock advanced — see note on the 5-session gap; no Tier-B trigger cleared.)

- **Tier A (3-session recurrence):** CRWD (provisional 3), STM (2), FLEX (2), PINS (2), VSH (1), SMCI (1) — **none refreshed today.** Note: Thu 6/11 and Fri 6/12 runs did not execute, so these counters have not advanced since 6/10; recurrence is by *consecutive sessions* and today is the next session after a gap. SMCI appeared once in an Eisman cohort list (GOOGL/MSFT/ORCL/SMCI/SOXX) — not a single-name catalyst; holds at session 1.
- **Tier B (single-event triggers, 5 categories, 2/day cap):**
  - **#1 confirmed M&A target:** none. ROKU is the subject of takeover *speculation* (Needham Buy + PT raise; JPM names Comcast as the most logical buyer) — analyst speculation, not a confirmed/named deal. Does NOT qualify; track as a watch.
  - **#2 FDA binary:** none.
  - **#3 beat + raise + +5%:** **ADBE FAILS** — beat (EPS $5.96 vs $5.82, rev $6.62B vs $6.46B) and raised FY guide, but stock fell ~6% (cut H2 ARR growth on freemium pivot = 10th straight quarter of deceleration). No +5%; in fact negative. No external S&P name cleared the full triple today.
  - **#4 sell-side initiation cluster (3+ banks same week):** none confirmed.
  - **#5 Tier-1 customer-win:** none.
- **SPCX (SpaceX)** — newly public (listed Fri at ~$2T, largest IPO ever, options debut Tue). Massive liquidity and AI/space-cohort relevance, repeatedly cited in "FAB 10" framing. Does NOT meet a Tier-B trigger (an IPO isn't one of the five), and it's a hyper-volatile brand-new listing. **Logging as session-1 watch** for the operator/Saturday research agent — not promoting.
- **STX (Seagate) +9%, AXTI +14.8%** — storage/compound-semi adjacency on the risk-on tape, but no confirmed single-name catalyst from the screen-level data. Not candidates.

## Macro / sector context

- **US-Iran peace deal (06-15).** Trump: deal "complete"; Hormuz reopened, Navy blockade removed, "let the oil flow." Oil −5%, 10y yields to one-month lows, S&P +1.9%. Resolves the prior brief's active exchange. Signing Fri 6/19 in Switzerland; CBS flags Israeli strikes in Lebanon as a durability tail risk.
- **FOMC June 16-17.** Hold priced ~97%+ (funds rate 3.50-3.75%, second consecutive hold). New **dot plot Wednesday is the live catalyst** vs. the March median (25bp of 2026 cuts; 7 members saw none). May CPI 4.2% keeps the consensus against cuts through 2026. A "change in Fed leadership" is referenced. **Decision lands the session after tomorrow's trader run.**
- **Anthropic export-control order (06-12 to 06-14).** Commerce Sec. Lutnick subjected Fable 5 / Mythos 5 to export controls to all foreign persons; Anthropic disabled the models for ALL customers. Triggered by suspected China-linked access + an autonomous-weapons dispute (Pentagon blacklist). EU pushback; controls expected to lift once safety is remediated. AI-sector/national-security overhang.
- **Trade policy:** Trump threatens 100% tariffs on French wine over France's digital tax on US tech (AAPL/AMZN/META/GOOGL), ahead of G7. Posture, not action.
- **Labor:** a "shadow unemployment" report says sidelined workers (people who want jobs but can't find them) now exceed 2008-crisis levels (+~1.2M). Soft offset under the sticky-inflation print.

## Library gaps

- **Macro-print / geopolitical-resolution event window (Iran deal + FOMC dot plot Wed)** — no `macro_event_window` overlay active. The trader cannot pre-position for the dot plot algorithmically (correct under the mandate), but the soft-signal handle is missing. **Suggested research:** macro/event-window overlay (pre-event sizing + post-event posture re-eval) covering scheduled prints (FOMC/CPI) and binary geopolitical resolutions.
  - gap_type: event_catalyst
- **VIX-threshold cross / vol-regime shift (VIX broke below 20, −9% to 17.68)** — `volatility_regime` is a confirmed registry coverage hole (no responder). The IV-compression regime favors vol-selling structures, but no strategy reads the VIX-regime transition. **Suggested research:** vol-regime overlay that flips posture on a confirmed VIX threshold cross; would also give `iron_condor_high_iv` a universe symbol to claim.
  - gap_type: volatility_regime — responder: NONE — library gap (coverage hole)
- **AI-policy / export-control shock overlay (Anthropic Fable/Mythos ban; NVDA-China substitution)** — no rule responds to national-security/export-policy events that hit AI-cohort names. Soft signal only. **Suggested research:** policy-event sentiment overlay tagging export-control / regulatory-AI headlines as a cohort risk flag.
  - gap_type: event_catalyst
- **Underwriter-franchise event for JPM (SpaceX IPO listed; OpenAI Q4 listing pending)** — `underwriter_franchise_event` still absent. The franchise tailwind from a record IPO doesn't map to any active JPM rule (trend-following, price-driven only). Re-affirmed.
  - gap_type: event_catalyst
- **M&A-arb (NUVL/GSK)** — `m_a_arbitrage_event` still absent; NUVL pre-close, trades freely. Re-affirmed.
  - gap_type: pairs_arbitrage
- **Capex-shock asymmetric-reaction detector (ORCL)** — last week's beat+raise+capex-shock print is now resolving to the UPSIDE (+5% Monday), which actually *validates* the Wed `equity_event_driven_catalyst` buy. The open soft-signal gap is the inverse: the keyword detector couldn't distinguish the asymmetric print at entry. Re-affirmed for Saturday research (positive/negative-signal nuance in `news_brief.has_positive_signal`).
  - gap_type: event_catalyst

## Recommendations for the trader

- **NOTABLE, constructive. Standard workflow with event-window awareness.** The dominant event (Iran deal) is a de-escalation — risk-on, not a shock — so the posture is "let rules ride the relief tape," not "defend." No HALT-WORTHY trigger.
- **MU (held, +9.98%) into the 6/24 print.** Pre-print event window is now open and the position is green with bullish flow. Don't override — let `equity_event_driven_catalyst`'s window logic and the trailing stop govern. The Wed stop-risk is gone.
- **ORCL (held, +8.25%) — the Wed catalyst buy is working.** The asymmetric capex-shock print resolved to the upside. Trust the rule's exit logic; no discretionary action.
- **FOMC dot plot Wednesday is the live macro catalyst** (lands after tomorrow's run). No `macro_event_window` rule, so the trader cannot pre-position — that's correct. Soft awareness only: a hawkish dot-plot revision is the main risk to the AI-cohort multiple over the next 48h; rules will react to price after the fact.
- **VIX broke below 20 (17.68).** Vol-selling structures are favored by IV rank, but no `vol_regime_shift_overlay` is active and `iron_condor_high_iv` claims no universe symbol — observation only.
- **Anthropic export-control overhang + NVDA-China substitution** are slow structural threads, not same-day catalysts. No rule fires on policy; observation only.
- **`cli execute` should run as scheduled.** If a rule fires (most likely MU/ORCL event-window or a fresh trend cross on the relief tape), execute; if none fires, no trade is the correct outcome. Algorithmic-only mandate governs.
