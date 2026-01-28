"""
Example queries for the Multi-Agent System
"""

# Example queries for testing the multi-agent system
WEATHER_QUERIES = [
    "What's the weather like in New York?",
    "What is the temperature in London?",
    "Will it rain in Tokyo tomorrow?",
    "How's the climate in Paris?",
    "Is it snowing in Chicago?",
    "What's the weather forecast for Los Angeles?",
    "Temperature in Miami today?",
    "Weather conditions in Sydney",
    "Is it sunny in Barcelona?",
    "What's the humidity level in Dubai?"
]

NEWS_QUERIES = [
    "Show me the latest headlines",
    "What's happening in tech news?",
    "Sports news updates",
    "Political news today",
    "Entertainment headlines",
    "Business news updates",
    "Science and technology news",
    "World news summary",
    "Market news today",
    "Celebrity gossip updates"
]

FINANCE_QUERIES = [
    "What is Apple stock price?",
    "Tesla stock performance",
    "Bitcoin price today",
    "How is Microsoft stock doing?",
    "Amazon stock analysis",
    "Gold price current",
    "Ethereum price",
    "S&P 500 index",
    "NASDAQ performance",
    "Currency exchange rates USD to EUR"
]

MULTI_AGENT_QUERIES = [
    "What's the weather and stock market news today?",
    "Tell me about tech news and Bitcoin price",
    "Weather in New York and latest financial updates",
    "Sports news and Tesla stock performance",
    "Climate change news and renewable energy stocks"
]

# Test cases for different scenarios
TEST_SCENARIOS = {
    "simple_weather": {
        "query": "What's the weather like in London?",
        "expected_agent": "weather",
        "expected_keywords": ["temperature", "weather", "forecast"]
    },
    "simple_news": {
        "query": "Show me latest headlines",
        "expected_agent": "news", 
        "expected_keywords": ["news", "headlines", "updates"]
    },
    "simple_finance": {
        "query": "What is AAPL stock price?",
        "expected_agent": "finance",
        "expected_keywords": ["stock", "price", "AAPL"]
    },
    "complex_query": {
        "query": "Weather in New York and Tesla stock news",
        "expected_agent": "multiple",
        "expected_keywords": ["weather", "stock", "news"]
    }
}

# Example usage
if __name__ == "__main__":
    print("Example Queries for Multi-Agent System")
    print("=" * 50)
    
    print("\nWeather Queries:")
    for query in WEATHER_QUERIES[:3]:
        print(f"  - {query}")
    
    print("\nNews Queries:")
    for query in NEWS_QUERIES[:3]:
        print(f"  - {query}")
        
    print("\nFinance Queries:")
    for query in FINANCE_QUERIES[:3]:
        print(f"  - {query}")
        
    print("\nMulti-Agent Queries:")
    for query in MULTI_AGENT_QUERIES[:3]:
        print(f"  - {query}")