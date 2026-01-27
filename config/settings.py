import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # API Keys for external services
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    # FastAPI Settings
    APP_NAME = "Multi-Agent System"
    APP_VERSION = "1.0.0"
    
    # Agent Settings
    MAX_ITERATIONS = 5

settings = Settings()