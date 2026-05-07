"""The harness — a single Claude agent loop that runs once per scheduled wake.

Each invocation is a fully self-contained run:
    1. Acquire lockfile (refuse to run twice in parallel).
    2. Initialize broker / market data / safety gate / regime classifier.
    3. Build system prompt + initial user message from on-disk memory.
    4. Run the Anthropic tool-use loop until the model stops calling tools.
    5. Persist the full transcript to runs/<timestamp>.json.
    6. Release the lock and exit.

There is intentionally no daemon and no in-memory state between runs. Whatever
the agent wants to remember tomorrow it must write to disk today via tools.

CLI:
    python -m quant_trading_system.orchestrator [--dry-run] [--allow-non-session]

Env (via .env):
    ANTHROPIC_API_KEY   — required
    ALPACA_API_KEY      — paper trading key
    ALPACA_SECRET_KEY   — paper trading secret
    ALPACA_PAPER=true   — default; flip with explicit live-money flags only
    DRY_RUN=true        — skip broker submission entirely
    SUPERVISOR_MODEL    — Anthropic model id, default claude-sonnet-4-5
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import traceback
import uuid
from pathlib import Path
from typing import Any

import structlog

from quant_trading_system import memory
from quant_trading_system.agent_tools import ToolContext
from quant_trading_system.config import Settings
from quant_trading_system.logging_config import setup_logging
from quant_trading_system.tool_registry import TOOLS, get_tool_function

logger = structlog.get_logger("orchestrator")

# Hard ceilings — even if the model loops, we won't run forever.
MAX_TURNS = 60
MAX_TOOL_CALLS = 120
DEFAULT_MAX_TOKENS = 4096


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are the autonomous trading orchestrator for a quantitative paper-trading harness.

# Your role

You wake once per scheduled day (M-F, post-close). In one self-contained run you:
  1. Read the handoff note from yesterday's run, plus recent conclusions.
  2. Reconcile yesterday's positions and orders against today's broker state.
  3. Read the deterministic health signals for the currently-active strategy.
  4. Decide whether to keep the active strategy, modify it, or rotate.
  5. Plan tomorrow's positions and submit any orders to the broker.
  6. Write today's conclusion file (narrative log of what you did and why).
  7. Write a handoff note for tomorrow's Claude.
  8. Stop calling tools — your run ends when you have nothing more to do.

You have no memory between runs. Anything you want tomorrow's Claude to know must
go in `write_conclusion` (full record) and `write_handoff` (short message to next-you).

# Operating rules

**Doing nothing is a valid outcome and is often the correct one.** If today's
check shows the active strategy is healthy, the regime is unchanged, yesterday's
trades are tracking as expected, and there's no compelling new entry signal,
the right decision is to leave everything alone, write a short conclusion saying
so, write the handoff, and stop. Do not submit trades, modify strategy
parameters, or rotate strategies because you feel you should "do something" —
the user explicitly does not want activity-for-activity's-sake. The harness
rewards stability. A run that calls no `submit_order`, no `update_strategy`,
no `set_active_strategy` is a fine run if that's what the data suggests.

When you *do* act, the constraints are:

- ALWAYS paper trading. The system has hard safety gates against live money;
  do not attempt to circumvent them.
- The `submit_order` tool always routes through SafetyGate. Don't try to bypass it.
- Tag every order with the `strategy_id` it implements. Untagged trades cannot
  be evaluated later.
- Position sizing must respect MAX_POSITION_SIZE_PCT (visible via account info).
  When in doubt, use `kelly_position_size` with conservative inputs.
- NEVER open a position without specifying the stop and take-profit plan in
  the order's `reasoning` field. If you can't articulate the exit, don't enter.
- Strategy persistence: the active strategy persists across days. ONLY rotate
  when the active strategy's deterministic health signals breach its declared
  thresholds, OR when the regime has clearly changed. Be conservative — the
  cost of churn is real, and a single bad day is not a reason to rotate.
- Edit strategy markdown files only when there's a concrete lesson worth
  recording. Cosmetic edits or speculative parameter tweaks are noise.
- Run is post-close (US market closed for the day). Submit orders intended
  for the next session with `time_in_force='day'` (limit/stop) or, for
  market-on-open, market orders accept being queued by Alpaca.
- If the broker is unavailable or returns errors, do NOT panic-modify
  strategies. Document the issue in the conclusion and stop.

# Workflow you should follow each run

  Step 1. Read the handoff note (`read_handoff`).
  Step 2. Read recent conclusions (`read_recent_conclusions`, days=14).
  Step 3. Read the active strategy (`get_active_strategy`).
  Step 4. Get current broker state (`get_account`, `get_positions`, `get_open_orders`).
  Step 5. Reconcile — if a position you opened yesterday is no longer present,
          call `log_trade_closed` with the realized pnl so future health signals
          can attribute it.
  Step 6. Read the active strategy's health (`get_strategy_health`). If
          thresholds_breached is non-empty, consider rotating.
  Step 7. Read regime (`classify_regime`). If the regime no longer matches the
          active strategy's preferred regime, consider rotating.
  Step 8. If rotating, call `list_strategies(status='active')`, read candidates
          with `read_strategy`, and call `set_active_strategy` with a clear reason.
  Step 9. Plan tomorrow's trades using the active strategy's rules + current
          market data. Submit through `submit_order` with stop+target reasoning.
  Step 10. Call `write_conclusion` with a narrative record of the run.
  Step 11. Call `write_handoff` with a short message for tomorrow's Claude
           ("here's what's open, here's what to watch, here's the open question").
  Step 12. Stop. Do not call any further tools.

# Output

When you stop calling tools, your final assistant message will end the run.
Keep it short — the conclusion file is the durable record.
"""


# ---------------------------------------------------------------------------
# Lockfile
# ---------------------------------------------------------------------------


class LockHeld(Exception):
    """Raised when another harness run is already in progress."""


def acquire_lock(path: Path, *, force: bool = False) -> Path:
    """Create a sentinel lockfile; refuse if it already exists.

    Stale locks (>4h old) are auto-cleared. Pass `force=True` to override.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        age = time.time() - path.stat().st_mtime
        if age < 4 * 3600 and not force:
            raise LockHeld(
                f"Lockfile present at {path} (age {int(age)}s). "
                "Another run may be in progress. Pass --force to override."
            )
        logger.warning("clearing_stale_lock", path=str(path), age_s=int(age))
        path.unlink(missing_ok=True)
    path.write_text(f"{os.getpid()}\n{dt.datetime.now().isoformat()}\n", encoding="utf-8")
    return path


def release_lock(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except Exception as e:
        logger.warning("lock_release_failed", error=str(e))


# ---------------------------------------------------------------------------
# Component initialization
# ---------------------------------------------------------------------------


def _init_components(settings: Settings):
    """Create market data, regime, alpaca, safety gate."""
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.brokers.safety_gate import SafetyGate
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.data.regime_classifier import RegimeClassifier

    market_data = MarketDataService(settings)
    regime = RegimeClassifier()

    alpaca = None
    if settings.ALPACA_API_KEY and not settings.DRY_RUN:
        try:
            alpaca = AlpacaClient(settings)
        except Exception as e:
            logger.warning("alpaca_init_failed", error=str(e))

    safety_gate = SafetyGate(settings, alpaca)

    return market_data, regime, alpaca, safety_gate


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


def _run_tool(ctx: ToolContext, name: str, args: dict[str, Any]) -> dict[str, Any]:
    fn = get_tool_function(name)
    if fn is None:
        return {"ok": False, "error": f"unknown tool: {name}"}
    try:
        return fn(ctx, **args)
    except TypeError as e:
        return {"ok": False, "error": f"tool argument error: {e}"}
    except Exception as e:
        logger.error("tool_exception", tool=name, error=str(e), traceback=traceback.format_exc())
        return {"ok": False, "error": f"tool failed: {e}"}


# ---------------------------------------------------------------------------
# Main agent loop
# ---------------------------------------------------------------------------


def _build_initial_user_message(run_id: str) -> str:
    today = dt.date.today().isoformat()
    now_iso = dt.datetime.now().astimezone().isoformat()
    return (
        f"# Run {run_id}\n\n"
        f"Today is {today}. Local time: {now_iso}.\n\n"
        "Begin your normal workflow: read the handoff, then recent conclusions, "
        "then the active strategy and broker state. Reconcile yesterday's "
        "positions before deciding anything new. End with `write_conclusion` "
        "then `write_handoff`, then stop."
    )


def run_orchestrator(
    settings: Settings,
    *,
    allow_non_session: bool = False,
    force_lock: bool = False,
) -> dict[str, Any]:
    """Run one orchestrator pass and return a summary dict."""
    setup_logging(settings)
    run_id = uuid.uuid4().hex[:8]
    structlog.contextvars.bind_contextvars(run_id=run_id)
    logger.info("run_start", dry_run=settings.DRY_RUN, paper=settings.ALPACA_PAPER)

    # Skip on non-session days (weekend / NYSE holiday) unless overridden.
    if not allow_non_session:
        try:
            import exchange_calendars as xcals

            nyse = xcals.get_calendar("XNYS")
            today = dt.date.today()
            if not nyse.is_session(today):
                logger.info("non_session_day_skip", date=today.isoformat())
                return {"skipped": True, "reason": "non_session_day"}
        except ImportError:
            # No calendar lib — fall back to weekday check
            if dt.date.today().weekday() >= 5:
                logger.info("weekend_skip")
                return {"skipped": True, "reason": "weekend"}

    # Acquire run lock
    lock_path = acquire_lock(memory.LOCK_FILE, force=force_lock)

    transcript: list[dict[str, Any]] = []
    try:
        market_data, regime, alpaca, safety_gate = _init_components(settings)
        ctx = ToolContext(
            settings=settings,
            market_data=market_data,
            regime_classifier=regime,
            safety_gate=safety_gate,
            alpaca_client=alpaca,
            run_id=run_id,
        )

        # --- Anthropic client ---
        try:
            from anthropic import Anthropic
        except ImportError:
            return {"error": "anthropic SDK not installed. pip install anthropic"}

        if not settings.ANTHROPIC_API_KEY:
            return {"error": "ANTHROPIC_API_KEY not set"}

        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        model = settings.SUPERVISOR_MODEL or "claude-sonnet-4-6"

        # --- Build initial messages ---
        initial_user = _build_initial_user_message(run_id)
        messages: list[dict[str, Any]] = [
            {"role": "user", "content": initial_user}
        ]
        transcript.append({"role": "user", "content": initial_user})

        # --- Loop ---
        turns = 0
        tool_calls = 0
        stop_reason = None
        final_text = ""

        while turns < MAX_TURNS and tool_calls < MAX_TOOL_CALLS:
            turns += 1
            logger.info("turn_start", turn=turns)
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=messages,
                )
            except Exception as e:
                logger.error("anthropic_error", error=str(e))
                transcript.append({"role": "system", "error": f"anthropic_error: {e}"})
                break

            stop_reason = response.stop_reason
            assistant_blocks = []
            text_chunks = []
            tool_uses = []
            for block in response.content:
                if block.type == "text":
                    assistant_blocks.append({"type": "text", "text": block.text})
                    text_chunks.append(block.text)
                elif block.type == "tool_use":
                    assistant_blocks.append({
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    })
                    tool_uses.append(block)

            messages.append({"role": "assistant", "content": response.content})
            transcript.append({
                "role": "assistant",
                "stop_reason": stop_reason,
                "blocks": assistant_blocks,
            })
            if text_chunks:
                final_text = "\n".join(text_chunks)

            if stop_reason == "end_turn" and not tool_uses:
                logger.info("agent_stopped", turn=turns, reason=stop_reason)
                break

            if not tool_uses:
                # Stop reason something else and no tools requested — bail
                logger.info("loop_end_no_tools", stop_reason=stop_reason)
                break

            # Execute tool calls
            tool_results_msg = []
            for tu in tool_uses:
                tool_calls += 1
                logger.info("tool_call", name=tu.name, args_keys=list(tu.input.keys()))
                result = _run_tool(ctx, tu.name, tu.input)
                tool_results_msg.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": json.dumps(result, default=str),
                })
                transcript.append({
                    "role": "tool_result",
                    "tool_use_id": tu.id,
                    "name": tu.name,
                    "input": tu.input,
                    "result": result,
                })
            messages.append({"role": "user", "content": tool_results_msg})

        if turns >= MAX_TURNS or tool_calls >= MAX_TOOL_CALLS:
            logger.warning("max_turns_or_calls_hit", turns=turns, tool_calls=tool_calls)
            transcript.append({
                "role": "system",
                "warning": f"hit ceiling: turns={turns}, tool_calls={tool_calls}",
            })

        return {
            "run_id": run_id,
            "turns": turns,
            "tool_calls": tool_calls,
            "stop_reason": stop_reason,
            "final_text": final_text,
            "transcript": transcript,
        }
    finally:
        release_lock(lock_path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _persist_run_log(result: dict[str, Any], run_id: str) -> Path:
    memory._ensure_dirs()
    fname = f"{dt.datetime.now().strftime('%Y-%m-%d-%H%M')}-{run_id}.json"
    path = memory.RUNS_DIR / fname
    path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Daily quant trading harness — one orchestrator pass."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Force DRY_RUN regardless of .env. SafetyGate will simulate orders.",
    )
    parser.add_argument(
        "--allow-non-session",
        action="store_true",
        help="Run even on weekends / NYSE holidays (useful for testing).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Override an existing lockfile.",
    )
    args = parser.parse_args()

    settings = Settings(_env_file=".env")
    if args.dry_run:
        settings.DRY_RUN = True

    try:
        result = run_orchestrator(
            settings,
            allow_non_session=args.allow_non_session,
            force_lock=args.force,
        )
    except LockHeld as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"FATAL: {e}\n{traceback.format_exc()}", file=sys.stderr)
        return 2

    if result.get("skipped"):
        print(f"Skipped: {result.get('reason')}")
        return 0

    log_path = _persist_run_log(result, result.get("run_id", "unknown"))
    print(f"Run complete. Log: {log_path}")
    if "error" in result:
        print(f"  error: {result['error']}", file=sys.stderr)
        return 3
    print(f"  turns: {result.get('turns')}, tool_calls: {result.get('tool_calls')}")
    if result.get("final_text"):
        print(f"\n--- final assistant message ---\n{result['final_text']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
