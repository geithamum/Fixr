import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing environment variable: {name}. Please set it in your environment or .env file.")
    return value

# Required API keys
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")
SERPAPI_KEY = get_env_variable("SERPAPI_KEY")

# Configuration settings
MAX_SEARCH_RESULTS = 5
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_CHUNKS = 5
MODEL_NAME = "gpt-4"
