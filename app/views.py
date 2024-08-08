from flask import render_template, jsonify, request
from app.models import Rave
from app.utils import read_json, write_json
from logs.logs import log_error, log_info
from openai import OpenAI
import os

# Initialize OpenAI client
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load rave data from JSON files
def load_rave_data():
    try:
        events = read_json("data/events.json")
        participants = read_json("data/participants.json")
        donations = read_json("data/donations.json")
        soundsystem = read_json("data/soundsystem.json")
        return events, participants, donations, soundsystem
    except Exception as e:
        log_error("Exception occurred while loading rave data", exc_info=True)
        return None, None, None, None

# Save rave data to JSON files
def save_rave_data(events, participants, donations, soundsystem):
    try:
        write_json("data/events.json", events)
        write_json("data/participants.json", participants)
        write_json("data/donations.json", donations)
        write_json("data/soundsystem.json", soundsystem)
    except Exception as e:
        log_error("Exception occurred while saving rave data", exc_info=True)

def index():
    """
    Render the main page of the Mini App.
    """
    return render_template("index.html")

def handle_submit():
    """
    Handle form submission from the Mini App.
    """
    data = request.get_json()
    user_input = data.get('input')

    # Process the user input (this could include various operations such as validation, updating the model, etc.)
    response_message = f"Thank you, {user_input}! Your submission has been received."

    # Example of updating the participants list
    events, participants, donations, soundsystem = load_rave_data()
    if participants is not None:
        participants.append({"name": user_input})
        save_rave_data(events, participants, donations, soundsystem)

        # Analyze data and provide suggestions
        analyze_data_and_optimize()

    return jsonify({"response": response_message})

def get_rave_info():
    """
    Get information about the current rave event.
    """
    events, participants, donations, soundsystem = load_rave_data()
    if events is not None:
        current_event = events.get("current_event", {})
        return jsonify(current_event)
    else:
        return jsonify({"error": "Unable to load rave information"}), 500

def get_participants():
    """
    Get the list of participants.
    """
    events, participants, donations, soundsystem = load_rave_data()
    if participants is not None:
        return jsonify(participants)
    else:
        return jsonify({"error": "Unable to load participants"}), 500

def get_donations():
    """
    Get the list of donations.
    """
    events, participants, donations, soundsystem = load_rave_data()
    if donations is not None:
        return jsonify(donations)
    else:
        return jsonify({"error": "Unable to load donations"}), 500

def get_soundsystem():
    """
    Get the current state of the soundsystem.
    """
    events, participants, donations, soundsystem = load_rave_data()
    if soundsystem is not None:
        return jsonify(soundsystem)
    else:
        return jsonify({"error": "Unable to load soundsystem information"}), 500

def analyze_data_and_optimize():
    try:
        events, participants, donations, soundsystem = load_rave_data()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI assistant that analyzes rave data and provides optimization suggestions."},
                {"role": "user", "content": f"Analyze the following rave data and provide suggestions for optimization:\n\nEvents: {events}\n\nParticipants: {participants}\n\nDonations: {donations}\n\nSoundsystem: {soundsystem}"}
            ]
        )
        analysis = response.choices[0].message.content
        log_info("AI Analysis and Suggestions:")
        log_info(analysis)
        # Implement suggested optimizations (this part would depend on the specific suggestions provided by AI)
    except Exception as e:
        log_error("Failed to analyze and optimize rave data", exc_info=True)
