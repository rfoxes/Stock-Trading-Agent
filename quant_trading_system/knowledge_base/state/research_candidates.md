# Short-horizon candidate backlog (operator-sourced research)

Seeded 2026-07-19 by operator-side research as part of the short-term
transition (`manual.md` §P1, `research_manual.md` §"Short-horizon
mandate"). **Owner: the Saturday research agent.**

**ALL SEVEN CANDIDATES ARE ALREADY IMPLEMENTED AS MECHANICAL STRATEGY
FOLDERS (2026-07-19)** — `strategy.md` + `strategy.py` under
`knowledge_base/strategies/equity/`, each at `status: testing` (cannot
execute live — the runtime refuses non-active strategies — but IS a
triage/battery candidate). Your job is adjudication, not implementation.
Work a few entries per Saturday inside the rank-3 slot (after
provisionals and gaps): run the battery listed on each entry
(`cli evaluate-add <id>`, or `cli evaluate-update` for the v2), apply the
verdict verbatim, log the outcome in the weekly log, then delete the
entry from this file (validated, rejected, or blocked — all outcomes get
logged and removed). A REJECTed strategy gets archived via
`cli archive-strategy`, not deleted from disk. **The battery decides.
Nothing here is pre-approved.**

Every candidate below was screened for engine fit: daily bars only,
signals computed post-close, entries fill next open, once-daily
management, per-symbol backtests, addition battery needs ≥20 trades in
the window (the known floor — favor high-frequency setups), long-side
bias is simplest. Intended holds: days to a few weeks. No intraday.

---

## Tier 1 — high trade frequency, cleanest engine fit

### 1. `equity_rsi2_pullback` — RSI(2) pullback in uptrend (Connors)
- **IMPLEMENTED:** `strategies/equity/rsi2_pullback/` (testing).
  Adjudicate: `cli evaluate-add equity_rsi2_pullback` on 2-3 liquid
  large caps.
- **Source:** Larry Connors & Cesar Alvarez, *Short Term Trading
  Strategies That Work* (2008); rules + long-run backtest evidence:
  https://www.quantifiedstrategies.com/rsi-2-strategy/ and
  https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2
- **Starting rules:** long when close > 200-day SMA AND RSI(2) < 10
  (test 5 too — the literature finds lower entry = higher forward
  return). Exit when close > 5-day SMA, or RSI(2) > 70, or close <
  200-day SMA. Hard stop ~3-4% or 1.5×ATR; time stop 10 sessions.
- **Hold:** ~2-7 sessions. **Trade count:** high — the single most
  likely candidate to clear the 20-trade floor per symbol on liquid
  large caps.
- **Notes:** structurally a cousin of `equity_mean_reversion_bollinger`
  (different trigger: RSI2-in-trend vs band+RSI14+volume). Implement as
  a NEW strategy, then let head-to-head adjudicate any symbol overlap.
  Documented caveat: vanilla edge has decayed since ~2010 on indices —
  exactly what the battery's OOS split exists to detect. `timeframe:
  [swing]`, `gap_types: [mean_reversion]`.

### 2. `equity_double_seven` — Double 7s (Connors & Alvarez)
- **IMPLEMENTED:** `strategies/equity/double_seven/` (testing).
  Adjudicate: `cli evaluate-add equity_double_seven`.
- **Source:** same book;
  https://www.quantifiedstrategies.com/larry-connors-double-seven-strategy-does-it-still-work/
  and the co-author's own follow-up:
  https://alvarezquanttrading.com/blog/double-7s-strategy/
- **Starting rules:** long when close > 200-day SMA AND close is a
  7-day low; exit when close is a 7-day high. Add a hard stop (2×ATR)
  and a 10-session time stop (the naked book version has no stop — our
  SafetyGate era wants one). Test 5-day and 10-day variants of the low/
  high lookback.
- **Hold:** ~3-10 sessions. **Trade count:** high (book backtest: 1,189
  trades, avg +0.63%/trade on index ETFs).
- **Notes:** published evidence says the edge weakened post-2010 —
  treat as a battery test case, not a conviction pick; REJECT is a
  legitimate outcome. `timeframe: [swing]`, `gap_types:
  [mean_reversion]`.

### 3. `equity_mean_reversion_bollinger_v2` — IBS filter on the
existing Bollinger strategy (UPDATE PATH, not a new add)
- **IMPLEMENTED:** `strategies/equity/mean_reversion_bollinger_v2/`
  (testing) — incumbent's exact rules + IBS entry filter/exit
  accelerator. Adjudicate: `cli evaluate-update
  equity_mean_reversion_bollinger equity_mean_reversion_bollinger_v2`;
  REPLACE/KEEP verbatim. Do NOT run the addition battery on this.
- **Source:** Alexander Soffronow Pagonidis, *The IBS Effect: Mean
  Reversion in Equity ETFs* (2013):
  https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf
  ; practitioner replications: https://jonathankinlay.com/2019/07/the-internal-bar-strength-indicator/
  and country-ETF confirmation: https://arxiv.org/pdf/2306.12434
- **IBS = (close − low) / (high − low)** on the daily bar. Paper: next-day
  returns after IBS < 0.20 average +0.35% vs −0.13% after IBS > 0.80;
  an IBS filter improved index-ETF strategy returns ~10pp while cutting
  time-in-market ~45%.
- **Starting change:** clone `equity_mean_reversion_bollinger` →
  `_v2`, add entry condition `IBS < 0.2` (params: `ibs_entry_max: 0.2`)
  and optional exit-accelerator `IBS > 0.8`. Everything else identical.
  Run `cli evaluate-update equity_mean_reversion_bollinger <v2>` —
  REPLACE or KEEP per the battery.
- **Caveat:** the published IBS edge is measured close-to-close; our
  entries fill next OPEN, which forfeits part of the overnight
  component. That is fine — the point is whether the filter improves
  OUR engine's fills, which is exactly what evaluate-update measures.
- **Why this first:** cheapest test in the backlog (no new template,
  uses the sanctioned update path, inherits an already-claimed symbol
  set).

## Tier 2 — solid literature, moderate frequency

### 4. `equity_short_term_reversal` — N-day washout reversal, long-only
- **IMPLEMENTED:** `strategies/equity/short_term_reversal/` (testing).
  Adjudicate: `cli evaluate-add equity_short_term_reversal`; if blocked
  on the trade floor, loosen `decline_entry_pct` first.
- **Source:** Lehmann (1990), *Fads, Martingales, and Market
  Efficiency*; net-of-costs large-cap evidence: De Groot, Huij & Zhou
  (2012), summarized at
  https://quantpedia.com/strategies/short-term-reversal-in-stocks
- **Starting rules (per-symbol adaptation of the portfolio anomaly):**
  long when the 5-day return is below −X% (start X ≈ 5-7%, calibrate per
  liquidity band) AND close > 200-day SMA (trend guard; keeps this
  "buy a dip in a healthy name," not falling-knife catching) AND no
  earnings inside 3 sessions (the same guard bollinger uses). Exit on
  5-day high, RSI(2) > 70, +1.5×ATR target, 2×ATR stop, or 7-session
  time stop.
- **Hold:** ~3-7 sessions. **Trade count:** tunable via X — if the
  battery blocks on <20 trades, loosen X before abandoning; a
  too-selective variant already failed the floor once this July
  (see `research_log/2026-07-11.md`).
- **Notes:** the academic long-short weekly-rebalance construction is
  NOT implementable here (portfolio short leg); this per-symbol
  long-leg adaptation is the engine-fit version. `timeframe: [swing]`,
  `gap_types: [mean_reversion]`.

### 5. `equity_post_event_drift` — gap+volume event-proxy drift
(backtestable PEAD)
- **IMPLEMENTED:** `strategies/equity/post_event_drift/` (testing) —
  event day detected from bars (gap ≥4% + volume ≥2.5×20d + strong
  close), session-counted time exit that works IN BACKTESTS. Adjudicate:
  `cli evaluate-add equity_post_event_drift` on high-news names
  (ARM/SMCI/MU/INTC cohort); then run it as an unrestricted-triage
  challenger on the event-driven provisionals.
- **Source (anomaly):** Ball & Brown (1968) lineage; modern survey:
  https://quantpedia.com/strategies/post-earnings-announcement-effect
  and https://quantpedia.com/50-years-in-pead-research/ (drift persists
  ~4 weeks to a quarter; ~2.6-9.4%/quarter abnormal in the literature).
- **Why a proxy:** `equity_event_driven_catalyst` is un-backtestable
  (enters on a non-replayable news_brief signal — research_tasks Open
  Q#5, the degenerate-0-trade problem behind most current
  provisionals). This candidate detects the *event day from the price
  bar itself*, so every battery and triage CAN replay it: event-day :=
  overnight gap ≥ +4% AND volume ≥ 2.5× 20-day average.
- **Starting rules:** on an event-day signal (computed post-close),
  enter next open; exit at +2×ATR target, −1.5×ATR stop, close < event-
  day low (thesis invalidated), or 15-session time stop (inside the
  empirical 4-week drift window). Optional: require close-in-top-half
  of event-day range (holds the gap).
- **Hold:** ~5-15 sessions. **Trade count:** on high-news names
  (ARM/SMCI/MU/INTC cohort) likely clears 20 over 2y; on quiet
  mega-caps it won't — pick backtest symbols accordingly.
- **Notes:** this is the engine-compatible answer to the recurring
  "earnings-window assignment" gap the trader keeps logging (TSM 7/16
  is the live example) — a REPLAYABLE responder for earnings_window /
  event_catalyst gap_types. If validated, it also gives the nine
  event-driven provisionals (GS/MS/PYPL/UNH/RIVN/QCOM...) a rankable
  challenger via unrestricted triage. `timeframe: [swing]`,
  `gap_types: [earnings_window, event_catalyst, gap_play]`.

### 6. `equity_turn_of_month` — turn-of-the-month on SPY/QQQ
- **IMPLEMENTED:** `strategies/equity/turn_of_month/` (testing;
  frontmatter-restricted to SPY/QQQ). Calendar signals derive from
  dates/bars, fully sim-replayable. Adjudicate: `cli evaluate-add
  equity_turn_of_month` on SPY over the widest window; if validated,
  head-to-head vs the trend-following placeholders on SPY/QQQ.
- **Source:** Lakonishok & Smidt (1988) lineage; strategy page:
  https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes
  ; robustness: https://quantpedia.com/an-examination-of-the-turn-of-the-month-effect/
  (one of the most persistent calendar effects; futures evidence:
  Carcano & Tornero).
- **Starting rules:** long SPY (and/or QQQ) at the open of the 4th-to-
  last trading day of the month (signal computes on the prior close —
  fits the next-open engine); exit at the open of the 4th trading day
  of the new month. Optional regime guard: skip when SPY < 200-day SMA.
- **Hold:** ~6-7 sessions, ~12 round-trips/year → ~24 trades over a 2y
  window: clears the 20-trade floor, barely — use the full backtest
  window.
- **Notes:** claims SPY/QQQ, which currently sit on quarantined
  trend-following placeholders — a clean migration head-to-head once it
  passes the addition battery. Purely calendar-driven: no news
  dependency, trivially replayable. `timeframe: [swing]`, `gap_types:
  [mean_reversion]` (none fit perfectly; consider whether the taxonomy
  wants a `calendar_seasonality` gap_type — that itself is a
  NEW_CATEGORY_NEEDED note for the registry).

## Tier 3 — upper band (weeks), lower frequency; run after Tiers 1-2

### 7. `equity_52wk_high_momentum` — 52-week-high proximity breakout
- **IMPLEMENTED:** `strategies/equity/fifty_two_week_high_momentum/`
  (testing). Adjudicate: `cli evaluate-add equity_52wk_high_momentum`
  (widest window — lowest trade frequency in the backlog); if the only
  battery-relevant difference vs `equity_breakout_volume_confirmation`
  is the anchor, switch to the evaluate-update path instead.
- **Source:** George & Hwang (2004), *The 52-Week High and Momentum
  Investing*, Journal of Finance:
  https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf ; practitioner
  summary: https://alphaarchitect.com/the-secret-to-momentum-is-the-52-week-high/
  (0.65%/mo raw for the 52wk-high sort vs 0.38%/mo classic momentum;
  anchoring-bias mechanism).
- **Starting rules:** long when close makes a new 52-week high (or
  crosses within 2% of it) with volume ≥ 1.5× 20-day average and close
  > 200-day SMA; exit on 3×ATR trailing stop, close < 20-day SMA, or
  20-session time stop. This is the multi-week end of our band.
- **Hold:** ~10-20 sessions. **Trade count:** low per symbol —
  borderline on the 20-trade floor; expect to need the widest window.
- **Notes:** overlaps `equity_breakout_volume_confirmation`
  (donchian-style breakout). Check novelty per the manual: if the
  battery-relevant difference is just the anchor (52wk high vs N-day
  high), implement as `equity_breakout_volume_confirmation_v2` and use
  the UPDATE battery instead of the addition battery. `timeframe:
  [swing]`, `gap_types: [breakout, trending]`.

## Considered and REJECTED before implementation (do not build)

- **Pre-FOMC announcement drift** (Lucca & Moench, NY Fed:
  https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf ;
  https://quantpedia.com/strategies/federal-open-market-committee-meeting-effect-in-stocks):
  the drift is concentrated in the ~24h BEFORE the statement and
  post-announcement returns average ~zero — an intraday/overnight
  effect our once-daily next-open engine cannot capture, and ~8
  meetings/yr can't clear the trade floor. The FOMC calendar still
  matters — as news-brief calendar context, not as a strategy.
- **Overnight anomaly / close-to-open drift**: requires buying at the
  close; our post-close run can only achieve next-open fills. Not
  implementable without an engine change.
- **Literal academic short-term reversal portfolio** (weekly-rebalanced
  long-short deciles): needs a cross-sectional portfolio + short leg;
  our engine is per-symbol and the pairs short leg is already a known
  blocker (Open Q#5). Superseded by the long-only per-symbol adaptation
  (entry #4).

## Standing note for whoever works this file

Sources here clear the manual's quality bar (peer-reviewed, Fed/NAAIM
papers, Quantpedia, published-author practitioner blogs — Connors/
Alvarez, Kinlay, QuantifiedStrategies/Groette, Alpha Architect). Some
practitioner pages block server-side fetching (403) — cite the URL and
implement from the rules recorded above; do not skip a candidate just
because WebFetch is blocked. Recalibrate all starting parameters via
backtest; the numbers above are literature priors, not tuned values.
