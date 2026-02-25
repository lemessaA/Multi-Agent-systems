import re
import os

filepath = "/home/lemessa-ahmed/multi-agent-system/tools/finance_tools.py"
with open(filepath, "r") as f:
    content = f.read()

# 1. Add yfinance retry helper
retry_helper = """class FinanceTools:
    @staticmethod
    def _yf_with_retry(func, *args, max_retries=3, **kwargs):
        import time
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise e
"""
content = content.replace("class FinanceTools:", retry_helper)

# 2. Replace get_google_finance_data with get_alpha_vantage_data
av_method = """    @staticmethod
    def get_alpha_vantage_data(symbol: str) -> Dict[str, Any]:
        \"\"\"Get real-time financial data from Alpha Vantage\"\"\"
        try:
            if not settings.ALPHA_VANTAGE_API_KEY:
                return {'error': 'Alpha Vantage API key not configured'}
                
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": settings.ALPHA_VANTAGE_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "Global Quote" in data and data["Global Quote"]:
                    quote = data["Global Quote"]
                    return {
                        'symbol': symbol.upper(),
                        'current_price': float(quote.get("05. price", 0)),
                        'change': float(quote.get("09. change", 0)),
                        'change_percent': float(quote.get("10. change percent", "0%").strip("%")),
                        'source': 'Alpha Vantage',
                        'timestamp': time.time()
                    }
                elif "Information" in data:
                    return {'error': f"Alpha Vantage rate limit: {data['Information']}"}
                else:
                    return {'error': f"Could not parse quote data for {symbol}"}
            else:
                return {'error': f"Failed to fetch Alpha Vantage data: HTTP {response.status_code}"}
        except Exception as e:
            return {'error': f"Alpha Vantage error: {str(e)}"}"""

content = re.sub(r'    @staticmethod\n    def get_google_finance_data.*?except Exception as e:\n            return \{\'error\': f"Google Finance error: \{str\(e\)\}"\}', av_method, content, flags=re.DOTALL)

# 3. Update references from get_google_finance_data to get_alpha_vantage_data
content = content.replace('FinanceTools.get_google_finance_data(symbol, "price")', 'FinanceTools.get_alpha_vantage_data(symbol)')
content = content.replace('FinanceTools.get_google_finance_data(f"{crypto.upper()}-USD", "price")', 'FinanceTools.get_alpha_vantage_data(f"{crypto.upper()}-USD")')

# 4. Replace yfinance calls with retry wrapper in get_stock_price
content = content.replace('stock = yf.Ticker(symbol)\n            info = stock.info\n            history = stock.history(period="1d")', 
                          'stock = yf.Ticker(symbol)\n            info = FinanceTools._yf_with_retry(lambda: stock.info)\n            history = FinanceTools._yf_with_retry(stock.history, period="1d")')

# 5. Replace yfinance calls with retry wrapper in get_crypto_price
content = content.replace('stock = yf.Ticker(symbol)\n            info = stock.info',
                          'stock = yf.Ticker(symbol)\n            info = FinanceTools._yf_with_retry(lambda: stock.info)')

# 6. Replace yfinance calls in get_advanced_portfolio_analysis
content = content.replace('hist = ticker.history(period=timeframe)',
                          'hist = FinanceTools._yf_with_retry(ticker.history, period=timeframe)')

# 7. Replace yfinance calls in get_technical_indicators
content = content.replace('hist = ticker.history(period=period)',
                          'hist = FinanceTools._yf_with_retry(ticker.history, period=period)')

# 8. Replace yfinance calls in get_exchange_rate
content = content.replace('stock = yf.Ticker(symbol)\n                info = stock.info',
                          'stock = yf.Ticker(symbol)\n                info = FinanceTools._yf_with_retry(lambda: stock.info)')

# 9. Update get_financial_news to use NewsAPI
news_method = """    @staticmethod
    def get_financial_news(symbol: str = None, category: str = "business") -> Dict[str, Any]:
        \"\"\"Get financial news using NewsAPI\"\"\"
        try:
            url = "https://newsapi.org/v2/everything" if symbol else "https://newsapi.org/v2/top-headlines"
            params = {'apiKey': settings.NEWS_API_KEY, 'language': 'en', 'pageSize': 5}
            
            if symbol:
                params['q'] = f"{symbol} stock OR finance OR market"
                params['sortBy'] = 'relevance'
            else:
                params['category'] = category
                params['country'] = 'us'
                
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                headlines = [article['title'] for article in data.get('articles', [])]
                
                return {
                    'symbol': symbol,
                    'category': category,
                    'headlines': headlines if headlines else ["No specific news found for this symbol today."],
                    'market_impact': 'unknown',
                    'timestamp': time.time(),
                    'source': 'NewsAPI'
                }
            else:
                return {'error': f"NewsAPI failed: {response.text}"}
        except Exception as e:
            return {'error': f"Financial news error: {str(e)}"}"""

content = re.sub(r'    @staticmethod\n    def get_financial_news.*?except Exception as e:\n            return \{\'error\': f"Financial news error: \{str\(e\)\}"\}', news_method, content, flags=re.DOTALL)

with open(filepath, "w") as f:
    f.write(content)

print("Patch applied to finance_tools.py")
