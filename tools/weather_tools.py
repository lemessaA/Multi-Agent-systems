import requests
from typing import Optional, Dict, Any
from config.settings import settings

class WeatherTools:
    @staticmethod  
    def get_current_weather(location: str) -> Dict[str, Any]:
        """Get current weather for a location using OpenWeather API"""
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'location': data['name'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all']
            }
        except Exception as e:
            return {'error': f"Failed to fetch weather: {str(e)}"}

    @staticmethod
    def get_weather_forecast(location: str, days: int = 5) -> Dict[str, Any]:
        """Get weather forecast for multiple days"""
        try:
            base_url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': location,
                'appid': settings.OPENWEATHER_API_KEY,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['list'][:days]:
                forecasts.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'weather': item['weather'][0]['description'],
                    'humidity': item['main']['humidity']
                })
            
            return {
                'location': data['city']['name'],
                'forecasts': forecasts
            }
        except Exception as e:
            return {'error': f"Failed to fetch forecast: {str(e)}"}