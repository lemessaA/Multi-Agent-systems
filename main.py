#!/usr/bin/env python3
"""
Multi-Agent System with Router Pattern
Run with: python main.py
"""

import uvicorn
import sys
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def check_environment():
    """Check required environment variables"""
    # For Ollama, no API key is required
    print("✅ Using Ollama - no API key required for LLM")
    
    # Check optional API keys for enhanced functionality
    optional_vars = ['OPENWEATHER_API_KEY', 'NEWS_API_KEY', 'ALPHA_VANTAGE_API_KEY']
    missing_optional = []
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_optional:
        print(f"⚠️  Optional API keys not set: {', '.join(missing_optional)}")
        print("For enhanced functionality, add these to your .env file:")
        print("OPENWEATHER_API_KEY=your_openweather_api_key_here")
        print("NEWS_API_KEY=your_newsapi_key_here")
        print("ALPHA_VANTAGE_API_KEY=your_alphavantage_key_here")
        print("\nNote: System will work with Ollama without these keys")
    
    print("✅ Environment check passed")
    return True

def main():
    """Main entry point"""
    print("🚀 Starting Multi-Agent System...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Start FastAPI server
    port = 8001 if os.getenv("PORT") else 8000
    print(f"🌐 Starting API server on http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print("\nExample queries:")
    print("  • Weather: 'What's the temperature in Paris?'")
    print("  • News: 'Show me top headlines'")
    print("  • Finance: 'What is AAPL stock price?'")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        uvicorn.run(
            "api.app:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Multi-Agent System...")
        sys.exit(0)

if __name__ == "__main__":
    main()