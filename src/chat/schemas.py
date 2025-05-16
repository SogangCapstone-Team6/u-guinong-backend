from pydantic import BaseModel

class ChatSchema(BaseModel):
    content: str