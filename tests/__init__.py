"""
Tests for the Multi-Agent System
"""

import sys
import os
import pytest
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test configuration
TEST_CONFIG = {
    "test_data_dir": Path(__file__).parent / "test_data",
    "mock_responses_dir": Path(__file__).parent / "mock_responses",
    "timeout": 30,
    "retry_attempts": 3
}

# Create test directories if they don't exist
for dir_path in [TEST_CONFIG["test_data_dir"], TEST_CONFIG["mock_responses_dir"]]:
    dir_path.mkdir(exist_ok=True)

# Test markers
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "agent: mark test as agent test"
    )
    config.addinivalue_line(
        "markers", "tool: mark test as tool test"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add markers based on file location
        if "test_api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "test_agents" in str(item.fspath):
            item.add_marker(pytest.mark.agent)
        elif "test_tools" in str(item.fspath):
            item.add_marker(pytest.mark.tool)
        
        # Add unit/integration markers based on test name
        if "integration" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        elif "test_" in item.name.lower():
            item.add_marker(pytest.mark.unit)

# Test utilities
class TestUtils:
    """Utility functions for testing"""
    
    @staticmethod
    def create_mock_weather_data(location="New York"):
        """Create mock weather data"""
        return {
            "location": {
                "name": location,
                "region": "NY",
                "country": "USA"
            },
            "current": {
                "temp_c": 22.0,
                "temp_f": 71.6,
                "condition": {
                    "text": "Partly cloudy"
                },
                "humidity": 65,
                "wind_kph": 15.0
            }
        }
    
    @staticmethod
    def create_mock_news_data():
        """Create mock news data"""
        return {
            "status": "ok",
            "totalResults": 2,
            "articles": [
                {
                    "title": "Test Article 1",
                    "description": "Test description 1",
                    "source": {"name": "Test Source"},
                    "publishedAt": "2024-01-28T10:00:00Z"
                },
                {
                    "title": "Test Article 2", 
                    "description": "Test description 2",
                    "source": {"name": "Test Source"},
                    "publishedAt": "2024-01-28T09:00:00Z"
                }
            ]
        }
    
    @staticmethod
    def create_mock_finance_data(symbol="AAPL"):
        """Create mock finance data"""
        return {
            "Global Quote": {
                "01. symbol": symbol,
                "02. open": "175.00",
                "03. high": "176.00",
                "04. low": "174.00",
                "05. price": "175.50",
                "06. volume": "50000000",
                "09. change": "0.50",
                "10. change percent": "0.29%"
            }
        }
    
    @staticmethod
    def create_mock_agent_response(agent_type="weather", response="Test response"):
        """Create mock agent response"""
        from schemas.models import AgentResponse, AgentType
        
        agent_type_map = {
            "weather": AgentType.WEATHER,
            "news": AgentType.NEWS,
            "finance": AgentType.FINANCE
        }
        
        return AgentResponse(
            agent_type=agent_type_map.get(agent_type, AgentType.WEATHER),
            response=response,
            source=f"{agent_type}_agent",
            confidence=0.9
        )

# Export test utilities
__all__ = [
    "TEST_CONFIG",
    "TestUtils"
]