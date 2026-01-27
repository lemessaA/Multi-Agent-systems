from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List, Optional
import uvicorn
import logging

from agents.router_agent import RouterAgent
from schemas.models import AgentRequest, AgentResponse, MultiAgentResponse, AgentType
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global router agent instance
router_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global router_agent
    logger.info("Initializing Multi-Agent System...")
    router_agent = RouterAgent()
    logger.info("Multi-Agent System initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down Multi-Agent System...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Multi-Agent System API",
        "version": settings.APP_VERSION,
        "agents": ["weather", "news", "finance"],
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents_initialized": router_agent is not None
    }

@app.post("/query", response_model=MultiAgentResponse)
async def query_agent(request: AgentRequest):
    """Main endpoint for querying the multi-agent system"""
    try:
        if router_agent is None:
            raise HTTPException(status_code=503, detail="Agent system not initialized")
        
        logger.info(f"Processing query: {request.query}")
        
        # Process query through router agent
        result = await router_agent.process(request)
        
        return MultiAgentResponse(
            conversation_id=result["conversation_id"],
            responses=result["responses"],
            execution_time=result["execution_time"]
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/{agent_type}", response_model=AgentResponse)
async def query_specific_agent(
    agent_type: AgentType,
    request: AgentRequest,
    background_tasks: BackgroundTasks
):
    """Query a specific agent directly"""
    try:
        if router_agent is None:
            raise HTTPException(status_code=503, detail="Agent system not initialized")
        
        # Update request with specified agent type
        request.agent_type = agent_type
        
        logger.info(f"Processing {agent_type} query: {request.query}")
        
        # Process with specific agent
        result = await router_agent.process(request)
        
        if not result["responses"]:
            raise HTTPException(status_code=404, detail=f"No response from {agent_type} agent")
        
        return result["responses"][0]
        
    except Exception as e:
        logger.error(f"Error processing {agent_type} query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {
                "type": "weather",
                "description": "Weather forecasting and current conditions",
                "capabilities": ["current_weather", "forecast"]
            },
            {
                "type": "news",
                "description": "News headlines and article search",
                "capabilities": ["top_headlines", "news_search"]
            },
            {
                "type": "finance",
                "description": "Stock prices, crypto, and exchange rates",
                "capabilities": ["stock_prices", "crypto_prices", "exchange_rates"]
            }
        ]
    }

@app.get("/examples")
async def get_examples():
    """Get example queries for each agent"""
    return {
        "weather": [
            "What's the weather like in Tokyo?",
            "Give me a 3-day forecast for London",
            "How humid is it in New York right now?"
        ],
        "news": [
            "What are the top headlines in the US?",
            "Show me the latest technology news",
            "Search for news about artificial intelligence"
        ],
        "finance": [
            "What's the current price of Apple stock?",
            "How much is Bitcoin worth?",
            "What's the EUR to USD exchange rate?"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )