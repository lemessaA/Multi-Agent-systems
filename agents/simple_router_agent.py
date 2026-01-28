from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from schemas.models import AgentType, AgentRequest, AgentResponse
from config.settings import settings
import uuid
from datetime import datetime

class RouterState:
    def __init__(self):
        self.query: str = ""
        self.agent_type: AgentType = None
        self.responses: List[AgentResponse] = []
        self.conversation_id: str = ""
        self.start_time: datetime = None

class SimpleRouterAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=settings.GROQ_API_KEY
        )
        
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
        prompt = PromptTemplate.from_template("""
        Analyze the user query and determine which agent(s) should handle it.
        
        Available agents:
        1. weather_agent - for weather-related queries (temperature, forecast, climate)
        2. news_agent - for news, headlines, current events
        3. finance_agent - for stocks, crypto, exchange rates, financial data
        
        Query: {query}
        
        Respond with ONLY one of: 'weather', 'news', 'finance', or 'multiple' if it requires multiple agents.
        """)
        
        chain = prompt | self.llm
        result = await chain.ainvoke({"query": state.query})
        
        return {"agent_type": result.content.strip().lower()}

    async def _execute_weather_agent(self, state: RouterState) -> Dict[str, Any]:
        """Execute weather agent - simplified version"""
        # Simple weather response for now
        response = AgentResponse(
            agent_type=AgentType.WEATHER,
            response=f"Weather information for: {state.query} (This is a placeholder response)",
            source="weather_agent",
            confidence=0.8
        )
        return {"responses": [response]}

    async def _execute_news_agent(self, state: RouterState) -> Dict[str, Any]:
        """Execute news agent - simplified version"""
        # Simple news response for now
        response = AgentResponse(
            agent_type=AgentType.NEWS,
            response=f"News information for: {state.query} (This is a placeholder response)",
            source="news_agent",
            confidence=0.8
        )
        return {"responses": [response]}

    async def _execute_finance_agent(self, state: RouterState) -> Dict[str, Any]:
        """Execute finance agent - simplified version"""
        # Simple finance response for now
        response = AgentResponse(
            agent_type=AgentType.FINANCE,
            response=f"Finance information for: {state.query} (This is a placeholder response)",
            source="finance_agent",
            confidence=0.8
        )
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

# Create the workflow instance (only when imported with API key)
def get_workflow():
    """Get the workflow instance"""
    return SimpleRouterAgent().workflow

# For LangGraph Studio, create workflow when module is loaded
try:
    workflow = SimpleRouterAgent().workflow
except Exception:
    # Fallback for testing without API key
    workflow = None
