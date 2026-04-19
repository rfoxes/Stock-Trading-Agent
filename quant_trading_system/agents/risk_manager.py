"""Risk Manager Agent — portfolio-level risk oversight with veto power.

Evaluates individual orders and portfolio-level risk, with the authority
to reject orders that would violate risk constraints.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import structlog

from quant_trading_system.models.trade import OrderRequest

if TYPE_CHECKING:
    from quant_trading_system.brokers.alpaca_client import AlpacaClient
    from quant_trading_system.config import Settings

logger = structlog.get_logger(__name__)


class RiskManagerAgent:
    """Portfolio-level risk oversight with veto power over individual orders.

    Checks:
        1. Correlation with existing positions (reject if >0.7 correlation)
        2. Sector concentration (max 25% in any one sector)
        3. Drawdown circuit breaker (halt new entries if portfolio drawdown exceeds threshold)
        4. Max portfolio delta for options (placeholder for future implementation)
    """

    # Simplified sector mapping for common tickers
    _SECTOR_MAP: dict[str, str] = {
        "AAPL": "technology",
        "MSFT": "technology",
        "GOOGL": "technology",
        "GOOG": "technology",
        "META": "technology",
        "NVDA": "technology",
        "AMD": "technology",
        "INTC": "technology",
        "CRM": "technology",
        "ADBE": "technology",
        "AMZN": "consumer_discretionary",
        "TSLA": "consumer_discretionary",
        "HD": "consumer_discretionary",
        "NKE": "consumer_discretionary",
        "JPM": "financials",
        "BAC": "financials",
        "GS": "financials",
        "MS": "financials",
        "V": "financials",
        "MA": "financials",
        "JNJ": "healthcare",
        "UNH": "healthcare",
        "PFE": "healthcare",
        "ABBV": "healthcare",
        "MRK": "healthcare",
        "XOM": "energy",
        "CVX": "energy",
        "COP": "energy",
        "PG": "consumer_staples",
        "KO": "consumer_staples",
        "PEP": "consumer_staples",
        "WMT": "consumer_staples",
        "SPY": "index",
        "QQQ": "index",
        "IWM": "index",
        "DIA": "index",
    }

    # Simplified correlation groups (symbols that tend to move together)
    _CORRELATION_GROUPS: list[set[str]] = [
        {"AAPL", "MSFT", "GOOGL", "GOOG", "META", "QQQ"},
        {"NVDA", "AMD", "INTC"},
        {"JPM", "BAC", "GS", "MS"},
        {"XOM", "CVX", "COP"},
        {"JNJ", "UNH", "PFE", "ABBV", "MRK"},
        {"AMZN", "TSLA", "HD"},
        {"V", "MA"},
        {"PG", "KO", "PEP", "WMT"},
    ]

    def __init__(self, settings: Settings, alpaca_client: Optional[AlpacaClient] = None) -> None:
        self._settings = settings
        self._client = alpaca_client
        self._log = logger.bind(agent="risk_manager")

    def evaluate_order(self, order: OrderRequest, portfolio: dict) -> dict:
        """Evaluate whether an order should be approved given portfolio risk constraints.

        Args:
            order: The proposed order to evaluate.
            portfolio: Current portfolio state with keys:
                - positions: list of dicts with symbol, market_value, side
                - equity: total portfolio equity
                - peak_equity: highest equity watermark (for drawdown)

        Returns:
            Dict with keys: approved (bool), reason (str), adjustments (dict).
        """
        self._log.info(
            "evaluate_order",
            symbol=order.symbol,
            side=order.side.value,
            qty=order.qty,
            agent=order.agent_name,
        )

        # Check 1: Correlation with existing positions
        correlation_result = self._check_correlation(order, portfolio)
        if not correlation_result["passed"]:
            self._log.warning(
                "order_rejected_correlation",
                symbol=order.symbol,
                reason=correlation_result["reason"],
            )
            return {
                "approved": False,
                "reason": correlation_result["reason"],
                "adjustments": {},
            }

        # Check 2: Sector concentration
        sector_result = self._check_sector_concentration(order, portfolio)
        if not sector_result["passed"]:
            self._log.warning(
                "order_rejected_sector",
                symbol=order.symbol,
                reason=sector_result["reason"],
            )
            return {
                "approved": False,
                "reason": sector_result["reason"],
                "adjustments": sector_result.get("adjustments", {}),
            }

        # Check 3: Drawdown circuit breaker
        drawdown_result = self._check_drawdown(portfolio)
        if not drawdown_result["passed"]:
            self._log.warning(
                "order_rejected_drawdown",
                reason=drawdown_result["reason"],
            )
            return {
                "approved": False,
                "reason": drawdown_result["reason"],
                "adjustments": {},
            }

        # Check 4: Options delta (placeholder)
        delta_result = self._check_portfolio_delta(order, portfolio)
        if not delta_result["passed"]:
            self._log.warning(
                "order_rejected_delta",
                reason=delta_result["reason"],
            )
            return {
                "approved": False,
                "reason": delta_result["reason"],
                "adjustments": {},
            }

        self._log.info("order_approved", symbol=order.symbol)
        return {
            "approved": True,
            "reason": "All risk checks passed",
            "adjustments": {},
        }

    def evaluate_portfolio(self, portfolio: dict) -> dict:
        """Run a portfolio-level risk assessment.

        Args:
            portfolio: Current portfolio state with keys:
                - positions: list of dicts with symbol, market_value, side, unrealized_pl
                - equity: total portfolio equity
                - peak_equity: highest equity watermark

        Returns:
            Dict with risk assessment details.
        """
        self._log.info("evaluate_portfolio")

        positions = portfolio.get("positions", [])
        equity = portfolio.get("equity", 0.0)
        peak_equity = portfolio.get("peak_equity", equity)

        # Calculate drawdown
        drawdown_pct = 0.0
        if peak_equity > 0:
            drawdown_pct = (peak_equity - equity) / peak_equity

        # Calculate sector exposures
        sector_exposures = self._calculate_sector_exposures(positions, equity)

        # Calculate max correlation among held positions
        max_correlation = self._calculate_max_position_correlation(positions)

        # Calculate portfolio beta estimate (simple: based on index exposure)
        portfolio_beta = self._estimate_portfolio_beta(positions, equity)

        # Determine overall risk level
        risk_level = "low"
        warnings = []

        if drawdown_pct > self._settings.MAX_DRAWDOWN_PAUSE_PCT:
            risk_level = "critical"
            warnings.append(
                f"Drawdown {drawdown_pct:.1%} exceeds pause threshold "
                f"{self._settings.MAX_DRAWDOWN_PAUSE_PCT:.1%}"
            )
        elif drawdown_pct > self._settings.MAX_DRAWDOWN_PAUSE_PCT * 0.7:
            risk_level = "high"
            warnings.append(f"Drawdown {drawdown_pct:.1%} approaching pause threshold")

        max_sector_exposure = max(sector_exposures.values()) if sector_exposures else 0.0
        if max_sector_exposure > self._settings.MAX_SECTOR_CONCENTRATION_PCT:
            if risk_level != "critical":
                risk_level = "high"
            warnings.append(
                f"Sector concentration {max_sector_exposure:.1%} exceeds limit "
                f"{self._settings.MAX_SECTOR_CONCENTRATION_PCT:.1%}"
            )

        if max_correlation > 0.7:
            if risk_level == "low":
                risk_level = "medium"
            warnings.append(f"High position correlation detected: {max_correlation:.2f}")

        assessment = {
            "risk_level": risk_level,
            "drawdown_pct": round(drawdown_pct, 4),
            "sector_exposures": sector_exposures,
            "max_position_correlation": round(max_correlation, 4),
            "portfolio_beta": round(portfolio_beta, 4),
            "position_count": len(positions),
            "warnings": warnings,
            "circuit_breaker_active": drawdown_pct > self._settings.MAX_DRAWDOWN_PAUSE_PCT,
        }

        self._log.info(
            "portfolio_assessment_complete",
            risk_level=risk_level,
            drawdown_pct=round(drawdown_pct, 4),
            warnings_count=len(warnings),
        )

        return assessment

    def _check_correlation(self, order: OrderRequest, portfolio: dict) -> dict:
        """Check if the new order would create high correlation with existing positions."""
        positions = portfolio.get("positions", [])
        held_symbols = {p.get("symbol", "") for p in positions}

        if not held_symbols:
            return {"passed": True, "reason": ""}

        # Find which correlation group the order symbol belongs to
        order_groups = [
            group for group in self._CORRELATION_GROUPS
            if order.symbol in group
        ]

        if not order_groups:
            return {"passed": True, "reason": ""}

        # Check if any existing position is in the same correlation group
        for group in order_groups:
            correlated_held = held_symbols & group
            # Exclude the symbol itself (in case of adding to existing position)
            correlated_held.discard(order.symbol)

            if correlated_held:
                # Calculate approximate correlation based on group overlap
                # More symbols from same group = higher implied correlation
                correlation_estimate = min(0.5 + 0.15 * len(correlated_held), 0.95)

                if correlation_estimate > 0.7:
                    return {
                        "passed": False,
                        "reason": (
                            f"Order for {order.symbol} would create >{correlation_estimate:.1%} "
                            f"estimated correlation with existing positions: "
                            f"{', '.join(sorted(correlated_held))}"
                        ),
                    }

        return {"passed": True, "reason": ""}

    def _check_sector_concentration(self, order: OrderRequest, portfolio: dict) -> dict:
        """Check if the new order would exceed sector concentration limits."""
        positions = portfolio.get("positions", [])
        equity = portfolio.get("equity", 0.0)

        if equity <= 0:
            return {"passed": True, "reason": ""}

        # Calculate current sector exposures
        sector_exposures = self._calculate_sector_exposures(positions, equity)

        # Determine the sector of the new order
        order_sector = self._SECTOR_MAP.get(order.symbol, "other")

        # Estimate the new order's market value
        # Use a rough estimate if we don't have exact price
        estimated_order_value = order.qty * (order.limit_price or 0.0)
        if estimated_order_value <= 0:
            # Cannot estimate value without price, allow the order through
            return {"passed": True, "reason": ""}

        # Calculate what sector exposure would be after the order
        current_sector_pct = sector_exposures.get(order_sector, 0.0)
        additional_pct = estimated_order_value / equity
        new_sector_pct = current_sector_pct + additional_pct

        max_sector_pct = self._settings.MAX_SECTOR_CONCENTRATION_PCT

        if new_sector_pct > max_sector_pct:
            # Calculate how much we could buy while staying within limits
            remaining_capacity_pct = max(0, max_sector_pct - current_sector_pct)
            max_allowed_value = remaining_capacity_pct * equity
            max_allowed_qty = int(max_allowed_value / (order.limit_price or 1.0))

            return {
                "passed": False,
                "reason": (
                    f"Order for {order.symbol} would push {order_sector} sector "
                    f"concentration to {new_sector_pct:.1%}, exceeding limit of "
                    f"{max_sector_pct:.1%}"
                ),
                "adjustments": {
                    "max_allowed_qty": max_allowed_qty,
                    "current_sector_pct": round(current_sector_pct, 4),
                },
            }

        return {"passed": True, "reason": ""}

    def _check_drawdown(self, portfolio: dict) -> dict:
        """Check if portfolio drawdown has exceeded the circuit breaker threshold."""
        equity = portfolio.get("equity", 0.0)
        peak_equity = portfolio.get("peak_equity", equity)

        if peak_equity <= 0:
            return {"passed": True, "reason": ""}

        drawdown_pct = (peak_equity - equity) / peak_equity

        if drawdown_pct > self._settings.MAX_DRAWDOWN_PAUSE_PCT:
            return {
                "passed": False,
                "reason": (
                    f"Portfolio drawdown of {drawdown_pct:.1%} exceeds circuit breaker "
                    f"threshold of {self._settings.MAX_DRAWDOWN_PAUSE_PCT:.1%}. "
                    f"New entries are halted until drawdown recovers."
                ),
            }

        return {"passed": True, "reason": ""}

    def _check_portfolio_delta(self, order: OrderRequest, portfolio: dict) -> dict:
        """Check portfolio delta for options positions.

        Placeholder: currently always passes. Will be implemented when options
        trading is enabled.
        """
        # Placeholder for options delta checking
        return {"passed": True, "reason": ""}

    def _calculate_sector_exposures(
        self, positions: list[dict], equity: float
    ) -> dict[str, float]:
        """Calculate the percentage of equity in each sector."""
        if equity <= 0:
            return {}

        sector_values: dict[str, float] = {}
        for position in positions:
            symbol = position.get("symbol", "")
            market_value = abs(float(position.get("market_value", 0.0)))
            sector = self._SECTOR_MAP.get(symbol, "other")
            sector_values[sector] = sector_values.get(sector, 0.0) + market_value

        return {
            sector: round(value / equity, 4)
            for sector, value in sector_values.items()
        }

    def _calculate_max_position_correlation(self, positions: list[dict]) -> float:
        """Estimate the maximum pairwise correlation among held positions."""
        held_symbols = {p.get("symbol", "") for p in positions}

        if len(held_symbols) < 2:
            return 0.0

        max_corr = 0.0
        for group in self._CORRELATION_GROUPS:
            overlap = held_symbols & group
            if len(overlap) >= 2:
                # Estimate correlation based on how many symbols share a group
                corr_estimate = min(0.5 + 0.1 * len(overlap), 0.95)
                max_corr = max(max_corr, corr_estimate)

        return max_corr

    def _estimate_portfolio_beta(self, positions: list[dict], equity: float) -> float:
        """Estimate portfolio beta based on position composition.

        Simple heuristic: index positions have beta ~1.0, tech ~1.3,
        healthcare ~0.8, etc.
        """
        if equity <= 0 or not positions:
            return 1.0

        sector_betas = {
            "technology": 1.3,
            "consumer_discretionary": 1.2,
            "financials": 1.1,
            "healthcare": 0.8,
            "energy": 1.0,
            "consumer_staples": 0.6,
            "index": 1.0,
            "other": 1.0,
        }

        weighted_beta = 0.0
        total_value = 0.0

        for position in positions:
            symbol = position.get("symbol", "")
            market_value = abs(float(position.get("market_value", 0.0)))
            sector = self._SECTOR_MAP.get(symbol, "other")
            beta = sector_betas.get(sector, 1.0)

            weighted_beta += beta * market_value
            total_value += market_value

        if total_value <= 0:
            return 1.0

        return weighted_beta / total_value
