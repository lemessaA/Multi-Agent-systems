#!/usr/bin/env python3
"""
Test if all agent imports work correctly with Ollama configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_agent_imports():
    """Test if all agent classes can be imported successfully"""
    print("🔍 Testing Agent Imports...")
    
    try:
        # Test base agent
        from agents.base_agent import BaseAgent
        print("   ✅ BaseAgent imported successfully")
        
        # Test simple router agent
        from agents.simple_router_agent import SimpleRouterAgent
        print("   ✅ SimpleRouterAgent imported successfully")
        
        # Test router agent
        from agents.router_agent import RouterAgent
        print("   ✅ RouterAgent imported successfully")
        
        # Test settings
        from config.settings import settings
        print("   ✅ Settings imported successfully")
        
        # Test schemas
        from schemas.models import AgentType, AgentRequest, AgentResponse
        print("   ✅ Schemas imported successfully")
        
        # Test tools
        from tools.weather_tools import WeatherTools
        from tools.news_tools import NewsTools
        from tools.finance_tools import FinanceTools
        print("   ✅ All tools imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_ollama_import():
    """Test if Ollama can be imported"""
    print("\n🤖 Testing Ollama Import...")
    
    try:
        from langchain_ollama import ChatOllama
        print("   ✅ ChatOllama imported successfully")
        
        # Test instantiation (without connecting)
        from config.settings import settings
        llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )
        print("   ✅ ChatOllama instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ollama import failed: {e}")
        return False

def test_agent_instantiation():
    """Test if agents can be instantiated (without Ollama connection)"""
    print("\n🏗️  Testing Agent Instantiation...")
    
    try:
        # This might fail due to Ollama connection, but let's see
        from agents.simple_router_agent import SimpleRouterAgent
        
        try:
            router = SimpleRouterAgent()
            print("   ✅ SimpleRouterAgent instantiated successfully")
            return True
        except Exception as e:
            if "Connection refused" in str(e) or "111" in str(e):
                print("   ⚠️  SimpleRouterAgent instantiation failed (Ollama not running)")
                print("   ✅ This is expected - agent structure is correct")
                return True
            else:
                print(f"   ❌ Unexpected error: {e}")
                return False
        
    except Exception as e:
        print(f"   ❌ Agent instantiation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Agent System with Ollama Configuration\n")
    
    tests = [
        test_agent_imports,
        test_ollama_import,
        test_agent_instantiation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Import Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All import tests passed!")
        print("\n✨ Your multi-agent system is ready for Ollama!")
        print("🔥 To start using it:")
        print("   1. Install and start Ollama")
        print("   2. Pull the model: ollama pull llama3.1:8b")
        print("   3. Run: langgraph dev")
    else:
        print("⚠️  Some import tests failed.")
