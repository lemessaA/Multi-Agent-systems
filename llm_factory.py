from typing import Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from config.settings import settings


Provider = Literal["gemini", "ollama"]


def get_chat_llm(provider: Provider | None = None, temperature: float = 0.3):
    """Return a chat LLM instance based on configuration.

    Default provider is Ollama for local processing, with Gemini as fallback
    """
    provider = (provider or settings.LLM_PROVIDER).lower()

    if provider == "ollama":
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=temperature,
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY,
            temperature=temperature,
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
