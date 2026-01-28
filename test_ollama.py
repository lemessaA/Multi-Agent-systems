#!/usr/bin/env python3
"""
Test script to verify Ollama integration
"""

from langchain_ollama import ChatOllama
from config.settings import settings

def test_ollama_connection():
    """Test Ollama connection and model availability"""
    print(f"🔍 Testing Ollama connection...")
    print(f"   Base URL: {settings.OLLAMA_BASE_URL}")
    print(f"   Model: {settings.OLLAMA_MODEL}")
    
    try:
        # Initialize Ollama
        llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )
        
        # Simple test
        print("   Sending test query...")
        response = llm.invoke('Hello, how are you?')
        
        print("✅ Ollama connection successful!")
        print(f"   Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("\n📋 Troubleshooting:")
        print("   1. Make sure Ollama is installed: https://ollama.ai/download")
        print("   2. Start Ollama service: ollama serve")
        print(f"   3. Pull the model: ollama pull {settings.OLLAMA_MODEL}")
        print("   4. Check if Ollama is running: ollama list")
        return False

if __name__ == "__main__":
    test_ollama_connection()
