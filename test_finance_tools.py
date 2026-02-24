#!/usr/bin/env python3
"""
Test enhanced finance tools with Google Finance integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.finance_tools import FinanceTools

def test_google_finance():
    """Test Google Finance integration"""
    print("🔍 Testing Google Finance Integration...")
    
    # Test stock price
    print("\n📈 Testing Stock Price (AAPL):")
    aapl_data = FinanceTools.get_google_finance_data("AAPL")
    if 'error' in aapl_data:
        print(f"   ❌ {aapl_data['error']}")
    else:
        print(f"   ✅ Price: ${aapl_data.get('current_price', 'N/A')}")
        print(f"   📊 Change: {aapl_data.get('change', 0.0)} ({aapl_data.get('change_percent', 0.0)}%)")
        print(f"   🌐 Source: {aapl_data.get('source', 'Unknown')}")
    
    # Test crypto
    print("\n₿ Testing Crypto Price (BTC):")
    btc_data = FinanceTools.get_google_finance_data("BTC-USD")
    if 'error' in btc_data:
        print(f"   ❌ {btc_data['error']}")
    else:
        print(f"   ✅ Price: ${btc_data.get('current_price', 'N/A')}")
        print(f"   📊 Change: {btc_data.get('change', 0.0)} ({btc_data.get('change_percent', 0.0)}%)")
        print(f"   🌐 Source: {btc_data.get('source', 'Unknown')}")

def test_real_time_quote():
    """Test real-time quote functionality"""
    print("\n⚡ Testing Real-Time Quote (TSLA):")
    tsla_data = FinanceTools.get_real_time_quote("TSLA")
    if 'error' in tsla_data:
        print(f"   ❌ {tsla_data['error']}")
    else:
        print(f"   ✅ Price: ${tsla_data.get('current_price', 'N/A')}")
        print(f"   🌐 Source: {tsla_data.get('source', 'Unknown')}")
        if tsla_data.get('google_finance_available'):
            print("   🎯 Google Finance data available!")
        else:
            print("   🔄 Using Yahoo Finance fallback")

def test_portfolio():
    """Test portfolio calculation"""
    print("\n💼 Testing Portfolio Calculation:")
    portfolio = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    portfolio_data = FinanceTools.get_portfolio_value(portfolio)
    
    if 'error' in portfolio_data:
        print(f"   ❌ {portfolio_data['error']}")
    else:
        print(f"   ✅ Portfolio Value: ${portfolio_data.get('total_value', 0):.2f}")
        print(f"   📊 Symbols: {portfolio_data.get('symbols_count', 0)}")
        for item in portfolio_data.get('portfolio', []):
            print(f"      - {item['symbol']}: ${item['price']:.2f} ({item['source']})")

def test_market_summary():
    """Test market summary"""
    print("\n📊 Testing Market Summary:")
    market_data = FinanceTools.get_market_summary()
    
    if 'error' in market_data:
        print(f"   ❌ {market_data['error']}")
    else:
        print(f"   ✅ {market_data.get('summary', 'Market summary')}")
        indices = market_data.get('indices', {})
        for symbol, data in indices.items():
            print(f"      - {data['name']}: ${data.get('price', 'N/A')} ({data.get('source', 'Unknown')})")

def test_enhanced_crypto():
    """Test enhanced crypto functionality"""
    print("\n₿ Testing Enhanced Crypto:")
    crypto_data = FinanceTools.get_crypto_price("ethereum")
    
    if 'error' in crypto_data:
        print(f"   ❌ {crypto_data['error']}")
    else:
        print(f"   ✅ ETH Price: ${crypto_data.get('current_price', 'N/A')}")
        print(f"   🌐 Source: {crypto_data.get('source', 'Unknown')}")
        if crypto_data.get('google_finance_available'):
            print("   🎯 Google Finance data available!")
        else:
            print("   🔄 Using Yahoo Finance fallback")

if __name__ == "__main__":
    print("🧪 Testing Enhanced Finance Tools with Google Finance Integration\n")
    
    tests = [
        test_google_finance,
        test_real_time_quote,
        test_portfolio,
        test_market_summary,
        test_enhanced_crypto
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All finance tools working with Google Finance integration!")
    else:
        print("⚠️  Some tests failed. Check output above.")
