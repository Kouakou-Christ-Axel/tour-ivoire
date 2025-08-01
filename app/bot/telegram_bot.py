from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from langchain_core.messages import SystemMessage, HumanMessage
from app.ai.prompts import extract_prompt

from app.ai.models import agent
from app.backend.utils import get_conversation_messages, add_conversation_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue sur IvoireTour ! 🇨🇮\n"
        "Dis-moi en quelques phrases ce que tu aimerais vivre comme aventure.\n"
        "Par exemple : 'Je veux visiter les plages, découvrir la gastronomie locale, depuis Abidjan, pour 5 jours.'"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Traite les messages texte reçus par le bot.
    """
    # Récupérer les messages de la conversation
    db_messages = get_conversation_messages(str(update.effective_chat.id))

    # Créer une nouvelle liste pour l'agent avec les objets LangChain
    agent_messages = [SystemMessage(content=extract_prompt)]

    # Convertir les messages de la base de données en objets LangChain
    if db_messages:
        for msg in db_messages:
            if msg.role == 'user':
                agent_messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                agent_messages.append(SystemMessage(content=msg.content))

    # Ajouter le message actuel
    agent_messages.append(HumanMessage(content=update.message.text))

    # Appeler l'agent avec la liste correcte
    response = agent.invoke(input={"messages": agent_messages})

    if not response:
        await update.message.reply_text("Désolé, je n'ai pas pu comprendre votre demande.")
        return

    ai_message = response["messages"][-1].content

    # Enregistrer les messages dans la conversation
    add_conversation_message(
        reference=str(update.effective_chat.id),
        role='user',
        content=update.message.text
    )
    add_conversation_message(
        reference=str(update.effective_chat.id),
        role='assistant',
        content=ai_message
    )

    await update.message.reply_text(ai_message)

def setup_handlers(application):
    application.add_handler(CommandHandler('start', start))
    # Filtrer les messages texte pour éviter les commandes
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
