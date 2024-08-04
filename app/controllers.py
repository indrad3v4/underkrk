from app.models import Rave
from app.utils import read_json, write_json, validate_date, validate_bpm, validate_soundsystem, validate_lineup, validate_participants
from flask import jsonify
from logs import error_logger

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
            write_json("data/events.json", self.rave_model.to_dict())
        except Exception as e:
            error_logger.error("Failed to save event data", exc_info=True)
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
            write_json("data/events.json", self.rave_model.to_dict())
        except Exception as e:
            error_logger.error("Failed to update event data", exc_info=True)
            return {"error": "Failed to update event data"}

        return {"success": "Event updated successfully"}

    def register_participant(self, user_id, role, verification_link=None):
        participant = {
            "user_id": user_id,
            "role": role,
            "verification_link": verification_link
        }
        self.rave_model.participants.append(participant)

        try:
            write_json("data/participants.json", self.rave_model.participants)
        except Exception as e:
            error_logger.error("Failed to register participant", exc_info=True)
            return {"error": "Failed to register participant"}

        return {"success": "Participant registered successfully"}

    def verify_participant(self, user_id):
        for participant in self.rave_model.participants:
            if participant["user_id"] == user_id:
                participant["verified"] = True
                try:
                    write_json("data/participants.json", self.rave_model.participants)
                except Exception as e:
                    error_logger.error("Failed to verify participant", exc_info=True)
                    return {"error": "Failed to verify participant"}
                return {"success": "Participant verified successfully"}

        return {"error": "Participant not found"}

    def generate_ai_response(self, user_message):
        try:
            completion = self.ai_client.chat_completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are AI-Powered Rave Coordinator Bot who helps roles in the rave get an ideal rave experience. You base your juicy yet funny tone of voice on values of peace, love, unity, respect. The rave details are: Insight: {self.rave_model.insight}, Sound System: {self.rave_model.soundsystem}, Lineup: {self.rave_model.lineup}, Place: {self.rave_model.place}, Time: {self.rave_model.time}, style='ravecore', bpm={self.rave_model.bpm}, Role: {role}"},
                    {"role": "user", "content": user_message}
                ]
            )
            response = completion.choices[0].message.content
            return {"response": response}
        except Exception as e:
            error_logger.error("Failed to generate AI response", exc_info=True)
            return {"error": "Failed to generate AI response"}

    def handle_donation(self, user_id, amount, element):
        donation = {
            "user_id": user_id,
            "amount": amount,
            "element": element
        }
        self.rave_model.donations.append(donation)

        try:
            write_json("data/donations.json", self.rave_model.donations)
        except Exception as e:
            error_logger.error("Failed to handle donation", exc_info=True)
            return {"error": "Failed to handle donation"}

        return {"success": "Donation received successfully"}
