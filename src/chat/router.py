import uuid

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from typing import Annotated

from src.database import get_db
from src.chat.models import Chat
from src.chat.schemas import ChatSchema
from src.auth.models import User
from src.auth.utils import get_user


router = APIRouter(
    prefix="/api/chat"
)

@router.get("/")
def chatting_main(user: Annotated[User, Depends(get_user)], db: Annotated[Session, Depends(get_db)]):
    db_chat = db.query(Chat).filter(user.email == Chat.user).all()

    chats = [{"chat_id": chat.chat_id} for chat in db_chat]

    return {"chats": chats}

@router.post("/")
def init_chatting(user: Annotated[User, Depends(get_user)], db: Annotated[Session, Depends(get_db)]):
    chat_id = uuid.uuid4()
    
    db_chat = Chat(
        chat_id=chat_id,
        user=user.email
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return {"chat_id": chat_id}

@router.get("/{chat_id}")
def get_chatting_history(chat_id: str, user: Annotated[User, Depends(get_user)], db: Annotated[Session, Depends(get_db)]):
    return {"response": chat_id}

@router.post("/{chat_id}")
def send_chatting(chat_id: str, chat: ChatSchema):
    return {"response": chat_id, "content": chat.content}