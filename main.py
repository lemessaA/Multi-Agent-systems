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
    required_vars = ['OPENAI_API_KEY']
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the following variables:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("OPENWEATHER_API_KEY=your_openweather_api_key_here (optional)")
        print("NEWS_API_KEY=your_newsapi_key_here (optional)")
        print("ALPHA_VANTAGE_API_KEY=your_alphavantage_key_here (optional)")
        return False
    
    print("✅ Environment variables check passed")
    return True

def main():
    """Main entry point"""
    print("🚀 Starting Multi-Agent System...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Start FastAPI server
    print("🌐 Starting API server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\nExample queries:")
    print("  • Weather: 'What's the temperature in Paris?'")
    print("  • News: 'Show me top headlines'")
    print("  • Finance: 'What is AAPL stock price?'")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        uvicorn.run(
            "api.app:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down Multi-Agent System...")
        sys.exit(0)

if __name__ == "__main__":
    main()