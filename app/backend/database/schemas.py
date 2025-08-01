from pydantic import BaseModel
from datetime import datetime

class ConversationSchema(BaseModel):
    id: str
    reference: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MessageSchema(BaseModel):
    id: str
    conversation_id: str
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True