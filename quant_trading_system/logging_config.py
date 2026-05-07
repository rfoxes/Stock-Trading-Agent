"""Logging setup — stdlib only.

The previous structlog-based setup needed processors and renderers that
aren't in the Cowork sandbox. This is a thin stdlib version that covers
the same two formats (console and json).
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime

from quant_trading_system.config import Settings


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


_CONSOLE_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging(settings: Settings) -> None:
    """Configure root logger with the requested format and level."""
    root = logging.getLogger()
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    if settings.LOG_FORMAT == "json":
        handler.setFormatter(_JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(_CONSOLE_FMT, datefmt="%Y-%m-%dT%H:%M:%S"))

    root.addHandler(handler)
    root.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
