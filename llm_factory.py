from typing import Literal

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings


Provider = Literal["gemini"]


def get_chat_llm(provider: Provider | None = None, temperature: float = 0.3):
    """Return a chat LLM instance based on configuration.

    Default provider is Gemini so we can easily test realtime functionality
    just by setting GEMINI_API_KEY and (optionally) GEMINI_MODEL.
    """
    provider = (provider or settings.LLM_PROVIDER).lower()

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY,
            temperature=temperature,
        )
