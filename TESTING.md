# Testing Guide for Multi-Agent System

This guide covers how to run and write tests for the Multi-Agent System.

## 📋 Table of Contents

- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Writing Tests](#writing-tests)
- [Test Examples](#test-examples)
- [Continuous Integration](#continuous-integration)

## 🏗️ Test Structure

```
tests/
├── __init__.py              # Test configuration and utilities
├── test_agents.py           # Agent-specific tests
├── test_api.py              # API endpoint tests
├── test_tools.py            # Tool/function tests
├── test_data/               # Test data files
└── mock_responses/          # Mock API responses

examples/
├── __init__.py              # Example exports
├── client_example.py        # API client example
└── example_queries.py       # Sample queries for testing
```

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py unit
python run_tests.py integration
python run_tests.py api
python run_tests.py agent
python run_tests.py tool
python run_tests.py quick
```

### Using pytest directly

```bash
# Run all tests with coverage
.venv/bin/python -m pytest tests/ -v --cov=agents --cov=api --cov=tools

# Run specific test file
.venv/bin/python -m pytest tests/test_agents.py -v

# Run with markers
.venv/bin/python -m pytest tests/ -v -m "unit"
.venv/bin/python -m pytest tests/ -v -m "integration"
.venv/bin/python -m pytest tests/ -v -m "api"
```

### Test Options

| Option | Description |
|--------|-------------|
| `all` | Run all tests (default) |
| `unit` | Run unit tests only |
| `integration` | Run integration tests only |
| `api` | Run API tests only |
| `agent` | Run agent tests only |
| `tool` | Run tool tests only |
| `quick` | Run quick tests (exclude slow ones) |

## 📝 Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual functions and methods
- Mock external dependencies
- Fast and isolated
- Example: Testing router logic

### Integration Tests (`@pytest.mark.integration`)
- Test multiple components together
- Test real API interactions
- Slower but more realistic
- Example: Full agent workflow

### API Tests (`@pytest.mark.api`)
- Test HTTP endpoints
- Test request/response handling
- Test error scenarios
- Example: POST /query endpoint

### Agent Tests (`@pytest.mark.agent`)
- Test agent behavior
- Test routing logic
- Test response generation
- Example: Weather agent routing

### Tool Tests (`@pytest.mark.tool`)
- Test individual tools
- Test API integrations
- Test data parsing
- Example: Weather API tool

## ✍️ Writing Tests

### Basic Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from tests import TestUtils

class TestMyComponent:
    @pytest.fixture
    def sample_data(self):
        return TestUtils.create_mock_weather_data()
    
    @pytest.mark.unit
    def test_basic_functionality(self, sample_data):
        # Arrange
        expected = "expected_result"
        
        # Act
        result = function_to_test(sample_data)
        
        # Assert
        assert result == expected
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        # Test async functions
        result = await async_function()
        assert result is not None
```

### Mocking External APIs

```python
@pytest.mark.asyncio
async def test_weather_api_call(self):
    with patch('tools.weather.requests.get') as mock_get:
        mock_get.return_value.json.return_value = TestUtils.create_mock_weather_data()
        mock_get.return_value.raise_for_status.return_value = None
        
        result = await get_weather("New York")
        
        assert "location" in result
        assert result["location"]["name"] == "New York"
```

### Testing Error Handling

```python
def test_error_handling(self):
    with patch('module.function', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            function_that_fails()
        
        assert "API Error" in str(exc_info.value)
```

## 📚 Test Examples

### Running Example Client

```bash
# Run the example client
.venv/bin/python examples/client_example.py

# Run example queries
.venv/bin/python examples/example_queries.py
```

### Using the MultiAgentClient

```python
from examples.client_example import MultiAgentClient
import asyncio

async def test_client():
    client = MultiAgentClient()
    
    # Single query
    result = await client.query_agent("What's the weather like in London?")
    print(result)
    
    # Batch test
    results = await client.test_all_categories()
    client.print_results(results)

# Run the test
asyncio.run(test_client())
```

## 🔄 Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m venv .venv
        . .venv/bin/activate
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        . .venv/bin/activate
        python run_tests.py all
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: python run_tests.py quick
        language: system
        pass_filenames: false
        always_run: true
```

## 🛠️ Test Utilities

### TestUtils Class

```python
from tests import TestUtils

# Create mock data
weather_data = TestUtils.create_mock_weather_data("London")
news_data = TestUtils.create_mock_news_data()
finance_data = TestUtils.create_mock_finance_data("AAPL")
agent_response = TestUtils.create_mock_agent_response("weather", "Sunny")
```

### Test Configuration

```python
from tests import TEST_CONFIG

# Access test configuration
timeout = TEST_CONFIG["timeout"]
retry_attempts = TEST_CONFIG["retry_attempts"]
test_data_dir = TEST_CONFIG["test_data_dir"]
```

## 📊 Coverage Reports

### Generate Coverage Report

```bash
# Generate HTML coverage report
.venv/bin/python -m pytest tests/ --cov=agents --cov=api --cov=tools --cov-report=html

# View the report
open htmlcov/index.html
```

### Coverage Goals

- **Target**: 80%+ coverage
- **Critical paths**: 90%+ coverage
- **Error handling**: 100% coverage

## 🐛 Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with pdb debugger
.venv/bin/python -m pytest tests/ -v --pdb

# Run specific test with debug
.venv/bin/python -m pytest tests/test_agents.py::TestSimpleRouterAgent::test_route_query_weather -v --pdb
```

### Verbose Output

```bash
# Very verbose output
.venv/bin/python -m pytest tests/ -v -s --tb=long

# Show local variables on failure
.venv/bin/python -m pytest tests/ -v --tb=long --showlocals
```

## 📋 Best Practices

### 1. Test Naming
- Use descriptive test names
- Follow `test_what_should_happen_when` pattern
- Group related tests in classes

### 2. Test Structure
- Use Arrange-Act-Assert pattern
- Keep tests simple and focused
- One assertion per test when possible

### 3. Mocking
- Mock external dependencies
- Use realistic mock data
- Don't mock the system under test

### 4. Async Testing
- Use `@pytest.mark.asyncio`
- Test both success and error cases
- Handle timeouts appropriately

### 5. Test Data
- Use fixtures for reusable data
- Keep test data minimal
- Use edge cases in tests

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the project root
   cd /path/to/multi-agent-system
   source .venv/bin/activate
   ```

2. **Missing Dependencies**
   ```bash
   # Install test dependencies
   .venv/bin/pip install pytest pytest-asyncio pytest-cov requests
   ```

3. **Environment Variables**
   ```bash
   # Set test environment variables
   export GROQ_API_KEY=test_key
   export OPENWEATHER_API_KEY=test_key
   ```

4. **Port Conflicts**
   ```bash
   # Kill processes using test ports
   lsof -ti:2024 | xargs kill -9
   ```

### Getting Help

- Check test logs for detailed error messages
- Use `--pdb` to debug failing tests
- Review test examples in this guide
- Check pytest documentation for advanced features

---

Happy Testing! 🧪✨
