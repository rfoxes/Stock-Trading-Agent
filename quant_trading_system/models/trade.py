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
class OptionsOrderRequest:
    """A multi-leg options order request from a trading agent.

    Each entry in `legs` is a dict with:
        contract_symbol: OCC-format option symbol (e.g. AAPL250620C00150000)
        side: "buy" | "sell"
        ratio: int (typically 1; some structures use other ratios)
    `qty` is the multiplier — total contracts per leg = leg.ratio * qty.

    For now we represent legs as dicts to keep the dataclass JSON-friendly;
    the helper `quant_trading_system.options.OptionLeg` is the structured form
    strategies construct internally.
    """

    qty: int                                   # multiplier across all legs
    legs: list[dict[str, Any]] = field(default_factory=list)
    order_class: str = "mleg"                  # alpaca uses "mleg" for multi-leg
    time_in_force: TimeInForce = TimeInForce.DAY
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[float] = None        # net debit/credit for the spread
    agent_name: str = ""
    strategy_name: str = ""
    reasoning: str = ""
    # For SafetyGate's defined-risk check: strategies declare what their max
    # loss is. None means "undefined risk" — requires explicit strategy flag.
    declared_max_loss_usd: Optional[float] = None
    allow_undefined_risk: bool = False         # set by strategy if applicable

    def __post_init__(self) -> None:
        if isinstance(self.time_in_force, str):
            self.time_in_force = TimeInForce(self.time_in_force)
        if isinstance(self.order_type, str):
            self.order_type = OrderType(self.order_type)
        if self.qty < 1:
            raise ValueError(f"qty must be >= 1, got {self.qty}")
        if not self.legs:
            raise ValueError("options order must have at least one leg")
        for i, leg in enumerate(self.legs):
            if not isinstance(leg, dict):
                raise ValueError(f"leg {i} must be a dict")
            for key in ("contract_symbol", "side"):
                if key not in leg:
                    raise ValueError(f"leg {i} missing required key {key!r}")
            if leg["side"].lower() not in ("buy", "sell"):
                raise ValueError(f"leg {i} side must be buy/sell")

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
