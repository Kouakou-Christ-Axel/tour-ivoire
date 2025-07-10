from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from app.config import Config

extract_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=Config.OPENAI_API_KEY,
)


def extract_preferences(messages: list) -> BaseMessage:
    """
    Extrait les préférences de voyage à partir des messages de l'utilisateur.

    Args:
        messages (list): Les messages de l'utilisateur, incluant un message système et un message humain.

    Returns:
        dict: Un dictionnaire contenant les préférences extraites.
    """

    response = extract_model.invoke(messages)
    return response
