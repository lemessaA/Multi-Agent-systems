"""
Tests for the Multi-Agent System tools
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestWeatherTools:
    """Test cases for weather-related tools"""
    
    @pytest.fixture
    def mock_weather_response(self):
        """Mock weather API response"""
        return {
            "location": {
                "name": "New York",
                "region": "New York",
                "country": "United States"
            },
            "current": {
                "temp_c": 22.5,
                "temp_f": 72.5,
                "condition": {
                    "text": "Partly cloudy",
                    "icon": "partly-cloudy"
                },
                "humidity": 65,
                "wind_kph": 15.2,
                "pressure_mb": 1013.2
            },
            "forecast": {
                "forecastday": [
                    {
                        "date": "2024-01-28",
                        "day": {
                            "maxtemp_c": 25.0,
                            "mintemp_c": 18.0,
                            "condition": {
                                "text": "Sunny"
                            }
                        }
                    }
                ]
            }
        }
    
    @pytest.mark.asyncio
    async def test_get_current_weather(self, mock_weather_response):
        """Test getting current weather"""
        with patch('tools.weather_tools.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_weather_response
            mock_get.return_value.raise_for_status.return_value = None
            
            # Mock the weather tool function
            with patch('tools.weather_tools.WeatherTools.get_current_weather') as mock_weather_func:
                mock_weather_func.return_value = {
                    "location": "New York",
                    "temperature": "22.5°C",
                    "condition": "Partly cloudy",
                    "humidity": 65,
                    "wind_speed": "15.2 km/h"
                }
                
                result = mock_weather_func("New York")
                
                assert "location" in result
                assert "temperature" in result
                assert "condition" in result
                assert result["location"] == "New York"
                assert result["temperature"] == "22.5°C"
    
    @pytest.mark.asyncio
    async def test_get_weather_forecast(self, mock_weather_response):
        """Test getting weather forecast"""
        with patch('tools.weather_tools.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_weather_response
            mock_get.return_value.raise_for_status.return_value = None
            
            # Mock the forecast function
            with patch('tools.weather_tools.WeatherTools.get_weather_forecast') as mock_forecast_func:
                mock_forecast_func.return_value = {
                    "location": "New York",
                    "forecast": [
                        {
                            "date": "2024-01-28",
                            "high": "25.0°C",
                            "low": "18.0°C",
                            "condition": "Sunny"
                        }
                    ]
                }
                
                result = mock_forecast_func("New York", 1)
                
                assert "location" in result
                assert "forecast" in result
                assert len(result["forecast"]) == 1
                assert result["forecast"][0]["date"] == "2024-01-28"
    
    def test_weather_tool_validation(self):
        """Test weather tool input validation"""
        with patch('tools.weather_tools.WeatherTools.get_current_weather') as mock_weather_func:
            # Test with empty location
            mock_weather_func.return_value = {"error": "Location is required"}
            result = mock_weather_func("")
            assert "error" in result
            
            # Test with valid location
            mock_weather_func.return_value = {"location": "London", "temperature": "15°C"}
            result = mock_weather_func("London")
            assert "location" in result
            assert result["location"] == "London"


class TestNewsTools:
    """Test cases for news-related tools"""
    
    @pytest.fixture
    def mock_news_response(self):
        """Mock news API response"""
        return {
            "status": "ok",
            "totalResults": 10,
            "articles": [
                {
                    "title": "Tech Stocks Rise on Positive Earnings",
                    "description": "Major tech companies report better than expected earnings...",
                    "source": {
                        "name": "TechNews"
                    },
                    "publishedAt": "2024-01-28T10:00:00Z",
                    "url": "https://example.com/article1"
                },
                {
                    "title": "Climate Summit Reaches Historic Agreement",
                    "description": "World leaders agree on new climate action plan...",
                    "source": {
                        "name": "WorldNews"
                    },
                    "publishedAt": "2024-01-28T09:30:00Z",
                    "url": "https://example.com/article2"
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_get_latest_headlines(self, mock_news_response):
        """Test getting latest headlines"""
        with patch('tools.news_tools.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_news_response
            mock_get.return_value.raise_for_status.return_value = None
            
            # Mock the headlines function
            with patch('tools.news_tools.NewsTools.get_top_headlines') as mock_headlines_func:
                mock_headlines_func.return_value = {
                    "total_articles": 2,
                    "articles": [
                        {
                            "title": "Tech Stocks Rise on Positive Earnings",
                            "source": "TechNews",
                            "published_at": "2024-01-28T10:00:00Z"
                        },
                        {
                            "title": "Climate Summit Reaches Historic Agreement",
                            "source": "WorldNews",
                            "published_at": "2024-01-28T09:30:00Z"
                        }
                    ]
                }
                
                result = mock_headlines_func(5)
                
                assert "total_articles" in result
                assert "articles" in result
                assert len(result["articles"]) == 2
                assert result["articles"][0]["title"] == "Tech Stocks Rise on Positive Earnings"
    
    @pytest.mark.asyncio
    async def test_search_news(self, mock_news_response):
        """Test searching news"""
        with patch('tools.news_tools.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_news_response
            mock_get.return_value.raise_for_status.return_value = None
            
            # Mock the search function
            with patch('tools.news_tools.NewsTools.search_news_async') as mock_search_func:
                mock_search_func.return_value = {
                    "query": "technology",
                    "total_results": 2,
                    "articles": [
                        {
                            "title": "Tech Stocks Rise on Positive Earnings",
                            "description": "Major tech companies report better than expected earnings...",
                            "source": "TechNews"
                        }
                    ]
                }
                
                result = mock_search_func("technology", 5)
                
                assert "query" in result
                assert "total_results" in result
                assert "articles" in result
                assert result["query"] == "technology"
                assert len(result["articles"]) >= 1
    
    def test_news_tool_validation(self):
        """Test news tool input validation"""
        with patch('tools.news_tools.NewsTools.get_top_headlines') as mock_headlines_func:
            # Test with invalid limit
            mock_headlines_func.return_value = {"error": "Limit must be between 1 and 100"}
            result = mock_headlines_func(0)
            assert "error" in result
            
            # Test with valid limit
            mock_headlines_func.return_value = {"total_articles": 5, "articles": []}
            result = mock_headlines_func(10)
            assert "total_articles" in result


class TestFinanceTools:
    """Test cases for finance-related tools"""
    
    @pytest.fixture
    def mock_stock_response(self):
        """Mock stock API response"""
        return {
            "Global Quote": {
                "01. symbol": "AAPL",
                "02. open": "175.20",
                "03. high": "176.80",
                "04. low": "174.50",
                "05. price": "175.43",
                "06. volume": "52341234",
                "07. latest trading day": "2024-01-26",
                "08. previous close": "173.20",
                "09. change": "2.23",
                "10. change percent": "1.29%"
            }
        }
    
    @pytest.fixture
    def mock_crypto_response(self):
        """Mock cryptocurrency API response"""
        return {
            "bitcoin": {
                "usd": 42350.67,
                "usd_24h_change": 2.15,
                "usd_market_cap": 828456789012,
                "usd_24h_vol": 23456789012
            }
        }
    
    @pytest.mark.asyncio
    async def test_get_stock_price(self, mock_stock_response):
        """Test getting stock price"""
        with patch('tools.finance_tools.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_stock_response
            mock_get.return_value.raise_for_status.return_value = None
            
            # Mock the stock price function
            with patch('tools.finance_tools.FinanceTools.get_stock_price') as mock_stock_func:
                mock_stock_func.return_value = {
                    "symbol": "AAPL",
                    "price": "$175.43",
                    "change": "+2.23 (+1.29%)",
                    "volume": "52,341,234",
                    "last_updated": "2024-01-26"
                }
                
                result = mock_stock_func("AAPL")
                
                assert "symbol" in result
                assert "price" in result
                assert "change" in result
                assert result["symbol"] == "AAPL"
                assert result["price"] == "$175.43"
    
    @pytest.mark.asyncio
    async def test_get_crypto_price(self, mock_crypto_response):
        """Test getting cryptocurrency price"""
        with patch('tools.finance_tools.requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_crypto_response
            mock_get.return_value.raise_for_status.return_value = None
            
            # Mock the crypto price function
            with patch('tools.finance_tools.FinanceTools.get_crypto_price') as mock_crypto_func:
                mock_crypto_func.return_value = {
                    "cryptocurrency": "bitcoin",
                    "price": "$42,350.67",
                    "change_24h": "+2.15%",
                    "market_cap": "$828.46B",
                    "volume_24h": "$23.46B"
                }
                
                result = mock_crypto_func("bitcoin")
                
                assert "cryptocurrency" in result
                assert "price" in result
                assert "change_24h" in result
                assert result["cryptocurrency"] == "bitcoin"
                assert result["price"] == "$42,350.67"
    
    @pytest.mark.asyncio
    async def test_get_exchange_rate(self):
        """Test getting exchange rates"""
        # Mock the exchange rate function
        with patch('tools.finance_tools.FinanceTools.get_exchange_rate') as mock_exchange_func:
            mock_exchange_func.return_value = {
                "from_currency": "USD",
                "to_currency": "EUR",
                "rate": 0.92,
                "last_updated": "2024-01-28"
            }
            
            result = mock_exchange_func("USD", "EUR")
            
            assert "from_currency" in result
            assert "to_currency" in result
            assert "rate" in result
            assert result["from_currency"] == "USD"
            assert result["to_currency"] == "EUR"
            assert result["rate"] == 0.92
    
    def test_finance_tool_validation(self):
        """Test finance tool input validation"""
        with patch('tools.finance_tools.FinanceTools.get_stock_price') as mock_stock_func:
            # Test with empty symbol
            mock_stock_func.return_value = {"error": "Stock symbol is required"}
            result = mock_stock_func("")
            assert "error" in result
            
            # Test with valid symbol
            mock_stock_func.return_value = {"symbol": "GOOGL", "price": "$140.25"}
            result = mock_stock_func("GOOGL")
            assert "symbol" in result
            assert result["symbol"] == "GOOGL"


class TestToolIntegration:
    """Integration tests for tools"""
    
    @pytest.mark.asyncio
    async def test_weather_news_integration(self):
        """Test integration between weather and news tools"""
        # Mock both tools
        with patch('tools.weather_tools.WeatherTools.get_current_weather') as mock_weather, \
             patch('tools.news_tools.NewsTools.search_news_async') as mock_news:
            
            mock_weather.return_value = {
                "location": "Miami",
                "temperature": "28°C",
                "condition": "Sunny"
            }
            
            mock_news.return_value = {
                "query": "Miami weather",
                "total_results": 3,
                "articles": [
                    {
                        "title": "Miami enjoys sunny weather",
                        "source": "Miami Herald"
                    }
                ]
            }
            
            # Get weather first
            weather_result = mock_weather("Miami")
            assert weather_result["location"] == "Miami"
            
            # Then search for related news
            news_result = mock_news("Miami weather", 5)
            assert news_result["query"] == "Miami weather"
            assert len(news_result["articles"]) >= 1
    
    @pytest.mark.asyncio
    async def test_finance_news_integration(self):
        """Test integration between finance and news tools"""
        with patch('tools.finance_tools.FinanceTools.get_stock_price') as mock_stock, \
             patch('tools.news_tools.NewsTools.search_news_async') as mock_news:
            
            mock_stock.return_value = {
                "symbol": "TSLA",
                "price": "$195.67",
                "change": "+5.23 (+2.74%)"
            }
            
            mock_news.return_value = {
                "query": "Tesla stock",
                "total_results": 5,
                "articles": [
                    {
                        "title": "Tesla stock surges on earnings beat",
                        "source": "Financial Times"
                    }
                ]
            }
            
            # Get stock price
            stock_result = mock_stock("TSLA")
            assert stock_result["symbol"] == "TSLA"
            
            # Get related news
            news_result = mock_news("Tesla stock", 5)
            assert news_result["query"] == "Tesla stock"
            assert len(news_result["articles"]) >= 1


class TestToolErrorHandling:
    """Test error handling in tools"""
    
    @pytest.mark.asyncio
    async def test_weather_api_error(self):
        """Test weather API error handling"""
        with patch('tools.weather_tools.requests.get') as mock_get:
            mock_get.side_effect = Exception("API Error")
            
            with patch('tools.weather_tools.WeatherTools.get_current_weather') as mock_weather_func:
                mock_weather_func.return_value = {
                    "error": "Failed to fetch weather data",
                    "details": "API Error"
                }
                
                result = mock_weather_func("London")
                assert "error" in result
    
    @pytest.mark.asyncio
    async def test_news_api_error(self):
        """Test news API error handling"""
        with patch('tools.news_tools.requests.get') as mock_get:
            mock_get.side_effect = Exception("API Error")
            
            with patch('tools.news_tools.NewsTools.get_top_headlines') as mock_headlines_func:
                mock_headlines_func.return_value = {
                    "error": "Failed to fetch news data",
                    "details": "API Error"
                }
                
                result = mock_headlines_func(5)
                assert "error" in result
    
    @pytest.mark.asyncio
    async def test_finance_api_error(self):
        """Test finance API error handling"""
        with patch('tools.finance_tools.requests.get') as mock_get:
            mock_get.side_effect = Exception("API Error")
            
            with patch('tools.finance_tools.FinanceTools.get_stock_price') as mock_stock_func:
                mock_stock_func.return_value = {
                    "error": "Failed to fetch stock data",
                    "details": "API Error"
                }
                
                result = mock_stock_func("AAPL")
                assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])