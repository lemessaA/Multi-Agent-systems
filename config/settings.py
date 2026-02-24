import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LLM provider / model
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # 'gemini' or 'ollama'

    # Gemini Settings
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    
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