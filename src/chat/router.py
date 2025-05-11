from fastapi import APIRouter

from .models import Chat

from src.database import SessionLocal

router = APIRouter(
    prefix="/api/chat"
)

@router.get("/")
def chat_main():
    return {"response": "chat_main"}

@router.post("/")
def chat_init():
    return {"response": "chat_init"}