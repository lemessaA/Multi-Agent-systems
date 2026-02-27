 A production-ready multi-agent system with intelligent routing, real-time data fetching, and a clean AI console UI.  
Built with **LangChain**, **LangGraph**, **FastAPI**, and **Streamlit**, with pluggable LLM providers (Gemini or Ollama).

### Overview

This project implements a smart router pattern over multiple specialized agents:

- **Weather agent**: current conditions and forecasts via OpenWeather.
- **News agent**: top headlines and topic search via NewsAPI (plus async helpers).
- **Finance agent**: stock, crypto, and FX data via external finance APIs.
- **Router agent (LangGraph)**: decides which agent should handle each request based on the natural-language query.

You can access the system via:

- A **FastAPI** backend (`/query`, `/query/{agent_type}`, `/agents`, `/examples`, `/health`).
- A **Streamlit AI console** (`streamlit_app.py`) with an “Auto (Smart Router)” mode and per-agent modes.

### Key Features

- **Smart auto-routing**  
  - Uses a structured `PromptTemplate` and LangGraph state machine to route queries to `weather`, `news`, or `finance` (or multiple where appropriate).
  - Returns a unified response with execution time and conversation ID.

- **Specialized agents with shared core**  
  - `BaseAgent` provides a consistent, domain-aware prompt that:
    - Explains each agent’s role (weather/news/finance).
    - Enforces a structured answer (short answer, key details, optional suggestions).
  - `WeatherAgent`, `NewsAgent`, and `FinanceAgent` plug in domain tools and custom parsing where needed.

- **Pluggable LLM provider**  
  - Centralized in `llm_factory.py`, which selects the underlying chat model:
    - **Gemini (default)** via `langchain-google-genai`.
    - **Ollama** fallback if installed and configured.

- **Modern API & UI**  
  - FastAPI app in `api/app.py` with CORS enabled and OpenAPI docs.
  - Streamlit UI in `streamlit_app.py` with:
    - Sidebar “AI Mode” selector (Auto / Weather / News / Finance).
    - Optional location context.
    - History-aware display of responses and intermediate details.

### Tech Stack

- **Backend**: FastAPI, LangChain, LangGraph, Pydantic v2.
- **LLM Providers**: Google Gemini (via `langchain-google-genai`), optional Ollama.
- **UI**: Streamlit.
- **Data Integrations**: OpenWeather, NewsAPI, finance APIs.

### Quick Start

#### 1. Requirements

- **Python**: 3.11+
- **Virtual environment** (recommended)
- **LLM provider**:
  - **Gemini** (default): `GEMINI_API_KEY` from Google AI Studio.
  - **Optional Ollama**: local Ollama installation and pulled model.

#### 2. Setup

```bash
git clone https://github.com/lemessaA/multi-agent-system.git
cd multi-agent-system

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env   # if .env.example is present
```

Then edit `.env` as needed.

### Environment Configuration

At minimum, configure your LLM provider and any external APIs you plan to use:

```env
# LLM provider selection
LLM_PROVIDER=gemini          # or 'ollama'

# Gemini settings (default provider)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-pro  # or another compatible Gemini model

# Ollama settings (only if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# External APIs (optional but recommended)
OPENWEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_newsapi_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_key
```

### Running the System

#### Backend (FastAPI)

From the project root with the venv activated:

```bash
python main.py
```

This starts FastAPI on `http://localhost:8000`.

You can also run directly with Uvicorn:

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

#### Streamlit AI Console

In a separate terminal (same venv):

```bash
streamlit run streamlit_app.py
```

This opens a browser UI where you can:

- Select **Auto (Smart Router)** or a specific agent.
- Enter natural language queries.
- Inspect responses and intermediate details.

### Verifying Installation

#### Health & Agents

```bash
curl http://localhost:8000/health
curl http://localhost:8000/agents
curl http://localhost:8000/examples
```

#### Auto-Routing Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the weather in Tokyo and show me the latest tech news?"
  }'
```

#### Direct Agent Queries

```bash
# Weather agent
curl -X POST "http://localhost:8000/query/weather" \
  -H "Content-Type: application/json" \
  -d '{"query": "3-day forecast for London"}'

# News agent
curl -X POST "http://localhost:8000/query/news" \
  -H "Content-Type: application/json" \
  -d '{"query": "Top business headlines in the US"}'

# Finance agent
curl -X POST "http://localhost:8000/query/finance" \
  -H "Content-Type: application/json" \
  -d '{"query": "Current price of AAPL and Bitcoin"}'
```

### Python Client Example

```python
import httpx
import asyncio

async def query_agent(query: str, agent_type: str | None = None):
    url = "http://localhost:8000/query"
    if agent_type:
        url = f"http://localhost:8000/query/{agent_type}"

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"query": query}, timeout=30.0)
        resp.raise_for_status()
        return resp.json()

async def main():
    result = await query_agent("Weather in Paris", "weather")
    print(result)

asyncio.run(main())
```

### Project Structure

```text
multi-agent-system/
├── agents/              # Agent implementations
│   ├── base_agent.py    # Shared agent core & prompt
│   ├── weather_agent.py
│   ├── news_agent.py
│   ├── finance_agent.py
│   ├── router_agent.py  # LangGraph router (production)
│   └── simple_router_agent.py  # Simplified LangGraph workflow
├── tools/               # External API integrations
│   ├── weather_tools.py
│   ├── news_tools.py
│   └── finance_tools.py
├── api/                 # FastAPI application
│   └── app.py           # API endpoints
├── config/              # Configuration
│   └── settings.py
├── schemas/             # Pydantic models
│   └── models.py
├── llm_factory.py       # LLM provider selection (Gemini/Ollama)
├── streamlit_app.py     # Streamlit AI console UI
├── main.py              # Entry point to start FastAPI server
└── tests/               # Test suite
```

### Performance & Limits

- Typical end-to-end latency: a few seconds per query (routing + agent + external APIs).
- When using Gemini, you are subject to Google AI **rate limits and quotas**:
  - If you see 429 `RESOURCE_EXHAUSTED` errors:
    - Upgrade your Gemini quota, or
    - Switch to `LLM_PROVIDER=ollama` for local, unlimited testing.

### Logging

- Logs can be written to `logs/app.log` (and stdout).
- Useful metrics to monitor:
  - Request and agent execution times.
  - External API errors and timeouts.
  - LLM usage and provider-side rate-limit responses.

