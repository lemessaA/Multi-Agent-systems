#!/usr/bin/env python3
"""
Debug finance agent execution
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.finance_agent import FinanceAgent

async def test_finance_direct():
    """Test finance agent directly"""
    print("🔍 Testing Finance Agent Directly...")
    
    try:
        agent = FinanceAgent()
        print("✅ FinanceAgent initialized")
        
        # Test Bitcoin price query
        query = "What is the current price of Bitcoin?"
        print(f"📝 Query: {query}")
        
        result = await agent.execute(query)
        print(f"📊 Result: {result}")
        
        # Check if result has actual data
        if isinstance(result, dict):
            if "responses" in result:
                responses = result["responses"]
                print(f"💬 Responses: {len(responses)}")
                for i, resp in enumerate(responses):
                    print(f"   {i+1}. {resp}")
                    if hasattr(resp, 'data') and resp.data:
                        print(f"      Data: {resp.data}")
            else:
                print("❌ No 'responses' key in result")
        else:
            print(f"❌ Result is not a dict: {type(result)}")
            
    except Exception as e:
        print(f"❌ Finance agent error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_finance_direct())
