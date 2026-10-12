from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_claude_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing. Check your .env file.")
    return Anthropic(api_key=api_key)
