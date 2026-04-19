"""Trade-related data models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class TimeInForce(str, Enum):
    DAY = "day"
    GTC = "gtc"
    IOC = "ioc"
    FOK = "fok"


class OrderStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    DRY_RUN = "dry_run"


class TradingMode(str, Enum):
    PAPER = "paper"
    LIVE = "live"
    DRY_RUN = "dry_run"


class OrderRequest(BaseModel):
    """An order request from a trading agent."""

    symbol: str
    side: OrderSide
    qty: float
    order_type: OrderType = OrderType.MARKET
    time_in_force: TimeInForce = TimeInForce.DAY
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    agent_name: str = ""
    strategy_name: str = ""
    reasoning: str = ""


class OrderResult(BaseModel):
    """Result of an order submission through the safety gate."""

    order_id: str = ""
    status: OrderStatus
    mode: TradingMode
    filled_qty: float = 0.0
    filled_avg_price: float = 0.0
    submitted_at: datetime = Field(default_factory=datetime.now)
    safety_checks_passed: list[str] = Field(default_factory=list)
    safety_checks_failed: list[str] = Field(default_factory=list)
    rejection_reason: str = ""
    original_request: Optional[OrderRequest] = None


class TradeRecord(BaseModel):
    """A completed trade record for logging and analysis."""

    trade_id: str
    order_id: str
    symbol: str
    side: OrderSide
    qty: float
    price: float
    mode: TradingMode
    agent_name: str
    strategy_name: str
    reasoning: str
    timestamp: datetime = Field(default_factory=datetime.now)
    pnl: Optional[float] = None
