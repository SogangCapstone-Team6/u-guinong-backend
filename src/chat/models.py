from sqlalchemy import Column, Integer, ForeignKey, UUID

from src.database import Base

class Chat(Base):
    __tablename__ = "chat"

    chat_id = Column(UUID(as_uuid=True), primary_key=True)
    user = Column(Integer, ForeignKey("user.id"))
    