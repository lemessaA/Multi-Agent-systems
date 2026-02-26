from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from schemas.models import AgentType, AgentRequest, AgentResponse
from agents.weather_agent import WeatherAgent
from agents.news_agent import NewsAgent
from agents.finance_agent import FinanceAgent
from llm_factory import get_chat_llm
import uuid
from datetime import datetime

class RouterState:
    def __init__(self):
        self.query: str = ""
        self.agent_type: AgentType = None
        self.responses: List[AgentResponse] = []
        self.conversation_id: str = ""
        self.start_time: datetime = None

class RouterAgent:
    def __init__(self):
        self.llm = get_chat_llm(temperature=0.1)
        
        # Initialize specialized agents
        self.agents = {
            AgentType.WEATHER: WeatherAgent(),
            AgentType.NEWS: NewsAgent(),
            AgentType.FINANCE: FinanceAgent()
        }
        
        # Create the router graph
        self.workflow = self._create_workflow()

    def _create_workflow(self):
        """Create LangGraph workflow for routing"""
        workflow = StateGraph(RouterState)

        # Add nodes
        workflow.add_node("router", self._route_query)
        workflow.add_node("weather_agent", self._execute_weather_agent)
        workflow.add_node("news_agent", self._execute_news_agent)
        workflow.add_node("finance_agent", self._execute_finance_agent)
        workflow.add_node("aggregator", self._aggregate_responses)

        # Add edges
        workflow.set_entry_point("router")
        
        workflow.add_conditional_edges(
            "router",
            self._decide_next_node,
            {
                "weather": "weather_agent",
                "news": "news_agent",
                "finance": "finance_agent",
                "multiple": "aggregator"
            }
        )
        
        workflow.add_edge("weather_agent", "aggregator")
        workflow.add_edge("news_agent", "aggregator")
        workflow.add_edge("finance_agent", "aggregator")
        workflow.add_edge("aggregator", END)

        return workflow.compile()

    async def _route_query(self, state: RouterState) -> Dict[str, Any]:
        """Route query to appropriate agent"""
        router_prompt = PromptTemplate.from_template(
            """You are an intelligent router that decides which specialized AI agents
should handle a user request.

Available agents:
- weather_agent: weather, temperature, forecasts, climate, conditions by location
- news_agent: news, headlines, breaking stories, topic-specific news, explanations
- finance_agent: stocks, crypto, forex, market data, financial insights

USER QUERY:
{query}

1. Decide which agent(s) are truly required.
2. Prefer a single agent when possible; only use multiple if the question clearly spans domains.
3. Think step-by-step but respond in a compact machine-readable form.

Respond with a single JSON object, and nothing else, in this format:

{{
  "route": "weather" | "news" | "finance" | "multiple",
  "reason": "short explanation of why this route was chosen"
}}

JSON:
"""
        )

        chain = router_prompt | self.llm
        result = await chain.ainvoke({"query": state.query})

        content = getattr(result, "content", "").strip()
        # Fallback: if parsing fails, treat content as a plain label
        try:
            import json

            data = json.loads(content)
            route = str(data.get("route", "")).strip().lower()
        except Exception:
            route = content.lower()

        return {"agent_type": route}

    async def _execute_weather_agent(self, state: RouterState) -> Dict[str, Any]:
        """Execute weather agent"""
        agent = self.agents[AgentType.WEATHER]
        response = await agent.execute(state.query)
        return {"responses": [response]}

    async def _execute_news_agent(self, state: RouterState) -> Dict[str, Any]:
        """Execute news agent"""
        agent = self.agents[AgentType.NEWS]
        response = await agent.execute(state.query)
        return {"responses": [response]}

    async def _execute_finance_agent(self, state: RouterState) -> Dict[str, Any]:
        """Execute finance agent"""
        agent = self.agents[AgentType.FINANCE]
        response = await agent.execute(state.query)
        return {"responses": [response]}

    def _decide_next_node(self, state: RouterState) -> str:
        """Decide next node based on router output"""
        return state.agent_type

    async def _aggregate_responses(self, state: RouterState) -> Dict[str, Any]:
        """Aggregate responses from multiple agents"""
        # If we have responses from execution nodes, add them
        if hasattr(state, 'responses') and state.responses:
            all_responses = state.responses
        else:
            all_responses = []
        
        return {
            "responses": all_responses,
            "execution_complete": True
        }

    async def process(self, request: AgentRequest) -> Dict[str, Any]:
        """Process query through router"""
        # Initialize state
        state = RouterState()
        state.query = request.query
        state.conversation_id = str(uuid.uuid4())
        state.start_time = datetime.now()
        
        # If agent type is specified, use it directly
        if request.agent_type:
            if request.agent_type == AgentType.WEATHER:
                result = await self._execute_weather_agent(state)
            elif request.agent_type == AgentType.NEWS:
                result = await self._execute_news_agent(state)
            elif request.agent_type == AgentType.FINANCE:
                result = await self._execute_finance_agent(state)
            else:
                # Use router for auto-detection
                result = await self.workflow.ainvoke(state)
        else:
            # Use router for auto-detection
            result = await self.workflow.ainvoke(state)
        
        execution_time = (datetime.now() - state.start_time).total_seconds()
        
        return {
            "conversation_id": state.conversation_id,
            "responses": result.get("responses", []),
            "execution_time": execution_time,
            "agent_type": request.agent_type or "auto"
        }