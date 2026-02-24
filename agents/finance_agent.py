from typing import List, Dict, Any

from agents.base_agent import BaseAgent
from tools.finance_tools import FinanceTools
from langchain_core.tools import Tool
from schemas.models import AgentType, AgentResponse


class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.FINANCE)

    def _initialize_tools(self) -> List[Tool]:
        """Initialize enhanced finance tools with Google Finance integration"""
        return [
            Tool(
                name="GetStockPrice",
                func=FinanceTools.get_stock_price,
                description=(
                    "Get current stock price with real-time data. Input should be stock symbol "
                    "(e.g., 'AAPL', 'GOOGL', 'TSLA'). Uses Google Finance primary."
                ),
            ),
            Tool(
                name="GetRealTimeQuote",
                func=FinanceTools.get_real_time_quote,
                description=(
                    "Get comprehensive real-time quote with multiple sources. "
                    "Input should be stock symbol (e.g., 'AAPL', 'TSLA')."
                ),
            ),
            Tool(
                name="GetCryptoPrice",
                func=FinanceTools.get_crypto_price,
                description=(
                    "Get cryptocurrency price with real-time data. Input should be crypto name "
                    "(e.g., 'bitcoin', 'ethereum'). Uses Google Finance primary."
                ),
            ),
            Tool(
                name="GetPortfolioValue",
                func=FinanceTools.get_portfolio_value,
                description=(
                    "Calculate portfolio value for multiple symbols. "
                    "Input should be comma-separated symbols (e.g., 'AAPL,GOOGL,MSFT')."
                ),
            ),
            Tool(
                name="GetMarketSummary",
                func=FinanceTools.get_market_summary,
                description=(
                    "Get overall market summary with major indices and movers."
                ),
            ),
            Tool(
                name="GetAdvancedPortfolioAnalysis",
                func=FinanceTools.get_advanced_portfolio_analysis,
                description=(
                    "Get advanced portfolio analysis with volatility, trends, and performance metrics. "
                    "Input should be comma-separated symbols (e.g., 'AAPL,GOOGL,MSFT')."
                ),
            ),
            Tool(
                name="GetMarketSentiment",
                func=FinanceTools.get_market_sentiment,
                description=(
                    "Get market sentiment analysis for a stock based on price movements. "
                    "Input should be stock symbol (e.g., 'AAPL', 'TSLA')."
                ),
            ),
            Tool(
                name="GetFinancialNews",
                func=FinanceTools.get_financial_news,
                description=(
                    "Get financial news with market impact analysis. "
                    "Optional symbol for company-specific news, or category for general news."
                ),
            ),
            Tool(
                name="GetTechnicalIndicators",
                func=FinanceTools.get_technical_indicators,
                description=(
                    "Get comprehensive technical analysis indicators (RSI, Bollinger Bands, Moving Averages). "
                    "Input should be stock symbol (e.g., 'AAPL', 'TSLA')."
                ),
            ),
        ]

    def _parse_response(self, raw_response: str) -> str:
        """Optionally customize parsing for finance responses."""
        return raw_response

    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """Execute finance query using enhanced tools"""
        try:
            # Use the base agent's execute method which will call tools
            result = await super().execute(query, **kwargs)
            
            # Extract meaningful response from the base agent result
            if isinstance(result, AgentResponse):
                return {
                    "responses": [result],
                    "data_source": "enhanced_finance_tools"
                }
            else:
                return {
                    "responses": [AgentResponse(
                        agent_type=self.agent_type,
                        response=str(result),
                        source="enhanced_finance_agent",
                        confidence=0.9
                    )],
                    "data_source": "enhanced_finance_tools"
                }
                
        except Exception as e:
            return {
                "responses": [AgentResponse(
                    agent_type=self.agent_type,
                    response=f"Finance processing error: {str(e)}",
                    source="enhanced_finance_agent",
                    confidence=0.0
                )],
                "data_source": "enhanced_finance_tools"
            }
