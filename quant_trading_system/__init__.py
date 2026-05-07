"""Single-agent quantitative paper-trading harness."""

__version__ = "0.2.0"

# Install a structlog shim into sys.modules so the harness can run inside the
# Cowork Linux sandbox where structlog isn't pip-installable. If real structlog
# IS available, prefer it.
import sys as _sys

if "structlog" not in _sys.modules:
    try:  # pragma: no cover
        import structlog as _real_structlog  # noqa: F401
    except ImportError:
        from quant_trading_system import _structlog_shim as _shim

        _sys.modules["structlog"] = _shim
        _sys.modules["structlog.contextvars"] = _shim.contextvars  # type: ignore[assignment]
        _sys.modules["structlog.stdlib"] = _shim.stdlib  # type: ignore[assignment]
