import json
import logging
import sqlite3
from logs import log_error

# Connect to SQLite database (create if not exists)
conn = sqlite3.connect('raves.db')
cursor = conn.cursor()

# Create table for raves if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS raves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insight TEXT,
    name TEXT,
    location TEXT,
    date TEXT,
    style TEXT,
    bpm INTEGER,
    soundsystem TEXT,
    lineup TEXT,
    participants TEXT,
    stages TEXT,
    donations TEXT
)
''')
conn.commit()

class Rave:
    def __init__(self, insight, name, location, date, style, bpm, soundsystem=None, lineup=None, participants=None, stages=None, donations=None):
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
        self.donations = donations if donations else []

    def save_to_db(self):
        try:
            cursor.execute('''
                INSERT INTO raves (insight, name, location, date, style, bpm, soundsystem, lineup, participants, stages, donations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.insight, self.name, self.location, self.date, self.style, self.bpm,
                json.dumps(self.soundsystem), json.dumps(self.lineup),
                json.dumps(self.participants), json.dumps(self.stages), json.dumps(self.donations)
            ))
            conn.commit()
        except Exception as e:
            log_error("Failed to save rave to database", exc_info=True, rave=self.__dict__)

    @staticmethod
    def load_from_db(rave_id):
        try:
            cursor.execute('SELECT * FROM raves WHERE id = ?', (rave_id,))
            row = cursor.fetchone()
            if row:
                return Rave(
                    insight=row[1], name=row[2], location=row[3], date=row[4],
                    style=row[5], bpm=row[6], soundsystem=json.loads(row[7]),
                    lineup=json.loads(row[8]), participants=json.loads(row[9]),
                    stages=json.loads(row[10]), donations=json.loads(row[11])
                )
        except Exception as e:
            log_error("Failed to load rave from database", exc_info=True, rave_id=rave_id)
        return None

    @staticmethod
    def load_all_from_db():
        try:
            cursor.execute('SELECT * FROM raves')
            rows = cursor.fetchall()
            return [Rave(
                insight=row[1], name=row[2], location=row[3], date=row[4],
                style=row[5], bpm=row[6], soundsystem=json.loads(row[7]),
                lineup=json.loads(row[8]), participants=json.loads(row[9]),
                stages=json.loads(row[10]), donations=json.loads(row[11])
            ) for row in rows]
        except Exception as e:
            log_error("Failed to load raves from database", exc_info=True)
            return []

# Example usage
rave = Rave("Insight", "Rave Name", "Location", "2024-08-04", "Style", 120)
rave.save_to_db()

loaded_rave = Rave.load_from_db(1)
print(loaded_rave.__dict__ if loaded_rave else "No rave found")
