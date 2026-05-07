"""Thin entry point. Delegates to the orchestrator harness.

Equivalent to `python -m quant_trading_system.orchestrator`.
"""

from __future__ import annotations

from quant_trading_system.orchestrator import main

if __name__ == "__main__":
    raise SystemExit(main())
