# Extra symbols
#
# Operator-declared additions to the harness universe — anything that
# should be tracked + tradeable that isn't already declared by an active
# strategy, held as a position, or covered by the news layer.
#
# Format: any uppercase ticker (2-5 chars) on a non-comment line is
# picked up. Comma, space, newline — all fine separators. Lines that
# start with `#` are comments and are ignored.
#
# Example (commented out so it doesn't actually add these — uncomment by
# removing the `#` to declare):
# Healthcare:   LLY UNH PFE MRK ABBV
# Energy:       XOM CVX OXY SLB
# Financials:   BAC GS WFC MS
# Consumer:     WMT COST PG KO
# Industrials:  CAT BA DE
# Today's-add ticker tape goes below this line.

# Added 2026-06-03 (trader, operator-directed): news-flagged candidates with
# 5+ session recurrence. Get them into the universe ahead of Sat research's
# head-to-head battery so a strategy can be claimant before they're stale.
MRVL CSCO HPE

---

# Added 2026-06-03 (operator, promote-candidate): Computex Day-3 sustained; STRONG candidate per news brief 6/3
ARM

# Added 2026-06-04 (news, promote-candidate): 8-session recurrence; Q2 print past (beat top/bottom, Q3 AI guide light); analyst PT raises Thu (Jefferies 550, WF 545, Morningstar ~650); custom-silicon cohort marker
AVGO

# Added 2026-06-04 (news, promote-candidate): 8-session recurrence; AI-server cohort marker; doubled in a month per Benzinga; TSMC capacity-constraint pricing-power read-through
DELL

# Added 2026-06-04 (news, promote-candidate): recurring carry-forward; Q3 print ~June 24 (in 20 days); -7% Thu sympathy on AVGO read-through; 940% rally context
MU
