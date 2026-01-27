import requests
import yfinance as yf
from typing import Optional, Dict, Any
from config.settings import settings

class FinanceTools:
    @staticmethod
    def get_stock_price(symbol: str) -> Dict[str, Any]:
        """Get current stock price using yfinance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            history = stock.history(period="1d")
            
            if history.empty:
                return {'error': f"No data found for symbol {symbol}"}
            
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
                'market_cap': info.get('marketCap')
            }
        except Exception as e:
            return {'error': f"Failed to fetch stock data: {str(e)}"}

    @staticmethod
    def get_crypto_price(crypto: str) -> Dict[str, Any]:
        """Get cryptocurrency price from CoinGecko"""
        try:
            # Simple fallback - in production use CoinGecko API
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
                '24h_volume': info.get('volume')
            }
        except Exception as e:
            return {'error': f"Failed to fetch crypto data: {str(e)}"}

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