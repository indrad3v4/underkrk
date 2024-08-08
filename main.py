import os
import json
import asyncio
from quart import Quart, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder
from bot.handlers import setup_handlers
from logs.logs import log_error  # Corrected import
from app.models import Rave  # Ensure this import is correct

# Initialize Quart app
app = Quart(__name__)

# Telegram bot token and chat IDs from environment variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
webhook_url = os.getenv("WEBHOOK_URL")

# Initialize Telegram bot application
application = ApplicationBuilder().token(bot_token).build()

# Load the rave model from the database
rave_model = None
try:
    rave_model = Rave.load_from_db(1)  # Use the correct method and identifier
except Exception as e:
    log_error("Failed to load rave model from the database", exc_info=True)

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
    try:
        # Update the event data in the database
        cursor.execute('''
            UPDATE raves
            SET insight = ?, name = ?, location = ?, date = ?, style = ?, bpm = ?, soundsystem = ?, lineup = ?, participants = ?, stages = ?, donations = ?
            WHERE id = 1
        ''', (
            data.get('insight'), data.get('name'), data.get('location'), data.get('date'), data.get('style'), data.get('bpm'),
            json.dumps(data.get('soundsystem')), json.dumps(data.get('lineup')),
            json.dumps(data.get('participants')), json.dumps(data.get('stages')), json.dumps(data.get('donations'))
        ))
        conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        log_error("Failed to update event data", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to add a new participant
@app.route('/add_participant', methods=['POST'])
async def add_participant():
    data = await request.get_json()
    user_id = data.get('user_id')
    role = data.get('role')
    verification_link = data.get('verification_link')

    try:
        Rave.add_participant(user_id, role, verification_link)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        log_error("Failed to add participant", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to update a participant
@app.route('/update_participant', methods=['POST'])
async def update_participant():
    data = await request.get_json()
    user_id = data.get('user_id')
    role = data.get('role')
    verification_link = data.get('verification_link')

    try:
        Rave.update_participant(user_id, role, verification_link)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        log_error("Failed to update participant", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to get participants
@app.route('/get_participants', methods=['GET'])
async def get_participants():
    try:
        participants = Rave.get_participants()
        return jsonify(participants), 200
    except Exception as e:
        log_error("Failed to retrieve participants", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# Save the updated rave model to the database
def save_rave_model():
    try:
        rave_model.save_to_db()
    except Exception as e:
        log_error("Failed to save rave model", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        # Run Quart app
        asyncio.run(set_webhook())
        app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8443)))
    except Exception as e:
        log_error("Failed to start the application", exc_info=True)
