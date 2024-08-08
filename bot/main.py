import os
from telegram.ext import ApplicationBuilder
from app.models import Rave
from app.utils import load_env_vars
from bot.handlers import setup_handlers
from logs.logs import log_error, log_info

# Load environment variables
load_env_vars()

# Telegram bot token and chat IDs from environment variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
group_chat_id = os.getenv("GROUP_CHAT_ID")
verification_chat_id = os.getenv("VERIFICATION_CHAT_ID")

# Initialize Rave model
try:
    rave_model = Rave.load_from_db(1)
    if not rave_model:
        rave_model = Rave(
            insight="",
            name="",
            location="",
            date="",
            style="",
            bpm=0,
            soundsystem=[],
            lineup=[],
            participants=[],
            stages=["Main Stage"],
            donations=[]
        )
        rave_model.save_to_db()
except Exception as e:
    log_error("Exception occurred while loading Rave model", exc_info=True)
    rave_model = Rave(
        insight="",
        name="",
        location="",
        date="",
        style="",
        bpm=0,
        soundsystem=[],
        lineup=[],
        participants=[],
        stages=["Main Stage"],
        donations=[]
    )

# Initialize Telegram bot application
application = ApplicationBuilder().token(bot_token).build()

# Set up bot handlers
setup_handlers(application, rave_model)

def main():
    """Start the bot."""
    try:
        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        log_info("Bot started and running.")
    except Exception as e:
        log_error("Exception occurred while running the bot", exc_info=True)

if __name__ == '__main__':
    main()
