from app.backend.database.database import SessionLocal
from app.backend.database.models import Conversation, Message


def get_conversation(reference: str) -> Conversation:
    """
    Récupère une conversation à partir de son ID.
    :param reference: Référence de la conversation
    :return: Conversation ou None si non trouvée
    """
    session = SessionLocal()
    try:
        return session.query(Conversation).filter(Conversation.reference == reference).first()
    finally:
        session.close()


def get_conversation_messages(reference: str) -> list:
    """
    Récupère les messages d'une conversation à partir de sa référence.
    :param reference:
    :return: liste de messages
    """

    session = SessionLocal()
    try:
        conversation = session.query(Conversation).filter(Conversation.reference == reference).first()

        if conversation:
            return conversation.messages

        # Si aucune conversation n'est trouvée, retourner une liste vide et creer une nouvelle conversation
        else:
            new_conversation = Conversation(reference=reference)
            session.add(new_conversation)
            session.commit()
            return new_conversation.messages
    finally:
        session.close()


def add_conversation_message(reference: str, role: str, content: str) -> None:
    """
    Ajoute un message à une conversation existante ou crée une nouvelle conversation si elle n'existe pas.
    :param reference: Référence de la conversation
    :param role: Rôle du message ('user' ou 'assistant')
    :param content: Contenu du message
    """

    session = SessionLocal()
    try:
        conversation = get_conversation(reference)
        if not conversation:
            conversation = Conversation(reference=reference)
            session.add(conversation)

        new_message = Message(role=role, content=content, conversation_id=conversation.id)
        session.add(new_message)
        session.commit()

    finally:
        session.close()
