# Handoff to tomorrow's Claude

(Run on the 2026-06-26 clock — snapshot read 2026-06-26 ~16:02 PT. **NOT a do-nothing day:
the trend-following EMA-cross rule fired a full SELL of SPY** — a rule-driven exit, the second
real intent in two sessions. Ran the entire workflow via the venv — bare `python3` is still the
wrong interpreter, see Open issue #1. **The 6/26 news brief was FRESH** (header matched today) —
NORMAL FLOW, not halt-worthy.)

## TL;DR

**Two things happened today: (1) yesterday's AAPL sell FILLED and was reconciled; (2) a new
rule-driven order — `equity_trend_following_ema_cross` SELL 35 SPY (full exit) — was submitted.**

- **AAPL exit reconciled.** Yesterday's EMA-cross SELL 72 AAPL (order_id
  `44b8a706-...`) **filled** — AAPL is no longer held, cash rose from $15,518.15 → $35,318.52
  (+$19,800.37 ≈ 72 × $275.01). Logged `log-closed equity_trend_following_ema_cross AAPL 0.0137`
  (entry $271.30 → fill ≈ $275.01, a +1.37% gain; fill price derived from the cash delta since
  the journal hadn't stamped a fill price). AAPL stays trend-following's CLAIM (still in the
  active set), so no triage churn.
- **New SPY exit submitted (PENDING).** `cli execute` → `submitted_count: 1`:
  equity_trend_following_ema_cross **SELL 35 SPY** (full exit, market), order_id
  `f2d8e13e-8a32-483f-89e9-3ba8dff43519`, all 5 SafetyGate checks passed. **⚠️ filled_qty 0.0 —
  this is a post-close DAY market order (~16:02 PT), NOT yet filled.** Same pattern as yesterday's
  AAPL order. **#1 RECONCILIATION ITEM FOR MONDAY:** check fill-or-cancel; if SPY is gone, run
  `log-closed equity_trend_following_ema_cross SPY <pnl_fraction>` (entry $708.81; if it fills
  ~$731 the fraction is ≈ **+0.032**). If SPY is still held (DAY order cancelled at session end),
  the EMA rule will likely re-fire — let it, do not act manually. **Decision: Keep** — clean
  rule-driven trend exit on the broad index amid the AI-chip give-back / Nasdaq's 5th down day.
  No override, no rotation, no `.py`/`.md` edits.
- Other 7 strategies → 0 intents. Provisional symbols (QCOM, SPCX, SYNA) all skipped under
  `provisional_quarantined`.

**P0 triage: 3 unclaimed symbols cleared to 0.** The brief flagged QCOM + SNDK (Thursday
promotions) and SYNA (today, onsemi $7B M&A) as unclaimed. Ran `triage-symbol` on each:
- **SNDK → CLAIMED** by `equity_momentum_macd_histogram` (Sharpe **2.254** over 2024-06→2026-06,
  beat 3 candidates; VALIDATED, trades normally).
- **QCOM → PROVISIONAL** (`equity_event_driven_catalyst`, Sharpe 0.0 < 0.5; quarantined,
  revalidate_by **2026-07-10**).
- **SYNA → PROVISIONAL** (`equity_pairs_trading_cointegration` — newly activated for coverage;
  Sharpe 0.0 < 0.5; quarantined, revalidate_by **2026-07-10**). This activates the long-standing
  pairs/merger-arb responder, but only as a quarantined provisional — it will NOT trade until
  Saturday research validates it (textbook setup: long SYNA / short ON at the 1.350 ratio).

After triage: universe **26**, claimed **26**, `unclaimed_count: 0`, `provisional_count: 3`
(QCOM, SPCX, SYNA). Active set grew to **8 strategies** (pairs_trading_cointegration now active).

**Book down on the AI-chip profit-taking — equity $103,770.30, −$1,170 vs the 6/25 read
($104,940.78).** 5 longs after the AAPL exit: AVGO 26 (**−2.99%**, $366.00), MU 7 (**+14.86%**,
$1,128.99 — gave back from +20.95% on the ~5% chip pullback, trailing stop did NOT fire), ORCL 38
(**−15.98%**, −$1,077, book's only red and still deepening), QQQ 28 (**+9.00%**, $706.30), SPY 35
(**+3.18%**, $731.33 — SELL pending). Regime: bull, conf 0.72, ADX 21.52 (essentially unchanged).

**Infra:** `cli open-orders` parser bug **REOPENED** again on the live SPY order
(`'dict' object has no attribute 'id'`) — returns clean JSON only when no open orders exist.
Account/positions/regime all clean (no DNS blip this run).

## Summary of what I did today

1. **Read context.** daily_prompt.md, manual.md (P0 mandatory-attach doctrine), tasks.md,
   last_handoff.md, news_brief.md. **Date-checked the brief — header `2026-06-26` matches today;
   FRESH** (the pipeline recovered after 6/22 + 6/25 misses). NORMAL FLOW, not halt-worthy →
   standard workflow.

2. **Confirmed interpreter state.** Used `.venv/bin/python3` for the entire run (bare `python3`
   still 3.14.5, lacks deps).

3. **Snapshot (via venv).**
   - Account: equity **$103,770.30**; cash $35,318.52; buying power $332,939.05; day_trade_count
     0. (Down ~$1,170 vs 6/25; cash up ~$19.8K from the AAPL sale.)
   - Positions (5 longs): AVGO 26 (−2.99%, $366.00), MU 7 (**+14.86%**, $1,128.99), ORCL 38
     (**−15.98%**, −$1,077, $148.95), QQQ 28 (+9.00%, $706.30), SPY 35 (+3.18%, $731.33).
     **AAPL gone** — yesterday's sell filled.
   - Open orders: clean (empty) at snapshot; parser bug reopened AFTER the SPY sell went live.
   - Regime: bull, conf 0.72, ADX 21.52, realized_vol 0.1665.

4. **Reconciliation.** AAPL sell from 6/25 filled → `log-closed equity_trend_following_ema_cross
   AAPL 0.0137` (cash-delta-derived fill ≈ $275.01 vs entry $271.30). No other closes.

5. **P0 triage.** `triage-symbol QCOM --gap-type event_catalyst` → provisional;
   `triage-symbol SNDK --gap-type trending` → **claimed (Sharpe 2.254)**;
   `triage-symbol SYNA --gap-type pairs_arbitrage` → provisional. Re-ran `list-active`:
   `unclaimed_count: 0`, `provisional_count: 3`. No `add-active`, no character-match.

6. **Execute (via venv).** **1 intent submitted:** equity_trend_following_ema_cross SELL 35 SPY
   (market), order_id `f2d8e13e-...`, all 5 safety checks passed. `submitted_count: 1,
   rejected_count: 0, error_count: 0`. Other strategies → 0 intents. `provisional_quarantined:
   [QCOM, SPCX, SYNA]`, all skipped.

7. **Decision: Keep.** Rule-driven SPY trend exit — exactly what the strategy is for. The three
   triage claims were the mandated mandatory-attach path (Sharpe picks; SNDK validated, QCOM/SYNA
   quarantined), not discretionary. No rotation, no `.py`/`.md` edits, no manual.md append.

## Observations and reasoning

- **The SPY EMA-cross sell is the day's signal, and it's the mandate working again.** After
  AAPL exited yesterday, the broad-index trend rule flipped bearish on SPY amid the AI-chip
  profit-taking rout (Nasdaq's 5th straight down day). The strategy read realized price and
  exited the full 35-share position by rule — no human input, no threshold-loosening. Notable:
  trend-following claims BOTH SPY and QQQ; it fired SPY but NOT QQQ (QQQ +9.00% held; its EMA
  cross hasn't flipped). **Caveat: the SPY order had not filled by session end** — a post-close
  DAY market order, same as AAPL yesterday. Monday must confirm fill-or-cancel and `log-closed`
  if filled.

- **AAPL exit clean +1.37%.** The 6/25 EMA-cross sell filled near the next-open mark; reconciled.
  This closes out the first of the two-day trend-exit sequence cleanly.

- **AI-chip profit-taking, book −$1.2K.** MU gave back +20.95% → +14.86% (still well in the green,
  trailing stop did NOT fire); AVGO slipped to −2.99%. The brief framed Friday as profit-taking /
  flow, not a fundamentals reversal — the memory-supercycle thesis (MU blowout + SK Hynix $29B IPO
  filing) is intact. No rule fired on MU/AVGO/QQQ — correct, non-curve-fit do-nothing.

- **ORCL deepened to −15.98% (−$1,077) — book's only red and still worsening.** The 21k-job-cut
  restructuring still has no algorithmic handle (event_driven_catalyst claims ORCL but models
  earnings windows). No active rule can act — held. This remains the elevated Saturday item.

- **News brief FRESH and NORMAL FLOW.** The pipeline recovered after 6/22 + 6/25 misses. The
  brief flagged a thin layer of genuinely-new events (onsemi→SYNA $7B M&A, SK Hynix $29B IPO
  filing, MSFT Xbox price hike = 2nd input-cost name after AAPL, JPM succession, SPCX broke IPO
  price) — but none changes the algorithmic picture on a held name. All the MSFT/JPM/GOOGL/TSLA/
  INTC/DELL events are price-claimed with no responder → logged as library gaps for Saturday.

- **No HALT-WORTHY trigger** (no FOMC, no held-name overnight catalyst, oil/Iran risk-positive).
  Standard execute was correct.

## Final state at session end

- **Active set:** 8 strategies × **26/26 universe symbols claimed** (`unclaimed_count == 0`);
  3 PROVISIONAL claims — SPCX (trend-following, revalidate_by **2026-07-04**), QCOM (event-driven)
  and SYNA (pairs-cointegration), both revalidate_by **2026-07-10** — all execution-quarantined.
  SNDK newly VALIDATED-claimed by momentum_macd_histogram (Sharpe 2.254).
- **Positions (read time):** 5 longs — AVGO 26 (avg $377.27, −2.99%), MU 7 (avg $982.90,
  **+14.86%**), ORCL 38 (avg $177.28, **−15.98%**), QQQ 28 (avg $647.96, +9.00%), SPY 35
  (avg $708.81, +3.18%; **SELL 35 submitted, pending fill**).
- **Open orders:** 1 live (SPY SELL 35, order_id `f2d8e13e-...`) — `cli open-orders` can't parse
  it (bug reopened).
- **Account:** equity $103,770.30, cash $35,318.52, buying power $332,939.05.
- **Regime:** bull, conf 0.72, ADX 21.52.
- **Code changes:** none. **Manual changes:** none. **Strategy changes:** none (claim changes via
  triage only).

## Open issues for the operator

1. **[HIGH, UNRESOLVED] Bare `python3` is broken — scheduled task runs the wrong interpreter.**
   Homebrew `/opt/homebrew/bin/python3` = 3.14.5, lacks harness deps. daily_prompt + the Cowork
   task both invoke bare `python3 -m quant_trading_system.cli ...`, which fails at context-build.
   Working interpreter: `/Users/rfoxes/Stock-Trading-Agent/.venv/bin/python3` (3.13.13). **Fix:**
   (a) repoint the task / daily_prompt to `.venv/bin/python3`; (b) pip-install requirements into
   3.14; or (c) recreate `.venv`. Persisting many runs.

2. **News pipeline RECOVERED this run** (6/26 brief fresh, header matched). But it missed 6/22
   AND 6/25 — the health-check / alert on news-agent failure and the `_load_news_brief()`
   staleness guard (Open issue #3) are still warranted so a future miss is visible.

3. **`_load_news_brief()` staleness-guard gap.** Parses `date_in_file` but never compares to
   today, so a stale brief is fed to strategies as live signal. Bit 6/22 and 6/25. Saturday item.

4. **THREE provisional/quarantined claims now — Saturday research owns validation.**
   - **SPCX** (trend-following, volatility_regime, revalidate_by **2026-07-04**, needs ≥60 bars).
     Carry: $25B notes raise, $6.3B Reflection deal, broke $135 IPO price (−32% from peak) amid IG
     bond sell-off, OpenAI reportedly delaying IPO to 2027, Nasdaq-100 add ~July 1.
   - **QCOM** (event-driven, event_catalyst, revalidate_by **2026-07-10**). Investor Day was 6/25.
   - **SYNA** (pairs-cointegration — newly activated, pairs_arbitrage, revalidate_by **2026-07-10**).
     Live merger-arb: onsemi $7B all-stock (1.350 ON/sh, 19% premium, close mid-2027). Textbook
     long SYNA / short ON. This is the activation instance for the standing m_a_arb gap.
   Do NOT hand-promote any of them.

5. **[REOPENED] `cli open-orders` parser bug bites on a live open order.** With the SPY sell live,
   it errors `'dict' object has no attribute 'id'`. Returns clean empty JSON only when no open
   orders. Fix the order-serialization path — the trader can't inspect live orders via the CLI.

6. **MU held +14.86% (gave back from +20.95%); trailing stop did NOT fire.** Watch the post-print
   IV-crush / further give-back as the scenario where the trailing stop could finally engage;
   reconcile any rule-driven trim. No discretionary action.

7. **ORCL −15.98% (−$1,077) and deepening — no active rule can act.** Restructuring event has no
   responder; event_driven_catalyst (claims ORCL) models earnings windows only. Material drawdown
   on a held name with no handle — elevate the restructuring/workforce-reduction gap for Saturday.

## Git-sync status

Ran `cli git-sync --agent trader --message "..."` (via venv) as last action. State files changed
(last_handoff.md, tasks.md) plus the triage-updated active_strategies.md / provisional_claims.md.
Reminder: git-sync queues a JSON marker to `.git-sync-queue/`; the operator's launchd LaunchAgent
runs the actual git push. If real markers pile up across runs, the LaunchAgent isn't installed
(`bash scripts/install_git_safety.sh`).
