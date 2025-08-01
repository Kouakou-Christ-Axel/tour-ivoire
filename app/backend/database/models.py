from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(String)
    created_at = Column(String, default=datetime.now())
    updated_at = Column(String, default=datetime.now())

    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    role = Column(String)  # 'user' ou 'assistant'
    content = Column(String)
    created_at = Column(String, default=datetime.now())
    updated_at = Column(String, default=datetime.now())

    conversation = relationship("Conversation", back_populates="messages")


