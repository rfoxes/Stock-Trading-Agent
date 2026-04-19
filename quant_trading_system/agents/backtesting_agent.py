"""Backtesting Agent — runs backtests and interprets results via Claude."""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog
from langchain_core.messages import HumanMessage, SystemMessage

from quant_trading_system.backtesting.equity_backtester import EquityBacktester
from quant_trading_system.backtesting.performance_report import PerformanceReporter
from quant_trading_system.models.strategy import (
    Conclusion,
    ConclusionType,
    Recommendation,
)

if TYPE_CHECKING:
    from quant_trading_system.config import Settings
    from quant_trading_system.data.market_data_service import MarketDataService
    from quant_trading_system.knowledge_base.chroma_client import KnowledgeBaseClient

logger = structlog.get_logger(__name__)

INTERPRETATION_PROMPT = """You are a quantitative analyst reviewing backtest results.

Strategy: {strategy_name}
Symbol: {symbol}
Period: {start_date} to {end_date}

Results:
{metrics}

Analyze these results and provide:
1. Is this strategy viable? Why or why not?
2. Key strengths and weaknesses
3. Recommendation: promote (add to live trading), watch (needs more testing), modify (adjust parameters), or retire (not viable)
4. If modify, what specific changes would you suggest?

Respond in JSON format:
{{"recommendation": "promote|watch|modify|retire", "reasoning": "...", "modification_notes": "..."}}
"""


class BacktestingAgent:
    """Agent that runs backtests and writes conclusions to the knowledge base."""

    def __init__(
        self,
        settings: Settings,
        market_data: MarketDataService,
        knowledge_base: KnowledgeBaseClient,
    ) -> None:
        self._settings = settings
        self._market_data = market_data
        self._kb = knowledge_base
        self._backtester = EquityBacktester(market_data)
        self._reporter = PerformanceReporter()
        from quant_trading_system.llm_factory import create_llm

        self._llm = create_llm(settings, model_name=settings.ANALYSIS_MODEL)

    def backtest_strategy(
        self,
        strategy_id: str,
        symbol: str,
        start_date: str,
        end_date: str,
        initial_cash: float = 100_000.0,
    ) -> dict:
        """Run a backtest for a strategy and write conclusions.

        Uses SMA crossover as a default signal generator for now.
        Full strategy-specific signal generation will be added later.
        """
        log = logger.bind(strategy=strategy_id, symbol=symbol)
        log.info("backtesting_start")

        # Get price data
        close = self._market_data.get_bars(symbol, "1Day", start_date, end_date)
        if close.empty:
            log.warning("no_data_for_backtest")
            return {"error": "No data available"}

        close_series = close["Close"]

        # Run backtest with default SMA crossover signals
        result = self._backtester.backtest_sma_crossover(
            close=close_series,
            initial_cash=initial_cash,
        )

        # Generate performance report
        report = self._reporter.generate_report(result, strategy_id)

        # Check promotion criteria
        promotion = self._reporter.meets_promotion_criteria(result)

        # Get LLM interpretation
        try:
            interpretation = self._interpret_results(
                strategy_id, symbol, start_date, end_date, report["metrics"]
            )
        except Exception as e:
            log.warning("interpretation_failed", error=str(e))
            interpretation = {
                "recommendation": "watch",
                "reasoning": f"LLM interpretation failed: {e}",
                "modification_notes": "",
            }

        # Map recommendation string to enum
        rec_map = {
            "promote": Recommendation.PROMOTE,
            "watch": Recommendation.WATCH,
            "modify": Recommendation.MODIFY,
            "retire": Recommendation.RETIRE,
            "demote": Recommendation.DEMOTE,
        }
        rec_str = interpretation.get("recommendation", "watch").lower()
        recommendation = rec_map.get(rec_str, Recommendation.WATCH)

        # Write conclusion to knowledge base
        conclusion = Conclusion(
            conclusion_type=ConclusionType.BACKTEST_RESULT,
            strategy_id=strategy_id,
            agent_id="backtesting_agent",
            ticker=symbol,
            summary=(
                f"Backtest of {strategy_id} on {symbol} ({start_date} to {end_date}). "
                f"Sharpe: {report['metrics'].get('sharpe', 0):.2f}, "
                f"Max DD: {report['metrics'].get('max_drawdown', 0):.2%}, "
                f"Win Rate: {report['metrics'].get('win_rate', 0):.1%}."
            ),
            metrics=report["metrics"],
            recommendation=recommendation,
            modification_notes=interpretation.get("modification_notes", ""),
        )
        self._kb.add_conclusion(conclusion)

        log.info(
            "backtesting_complete",
            recommendation=recommendation.value,
            sharpe=report["metrics"].get("sharpe", 0),
            promoted=promotion["promoted"],
        )

        return {
            "backtest_result": result,
            "report": report,
            "promotion": promotion,
            "interpretation": interpretation,
            "conclusion": conclusion.model_dump(),
        }

    def _interpret_results(
        self,
        strategy_name: str,
        symbol: str,
        start_date: str,
        end_date: str,
        metrics: dict,
    ) -> dict:
        """Use Claude to interpret backtest results."""
        prompt = INTERPRETATION_PROMPT.format(
            strategy_name=strategy_name,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            metrics=str(metrics),
        )

        response = self._llm.invoke([
            SystemMessage(content="You are a quantitative analyst. Respond only in valid JSON."),
            HumanMessage(content=prompt),
        ])

        import json

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "recommendation": "watch",
                "reasoning": response.content,
                "modification_notes": "",
            }
