import json

from logs import error_logger

class Rave:
    def __init__(self, insight, name, location, date, style, bpm, soundsystem=None, lineup=None, participants=None, stages=None):
        self.insight = insight
        self.name = name
        self.location = location
        self.date = date
        self.style = style
        self.bpm = bpm
        self.soundsystem = soundsystem if soundsystem else []
        self.lineup = lineup if lineup else []
        self.participants = participants if participants else []
        self.stages = stages if stages else ["Main Stage"]

    def update_event(self, location=None, date=None, style=None, bpm=None, soundsystem=None, lineup=None):
        if location:
            self.location = location
        if date:
            self.date = date
        if style:
            self.style = style
        if bpm:
            self.bpm = bpm
        if soundsystem:
            self.soundsystem = soundsystem
        if lineup:
            self.lineup = lineup

    def add_participant(self, user_id, role, verification_link=None):
        participant = {
            "user_id": user_id,
            "role": role,
            "verification_link": verification_link,
            "verified": False
        }
        self.participants.append(participant)

    def verify_participant(self, user_id):
        for participant in self.participants:
            if participant["user_id"] == user_id:
                participant["verified"] = True
                return True
        return False

    def add_donation(self, user_id, amount, element):
        donation = {
            "user_id": user_id,
            "amount": amount,
            "element": element
        }
        self.donations.append(donation)

    def to_dict(self):
        return {
            "insight": self.insight,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "style": self.style,
            "bpm": self.bpm,
            "soundsystem": self.soundsystem,
            "lineup": self.lineup,
            "participants": self.participants,
            "stages": self.stages
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            insight=data.get("insight", ""),
            name=data.get("name", ""),
            location=data.get("location", ""),
            date=data.get("date", ""),
            style=data.get("style", ""),
            bpm=data.get("bpm", 0),
            soundsystem=data.get("soundsystem", []),
            lineup=data.get("lineup", []),
            participants=data.get("participants", []),
            stages=data.get("stages", ["Main Stage"])
        )

    @classmethod
    def load_from_file(cls, file_path):
        try:
            with open(file_path, "r") as file:
                if file.read().strip():  # Check if the file is not empty
                    file.seek(0)  # Reset file pointer to the beginning
                    data = json.load(file)
                    # process data...
                    return cls.from_dict(data)
                else:
                    raise ValueError("File is empty")
        except json.JSONDecodeError as e:
            print("JSON decoding error:", e)
            return None
        except FileNotFoundError as e:
            print("File not found error:", e)
            return None
        except Exception as e:
            print("An unexpected error occurred:", e)
            return None