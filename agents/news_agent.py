from agents.base_agent import BaseAgent
from tools.news_tools import NewsTools
from langchain.agents import Tool
from schemas.models import AgentType
from typing import List
import asyncio

class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.NEWS)

    def _initialize_tools(self) -> List[Tool]:
        return [
            Tool(
                name="GetTopHeadlines",
                func=NewsTools.get_top_headlines,
                description="Get top news headlines. Input can be country code (e.g., 'us') or 'category,country' (e.g., 'technology,us')."
            ),
            Tool(
                name="SearchNews",
                func=lambda query: asyncio.run(NewsTools.search_news_async(query)),
                description="Search for news articles. Input should be a search query (e.g., 'artificial intelligence')."
            )
        ]