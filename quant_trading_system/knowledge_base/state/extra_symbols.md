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

# Added 2026-06-09 (news, promote-candidate): 3-session recurrence: Apple picks-and-shovels foundry-anchor framing + TSM-surging Day-1 Mon refresh; cohort foundry-layer anchor across WWDC + Intel-foundry-rotation narratives
TSM

# Added 2026-06-09 (news, promote-candidate): Tier-B #5 Tier-1-customer-win: The Information / Reuters report Mon 6/8 that Google placed >3M TPU manufacturing order with Intel Foundry for 2028. Largest hyperscaler validation of Intel's contract foundry to date; INTC +13% intraday. NVDA additionally evaluating backup foundry use (speculative leg, not qualifying).
INTC

# Added 2026-06-09 (news, promote-candidate): Tier-B #4 sell-side initiation cluster: 7+ banks initiated Mon 6/8 (Needham 00, Mizuho 00, Wedbush 70, Barclays 80, UBS 00, Rosenblatt 00, Morgan Stanley 50, Craig-Hallum 25). Post-IPO-quiet-period structural attention; CBRS +17% intraday. AI-inference cohort relevance to NVDA.
CBRS

# Added 2026-06-09 (news, promote-candidate): 3-session recurrence; BofA PT boost + multiple Q4 AMC preview articles Tue + Mon BofA 6-chip secular upside + Q4 preview articles
ORCL

# Added 2026-06-09 (news, promote-candidate): Tier-B #1 confirmed M&A target: GSK 0.6B all-cash 24/share (40% premium); FDA Priority Review PDUFA 2026-11-27
NUVL

# Added 2026-06-16 (news, promote-candidate): Operator-directed 2026-06-16: SpaceX largest-IPO-ever (~$2T, listed 6/12); FAB-10 frontier cohort; Nasdaq-100 fast-entry inclusion ~July1 forces QQQ rebalance + historic options debut. Operator override of Tier-A/B discipline (an IPO is not a Tier-B trigger). Sector=industrials (aerospace; Starlink leg => could be communication_services).
SPCX

# Added 2026-06-25 (news, promote-candidate): Tier-B #5 Tier-1 customer win: Qualcomm Investor Day named Meta as anchor customer for Dragonfly C1000 data-center CPU (2028 production); raised FY2029 non-handset target to $40B incl $15B data-center; stock +7.4%
QCOM

# Added 2026-06-25 (news, promote-candidate): Tier-A 3-session recurrence: memory/NAND supercycle now hard-validated by MU record print; SNDK +16% in cohort (WDC/STX), ~600% YTD, Defiance DRAM ETF launch, sustained sell-side cohort framing
SNDK

# Added 2026-06-26 (news, promote-candidate): Tier-B #1 confirmed M&A target: onsemi (ON) to acquire Synaptics in $7B all-stock deal (1.350 ON/sh, 19% premium), definitive agreement + SEC 8-K/425 filed 2026-06-25, close mid-2027. Live merger-arb instance for the m_a_arbitrage activation gap.
SYNA

# Added 2026-07-08 (news, promote-candidate): Tier-0 news-subject 7/8: product launch — validated Kubernetes Edge AI appliance w/ Red Hat/Everpure, stock surging; AI-server cohort (DELL/HPE adjacent)
SMCI

# Added 2026-07-08 (news, promote-candidate): Tier-0 news-subject 7/8: Rocket Lab's $8B Iridium acquisition (announced 7/1), space-consolidation leader; SPCX cohort
RKLB

# Added 2026-07-08 (news, promote-candidate): Tier-0 subject + Tier-B #1 confirmed M&A target: Rocket Lab $8B buyout at $54/sh, closes ~mid-2027; merger-arb candidate
IRDM

# Added 2026-07-08 (news, promote-candidate): Tier-0 news-subject 7/8: Hunterbrook short report on China scandium supply claims triggered major dip; AI-datacenter power
BE

# Added 2026-07-09 (news, promote-candidate): Tier-B #5 Tier-1 customer-win: Anthropic $19B 20-year AI-datacenter lease (Hawesville KY, 401MW), MS PT raise 7/9; AI-infra/datacenter cohort (BE/SMCI-adjacent). US-tradable (NASDAQ:WULF).
WULF

# Added 2026-07-10 (news, promote-candidate): Tier-0 news-subject + standing operator/prior-agent directive: SK Hynix $26.5B Nasdaq ADR debut 7/10 (largest-ever foreign US IPO), opened +14-17% over $149 offer, memory cohort. SKHY = permanent regular-way ticker live Mon 7/13 (temp when-issued line SKHYV traded ~$168-170 today; no Alpaca regular-way price history until 7/13).
SKHY

# Added 2026-07-13 (news, promote-candidate): Tier-0 news-subject (operator directive 2026-07-08): RIVN own coverage line + concrete catalyst = discounted 75M-share public offering (dilutive capital raise) on Mon 7/13; US-tradable (NASDAQ). EV peer to TSLA. Lands unclaimed -> trader triage (watch-grade expected).
RIVN
