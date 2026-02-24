#!/usr/bin/env python3
"""
Test response times of the multi-agent system
"""

import time
import asyncio
import aiohttp
import json
from datetime import datetime

async def test_response_time(query: str, agent_type: str = None) -> dict:
    """Test response time for a single query"""
    url = "http://localhost:8002/query"
    payload = {
        "query": query,
        "agent_type": agent_type,
        "parameters": {}
    }
    
    start_time = time.time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    return {
                        "query": query,
                        "agent_type": agent_type or "auto",
                        "response_time": response_time,
                        "success": True,
                        "conversation_id": data.get("result", {}).get("conversation_id"),
                        "execution_time": data.get("result", {}).get("execution_time", 0),
                        "provider": data.get("provider", "unknown")
                    }
                else:
                    end_time = time.time()
                    return {
                        "query": query,
                        "agent_type": agent_type or "auto",
                        "response_time": end_time - start_time,
                        "success": False,
                        "error": f"HTTP {response.status}"
                    }
    except Exception as e:
        end_time = time.time()
        return {
            "query": query,
            "agent_type": agent_type or "auto",
            "response_time": end_time - start_time,
            "success": False,
            "error": str(e)
        }

async def run_performance_tests():
    """Run comprehensive performance tests"""
    print("🚀 Testing Multi-Agent System Response Times")
    print("=" * 60)
    
    test_queries = [
        ("What is the weather in London?", "weather"),
        ("What are the latest tech news headlines?", "news"),
        ("What is the current price of Bitcoin?", "finance"),
        ("Weather in Tokyo and latest AI news", None),  # Auto routing
        ("Current price of AAPL and Tesla stock", "finance"),
        ("3-day weather forecast for New York", "weather"),
        ("Top business news today", "news"),
        ("Portfolio value of AAPL, GOOGL, MSFT", "finance"),
    ]
    
    results = []
    
    for i, (query, agent_type) in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        if agent_type:
            print(f"   🎯 Agent: {agent_type}")
        else:
            print("   🎯 Agent: Auto-routing")
        
        result = await test_response_time(query, agent_type)
        results.append(result)
        
        if result["success"]:
            print(f"   ✅ Response time: {result['response_time']:.3f}s")
            print(f"   📊 Execution time: {result['execution_time']:.3f}s")
            print(f"   🤖 Provider: {result['provider']}")
            print(f"   🆔 Conversation ID: {result['conversation_id']}")
        else:
            print(f"   ❌ Error: {result['error']}")
            print(f"   ⏱️  Time: {result['response_time']:.3f}s")
    
    # Performance summary
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    successful_results = [r for r in results if r["success"]]
    if successful_results:
        avg_response_time = sum(r["response_time"] for r in successful_results) / len(successful_results)
        min_response_time = min(r["response_time"] for r in successful_results)
        max_response_time = max(r["response_time"] for r in successful_results)
        
        print(f"📈 Total Tests: {len(results)}")
        print(f"✅ Successful: {len(successful_results)}")
        print(f"❌ Failed: {len(results) - len(successful_results)}")
        print(f"⏱️  Average Response Time: {avg_response_time:.3f}s")
        print(f"⚡ Fastest Response: {min_response_time:.3f}s")
        print(f"🐌 Slowest Response: {max_response_time:.3f}s")
        
        # Performance by agent type
        print("\n📊 BY AGENT TYPE:")
        agent_stats = {}
        for result in successful_results:
            agent = result["agent_type"]
            if agent not in agent_stats:
                agent_stats[agent] = []
            agent_stats[agent].append(result["response_time"])
        
        for agent, times in agent_stats.items():
            avg_time = sum(times) / len(times)
            print(f"   {agent.capitalize()}: {avg_time:.3f}s (avg) - {len(times)} tests")
    else:
        print("❌ All tests failed!")

if __name__ == "__main__":
    asyncio.run(run_performance_tests())
