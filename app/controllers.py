from app.models import Rave
from flask import jsonify
from logs.logs import log_error, log_info
from openai import OpenAI
import os

class RaveController:
    def __init__(self, rave_model, ai_client, group_chat_id, verification_chat_id):
        self.rave_model = rave_model
        self.ai_client = ai_client
        self.group_chat_id = group_chat_id
        self.verification_chat_id = verification_chat_id

    def create_event(self, name, location, date, style, bpm):
        if not validate_date(date):
            return {"error": "Invalid date format"}
        if not validate_bpm(bpm):
            return {"error": "BPM must be a positive integer"}

        self.rave_model.name = name
        self.rave_model.location = location
        self.rave_model.date = date
        self.rave_model.style = style
        self.rave_model.bpm = bpm

        try:
            self.rave_model.save_to_db()
            log_info("Event created successfully: " + name)
            self.analyze_and_optimize()
        except Exception as e:
            log_error("Failed to save event data", exc_info=True)
            return {"error": "Failed to save event data"}

        return {"success": "Event created successfully"}

    def update_event(self, location=None, date=None, style=None, bpm=None, soundsystem=None, lineup=None):
        if location:
            self.rave_model.location = location
        if date:
            if not validate_date(date):
                return {"error": "Invalid date format"}
            self.rave_model.date = date
        if style:
            self.rave_model.style = style
        if bpm:
            if not validate_bpm(bpm):
                return {"error": "BPM must be a positive integer"}
            self.rave_model.bpm = bpm
        if soundsystem:
            if not validate_soundsystem(soundsystem):
                return {"error": "Invalid soundsystem data"}
            self.rave_model.soundsystem = soundsystem
        if lineup:
            if not validate_lineup(lineup):
                return {"error": "Invalid lineup data"}
            self.rave_model.lineup = lineup

        try:
            self.rave_model.save_to_db()
            log_info("Event updated successfully: " + self.rave_model.name)
            self.analyze_and_optimize()
        except Exception as e:
            log_error("Failed to update event data", exc_info=True)
            return {"error": "Failed to update event data"}

        return {"success": "Event updated successfully"}

    def register_participant(self, user_id, role, verification_link=None):
        try:
            Rave.add_participant(user_id, role, verification_link, self.rave_model.id)
            log_info("Participant registered successfully: " + user_id)
            self.analyze_and_optimize()
        except Exception as e:
            log_error("Failed to register participant", exc_info=True)
            return {"error": "Failed to register participant"}

        return {"success": "Participant registered successfully"}

    def verify_participant(self, user_id):
        try:
            participants = Rave.get_participants()
            for participant in participants:
                if participant["user_id"] == user_id:
                    participant["verified"] = True
                    Rave.update_participant(user_id, participant["role"], participant["verification_link"], self.rave_model.id)
                    log_info("Participant verified successfully: " + user_id)
                    self.analyze_and_optimize()
                    return {"success": "Participant verified successfully"}
        except Exception as e:
            log_error("Failed to verify participant", exc_info=True)
            return {"error": "Failed to verify participant"}

        return {"error": "Participant not found"}

    def generate_ai_response(self, user_message):
        try:
            completion = self.ai_client.chat_completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are AI-Powered Rave Coordinator Bot who helps roles in the rave get an ideal rave experience. You base your juicy yet funny tone of voice on values of peace, love, unity, respect. The rave details are: Insight: {self.rave_model.insight}, Sound System: {self.rave_model.soundsystem}, Lineup: {self.rave_model.lineup}, Place: {self.rave_model.location}, Time: {self.rave_model.date}, style='ravecore', bpm={self.rave_model.bpm}, Role: {role}"},
                    {"role": "user", "content": user_message}
                ]
            )
            response = completion.choices[0].message.content
            log_info("AI response generated: " + response)
            return {"response": response}
        except Exception as e:
            log_error("Failed to generate AI response", exc_info=True)
            return {"error": "Failed to generate AI response"}

    def handle_donation(self, user_id, amount, element):
        try:
            Rave.add_donation(user_id, amount, element, self.rave_model.id)
            log_info("Donation received successfully: " + user_id + " - " + str(amount))
            self.analyze_and_optimize()
        except Exception as e:
            log_error("Failed to handle donation", exc_info=True)
            return {"error": "Failed to handle donation"}

        return {"success": "Donation received successfully"}

    def analyze_and_optimize(self):
        try:
            events, participants, donations, soundsystem = self.load_rave_data()
            response = self.ai_client.chat_completions.create(
                model="gpt-4o-mini",
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

    def load_rave_data(self):
        try:
            rave = Rave.load_from_db(self.rave_model.id)
            return rave.name, rave.participants, rave.donations, rave.soundsystem
        except Exception as e:
            log_error("Exception occurred while loading rave data", exc_info=True)
            return None, None, None, None
