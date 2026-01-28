"""
Tests for the Multi-Agent System agents
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from agents.simple_router_agent import SimpleRouterAgent, RouterState
from schemas.models import AgentType, AgentRequest, AgentResponse


class TestSimpleRouterAgent:
    """Test cases for SimpleRouterAgent"""
    
    @pytest.fixture
    def router_agent(self):
        """Create a SimpleRouterAgent instance for testing"""
        with patch('agents.simple_router_agent.settings.GROQ_API_KEY', 'test_key'):
            return SimpleRouterAgent()
    
    @pytest.fixture
    def sample_state(self):
        """Create a sample RouterState for testing"""
        state = RouterState()
        state.query = "What's the weather like in New York?"
        state.conversation_id = "test-conversation-123"
        state.start_time = None
        return state
    
    @pytest.mark.asyncio
    async def test_route_query_weather(self, router_agent, sample_state):
        """Test routing to weather agent"""
        sample_state.query = "What's the weather like in London?"
        
        with patch.object(router_agent.llm, 'ainvoke') as mock_llm:
            mock_llm.return_value = Mock(content="weather")
            
            result = await router_agent._route_query(sample_state)
            
            assert result["agent_type"] == "weather"
            mock_llm.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_route_query_news(self, router_agent, sample_state):
        """Test routing to news agent"""
        sample_state.query = "Show me latest headlines"
        
        with patch.object(router_agent.llm, 'ainvoke') as mock_llm:
            mock_llm.return_value = Mock(content="news")
            
            result = await router_agent._route_query(sample_state)
            
            assert result["agent_type"] == "news"
            mock_llm.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_route_query_finance(self, router_agent, sample_state):
        """Test routing to finance agent"""
        sample_state.query = "What is Apple stock price?"
        
        with patch.object(router_agent.llm, 'ainvoke') as mock_llm:
            mock_llm.return_value = Mock(content="finance")
            
            result = await router_agent._route_query(sample_state)
            
            assert result["agent_type"] == "finance"
            mock_llm.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_route_query_multiple(self, router_agent, sample_state):
        """Test routing to multiple agents"""
        sample_state.query = "Weather and stock market news"
        
        with patch.object(router_agent.llm, 'ainvoke') as mock_llm:
            mock_llm.return_value = Mock(content="multiple")
            
            result = await router_agent._route_query(sample_state)
            
            assert result["agent_type"] == "multiple"
            mock_llm.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_weather_agent(self, router_agent, sample_state):
        """Test weather agent execution"""
        result = await router_agent._execute_weather_agent(sample_state)
        
        assert "responses" in result
        assert len(result["responses"]) == 1
        assert result["responses"][0].agent_type == AgentType.WEATHER
        assert "New York" in result["responses"][0].response
    
    @pytest.mark.asyncio
    async def test_execute_news_agent(self, router_agent, sample_state):
        """Test news agent execution"""
        result = await router_agent._execute_news_agent(sample_state)
        
        assert "responses" in result
        assert len(result["responses"]) == 1
        assert result["responses"][0].agent_type == AgentType.NEWS
        assert "New York" in result["responses"][0].response
    
    @pytest.mark.asyncio
    async def test_execute_finance_agent(self, router_agent, sample_state):
        """Test finance agent execution"""
        result = await router_agent._execute_finance_agent(sample_state)
        
        assert "responses" in result
        assert len(result["responses"]) == 1
        assert result["responses"][0].agent_type == AgentType.FINANCE
        assert "New York" in result["responses"][0].response
    
    def test_decide_next_node(self, router_agent, sample_state):
        """Test decision logic for next node"""
        sample_state.agent_type = "weather"
        assert router_agent._decide_next_node(sample_state) == "weather"
        
        sample_state.agent_type = "news"
        assert router_agent._decide_next_node(sample_state) == "news"
        
        sample_state.agent_type = "finance"
        assert router_agent._decide_next_node(sample_state) == "finance"
        
        sample_state.agent_type = "multiple"
        assert router_agent._decide_next_node(sample_state) == "multiple"
    
    @pytest.mark.asyncio
    async def test_aggregate_responses(self, router_agent, sample_state):
        """Test response aggregation"""
        sample_state.responses = [
            AgentResponse(
                agent_type=AgentType.WEATHER,
                response="Sunny, 75°F",
                source="weather_agent",
                confidence=0.9
            )
        ]
        
        result = await router_agent._aggregate_responses(sample_state)
        
        assert result["responses"] == sample_state.responses
        assert result["execution_complete"] is True
    
    @pytest.mark.asyncio
    async def test_process_with_auto_routing(self, router_agent):
        """Test processing with automatic routing"""
        request = AgentRequest(query="What's the weather like in Tokyo?")
        
        with patch.object(router_agent.workflow, 'ainvoke') as mock_workflow:
            mock_workflow.return_value = {
                "responses": [
                    AgentResponse(
                        agent_type=AgentType.WEATHER,
                        response="Cloudy, 68°F",
                        source="weather_agent",
                        confidence=0.8
                    )
                ]
            }
            
            result = await router_agent.process(request)
            
            assert "conversation_id" in result
            assert "responses" in result
            assert "execution_time" in result
            assert result["agent_type"] == "auto"
            mock_workflow.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_with_specific_agent(self, router_agent):
        """Test processing with specific agent type"""
        request = AgentRequest(
            query="What's the weather like in Paris?",
            agent_type=AgentType.WEATHER
        )
        
        with patch.object(router_agent, '_execute_weather_agent') as mock_weather:
            mock_weather.return_value = {
                "responses": [
                    AgentResponse(
                        agent_type=AgentType.WEATHER,
                        response="Rainy, 55°F",
                        source="weather_agent",
                        confidence=0.9
                    )
                ]
            }
            
            result = await router_agent.process(request)
            
            assert "conversation_id" in result
            assert "responses" in result
            assert "execution_time" in result
            assert result["agent_type"] == AgentType.WEATHER
            mock_weather.assert_called_once()


class TestRouterState:
    """Test cases for RouterState"""
    
    def test_router_state_initialization(self):
        """Test RouterState initialization"""
        state = RouterState()
        
        assert state.query == ""
        assert state.agent_type is None
        assert state.responses == []
        assert state.conversation_id == ""
        assert state.start_time is None


class TestAgentResponse:
    """Test cases for AgentResponse"""
    
    def test_agent_response_creation(self):
        """Test AgentResponse creation"""
        response = AgentResponse(
            agent_type=AgentType.WEATHER,
            response="Sunny, 75°F",
            source="weather_agent",
            confidence=0.9
        )
        
        assert response.agent_type == AgentType.WEATHER
        assert response.response == "Sunny, 75°F"
        assert response.source == "weather_agent"
        assert response.confidence == 0.9


if __name__ == "__main__":
    pytest.main([__file__, "-v"])