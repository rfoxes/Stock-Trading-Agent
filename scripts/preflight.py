"""Pre-flight check for the harness.

Run this once after cloning + installing requirements. It verifies:
  1. All imports resolve.
  2. Strategy markdown files parse cleanly.
  3. State files are present and well-formed.
  4. The trade journal directory is writable.
  5. Anthropic + Alpaca credentials are configured (without making API calls).

It does NOT call the broker or the LLM. Safe to run any time.
Exit code 0 on success, non-zero on first failure.

    python scripts/preflight.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def fail(msg: str) -> None:
    print(f"  ✗ {msg}")
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def warn(msg: str) -> None:
    print(f"  ! {msg}")


def main() -> int:
    print("[1/5] Importing harness modules...")
    try:
        from quant_trading_system import agent_tools, health, journal, memory
        from quant_trading_system import orchestrator, tool_registry
        from quant_trading_system.config import Settings
    except ImportError as e:
        fail(f"import failure: {e}")
    ok("all modules import")

    print("[2/5] Reading strategies from disk...")
    strats = memory.list_strategies()
    if not strats:
        fail("no strategies found in knowledge_base/strategies/")
    parsed_ok = 0
    for s in strats:
        if not s.id or not s.frontmatter:
            print(f"    ! malformed: {s.path}")
            continue
        parsed_ok += 1
    ok(f"{parsed_ok}/{len(strats)} strategies parsed")

    print("[3/5] Checking state files...")
    if not memory.ACTIVE_STRATEGY_FILE.exists():
        fail(f"missing {memory.ACTIVE_STRATEGY_FILE}")
    if not memory.HANDOFF_FILE.exists():
        fail(f"missing {memory.HANDOFF_FILE}")
    if not memory.SUMMARY_FILE.exists():
        fail(f"missing {memory.SUMMARY_FILE}")
    ok("active_strategy.md, last_handoff.md, summary.md all present")

    print("[4/5] Checking writable scratch dirs...")
    memory._ensure_dirs()
    test_path = memory.RUNS_DIR / ".preflight_write_test"
    try:
        test_path.write_text("ok")
        test_path.unlink()
    except OSError as e:
        fail(f"runs/ not writable: {e}")
    test_path = memory.TRADES_DIR / ".preflight_write_test"
    try:
        test_path.write_text("ok")
        test_path.unlink()
    except OSError as e:
        fail(f"trades/ not writable: {e}")
    ok("runs/ and trades/ are writable")

    print("[5/5] Checking credentials in env...")
    settings = Settings(_env_file=str(REPO_ROOT / ".env"))
    if not settings.ALPACA_API_KEY:
        fail("ALPACA_API_KEY not set in .env (paper key required for both modes)")
    if not settings.ALPACA_SECRET_KEY:
        fail("ALPACA_SECRET_KEY not set in .env")
    if not settings.ALPACA_PAPER:
        fail("ALPACA_PAPER must be true (live trading is gated separately)")
    ok("ALPACA paper credentials present")
    if not settings.ANTHROPIC_API_KEY:
        warn(
            "ANTHROPIC_API_KEY not set — that's fine for Cowork mode "
            "(Claude is the orchestrator) but required for standalone mode "
            "(orchestrator.py calls Anthropic directly)."
        )
    else:
        ok("ANTHROPIC_API_KEY present (standalone mode usable)")

    print("\nPre-flight passed. Next steps:")
    print("  Cowork mode:    paste daily_prompt.md into a scheduled task")
    print("  Standalone:     python -m quant_trading_system.orchestrator --dry-run --allow-non-session")
    return 0


if __name__ == "__main__":
    sys.exit(main())
