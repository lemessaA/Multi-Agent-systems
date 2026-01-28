import os
from dotenv import load_dotenv

load_dotenv()
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("All env vars starting with GROQ:", {k: v for k, v in os.environ.items() if k.startswith("GROQ")})
