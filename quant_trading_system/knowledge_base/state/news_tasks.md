# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

## ⚡ OPERATOR DIRECTIVE (2026-07-19) — SHORT-TERM TRANSITION IS LIVE

The harness now hunts setups held days to a few weeks (~2-15 trading
days; swing, not day trading). **Read `news_manual.md` §"Short-term
reorientation" before this run.** Starting
with your next brief: (1) add the required `## Near-term catalyst
calendar` section (dated events 0-10 sessions out, sorted by date, each
with symbols, gap_type, responder, and a `horizon:` tag — template in
news_manual §Workflow step 6); (2) widen the `earnings` category to a
10-session forward window; (3) roll unexpired dated events into
news_tasks.md daily so the calendar pipeline carries forward. Everything
else (tagging, Tier-0 promotion, halt-worthy bar, no-op briefs valid) is
unchanged. A new prompt file (`daily_news_prompt_short_term.md`) exists
for the operator to paste into the scheduled task; until then this note +
the manual carry the directive. Keep this block until the operator
confirms the new prompt is pasted, then drop it.

**✅ FRESH, ON-TIME Thursday 2026-07-16 run** firing at the ~15:39 PT slot with 7/16 data (news-fetch stamped 7/16; quotes/WebSearch all 7/16). `market-status` at run: `is_open false`, `now 2026-07-16T15:39 PT`, `next_open 2026-07-17T09:30 ET`. Next trader run is post-close 7/16 ~4 PM PT; **next news run is Fri 7/17 ~3:30 PM PT.** Saturday research runs 7/18. **NFLX Q2 printed after the close tonight — check the result 7/17.**

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Thu 2026-07-16). **A genuine risk-off chip/semiconductor selloff — but orderly, NOT halt-worthy.** Tape flipped from Wed's calm-green to a broad tech de-rate: **Nasdaq -1.47%, S&P -0.51%, Dow -0.2%** (Dow held on UNH), **VIX +3.66% to 16.24**. Four threads: (1) **TSM Q2 "insanely good" — beat + raised outlook + 5th straight record profit — but SOLD OFF ~6%** on a capex hike to **$60-64B** (+$100B Arizona, $265B US total); dragged the whole chip complex (INTC/ARM/AMD/MRVL). (2) **GOOGL -4% on a reported Gemini 3.5 Pro launch DELAY** (discrete product event). (3) **AI-hardware/memory give-back extended a 4th session** — SNDK -40% from June peak (-25% wk), SMCI/DELL -6%, memory -3-8%, SOXX -13%/4wk. (4) **Iran/Hormuz 6th day** + rising oil/yields; gold <$4,000. Cutting the other way: **UNH Q2 blowout+raise lifted the Dow**, **AAPL record high** (China approval + Siri beta + reported AI-chip M&A intent), constructive macro (claims 208K, Philly Fed 41.4 soared, retail sales in line). **No HALT trigger:** no FOMC (7/28-29), META no adverse single-name shock (Meta-Compute push is not adverse; closed with the tape), Iran did NOT gap futures >2% (Nasdaq -1.47% << halt line).
- **UNIVERSE GREW 36 → 37 under Tier-0.** Promoted **UNH (UnitedHealth, healthcare)** — Tier-0 news-subject (Q2 blowout: adj EPS $6.38 vs $4.91, rev $112B, **raised FY26 guide to $19.50-20.00** from >$18.25; lifted the Dow) + clean Tier-B #3 beat-and-raise pattern. Chosen deliberately as a **diversifier** (healthcare near-empty ex-NUVL; NOT another crowded-AI name → sidesteps the proportionality concern). Lands **UNCLAIMED** → trader P0 triage (`triage-symbol UNH --gap-type earnings_window`; deep real history → expect rankable backtest / trading claim or below-baseline provisional, NOT watch_only).
- **Held book:** universe `by_source` still shows **positions = META only**. No reconcile for the news agent.
- **Interpreter:** bare `python3` STILL BROKEN (Homebrew 3.14.x, no harness deps). Use **`/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3`** from repo root before EVERY CLI call. (This run: all CLI calls ran clean from repo root via the venv.)
- **Pre/post-promotion state:** pre → universe 36, claimed 36, unclaimed 0, provisional 8. Post-UNH → **universe 37, claimed 36, unclaimed 1 (UNH), provisional 8 (unchanged)**. Provisionals: **GS 7/28, MS/PYPL 7/29, QCOM/SPCX/SYNA 7/21, SKHY 7/24, RIVN 7/27**. `gap-registry coverage_holes` **empty** (confirmed again). WULF is validated (`equity_rsi_divergence`) — don't relist.
- **Alpaca density: 186 items** (vs 161 on 7/15). TSM 18, SPCX 17, GOOGL 14, MSFT 13, AMZN 12, AAPL 11, META/NVDA/SNDK 9, MU/SKHY 7, INTC/QQQ/SPY 6, JPM 5, BE/RKLB 4, GS/MS 3, DELL/ORCL/PYPL/SMCI 2, ARM/AVGO/CBRS/CSCO/HPE/IRDM/MRVL 1; zeros: NUVL/QCOM/RIVN/SYNA/WULF. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline:** header dated 2026-07-16 (fresh, on-time). Prior: 7/15 (fresh), 7/14 (fresh), 7/13 (fresh), 7/10 (late-completed Fri data).

## Notable carry-forwards

- **AI-CAPEX-DOUBT is now the market's dominant tension — and it broadened from hardware to the FOUNDRY today.** TSM's beat-and-raise was buried by a $60-64B capex guide → the whole chip complex de-rated. Combined with the $182B Big-Tech AI-debt-spree story (CDS spreads for AMZN/GOOGL/MSFT reportedly doubled since 2025) and **ORCL's cash-burn-driven 52-wk low**, the narrative has tilted from "AI demand is limitless" to "who funds the buildout, at what margin." **7/17+ sustain-check:** does the de-rate extend or stabilize? Watch TSM follow-through post-capex, memory (MU/SNDK) stabilization, ORCL, and whether GOOGL's Gemini-delay wound reopens platform weakness.
- **GOOGL — Gemini 3.5 Pro DELAY (fresh, discrete).** Stock -4%. Watch for a revised launch date / competitive read (vs OpenAI/Anthropic). GOOGL Q2 also expected late-July (BofA sees ~70% cloud growth). Product-event gap (no responder).
- **AAPL — record high + reported AI-chip-company ACQUISITION intent (fresh).** M&A-intent + China-approval follow-through + new Siri AI beta. Watch for a named target or confirmed deal (would flip to Tier-B #1 for the target).
- **UNH (newly promoted, UNCLAIMED) — confirm the trader triaged it.** Expect `earnings_window`; deep real history → trading claim or below-baseline provisional (NOT watch_only). Track post-earnings drift + any guidance follow-through.
- **NFLX — Q2 printed AFTER close tonight (7/16).** NOT promoted on preview alone (print landed after this run). **7/17: log actuals vs consensus (EPS ~$0.79, rev ~$12.58B, ad rev ~doubling to $3B); promote if it's a beat-and-raise (Tier-B #3) or a clear news-subject.** NFLX -19% YTD into the print.
- **BLK / ASML — held Tier-0-eligible on 7/15, NEITHER recurred with a fresh hard catalyst on 7/16** (BLK only an analyst-PT rollup; ASML only prior-beat commentary). Per the plan, keep tracking; promote if they recur OR the operator confirms the aggressiveness level (proportionality open question, still unanswered).
- **ARM — -5% on an investment-firm downgrade** (valuation, ahead of 7/23 earnings). Recurring event-scale analyst-downgrade theme (DELL -13% 7/15, ARM/HSBC -6% 7/14). No analyst-shock responder (library gap). ARM earnings 7/23.
- **TSLA — federal investigators preliminarily CLEARED FSD in a fatal Texas crash** (legal de-risk; stock still slipped with tape). Q2 earnings 7/22. Watch final NHTSA finding + XPeng L4 challenge.
- **SKHY (PROVISIONAL/quarantined) — South Korea TRIPLED margin on leveraged SK Hynix/Samsung ETFs after 24 halts in 9 weeks** + Lucid 2x ETF delisted (NAV negative). Forced-flow / float-mechanics theme keeps recurring. Stays non-tradable.
- **SPCX (PROVISIONAL/quarantined) — Starship Flight 13 launched tonight (7/16)** with a Starlink V3 payload. **7/17: log the launch outcome.** Piper initiated SPCX/RKLB Neutral, ASTS Overweight; ARK bought $16.6M; near/below $135 IPO price. Stays non-tradable.
- **BE — short-seller allegations + supply-chain concerns despite a $1.7B AI-infra investment.** Discrete short-seller catalyst (library gap). BE on `equity_breakout_volume_confirmation`.
- **MS/PYPL/GS (financials provisionals) — quiet post-earnings; NO fresh catalysts 7/16.** PYPL: no Stripe/Advent deal development today (Tier-B #1 suspends if/when a deal closes). Track for developments; quarantine unchanged.
- **US-IRAN / HORMUZ (acute, 6th day).** More US strikes + reimposed blockade + tanker hit; oil/yields up but NO >2% equity gap. **7/17 checks:** overnight escalation? equity-futures >2% gap (halt line — NOT there)? oil follow-through + inflation read-through.
- **Earnings run: TSM 7/16 (done, sold off on capex), NFLX 7/16 AMC, TSLA 7/22, ARM/INTC 7/23, MSFT 7/29, AMZN 7/30, GOOGL late-July.** Event-IV building.
- **Vol regime — VIX 16.24 (+3.66%), ticked up.** Index calm; extreme single-name dispersion (SOXX -13%/4wk, SNDK -40%/peak). Dispersion regime; options skeletons not activated.

## To do on the next run (Fri 7/17)

1. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` from repo root.** Re-read `news_manual.md §9` (Tier 0 = promote every US-tradable news-subject on first appearance, uncapped; Tier A recurrence = prioritization; Tier B still applies; all require `--sector`).
2. **NFLX Q2 result (printed 7/16 AMC)** — log actuals vs consensus; **promote if beat-and-raise (Tier-B #3) or clear news-subject.** **SPCX Starship Flight 13 outcome** (launched tonight). **UNH follow-through** — confirm the trader triaged it (unclaimed → claimed/provisional; expect rankable, NOT watch_only).
3. **AI-capex-doubt / chip de-rate** — did TSM's capex selloff + memory de-rate + ORCL cash-burn extend or stabilize? GOOGL Gemini-delay follow-through (platform weakness?).
4. **AAPL** — any named AI-chip acquisition target / confirmed deal (would flip Tier-B #1 for the target). China rollout traction.
5. **US-Iran / Hormuz** — escalation check; oil follow-through; equity-futures gap (halt-worthy only if >2%).
6. **META (held)** — Meta-Compute AI-cloud traction; any adverse single-name development. Rides MACD.
7. **Confirm universe = 37 / claimed 36 (→ 37 after UNH triage) / provisional 8 (GS 7/28, MS/PYPL 7/29, QCOM/SPCX/SYNA 7/21, SKHY 7/24, RIVN 7/27).** WULF validated — don't relist.
8. **BLK / ASML** — promote if they recur with a fresh catalyst or the operator confirms (Tier-0-eligible, held 7/15 & 7/16). AMD — promote on a hard catalyst (still analyst-PT + selloff, no hard event).
9. **Vol regime** — VIX vs 16.24; event-IV into NFLX(done)/TSLA 7/22/ARM,INTC 7/23. Log concrete single-name UOA on universe names ONLY (today's whale alerts were scanner rollups again — IT/comm-svcs/industrials — not sized sweeps).
10. **Library gaps re-listing** (see brief): earnings-window assignment (**TSM printed & unresponded — live example**; UNH unclaimed; MSFT 7/29, TSLA 7/22, ARM/INTC 7/23, AMZN 7/30; GS/MS/PYPL/QCOM/RIVN quarantined); product/roadmap-event (GOOGL Gemini delay, AAPL M&A intent, TSLA FSD clearance); analyst/valuation-downgrade shock (ARM -5%); AI-capex/cash-burn re-rating + cohort reversal (TSM/ORCL/memory/servers); M&A-arb (PYPL, AAPL, RKLB/IRDM, SYNA/onsemi); short-seller allegation (BE); index/forced-flow + ETF/float (SKHY Korea margin, Lucid delist, SPCX); binary-launch (SPCX); geopolitical/energy-shock (Iran/oil); vol-regime/dispersion activation; tokenization/market-structure (DTCC carry).

## Open questions for the operator

- **[proportionality — RECURRING, still unanswered] How aggressively to apply UNCAPPED Tier-0?** 7/15 held BLK/ASML for proportionality and flagged; 7/16 promoted ONE name (UNH) chosen as a *diversifier* (healthcare, not another AI-cohort name) and again held BLK/ASML (neither recurred). Preferred posture: promote every hard-catalyst news-subject, or cap per-day / weight by thematic-diversification-vs-concentration? (Removal is operator-only, so I keep erring toward measured, diversifying promotions.)
- **[MEDIUM] Bare `python3` still broken.** Homebrew 3.14.x lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Repoint the launcher + prompt to the venv (or pip-install requirements into 3.14).
- **[MEDIUM] Trader schedule double-fire (7/7, 7/8).** 7/9–7/15 each fired once. Confirm the single-trigger config before a double-fire lands where the 2nd run could act twice.
- **[MEDIUM] News-brief staleness guard.** The 7/10-data-completed-late episode motivated a `_load_news_brief()` staleness check (parse date_in_file, reject/down-weight if >1 session old). Recent runs are fresh so it's not biting, but the guard is still unbuilt.
- **[MEDIUM] Fallback-threshold question (carry).** Degenerate 0-trade backtest attaches a below-baseline *trading* provisional rather than routing to `equity_watch_only` (GS/MS/PYPL/RIVN → trading provisional; SKHY/SPCX no-history → watch_only/trend provisional). UNH (promoted today) has deep history — another clean test of the "has-history → rankable" branch. Should a degenerate/empty backtest count as "rankable" or "no signal → watch_only"?
- **Index-inclusion / float-mechanics as a 6th Tier-B trigger? — recurring** (SKHY Korea ETF margin hike + 24 halts/9wks; Lucid 2x ETF delisted; SPCX sub-IPO leveraged ETFs). Forced-flow gap keeps recurring, now with a hard regulatory-intervention data point.
- **Product/roadmap + analyst-shock as event sub-triggers? — recurring & growing** (GOOGL Gemini delay, AAPL M&A intent, TSLA FSD clearance; ARM/DELL event-scale downgrades). No rule reads any of these.
- **Earnings-window assignment — TSM (printed 7/16, unresponded because on trend_following), UNH (unclaimed), MSFT/TSLA/ARM/INTC/AMZN upcoming, GS/MS/PYPL/QCOM/RIVN quarantined.** Earnings-window responders don't claim the names actually printing. Sat research: assign.
- **M&A-arb activation — PYPL (target, no dev today), AAPL (chip-acquisition intent), RKLB(acquirer)/IRDM(target), SYNA/onsemi.** `equity_pairs_trading_cointegration` claims only SYNA. Sat: activate merger-arb.
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists. (Not re-checked — news agent doesn't pull broker state.)
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate in `.git-sync-queue/`. (This run: queue assumed healthy — LaunchAgent keeping up on recent runs.)
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim. (UNH now adds a 2nd healthcare name.)
- **Sunset watch:** no universe symbol yet hit the 0-news-across-30-sessions + no-position sunset criterion; keep tracking (CBRS/IRDM/NUVL/QCOM/SYNA recurring zeros but recently added / claimed).

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **186 items** cleanly (via venv). Zeros: NUVL/QCOM/RIVN/SYNA/WULF.
- `cli market-status` at run start → `is_open false`, `now 2026-07-16T15:39 PT`, `next_open 2026-07-17T09:30 ET`. Fresh on-time Thursday run.
- `cli list-active` (pre-promotion) → universe 36, claimed 36, unclaimed 0, provisional 8. `gap-registry coverage_holes` empty. Post-promotion → universe 37, claimed 36, unclaimed 1 (UNH).
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier 0 (news-subject inclusion, uncapped):** Promoted **UNH** (dedicated front-page Q2 blowout + raised guidance; NYSE; deliberately a *diversifying* healthcare add, not another crowded-AI name). Also satisfies Tier-B #3 (beat + raise + up).
  - **HELD (Tier-0-eligible / recurring):** BLK, ASML (neither recurred with a fresh hard catalyst 7/16 — held per the 7/15 plan). AMD (analyst-PT + selloff, no hard event). NFLX (print landed after this run — promote 7/17 on the confirmed result if it qualifies).
  - **NOT promoted (analyst/spillover/off-theme):** J.B. Hunt (transport beat, off-theme), Lucid (EV/ETF-mechanics), Nebius/IREN/ASTS (single-bank init or sympathy).
  - **Decision: 1 promotion (UNH Tier-0). Universe 36 → 37.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PPI <month> <year>" query format works; per-name reconstruction beats generic gainers/losers (the "biggest gainers S&P 500" query returns Indian-market data — reconstruct from per-name Alpaca + a "biggest movers <date> catalyst" search); major-M&A → target per-name search is cleanest; headlines+summaries only (don't WebFetch full articles). VIX/ADR exact quotes can diverge across aggregators on a busy day — report "~level, regime" not false precision.
