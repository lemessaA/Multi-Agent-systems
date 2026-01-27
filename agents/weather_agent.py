from agents.base_agent import BaseAgent
from tools.weather_tools import WeatherTools
from langchain.agents import Tool
from schemas.models import AgentType
from typing import List

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.WEATHER)

    def _initialize_tools(self) -> List[Tool]:
        return [
            Tool(
                name="GetCurrentWeather",
                func=WeatherTools.get_current_weather,
                description="Get current weather for a location. Input should be a city name (e.g., 'London', 'New York')."
            ),
            Tool(
                name="GetWeatherForecast",
                func=WeatherTools.get_weather_forecast,
                description="Get weather forecast for multiple days. Input should be 'city_name, days' (e.g., 'Tokyo, 3')."
            )
        ]
    
    def _parse_response(self, raw_response: str) -> str:
        """Specialized parsing for weather responses"""
        if "Error" in raw_response or "Failed" in raw_response:
            return f"Sorry, I couldn't fetch weather data. Please try again or check the location name."
        return raw_response