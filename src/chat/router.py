import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Annotated
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory

from src.database import get_db
from src.chat.models import Chat
from src.auth.models import User
from src.auth.utils import get_user
from src.llm.agent import graph
from src.core.config import SQLALCHEMY_DATABASE_URL

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
    chat_uuid = uuid.UUID(chat_id)
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_uuid).first()
    
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid chat id"
        )

    if db_chat.user != user.email :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No access to given chat id"
        )

    chat_message_history = SQLChatMessageHistory(
        session_id=chat_id, connection=SQLALCHEMY_DATABASE_URL
    )

    chatting_history = [{
        "content": message.content,
        "type": 1 if type(message) is HumanMessage else 0
    } for message in chat_message_history.messages
    ]
    
    return {"chatting_history": chatting_history}

@router.post("/{chat_id}")
async def send_chatting(
    chat_id: str, 
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)], 
    content: Annotated[str, Form(...)], 
    disease: Annotated[str, Form] | None='',
    image: Annotated[UploadFile, Form] | None=File(None)
):
    chat_uuid = uuid.UUID(chat_id)
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_uuid).first()
    
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid chat id"
        )

    if db_chat.user != user.email :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No access to given chat id"
        )

    config = {"configurable": {"thread_id": chat_id}}
    response = await graph.ainvoke({
            "messages" : HumanMessage(content=content),
            "input" : content,
            "disease" : disease
         }, config=config)
    
    response_content = response["messages"][-1].content
    chat_message_history = SQLChatMessageHistory(
        session_id=chat_id, connection=SQLALCHEMY_DATABASE_URL
    )

    chat_message_history.add_user_message(content)
    chat_message_history.add_ai_message(response_content)

    return {"response": response_content}
