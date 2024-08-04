from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from logs import logging, error_logger
from app.models import Rave
import json



# Initialize the Rave model (assuming it's already loaded or passed to this module)
# This should ideally be passed or accessed from the main bot application
# Attempt to load the rave model from a JSON file
try:
    with open("data/events.json", "r") as file:
        if file.read().strip():  # Check if the file is not empty
            file.seek(0)  # Reset file pointer to the beginning
            rave_model = Rave.load_from_file("data/events.json")
        else:
            print("events.json file is empty. Please provide valid JSON data.")
except json.JSONDecodeError as e:
    print("Failed to decode JSON from events.json:", e)
except FileNotFoundError as e:
    print("events.json file not found:", e)
except Exception as e:
    print("An unexpected error occurred:", e)

async def handle_payment(update: Update, context: CallbackContext) -> None:
    try:
        query = update.callback_query
        user_id = query.from_user.id
        username = query.from_user.username if query.from_user.username else query.from_user.first_name
        element = context.user_data.get('element')
        amount = float(query.data.split('_')[1])

        # Update the donations in the Rave model
        rave_model.add_donation(user_id, amount, element)
        rave_model.save_to_file("data/events.json")

        # Acknowledge the donation
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Thank you for your donation of ${amount} towards {element}, {username}!"
        )

        # Notify the group chat
        await context.bot.send_message(
            chat_id=os.getenv("GROUP_CHAT_ID"),
            text=f"{username} has donated ${amount} towards {element}!"
        )

        logging.info(f"User @{username} donated ${amount} towards {element}.")
    except Exception as e:
        error_logger.error("Exception occurred while handling payment", exc_info=True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while processing your donation. Please try again."
        )

def setup_payment_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_payment, pattern=r'donate_\d+'))
