"""Minimal structlog-compatible API on top of stdlib logging.

The Cowork sandbox doesn't have structlog installed, but several harness
modules (`safety_gate`, `data/*`, `journal`, `health`, etc.) call into a
structlog-style API: ``structlog.get_logger(__name__)``, ``logger.bind(**ctx)``,
``logger.info("event", key=value, ...)``, ``structlog.contextvars.bind_contextvars(...)``.

Rewriting every call site would be a big mechanical change. Instead, this
module provides just enough of the structlog surface that those calls work,
backed by stdlib ``logging``.

Registered as ``sys.modules["structlog"]`` from ``quant_trading_system/__init__.py``
so plain ``import structlog`` succeeds.
"""

from __future__ import annotations

import logging
from typing import Any


def _format_kv(message: str, kwargs: dict[str, Any]) -> str:
    if not kwargs:
        return message
    extras = " ".join(f"{k}={v!r}" for k, v in kwargs.items())
    return f"{message} {extras}"


class _BoundLogger:
    """Thin wrapper exposing structlog-style ``info("event", **kwargs)`` over stdlib."""

    def __init__(self, logger: logging.Logger, context: dict[str, Any] | None = None) -> None:
        self._logger = logger
        self._ctx = context or {}

    def bind(self, **kwargs: Any) -> "_BoundLogger":
        return _BoundLogger(self._logger, {**self._ctx, **kwargs})

    def unbind(self, *keys: str) -> "_BoundLogger":
        new = {k: v for k, v in self._ctx.items() if k not in keys}
        return _BoundLogger(self._logger, new)

    def new(self, **kwargs: Any) -> "_BoundLogger":
        return _BoundLogger(self._logger, dict(kwargs))

    def _emit(self, level: int, message: str, **kwargs: Any) -> None:
        merged = {**self._ctx, **kwargs}
        self._logger.log(level, _format_kv(str(message), merged))

    def debug(self, message: str, **kwargs: Any) -> None:
        self._emit(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self._emit(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._emit(logging.WARNING, message, **kwargs)

    warn = warning

    def error(self, message: str, **kwargs: Any) -> None:
        self._emit(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self._emit(logging.CRITICAL, message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        merged = {**self._ctx, **kwargs}
        self._logger.exception(_format_kv(str(message), merged))


def get_logger(name: str = "harness", *args: Any, **kwargs: Any) -> _BoundLogger:
    """Return a structlog-style bound logger backed by stdlib logging."""
    return _BoundLogger(logging.getLogger(name))


# ---------------------------------------------------------------------------
# structlog.contextvars compatibility
# ---------------------------------------------------------------------------


class _ContextvarsModule:
    """No-op stand-in for structlog.contextvars."""

    def bind_contextvars(self, **kwargs: Any) -> None:
        # We don't propagate context across stdlib logging here. The shim is
        # best-effort; callers' bound loggers still carry their context.
        return None

    def clear_contextvars(self) -> None:
        return None

    def merge_contextvars(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {}


contextvars = _ContextvarsModule()


# ---------------------------------------------------------------------------
# Other commonly-imported attributes (no-op or trivial)
# ---------------------------------------------------------------------------


class _StdlibProcessor:
    """Placeholder so ``structlog.stdlib.LoggerFactory()`` etc. don't crash."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self


class _StdlibModule:
    LoggerFactory = _StdlibProcessor
    BoundLogger = _BoundLogger
    add_log_level = _StdlibProcessor()
    filter_by_level = _StdlibProcessor()


stdlib = _StdlibModule()


def configure(*args: Any, **kwargs: Any) -> None:
    """Accept and ignore structlog.configure(...) calls."""
    return None


def make_filtering_bound_logger(*args: Any, **kwargs: Any) -> Any:
    return _BoundLogger


def reset_defaults() -> None:
    return None
