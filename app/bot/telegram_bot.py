from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from app.backend.services.message_service import prepare_agent_messages, process_agent_response, save_messages


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
    chat_id = str(update.effective_chat.id)
    user_message = update.message.text

    # Préparer les messages pour l'agent
    agent_messages = prepare_agent_messages(chat_id, user_message)

    # Appeler l'agent et traiter la réponse
    ai_message = process_agent_response(agent_messages)

    if not ai_message:
        await update.message.reply_text("Désolé, je n'ai pas pu comprendre votre demande.")
        return

    # Enregistrer les messages dans la base de données
    save_messages(chat_id, user_message, ai_message)

    # Répondre à l'utilisateur
    await update.message.reply_text(ai_message)

def setup_handlers(application):
    application.add_handler(CommandHandler('start', start))
    # Filtrer les messages texte pour éviter les commandes
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
