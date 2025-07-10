from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from langchain_core.messages import SystemMessage, HumanMessage
from app.ai.prompts import extract_prompt

from app.ai.models import extract_preferences


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
    messages = [
        SystemMessage(content=extract_prompt),
        HumanMessage(content=update.message.text)
    ]
    response = extract_preferences(messages)

    if not response:
        await update.message.reply_text("Désolé, je n'ai pas pu comprendre votre demande.")
        return

    await update.message.reply_text(response.text())


def setup_handlers(application):
    application.add_handler(CommandHandler('start', start))
    # Filtrer les messages texte pour éviter les commandes
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
