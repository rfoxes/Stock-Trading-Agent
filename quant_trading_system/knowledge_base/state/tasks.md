# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-05-27, Wed, post-close run.)

- **Active strategy:** `equity_trend_following_ema_cross`
  (`since: 2026-05-27`). Operator directive executed. Attribution of the
  10 longs is now formal. End of the 14-day do-nothing run.
- **Today's `execute`:** strategy generated 3 ADX-fade exits (JPM, META,
  MSFT). All 3 rejected by SafetyGate (`daily_loss`: 2.3% > 2.0% cap).
  No orders submitted, book unchanged. Journal now has 3
  `order_rejected` events.
- **Broker baseline:** same 10 longs, same qty, same avg-entry to the
  cent. Equity $111,589.39 (+0.93% vs. Tue). Buying power $15,058.17.
  Cash -$96,531.22 (unchanged to the cent for the 15th day). No open
  orders.
- **Regime:** `bull, conf=0.76, adx=26.3`. Byte-identical to yesterday.
- **Position health update:**
  - **JPM** -4.46% unreal (was -2.12%) — dropped on Dimon $20B M&A +
    "tempered earnings" comments. Now an exit candidate (ADX 19.7).
  - **META** -7.23% unreal (was -10.54%) — *bounced* +3.70% on SCOTUS
    denial day. ADX 19.3 → exit candidate.
  - **MSFT** -1.60% unreal — small loss but ADX is 16.4, deeply
    trendless. Surprise exit candidate.
  - Others: all positive unreal, no exit triggers.

## To do tomorrow (Thu 5/28)

1. Standard read-and-snapshot sequence (manual.md §1–2). Check `state/`
   mtimes for any new operator note since 2026-05-27 21:54.
2. **Run `execute` again.** The active strategy is set; daily `execute`
   is the normal flow now. Expected scenarios:
   - **(A) Same 3-name basket re-rejected** if Thu marks keep the
     combined loss ≥ 2.0%. → No orders submit. Document and stop.
   - **(B) Basket unbundles** if e.g. JPM's ADX(19.7 today) recovers
     above 20, leaving META+MSFT (~1.5% loss) which would pass the
     `daily_loss` gate. → Orders submit and fill. Then run
     `log-closed equity_trend_following_ema_cross <symbol> <pnl>` for
     each closed position using the **actual realised pnl fraction**
     from the fill (not today's unreal numbers).
   - **(C) Outage / ModuleNotFoundError / broker unreachable** → don't
     edit strategies. Document in handoff and stop. (Manual §safety.)
3. **Do NOT loosen the `daily_loss` cap** to force the exits through.
   The gate is working as designed — a graduated multi-day exit of three
   losing positions is the intended behaviour. Force-flushing requires
   operator authorisation, not a Claude-side parameter tweak.
4. **Watch MSFT specifically.** It's the unexpected exit candidate (ADX
   16.4). If the basket unbundles and JPM/META exit but MSFT keeps
   getting re-targeted day after day, that's a "first to flush when the
   gate opens" pattern worth noting. If MSFT suddenly stops getting
   targeted (ADX climbs back above 20), note that too.
5. **News brief: read it.** CRM prints AMC tonight (adjacent MSFT
   enterprise-AI sentiment, not on watchlist). Iran de-escalation
   continues unless reversed. SCOTUS-META is now priced-in noise.
6. **No script edits.** Library is fine; the live strategy behaved
   correctly today.

## Open questions for the operator

1. **Daily_loss cap behaviour confirmed expected?** Today's basket of 3
   ADX-fade exits was blocked at 2.3% > 2.0% cap. Implicit assumption:
   you want a graduated multi-day exit rather than a single-day flush
   of attributed losers. If you actually want instant clearance, the
   cap needs a config bump or a one-time override mechanism (not
   currently present in the CLI). Will continue to honour the gate
   until you say otherwise.
2. **MSFT exit was not anticipated by yesterday's handoff.** ADX 16.4
   exit triggered cleanly. Just flagging — no action requested.
3. **Holiday-MTM diligence remains closed.** No outstanding question.
