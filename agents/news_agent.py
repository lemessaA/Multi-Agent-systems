from typing import List

from agents.base_agent import BaseAgent
from tools.news_tools import NewsTools
from langchain_core.tools import Tool
from schemas.models import AgentType
import asyncio


class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEWS)

    def _initialize_tools(self) -> List[Tool]:
        # Tools are registered for potential future use; the current BaseAgent
        # implementation does not automatically call them.
        return [
            Tool(
                name="GetTopHeadlines",
                func=NewsTools.get_top_headlines,
                description=(
                    "Get top news headlines. Input can be country code (e.g., 'us') "
                    "or 'category,country' (e.g., 'technology,us')."
                ),
            ),
            Tool(
                name="SearchNews",
                func=lambda query: asyncio.run(NewsTools.search_news_async(query)),
                description=(
                    "Search for news articles. Input should be a search query "
                    "(e.g., 'artificial intelligence')."
                ),
            ),
        ]

    def _parse_response(self, raw_response: str) -> str:
        """Optionally customize parsing for news responses."""
        return raw_response

