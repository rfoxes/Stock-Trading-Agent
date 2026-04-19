"""Alpaca broker client wrapper with structured logging."""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.models import Order, Position
    from alpaca.trading.requests import (
        GetOrdersRequest,
        LimitOrderRequest,
        MarketOrderRequest,
        StopLimitOrderRequest,
        StopOrderRequest,
    )

    from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)


class AlpacaClient:
    """Wrapper around alpaca-py TradingClient with logging.

    This client should NEVER be called directly by agents.
    All orders must go through SafetyGate.
    """

    def __init__(self, settings: Settings) -> None:
        from alpaca.trading.client import TradingClient

        self._settings = settings
        self._client = TradingClient(
            api_key=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            paper=settings.ALPACA_PAPER,
        )
        logger.info(
            "alpaca_client_initialized",
            paper=settings.ALPACA_PAPER,
        )

    @property
    def trading_client(self) -> TradingClient:
        return self._client

    def get_account(self) -> dict:
        """Get current account information."""
        account = self._client.get_account()
        logger.debug("account_fetched", buying_power=str(account.buying_power))
        return {
            "equity": float(account.equity),
            "buying_power": float(account.buying_power),
            "cash": float(account.cash),
            "portfolio_value": float(account.portfolio_value or account.equity),
            "day_trade_count": account.daytrade_count,
        }

    def get_positions(self) -> list[dict]:
        """Get all current positions."""
        positions: list[Position] = self._client.get_all_positions()
        result = []
        for pos in positions:
            result.append({
                "symbol": pos.symbol,
                "qty": float(pos.qty),
                "side": pos.side.value if pos.side else "long",
                "market_value": float(pos.market_value) if pos.market_value else 0.0,
                "unrealized_pl": float(pos.unrealized_pl) if pos.unrealized_pl else 0.0,
                "unrealized_plpc": float(pos.unrealized_plpc) if pos.unrealized_plpc else 0.0,
                "current_price": float(pos.current_price) if pos.current_price else 0.0,
                "avg_entry_price": float(pos.avg_entry_price) if pos.avg_entry_price else 0.0,
            })
        logger.debug("positions_fetched", count=len(result))
        return result

    def submit_order(
        self,
        order_request: MarketOrderRequest
        | LimitOrderRequest
        | StopOrderRequest
        | StopLimitOrderRequest,
    ) -> Order:
        """Submit an order to Alpaca."""
        logger.info(
            "submitting_order",
            symbol=order_request.symbol,
            qty=str(order_request.qty),
            side=order_request.side.value,
            type=order_request.type.value if order_request.type else "market",
        )
        order = self._client.submit_order(order_request)
        logger.info(
            "order_submitted",
            order_id=str(order.id),
            status=order.status.value if order.status else "unknown",
        )
        return order

    def get_order(self, order_id: str) -> Order:
        """Get order by ID."""
        return self._client.get_order_by_id(order_id)

    def cancel_order(self, order_id: str) -> None:
        """Cancel an order."""
        logger.info("cancelling_order", order_id=order_id)
        self._client.cancel_order_by_id(order_id)

    def get_open_orders(self) -> list[Order]:
        """Get all open orders."""
        from alpaca.trading.requests import GetOrdersRequest
        from alpaca.trading.enums import QueryOrderStatus

        request = GetOrdersRequest(status=QueryOrderStatus.OPEN)
        return self._client.get_orders(request)
