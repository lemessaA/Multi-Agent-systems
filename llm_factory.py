from typing import Literal

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings


Provider = Literal["gemini", "ollama"]


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

    # Fallback to Ollama (optional; requires langchain-ollama to be installed)
    try:
        from langchain_ollama import ChatOllama  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "Ollama provider requested but 'langchain-ollama' is not installed. "
            "Either install langchain-ollama or set LLM_PROVIDER=gemini."
        ) from exc

    return ChatOllama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=temperature,
    )

