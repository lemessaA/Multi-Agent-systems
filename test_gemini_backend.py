#!/usr/bin/env python3
"""
Test backend with Gemini LLM provider
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_gemini_backend():
    """Test backend with Gemini LLM"""
    print("🚀 Testing Backend with Gemini LLM...")
    
    try:
        # Test imports
        from agents.simple_router_agent import SimpleRouterAgent
        from schemas.models import AgentRequest
        from config.settings import settings
        from llm_factory import get_chat_llm
        
        print("✅ All imports successful")
        print(f"🤖 Provider: {settings.LLM_PROVIDER}")
        print(f"🌐 Gemini Model: {settings.GEMINI_MODEL}")
        
        # Test LLM factory with Gemini
        try:
            llm = get_chat_llm(provider="gemini", temperature=0.1)
            print("✅ Gemini LLM initialized successfully")
            
            # Simple test
            response = await llm.ainvoke("Hello, respond with just 'OK'")
            print(f"✅ Gemini response: {response.content}")
            
        except Exception as e:
            print(f"❌ Gemini LLM failed: {e}")
            if "API key" in str(e):
                print("💡 Set GEMINI_API_KEY in your .env file")
            return False
        
        # Test router agent with Gemini
        try:
            router = SimpleRouterAgent()
            print("✅ Router agent initialized with Gemini")
            
            # Test a simple query
            test_request = AgentRequest(
                query="What is the capital of France?",
                agent_type=None,
                parameters={}
            )
            
            print("📝 Processing test query...")
            result = await router.process(test_request)
            
            print("✅ Query processed successfully!")
            print(f"📊 Result: {result}")
            
        except Exception as e:
            print(f"❌ Router agent failed: {e}")
            return False
        
        # Test tools directly
        print("\n🔧 Testing Tools...")
        
        from tools.weather_tools import WeatherTools
        from tools.news_tools import NewsTools
        from tools.finance_tools import FinanceTools
        
        print("✅ Weather tools imported")
        print("✅ News tools imported") 
        print("✅ Finance tools imported")
        
        # Test weather tool (will fail without API key but shows structure)
        try:
            weather_result = WeatherTools.get_current_weather("London")
            if "error" in weather_result:
                print(f"⚠️  Weather tool: {weather_result['error']}")
            else:
                print(f"✅ Weather tool: {weather_result}")
        except Exception as e:
            print(f"❌ Weather tool error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Starting Gemini Backend Tests\n")
    
    # Set environment to use Gemini
    os.environ["LLM_PROVIDER"] = "gemini"
    
    success = asyncio.run(test_gemini_backend())
    
    print(f"\n📊 Test Results:")
    print(f"   Gemini Backend: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 Backend is working with Gemini!")
        print("🔥 To start the API server:")
        print("   1. Set GEMINI_API_KEY in your .env file")
        print("   2. Run: python main.py")
        print("   3. Or use Ollama by setting LLM_PROVIDER=ollama")
    else:
        print("\n⚠️  Tests failed. Check the output above.")
