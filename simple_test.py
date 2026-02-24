#!/usr/bin/env python3
"""
Minimal backend test without middleware issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
import uvicorn

# Create minimal FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Backend is working", "Ollama": "Configured"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "backend": "operational"}

@app.get("/test/ollama")
def test_ollama():
    try:
        from config.settings import settings
        return {
            "ollama_configured": True,
            "base_url": settings.OLLAMA_BASE_URL,
            "model": settings.OLLAMA_MODEL
        }
    except Exception as e:
        return {"error": str(e), "ollama_configured": False}

if __name__ == "__main__":
    print("🚀 Starting Minimal Backend Test...")
    print("🌐 http://localhost:8003")
    
    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="info")
