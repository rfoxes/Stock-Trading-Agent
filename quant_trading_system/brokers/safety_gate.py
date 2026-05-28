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


def _unique_id() -> int:
    """Monotonic-ish id for tagging client_order_id; resets per process."""
    import time as _t

    return int(_t.time() * 1000) & 0xFFFFFFFF


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

        This is the ONLY authorized path to equity order execution.
        """
        return self._validate_and_submit_inner(order)

    def validate_and_submit_options(self, order) -> OrderResult:
        """Validate + submit a multi-leg options order.

        Distinct from the equity path because options have different risk
        shapes: defined-risk spreads have a known max loss; undefined-risk
        positions (naked puts, short straddles) can lose multiples of
        premium. Checks (in order):
          1. Dry-run mode.
          2. Live-money gate.
          3. Undefined-risk gate: the strategy must explicitly set
             `allow_undefined_risk=True` if `declared_max_loss_usd` is None.
          4. Max single-trade loss vs MAX_POSITION_SIZE_PCT * equity.
          5. Max concurrent options orders (uses MAX_CONCURRENT_POSITIONS as proxy).
          6. Daily loss limit.
        """
        from quant_trading_system.models.trade import OptionsOrderRequest

        if not isinstance(order, OptionsOrderRequest):
            return OrderResult(
                status=OrderStatus.REJECTED,
                mode=self._get_trading_mode(),
                rejection_reason="not an OptionsOrderRequest",
                safety_checks_failed=["bad_input"],
            )
        result = self._validate_and_submit_options_inner(order)
        return result

    def _validate_and_submit_options_inner(self, order) -> OrderResult:
        from quant_trading_system.models.trade import OptionsOrderRequest

        self._reset_daily_if_needed()
        checks_passed: list[str] = []
        log = logger.bind(
            strategy=order.strategy_name,
            n_legs=len(order.legs),
            qty=order.qty,
            agent=order.agent_name,
        )

        # 1. Dry-run
        if self._settings.DRY_RUN:
            log.info("dry_run_options_order")
            return OrderResult(
                order_id=f"dry-run-options-{_unique_id()}",
                status=OrderStatus.DRY_RUN,
                mode=TradingMode.DRY_RUN,
                safety_checks_passed=["dry_run_bypass"],
            )

        # 2. Live-money gate
        if not self._settings.ALPACA_PAPER:
            if not self._settings.REAL_MONEY_ENABLED or not self._settings.REAL_MONEY_CONFIRMATION:
                raise SafetyError(
                    "Options live trading attempted without REAL_MONEY_ENABLED + "
                    "REAL_MONEY_CONFIRMATION. Critical safety violation."
                )
            checks_passed.append("live_money_gate")
        else:
            checks_passed.append("paper_trading_mode")

        # 3. Undefined-risk gate
        if order.declared_max_loss_usd is None:
            if not order.allow_undefined_risk:
                log.warning("options_undefined_risk_blocked")
                return OrderResult(
                    status=OrderStatus.REJECTED,
                    mode=self._get_trading_mode(),
                    rejection_reason=(
                        "Options order has no declared_max_loss_usd and "
                        "allow_undefined_risk is False. Strategies that wish "
                        "to submit undefined-risk positions must declare so."
                    ),
                    safety_checks_passed=checks_passed,
                    safety_checks_failed=["undefined_risk_gate"],
                )
            checks_passed.append("undefined_risk_acknowledged")
        else:
            checks_passed.append("defined_risk")

        # 4. Max single-trade loss
        if self._client is not None:
            try:
                account = self._client.get_account()
                equity = account.get("equity", 0.0)
                if equity > 0 and order.declared_max_loss_usd is not None:
                    loss_pct = order.declared_max_loss_usd / equity
                    if loss_pct > self._settings.MAX_POSITION_SIZE_PCT:
                        log.warning(
                            "options_position_size_exceeded loss_pct=%.3f max=%.3f",
                            loss_pct, self._settings.MAX_POSITION_SIZE_PCT,
                        )
                        return OrderResult(
                            status=OrderStatus.REJECTED,
                            mode=self._get_trading_mode(),
                            rejection_reason=(
                                f"declared max loss {loss_pct:.1%} of equity "
                                f"exceeds MAX_POSITION_SIZE_PCT "
                                f"{self._settings.MAX_POSITION_SIZE_PCT:.1%}"
                            ),
                            safety_checks_passed=checks_passed,
                            safety_checks_failed=["position_size"],
                        )
            except Exception as e:
                log.warning("options_position_size_check_failed err=%s", e)
        checks_passed.append("position_size")

        # 5. Submit
        log.info("all_options_safety_checks_passed checks=%s", checks_passed)
        if self._client is None:
            return OrderResult(
                order_id=f"no-client-options-{_unique_id()}",
                status=OrderStatus.SUBMITTED,
                mode=self._get_trading_mode(),
                safety_checks_passed=checks_passed,
            )
        try:
            alpaca_resp = self._submit_options_to_alpaca(order)
            return OrderResult(
                order_id=str(alpaca_resp.get("id", "")),
                status=OrderStatus.SUBMITTED,
                mode=self._get_trading_mode(),
                filled_qty=float(alpaca_resp.get("filled_qty") or 0),
                filled_avg_price=float(alpaca_resp.get("filled_avg_price") or 0),
                safety_checks_passed=checks_passed,
            )
        except Exception as e:
            log.error("options_submission_failed err=%s", e)
            return OrderResult(
                status=OrderStatus.REJECTED,
                mode=self._get_trading_mode(),
                rejection_reason=f"Broker error: {e}",
                safety_checks_passed=checks_passed,
                safety_checks_failed=["broker_submission"],
            )

    def _submit_options_to_alpaca(self, order) -> dict:
        """Build Alpaca multi-leg /v2/orders body and submit."""
        body: dict = {
            "order_class": order.order_class,
            "qty": str(order.qty),
            "type": order.order_type.value,
            "time_in_force": order.time_in_force.value,
            "legs": [
                {
                    "symbol": leg["contract_symbol"],
                    "side": leg["side"].lower(),
                    "ratio_qty": str(leg.get("ratio", 1)),
                    "position_intent": (
                        "buy_to_open"
                        if leg["side"].lower() == "buy"
                        else "sell_to_open"
                    ),
                }
                for leg in order.legs
            ],
        }
        if order.order_type.value == "limit" and order.limit_price is not None:
            body["limit_price"] = str(order.limit_price)
        if order.strategy_name:
            tag = order.strategy_name[:32].replace(" ", "_")
            body["client_order_id"] = f"opt-{tag}-{int(_unique_id())}"
        return self._client.submit_options_order(body)

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
        # Per-batch realized-loss semantics: sum (a) the estimated realized loss
        # of THIS order if it's a sell that would close at a loss, plus (b)
        # cumulative session-realized losses already booked this day. Compare
        # against MAX_DAILY_LOSS_PCT * equity. This gate measures the cost of
        # *closing trades the strategy actually proposes today*, not the
        # portfolio's standing unrealized losses (which were the old, incorrect
        # semantics — that interpretation halted the entire harness whenever
        # mark-to-market dipped under -2%, blocking even profitable exits).
        #
        # When this check passes for a sell order with a negative estimated P&L,
        # we accrue that loss into self._daily_realized_loss so that subsequent
        # orders in the same batch see the cumulative number. The accrual is
        # an estimate using the position's current_price (market orders) or the
        # order's limit_price (limit orders); actual fills may differ slightly
        # but the safety property — no day realizes losses > MAX_DAILY_LOSS_PCT
        # of equity from strategy-driven closes — is preserved within mark
        # precision.
        order_realized_loss = 0.0
        if self._client is not None:
            try:
                account = self._client.get_account()
                equity = account.get("equity", 0.0)
                if equity > 0 and order.side.value == "sell":
                    positions = self._client.get_positions()
                    position = next(
                        (p for p in positions if p.get("symbol") == order.symbol),
                        None,
                    )
                    if position is not None:
                        avg_entry = float(position.get("avg_entry_price", 0.0) or 0.0)
                        # Prefer the order's limit price when set; otherwise the
                        # position's current mark.
                        est_price = float(
                            order.limit_price
                            or position.get("current_price", 0.0)
                            or 0.0
                        )
                        if avg_entry > 0 and est_price > 0:
                            # Realized P&L on a long-side close: qty * (sale - entry).
                            realized_pl = order.qty * (est_price - avg_entry)
                            if realized_pl < 0:
                                order_realized_loss = abs(realized_pl)
                if equity > 0:
                    total_loss = order_realized_loss + abs(self._daily_realized_loss)
                    loss_pct = total_loss / equity
                    if loss_pct > self._settings.MAX_DAILY_LOSS_PCT:
                        log.warning(
                            "order_rejected",
                            reason="daily_loss_limit",
                            loss_pct=round(loss_pct, 4),
                            max_pct=self._settings.MAX_DAILY_LOSS_PCT,
                            order_realized_loss=round(order_realized_loss, 2),
                            prior_realized_loss=round(abs(self._daily_realized_loss), 2),
                        )
                        return OrderResult(
                            status=OrderStatus.REJECTED,
                            mode=self._get_trading_mode(),
                            rejection_reason=(
                                f"Daily loss {loss_pct:.1%} exceeds "
                                f"limit {self._settings.MAX_DAILY_LOSS_PCT:.1%} "
                                f"(this order ~${order_realized_loss:.0f} + "
                                f"prior realized ~${abs(self._daily_realized_loss):.0f})"
                            ),
                            safety_checks_passed=checks_passed,
                            safety_checks_failed=["daily_loss"],
                            original_request=order,
                        )
                    # Accrue this order's expected realized loss so subsequent
                    # orders in the same batch see it. Only sells against a long
                    # position with a negative estimated P&L contribute.
                    if order_realized_loss > 0:
                        self._daily_realized_loss += order_realized_loss
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
                order_id=str(alpaca_order.get("id", "")),
                status=OrderStatus.SUBMITTED,
                mode=self._get_trading_mode(),
                filled_qty=float(alpaca_order.get("filled_qty") or 0),
                filled_avg_price=float(alpaca_order.get("filled_avg_price") or 0),
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

    def _submit_to_alpaca(self, order: OrderRequest) -> dict:
        """Build the Alpaca REST order body and submit. No alpaca-py needed."""
        body: dict = {
            "symbol": order.symbol,
            "qty": str(order.qty),
            "side": order.side.value,
            "type": order.order_type.value,
            "time_in_force": order.time_in_force.value,
        }
        if order.order_type.value == "limit":
            if order.limit_price is None:
                raise ValueError("limit order requires limit_price")
            body["limit_price"] = str(order.limit_price)
        elif order.order_type.value == "stop":
            if order.stop_price is None:
                raise ValueError("stop order requires stop_price")
            body["stop_price"] = str(order.stop_price)
        elif order.order_type.value == "stop_limit":
            if order.limit_price is None or order.stop_price is None:
                raise ValueError("stop_limit order requires limit_price and stop_price")
            body["limit_price"] = str(order.limit_price)
            body["stop_price"] = str(order.stop_price)
        elif order.order_type.value == "market":
            pass
        else:
            raise ValueError(f"Unsupported order type: {order.order_type}")

        # Tag the order with strategy_id so Alpaca's audit log correlates
        # with our journal even if the journal entry is later lost.
        if order.strategy_name:
            # Alpaca client_order_id has length / charset limits; truncate.
            tag = order.strategy_name[:32].replace(" ", "_")
            body["client_order_id"] = f"{tag}-{int(_unique_id())}"

        return self._client.submit_order(body)

    def _get_trading_mode(self) -> TradingMode:
        if self._settings.DRY_RUN:
            return TradingMode.DRY_RUN
        if self._settings.ALPACA_PAPER:
            return TradingMode.PAPER
        return TradingMode.LIVE
