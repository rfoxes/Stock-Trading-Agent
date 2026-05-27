# News tasks for the next run

Yesterday's news agent writes this. Replace, don't append.

---

## Status as of the last update

- **Last brief assessment:** NOTABLE (2026-05-27, Wed). Three watchlist event items: (1) SCOTUS denied META's appeal — Vermont Instagram-addiction lawsuit can proceed; (2) Jamie Dimon publicly floated $20B JPM M&A capacity (also flagged "higher costs"); (3) Jensen Huang committed NVDA to $150B/yr Taiwan investment + dividend boost. Plus macro: Kevin Warsh formally seated as Fed Chair (sworn in May 22); first Warsh FOMC June 16–17; Goldman raised SPX target to 8,000.
- **Iran de-escalated**: White House denied Iran-floated draft MOU as "complete fabrication"; Trump said deal close; oil -5.55% to $88.68 (full unwind of yesterday's strikes spike). Risk-on close: Dow / S&P at fresh records (Dow 50,644 +0.36%; S&P 7,520 +0.02%; Nasdaq 26,675 +0.07%). VIX 17.01.
- **Universe last covered:** full 10-name watchlist (SPY, QQQ, AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM). Alpaca News returned 92 items (NVDA 24, TSLA 13, AAPL 10, MSFT 10, AMZN 9, META 6, JPM 6, QQQ 5, SPY 5, GOOGL 4). All six category HTMLs written (macro, earnings, geopolitics, policy, volatility, options_flow). Cleanup deleted 0 (90-day retention still not hit).

## Notable carry-forwards

- **META exit-risk just got fresh.** The SCOTUS denial is a real adverse legal event for META, on top of its -10.5% unreal position in the unattributed book. If META gaps down on Thu open, this is the most likely catalyst chain to flag as triggering an exit. Watch overnight options activity (no put-sweep size flagged today) and the Thu pre-market tape.
- **CRM prints AMC tonight (May 27)** — not on watchlist but a MSFT-sentiment leading indicator. **Confirm tomorrow morning** whether CRM beat / missed and whether Agentforce ARR accelerated. A bad print would be a soft-negative for MSFT enterprise-AI narrative. Options implied 8.7% post-print move.
- **MRVL beat AMC tonight ($0.80 vs. $0.75 est., +6.7%).** Constructive read-through for NVDA / semi sentiment. Confirm the post-print stock reaction overnight.
- **Iran is now a tailwind, not a watch-item.** Deal optics improving; oil collapsed. If overnight news flips back (Iranian retaliation, Trump pulls out of talks), re-escalate. Otherwise drop it from the daily watch-list.
- **JPM Dimon $20B M&A signal** is slow-burn — won't move JPM unless a specific target rumor surfaces. Background note only.
- **GOOGL EU DMA penalty** still pending dollar figure; no movement today.
- **Warsh-era Fed.** Trader handoffs should note "Warsh seated, hawkish-leaning, first FOMC June 16–17" as macro regime context. No action items today.

## To do today (tomorrow's run, Thu 2026-05-28)

1. Run the standard workflow (news_manual.md §"Workflow").
2. **CRM post-print read-through:** check whether CRM gapped > 5% either way on the print, and whether MSFT pre-market is reacting. Note in the brief.
3. **MRVL post-print read-through:** beat was reported (+6.7%); confirm the stock reaction and any NVDA-sentiment spillover.
4. **META Thu pre-market check:** any overnight gap-down on the SCOTUS news? If META is -3%+ pre-market, that's a single-name escalation worth flagging prominently.
5. **Iran-deal status:** if a real deal text surfaces (or talks visibly collapse) overnight, treat as a fresh catalyst. If the day's news is just more posturing, drop to background.
6. **No FOMC, CPI, payrolls this week.** Macro section will likely be quiet — that's fine, write it short.
7. **No watchlist earnings this week.** Earnings section is just MRVL / CRM read-throughs.

## Open questions for the operator

(none new)

## Operational notes

- `cli news-fetch` returned 92 items cleanly (no proxy errors). WebSearch returned useful results for FOMC/Warsh, Iran, VIX, earnings, and tariff/policy queries. Yesterday's note that "WebSearch returns nothing useful for 'CPI release'" wasn't tested today (no CPI this week); leave the note.
- `git-sync` ran as the final tool call. If it failed for any reason, surface in tomorrow's notes.
