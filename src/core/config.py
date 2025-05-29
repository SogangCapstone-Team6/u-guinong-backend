import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
LANGSMITH_TRACING=os.environ.get("LANGSMITH_TRACING").lower() == "true"
LANGSMITH_API_KEY=os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_ENDPOINT=os.environ.get("LANGSMITH_ENDPOINT")
LANGSMITH_PROJECT=os.environ.get("LANGSMITH_PROJECT")
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
SECTIONS_PATH=os.environ.get("SECTIONS_PATH")
CHUNK_INDEX_PATH=os.environ.get("CHUNK_INDEX_PATH")
TOP_K_SECTIONS=os.environ.get("TOP_K_SECTIONS")
TOP_K_CHUNKS=os.environ.get("TOP_K_CHUNKS")
