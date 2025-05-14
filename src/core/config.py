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