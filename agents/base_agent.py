from abc import ABC, abstractmethod
from typing import Dict, Any, List

from langchain_core.prompts import PromptTemplate

from llm_factory import get_chat_llm
from schemas.models import AgentType, AgentResponse


class BaseAgent(ABC):
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.llm = get_chat_llm(temperature=0.3)
        # Hook for subclasses to register tools if needed.
        self.tools = self._initialize_tools()

    @abstractmethod
    def _initialize_tools(self) -> List[Any]:
        """Initialize agent-specific tools (optional for this simplified agent)."""
        pass

    async def execute(self, query: str, **kwargs) -> AgentResponse:
        """Execute agent with given query using a simple LLM prompt."""
        try:
            prompt = PromptTemplate.from_template(
                "You are a {agent_type} agent. Answer the user's question.\n\n"
                "Question: {input}"
            )
            chain = prompt | self.llm
            result = await chain.ainvoke(
                {"agent_type": self.agent_type.value, "input": query, **kwargs}
            )

            content = getattr(result, "content", str(result))
            response = self._parse_response(content)

            return AgentResponse(
                agent_type=self.agent_type,
                response=response,
                data=self._extract_data(result),
                source=f"{self.agent_type.value}_agent",
                confidence=0.9,
            )
        except Exception as e:
            return AgentResponse(
                agent_type=self.agent_type,
                response=f"Error: {str(e)}",
                source=f"{self.agent_type.value}_agent",
                confidence=0.0,
            )

    def _parse_response(self, raw_response: str) -> str:
        """Parse raw agent response"""
        return raw_response

    def _extract_data(self, result) -> Dict[str, Any]:
        """Extract structured data from agent result"""
        # Handle AIMessage objects
        if hasattr(result, 'content'):
            return {
                "raw_output": result.content,
                "intermediate_steps": []
            }
        # Handle dict objects
        elif isinstance(result, dict):
            return {
                "raw_output": result.get('output', ''),
                "intermediate_steps": str(result.get('intermediate_steps', []))
            }
        # Handle other objects
        else:
            return {
                "raw_output": str(result),
                "intermediate_steps": []
            }