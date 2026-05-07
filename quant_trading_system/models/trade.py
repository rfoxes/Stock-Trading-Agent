"""Trade-related data models.

Plain dataclasses + enums — no pydantic dependency, so this works inside the
Cowork Linux sandbox.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


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


def _enum_value(v: Any) -> Any:
    if isinstance(v, Enum):
        return v.value
    return v


def _serialize(obj: Any) -> Any:
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize(v) for v in obj]
    return obj


@dataclass
class OrderRequest:
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

    def __post_init__(self) -> None:
        # Coerce string inputs into enum values for ergonomic construction
        if isinstance(self.side, str):
            self.side = OrderSide(self.side)
        if isinstance(self.order_type, str):
            self.order_type = OrderType(self.order_type)
        if isinstance(self.time_in_force, str):
            self.time_in_force = TimeInForce(self.time_in_force)

    def model_dump(self) -> dict[str, Any]:
        """Compat shim for the previous pydantic API."""
        return _serialize(asdict(self))


@dataclass
class OrderResult:
    """Result of an order submission through the safety gate."""

    status: OrderStatus
    mode: TradingMode
    order_id: str = ""
    filled_qty: float = 0.0
    filled_avg_price: float = 0.0
    submitted_at: datetime = field(default_factory=datetime.now)
    safety_checks_passed: list[str] = field(default_factory=list)
    safety_checks_failed: list[str] = field(default_factory=list)
    rejection_reason: str = ""
    original_request: Optional[OrderRequest] = None

    def model_dump(self) -> dict[str, Any]:
        return _serialize(asdict(self))


@dataclass
class TradeRecord:
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
    timestamp: datetime = field(default_factory=datetime.now)
    pnl: Optional[float] = None

    def __post_init__(self) -> None:
        if isinstance(self.side, str):
            self.side = OrderSide(self.side)
        if isinstance(self.mode, str):
            self.mode = TradingMode(self.mode)

    def model_dump(self) -> dict[str, Any]:
        return _serialize(asdict(self))
