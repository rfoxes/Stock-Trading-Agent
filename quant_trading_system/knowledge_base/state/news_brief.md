# News brief for 2026-07-10

> **⚠️ RUN-TIMING NOTE (read first).** This is the **Friday 2026-07-10** news run: it fired at the ~15:35 PT slot and **all data is 7/10** (news-fetch stamped 7/10; quotes, WebSearch close figures, VIX, and the SK Hynix debut are Friday facts). The session was **suspended over the weekend and only completed Monday 2026-07-13 ~09:52 PT** (market clock now `is_open true`, `next_open 2026-07-14`). Content was **not** re-dated to 7/13 — re-labeling Friday's data as Monday's would be false. **If a trader reads this on/after 7/13, treat it as a 1-session-old (Friday→Monday) brief and prefer a fresh 7/13 news run.** One confirmation gained from the late completion: **SKHY now quotes live on Alpaca** (regular-way trading began 7/13 as predicted; mid ~$156.5, bid/ask 151/162 thin early book), so the no-price-history caveat below is now easing. This is the schedule-stability / brief-staleness open issue (already logged HIGH) manifesting concretely.

## Headline assessment

**NOTABLE — event-rich but constructive and contained; NOT halt-worthy.** The marquee item is **SK Hynix's Nasdaq debut**: it raised **$26.5B — the largest US IPO ever by a foreign company** (surpassing Alibaba's $25B in 2014). ADRs priced $149 and opened ~$170 (+14%, indicated +17%); the chairman told CNBC "demand is enormous." The event is two-sided for our memory/semis cohort — it's **rotating liquidity within the complex** (AI-proximity winners like NVDA vs **Micron, "already cracking"** under IPO-drain pressure). The sole held name **META** caught a *fresh EU regulatory action* (DSA "addictive features" finding, fines up to 6% of revenue at risk) but **still closed up (~+6%)** on a leaked multi-year AI-hardware capex memo — the market favored the buildout over the regulatory tail. `market-status`: `is_open false`, `now 2026-07-10 15:35 PT`, `next_open 2026-07-13 09:30 ET` (**Monday** — no session 7/11–7/12) — canonical post-close run, single fire.

**None of the three HALT-WORTHY triggers fires:** (1) **no FOMC decision today** — the pivot is Tue 7/14 (June CPI + Warsh testimony + JPM); (2) the held-name (META) event was regulatory but *preliminary* and *not* a >5σ adverse catalyst — META closed **up**; (3) **no geopolitical >2% futures gap** — Middle East risk lingered only as backdrop, oil contained. 109 Alpaca items (META 14 / MU 12 / NVDA 11 / SPCX 10). **Universe grew 31 → 32: promoted SKHY** (SK Hynix; Tier-0 news-subject + standing operator/prior-agent directive). `list-active` (pre-SKHY): claimed 31/31, **unclaimed 0**, **provisional 4 (QCOM, SPCX, SYNA, WULF)**; `gap-registry coverage_holes` **empty**.

> **For the trader (P0 triage):** newly-promoted **SKHY** is in the universe but will be **UNCLAIMED**. Caveat: **SKHY has no Alpaca price history yet** — Friday 7/10 traded under a *temporary when-issued* line **SKHYV** (~$168–170); the **permanent SKHY ticker begins regular-way trading Monday 7/13** (your next session) and joins the Nasdaq Composite. Expect `triage-symbol SKHY --gap-type event_catalyst` to hit the **no-price-history path → provisional/quarantined** (SPCX-style) until enough regular-way bars accrue. That's expected and harmless per Tier-0 (watch attach only). Interim price ref: SKHYV ~$168–170 (+~14% over the $149 offer). Provisional 4 (QCOM/SPCX/SYNA/WULF) untouched by me.

> **On the held book:** universe still shows **positions = META only** (per the 7/9 reconciliation — AVGO/MU/ORCL closed). Soft-signal note: META had a **mixed** day — a preliminary EU DSA fine risk offset by a positive AI-capex memo; net it closed up. Its position rides its own MACD rule; I do not and cannot advise overriding an algorithmic exit.

## Watchlist + positions

Event-driven lines (a thing that *happened*), each tagged with a canonical `gap_type` + algorithmic responder. Price moves omitted — the trader has bars.

- **META (held): EU issued a preliminary DSA finding that Instagram/Facebook may breach digital rules over "addictive" engagement design — fines up to 6% of global annual revenue at risk.** Also: a leaked memo revealed multi-year AI-hardware spending deals (capex); Muse Spark 1.1 AI launched (Zuckerberg posted on X for the first time since 2023); in-house "Iris" chip **augments** (not replaces) NVDA/AMD. Regulatory tail + positive capex/product on the one held name; net the stock rose.
  - gap_type: event_catalyst (regulatory — plus capex/product)
  - responder: NONE — library gap (META claimed by `equity_momentum_macd_histogram` (trending); no regulatory or capex/product responder — position rides its MACD exit)
- **AAPL: sued OpenAI for trade-secret theft** — alleges OpenAI used job interviews to extract Apple hardware secrets (new lawsuit, filed after close).
  - gap_type: event_catalyst (litigation)
  - responder: NONE — library gap (AAPL claimed by `equity_trend_following_ema_cross`; no litigation responder)
- **MU: SK Hynix's $26.5B Nasdaq debut is draining AI-trade liquidity — MU "already cracking" under the rotation; + Commerce Sec. Lutnick pressuring Samsung/SK Hynix to build US fabs** (reshoring, MU-aligned; "Micron's CEO may not be happy"). MU's $250B US-capex plan (7/9) still circulating.
  - gap_type: event_catalyst (sector liquidity-rotation / IPO-drain; policy)
  - responder: NONE — library gap (MU claimed by `equity_event_driven_catalyst`, but the lot exited 7/9 on the time stop; no forced-flow / liquidity-rotation responder)
- **GOOGL: report that OpenAI/Google AI models reached Pentagon-blacklisted Chinese tech giants via overseas subsidiaries** — export-control / national-security concern.
  - gap_type: event_catalyst (regulatory / export-control)
  - responder: NONE — library gap (GOOGL claimed by `equity_trend_following_ema_cross`; no regulatory responder)
- **INTC: JPMorgan named INTC a highest-conviction Q3 short idea** (after INTC doubled YTD); Q2 earnings 7/23. (The short call is sell-side positioning, borderline opinion — logged as context, not a hard catalyst; the earnings date is the real event.)
  - gap_type: earnings_window (7/23) — plus event_catalyst (short thesis)
  - responder: NONE — library gap (INTC claimed by `equity_breakout_volume_confirmation`; earnings-window assignment gap; no short-thesis responder)
- **JPM: Q2 print Tuesday 7/14 (window OPEN, most urgent)** — bank-season opener, same day as June CPI + Warsh testimony. Est ~$5.61/sh on ~$49.56B rev; $50B buyback effective 7/1.
  - gap_type: earnings_window
  - responder: NONE — library gap (JPM claimed by `equity_trend_following_ema_cross`, not `equity_event_driven_catalyst` — assignment gap; most urgent)
- **TSLA: Q2 earnings 7/22**; today: "Ex-Elon" ETFs proposed (strip TSLA/SPCX from indexes — forced-flow theme) and global EV sales hit 2M in June (Europe +31%, NA/China down — demand signal). No fresh hard corporate event.
  - gap_type: earnings_window (7/22)
  - responder: NONE — library gap (TSLA claimed by `equity_trend_following_ema_cross`; earnings-window assignment gap)
- **RKLB: added to First Trust's new FSPC Space Economy ETF** (index/inclusion — mild); Starlink-cohort read-through. M&A follow-through (Iridium) quiet today.
  - gap_type: event_catalyst (ETF inclusion / forced-flow)
  - responder: NONE — library gap (RKLB claimed by `equity_breakout_volume_confirmation`; no inclusion responder)
- **BE: short-seller (Hunterbrook) pushback continues** — management still defending supply-chain credibility; thesis contested, not resolved. (Watched carry.)
  - gap_type: event_catalyst (activist short / controversy)
  - responder: NONE — library gap (BE claimed by `equity_breakout_volume_confirmation`; no short-report responder)
- **SPCX (PROVISIONAL / execution-quarantined): no new hard corporate catalyst** — SpaceX IPO aftermath (Musk now "first trillionaire"), China's first reusable-booster landing (competitive), Starlink 10 Gbps (product), new FSPC + Ex-Elon ETFs (forced-flow). Index/forced-flow noise persists.
  - gap_type: event_catalyst — index-inclusion / forced-flow, unmodeled → **NEW_CATEGORY_NEEDED (index_rebalance)**
  - responder: NONE — library gap (SPCX's trend-following claim is provisional/quarantined; no rule reads forced-flow / index mechanics)

**No fresh single-name news** (price/analyst/cohort only — nothing that *happened*): **AMZN** (Dan Loeb's Third Point trimmed AMZN 10% / exited BABA = a Q1 13F, not an event; Q2 earnings 7/30 carry), **NVDA** (AI-proximity winner + ARK "AMD more performant per dollar" opinion — cohort), **AVGO** (whale-scan + tariff cross-tag; lot exited 7/9), **MSFT** (Warsh AI-task-force names Xbox's Asha Sharma — see Macro; no fresh corporate event), **WULF** (only a crypto-cohort roundup; no Anthropic-lease follow-through — stays provisional/quarantined), **DELL / TSM / ORCL / SNDK** (memory/semis cohort read-through), **ARM** (rotation/price; earnings 7/23), **CBRS / CSCO / HPE / IRDM / MRVL / NUVL** (0 items), **QCOM / SYNA** (0 items; provisional).

## Sector themes

- **Memory / AI-proximity split — the day's dominant structural event.** SK Hynix's **$26.5B** Nasdaq debut (largest-ever foreign US IPO, +14–17% pop) is rotating liquidity *within* the complex: AI-proximity winners (NVDA, SK Hynix) vs pressured (MU "already cracking"). "The semiconductor sector is splitting into winners and losers based on AI proximity." This is a **liquidity-drain / forced-flow event**, not just price action. SK Hynix joins the Nasdaq Composite Monday.
- **AI-datacenter capex intact.** Meta's leaked multi-year AI-hardware spend memo + 14GW (carry); Micron's $250B (carry); record $7.1B semiconductor-ETF inflow earlier in the week. Multi-node buildout (compute/memory/power) continues.
- **Regulatory pressure broadening across Big Tech.** EU DSA "addictive features" action on **META** (up to 6% of revenue); **AAPL v. OpenAI** trade-secret lawsuit; a report of US AI models reaching blacklisted Chinese firms (**GOOGL**). The legal/regulatory tail is thickening across the mega-caps simultaneously.
- **Index / forced-flow mechanics keep recurring.** SK Hynix → Nasdaq Composite Monday; new "Ex-Elon" ETFs (strip TSLA/SPCX); First Trust FSPC Space Economy ETF (RKLB); leveraged single-stock SK Hynix ETFs launched. Passive-flow theme, still unmodeled.
- **Vol regime — benign index, event-IV building.** VIX ~15.84 (down ~6.3%, contango). Vol concentrated in the SK Hynix listing + event-IV into the 7/14 CPI/Warsh/JPM cluster and the 7/22–30 earnings run — not the index.

## Candidates for the universe

**PROMOTED today (universe 31 → 32):**
- **SKHY (SK Hynix, technology)** — $26.5B Nasdaq ADR debut, the **largest-ever US IPO by a foreign company**; priced $149, opened ~$170 (+14%). Strong debut (chairman: "demand is enormous"), *not* "wonky." Tier-0 news-subject (own marquee coverage) + the standing operator/prior-agent directive to promote on debut. **Caveat: promoted under the permanent ticker SKHY, which begins regular-way trading Monday 7/13** — Friday's when-issued line was **SKHYV** (~$168–170). SKHY has **no Alpaca price history until 7/13**, so it lands unclaimed and will triage to no-price-history provisional/quarantined until bars accrue. Memory cohort.

**Tracking (NOT promoted — foreign / no clean US-tradable single-name catalyst):**
- **Samsung** — Lutnick reshoring pressure; foreign (KRX). Track.
- **WDC (Western Digital)** — memory sympathy on the SK Hynix/Micron rotation; no WDC-specific event. Track (recurring memory-cohort).
- **AMD** — ARK "more performant per dollar than NVDA" (opinion, cohort). Track.
- **DAL (Delta)** — Q2 beat, season opener; outside the AI/semis core. Track only.
- **CRCL / cryptobank** — US cryptobank approval; outside the equity universe. Track (crypto-policy, WULF-adjacent).

## Macro / sector context

- **No US macro print today (Fri 7/10).** The week's pivot is **Tue 7/14**: **June CPI** (headline forecast eased to ~3.9% YoY; core ~2.9%) lands 90 minutes before **Fed Chair Warsh's semi-annual testimony** (House Tue, Senate Wed) — the last inflation read before the **7/28–29 FOMC**. **June PPI + Empire State Wed 7/15**; retail sales Thu. Fed funds 3.50–3.75%; June minutes (7/8) were hawkish (nine hawkish dots).
- **Policy:** Commerce Sec. **Lutnick** told Samsung/SK Hynix they have "no choice" but to build US AI-memory fabs (reshoring, MU-aligned); **Trump** deferred aircraft tariffs after a security review (6-month clock); the US **approved a cryptobank**; **Fed Chair Warsh launched an AI task force** (Marc Andreessen + Xbox CEO Asha Sharma) to study AI's macro impact.
- **Geopolitics:** Middle East risk lingered as a backdrop but **no fresh escalation** moved markets; oil contained. The 7/9 US-Iran strikes remain the last hard item and were treated as contained.
- **Vol:** VIX ~15.84 (benign, contango); single-name tech dispersion elevated (carry). Vol is event/name-driven, not index-driven.

## Library gaps

`gap-registry coverage_holes` is **empty** — every item below is an **activation / assignment / taxonomy** gap (a rule/event-type isn't mapped), not a registry hole. Re-listed for tomorrow's `tasks.md` → Saturday research:

- **Regulatory / agency & litigation — NEW instances: EU DSA "addictive features" action on META (up to 6% of revenue); AAPL v. OpenAI trade-secret lawsuit; US-AI-models-to-blacklisted-China report (GOOGL).** No rule reads an agency action, a lawsuit, or an export-control event. *Research: a regulatory/litigation-event overlay.*
- **Sector liquidity-rotation / IPO-drain — NEW: SK Hynix's $26.5B listing draining AI-trade liquidity, pressuring MU.** No rule reads a forced-flow / large-IPO capital-rotation event. *Research: a forced-flow / liquidity-rotation overlay (overlaps with index-inclusion below).*
- **Index-inclusion / forced-flow — SK Hynix → Nasdaq Composite Mon; "Ex-Elon" ETFs (TSLA/SPCX); FSPC Space Economy ETF (RKLB); SPCX.** Recurring across many sessions → argues for a **6th Tier-B trigger** or a forced-flow overlay. `NEW_CATEGORY_NEEDED (index_rebalance)`.
- **Earnings/print-window assignment — JPM (7/14, window OPEN, most urgent), TSLA (7/22), ARM/INTC (7/23), AMZN (7/30).** All claimed by trend-following/breakout, not `equity_event_driven_catalyst` / `long_straddle_earnings`.
- **Capital-allocation / capex-commitment — MU $250B (carry); META AI-hardware memo / 14GW.** No rule reads a multi-year capex plan.
- **Activist-short / controversy — BE Hunterbrook rebuttal (ongoing).** No rule reads a short report or its rebuttal.
- **Vol-regime activation — benign VIX ~15.8 vs event-IV into the 7/14 cluster and the 7/22–30 earnings run.** Structures exist (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) but aren't activated on an earnings-IV / dispersion screen.
- **New-listing no-price-history triage — SKHY promoted but has no Alpaca regular-way bars until 7/13.** Same pattern as SPCX: a promoted name that can't be backtested until data accrues. Feeds the recurring fallback-threshold question (does a no-history / 0-trade score route to `equity_watch_only` vs a below-baseline trading provisional?).

## Recommendations for the trader

- **NOTABLE, not gating.** Weight this as a soft signal — nothing here requires deviation from the algorithmic-only mandate. The memory-cohort rotation and META's regulatory headline are informational; positions ride their own rules.
- **SKHY triage (next run = Mon 7/13):** run `triage-symbol SKHY --gap-type event_catalyst`. **Expect the no-price-history path → provisional/quarantined** (SKHY's regular-way data starts 7/13; Friday's SKHYV line is temporary). This is the legitimate resting outcome for a brand-new listing — do not force a trading claim. Interim price ref SKHYV ~$168–170.
- **Held name META:** the EU DSA finding is **preliminary** (a "may breach" notice, not a fine) and META closed **up** on the AI-capex memo — no basis to override its MACD rule. Soft note only.
- **Provisionals unchanged:** QCOM/SPCX/SYNA/WULF stay quarantined (`revalidate_by` 7/21 for the first three; WULF 7/23). WULF had **no fresh event** today. SPCX's forced-flow noise does not change its quarantine.
- **Digest the 7/14 cluster** (June CPI ~3.9%/2.9% forecast + Warsh testimony + JPM earnings) and the elevated event-IV into the 7/22–30 earnings run (TSLA 7/22, ARM/INTC 7/23, AMZN 7/30). Rate/vol-sensitive; none makes today halt-worthy.
- **Standard workflow otherwise.** The event cluster is genuinely two-sided-but-constructive — don't manufacture action from it.
