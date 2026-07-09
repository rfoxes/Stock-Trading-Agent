# News brief for 2026-07-09

## Headline assessment

**NOTABLE — a risk-on, event-rich day, NOT halt-worthy.** The marquee item is **Micron's $250B+ US investment commitment through 2035** (up from $200B; NY campus centerpiece, second Boise ID fab, Manassas VA, +$3B for domestic wafer supply; goal 40% of DRAM made in US) — MU +8%. It anchored a **memory-supercycle** session that also carried **SK Hynix's $29B ADR** pricing at $149 (7x oversubscribed, lists **7/10 as SKHY**), a WDC sympathy lift, and **ARM +11%** on pre-print positioning into its confirmed 7/23 earnings. Held name **META** got a *positive* capex event (broke ground on its first Canadian data center, launched Muse Image, 14GW compute plans). The macro backdrop turned **risk-on**: despite CENTCOM confirming **another round of US strikes on Iran**, crude **fell** and equities **rose** (Nasdaq +1.30%, S&P +0.81%, SMH +2.5%) — the market looked past the hostilities and yesterday's oil spike unwound. `market-status`: `is_open false`, `now 2026-07-09 15:40 PT`, `next_open 2026-07-10 09:30 ET` — canonical post-close run.

**None of the three HALT-WORTHY triggers fires:** (1) no FOMC *decision* today (June minutes 7/8 remain the signal; CPI + Warsh testimony land 7/14); (2) no adverse overnight catalyst on the held name — **META's event was positive** (data-center capex); (3) the Iran escalation did **not** gap equities >2% — it moved them **up**, and oil **down**. 168 Alpaca items (NVDA 25 / MU 17 / SPCX 17 / MSFT 12). **Universe grew 30 → 31: promoted WULF** (TeraWulf, Anthropic $19B 20-yr AI-datacenter lease — Tier-B #5 anchor-customer win). `list-active`: claimed 30/30 (pre-WULF), **unclaimed 0**, **provisional 3 (QCOM, SPCX, SYNA)** `revalidate_by 2026-07-21`; `gap-registry coverage_holes` **empty**.

> **For the trader (P0 triage):** newly-promoted **WULF** is in the universe but **UNCLAIMED** — run `triage-symbol WULF --gap-type event_catalyst`; per mandatory-attach doctrine a no-edge name gets `equity_watch_only`. I promote + tag only; I cannot attach strategies. Provisional 3 (QCOM/SPCX/SYNA) untouched.

> **On the held book:** the universe now shows **positions = META only** — consistent with the 7/8 handoff's prediction that the AVGO/MU/ORCL `equity_event_driven_catalyst` exits fill at the 7/9 open. That is the trader's reconciliation (`log-closed`), not mine. Soft-signal note only: **MU received a *positive* $250B-capex catalyst today**, which post-dates its time-stop exit — informational; I do not and cannot advise overriding an algorithmic exit.

## Watchlist + positions

Event-driven lines (a thing that *happened*), each tagged with a canonical `gap_type` + algorithmic responder. Price moves omitted — the trader has bars.

- **MU: committed $250B+ to US investment through 2035** (up from $200B) — second Boise ID DRAM fab, Manassas VA expansion, NY campus centerpiece, +$3B for domestic supply chain (TX raw-wafer financing); stated goal 40% of DRAM produced in US. A major capital-allocation / capex event, policy-aligned (Trump reshoring). MU +8%. (Its position was exited at the 7/9 open on the time-stop — this catalyst post-dates that.)
  - gap_type: event_catalyst (capital allocation / capex commitment)
  - responder: NONE — library gap (MU is claimed by `equity_event_driven_catalyst`, but that models MU's *own earnings/catalyst window*, not a multi-year capex plan; and the MU lot was just exited on the time-stop)
- **META (held): broke ground on its first Canadian data center, launched Muse Image, tied to 14GW compute plans** — a capex/product event on the sole held name. AI-buildout positive.
  - gap_type: event_catalyst (capex / product)
  - responder: NONE — library gap (META claimed by `equity_momentum_macd_histogram` (trending); no capex/product responder — position rides its MACD exit)
- **TSLA: NHTSA warned AV companies over a "clear pattern" of first-responder interference, demanding fixes by end-July** (regulatory action on the robotaxi/FSD cohort — also hits GOOGL/Waymo, AMZN/Zoox, UBER). Separately, Model Y reclaimed China's #1 best-seller in June (demand signal). Q2 earnings 7/22.
  - gap_type: event_catalyst (regulatory) — plus earnings_window (7/22)
  - responder: NONE — library gap (TSLA claimed by `equity_trend_following_ema_cross`; no regulatory responder, and the earnings-window strategy does not claim TSLA — assignment gap)
- **MSFT: swapping OpenAI/Anthropic models for in-house AI in Excel & Outlook; OpenAI (MSFT-backed) launched "ChatGPT Work" workplace agent** — a vendor/strategy shift plus a partner product launch.
  - gap_type: event_catalyst (product / vendor strategy)
  - responder: NONE — library gap (MSFT claimed by `equity_momentum_macd_histogram` (trending); no product/vendor responder)
- **ARM: +11% on aggressive institutional buying ahead of confirmed 7/23 Q2 earnings** — pre-print IV-expansion / positioning. (The breakout itself is price, for the trader's `equity_breakout_volume_confirmation` rule; the *event* is the earnings date.)
  - gap_type: earnings_window (7/23)
  - responder: NONE — library gap (earnings-window responders are `equity_event_driven_catalyst` / `long_straddle_earnings`; neither claims ARM — assignment gap. ARM's momentum is claimed by breakout_volume_confirmation, which reads price not the calendar)
- **RKLB: Street digested its $8B Iridium acquisition + a $3.6B bridge loan** (recurring satellite-connectivity revenue thesis) — M&A follow-through; RKLB is the acquirer leg.
  - gap_type: pairs_arbitrage (merger, acquirer leg) / event_catalyst
  - responder: NONE — library gap (RKLB claimed by `equity_breakout_volume_confirmation`; merger-arb lives in `equity_pairs_trading_cointegration`, which claims only SYNA — RKLB/IRDM pair unmodeled)
- **BE: management escalated its rebuttal of the Hunterbrook short report; shares rallied** — the short thesis is being contested, not confirmed. (Watched carry from 7/8.)
  - gap_type: event_catalyst (activist short / controversy)
  - responder: NONE — library gap (BE claimed by `equity_breakout_volume_confirmation`; no short-report/controversy responder)
- **JPM: firmed into its 7/14 Q2 print (window OPEN, most urgent)** — bank season opens Tuesday alongside June CPI + the Warsh testimony. Est ~$5.61/sh on ~$49.56B rev; $50B buyback effective 7/1.
  - gap_type: earnings_window
  - responder: NONE — library gap (JPM claimed by `equity_trend_following_ema_cross`, not `equity_event_driven_catalyst` — assignment gap; most urgent)
- **INTC: Q2 earnings 7/23** (today: semi-rotation + whale-scan only, no fresh corporate event).
  - gap_type: earnings_window (7/23)
  - responder: NONE — library gap (INTC claimed by `equity_breakout_volume_confirmation` — assignment gap)
- **AMZN: Q2 earnings 7/30** (BNP Paribas Outperform, $345 target); also named in the NHTSA AV warning (Zoox). No fresh hard corporate event.
  - gap_type: earnings_window (7/30)
  - responder: NONE — library gap (AMZN claimed by trend-following — assignment gap)
- **SPCX (PROVISIONAL / execution-quarantined): no new hard corporate event** — heavy commentary (Grantham/Chanos/Gary Black bearish; JPM "$1.77T merger-currency" for a Tesla combination), Grok 4.5 launch, Blue Origin $10B raise, BlackRock QQQ-challenger ETF war. The index-inclusion / forced-flow theme persists.
  - gap_type: event_catalyst — index-inclusion forced-flow, unmodeled → **NEW_CATEGORY_NEEDED (index_rebalance)**
  - responder: NONE — library gap (SPCX's trend-following claim is provisional/quarantined AND no rule reads forced-flow / index mechanics)

**No fresh single-name news** (price/analyst/cohort only — nothing that *happened*): **AAPL** (Apple-Broadcom deal carrying; Luxshare HK-supplier IPO -5%; senator-sale noise), **AVGO** (Apple-deal carry, Morningstar "cheap list" = opinion; lot exited at open), **NVDA** (cohort/valuation/opinion; Mindbeam NVDA-backed pain-drug = minor), **DELL** (Evercore PT→$500 is an analyst PT = dropped; AI-demand rally = price), **GOOGL** (NHTSA/Waymo folded into the TSLA line; DMA carry), **SNDK** (memory-cohort read-through only), **TSM** ("backbone of AI" commentary), **ORCL** (exited at open; whale-scan mention), **CBRS/QQQ/SPY** (flow rollups), **CSCO / HPE / IRDM / MRVL / NUVL** (0 items), **QCOM / SYNA** (0 items; provisional).

## Sector themes

- **Memory supercycle broadening — the day's dominant theme.** Micron's **$250B** US buildout + **SK Hynix's $29B ADR** (7x oversubscribed, priced $149, lists **7/10 as SKHY**) + a Western Digital sympathy lift, with retail reportedly rotating MU → SK Hynix and Cramer warning bankers on aggressive pricing. Pricing cycle intact; the marginal development is a **funding-rotation** overhang as a second mega-cap memory name lists in the US.
- **AI-datacenter capex.** Meta 14GW compute + first Canadian DC; Micron's fabs; **TeraWulf's $19B, 20-yr Anthropic lease** (promoted as WULF); Lumentum/MARA optics-and-land moves. Sustained multi-node (compute / memory / power / optics) buildout.
- **Tech volatility regime — dispersion, not index.** Tech single-name vol hit a **23-year high** (options price bigger Nasdaq-100 swings than the S&P) even as **VIX sits at 16.9**. Vol lives in single-name tech + event-IV, not the index — the key read for the options side.
- **Sector rotation.** "Selling winners, buying losers" to start H2 — energy bid, some intraday tech-mega-cap give-back — though indices *closed up*, led by semis. A rotational undertone worth tracking (feeds `equity_sector_rotation_momentum`).
- **Space / forced-flow.** RKLB/Iridium M&A, SpaceX's fast-tracked Nasdaq-100 inclusion (Grantham: Nasdaq "cheated"), Blue Origin's $10B raise, and BlackRock's new QQQ-challenger ETF — the index/passive-flow mechanics theme keeps recurring (still unmodeled).

## Candidates for the universe

**PROMOTED today (universe 30 → 31):**
- **WULF (TeraWulf, technology)** — Anthropic **$19B, 20-year AI-datacenter lease** (Hawesville KY, 401MW) + Fluidstack Abernathy JV sale; MS raised PT. Tier-B #5 (Tier-1 anchor-customer win). AI-infra/datacenter cohort (BE/SMCI-adjacent). Lands **unclaimed** → trader mandatory-attach triage.

**Tracking (NOT promoted — not yet US-tradable / no clean single-name hard catalyst):**
- **SK Hynix (SKHY)** — priced $149/ADR today; **lists on Nasdaq 7/10** ($29B, largest-ever foreign US listing). **Promote on its 7/10 debut** — ticker now confirmed **SKHY**; memory cohort (technology). Not addable until it trades.
- **ANET (Arista)** — +8.8% near a 52-week high, but no concrete catalyst stated (price/momentum). Track.
- **LITE (Lumentum)** — surging on Meta 14GW + MARA land (sympathy, no LITE-specific event). Track.
- **NOK (Nokia)** — rose on a NestAI defense-tech partnership; foreign-HQ telecom, tangential to the AI/semis core. Track, don't promote.
- **WDC (Western Digital)** — memory sympathy on Micron's $250B (no WDC-specific event). Track (recurring memory-cohort).
- **Blue Origin** (private, $10B raise) / **Luxshare** (HK IPO) — not US-tradable. Track.

## Macro / sector context

- **Risk-on tape despite fresh US-Iran strikes.** CENTCOM confirmed another round of strikes on Iran, but crude **fell** and equities **rose** (Nasdaq +1.30%, S&P +0.81%, Dow +0.27%; SMH +2.5%, MU +4.5%). Yesterday's +5% Brent spike unwound — the oil-risk channel that pressured chips on 7/8 did not persist. Watch overnight for renewed escalation, but the geopolitical tail closed **contained**.
- **Labor / inflation.** Weekly initial jobless claims fell to **215k** (healthy). China June CPI cooled to **1.0%** YoY (below 1.1% est; food -1.6%) — continued Chinese disinflation.
- **7/14 is the week's pivot.** June CPI + new Fed Chair **Warsh's semi-annual congressional testimony** + bank earnings (JPM) all land Tuesday — the first hard inflation read since the hawkish June minutes (median end-2026 ~3.8%). No Fed action today; funds 3.50-3.75%.
- **Regulatory.** NHTSA's AV first-responder warning (fixes due end-July) is the fresh action; EU DMA App Store ruling + SEC reporting overhaul remain live carries.
- **Vol.** VIX 16.9 (benign, contango) but record tech single-name dispersion — vol concentrated in names/events, not the index.

## Library gaps

`gap-registry coverage_holes` is **empty** — every item below is an **activation / assignment / taxonomy** gap (a rule/event-type isn't mapped), not a registry hole. Re-listed for tomorrow's `tasks.md` → Saturday research:

- **Capital-allocation / capex-commitment window — NEW instance (MU $250B; META 14GW / Canadian DC; Micron fabs).** No rule reads a multi-year capex or reshoring announcement; today it's a *positive* catalyst on a name just exited on a time-stop (MU). *Research: a capital-allocation / capex overlay.*
- **Regulatory / agency action — NHTSA AV first-responder warning (TSLA/GOOGL/AMZN/UBER, NEW); carry EU DMA + SEC.** No rule reads an agency action. *Research: a regulatory-event overlay.*
- **Earnings/print-window assignment — JPM (7/14, window OPEN, most urgent), ARM (7/23, +11% pre-print today), TSLA (7/22), INTC (7/23), AMZN (7/30).** All claimed by trend-following/breakout, not `equity_event_driven_catalyst` / `long_straddle_earnings`.
- **M&A-arb activation — RKLB (acquirer) / IRDM (target, $54/sh) + SYNA/onsemi (carry).** `equity_pairs_trading_cointegration` declares pairs_arbitrage but claims only SYNA; the RKLB/IRDM merger pair is unmodeled.
- **Product / vendor-strategy event — MSFT in-house AI swap (dropping OpenAI/Anthropic in Excel/Outlook); OpenAI "ChatGPT Work"; Grok 4.5.** No rule reads a product launch or a vendor/partner strategy shift.
- **Activist-short / controversy event — BE Hunterbrook rebuttal (escalated, shares rallied).** No rule reads a short report or its rebuttal.
- **Index-inclusion / forced-flow — SPCX Nasdaq-100 (Grantham critique) + SK Hynix listing 7/10 + BlackRock QQQ-challenger ETF (NEW_CATEGORY_NEEDED, index_rebalance).** Recurring across sessions — argues for a 6th Tier-B trigger or a forced-flow overlay.
- **Vol-regime activation — record tech single-name IV vs a benign 16.9 VIX; event-IV into the earnings cluster.** Structures exist (`iron_condor_high_iv`, `long_straddle_earnings`, `jade_lizard`, `calendar_spread`) but aren't activated on single-name dispersion or an earnings-IV screen.
- **Mandatory-attach for WULF — newly promoted, unclaimed.** Trader `triage-symbol` assigns it (likely `equity_watch_only`); Saturday research validates whether the Anthropic-lease name deserves a *trading* strategy.

## Recommendations for the trader

- **NOTABLE, not gating.** Weight this as a soft signal — nothing here requires deviation from the algorithmic-only mandate. Tape is risk-on (equities up, oil down); the held name (META) got a *positive* capex event. Positions ride their own rules.
- **Run mandatory-attach triage on WULF first** — it's in the universe but unclaimed. `triage-symbol WULF --gap-type event_catalyst`; expect `equity_watch_only` unless a library strategy clears baseline (that's the legitimate resting grade).
- **Reconcile the 7/9-open fills** (AVGO/MU/ORCL exits predicted by the 7/8 handoff — universe now shows positions = META only) via `log-closed equity_event_driven_catalyst`. **MU's $250B capex news post-dates its time-stop exit** — I flag it as positive context only; do NOT override an algorithmic exit.
- **Confirm provisional 3 (QCOM/SPCX/SYNA) stay quarantined.** SPCX's forced-flow noise does not change its quarantine.
- **Digest the 7/14 cluster** (June CPI + Warsh testimony + JPM earnings) and the elevated single-name tech IV into the earnings run (JPM 7/14 → ARM/INTC/TSLA 7/22-23 → AMZN 7/30). Neither makes today halt-worthy; both lean rate/vol-sensitive.
- **SK Hynix (SKHY) lists 7/10** — tomorrow's news agent promotes it on debut (memory cohort). Standard workflow otherwise; the event cluster is genuinely two-sided-but-constructive — don't manufacture action from it.
