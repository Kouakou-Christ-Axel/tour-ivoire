from langchain_core.messages import SystemMessage, HumanMessage
from typing import Union
from app.ai.prompts import extract_prompt
from app.backend.utils import get_conversation_messages, add_conversation_message
from app.ai.models import agent

MessageType = Union[SystemMessage, HumanMessage]

def prepare_agent_messages(chat_id: str, user_message: str):
    """
    Prépare les messages pour l'agent en incluant les messages de la base de données.
    """
    db_messages = get_conversation_messages(chat_id)
    agent_messages: list[MessageType] = [SystemMessage(content=extract_prompt)]

    if db_messages:
        for msg in db_messages:
            if msg.role == 'user':
                agent_messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                agent_messages.append(SystemMessage(content=msg.content))

    agent_messages.append(HumanMessage(content=user_message))
    return agent_messages

def process_agent_response(agent_messages):
    """
    Appelle l'agent et retourne la réponse.
    """
    response = agent.invoke(input={"messages": agent_messages})
    if response:
        return response["messages"][-1].content
    return None

def save_messages(chat_id: str, user_message: str, ai_message: str):
    """
    Enregistre les messages utilisateur et assistant dans la base de données.
    """
    add_conversation_message(reference=chat_id, role='user', content=user_message)
    add_conversation_message(reference=chat_id, role='assistant', content=ai_message)