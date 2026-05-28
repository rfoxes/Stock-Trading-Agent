# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (2026-05-28, Thu). Three watchlist event items: (1) META launched global paid subscriptions across Instagram, Facebook, WhatsApp, and Meta AI ($3–$4/mo) — first material business-model expansion in years, BNP $955 target, ~$13.5B incremental rev by 2028; (2) Snowflake signed $6B 5-year AWS Graviton commitment alongside +37% post-print on raised FY27 guide — direct positive for AMZN cloud-share narrative; (3) Laura Loomer wrote to Pentagon flagging Jensen Huang's just-reported Tsinghua University advisory-board role as a "massive scandal." Plus a mixed April PCE (3.8% headline, 3-year high; 3.3% core; monthly 0.4% slightly cooler than 0.5% est.) and a tentative US-Iran 60-day ceasefire MoU framework that Trump hasn't approved (US/Iran also briefly exchanged fire early Thursday before the diplomatic news landed). S&P closed fresh record 7,563.63 (+0.58%); VIX 15.7–16.3 (off ~1pt from 17.01).
- **Universe last covered:** full 10-name watchlist (SPY, QQQ, AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM). Alpaca News returned 83 items (NVDA 17, MSFT 14, AMZN 13, TSLA 9, META 8, GOOGL 6, SPY 6, AAPL 5, QQQ 3, JPM 2). All six category HTMLs written (macro, earnings, geopolitics, policy, volatility, options_flow). Cleanup deleted 0 (90-day retention still not hit).

## Notable carry-forwards

- **META cleanest positive single-name catalyst of the week.** Paid subscriptions launched today across all four properties; analyst $955 target; ~$13.5B 2028 revenue add. Combined with yesterday's bounce on priced-in SCOTUS denial + Zuckerberg-cloud-hint, META's bear case is materially softened. Watch for follow-on coverage tomorrow (subscription pricing reactions, take-rate datapoints if any leak).
- **NVDA Loomer/Tsinghua story is the new political-risk overhang.** Loomer letters have historically translated into administration action. Tomorrow: check for any Truth Social post or Pentagon response. If WH distance themselves from Huang's advisory role, that's a NVDA-negative escalation. If nothing happens, it fades. AAPL (Cook) and TSLA (Musk) reportedly on same Tsinghua board — multi-name policy-risk path exists.
- **Iran MoU needs Trump approval.** Tentative 60-day framework reached today; Trump said "not satisfied." Overnight Truth Social signal could resolve either direction. If rejected → futures gap risk + oil bid back. If approved → mild risk-on continuation. Treat as a fresh input tomorrow morning.
- **SNOW worth adding to extra_symbols.** Direct AMZN read-through plus standalone AI-monetization-narrative leader. Recurring catalyst.
- **MU / INTC / DELL / SNDK / AKAM** — large gainers today; MU and DELL recur from yesterday. Check tomorrow whether AKAM (+28.2%) and INTC (+13.5%) had confirmed catalysts (likely yes given size). AKAM specifically warrants a quick confirmation pass — that's earnings-grade movement.
- **AI-monetization theme.** SNOW +37% on revenue-now framing; CRM/MRVL flat-down on revenue-later framing. Next watchlist prints (late July onward) will be judged on this same axis. Soft-negative MSFT bias going into the late-July print window.
- **Warsh-era Fed remains background context.** First Warsh FOMC June 16–17. PCE today reinforced hawkish framing; ~50% probability of ≥25bp hike by year-end per CME FedWatch.
- **VIX in vol-selling territory (~16).** Index IV rank likely <30; NOT a high-IV regime for the `iron_condor_high_iv` skeleton. NVDA single-name IV elevated on positioning, no catalyst.

## To do today (tomorrow's run, Fri 2026-05-29)

1. Run the standard workflow (news_manual.md §"Workflow").
2. **META subscription follow-on:** check for any take-rate or pricing-reaction coverage; check whether META gapped on the subscription news tomorrow.
3. **NVDA Loomer follow-on:** any Truth Social signal, Pentagon response, or WH distancing from Huang? If yes, NVDA-negative; if no, fade the story.
4. **Iran MoU status:** check for Trump approval / rejection. If rejected, expect futures gap + oil re-bid; flag prominently. If approved, drop to background.
5. **SPX gainers confirmation:** validate that AKAM +28.2%, INTC +13.5%, MU +13.8%, SNDK +14.3%, DELL +12.3%, MNST +13.9%, CPAY +11.1% had real catalysts (earnings beats most likely). Add the confirmed-catalyst names to candidates section.
6. **No FOMC, CPI, payrolls this week.** Macro section will be quiet — that's fine.
7. **No watchlist earnings in next 14 days.** Earnings section will be sparse — SNOW/CRM/MRVL post-print follow-throughs only.
8. **Friday-PM run:** weekend means the Saturday research agent will read your brief. If anything looks worth deeper research (Loomer/NVDA path, META subscription economics, SNOW take-rate methodology), flag it in `news_tasks.md` for Saturday.

## Open questions for the operator

- The brief now consistently flags SNOW, MU, DELL as "candidates for universe" multiple sessions in a row. Worth a deliberate operator decision on `state/extra_symbols.md` inclusion.
- AKAM's +28.2% move is large enough to warrant operator awareness even if it stays out of the universe.

## Operational notes

- `cli news-fetch` returned 83 items cleanly (no proxy errors). WebSearch returned useful results for PCE/Fed, Iran/Hormuz, VIX, NVDA options skew, SPX movers, and earnings calendar queries.
- `git-sync` failed yesterday (stale `.git/index.lock` from another git process; sandbox couldn't unlink). If yesterday's trader handoff didn't clear it, today's `git-sync` may hit the same error. Surface the error if it recurs.
- Previous note: "WebSearch returns nothing useful for 'CPI release' queries; use 'CPI <month> <year>' instead" — not exercised today (no CPI on calendar); leave the note for future runs.
