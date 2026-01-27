from agents.base_agent import BaseAgent
from tools.finance_tools import FinanceTools
from langchain.agents import Tool
from schemas.models import AgentType
from typing import List

class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.FINANCE)

    def _initialize_tools(self) -> List[Tool]:
        return [
            Tool(
                name="GetStockPrice",
                func=FinanceTools.get_stock_price,
                description="Get current stock price. Input should be stock symbol (e.g., 'AAPL', 'GOOGL', 'TSLA')."
            ),
            Tool(
                name="GetCryptoPrice",
                func=FinanceTools.get_crypto_price,
                description="Get cryptocurrency price. Input should be crypto name (e.g., 'bitcoin', 'ethereum')."
            ),
            Tool(
                name="GetExchangeRate",
                func=FinanceTools.get_exchange_rate,
                description="Get exchange rate between currencies. Input should be 'from_currency,to_currency' (e.g., 'EUR,USD')."
            )
        ]