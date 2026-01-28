# Ollama Setup Guide

This guide will help you set up Ollama to run your multi-agent system locally.

## Prerequisites

- Python 3.11+
- Ollama installed locally

## Installation Steps

### 1. Install Ollama

Visit [https://ollama.ai/download](https://ollama.ai/download) and install Ollama for your operating system.

### 2. Start Ollama Service

```bash
# Start the Ollama service
ollama serve
```

This will start the Ollama server on `http://localhost:11434`.

### 3. Pull the Required Model

```bash
# Pull the Llama 3.1 8B model
ollama pull llama3.1:8b

# Verify the model is installed
ollama list
```

### 4. Configure Environment

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Optional: External API keys for enhanced functionality
OPENWEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_newsapi_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_key
```

### 5. Test the Connection

```bash
# Test Ollama integration
python test_ollama.py
```

You should see:
```
✅ Ollama connection successful!
   Response: Hello! I'm doing well, thank you for asking...
```

### 6. Run the Multi-Agent System

```bash
# Start the LangGraph development server
langgraph dev

# Or run the FastAPI server directly
python main.py
```

## Available Models

You can use different models by changing the `OLLAMA_MODEL` in your `.env` file:

- `llama3.1:8b` - Default (8B parameters)
- `llama3.1:70b` - Larger model (70B parameters)
- `qwen2.5:7b` - Alternative model
- `codellama:7b` - Code-focused model

## Troubleshooting

### Connection Refused Error

If you get "Connection refused" error:

1. **Check if Ollama is running:**
   ```bash
   ollama list
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Check if the model is installed:**
   ```bash
   ollama pull llama3.1:8b
   ```

### Model Not Found Error

If you get "model not found" error:

```bash
# Pull the required model
ollama pull llama3.1:8b
```

### Performance Issues

For better performance:

1. **Use a smaller model:**
   ```env
   OLLAMA_MODEL=llama3.1:8b
   ```

2. **Increase Ollama memory allocation** (if you have sufficient RAM)

3. **Use GPU acceleration** (if supported by your hardware)

## Configuration Options

### Custom Ollama Server

If Ollama is running on a different server:

```env
OLLAMA_BASE_URL=http://your-server:11434
OLLAMA_MODEL=llama3.1:8b
```

### Model Parameters

You can adjust model parameters in the agent files:

```python
# In agents/simple_router_agent.py
self.llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0.1,  # Lower for more deterministic responses
    num_ctx=4096,     # Context window size
)
```

## Next Steps

Once Ollama is set up and running:

1. Test the multi-agent system with sample queries
2. Open LangSmith Studio: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`
3. Explore the API documentation: `http://127.0.0.1:2024/docs`

## Benefits of Using Ollama

- **Local Processing**: No API keys required for the LLM
- **Privacy**: All processing happens locally
- **Cost**: Free to use (no per-token costs)
- **Customization**: Can use custom fine-tuned models
- **Offline**: Works without internet connection (for LLM processing)
