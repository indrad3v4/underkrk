import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration class.
    """
    APP_NAME = "UnderKrakow Rave Bot"
    DEBUG = False
    TESTING = False

    # Telegram bot configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
    VERIFICATION_CHAT_ID = os.getenv("VERIFICATION_CHAT_ID")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    # OpenAI configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"

    # File paths for JSON data
    EVENTS_FILE_PATH = "data/events.json"
    PARTICIPANTS_FILE_PATH = "data/participants.json"
    DONATIONS_FILE_PATH = "data/donations.json"
    SOUNDSYSTEM_FILE_PATH = "data/soundsystem.json"

    # Rave event default configuration
    RAVE_INSIGHT = "Craving euphoria in nature? Welcome to UnderKrakow Rave! Engage in a pleasure rave experience as summer peaks!"
    RAVE_NAME = "UnderKrakow Rave"
    RAVE_LOCATION = "Under bridge in Scenic forest in Krakow"
    RAVE_DATE = "2024-08-17 from 12:00 PM"
    RAVE_STYLE = "ravecore"
    RAVE_BPM = 150
    RAVE_SOUNDSYSTEM = ["Default Sound System"]
    RAVE_LINEUP = []
    RAVE_PARTICIPANTS = []
    RAVE_STAGES = ["Main Stage"]

class DevelopmentConfig(Config):
    """
    Development configuration class.
    """
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """
    Production configuration class.
    """
    DEBUG = False
    TESTING = False
