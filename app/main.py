import os

from bot.telegram_bot import setup_handlers
from telegram.ext import ApplicationBuilder
from config import Config


def main():
    # Create the application instance
    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

    setup_handlers(app)

    print("Starting bot...")
    # Start the bot
    app.run_polling()


if __name__ == "__main__":
    main()
