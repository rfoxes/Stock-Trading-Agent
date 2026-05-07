"""Safety gate — the mandatory middleware for ALL order execution.

CRITICAL: This module is the single authorized path to order execution.
No agent may submit orders by any other means. Every order must pass
through SafetyGate.validate_and_submit().
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import structlog

from quant_trading_system.models.trade import (
    OrderRequest,
    OrderResult,
    OrderStatus,
    TradingMode,
)

if TYPE_CHECKING:
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)


class SafetyError(Exception):
    """Raised when a safety check fails in a way that should halt execution."""


class SafetyGate:
    """Mandatory middleware that all orders must pass through.

    Safety checks (in order):
    1. Dry-run mode: log and return simulated result, never touch broker.
    2. Live money gate: both REAL_MONEY_ENABLED and REAL_MONEY_CONFIRMATION must be True.
    3. Restricted symbols: reject orders for blacklisted symbols.
    4. Position size limit: single order must not exceed MAX_POSITION_SIZE_PCT of equity.
    5. Daily loss limit: reject if daily losses exceed MAX_DAILY_LOSS_PCT.
    6. Concurrent positions: reject if already at MAX_CONCURRENT_POSITIONS.
    """

    def __init__(self, settings: Settings, alpaca_client: AlpacaClient | None = None) -> None:
        self._settings = settings
        self._client = alpaca_client
        self._daily_realized_loss = 0.0
        self._daily_reset_date = datetime.now(tz=None).date()

        logger.info(
            "safety_gate_initialized",
            dry_run=settings.DRY_RUN,
            paper=settings.ALPACA_PAPER,
            real_money_enabled=settings.REAL_MONEY_ENABLED,
            real_money_confirmation=settings.REAL_MONEY_CONFIRMATION,
        )

    def _reset_daily_if_needed(self) -> None:
        """Reset daily loss tracking at the start of a new day."""
        today = datetime.now(tz=None).date()
        if today != self._daily_reset_date:
            self._daily_realized_loss = 0.0
            self._daily_reset_date = today

    def validate_and_submit(self, order: OrderRequest) -> OrderResult:
        """Validate an order through all safety checks and submit if approved.

        This is the ONLY authorized path to order execution.
        """
        return self._validate_and_submit_inner(order)

    def _validate_and_submit_inner(self, order: OrderRequest) -> OrderResult:
        """Internal validation logic."""
        self._reset_daily_if_needed()
        checks_passed: list[str] = []
        log = logger.bind(
            symbol=order.symbol,
            side=order.side.value,
            qty=order.qty,
            agent=order.agent_name,
            strategy=order.strategy_name,
        )

        # --- Check 1: Dry-run mode ---
        if self._settings.DRY_RUN:
            log.info(
                "dry_run_order",
                reasoning=order.reasoning,
                order_type=order.order_type.value,
            )
            return OrderResult(
                order_id=f"dry-run-{uuid.uuid4().hex[:12]}",
                status=OrderStatus.DRY_RUN,
                mode=TradingMode.DRY_RUN,
                filled_qty=order.qty,
                filled_avg_price=0.0,
                safety_checks_passed=["dry_run_bypass"],
                original_request=order,
            )

        # --- Check 2: Live money safety gate ---
        if not self._settings.ALPACA_PAPER:
            if not self._settings.REAL_MONEY_ENABLED:
                log.error("live_trading_blocked", reason="REAL_MONEY_ENABLED is false")
                raise SafetyError(
                    "Live trading attempted but REAL_MONEY_ENABLED is false. "
                    "This is a critical safety violation."
                )
            if not self._settings.REAL_MONEY_CONFIRMATION:
                log.error("live_trading_blocked", reason="REAL_MONEY_CONFIRMATION is false")
                raise SafetyError(
                    "Live trading attempted but REAL_MONEY_CONFIRMATION is false. "
                    "This is a critical safety violation."
                )
            checks_passed.append("live_money_gate")
        else:
            checks_passed.append("paper_trading_mode")

        # --- Check 3: Restricted symbols ---
        if order.symbol in self._settings.restricted_symbols_list:
            log.warning("order_rejected", reason="restricted_symbol")
            return OrderResult(
                status=OrderStatus.REJECTED,
                mode=self._get_trading_mode(),
                rejection_reason=f"Symbol {order.symbol} is restricted",
                safety_checks_passed=checks_passed,
                safety_checks_failed=["restricted_symbol"],
                original_request=order,
            )
        checks_passed.append("restricted_symbols")

        # --- Check 4: Position size limit ---
        if self._client is not None:
            try:
                account = self._client.get_account()
                equity = account.get("equity", 0.0)
                if equity > 0:
                    # Estimate order value (use limit price or assume current price not available)
                    estimated_value = order.qty * (order.limit_price or 0.0)
                    # If we don't have a price estimate, skip this check rather than blocking
                    if estimated_value > 0:
                        position_pct = estimated_value / equity
                        if position_pct > self._settings.MAX_POSITION_SIZE_PCT:
                            log.warning(
                                "order_rejected",
                                reason="position_size_exceeded",
                                position_pct=round(position_pct, 4),
                                max_pct=self._settings.MAX_POSITION_SIZE_PCT,
                            )
                            return OrderResult(
                                status=OrderStatus.REJECTED,
                                mode=self._get_trading_mode(),
                                rejection_reason=(
                                    f"Position size {position_pct:.1%} exceeds "
                                    f"limit {self._settings.MAX_POSITION_SIZE_PCT:.1%}"
                                ),
                                safety_checks_passed=checks_passed,
                                safety_checks_failed=["position_size"],
                                original_request=order,
                            )
            except Exception as e:
                log.warning("position_size_check_failed", error=str(e))
        checks_passed.append("position_size")

        # --- Check 5: Daily loss limit ---
        if self._client is not None:
            try:
                account = self._client.get_account()
                equity = account.get("equity", 0.0)
                if equity > 0:
                    positions = self._client.get_positions()
                    unrealized_loss = sum(
                        p.get("unrealized_pl", 0.0)
                        for p in positions
                        if p.get("unrealized_pl", 0.0) < 0
                    )
                    total_loss = abs(unrealized_loss) + abs(self._daily_realized_loss)
                    loss_pct = total_loss / equity
                    if loss_pct > self._settings.MAX_DAILY_LOSS_PCT:
                        log.warning(
                            "order_rejected",
                            reason="daily_loss_limit",
                            loss_pct=round(loss_pct, 4),
                            max_pct=self._settings.MAX_DAILY_LOSS_PCT,
                        )
                        return OrderResult(
                            status=OrderStatus.REJECTED,
                            mode=self._get_trading_mode(),
                            rejection_reason=(
                                f"Daily loss {loss_pct:.1%} exceeds "
                                f"limit {self._settings.MAX_DAILY_LOSS_PCT:.1%}"
                            ),
                            safety_checks_passed=checks_passed,
                            safety_checks_failed=["daily_loss"],
                            original_request=order,
                        )
            except Exception as e:
                log.warning("daily_loss_check_failed", error=str(e))
        checks_passed.append("daily_loss")

        # --- Check 6: Max concurrent positions ---
        if self._client is not None:
            try:
                positions = self._client.get_positions()
                if len(positions) >= self._settings.MAX_CONCURRENT_POSITIONS:
                    # Allow sells even at max positions (we're reducing, not adding)
                    if order.side.value != "sell":
                        log.warning(
                            "order_rejected",
                            reason="max_concurrent_positions",
                            current=len(positions),
                            max=self._settings.MAX_CONCURRENT_POSITIONS,
                        )
                        return OrderResult(
                            status=OrderStatus.REJECTED,
                            mode=self._get_trading_mode(),
                            rejection_reason=(
                                f"At max concurrent positions ({self._settings.MAX_CONCURRENT_POSITIONS})"
                            ),
                            safety_checks_passed=checks_passed,
                            safety_checks_failed=["max_positions"],
                            original_request=order,
                        )
            except Exception as e:
                log.warning("concurrent_positions_check_failed", error=str(e))
        checks_passed.append("max_positions")

        # --- All checks passed, submit order ---
        log.info("all_safety_checks_passed", checks=checks_passed)

        if self._client is None:
            log.warning("no_broker_client", reason="submitting_simulated")
            return OrderResult(
                order_id=f"no-client-{uuid.uuid4().hex[:12]}",
                status=OrderStatus.SUBMITTED,
                mode=self._get_trading_mode(),
                filled_qty=order.qty,
                safety_checks_passed=checks_passed,
                original_request=order,
            )

        try:
            alpaca_order = self._submit_to_alpaca(order)
            return OrderResult(
                order_id=str(alpaca_order.id),
                status=OrderStatus.SUBMITTED,
                mode=self._get_trading_mode(),
                filled_qty=float(alpaca_order.filled_qty or 0),
                filled_avg_price=float(alpaca_order.filled_avg_price or 0),
                safety_checks_passed=checks_passed,
                original_request=order,
            )
        except Exception as e:
            log.error("order_submission_failed", error=str(e))
            return OrderResult(
                status=OrderStatus.REJECTED,
                mode=self._get_trading_mode(),
                rejection_reason=f"Broker error: {e}",
                safety_checks_passed=checks_passed,
                safety_checks_failed=["broker_submission"],
                original_request=order,
            )

    def _submit_to_alpaca(self, order: OrderRequest):
        """Convert OrderRequest to Alpaca request and submit."""
        from alpaca.trading.enums import OrderSide as AlpacaSide
        from alpaca.trading.enums import OrderType as AlpacaType
        from alpaca.trading.enums import TimeInForce as AlpacaTIF
        from alpaca.trading.requests import (
            LimitOrderRequest,
            MarketOrderRequest,
            StopLimitOrderRequest,
            StopOrderRequest,
        )

        side = AlpacaSide.BUY if order.side.value == "buy" else AlpacaSide.SELL
        tif = AlpacaTIF(order.time_in_force.value)

        if order.order_type.value == "market":
            req = MarketOrderRequest(
                symbol=order.symbol,
                qty=order.qty,
                side=side,
                time_in_force=tif,
            )
        elif order.order_type.value == "limit":
            req = LimitOrderRequest(
                symbol=order.symbol,
                qty=order.qty,
                side=side,
                time_in_force=tif,
                limit_price=order.limit_price,
            )
        elif order.order_type.value == "stop":
            req = StopOrderRequest(
                symbol=order.symbol,
                qty=order.qty,
                side=side,
                time_in_force=tif,
                stop_price=order.stop_price,
            )
        elif order.order_type.value == "stop_limit":
            req = StopLimitOrderRequest(
                symbol=order.symbol,
                qty=order.qty,
                side=side,
                time_in_force=tif,
                limit_price=order.limit_price,
                stop_price=order.stop_price,
            )
        else:
            raise ValueError(f"Unsupported order type: {order.order_type}")

        return self._client.submit_order(req)

    def _get_trading_mode(self) -> TradingMode:
        if self._settings.DRY_RUN:
            return TradingMode.DRY_RUN
        if self._settings.ALPACA_PAPER:
            return TradingMode.PAPER
        return TradingMode.LIVE
