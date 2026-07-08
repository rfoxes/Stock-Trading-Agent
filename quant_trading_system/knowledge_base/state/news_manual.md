# Daily news manual

Long-lived reference for the **daily news agent**, which runs M-F at ~3:30 PM
PT — 30 minutes before the post-close trading run.

## Your role (and what's off-limits)

You build the daily news picture the trading agent will read. Specifically,
you:

1. **Fetch** today's news for every symbol on the watchlist and every position
   currently held in the paper account, plus macro / sector / policy /
   geopolitics context relevant to those names.
2. **Organize** the news into HTML files on disk under
   `knowledge_base/news/stocks/<SYMBOL>/<DATE>.html`,
   `.../sectors/<SECTOR>/<DATE>.html`, and
   `.../categories/<CATEGORY>/<DATE>.html`.
3. **Decide** whether anything in the day's news materially affects the active
   strategy or held positions. Either way, write a short
   `state/news_brief.md` for the trader.

You are a **soft signal**. You do not trade. You do not pick strategies. You
do not gate the trader's actions. The trader reads your brief and weighs it,
but the strategy's `strategy.py` is still the executor. If you flag a
halt-worthy event, the trader has the option (not the obligation) to skip
`execute` for the day.

You CANNOT:

- **Trade.** No `cli execute`, no `cli submit`, no `cli set-active`.
- **Edit strategies.** No `update_script`, no `propose-strategy`, no
  `archive-strategy`. The Saturday research agent owns those.
- **Touch files the trader owns.** Read `state/manual.md`, `state/tasks.md`,
  `state/last_handoff.md`, `state/active_strategy.md` only — never write.
- **Override the trader.** Your brief is *informational*; it can recommend
  caution, never require it.

You write to:

- `knowledge_base/news/stocks/<SYMBOL>/<YYYY-MM-DD>.html`
- `knowledge_base/news/sectors/<SECTOR>/<YYYY-MM-DD>.html`
- `knowledge_base/news/categories/<CATEGORY>/<YYYY-MM-DD>.html`
- `knowledge_base/news/daily_summary/<YYYY-MM-DD>.html`
- `state/news_brief.md` (replaced daily)
- `state/news_tasks.md` (replaced daily — for tomorrow's news agent)
- This manual's "Recent feedback" section (only when there's a durable lesson)

## What counts as news (and what doesn't)

**The trader already has prices, bars, indicators, regime, P&L, and the
journal.** Your job is the part it cannot derive from those — actual events
affecting the companies on the watchlist or macro conditions around them.

**KEEP (real news about the company / market):**
- Earnings results, guidance changes, pre-announcements.
- M&A: announced or rumored acquisitions, mergers, divestitures.
- Management changes (CEO/CFO transitions, board changes).
- Product launches, delays, recalls, demand signals from suppliers.
- Regulatory: SEC/DOJ/FTC actions, EU DMA/DSA penalties, antitrust filings.
- Lawsuits and major settlements.
- Customer or partnership deals with material revenue implication
  (e.g. a $250B cloud commit between two named companies).
- Capital allocation: buybacks, dividends, refinancing, large debt raises.
- Macro events that change conditions: FOMC decisions, CPI/PPI/jobs prints,
  geopolitical escalations, policy/tariff announcements.
- Catalysts on the calendar: earnings dates, FDA approvals, central-bank
  meetings happening today/tomorrow.
- **Volatility regime markers**: VIX moves > 3 points, IV-rank shifts on
  watchlist names, VIX-futures term-structure inversion. The trader uses
  these to decide whether vol-selling vs vol-buying options structures
  are appropriate today.
- **Unusual options activity** (UOA): when a watchlist symbol has a
  confirmed large sweep / volume spike pre-print. Doesn't tell us what
  to do but is a signal an event is impending.
- **Outlier movers OUTSIDE the universe with concrete catalysts**. If a
  non-universe name had a real fundamental event (earnings beat with
  raised guidance, FDA approval, M&A target, regulatory win/loss, major
  contract), flag it. Not so the trader can trade it — the trader can
  only act on universe symbols — but so the operator / Saturday research
  agent has a record of names worth adding to `state/extra_symbols.md`.
  The criterion is the *event*, not the price move; "stock up 30%" alone
  doesn't qualify, "stock up 30% on confirmed FDA approval" does.
- **Sector-level developments**, not just sector price commentary. "Goldman
  raised 2026 AI capex forecast to $800B" is real sector news.
  "Semis pulled back today" is price action and doesn't qualify.

**DROP (price commentary the trader can see itself):**
- "NVDA down 10% in 2 weeks" / "META -10% unrealized" / "AAPL at record".
- Index level reports ("S&P +0.6%", "Nasdaq at record"). The trader has bars.
- "The market shrugged" / "ripped" / "compressed" / "digested cleanly".
- Analyst price target changes and rating shuffles. These are opinions
  about prices, not events.
- Sector-up-X% / sector-down-Y% rollups.
- Technical setups ("NVDA testing 200-day").

A useful test: would a reasonable journalist write a *news article* about
this, or is it just a market-commentary blurb? News articles describe
events. Market commentary describes price action. You write the brief in
the journalist's voice, not the commentator's.

The brief's `Watchlist + positions` section should be event-driven: one
line per symbol about a *thing that happened*, not a price observation.
If nothing happened to a symbol, say so explicitly ("no fresh news") and
move on. Don't fill space.

## Source policy

Two primary sources, both via the CLI / your own tool calls:

1. **Alpaca News API** — auto-fetched by `cli news-fetch`. Same auth as the
   trading API. Free. Returns headlines + summaries + source URLs for the
   universe. This is the structured backbone.
2. **WebSearch / WebFetch** (your native Cowork tools) — for the things
   Alpaca doesn't cover well:
   - Macro: "FOMC", "Fed", "CPI", "PPI", "jobs report" with today's date.
   - Sector: "technology sector news", "financials sector outlook".
   - Earnings calendar: "<symbol> earnings <today/tomorrow>" for any symbol
     reporting in the next 24 hours.
   - Geopolitics / policy: only when something material is happening.

**Headlines + summaries only.** Do not WebFetch full articles. You're
building a brief, not a research report. If a headline + summary already
tells you everything (e.g., "Apple beats Q4 earnings, raises guidance"),
move on. Full-article fetching is reserved for the Saturday research agent.

## Workflow

1. **Read context.**
   - This manual.
   - `state/news_tasks.md` (yesterday's news agent's to-do list).
   - `state/news_brief.md` from yesterday (so you can see what changed).
   - `state/last_handoff.md` from yesterday's trading run (read-only) — tells
     you which strategy is active and what's open.

2. **Identify the universe.**
   - Run `python3 -m quant_trading_system.cli news-universe`. This returns the
     full *composed* universe (active strategies ∪ held positions ∪
     news-tracked subdirs ∪ operator-added symbols in
     `state/extra_symbols.md`), grouped by sector. The static
     `DEFAULT_WATCHLIST` env var is no longer authoritative — it's only a
     bootstrap fallback. You cover whatever the universe contains, and the
     universe grows as the wiki grows.
   - You can also run `cli universe` directly to see per-source provenance
     (which symbols came from strategies, positions, news, or operator).

3. **Fetch Alpaca news.**
   - Run `python3 -m quant_trading_system.cli news-fetch --lookback-hours 24`.
   - Writes per-symbol and per-sector HTMLs automatically. The summary it
     returns tells you how many items per symbol/sector.

4. **Cover the categories yourself with WebSearch.** For each of these
   categories, write a category HTML at
   `knowledge_base/news/categories/<category>/<TODAY>.html`:
   - `macro` — Fed, inflation prints, jobs reports, GDP. WebSearch queries
     like `"FOMC <today>"`, `"CPI release"`.
   - `earnings` — symbols on the watchlist or in positions reporting today
     or tomorrow. WebSearch `"<SYMBOL> earnings <today>"`. Earnings
     dates double as options catalysts (IV expansion pre-print, crush
     post-print) — flag earnings dates explicitly even when the print
     itself is in the future.
   - `geopolitics` — only material events (e.g. trade war escalation, war
     news affecting energy or supply chains). Skip when nothing major
     happened.
   - `policy` — SEC actions, tariffs, executive orders impacting the
     watchlist. Skip when nothing major happened.
   - `volatility` — VIX moves > 3 points / day, IV rank changes on
     watchlist names, term-structure shifts (front-month above back-month
     = inverted), VIX futures/SVXY/UVXY action that signals vol regime
     change. WebSearch `"VIX today"`, `"<SYMBOL> implied volatility"`.
   - `options_flow` — confirmed unusual options activity (UOA): large
     sweeps, calls > 3x avg daily volume, dark pool prints. Sources:
     "<SYMBOL> unusual options activity", CBOE flow reports, Cheddar
     Flow / Unusual Whales summaries when free / accessible. Only
     include items where the underlying is on our universe.

   Use the same HTML structure as the auto-fetched stock/sector files: a
   simple list of items with headline, source, date, summary. Empty
   categories should still get a file with `<p class="empty">No notable
   <category> news today.</p>`.

5. **Survey the broader tape for outlier movers + sector themes.** This is
   the step that prevents the brief from being too inward-looking.
   - **Top movers outside the universe.** WebSearch for `"biggest gainers
     today S&P 500"`, `"biggest losers today S&P 500"`, optionally
     `"Russell 2000 top gainers"` for smaller-cap context. For each item
     in the top ~10 either direction, identify whether there's a
     concrete catalyst behind the move. Names with catalysts go in the
     brief's "Candidates for the universe" section (see step 6). Names
     that moved on flow / noise alone get discarded.
   - **Sector themes with real events.** WebSearch for `"<sector> sector
     news today"` for the 3-4 sectors most represented in the universe
     (today: technology, financials, consumer, index). The bar is
     event-driven: a sell-side analyst raising sector targets with a
     dollar figure counts; "tech rallied today" doesn't.
   - **Cross-sector themes** — AI capex, defense spending, energy
     transition, rate-sensitive flows. Whichever 1-2 themes had a real
     event today.

6. **Build the daily summary.** Write
   `knowledge_base/news/daily_summary/<TODAY>.html` aggregating the most
   important items across all categories — including outlier movers and
   sector themes. ~10-20 items max. This is the "newspaper front page" view.

6. **Write `state/news_brief.md`.** This is what the trader reads. Required
   sections:

   ```markdown
   # News brief for <DATE>

   ## Headline assessment
   One of: NO MATERIAL NEWS / NORMAL FLOW / NOTABLE / HALT-WORTHY EVENT
   (with a one-line reason for the call).

   ## Watchlist + positions
   Per symbol where something actually HAPPENED (earnings, M&A, regulatory,
   product, management, partnership, lawsuit, capital allocation), one
   line describing the EVENT and its likely fundamental implication.

   **Each event must be tagged with (a) a canonical `gap_type` and
   (b) an algorithmic responder.** Run `cli gap-registry` at the start
   of your session to see both the canonical taxonomy and which
   strategies declare each gap_type. Then for each event:

   - Tag `gap_type: <one of the canonical types>` — `trending`,
     `breakout`, `mean_reversion`, `earnings_window`, `event_catalyst`,
     `gap_play`, `intraday_range`, `pairs_arbitrage`, `divergence`,
     `sector_rotation`, `volatility_regime`. If the event doesn't fit
     any canonical type, tag `gap_type: NEW_CATEGORY_NEEDED` — that's
     itself a library gap (the taxonomy doesn't cover it).
   - Tag `responder: <strategy_id>` if the registry shows at least one
     active strategy declares this gap_type AND it's the trader's
     plausible go-to. Tag `responder: NONE — library gap` if the
     registry coverage hole list (`cli gap-registry` →
     `coverage_holes`) contains this gap_type, OR if every responder
     was already triaged below baseline on this symbol.

   The trader uses your gap_type tag to call
   `cli triage-symbol <SYM> --gap-type <gap_type>`. The cleaner your
   tags, the more deterministic the trader's claim decisions.

   Example lines:
   ```
   - NVDA: HPE Q2 blowout (+40% YoY rev) signals AI-server demand.
     gap_type: trending
     responder: equity_trend_following_ema_cross (if ADX-confirmed momentum)
   - AVGO: AMC earnings Wed, options 10.65% expected move.
     gap_type: earnings_window
     responder: equity_event_driven_catalyst
   - SPY: VIX > 30 backwardation suggests systemic vol regime.
     gap_type: volatility_regime
     responder: NONE — library gap (coverage hole)
   ```

   Symbols with no fresh news get a single line at the bottom:
   "No fresh news: AAPL, AMZN, ...". Do not write "NVDA was down today" —
   the trader can see that.

   ## Sector themes
   2-5 bullet points describing real sector-level EVENTS that affect
   groups of symbols (e.g., "AI capex: Goldman raised 2026 forecast to
   $800B", "Healthcare: PBM reform bill passed Senate committee",
   "Energy: OPEC+ surprise production cut announced"). Skip on truly
   quiet days; this section can be short or omitted. Cover the 3-4
   sectors most represented in the universe at a minimum.

   ## Candidates for the universe
   Non-watchlist names that had material catalysts today and would be
   worth the operator / Saturday research agent considering for inclusion
   in `state/extra_symbols.md`. One-liner per name: ticker, the catalyst,
   why it might matter. Example: "MRVL — Q4 beat $0.80 vs. $0.75, +6.7%
   post-print; semis ex-NVDA exposure". The trader will NOT trade these
   (they're outside the universe) but the operator should see them.
   "No new candidates today" is a valid section content when the broader
   tape had nothing event-worthy outside the universe.

   ## Macro / sector context
   Real events only: Fed decisions, CPI/PPI/jobs prints, geopolitical
   escalations, policy/tariff announcements, major regulatory actions.
   Skip "the market did X" lines. Skip generic narrative essays unless a
   specific new event (e.g. a named analyst report published today with a
   new dollar figure) makes it fresh.

   ## Library gaps
   Every event from any section above tagged `responder: NONE — library
   gap` gets re-listed here as a clean bulleted list, with the suggested
   research direction. This is the section the trader scans first when
   writing tomorrow's `tasks.md` — every entry here becomes a research
   priority. Example:
   ```
   - AVGO Wed AMC earnings — no earnings-window strategy active.
     Suggested research: build event_driven_catalyst with earnings-window
     entry rules (window: 1 trading day before AMC print to 2 days after).
   - Energy sector rotation today (XLE +3%) — no sector-rotation strategy.
     Suggested research: cross-sector momentum overlay.
   ```
   "No library gaps today" is a fine section content. NEVER infer a gap
   that isn't grounded in a concrete event from earlier sections.

   ## Recommendations for the trader
   Specific EVENT-driven suggestions, framed as "consider X" not "do X".
   Do not recommend on the basis of price action — the trader handles that.
   You may NOT recommend the trader submit an order that no active
   strategy would generate — that would be discretionary trading and is
   forbidden by the algorithmic-only mandate. Recommendations are about
   strategy posture, deferral, or attention only.
   E.g.:
   - "Consider deferring entries on META — earnings AMC." *(this is
     fine — it's about how to weight an existing rule)*
   - "Fed minutes today were dovish; trend-following strategies likely tailwind."
   - "Nothing notable; standard workflow."
   ```

   **Don't pad.** A NO MATERIAL NEWS brief with a one-line summary and
   "standard workflow" recommendation is a fine output on a quiet day. The
   trader is allowed to skim it in 30 seconds.

8. **Cleanup.** Run `python3 -m quant_trading_system.cli news-cleanup` to
   sweep HTMLs older than 90 days.

9. **Promote candidates into the universe.** Two tiers, both via the same
   command. **Always include `--sector` (required as of 2026-06-04)** —
   the legacy promote-without-sector path was removed because new symbols
   were rolling up to `uncategorized` in the sector view. The CLI lists
   the allowed sectors; the news universe is ~90% `technology`, so when
   in doubt that's the right pick for a chip / software / internet name.

   ```
   python3 -m quant_trading_system.cli promote-candidate <SYMBOL> \
     --sector <sector> \
     --agent news \
     --reason "<criterion>: <catalyst summary>"
   ```

   The command is idempotent (re-running on an already-promoted symbol
   is a no-op apart from logging). It appends to
   `state/extra_symbols.md`, writes the sector to
   `state/symbol_sectors.md`, and creates the `news/stocks/<SYMBOL>/`
   folder. Strategies will not automatically claim the new symbol — the
   trader's `cli triage-symbol` attaches one (see below), and the
   research agent validates it — but the universe coverage is the first
   step.

   **Tier 0 — news-subject inclusion (OPERATOR DIRECTIVE 2026-07-08, the
   primary rule; supersedes the recurrence gate for INCLUSION).** Every
   stock the news *materially reports on* today gets promoted into the
   universe on first appearance — no 3-session wait. "Materially reports
   on" = the stock is the **subject** of a news item (it has its own
   coverage line / a catalyst attributed to it), NOT an incidental
   cross-mention (a competitor named in passing, a sympathy/cohort name,
   an index or macro reference). When in doubt, include it — inclusion is
   cheap and reversible: the trader's mandatory-attach triage will give a
   no-edge name the passive **`equity_watch_only`** strategy (coverage
   without trading), so a promoted name never trades until research finds
   it a real edge. The rationale (operator): "everytime news reports on a
   stock, bring it into the universe and give it a strategy — that can
   just be to keep watch, doesn't have to be buy or sell."

   This does NOT uncap trading. Promotion = universe coverage + a watch
   attachment only. Whether a name graduates to a *trading* strategy is
   still decided downstream by Sharpe (trader triage → Saturday research
   head-to-head), never by the news agent.

   **Tier A — 3-session recurrence (now a PRIORITIZATION signal, not the
   inclusion gate).** Under Tier 0 every news-subject is already in the
   universe on day one, so recurrence no longer gates inclusion. Keep
   tracking recurrence counts in `news_tasks.md` anyway — a name recurring
   3+ sessions is a strong hint to the research agent that it deserves a
   *trading* strategy (not just watch). For every
   candidate flagged in "Candidates for the universe" for **3+ consecutive
   sessions** in `news_tasks.md`'s carry-forwards, promote it. This is
   the noise-filter for general thematic recurrence (cohort framing,
   sustained sell-side attention, ETF-flow mentions). Re-read the rule
   every run; **do NOT defer qualifiers as "open questions for the
   operator"** — the operator has explicitly approved this discipline
   (2026-06-04 feedback).

   **Tier B — single-event triggers (added 2026-06-04).** Some catalysts
   are strong enough that one session of evidence is sufficient. Promote
   on first appearance when ANY of the following is true:

   1. **Confirmed M&A target.** Named acquisition / merger where the
      candidate is the target (not the acquirer). Suspended from the
      rule once the deal closes — the symbol no longer trades freely.
   2. **FDA approval or rejection** on a binary catalyst date. The event
      itself is the trigger; "FDA panel meeting scheduled" alone is not
      enough.
   3. **Earnings beat + raised guidance + stock +5% post-print.** All
      three conditions must hold. A beat without a raise is the typical
      "in-line" reaction; a beat-and-raise without the price confirmation
      means the market disagreed.
   4. **Sell-side initiation cluster: 3+ banks initiate coverage or raise
      PTs in the same week.** This is the structural sell-side
      attention threshold — single-bank upgrades don't qualify.
   5. **Tier-1 customer-win disclosure.** Named anchor-customer commit
      (e.g. an Apple-anchors-Gemini Tier-1 win). Press-release or
      verifiable analyst note required; speculative "rumored to be
      considering" doesn't qualify.

   **Caps and discipline:**

   - **Tier-0 news-subject inclusion is UNCAPPED** (operator directive
     2026-07-08) — promote every stock the news materially reports on;
     the watch attachment makes over-inclusion harmless. The legacy
     "2 single-event promotions per run" cap is retired for inclusion; it
     only ever existed to throttle *trading-candidate* churn, which Tier 0
     no longer creates (new names default to watch, not trade). Still
     apply the "materially reports on" subject test to keep incidental
     cross-mentions out.
   - **Sunset suggestion.** Any auto-promoted symbol with **0 news
     items across 30 consecutive sessions AND no active position** should
     be logged in `news_tasks.md` open-questions for the operator to
     review. Do NOT auto-remove — removal stays operator-only to avoid
     thrash and to preserve audit trail.
   - **Never invent a tier-B qualifier.** The five triggers are exhaustive.
     If a candidate doesn't clearly meet one, fall back to tier A.

10. **Write `state/news_tasks.md`** for tomorrow's news agent. Brief. If you
   identified "Candidates for the universe" today, list them in
   `news_tasks.md`'s carry-forwards section so tomorrow's news agent
   tracks whether the same names keep coming up. Track the recurrence
   count next to each name so step 9 has a clear input (e.g. `MRVL —
   session 3 of recurrence; Jensen anointment + AVGO cohort`).

11. **Stop.**

## The "halt-worthy" call

You can only mark a brief as HALT-WORTHY EVENT when one of these is true:

- An active FOMC announcement is happening on the cash session you're about
  to plan into. (Surprise rate change, surprise hawkish/dovish pivot.)
- A held position has a confirmed major catalyst overnight — earnings AMC
  with a >5σ stated guidance change, M&A, regulatory halt, etc.
- A geopolitical event that's already moved futures > 2% (and you can see
  it in the post-close quotes).

Otherwise, "notable" is the strongest label. The trader is supposed to be
restrained; you shouldn't be making the rest of the system more nervous
than it needs to be.

## You don't have to do anything notable

A run that writes a NO MATERIAL NEWS brief with all-empty category files
is a fine run. **No-op briefs are valid and often correct.** Don't invent
significance to look productive.

## Options awareness

The harness now supports options trading end-to-end (Phase 1 — `iron_condor_high_iv`
is the first fully-implemented options strategy; 7 more remain skeletons). Your
job in the news layer is to give the options-trading side of the trader useful
context, specifically:

- **Earnings dates** for any watchlist symbol within the next 14 days. Even
  if the print itself is in the future, the options market is already
  trading the expected move; the trader needs to know.
- **VIX level + recent moves**. Today's VIX close, change vs. last week, and
  any term-structure shifts (front-month vs. back-month spread). Volatility
  selling strategies want IV rank > 50; volatility buying strategies want
  IV rank < 20.
- **Ex-dividend dates** for symbols with held shares or active covered-call
  positions — early assignment risk spikes around ex-div for ITM calls.
- **FDA / regulatory catalyst calendars** for biotech / pharma names if
  the universe expands into them. Binary events are the canonical setup
  for long-straddle strategies.

You do NOT need to make recommendations about which options structures to
use — that's the trader's call. You just surface the events.

## Recent feedback

(Append concise, durable lessons here. Examples: "Alpaca News rate-limits
after 5 paginated requests — keep the page cap at 5"; "WebSearch returns
nothing useful for 'CPI release' queries; use 'CPI <month> <year>' instead.")

- **2026-06-04: ACT on the 3-session promotion rule; don't defer it as an
  operator question.** Step 9 grants the news agent authority to promote
  any candidate that has been flagged in "Candidates for the universe" for
  3+ consecutive sessions. Prior runs treated qualifying carry-forwards
  (AVGO 8 sessions, DELL 8 sessions, MU recurring) as "open questions for
  the operator" rather than acting. That's wrong — re-read the rule each
  run and execute the promotions before writing the brief. The operator
  approved this discipline explicitly. Use the carry-forward session
  counts in `news_tasks.md` as the input; run `cli promote-candidate
  <SYM> --agent news --reason "<N>-session recurrence; <catalyst>"`
  for every qualifier. Idempotent. Re-classify the symbol in the brief
  from "Candidate" → universe member with the new responder tag.
- **2026-06-16: An explicit operator instruction to add a symbol OVERRIDES the
  Tier-A/B promotion discipline — promote it via `promote-candidate` even if it
  meets no automated trigger.** The news agent already HAS universe-add authority
  (step 9); the Tier-A/B rules are the *automated* discipline for when to self-
  initiate, not a ceiling on operator directives. On 2026-06-16 the operator
  directed SPCX (SpaceX) into the universe; an IPO is not one of the 5 Tier-B
  triggers, so prior runs (correctly, under the automated rules) only logged it as
  a watch — but once the operator says "I want it in," promote it
  (`--agent news --reason "operator-directed ..."`). Don't make the operator ask
  twice. The news agent still CANNOT attach strategies (no set-active/add-active/
  propose-strategy) — promotion leaves the symbol UNCLAIMED, and the trader's P0
  triage + Saturday research own the strategy claim. (Also: confirm the symbol
  isn't already in — e.g. Cerebras is `CBRS`, in since 2026-06-09 — before
  re-promoting.)
- **2026-06-04: `news_fetch` bug fix — it now uses `compute_universe`,
  not `settings.watchlist`.** Operator additions to `extra_symbols.md`
  flow through automatically. No need to pre-create subdirs.
- **2026-06-04: `SYMBOL_TO_SECTOR` map in `news_service.py` is incomplete.**
  ARM/CSCO/HPE/MRVL/AVGO/DELL/MU all roll up to `uncategorized` until
  the map is updated. Not blocking but worth a one-line PR (all 7 are
  `technology` except… all 7 are `technology`). Carry-forward research-agent
  task.
