# Symbol → sector overrides

Canonical extensible sector map for the news layer. Loaded at import time
by `news_service.SYMBOL_TO_SECTOR`. The seed defaults baked into
`news_service.py` cover the original 10-name watchlist; everything else
lives here.

**Format** (one entry per line, `<TICKER>: <sector>`):

```
AVGO: technology
DELL: technology
```

**Lines starting with `#` are comments. Blank lines are ignored.**

## Allowed sectors

The trader and research layer assume a small fixed set. Use one of:

- `technology`
- `financials`
- `consumer_discretionary`
- `consumer_staples`
- `healthcare`
- `energy`
- `industrials`
- `materials`
- `utilities`
- `real_estate`
- `communication_services`
- `index`            (for ETF benchmarks: SPY, QQQ, DIA, IWM, etc.)
- `crypto`           (for BTC, ETH, etc. if ever in scope)

If a symbol's true sector isn't in the list, pick the closest match and
add a comment explaining the choice. Do NOT invent a new sector without
updating `news_service.py` and the strategies that consume the map.

## Adding entries

`promote-candidate` writes to this file automatically. Do NOT hand-edit
unless you have a reason — the `--sector` flag on `cli promote-candidate`
is the canonical path. Hand-edits are still respected at runtime; the
in-memory map is rebuilt from `news_service.SYMBOL_TO_SECTOR` (seed) ∪
this file (overrides) on each import.

---

# Added 2026-06-04 (operator-directed backfill): the 7 symbols that
# entered the universe over 6/3-6/4 (ARM/CSCO/HPE/MRVL operator-add,
# AVGO/DELL/MU news-agent §9 promotion) all rolled to "uncategorized"
# because the seed map only covered the original 10. All are technology.
ARM: technology
AVGO: technology
CSCO: technology
DELL: technology
HPE: technology
MRVL: technology
MU: technology

# Added 2026-06-09 (news, promote-candidate)
TSM: technology

# Added 2026-06-09 (news, promote-candidate)
INTC: technology

# Added 2026-06-09 (news, promote-candidate)
CBRS: technology
