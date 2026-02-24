import requests
import yfinance as yf
import pandas as pd
import time
import re
from typing import Optional, Dict, Any
from config.settings import settings

class FinanceTools:
    @staticmethod
    def get_google_finance_data(symbol: str, data_type: str = "price") -> Dict[str, Any]:
        """Get real-time financial data from Google Finance"""
        try:
            # Google Finance URL construction
            base_url = "https://www.google.com/finance/quote"
            
            if data_type == "price":
                url = f"{base_url}/{symbol}"
            elif data_type == "chart":
                url = f"{base_url}/{symbol}:NASDAQ"
            else:
                url = f"{base_url}/{symbol}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse Google Finance response
                content = response.text
                
                # Extract price data (simplified parsing)
                import re
                
                price_match = re.search(r'data-last-price="([^"]+)"', content)
                change_match = re.search(r'data-change="([^"]+)"', content)
                change_percent_match = re.search(r'data-change-percent="([^"]+)"', content)
                
                if price_match:
                    current_price = float(price_match.group(1).replace(',', ''))
                    change = float(change_match.group(1)) if change_match else 0.0
                    change_percent = float(change_percent_match.group(1)) if change_percent_match else 0.0
                    
                    return {
                        'symbol': symbol.upper(),
                        'current_price': current_price,
                        'change': change,
                        'change_percent': change_percent,
                        'source': 'Google Finance',
                        'timestamp': time.time()
                    }
                else:
                    return {'error': f"Could not parse price data for {symbol}"}
            else:
                return {'error': f"Failed to fetch Google Finance data: HTTP {response.status_code}"}
                
        except Exception as e:
            return {'error': f"Google Finance error: {str(e)}"}

    @staticmethod
    def get_real_time_quote(symbol: str) -> Dict[str, Any]:
        """Get comprehensive real-time quote from multiple sources"""
        try:
            # Try Google Finance first (fastest)
            google_data = FinanceTools.get_google_finance_data(symbol, "price")
            
            if 'error' not in google_data:
                return google_data
            
            # Fallback to yfinance
            yf_data = FinanceTools.get_stock_price(symbol)
            
            if 'error' not in yf_data:
                yf_data['source'] = 'Yahoo Finance (fallback)'
                return yf_data
            
            return {'error': f"Unable to fetch real-time data for {symbol}"}
            
        except Exception as e:
            return {'error': f"Real-time quote error: {str(e)}"}

    @staticmethod
    def get_market_movers(market: str = "US") -> Dict[str, Any]:
        """Get market movers and top gainers/losers"""
        try:
            # Google Finance market movers URL
            url = f"https://www.google.com/finance/markets/index/{market}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # This is a simplified version - in production, you'd parse the HTML
                return {
                    'market': market,
                    'source': 'Google Finance',
                    'timestamp': time.time(),
                    'note': 'Market movers data available (requires HTML parsing for full data)'
                }
            else:
                return {'error': f"Failed to fetch market movers: HTTP {response.status_code}"}
                
        except Exception as e:
            return {'error': f"Market movers error: {str(e)}"}

    @staticmethod
    def get_stock_price(symbol: str) -> Dict[str, Any]:
        """Get current stock price using Google Finance with yfinance fallback"""
        try:
            # Try Google Finance first for real-time data
            google_data = FinanceTools.get_google_finance_data(symbol, "price")
            
            if 'error' not in google_data:
                return google_data
            
            # Fallback to yfinance for comprehensive data
            stock = yf.Ticker(symbol)
            info = stock.info
            history = stock.history(period="1d")
            
            if history.empty:
                return {'error': f"No data found for symbol {symbol}"}
            
            # Combine data from both sources
            return {
                'symbol': symbol,
                'current_price': info.get('currentPrice', info.get('regularMarketPrice')),
                'open': float(history['Open'].iloc[0]),
                'high': float(history['High'].iloc[0]),
                'low': float(history['Low'].iloc[0]),
                'close': float(history['Close'].iloc[0]),
                'volume': int(history['Volume'].iloc[0]),
                'company_name': info.get('longName', ''),
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap'),
                'source': 'Yahoo Finance (Google Finance unavailable)',
                'google_finance_available': False
            }
        except Exception as e:
            return {'error': f"Failed to fetch stock data: {str(e)}"}

    @staticmethod
    def get_crypto_price(crypto: str) -> Dict[str, Any]:
        """Get cryptocurrency price using Google Finance with yfinance fallback"""
        try:
            # Try Google Finance first for real-time crypto data
            google_data = FinanceTools.get_google_finance_data(f"{crypto.upper()}-USD", "price")
            
            if 'error' not in google_data:
                return {
                    'crypto': crypto,
                    'symbol': f"{crypto.upper()}-USD",
                    'current_price': google_data['current_price'],
                    'change': google_data.get('change', 0.0),
                    'change_percent': google_data.get('change_percent', 0.0),
                    'source': 'Google Finance',
                    'timestamp': google_data.get('timestamp')
                }
            
            # Fallback to yfinance for crypto
            cryptos = {
                'bitcoin': 'BTC-USD',
                'ethereum': 'ETH-USD',
                'solana': 'SOL-USD',
                'cardano': 'ADA-USD'
            }
            
            symbol = cryptos.get(crypto.lower(), f"{crypto.upper()}-USD")
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                'crypto': crypto,
                'symbol': symbol,
                'current_price': info.get('currentPrice'),
                'market_cap': info.get('marketCap'),
                '24h_high': info.get('dayHigh'),
                '24h_low': info.get('dayLow'),
                '24h_volume': info.get('volume'),
                'source': 'Yahoo Finance (Google Finance unavailable)',
                'google_finance_available': False
            }
        except Exception as e:
            return {'error': f"Failed to fetch crypto data: {str(e)}"}

    @staticmethod
    def get_portfolio_value(symbols: list) -> Dict[str, Any]:
        """Calculate portfolio value for multiple symbols"""
        try:
            portfolio_data = []
            total_value = 0.0
            
            for symbol in symbols:
                data = FinanceTools.get_real_time_quote(symbol)
                if 'error' not in data and 'current_price' in data:
                    portfolio_data.append({
                        'symbol': symbol,
                        'price': data['current_price'],
                        'source': data.get('source', 'Unknown')
                    })
                    total_value += data['current_price']
            
            return {
                'portfolio': portfolio_data,
                'total_value': total_value,
                'symbols_count': len(symbols),
                'currency': 'USD',
                'timestamp': time.time()
            }
        except Exception as e:
            return {'error': f"Portfolio calculation error: {str(e)}"}

    @staticmethod
    def get_market_summary() -> Dict[str, Any]:
        """Get overall market summary"""
        try:
            # Get major indices
            indices = ['^GSPC', '^DJI', '^IXIC', '^RUT']  # S&P 500, Dow Jones, NASDAQ, Russell 2000
            market_data = {}
            
            for index in indices:
                data = FinanceTools.get_real_time_quote(index)
                if 'error' not in data:
                    market_data[index] = {
                        'name': index.replace('^', ''),
                        'price': data.get('current_price'),
                        'change': data.get('change', 0.0),
                        'source': data.get('source', 'Unknown')
                    }
            
            # Get market movers
            movers = FinanceTools.get_market_movers("US")
            
            return {
                'indices': market_data,
                'market_movers': movers,
                'summary': f"Market data for {len(market_data)} indices",
                'timestamp': time.time()
            }
        except Exception as e:
            return {'error': f"Market summary error: {str(e)}"}

    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str = "USD") -> Dict[str, Any]:
        """Get exchange rate using Alpha Vantage"""
        try:
            if not settings.ALPHA_VANTAGE_API_KEY:
                # Fallback using yfinance for FX pairs
                symbol = f"{from_currency}{to_currency}=X"
                stock = yf.Ticker(symbol)
                info = stock.info
                
                return {
                    'from': from_currency,
                    'to': to_currency,
                    'rate': info.get('regularMarketPrice', 'N/A'),
                    'source': 'Yahoo Finance'
                }
            
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': from_currency,
                'to_currency': to_currency,
                'apikey': settings.ALPHA_VANTAGE_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'Realtime Currency Exchange Rate' in data:
                rate_data = data['Realtime Currency Exchange Rate']
                return {
                    'from': from_currency,
                    'to': to_currency,
                    'rate': float(rate_data['5. Exchange Rate']),
                    'timestamp': rate_data['6. Last Refreshed'],
                    'source': 'Alpha Vantage'
                }
            return {'error': 'Exchange rate not available'}
        except Exception as e:
            return {'error': f"Failed to fetch exchange rate: {str(e)}"}