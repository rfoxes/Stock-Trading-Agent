"""FastAPI dashboard application."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from quant_trading_system.dashboard.event_bus import event_bus

if TYPE_CHECKING:
    from quant_trading_system.config import Settings

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# These get set by main.py when the dashboard starts
_settings: Settings | None = None
_kb_client = None
_market_data = None
_regime_classifier = None
_risk_manager = None
_safety_gate = None
_alpaca_client = None


def create_app(
    settings: Settings,
    kb_client=None,
    market_data=None,
    regime_classifier=None,
    risk_manager=None,
    safety_gate=None,
    alpaca_client=None,
) -> FastAPI:
    """Create the FastAPI dashboard app with injected dependencies."""
    global _settings, _kb_client, _market_data, _regime_classifier
    global _risk_manager, _safety_gate, _alpaca_client

    _settings = settings
    _kb_client = kb_client
    _market_data = market_data
    _regime_classifier = regime_classifier
    _risk_manager = risk_manager
    _safety_gate = safety_gate
    _alpaca_client = alpaca_client

    app = FastAPI(title="Trading System Dashboard", docs_url="/api/docs")

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        return templates.TemplateResponse(request, "index.html")

    @app.get("/api/status")
    async def get_status():
        mode = "dry_run" if _settings.DRY_RUN else ("paper" if _settings.ALPACA_PAPER else "live")
        return {
            "mode": mode,
            "llm_provider": _settings.LLM_PROVIDER,
            "llm_model": _settings.OLLAMA_MODEL or _settings.ANALYSIS_MODEL,
            "system_status": event_bus.system_status,
            "cycle_count": event_bus.cycle_count,
            "regime": event_bus.regime,
            "watchlist": _settings.watchlist,
        }

    @app.get("/api/portfolio")
    async def get_portfolio():
        portfolio = event_bus.portfolio
        if not portfolio and _alpaca_client:
            try:
                account = _alpaca_client.get_account()
                positions = _alpaca_client.get_positions()
                portfolio = {
                    "equity": account.get("equity", 0),
                    "cash": account.get("cash", 0),
                    "buying_power": account.get("buying_power", 0),
                    "positions": positions,
                    "unrealized_pnl": sum(p.get("unrealized_pl", 0) for p in positions),
                }
            except Exception:
                portfolio = {
                    "equity": _settings.PAPER_PORTFOLIO_SIZE,
                    "cash": _settings.PAPER_PORTFOLIO_SIZE,
                    "buying_power": _settings.PAPER_PORTFOLIO_SIZE,
                    "positions": [],
                    "unrealized_pnl": 0,
                }
        elif not portfolio:
            portfolio = {
                "equity": _settings.PAPER_PORTFOLIO_SIZE,
                "cash": _settings.PAPER_PORTFOLIO_SIZE,
                "buying_power": _settings.PAPER_PORTFOLIO_SIZE,
                "positions": [],
                "unrealized_pnl": 0,
            }
        return portfolio

    @app.get("/api/orders")
    async def get_orders():
        return {"orders": event_bus.orders}

    @app.get("/api/strategies")
    async def get_strategies():
        if _kb_client is None:
            return {"strategies": []}
        try:
            strats = _kb_client.get_all_strategies()
            return {"strategies": strats}
        except Exception as e:
            return {"strategies": [], "error": str(e)}

    @app.get("/api/backtest-results")
    async def get_backtest_results():
        return {"results": event_bus.backtest_results}

    @app.get("/api/risk")
    async def get_risk():
        risk = event_bus.risk
        if not risk:
            risk = {
                "risk_level": "low",
                "drawdown_pct": 0,
                "sector_exposures": {},
                "circuit_breaker_active": False,
                "warnings": [],
            }
        return risk

    @app.get("/api/regime")
    async def get_regime():
        regime = event_bus.regime
        if not regime and _market_data and _regime_classifier:
            try:
                spy_data = _market_data.get_bars("SPY", "1Day")
                if not spy_data.empty:
                    regime = _regime_classifier.classify(spy_data)
            except Exception:
                pass
        if not regime:
            regime = {"regime": "unknown", "confidence": 0, "indicators": {}, "reasoning": ""}
        return regime

    @app.get("/api/config")
    async def get_config():
        """Return sanitized configuration (no API keys)."""
        return {
            "llm_provider": _settings.LLM_PROVIDER,
            "ollama_model": _settings.OLLAMA_MODEL,
            "ollama_base_url": _settings.OLLAMA_BASE_URL,
            "paper_mode": _settings.ALPACA_PAPER,
            "dry_run": _settings.DRY_RUN,
            "paper_portfolio_size": _settings.PAPER_PORTFOLIO_SIZE,
            "max_position_size_pct": _settings.MAX_POSITION_SIZE_PCT,
            "max_daily_loss_pct": _settings.MAX_DAILY_LOSS_PCT,
            "max_drawdown_pause_pct": _settings.MAX_DRAWDOWN_PAUSE_PCT,
            "max_concurrent_positions": _settings.MAX_CONCURRENT_POSITIONS,
            "watchlist": _settings.watchlist,
            "supervisor_model": _settings.SUPERVISOR_MODEL,
            "analysis_model": _settings.ANALYSIS_MODEL,
            "routing_model": _settings.ROUTING_MODEL,
        }

    @app.get("/api/events")
    async def sse_events():
        """Server-Sent Events stream for real-time updates."""
        return StreamingResponse(
            event_bus.subscribe(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    return app
