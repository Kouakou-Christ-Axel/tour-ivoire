from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import create_react_agent

from app.ai.tools.tools import agent_tools
from app.config import Config

model = init_chat_model(
    model="gpt-4o-mini",
    temperature=0,
    api_key=Config.OPENAI_API_KEY,
    model_provider='openai',
)

agent = create_react_agent(model, agent_tools)


def converse(messages: list) -> BaseMessage:
    """
    Extrait les préférences de voyage à partir des messages de l'utilisateur.

    Args:
        messages (list): Les messages de l'utilisateur, incluant un message système et un message humain.

    Returns:
        dict: Un dictionnaire contenant les préférences extraites.
    """

    response = model.invoke(messages)
    return response
