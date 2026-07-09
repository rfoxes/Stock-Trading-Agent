# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

**NEXT RUN IS FRIDAY 2026-07-10, 3:30 PM PT** (30 min before the trader run). Markets OPEN Fri 7/10 (`market-status` → `next_open 2026-07-10T09:30 ET`). **SK Hynix ($29B ADR, ticker SKHY) LISTS ON NASDAQ 7/10 — PROMOTE IT ON ITS DEBUT** (memory cohort, technology; priced $149/ADR on 7/9).

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (Thu 2026-07-09, canonical post-close 15:40 PT run). A **risk-on, event-rich day**: marquee = **Micron's $250B+ US investment through 2035** (up from $200B; NY campus, Boise ID fab #2, Manassas VA, +$3B TX wafers; 40%-US-DRAM goal; MU +8%) anchoring the **memory supercycle** (SK Hynix $29B ADR 7x oversubscribed → lists 7/10 as SKHY; WDC sympathy lift; ARM +11% pre-print). Held **META** got a *positive* capex event (first Canadian data center + Muse Image + 14GW compute). **Macro turned risk-on:** CENTCOM confirmed **fresh US strikes on Iran**, but oil **fell** and equities **rose** (Nasdaq +1.30%, S&P +0.81%, SMH +2.5%) — yesterday's oil spike unwound. **NOT halt-worthy:** no FOMC decision; held-name event was positive; equities gapped **up** not down.
- **UNIVERSE GREW 30 → 31 under Tier-0.** Promoted **WULF** (TeraWulf — Anthropic $19B 20-yr AI-datacenter lease, Tier-B #5 anchor-customer win, technology). Lands **UNCLAIMED** → trader mandatory-attach triage assigns `equity_watch_only` or a validated strategy.
- **Held book:** universe `by_source` now shows **positions = META only** → consistent with the 7/8 handoff's predicted AVGO/MU/ORCL `equity_event_driven_catalyst` exits filling at the 7/9 open. Trader reconciles via `log-closed` (not the news agent's job). **MU's $250B capex catalyst post-dates its time-stop exit** — flagged as positive context only.
- **Interpreter:** bare `python3` STILL **BROKEN** (Homebrew 3.14.5, no deps). Entire run used the venv. **Use `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` and run from repo root before EVERY CLI call.** Operator action still required (open questions).
- **Pre-promotion state:** `list-active` → universe 30, claimed 30, **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)**, all `revalidate_by 2026-07-21`. `gap-registry coverage_holes` = **empty** (confirmed again). Research validated SMCI/RKLB/IRDM/BE on 7/8 (provisional 7 → 3). Post-promotion universe = 31 (WULF unclaimed).
- **Alpaca density: 168 items** (vs 106 on 7/8). NVDA 25, MU 17, SPCX 17, MSFT 12, AAPL/AMZN/META/TSLA 10, AVGO/QQQ 7, GOOGL 6, DELL/INTC 5, JPM/ORCL 4, SPY/TSM 3, ARM/CBRS/MRVL/SMCI/SNDK 2, BE/QCOM/RKLB 1; CSCO/HPE/IRDM/NUVL/SYNA 0. All 6 category HTMLs + daily summary written. `news-cleanup` → 0 deleted.
- **Brief pipeline FRESH today** (dated 2026-07-09). Prior: 7/8 fresh, 7/7 fresh, 7/6 fresh, 7/3 holiday fresh; earlier misses 6/22, 6/25, 6/29. Staleness-guard ask still stands (open questions).

## Notable carry-forwards

- **MU — $250B US investment through 2035 (NEW, capital allocation).** NY campus centerpiece, Boise ID fab #2, Manassas VA, +$3B TX supply chain; 40%-US-DRAM goal. Positive catalyst that post-dates the time-stop exit. No responder (capex-window library gap). Watch for follow-through / analyst reaction.
- **MEMORY COHORT — still the live story; SK Hynix listing is the near-term event.** (1) MU $250B confirms the up-cycle; (2) **SK Hynix (SKHY) lists 7/10** ($29B ADR, 7x oversubscribed, priced $149) = funding-rotation + promotable; (3) China CXMT threat (carry) + WDC/SNDK read-through. Sustain-check: does SKHY debut strong or "wonky" (Cramer's pricing warning)?
- **META (held) — first Canadian data center groundbreaking + Muse Image + 14GW compute (NEW, capex/product).** Rides its MACD rule. Positive AI-buildout event.
- **TSLA — NHTSA AV first-responder warning (NEW regulatory, fixes due end-July; also GOOGL/AMZN/UBER) + Model Y China #1 June.** Q2 earnings 7/22. No regulatory responder.
- **MSFT — in-house AI vendor swap (dropping OpenAI/Anthropic in Excel/Outlook) + OpenAI "ChatGPT Work" agent (NEW, product/vendor).** No product responder.
- **ARM — +11% pre-print into confirmed 7/23 earnings.** Earnings-window assignment gap (claimed by breakout, not event_driven). IV building.
- **RKLB / IRDM — $8B Iridium deal + $3.6B bridge loan digestion (follow-through).** RKLB (acquirer) climbing; IRDM (target) quiet (0 items). Merger-arb activation gap (pairs claims only SYNA).
- **BE — management escalated Hunterbrook short-report rebuttal, shares rallied.** Thesis contested, not confirmed. Track whether the short escalates or fades.
- **JPM — Q2 earnings Tue 7/14, window OPEN, most urgent** (opens bank season; same day as CPI + Warsh testimony). $50B buyback effective 7/1. Earnings-window assignment gap.
- **INTC 7/23, TSLA 7/22, AMZN 7/30 earnings** — IV builds; earnings-window assignment gap (all non-event_driven claims).
- **SPCX (PROVISIONAL/quarantined) — no new hard event; index-flow noise (Grantham/Chanos bearish, JPM Tesla-merger currency, Grok 4.5, Blue Origin $10B raise, BlackRock QQQ-challenger ETF).** Stays non-tradable. FCC 100k-sat vote 7/22 carry.
- **Vol regime — VIX 16.9 (benign, contango) BUT tech single-name vol at 23-yr high** (Nasdaq options price bigger swings than S&P). Vol in single-name dispersion + event-IV into the earnings cluster + SKHY listing.
- **Macro/geopolitics — fresh US-Iran strikes but oil FELL / equities ROSE (contained); jobless claims 215k; China CPI 1.0%; June CPI + Warsh testimony + JPM all 7/14.**

## To do on the next run (Fri 2026-07-10)

1. **Run the standard workflow** (`news_manual.md §"Workflow"`). **Re-read §9 every run.** Tier 0 (promote EVERY US-tradable news-subject on first appearance — uncapped; watch attach harmless) is the primary inclusion rule; Tier A (recurrence) is a prioritization hint; Tier B still applies. All require `--sector` (allowed: communication_services, consumer_discretionary, consumer_staples, crypto, energy, financials, healthcare, index, industrials, materials, real_estate, technology, utilities).
2. **USE `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` AND run from the repo root** for EVERY CLI call.
3. **PROMOTE SK Hynix (SKHY) ON ITS 7/10 DEBUT** — `promote-candidate SKHY --sector technology --agent news --reason "Tier-0 news-subject: $29B Nasdaq ADR debut 7/10, memory cohort"`. Ticker confirmed SKHY (priced $149/ADR 7/9). Confirm it's actually trading (Alpaca has it) before/after promoting; watch whether the debut is strong or "wonky."
4. **WULF triage-check** — confirm the trader attached watch_only (or validated) to WULF and it moved unclaimed → claimed. Watch WULF follow-through (Anthropic-lease momentum / any Abernathy-JV-sale detail).
5. **Iran follow-through** — did the fresh strikes widen overnight, or did the risk-on read hold? Check the 7/10 futures gap / oil. Most likely item to shift the halt-worthy call if it escalates (today it de-escalated in market terms).
6. **Memory sustain-check** — SKHY debut reaction; MU $250B follow-through; WDC/SNDK/ARM cohort; China CXMT (carry).
7. **Confirm universe = 31 / provisional 3 (QCOM, SPCX, SYNA).** Check WULF claim status.
8. **Earnings run-up** — JPM 7/14 (most urgent; + CPI + Warsh same day), ARM/INTC 7/23, TSLA 7/22, AMZN 7/30. Log event-IV; ARM saw the cleanest pre-print flow today.
9. **Vol regime** — VIX vs ~16.9; tech single-name dispersion (23-yr high) vs benign index; event-IV into JPM 7/14. Log concrete UOA on universe names only (today's whale-alerts were scan rollups; ARM pre-print buying was the cleanest single-name read).
10. **Outlier movers + sector breakdown.** Generic gainers/losers query STILL screen-level — per-name reconstruction from Alpaca remains the workable path. Today's clean promote (WULF) done; SKHY carries to 7/10; ANET/LITE/NOK/WDC tracked (no clean single-name hard catalyst).
11. **Library gaps re-listing** (see brief): capital-allocation/capex-window (MU $250B, META 14GW — NEW); regulatory/agency (NHTSA AV NEW + EU DMA/SEC); earnings-window assignment (JPM 7/14, ARM/INTC/TSLA/AMZN); M&A-arb (RKLB/IRDM + SYNA/onsemi); product/vendor-strategy (MSFT in-house AI, OpenAI ChatGPT Work, Grok 4.5); activist-short (BE); index-inclusion/forced-flow (SPCX + SKHY + BlackRock ETF; NEW_CATEGORY_NEEDED); vol-regime activation. Sat research = next.

## Open questions for the operator

- **[HIGH] Bare `python3` still broken.** Homebrew 3.14.5 lacks harness deps. Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13). Repoint the scheduled-task launcher + daily_news_prompt.md to the venv python (or pip-install requirements into 3.14). **daily_news_prompt.md line ~31 still says "There is no virtualenv" — stale, contradicts reality.** Also: the Bash shell cwd drifts between calls — always run from repo root.
- **[HIGH] News-agent schedule stability + brief-staleness guard.** Earlier misses 6/22, 6/25, 6/29; 6/30–7/9 fresh. Asks: (a) stabilize schedule / add a health-check alert on miss-or-double; (b) `_load_news_brief()` staleness guard — parses date_in_file but never compares to today; a stale brief should be rejected/down-weighted.
- **[MEDIUM] Trader off-schedule / double-fire (7/7 09:09 + 16:03, 7/8 16:03 + 16:51).** Confirmed recurring on order-submitting days per the 7/8 handoff double-fire addendum — the single-trigger config MUST be fixed before a double-fire lands where the 2nd run could act twice. This news run fired once, correctly (post-close ~15:40 PT).
- **[MEDIUM] Fallback-threshold question (carry).** A Sharpe-0.0-from-0-trades backtest attaches a below-baseline *trading* provisional rather than routing to `equity_watch_only` (bit SMCI/RKLB/IRDM/BE on 7/8; research since validated them). Should a degenerate 0-trade score count as "rankable" or "no signal → watch_only"? Affects WULF's grade label if its backtest is degenerate.
- **Index-inclusion as a 6th Tier-B trigger? — recurring (SPCX 7/7-7/9; SK Hynix 7/10; BlackRock ETF war 7/9).** Forced-flow gap keeps recurring.
- **Earnings-window assignment — JPM (7/14, most urgent), ARM (7/23), TSLA (7/22), INTC (7/23), AMZN (7/30).** Earnings-window responder (`equity_event_driven_catalyst`/`long_straddle_earnings`) doesn't claim these. Sat: assign.
- **New event-window sub-triggers (recurring) — capital-allocation/capex (MU $250B, META 14GW, NEW), regulatory/agency (NHTSA AV NEW + EU DMA/SEC), product/vendor (MSFT in-house AI/OpenAI/Grok), activist-short (BE).** No rule reads any of these.
- **M&A-arb activation — RKLB (acquirer)/IRDM (target $54/sh) + SYNA/onsemi.** `equity_pairs_trading_cointegration` claims only SYNA. Sat: activate merger-arb on IRDM/RKLB/SYNA.
- **Provisional claim-REASON prose drift (carry).** The 7/7 reset re-stamped some claim reasons to PROVISIONAL/QUARANTINED while only QCOM/SPCX/SYNA are actually quarantined (structured `provisional_claims`). Reconcile via re-triage, not a hand-edit.
- **SPCX past its (reset) 7/21 revalidate deadline path.** Nasdaq-100 member + FCC 100k-sat filing while quarantined. Operator: expedited validation for an index-add forced-flow name, or accept it stays non-tradable?
- **`cli open-orders` parser bug (LIVE-ORDER-SPECIFIC).** `'dict' object has no attribute 'id'` when a live open order exists; clean when none. (Not re-checked this run — news agent doesn't pull broker state.)
- **git-sync LaunchAgent.** Verify `launchctl list | grep harness` if markers accumulate in `.git-sync-queue/`.
- **NUVL biotech-vs-tech-universe mismatch (carry).** Provisionally trend-following; Sat owns proper claim.
- **Tier-0 volume pace (carry).** 7/8 promoted 4 (SMCI/RKLB/IRDM/BE); 7/9 promoted 1 (WULF). Pace acceptable so far — flagging in case rich M&A/product days accelerate universe growth.

## Operational notes

- `cli news-fetch --lookback-hours 24` returned **168 items** cleanly (via venv). CSCO/HPE/IRDM/NUVL/SYNA 0.
- `cli market-status` → `is_open: false`, **`next_open_iso: 2026-07-10T09:30:00-04:00`**, `now_iso: 2026-07-09T15:40 PT` (canonical post-close run).
- `cli list-active` (pre-promotion) → universe 30, claimed 30, **unclaimed 0**, provisional 3 (QCOM, SPCX, SYNA, all `revalidate_by 2026-07-21`). `gap-registry coverage_holes` empty. Post-promotion universe 31 (WULF unclaimed).
- WebSearch strong Thu: Micron $250B US investment through 2035 (Bloomberg/Reuters/GuruFocus); SK Hynix ADR priced $149, lists 7/10 as SKHY, 7x oversubscribed, $29B (CNBC/Yahoo/ThinkMarkets); Iran fresh US strikes but oil fell / stocks rose — Nasdaq +1.30% S&P +0.81% (CNBC/Schwab/Globe&Mail); VIX 16.90; TeraWulf/Anthropic $19B 20-yr Kentucky lease (DCD/CNBC/Coindesk, announced 7/6); jobless claims 215k; China CPI 1.0%.
- WebSearch weak: generic "biggest gainers/losers" still screen-level. Per-name reconstruction from Alpaca is the workable path.
- **Promotion analysis (`news_manual.md §9`):**
  - **Tier 0 (news-subject inclusion, uncapped):** Promoted **WULF** (own coverage line + confirmed Tier-1 anchor-customer catalyst + US-tradable + in-theme AI-infra). SK Hynix (SKHY) is a materially-reported news-subject but NOT yet US-tradable (lists 7/10) → carried, not promoted. Foreign/not-tradable subjects (Blue Origin private, Luxshare HK) tracked. Sympathy/price-only (WDC, ANET, LITE, DELL PT-raise) dropped from promotion. NOK (defense partnership) judged tangential/foreign → tracked.
  - **Tier B:** WULF satisfies #5 (Tier-1 customer-win — Anthropic $19B 20-yr lease). No other candidate met a Tier-B trigger today.
  - **Decision: 1 promotion (WULF, Tier-0/Tier-B #5). Universe 30 → 31.**
- **`gap-registry coverage_holes` empty (confirmed)** — all gaps are activation/assignment/taxonomy, not registry holes.
- Previous notes (still held): "CPI/PCE/import-price <month> <year>" query format works; per-name reconstruction beats generic gainers/losers; major-M&A → target per-name search is cleanest.
