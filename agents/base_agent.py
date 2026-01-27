from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain.agents import Tool, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from config.settings import settings
from schemas.models import AgentType, AgentResponse

class BaseAgent(ABC):
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            api_key=settings.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._initialize_tools()
        self.agent = self._create_agent()
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=settings.MAX_ITERATIONS,
            handle_parsing_errors=True
        )

    @abstractmethod
    def _initialize_tools(self) -> List[Tool]:
        """Initialize agent-specific tools"""
        pass

    def _create_agent(self):
        """Create ReAct agent"""
        prompt = PromptTemplate.from_template(
            """You are a {agent_type} agent. Use the available tools to answer questions.
            
            Previous conversation:
            {chat_history}
            
            Question: {input}
            
            {agent_scratchpad}"""
        )
        
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt.partial(agent_type=self.agent_type.value)
        )

    async def execute(self, query: str, **kwargs) -> AgentResponse:
        """Execute agent with given query"""
        try:
            # Prepare inputs
            inputs = {
                "input": query,
                **kwargs
            }
            
            # Execute agent
            result = await self.agent_executor.ainvoke(inputs)
            
            # Parse response
            response = self._parse_response(result.get('output', ''))
            
            return AgentResponse(
                agent_type=self.agent_type,
                response=response,
                data=self._extract_data(result),
                source=f"{self.agent_type.value}_agent",
                confidence=0.9
            )
        except Exception as e:
            return AgentResponse(
                agent_type=self.agent_type,
                response=f"Error: {str(e)}",
                source=f"{self.agent_type.value}_agent",
                confidence=0.0
            )

    def _parse_response(self, raw_response: str) -> str:
        """Parse raw agent response"""
        return raw_response

    def _extract_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured data from agent result"""
        return {
            "raw_output": result.get('output', ''),
            "intermediate_steps": str(result.get('intermediate_steps', []))
        }