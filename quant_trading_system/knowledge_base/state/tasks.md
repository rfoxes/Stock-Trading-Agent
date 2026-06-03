# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This
file is just "the specific things you should do."

---

## Status as of the last update (Tue 2026-06-02, post-close)

- **Active set:** one strategy — `equity_trend_following_ema_cross`
  owning [AAPL, AMZN, GOOGL, JPM, NVDA, QQQ, SPY, TSLA]. Verify with
  `cli list-active`. Unclaimed in universe: META, MSFT.
- **Today's execute:** 1 intent, 1 submitted, 0 rejected. **TSLA full
  exit (48 shares, market, day) — ADX(14)=18.9 fade, est. P&L +$846.**
  Order_id `ee8663af-4644-46b6-b1a9-fa0c326a1393`. AH paper — should
  fill at Wed open.
- **Account:** equity $110,981.21 (+$619.61 / +0.56% vs Mon), buying_power
  $51,326.07, cash -$59,655.14 (unchanged).
- **Regime:** bull, conf 0.80, ADX 29.69 (7th consecutive bull day; flat
  vs Mon).
- **Mon→Tue unrealized %:** AAPL +12.71→+15.92, AMZN +4.29→+3.00,
  GOOGL +9.32→+7.20, JPM -5.26→-3.86, NVDA +12.33→+11.09,
  QQQ +14.23→+15.05, SPY +6.75→+7.07, TSLA +2.48→+4.37.

## To do tomorrow (Wed 6/3)

1. **Read last_handoff.md, then news_brief.md FIRST.** AVGO + CRWD
   print AMC tonight — watch the brief's assessment, but you have no
   exposure to either (logged library gaps).

2. **Standard read-and-snapshot.** Include `cli list-active`.

3. **Reconcile TSLA close.** The Tue TSLA sell (48 shares) should have
   filled at Wed open. After running `cli positions`, if TSLA is gone,
   compute the realized P&L fraction and log it:
   ```
   python3 -m quant_trading_system.cli log-closed equity_trend_following_ema_cross TSLA <pnl_fraction>
   ```
   `pnl_fraction` = (filled_avg_price − avg_entry 403.98) / avg_entry.
   At Tue close mark this would be ~+0.0437 (+4.37%), but use the
   actual fill. If for some reason TSLA didn't fill and is still on
   the books, do NOT log-closed; document the open order in your handoff.

4. **Run `cli execute`.** Watch items going in:
   - **GOOGL** — Day 3 of $80B raise dilution; another -3-4% session
     could fire EMA-cross / ADX-fade.
   - **JPM** — still the standing ADX-fade candidate (held through Tue
     at ADX ≥ 20 even as other names faded).
   - **NVDA** — AI EO + HPE tailwind continues; expected hold.
   - **AMZN** — mild fade Tue; no event.
   - **AAPL, QQQ, SPY** — green; expected hold.

5. **HALT-WORTHY check:** unchanged criteria (FOMC, held-name earnings,
   futures gap >2%, geopolitical shock). Iran-Hormuz softened Tue but
   it's still a live overhang.

6. **Library gaps — log any new ones from `news_brief.md`.** Carry the
   list below into the next `tasks.md` if no responder is built in the
   meantime. **AVGO + CRWD print Wed AMC** — the news brief on Thu will
   either reaffirm the earnings-window gap (if either printed and
   nothing in the library responded) or, if Saturday's research agent
   has built `event_driven_catalyst`, validate the new responder.

7. **Do NOT revert** safety_gate.py rescope, `max_exits_per_run`,
   git-sync queue architecture, `active_strategies.md`, or launchd
   plists.

8. **Run `cli git-sync --agent trader --message "..."` as last action.**
   Expect `"queued"` in the response — that's success. Then `cli
   git-doctor` once. If pending_marker_count > 3 or stale_lock_count > 0,
   the operator hasn't installed the LaunchAgents — flag in handoff.

## Library gaps for the research agent (carry to research_tasks.md next Sat)

- **AVGO Wed 6/3 AMC earnings** — consensus $22.11B / $2.40 / AI +140%
  YoY; options 10.65% expected move. No earnings-window strategy in
  active set. Sat research priority: build/activate
  `event_driven_catalyst` with earnings-window entry rules. AVGO not
  in universe — needs `extra_symbols.md` addition if strategy is to
  use it. (Operator decision pending; will be moot post-Wed.)
- **CRWD Wed 6/3 AMC earnings** — consensus $1.36B / $1.07. Same gap
  shape as AVGO. Outside universe.
- **GOOGL secondary-offering dilution overlay** — no "secondary-offering
  dilution gap" rule. Trend-follower treats dilution like any gap.
  Multi-month overhang (remaining $40B ATM tranche starts Q3).
- **OpenAI Robotics → TSLA -$75B competitive event** — no
  "competitor-product-launch" overlay. Trend-follower reacted via
  ADX/EMA (TSLA exit fired Tue) but cannot distinguish the catalyst
  from generic weakness. Suggested: news-event-driven overlay that
  adjusts position sizing on confirmed competitor-product-launch for
  named holdings.
- **Trump AI Security EO** — no "policy-tailwind sizing" overlay.
  NVDA / GOOGL would be beneficiaries of a thematic-overlay for
  policy-event positive sizing.
- **EU cloud procurement rules** — no "regulatory-headwind sizing"
  rule for AMZN / MSFT / GOOGL cloud exposure.
- **META, MSFT** — still in the universe (Strategy frontmatter or
  extras) but no active strategy claims them, no positions held.
  Operator decision pending: drop from universe or claim with
  trend-following.
- **DELL, HPE, FLNC, MU, NTAP, OKTA, NOW, TEAM, SNOW** — flagged 5+
  consecutive sessions by news as universe candidates; no active
  strategy claims any of them. Same options as before: expand
  trend-following's claim list (after a head-to-head on each symbol
  vs. its current best) or build a multi-name momentum strategy.
- **MRVL** — NEW STRONG CANDIDATE per Tue news brief. +33% on Jensen
  "next trillion" anointment; $250B market cap; NVDA $2B stake
  validated. Optical-interconnect / networking-chip thesis.

## Open questions for the operator

1. **Please run `bash scripts/install_git_safety.sh` once from a real
   terminal.** Idempotent. One-time fix for the git-lock wedge.
   Verify with `launchctl list | grep harness`.

2. **AVGO Wed AMC** — last chance to add to `state/extra_symbols.md`
   before Wed close. Moot if the print happens without the symbol
   being included.

3. **Strategy health gap widening.** 30d cum_return -4.08% vs SPY
   +6.72% (-10.8 pp, +0.8 pp wider than Mon). Small-sample (N=2) but
   consistent gap. If TSLA exit fills profitably tomorrow, realized
   improves by ~0.76 pp.
