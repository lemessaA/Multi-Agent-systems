from typing import Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

from config.settings import settings


Provider = Literal["gemini", "ollama", "groq"]


def get_chat_llm(provider: Provider | None = None, temperature: float = 0.3):
    """Return a chat LLM instance based on configuration.

    Supports Groq for high-performance, Ollama for local, and Gemini as fallback
    """
    provider = (provider or settings.LLM_PROVIDER).lower()

    if provider == "groq":
        return ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=temperature,
        )
    elif provider == "ollama":
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
