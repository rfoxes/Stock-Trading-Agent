# Research tasks for the next Saturday run

Yesterday's Saturday Claude writes this file. Replace it (don't append)
when you write the version for the next Saturday's Claude.

Brief is fine. Full narrative belongs in the weekly log.

---

## Status as of the last update

(Filled in by yesterday's Saturday Claude. The defaults below apply for
the first run before any actual research has happened.)

- **Library size:** 18 strategies (10 equity, 8 options), 0 archived.
- **Last week's additions:** none — this is the first scheduled Saturday
  run after the research harness was added.
- **Last week's updates/archives:** none.
- **Open candidates from last week:** none.

## To do this Saturday

1. Run the standard read-and-survey sequence (research_manual.md §1-2).
2. **First-run priority:** read the existing 18 strategies briefly via
   `cli list-strategies` and pick 2 strategies that look thin or
   obviously dated to update. Don't add new strategies in week 1; calibrate
   on the existing library first.
3. Run `cli simulate equity_trend_following_ema_cross --symbol SPY` and
   `cli simulate equity_mean_reversion_bollinger --symbol SPY` to confirm
   the new walk-forward backtester actually runs against real data in
   your sandbox. If both work, the research path is healthy. If neither
   does, document the failure and stop — the harness needs operator
   attention before research can proceed.
4. Write `knowledge_base/research_log/<today>.md` and the next
   `research_tasks.md`.

## Open questions for the operator

(none yet)
