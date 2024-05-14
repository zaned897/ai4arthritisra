import os
from dotenv import load_dotenv
load_dotenv()

def get_openai_key() -> str:
    """Get the OpenAI key from the environment"""
    return os.getenv("OPENAI_API_KEY")
