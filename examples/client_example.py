"""
Client example for the Multi-Agent System
Demonstrates how to interact with the API and LangGraph Studio
"""

import asyncio
import json
import requests
from typing import Dict, Any, List
from examples.example_queries import WEATHER_QUERIES, NEWS_QUERIES, FINANCE_QUERIES, MULTI_AGENT_QUERIES


class MultiAgentClient:
    """Client for interacting with the Multi-Agent System"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:2024"):
        self.base_url = base_url
        self.assistant_id = "agen"
    
    async def query_agent(self, query: str, agent_type: str = None) -> Dict[str, Any]:
        """
        Send a query to the multi-agent system
        
        Args:
            query: The user query
            agent_type: Optional specific agent to use (weather, news, finance)
            
        Returns:
            Response from the agent system
        """
        url = f"{self.base_url}/runs/stream"
        
        payload = {
            "assistant_id": self.assistant_id,
            "input": {
                "messages": [{
                    "role": "user", 
                    "content": query
                }]
            }
        }
        
        if agent_type:
            payload["input"]["agent_type"] = agent_type
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            # Parse streaming response
            events = []
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        try:
                            events.append(json.loads(data))
                        except json.JSONDecodeError:
                            continue
            
            return {
                "success": True,
                "events": events,
                "query": query,
                "agent_type": agent_type
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "agent_type": agent_type
            }
    
    async def batch_test(self, queries: List[str], agent_type: str = None) -> List[Dict[str, Any]]:
        """
        Test multiple queries in batch
        
        Args:
            queries: List of queries to test
            agent_type: Optional specific agent to use
            
        Returns:
            List of responses
        """
        results = []
        for i, query in enumerate(queries):
            print(f"Testing query {i+1}/{len(queries)}: {query}")
            result = await self.query_agent(query, agent_type)
            results.append(result)
            
            # Add delay between requests
            await asyncio.sleep(1)
        
        return results
    
    def print_results(self, results: List[Dict[str, Any]]):
        """Print test results in a readable format"""
        print("\n" + "="*80)
        print("TEST RESULTS")
        print("="*80)
        
        for i, result in enumerate(results):
            print(f"\n{i+1}. Query: {result['query']}")
            print(f"   Agent Type: {result.get('agent_type', 'auto')}")
            
            if result['success']:
                print("   ✅ Success")
                events = result.get('events', [])
                for event in events:
                    if 'error' in event:
                        print(f"   ⚠️  Error: {event['error']}")
                    elif 'data' in event:
                        print(f"   📊 Data: {event['data']}")
            else:
                print(f"   ❌ Failed: {result['error']}")
    
    async def test_all_categories(self):
        """Test queries from all categories"""
        print("🧪 Testing all query categories...")
        
        # Test weather queries
        print("\n🌤️  Testing Weather Queries:")
        weather_results = await self.batch_test(WEATHER_QUERIES[:3])
        self.print_results(weather_results)
        
        # Test news queries
        print("\n📰 Testing News Queries:")
        news_results = await self.batch_test(NEWS_QUERIES[:3])
        self.print_results(news_results)
        
        # Test finance queries
        print("\n💰 Testing Finance Queries:")
        finance_results = await self.batch_test(FINANCE_QUERIES[:3])
        self.print_results(finance_results)
        
        # Test multi-agent queries
        print("\n🔄 Testing Multi-Agent Queries:")
        multi_results = await self.batch_test(MULTI_AGENT_QUERIES[:2])
        self.print_results(multi_results)
        
        return {
            "weather": weather_results,
            "news": news_results,
            "finance": finance_results,
            "multi_agent": multi_results
        }


async def main():
    """Main example usage"""
    client = MultiAgentClient()
    
    print("🚀 Multi-Agent System Client Example")
    print("="*50)
    
    # Test single query
    print("\n🔍 Testing single query...")
    result = await client.query_agent("What's the weather like in New York?")
    client.print_results([result])
    
    # Test all categories
    await client.test_all_categories()
    
    print("\n✨ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())