from app.ai.seeds.seed_cities import seed_cities
from bot.telegram_bot import setup_handlers
from telegram.ext import ApplicationBuilder
from config import Config


def main():
    seed_cities()
    # Create the application instance
    app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()

    setup_handlers(app)

    print("Le Telegram bot est en cours d'exécution...")
    # Start the bot
    app.run_polling()


if __name__ == "__main__":
    main()
