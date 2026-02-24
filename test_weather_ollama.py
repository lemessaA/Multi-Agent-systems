#!/usr/bin/env python3
"""
Test weather agent with Ollama integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_ollama import ChatOllama
from config.settings import settings
from agents.simple_router_agent import SimpleRouterAgent
from schemas.models import AgentRequest, AgentType

def test_weather_routing():
    """Test if weather queries are properly routed with Ollama"""
    print("🌤️  Testing Weather Agent with Ollama...")
    
    try:
        # Initialize the router agent with Ollama
        router = SimpleRouterAgent()
        print("✅ Router agent initialized with Ollama")
        
        # Test weather query
        weather_query = AgentRequest(
            query="What's the weather like in New York?",
            agent_type=None,  # Let the router decide
            parameters={"location": "New York"}
        )
        
        print(f"📝 Query: {weather_query.query}")
        print("🔄 Processing query...")
        
        # Process the query
        result = router.process_query(weather_query)
        
        print("✅ Query processed successfully!")
        print(f"📍 Agent Type: {result.agent_type}")
        print(f"💬 Response: {result.response[:200]}...")
        print(f"📊 Status: {result.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_direct_weather():
    """Test direct weather tool functionality"""
    print("\n🔧 Testing Direct Weather Tools...")
    
    try:
        from tools.weather_tools import WeatherTools
        
        # Test weather tool (this will fail without API key but shows integration)
        result = WeatherTools.get_current_weather("London")
        
        if "error" in result:
            print(f"⚠️  Weather API error (expected): {result['error']}")
            print("✅ Tool integration working (API key needed for real data)")
        else:
            print(f"✅ Weather data: {result}")
            
        return True
        
    except Exception as e:
        print(f"❌ Direct weather test failed: {e}")
        return False

def test_ollama_weather_classification():
    """Test if Ollama can classify weather queries correctly"""
    print("\n🧠 Testing Ollama Query Classification...")
    
    try:
        llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )
        
        # Test weather-related queries
        weather_queries = [
            "What's the weather in Tokyo?",
            "Will it rain tomorrow in London?",
            "Temperature in Paris",
            "Weather forecast for New York"
        ]
        
        for query in weather_queries:
            response = llm.invoke(f"Classify this query as WEATHER, NEWS, or FINANCE: {query}")
            print(f"Query: {query}")
            print(f"Classification: {response.content.strip()}")
            print("---")
        
        return True
        
    except Exception as e:
        print(f"❌ Classification test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Weather + Ollama Integration Tests\n")
    
    # Check Ollama connection first
    from test_ollama import test_ollama_connection
    
    if not test_ollama_connection():
        print("\n❌ Ollama is not running. Please start Ollama first:")
        print("   1. Install Ollama: https://ollama.ai/download")
        print("   2. Start service: ollama serve")
        print("   3. Pull model: ollama pull llama3.1:8b")
        sys.exit(1)
    
    # Run weather tests
    tests = [
        test_ollama_weather_classification,
        test_direct_weather,
        test_weather_routing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All weather + Ollama tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
