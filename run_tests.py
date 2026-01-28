#!/usr/bin/env python3
"""
Test runner for the Multi-Agent System
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return None
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return None

def run_unit_tests():
    """Run unit tests only"""
    print("🧪 Running Unit Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/ -v -m 'unit or not integration' --tb=short"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ Unit tests passed!")
        return True
    else:
        print("❌ Unit tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def run_integration_tests():
    """Run integration tests only"""
    print("🔗 Running Integration Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/ -v -m 'integration' --tb=short"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ Integration tests passed!")
        return True
    else:
        print("❌ Integration tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def run_api_tests():
    """Run API tests only"""
    print("🌐 Running API Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/test_api.py -v --tb=short"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ API tests passed!")
        return True
    else:
        print("❌ API tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def run_agent_tests():
    """Run agent tests only"""
    print("🤖 Running Agent Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/test_agents.py -v --tb=short"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ Agent tests passed!")
        return True
    else:
        print("❌ Agent tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def run_tool_tests():
    """Run tool tests only"""
    print("🔧 Running Tool Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/test_tools.py -v --tb=short"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ Tool tests passed!")
        return True
    else:
        print("❌ Tool tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Running All Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/ -v --tb=short --cov=agents --cov=api --cov=tools --cov-report=term-missing --cov-report=html"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def run_quick_tests():
    """Run quick tests (exclude slow tests)"""
    print("⚡ Running Quick Tests...")
    print("=" * 50)
    
    cmd = ".venv/bin/python -m pytest tests/ -v -m 'not slow' --tb=short"
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print("✅ Quick tests passed!")
        return True
    else:
        print("❌ Quick tests failed!")
        if result:
            print(result.stdout)
            print(result.stderr)
        return False

def check_dependencies():
    """Check if test dependencies are installed"""
    print("🔍 Checking test dependencies...")
    
    required_packages = [
        "pytest",
        "pytest-asyncio", 
        "pytest-cov",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        cmd = f".venv/bin/python -c 'import {package}'"
        result = run_command(cmd)
        
        if not result or result.returncode != 0:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        install_cmd = f".venv/bin/pip install {' '.join(missing_packages)}"
        result = run_command(install_cmd)
        
        if result and result.returncode == 0:
            print("✅ Dependencies installed!")
            return True
        else:
            print("❌ Failed to install dependencies!")
            return False
    else:
        print("✅ All dependencies are installed!")
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test runner for Multi-Agent System")
    parser.add_argument(
        "test_type",
        choices=["all", "unit", "integration", "api", "agent", "tool", "quick"],
        help="Type of tests to run",
        default="all",
        nargs="?"
    )
    parser.add_argument(
        "--no-deps",
        action="store_true",
        help="Skip dependency check"
    )
    
    args = parser.parse_args()
    
    print("🧪 Multi-Agent System Test Runner")
    print("=" * 50)
    
    # Check dependencies
    if not args.no_deps:
        if not check_dependencies():
            print("❌ Dependency check failed!")
            sys.exit(1)
    
    # Run tests based on type
    success = False
    
    if args.test_type == "all":
        success = run_all_tests()
    elif args.test_type == "unit":
        success = run_unit_tests()
    elif args.test_type == "integration":
        success = run_integration_tests()
    elif args.test_type == "api":
        success = run_api_tests()
    elif args.test_type == "agent":
        success = run_agent_tests()
    elif args.test_type == "tool":
        success = run_tool_tests()
    elif args.test_type == "quick":
        success = run_quick_tests()
    
    # Exit with appropriate code
    if success:
        print("\n🎉 Tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
