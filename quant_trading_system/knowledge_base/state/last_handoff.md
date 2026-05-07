# Handoff to first Claude

This is the first scheduled run of the harness. There is no trading history,
no prior conclusions, and no active strategy yet. Treat today as a setup day
rather than a normal trading day.

## What you should do today

1. Read this handoff (you're doing it now), then `read_summary` (likely empty),
   then `read_recent_conclusions` (will be empty too).
2. Call `get_account` and `get_positions` to confirm the broker is reachable
   and the paper portfolio is in a known state.
3. Call `classify_regime` on SPY to see what the market is doing right now.
4. Call `list_strategies(status="active")` to see what's available, then
   `read_strategy` on 2-3 candidates that match the regime.
5. Pick the best fit and call `set_active_strategy` with a real reason.
6. If you're confident enough, plan a small starter position (one symbol,
   conservative size via `kelly_position_size`) and submit it through
   `submit_order`. It is also acceptable to do no trades on day 1 and just
   document the decision.
7. Call `write_conclusion` with a narrative summary: what you observed about
   the market, why you picked the strategy you did, what trade(s) (if any)
   you placed.
8. Call `write_handoff` for tomorrow's Claude. Tell tomorrow-you what's open,
   what to monitor, and any open questions that today's data couldn't answer.

## Key constraints to remember

- Paper trading only. Don't try to bypass SafetyGate.
- This is post-close (4 PM PST = 7 PM ET). Orders for tomorrow's session
  go in with `time_in_force='day'` (or 'gtc' for limits that can persist).
- Tag every order with the chosen `strategy_id`.
- Conservative day 1. Establishing a clean record matters more than alpha.

Good luck.
