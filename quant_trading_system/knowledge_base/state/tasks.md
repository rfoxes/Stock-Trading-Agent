# Tasks for the next run

This file is the focused to-do list for tomorrow's Claude. Yesterday's
Claude wrote it after finishing today's work. Replace it (don't append)
when you write the version for the next-next Claude.

Keep it short. The full narrative belongs in `last_handoff.md`. This file
is just "the specific things you should do."

---

## Status as of the last update

(Filled in by yesterday's Claude — 2026-05-26, Tue, post-close run.)

- **Active strategy:** none. 14th consecutive do-nothing run.
- **Broker baseline:** still the same 10 unattributed longs (SPY, QQQ,
  AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM), same lot sizes, same
  avg-entry to the cent. Equity $110,557.20 (-0.55% vs. Mon holiday MTM,
  -0.55% on a +0.61% S&P day). Buying power $14,025.98. No open orders.
  Journal still empty.
- **Tuesday-open reconciliation: clean.** Holiday MTM drifted at most
  -1.62% (AMZN) on actual Tue close. No further investigation needed.
- **Regime:** `bull, conf=0.76, adx=26.3`. Unchanged classification.
- **Operator silence:** ATTENTION.md mtime still 2026-05-14 17:44.
  No new note in `state/` resolving the attribution question. The new
  `state/manual.md` and `state/tasks.md` written 2026-05-25 17:08 are
  still the latest operator signals.
- **Open positions of note:** META unreal -10.5% (-$2,011 abs); the
  -15% escalation trigger has not fired but the gap closed -0.44pp
  from yesterday on actual Tue tape.

## To do tomorrow (Wed 5/27)

**OPERATOR DIRECTIVE (added by operator 2026-05-27, supersedes decision
tree below):** Attribute the existing 10 unattributed positions to
`equity_trend_following_ema_cross`. Run:

```
python3 -m quant_trading_system.cli set-active equity_trend_following_ema_cross \
    --reason "Operator-assigned attribution per state/tasks.md (2026-05-27 operator directive). Existing 10 long positions (SPY, QQQ, AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, JPM) are now under harness management."
```

Then run `execute`. Expected first-session effects per the strategy's
rules: META (and possibly JPM) likely exit on the next session's open
due to EMA12<EMA26 / ADX-fade conditions. That outcome is intended and
authorised by the operator. Do NOT defer.

The original decision tree below is preserved for context but the
operator directive above takes precedence today.

1. Run the standard read-and-snapshot sequence (manual.md §1–2). Same
   shape as today.
2. **Check `state/` mtimes** (not just contents) for any new operator
   signal since 2026-05-25 17:08. If anything moved, read it.
3. **Decision tree (superseded today by operator directive above):**
   - **Path A:** if a new note attributes existing positions to `<id>`
     → `set-active <id>` with reason "Operator-assigned attribution per
     `state/<note>`", then `execute`. Expect META (and possibly JPM)
     to exit on the next session's open.
   - **Path B:** if the broker is flat (positions list empty)
     → `set-active equity_trend_following_ema_cross` is clean, then
     `execute`. Day-1 sizing should fit the ~$14K buying-power cushion.
   - **Path C:** neither → 15th do-nothing day. One-paragraph
     conclusion. Don't force `set-active`.
4. If META gapped further down on Wed open, log the new unreal % in
   your handoff but do NOT take unilateral action on an unattributed
   name.
5. Write a new `tasks.md` and `last_handoff.md`. Fill the Status section
   from real probe observations. The next `tasks.md` should reflect that
   attribution has happened — no need to keep the directive block above
   in tomorrow's file.

## Open questions for the operator

(Same as yesterday — operator has not yet weighed in.)

1. **Should the harness take ownership of the existing 10 longs?**
   If yes: add a one-line attribution in this file (e.g., "Attribute
   existing positions to `equity_trend_following_ema_cross`"). If no:
   flat-close them (or move them to a separate account) so the harness
   starts from `positions == []`.
2. **The new `state/tasks.md` you placed on 5/25 asserted "account
   flat, no open orders" in its Status section.** Was that template
   default-committed-verbatim, or did you intend for Claude to ignore
   broker state? Either is fine; just want confirmation before acting.
3. **No new question today.** The Memorial-Day MTM anomaly (flagged
   in yesterday's open questions) is resolved — reconciled cleanly on
   Tuesday's open. No future-holiday handling needed beyond a sentence.
