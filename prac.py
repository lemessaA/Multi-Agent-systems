# Complete starter template with all concepts
from langchain.chat_models import init_chat_model
from langchain.tools import tool
import os

# 1. Setup
os.environ["OPENAI_API_KEY"] = "your-key"
model = init_chat_model("gpt-4", temperature=0.5)

# 2. Basic usage
response = model.invoke("Explain quantum computing simply")
print(response)

# 3. Streaming
for chunk in model.stream("Tell me a story"):
    print(chunk.text, end="")

# 4. Tool calling example
@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    return str(eval(expression))

model_with_math = model.bind_tools([calculate])
result = model_with_math.invoke("What is 15 * 24?")