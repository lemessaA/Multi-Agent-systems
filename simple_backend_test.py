#!/usr/bin/env python3
"""
Simple backend test without middleware issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn
from agents.simple_router_agent import SimpleRouterAgent
from schemas.models import AgentRequest
from config.settings import settings

# Create app without middleware
app = FastAPI(title="Multi-Agent Test", version="1.0.0")

# Global agent
router_agent = None

@app.on_event("startup")
async def startup_event():
    global router_agent
    print("🚀 Initializing Multi-Agent System...")
    try:
        router_agent = SimpleRouterAgent()
        print("✅ Multi-Agent System initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")

@app.get("/")
async def root():
    return {
        "message": "Multi-Agent System API",
        "version": "1.0.0",
        "status": "running",
        "provider": settings.LLM_PROVIDER
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "agent_initialized": router_agent is not None,
        "provider": settings.LLM_PROVIDER
    }

@app.post("/query")
async def query_agent(request: AgentRequest):
    """Test query endpoint"""
    try:
        if router_agent is None:
            return {"error": "Agent system not initialized"}
        
        print(f"📝 Processing: {request.query}")
        
        # Process query
        result = await router_agent.process(request)
        
        return {
            "success": True,
            "result": result,
            "provider": settings.LLM_PROVIDER
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    print("🚀 Starting Simple Backend Test...")
    print("🌐 http://localhost:8002")
    print("📚 http://localhost:8002/docs")
    print(f"🤖 Provider: {settings.LLM_PROVIDER}")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8002,
        log_level="info"
    )
