# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This
file is just "the specific things you should do."

---

## Status as of the last update (Thu 2026-06-04, post-close)

- **Active set:** one strategy — `equity_trend_following_ema_cross` owning
  [AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA]. 7 longs held (TSLA closed
  Wed). Verify with `cli list-active`. **Unclaimed in universe: ARM, CSCO,
  HPE, META, MRVL, MSFT** (4 operator-added Thu: ARM, CSCO, HPE, MRVL).
- **Today's execute:** 0 intents, 0 submitted, 0 rejected, 0 errors.
  Correct algorithmic outcome — NORMAL FLOW day, no rule fired.
- **Account:** equity $110,697.80 (+$1,822.25 / +1.67% vs Wed),
  buying_power $142,235.69, cash -$39,579.96 (unchanged).
- **Regime:** bull, conf 0.81, ADX 30.71 (9th consecutive bull day).
- **Strategy 30d health (unchanged count fields; SPY rolled):**
  orders_submitted 3, orders_rejected 4, trades_closed 3, win_rate 0.6667,
  rolling_sharpe -0.200, cum_return -0.7% vs SPY +5.37% (-6.07pp gap,
  improved from -6.68pp Wed via rolling-window math).
- **Wed→Thu unrealized %:** AAPL +15.69→+14.73, AMZN +1.07→+2.05,
  **GOOGL +5.53→+9.54 (+4.01pp, Apple-Gemini contract win)**,
  **JPM -3.89→-0.69 (+3.20pp, financials rotation)**,
  **NVDA +7.17→+8.78 (+1.61pp, Siri 2.0 Blackwell anchor offset AVGO drag)**,
  QQQ +14.07→+13.79, SPY +5.92→+6.58.
- **Git-sync LaunchAgent OPERATIONAL** as of Thu git-doctor
  (pending_marker_count=1, only `marker_test.json`). Wed/Tue top operator
  priority RESOLVED.

## To do tomorrow (Fri 6/5)

1. **Read last_handoff.md, then news_brief.md FIRST.** **NFP releases Fri
   8:30 AM ET** — week's biggest macro event. Brief will summarize the
   reaction. Read the brief's headline assessment carefully — print could
   shift the tape's posture significantly.

2. **Standard read-and-snapshot.** Include `cli list-active` and
   `cli git-doctor` (expect pending_marker_count low; LaunchAgent draining).

3. **No open-orders reconciliation expected** — Thu was a flat day with
   no trades.

4. **Run `cli execute`.** Specific algorithmic risks tomorrow:
   - **NFP-driven shock scenarios:**
     - Hot print (>200K) → yield surge → trend-tech weakness candidate;
       NVDA/AAPL/GOOGL could see ADX fade if -3-5% sessions follow.
     - Cold print (<100K) → rate-cut rally → JPM ADX could compress
       further as financials rotation reverses; trend-tech firms up.
     - In-line (130-180K) → no immediate impact; standard workflow.
   - **JPM** — still standing ADX-fade candidate but rotation Thu pushed
     ADX higher; longer leash now.
   - **GOOGL** — Day-5 dilution overhang on $84.75B raise; Apple-Gemini
     contract is the dominant fundamental driver.
   - **NVDA** — Siri-Blackwell narrative is bullish; cohort drag from
     AVGO weakening. Expected hold absent NFP shock.
   - **AAPL** — holding into WWDC Mon-Fri next week.
   - **AMZN, SPY, QQQ** — no specific catalyst; expected hold.

5. **HALT-WORTHY check:** unchanged criteria (FOMC, held-name earnings,
   futures gap >2%, geopolitical shock). NFP itself is NOT halt-worthy
   under the current rules (no event-window rule exists). VIX 16.06 Thu,
   sub-threshold. Watch for VIX > 19 on NFP shock as a regime signal.

6. **Library gaps — log any new ones.** Carry forward the list below.
   Two new this Thu (event-window related):
   - **NEW: Tier-1 customer-win event** (Apple-Gemini drove GOOGL +4pp Thu;
     algorithm has no rule for this signal type).
   - **NEW: WWDC June 8-12 event-window on held AAPL** (no event-window
     rule).
   - **NEW: NFP macro-event-window** (no rule).

7. **Do NOT revert** safety_gate.py rescope, `max_exits_per_run`,
   git-sync queue architecture, `active_strategies.md`, launchd plists,
   or `agent_tools.news_fetch` universe fix.

8. **Run `cli git-sync --agent trader --message "..."` as last action.**
   Expect `"queued"` in the response. Then `cli git-doctor` once. With
   LaunchAgent now operational, pending_marker_count should stay low
   (≤3). If pending_marker_count > 5 or stale_lock_count > 0, re-flag
   in handoff.

## Library gaps for the research agent (carry to research_tasks.md next Sat)

- **NEW Thu: Tier-1 customer-win event (Apple-Gemini → GOOGL +4pp Thu).**
  No "product-tier-1-customer-win" rule. Same signal-type as NVDA Blackwell
  anchor + AAPL Siri 2.0. Suggested: enterprise-anchor-win event overlay
  (when a held name is named as anchor cloud/silicon/customer in a Tier-1
  deal, tilt position posture for 5-10 day repricing window).
- **NEW Thu: AAPL WWDC June 8-12 event-window.** No "event-window posture"
  rule. Trader has no concept of a 5-day product-launch window on a held
  name. Suggested: event-window overlay (defer entries / tighten exits
  inside the window).
- **NEW Thu: NFP / CPI / FOMC macro-event-window.** No "macro-event-window"
  rule. Suggested: macro-event-window overlay (defer entries / hold exits
  on print mornings).
- **AVGO peer-earnings cohort-spillover (Wed→Thu carry, played out as
  mixed signal — NVDA actually gained Thu despite cohort drag).** No
  "cohort-spillover from peer earnings" rule. Empirical Thu result
  weakens the "always-negative" framing of this gap; suggest research
  agent test BOTH directions.
- **Iran-Hormuz / oil-spike risk-off (Wed gap, calmed Thu).** No
  "geopolitical shock / oil-spike risk-off" overlay. Lower priority now.
- **Hot ADP+ISM → yield surge → rate-hike chatter (Wed gap).** No
  "rate-policy-shift sizing" rule. Trend-follower has no Treasury-yield
  sensitivity.
- **Cliffwater + Blackstone BCRED 2-day private-credit-gate cluster (JPM
  exposure).** No "credit-stress" overlay for JPM. Wed/Thu carry — Thu
  played out as moot (rotation tailwind dominated).
- **GOOGL Day-5 $84.75B raise** — no "secondary-offering dilution gap"
  rule. Multi-week overhang. Thu the Apple-Gemini news dominated.
- **TSMC capacity-constraint pricing-power signal** — no "supply-side
  pricing-power" overlay.
- **Trump AI EO 60-day "trusted partner" framework (Day-3)** — no
  "policy-tailwind sizing" overlay for NVDA / MSFT / ORCL beneficiaries.
- **EU cloud procurement rules** — no "regulatory-headwind sizing" rule
  for AMZN / MSFT / GOOGL.
- **AVGO not in universe + earnings-window strategy** — print past;
  decision is to leave gap until earnings-window strategy is built
  generally (covers CRWD Q1 ~Aug, MU ~June 24, NVDA ~Aug, ORCL ~June 18).
- **CRWD 4-for-1 split** — no corporate-action handler. Informational.
- **META, MSFT carry-over** — still unclaimed (not held). MSFT Thu got
  "undervalued" framing; META Thu got FCC undersea cable tailwind + ARK
  +$3.5M. Operator decision pending.
- **ARM, CSCO, HPE, MRVL operator-added Thu** — now in universe but
  unclaimed. Need head-to-head vs trend-following OR purpose-built
  strategy from research agent. CSCO 11 PT raises in a week + STM
  SpaceX-IPO optionality + MRVL Jensen-anointment all still STRONG.
- **DELL, FLNC, MU, NTAP, OKTA, NOW, TEAM, SNOW, STM** — universe-expansion
  candidates flagged repeatedly by news agent. Several at 8+ sessions
  consecutive (DELL, STM). Auto-promote threshold is 3 sessions —
  news agent should be calling promote-candidate for these.

## Open questions for the operator

1. **AAPL WWDC June 8-12 next week.** Trader has no event-window rule;
   will execute normally through it. If WWDC reveals are bullish, AAPL
   rises on the tape with no algorithmic edit needed. If it disappoints,
   EMA-cross / ADX-fade may fire mid-week. **Operator-visibility item.**

2. **Strategy health gap to SPY narrowing slowly.** Mon -10.8pp → Wed
   -6.68pp → Thu -6.07pp. Still N=3 realized; no rotation argument
   either way. Will continue to monitor as the window rolls.

3. **4 operator-added symbols (ARM, CSCO, HPE, MRVL) unclaimed.**
   Universe now 14, of which 8 claimed + 6 unclaimed. Need decision on
   whether to claim the new 4 with trend-following (after head-to-head)
   or wait for purpose-built strategies from Sat research agent.

4. **Auto-promote threshold check.** News agent should be calling
   `cli promote-candidate` for any candidate flagged 3+ consecutive
   sessions. Several names (DELL, STM, CSCO, MU) appear to qualify but
   haven't been promoted recently. Verify auto-promote is firing as
   intended in news agent.
