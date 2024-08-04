import os
import json
import asyncio
from quart import Quart, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder
from bot.handlers import setup_handlers
from logs import log_error
from app.models import Rave

# Initialize Quart app
app = Quart(__name__)

# Telegram bot token and chat IDs from environment variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
webhook_url = os.getenv("WEBHOOK_URL")

# Initialize Telegram bot application
application = ApplicationBuilder().token(bot_token).build()

# Load the rave model from a JSON file
rave_model = None
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

if rave_model:
    # Set up bot handlers
    setup_handlers(application, rave_model)
else:
    print("Failed to initialize rave_model. Handlers not set up.")

# Quart route for webhook
@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        update = Update.de_json(await request.get_json(), application.bot)
        application.update_queue.put(update)
        return "OK", 200
    except Exception as e:
        log_error("Failed to process webhook", exc_info=True)
        return "Internal Server Error", 500

async def set_webhook():
    try:
        # Set webhook URL
        await application.bot.set_webhook(url=webhook_url)
    except Exception as e:
        log_error("Failed to set webhook", exc_info=True)

# Endpoint to handle updates
@app.route('/update_event', methods=['POST'])
async def update_event():
    data = await request.get_json()
    file_path = os.path.join('data', 'events.json')

    try:
        with open(file_path, 'r+') as file:
            event_data = json.load(file)
            # Update event_data with new data
            event_data.update(data)
            file.seek(0)
            json.dump(event_data, file, indent=4)
            file.truncate()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to add a new participant
@app.route('/add_participant', methods=['POST'])
async def add_participant():
    data = await request.get_json()
    user_id = data.get('user_id')
    role = data.get('role')
    verification_link = data.get('verification_link')

    Rave.add_participant(user_id, role, verification_link)
    return jsonify({"status": "success"}), 200

# Endpoint to update a participant
@app.route('/update_participant', methods=['POST'])
async def update_participant():
    data = await request.get_json()
    user_id = data.get('user_id')
    role = data.get('role')
    verification_link = data.get('verification_link')

    Rave.update_participant(user_id, role, verification_link)
    return jsonify({"status": "success"}), 200

# Endpoint to get participants
@app.route('/get_participants', methods=['GET'])
async def get_participants():
    participants = Rave.get_participants()
    return jsonify(participants), 200

# Save the updated rave model to the JSON file
def save_rave_model():
    file_path = os.path.join('data', 'events.json')
    try:
        with open(file_path, 'w') as file:
            json.dump(rave_model.to_dict(), file, indent=4)
    except Exception as e:
        log_error("Failed to save rave model", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        # Run Quart app
        asyncio.run(set_webhook())
        app.run(port=int(os.getenv("PORT", 8443)))
    except Exception as e:
        log_error("Failed to start the application", exc_info=True)
