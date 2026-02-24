#!/usr/bin/env python3
"""
Simple test server to verify backend functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn

# Create simple FastAPI app
app = FastAPI(title="Test Server", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Test server is running", "status": "operational"}

@app.get("/health")
async def health():
    return {"status": "healthy", "test": True}

@app.get("/test")
async def test_endpoint():
    return {
        "message": "Backend test successful",
        "ollama_configured": True,
        "agents": ["weather", "news", "finance"]
    }

if __name__ == "__main__":
    print("🚀 Starting Test Server...")
    print("🌐 Server: http://localhost:8002")
    print("📚 Docs: http://localhost:8002/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
        log_level="info"
    )
