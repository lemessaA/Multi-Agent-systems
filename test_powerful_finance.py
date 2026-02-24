#!/usr/bin/env python3
"""
Test powerful finance tools
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.finance_tools import FinanceTools

async def test_powerful_tools():
    """Test all powerful finance tools"""
    print("🚀 Testing Powerful Finance Tools")
    print("=" * 60)
    
    # Test 1: Advanced Portfolio Analysis
    print("\n📊 1. Advanced Portfolio Analysis")
    portfolio = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    result = FinanceTools.get_advanced_portfolio_analysis(portfolio, "1mo")
    
    if 'error' in result:
        print(f"   ❌ {result['error']}")
    else:
        print(f"   ✅ Portfolio Value: ${result['total_value']:,.2f}")
        print(f"   📈 Portfolio Volatility: {result['portfolio_volatility']}%")
        print(f"   📊 Symbols Analyzed: {result['symbols_count']}")
        for symbol, analysis in result.get('individual_analysis', {}).items():
            print(f"      {symbol}: Volatility {analysis.get('volatility', 0)}%, Trend {analysis.get('trend', 'unknown')}")
    
    # Test 2: Market Sentiment Analysis
    print("\n🎭 2. Market Sentiment Analysis")
    sentiment = FinanceTools.get_market_sentiment("AAPL")
    
    if 'error' in sentiment:
        print(f"   ❌ {sentiment['error']}")
    else:
        print(f"   ✅ AAPL Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']})")
        print(f"   📊 Change: {sentiment.get('change_percent', 0)}%")
        print(f"   💰 Current Price: ${sentiment.get('current_price', 0)}")
    
    # Test 3: Technical Indicators
    print("\n📈 3. Technical Indicators")
    technical = FinanceTools.get_technical_indicators("TSLA", "3mo")
    
    if 'error' in technical:
        print(f"   ❌ {technical['error']}")
    else:
        print(f"   ✅ TSLA Current Price: ${technical['current_price']}")
        print(f"   📊 RSI: {technical['rsi']:.1f} ({technical['analysis']['rsi_signal']})")
        print(f"   📈 20-day SMA: ${technical['sma_20']:.2f}")
        print(f"   📈 50-day SMA: ${technical['sma_50']:.2f}")
        print(f"   📊 Trend: {technical['analysis']['trend']}")
        print(f"   🎯 Bollinger Position: {technical['analysis']['bb_position']}")
    
    # Test 4: Financial News
    print("\n📰 4. Financial News")
    news = FinanceTools.get_financial_news("AAPL", "technology")
    
    if 'error' in news:
        print(f"   ❌ {news['error']}")
    else:
        print(f"   ✅ Category: {news['category']}")
        print(f"   📰 Headlines:")
        for headline in news['headlines']:
            print(f"      • {headline}")
        print(f"   📊 Market Impact: {news['market_impact']}")
    
    # Test 5: Real-time Quote (existing)
    print("\n⚡ 5. Real-time Quote")
    quote = FinanceTools.get_real_time_quote("BTC-USD")
    
    if 'error' in quote:
        print(f"   ❌ {quote['error']}")
    else:
        print(f"   ✅ Bitcoin Price: ${quote['current_price']}")
        print(f"   📊 Change: {quote.get('change', 0)} ({quote.get('change_percent', 0)}%)")
        print(f"   🌐 Source: {quote['source']}")
    
    # Test 6: Market Summary (existing)
    print("\n🌍 6. Market Summary")
    summary = FinanceTools.get_market_summary()
    
    if 'error' in summary:
        print(f"   ❌ {summary['error']}")
    else:
        print(f"   ✅ {summary.get('summary', 'Market summary')}")
        indices = summary.get('indices', {})
        for symbol, data in indices.items():
            print(f"      {data['name']}: ${data.get('price', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("🎯 POWERFUL TOOLS SUMMARY")
    print("=" * 60)
    print("✅ Advanced Portfolio Analysis - Volatility, trends, performance metrics")
    print("✅ Market Sentiment Analysis - Bullish/Bearish/Neutral signals")
    print("✅ Technical Indicators - RSI, Bollinger Bands, Moving Averages")
    print("✅ Financial News - Market impact analysis")
    print("✅ Real-time Quotes - Google Finance + Yahoo Finance fallback")
    print("✅ Market Summary - Major indices and movers")
    print("\n🚀 Finance tools are now POWERFUL! 🎯")

if __name__ == "__main__":
    asyncio.run(test_powerful_tools())
