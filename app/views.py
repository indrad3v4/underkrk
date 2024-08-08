from flask import render_template, jsonify, request
from app.models import Rave
from logs.logs import log_error, log_info
from openai import OpenAI
import os

# Initialize OpenAI client
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    rave_model = Rave.load_from_db(1)
    if rave_model:
        rave_model.participants.append({"name": user_input})
        rave_model.save_to_db()

        # Analyze data and provide suggestions
        analyze_data_and_optimize(rave_model)

    return jsonify({"response": response_message})

def get_rave_info():
    """
    Get information about the current rave event.
    """
    rave_model = Rave.load_from_db(1)
    if rave_model:
        return jsonify(rave_model.__dict__)
    else:
        return jsonify({"error": "Unable to load rave information"}), 500

def get_participants():
    """
    Get the list of participants.
    """
    rave_model = Rave.load_from_db(1)
    if rave_model:
        return jsonify(rave_model.participants)
    else:
        return jsonify({"error": "Unable to load participants"}), 500

def get_donations():
    """
    Get the list of donations.
    """
    rave_model = Rave.load_from_db(1)
    if rave_model:
        return jsonify(rave_model.donations)
    else:
        return jsonify({"error": "Unable to load donations"}), 500

def get_soundsystem():
    """
    Get the current state of the soundsystem.
    """
    rave_model = Rave.load_from_db(1)
    if rave_model:
        return jsonify(rave_model.soundsystem)
    else:
        return jsonify({"error": "Unable to load soundsystem information"}), 500

def analyze_data_and_optimize(rave_model):
    try:
        response = client.chat_completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI assistant that analyzes rave data and provides optimization suggestions."},
                {"role": "user", "content": f"Analyze the following rave data and provide suggestions for optimization:\n\nEvents: {rave_model.__dict__}"}
            ]
        )
        analysis = response.choices[0].message.content
        log_info("AI Analysis and Suggestions:")
        log_info(analysis)
        # Implement suggested optimizations (this part would depend on the specific suggestions provided by AI)
    except Exception as e:
        log_error("Failed to analyze and optimize rave data", exc_info=True)

