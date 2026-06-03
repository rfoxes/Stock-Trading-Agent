# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This
file is just "the specific things you should do."

---

## Status as of the last update (Wed 2026-06-03, post-close)

- **Active set:** one strategy — `equity_trend_following_ema_cross`
  owning [AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA]. **TSLA closed
  today (filled $418.23, logged +0.0353).** 7 longs held. Verify with
  `cli list-active`. Unclaimed in universe: META, MSFT.
- **Today's execute:** 0 intents, 0 submitted, 0 rejected, 0 errors.
  Correct algorithmic outcome — no per-symbol ADX/EMA rule fired despite
  -0.74% S&P / -0.89% Nasdaq sell on Iran shock + hot ADP+ISM +
  AVGO Q3 AI guide light.
- **Account:** equity $108,875.55 (-$2,105.66 / -1.90% vs Tue),
  buying_power $69,295.61, cash -$39,579.94 (improved by ~$20K on TSLA
  exit cash).
- **Regime:** bull, conf 0.80, ADX 29.69 (8th consecutive bull day).
- **Strategy 30d health (improved Tue→Wed):** orders_submitted 3,
  orders_rejected 4, trades_closed 3, **win_rate 0.6667** (was 0.50),
  **rolling_sharpe -0.200** (was -3.64), **cum_return -0.7%** vs SPY
  +5.99% (-6.68 pp gap vs -10.8 pp Tue).
- **Tue→Wed unrealized %:** AAPL +15.92→+15.69, AMZN +3.00→+1.07,
  GOOGL +7.20→+5.53, JPM -3.86→-3.89, NVDA +11.09→+7.17 (-3.92pp,
  cohort-pressure on AVGO Q3 AI guide), QQQ +15.05→+14.07,
  SPY +7.07→+5.92.

## To do tomorrow (Thu 6/4)

1. **Read last_handoff.md, then news_brief.md FIRST.** The big Thu
   open risk is **NVDA gap-down** from AVGO AH cohort-spillover
   (-5-8% AH on Q3 AI guide $16B vs $17.2B consensus). Watch the
   brief for confirmation.

2. **Standard read-and-snapshot.** Include `cli list-active` and
   `cli git-doctor`.

3. **No reconciliation expected.** TSLA already logged. No other
   open orders Wed close.

4. **Run `cli execute`.** Specific algorithmic risks tomorrow:
   - **NVDA** — top exit-fire candidate if AH cohort sell-through
     materializes. Already shed 3.92pp Wed; ADX(14) didn't trip but
     likely close to threshold. **If exit fires, it's clean — news
     context aligns (AVGO Q3 AI guide light spillover).**
   - **GOOGL** — Day-3 $84.75B (upsized from $80B) dilution
     overhang. Another -3-4% session could fire EMA-cross/ADX-fade.
   - **JPM** — still the standing ADX-fade candidate; held ≥20 for
     5+ sessions through multiple catalysts (Cliffwater credit-stress,
     yield surge).
   - **AMZN, AAPL** — broad-sell hit, no idiosyncratic catalyst;
     expected hold.
   - **SPY, QQQ** — Tue's 8-session win streak broke Wed -0.74/-0.89%;
     one bad day ≠ trend reversal. Two consecutive -1%+ would
     put index trend rules in play.

5. **HALT-WORTHY check:** unchanged criteria (FOMC, held-name
   earnings, futures gap >2%, geopolitical shock). Iran-Kuwait/Bahrain
   is a live overhang but futures gap was <2% Wed. Watch for further
   escalation overnight. VIX 15.77 (BENIGN-LOW unchanged).

6. **Library gaps — log any new ones.** Carry forward the list
   below. Several new this Wed:
   - cohort-spillover from peer earnings (NVDA ← AVGO)
   - geopolitical / oil-shock overlay (Iran-Kuwait/Bahrain)
   - rate-regime overlay (10Y yield breakout → duration risk)
   - bank-name credit-stress sensitivity (JPM ← Cliffwater)

7. **Do NOT revert** safety_gate.py rescope, `max_exits_per_run`,
   git-sync queue architecture, `active_strategies.md`, or launchd
   plists.

8. **Run `cli git-sync --agent trader --message "..."` as last
   action.** Expect `"queued"` in the response — that's success.
   Then `cli git-doctor` once. If pending_marker_count > 3 or
   stale_lock_count > 0, flag in handoff (operator install run is
   confirmed complete; persistent backlog would indicate the
   LaunchAgent stopped).

## Library gaps for the research agent (carry to research_tasks.md next Sat)

- **NEW Wed: AVGO Q3 AI guide light → NVDA cohort spillover.**
  No "cohort-spillover from peer earnings" rule. Direct unhedged
  exposure on held NVDA. Suggested: peer-earnings-event overlay
  (adjust posture when named cohort peer prints guide miss within
  ±2 sessions).
- **NEW Wed: Iran-Kuwait/Bahrain missile shock.** No "geopolitical
  shock / oil-spike risk-off" overlay. Suggested: macro-shock event
  overlay (oil >X gap, breaking-news shock → tighten stop discipline).
- **NEW Wed: hot ADP+ISM → rate-hike chatter.** No "rate-policy-shift
  sizing" rule. Trend-follower has no Treasury-yield sensitivity.
  Suggested: rate-regime overlay (10Y yield breakout → dampen
  long-duration tech weight).
- **NEW Wed: Cliffwater 5% redemption gate (JPM exposure).** No
  "credit-stress" overlay for JPM. Suggested: bank-name credit-stress
  sensitivity sizing.
- **GOOGL $84.75B raise Day-3 (upsized from $80B Tue)** — no
  "secondary-offering dilution gap" rule. Multi-month overhang
  (remaining ATM tranche Q3+). Trend-follower treats dilution-gap
  like any gap.
- **OpenAI Robotics → TSLA -$75B competitive event (Tue carry-over)** —
  no "competitor-product-launch" overlay. Moot now that TSLA exited.
- **Trump AI Security EO (Day-2)** — no "policy-tailwind sizing"
  overlay for NVDA / MSFT / ORCL beneficiaries.
- **EU cloud procurement rules** — no "regulatory-headwind sizing"
  rule for AMZN / MSFT / GOOGL cloud exposure.
- **AVGO not in universe + earnings-window strategy** — Wed AMC
  print materialized as expected (beat top/bottom, light Q3 AI
  guide). Use case for AVGO now is "exposure to the dip-buy"
  rather than "catch the print." Decision: leave gap until
  earnings-window strategy is built generally (covers CRWD, MU,
  NVDA, etc).
- **CRWD 4-for-1 split announced** — no corporate-action handler.
  Not held; informational.
- **META, MSFT carry-over** — still unclaimed in universe (not
  held). Operator decision pending: drop from universe or claim with
  trend-following.
- **DELL, HPE, FLNC, MU, NTAP, OKTA, NOW, TEAM, SNOW, MRVL, CSCO,
  STM, ARM** — universe-expansion candidates flagged repeatedly.
  CSCO new strong (11 PT raises in a week). STM new (SpaceX-IPO
  optionality). MRVL still strong post-Tue Jensen anointment.

## Open questions for the operator

1. **GIT-SYNC LAUNCHAGENT NOT DRAINING (re-flagged).** Tue handoff
   claimed install was complete and operational. Wed git-doctor shows
   pending_marker_count=8, including Tue's own trader marker. Either
   the install didn't complete, the LaunchAgent crashed, or its
   runner script is erroring. Please verify
   `launchctl list | grep harness` and check runner logs. Markers are
   safe on disk; queue will drain whenever fixed. Top operator
   priority.

2. **NVDA Thu open is the main visibility item.** If AVGO AH
   translates to NVDA -3-5% Thu open, an ADX-fade exit is plausible.
   This would be the second held name to exit on a peer-earnings
   cohort catalyst (after TSLA Tue on OpenAI Robotics). Not a strategy
   issue — it's the strategy doing its job — but worth knowing.

3. **Strategy health gap to SPY narrowed materially.** Tue -10.8 pp,
   Wed -6.68 pp (+4.1pp improvement from TSLA realized + rolling
   window). N=3 realized so still small-sample; not yet a basis to
   keep or rotate either way. Continue to monitor.
