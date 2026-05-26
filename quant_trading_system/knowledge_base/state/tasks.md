# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-05-25, Memorial Day, post-close run.)

- **Active strategy:** none. Today's tasks.md (operator-placed) said to set-active `equity_trend_following_ema_cross`; deferred — see handoff item 1.
- **Last run's outcome:** 13th consecutive do-nothing run; no trades, no edits to strategy files, no `set-active`. Wrote a new conclusion (`2026-05-25.md`), a new handoff, and this file.
- **Broker state to verify:** **NOT flat.** 10 unattributed longs from day 5 still on the account (SPY, QQQ, AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM). Net unreal ≈ +$11.2K on holiday MTM. Equity $111,167.72. No open orders. Journal still empty.
- **Blockers from last run:** the runtime's default watchlist exactly matches the 10 unattributed positions, so `set-active equity_trend_following_ema_cross` + `execute` would let the strategy's exit pass touch the operator's book on Tuesday's open. Needs operator clarification before acting (see handoff item 1, paths A/B).

## To do tomorrow (Tue 5/26 — first fresh-tape session after the long weekend)

1. Run the standard read-and-snapshot sequence (manual.md §1–2). Compare Tuesday's open marks against today's holiday MTM to verify the paper-broker mark service reconciled cleanly. If a name diverges materially on Tuesday vs. today's holiday mark, document it but don't act.
2. Check `state/` for any new operator note resolving the broker baseline. Specifically:
   - If a note says "attribute existing positions to `<id>`" → `set-active <id>` with reason "Operator-assigned attribution per `state/<note>`" and then `execute` to let the strategy manage exits. Expect META (-10.1% unreal today) to be the most likely first exit candidate; that's intended under explicit attribution.
   - If the broker is now flat (positions list empty) → `set-active equity_trend_following_ema_cross` is clean (no exit-pass collateral damage), then `execute`. Conservative day-1 sizing should be fine; current buying-power cushion is ~$3.5K (~32% of one 10%-capped position).
   - If nothing changed in `state/` and the broker is unchanged → write another do-nothing conclusion. Don't force `set-active`.
3. If you do call `set-active` and `execute`, read the execute output's `intents` / `submitted` / `rejected` fields carefully. SafetyGate-rejected intents are useful diagnostic signal, not failures.
4. Write a new `tasks.md` and `last_handoff.md`. The Status section here was wrong-by-template on the version I received; please write yours from real probe observations.

## Open questions for the operator

1. **Should the harness take ownership of the existing 10 longs?** If yes, please add a one-line attribution in this file (e.g., "Attribute existing positions to `equity_trend_following_ema_cross`"). If no, please flat-close them (or move them to a separate account) so the harness starts from `positions == []`.
2. **The new `state/tasks.md` you placed today asserted "account flat, no open orders" in its Status section.** Was that an oversight (the template's default got committed verbatim) or did you intend for today's Claude to ignore the broker state? Either is fine, but I deferred until you confirm.
3. **The paper broker's holiday mark-to-market rolled position marks forward +1.59% on a closed Memorial Day** while the SPY quote stayed byte-identical to Friday's stale after-hours quote. Not an issue if it reconciles on Tue's open, but worth knowing about for any future holiday runs.
