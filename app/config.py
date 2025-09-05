import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


class Config:
    """
    Configuration class to hold environment variables and other settings.
    """
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default to SQLite for local development
    TRIPADVISOR_API_KEY = os.getenv("TRIPADVISOR_API_KEY", "")
    
    # RapidAPI credentials
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "501b353461mshb7dad30140a4e71p1135acjsn20b844c9d4aa")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "tripadvisor16.p.rapidapi.com")
