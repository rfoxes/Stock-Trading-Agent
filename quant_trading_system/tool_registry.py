"""Anthropic tool definitions (JSON schemas) for the orchestrator.

Each entry pairs an Anthropic tool spec (what the LLM sees) with the Python
callable that implements it (defined in agent_tools.py).

Tool descriptions are written for the model — be specific about when to use
each tool, what it returns, and any pitfalls. Verbose descriptions reduce the
amount of trial-and-error the model needs.
"""

from __future__ import annotations

from typing import Any, Callable

from quant_trading_system.agent_tools import TOOL_FUNCTIONS, ToolContext

# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS: list[dict[str, Any]] = [
    # -- Strategy I/O ------------------------------------------------------
    {
        "name": "list_strategies",
        "description": (
            "List trading strategies on disk. Returns a compact summary of each "
            "(id, name, type, status, timeframe, market_regime). Use this to see "
            "what's available before reading any single one in detail."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by status (active, testing, deprecated, archived).",
                    "enum": ["active", "testing", "deprecated", "proposed", "archived"],
                },
                "type": {
                    "type": "string",
                    "description": "Filter by type.",
                    "enum": ["equity", "options"],
                },
                "include_archived": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "read_strategy",
        "description": (
            "Read the full markdown of a single strategy: its YAML frontmatter "
            "(parameters, thresholds, risk_management, indicators) and the prose body "
            "with entry/exit rules and rationale. Call this before deciding to use, "
            "modify, or archive a strategy."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id"],
            "properties": {
                "strategy_id": {"type": "string"},
            },
        },
    },
    {
        "name": "update_strategy",
        "description": (
            "Edit an existing strategy file. Provide either `frontmatter_updates` "
            "(merged into existing frontmatter), `body` (full markdown body "
            "replacement), or both. Use this to record parameter tweaks, threshold "
            "updates, or new lessons learned in the body. "
            "DO NOT rewrite the body wholesale unless the rationale truly changed."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id"],
            "properties": {
                "strategy_id": {"type": "string"},
                "frontmatter_updates": {
                    "type": "object",
                    "description": "Top-level keys to merge into existing frontmatter.",
                },
                "body": {
                    "type": "string",
                    "description": "Optional full replacement of the markdown body.",
                },
            },
        },
    },
    {
        "name": "create_strategy",
        "description": (
            "Create a new strategy file. Use only when proposing a genuinely new "
            "approach. New strategies should start with status='testing' and clear "
            "thresholds in frontmatter."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id", "type", "frontmatter", "body"],
            "properties": {
                "strategy_id": {"type": "string", "description": "Snake_case id, e.g. 'rsi_pullback'."},
                "type": {"type": "string", "enum": ["equity", "options"]},
                "frontmatter": {"type": "object", "description": "YAML frontmatter contents."},
                "body": {"type": "string", "description": "Markdown body."},
            },
        },
    },
    {
        "name": "archive_strategy",
        "description": (
            "Move a strategy to the archived/ subdir and set status=archived. "
            "Always pass a `reason`. Use when a strategy has consistently failed its "
            "thresholds and you've decided to retire it."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id", "reason"],
            "properties": {
                "strategy_id": {"type": "string"},
                "reason": {"type": "string"},
            },
        },
    },
    # -- Conclusions / state ----------------------------------------------
    {
        "name": "write_conclusion",
        "description": (
            "Write today's conclusion file (knowledge_base/conclusions/YYYY-MM-DD.md). "
            "This is a narrative record of: what you decided today, why, and what you "
            "did. Use clear prose. Always do this before write_handoff."
        ),
        "input_schema": {
            "type": "object",
            "required": ["content"],
            "properties": {"content": {"type": "string"}},
        },
    },
    {
        "name": "append_conclusion",
        "description": (
            "Append to today's conclusion file. Useful if you want to add a "
            "follow-up note after taking another tool action."
        ),
        "input_schema": {
            "type": "object",
            "required": ["content"],
            "properties": {"content": {"type": "string"}},
        },
    },
    {
        "name": "read_recent_conclusions",
        "description": (
            "Return the last N daily conclusion files. Read these to understand "
            "what previous Claude runs were thinking and what they did."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"days": {"type": "integer", "default": 14}},
        },
    },
    {
        "name": "read_handoff",
        "description": (
            "Read the handoff note from yesterday's Claude. This is your direct "
            "message from the previous run — read it first before deciding anything."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "write_handoff",
        "description": (
            "Write the handoff note for tomorrow's Claude. ALWAYS call this last, "
            "after write_conclusion. Include: what's open, what to watch for, any "
            "open questions you'd want a fresh perspective on tomorrow."
        ),
        "input_schema": {
            "type": "object",
            "required": ["content"],
            "properties": {"content": {"type": "string"}},
        },
    },
    {
        "name": "get_active_strategy",
        "description": (
            "Return the currently-active strategy: its id, when it was activated, "
            "and the original reason."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "set_active_strategy",
        "description": (
            "Switch the active strategy. ONLY do this when the current strategy's "
            "deterministic health signals have breached its declared thresholds, OR "
            "when the market regime has changed in a way that clearly disqualifies "
            "the current strategy. Always include a concrete `reason`."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id", "reason"],
            "properties": {
                "strategy_id": {"type": "string"},
                "reason": {"type": "string"},
                "notes": {"type": "string"},
            },
        },
    },
    {
        "name": "read_summary",
        "description": "Read the rolling long-horizon summary of the system's behavior.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "update_summary",
        "description": (
            "Replace the rolling summary file. Update only when there's a real new "
            "longer-term lesson worth carrying forward — not every day."
        ),
        "input_schema": {
            "type": "object",
            "required": ["content"],
            "properties": {"content": {"type": "string"}},
        },
    },
    # -- Market ------------------------------------------------------------
    {
        "name": "get_bars",
        "description": (
            "Get recent OHLCV bars for a symbol. Returns up to the last 60 rows. "
            "Use 1Day for swing-horizon analysis."
        ),
        "input_schema": {
            "type": "object",
            "required": ["symbol"],
            "properties": {
                "symbol": {"type": "string"},
                "timeframe": {
                    "type": "string",
                    "enum": ["1Min", "5Min", "15Min", "1Hour", "1Day", "1Week"],
                    "default": "1Day",
                },
                "lookback_days": {"type": "integer", "default": 60},
            },
        },
    },
    {
        "name": "classify_regime",
        "description": (
            "Classify the current market regime (bull/bear/sideways/volatile) "
            "using a benchmark symbol's daily bars. Returns regime, confidence, "
            "and the underlying indicator values."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"symbol": {"type": "string", "default": "SPY"}},
        },
    },
    {
        "name": "compute_indicator",
        "description": (
            "Compute the most recent value of a single technical indicator. "
            "Supported: sma, ema, rsi, macd, bbands, atr, adx, obv. Returns the "
            "value (or component values for macd/bbands)."
        ),
        "input_schema": {
            "type": "object",
            "required": ["symbol", "indicator"],
            "properties": {
                "symbol": {"type": "string"},
                "indicator": {
                    "type": "string",
                    "enum": ["sma", "ema", "rsi", "macd", "bbands", "atr", "adx", "obv"],
                },
                "period": {"type": "integer"},
                "lookback_days": {"type": "integer", "default": 250},
            },
        },
    },
    {
        "name": "get_quote",
        "description": "Latest bid/ask for a symbol from the broker. May be unavailable outside market hours.",
        "input_schema": {
            "type": "object",
            "required": ["symbol"],
            "properties": {"symbol": {"type": "string"}},
        },
    },
    {
        "name": "market_status",
        "description": "Whether the US equities market is open right now and the next session open time.",
        "input_schema": {"type": "object", "properties": {}},
    },
    # -- Portfolio ---------------------------------------------------------
    {
        "name": "get_account",
        "description": "Account equity, cash, and buying power.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_positions",
        "description": "All currently-held positions with unrealized P&L.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_open_orders",
        "description": (
            "All open orders on the broker. Includes orders queued for the next "
            "session (e.g. submitted post-close with tif=opg)."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_recent_trades",
        "description": (
            "Read journal events: order submissions, rejections, closes. Filter by "
            "strategy_id if you want one strategy's recent activity."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "default": 30},
                "strategy_id": {"type": "string"},
            },
        },
    },
    {
        "name": "get_strategy_health",
        "description": (
            "Deterministic health snapshot for one strategy: order counts, win rate, "
            "rolling Sharpe, max drawdown, P&L vs SPY, and which thresholds (if "
            "declared in frontmatter) are currently breached. Read this before "
            "deciding whether to switch."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id"],
            "properties": {
                "strategy_id": {"type": "string"},
                "lookback_days": {"type": "integer", "default": 30},
            },
        },
    },
    {
        "name": "get_portfolio_health",
        "description": (
            "Cheap top-level snapshot across all active strategies. Useful as your "
            "first portfolio-wide read each morning."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"lookback_days": {"type": "integer", "default": 30}},
        },
    },
    # -- Sizing ------------------------------------------------------------
    {
        "name": "kelly_position_size",
        "description": (
            "Convert a Kelly-style edge estimate into a concrete share count. "
            "Defaults to half-Kelly (fraction=0.5). Always capped at MAX_POSITION_SIZE_PCT."
        ),
        "input_schema": {
            "type": "object",
            "required": ["win_rate", "avg_win", "avg_loss", "price_per_share"],
            "properties": {
                "win_rate": {"type": "number", "description": "0–1"},
                "avg_win": {"type": "number", "description": "Average win as a fraction of capital risked, e.g. 0.03"},
                "avg_loss": {"type": "number", "description": "Average loss as a fraction, positive value"},
                "portfolio_value": {"type": "number"},
                "price_per_share": {"type": "number"},
                "fraction": {"type": "number", "default": 0.5},
                "max_position_pct": {"type": "number"},
            },
        },
    },
    # -- Trading -----------------------------------------------------------
    {
        "name": "submit_order",
        "description": (
            "Submit an order. Always passes through SafetyGate (paper trading + risk "
            "checks). Always tagged with `strategy_id` for attribution. For trades "
            "intended to fire at the next session open after a post-close run, use "
            "order_type='market' with a limit price OR set time_in_force='day'/'gtc' "
            "for limit orders. NEVER submit a position-opening order without an "
            "accompanying stop or take-profit plan documented in `reasoning`."
        ),
        "input_schema": {
            "type": "object",
            "required": ["symbol", "side", "qty", "strategy_id", "reasoning"],
            "properties": {
                "symbol": {"type": "string"},
                "side": {"type": "string", "enum": ["buy", "sell"]},
                "qty": {"type": "number"},
                "order_type": {
                    "type": "string",
                    "enum": ["market", "limit", "stop", "stop_limit"],
                    "default": "market",
                },
                "strategy_id": {"type": "string", "description": "Strategy this trade is attributed to."},
                "time_in_force": {
                    "type": "string",
                    "enum": ["day", "gtc", "ioc", "fok"],
                    "default": "day",
                },
                "limit_price": {"type": "number"},
                "stop_price": {"type": "number"},
                "reasoning": {"type": "string", "description": "Brief: why this trade, what's the stop/target."},
            },
        },
    },
    {
        "name": "cancel_order",
        "description": "Cancel an open order on the broker by id.",
        "input_schema": {
            "type": "object",
            "required": ["order_id"],
            "properties": {"order_id": {"type": "string"}},
        },
    },
    {
        "name": "log_trade_closed",
        "description": (
            "Log that a position closed. Call this when you reconcile yesterday's "
            "open positions vs today's portfolio and notice one is now flat. "
            "Provide realized pnl as a fraction of capital invested (e.g. 0.04 for +4%)."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id", "symbol", "pnl"],
            "properties": {
                "strategy_id": {"type": "string"},
                "symbol": {"type": "string"},
                "pnl": {"type": "number", "description": "Realized return, fraction (e.g. 0.03 = +3%)."},
                "pnl_pct": {"type": "number"},
                "notes": {"type": "string"},
            },
        },
    },
    # -- Backtest ----------------------------------------------------------
    {
        "name": "run_backtest",
        "description": (
            "Run an equity backtest of a strategy on a single symbol. Returns "
            "metrics. Useful when proposing or modifying a strategy — don't "
            "promote a new strategy to active without backtest evidence."
        ),
        "input_schema": {
            "type": "object",
            "required": ["strategy_id", "symbol", "start", "end"],
            "properties": {
                "strategy_id": {"type": "string"},
                "symbol": {"type": "string"},
                "start": {"type": "string", "description": "YYYY-MM-DD"},
                "end": {"type": "string", "description": "YYYY-MM-DD"},
            },
        },
    },
]


def get_tool_function(name: str) -> Callable | None:
    """Look up the Python function for a tool name."""
    return TOOL_FUNCTIONS.get(name)


def all_tool_names() -> list[str]:
    return [t["name"] for t in TOOLS]
