from fastapi import FastAPI

from src.llm.agent import get_graph
from src.auth import router as auth_router
from src.chat import router as chat_router

graph = get_graph()
app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)