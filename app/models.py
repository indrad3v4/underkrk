import json
import sqlite3
from logs.logs import log_error

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
    date DATE,
    style TEXT,
    bpm INTEGER,
    soundsystem TEXT,
    lineup TEXT,
    participants TEXT,
    stages TEXT,
    donations TEXT
)
''')

# Create table for participants if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    verification_link TEXT,
    rave_id INTEGER,
    FOREIGN KEY(rave_id) REFERENCES raves(id)
)
''')

# Create table for soundsystem if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS soundsystem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rave_id INTEGER,
    FOREIGN KEY(rave_id) REFERENCES raves(id)
)
''')

# Create table for lineup if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS lineup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name TEXT,
    rave_id INTEGER,
    FOREIGN KEY(rave_id) REFERENCES raves(id)
)
''')

# Create table for stages if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rave_id INTEGER,
    FOREIGN KEY(rave_id) REFERENCES raves(id)
)
''')

# Create table for donations if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    amount REAL,
    element TEXT,
    rave_id INTEGER,
    FOREIGN KEY(rave_id) REFERENCES raves(id)
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
    def add_participant(user_id, role, verification_link, rave_id):
        try:
            cursor.execute('''
                INSERT INTO participants (user_id, role, verification_link, rave_id)
                VALUES (?, ?, ?, ?)
            ''', (user_id, role, verification_link, rave_id))
            conn.commit()
        except Exception as e:
            log_error("Failed to add participant to database", exc_info=True, user_id=user_id, role=role, verification_link=verification_link)

    @staticmethod
    def update_participant(user_id, role=None, verification_link=None, rave_id=None):
        try:
            if role:
                cursor.execute('''
                    UPDATE participants
                    SET role = ?
                    WHERE user_id = ?
                ''', (role, user_id))
            if verification_link:
                cursor.execute('''
                    UPDATE participants
                    SET verification_link = ?
                    WHERE user_id = ?
                ''', (verification_link, user_id))
            if rave_id:
                cursor.execute('''
                    UPDATE participants
                    SET rave_id = ?
                    WHERE user_id = ?
                ''', (rave_id, user_id))
            conn.commit()
        except Exception as e:
            log_error("Failed to update participant in database", exc_info=True, user_id=user_id, role=role, verification_link=verification_link)

    @staticmethod
    def get_participants():
        try:
            cursor.execute('SELECT * FROM participants')
            return cursor.fetchall()
        except Exception as e:
            log_error("Failed to retrieve participants from database", exc_info=True)
            return []

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

    @staticmethod
    def add_soundsystem(name, rave_id):
        try:
            cursor.execute('''
                INSERT INTO soundsystem (name, rave_id)
                VALUES (?, ?)
            ''', (name, rave_id))
            conn.commit()
        except Exception as e:
            log_error("Failed to add soundsystem to database", exc_info=True, name=name, rave_id=rave_id)

    @staticmethod
    def get_soundsystem(rave_id):
        try:
            cursor.execute('SELECT name FROM soundsystem WHERE rave_id = ?', (rave_id,))
            return cursor.fetchall()
        except Exception as e:
            log_error("Failed to retrieve soundsystem from database", exc_info=True)
            return []
    
    @staticmethod
    def add_lineup(artist_name, rave_id):
        try:
            cursor.execute('''
                INSERT INTO lineup (artist_name, rave_id)
                VALUES (?, ?)
            ''', (artist_name, rave_id))
            conn.commit()
        except Exception as e:
            log_error("Failed to add lineup to database", exc_info=True, artist_name=artist_name, rave_id=rave_id)
    
    @staticmethod
    def get_lineup(rave_id):
        try:
            cursor.execute('SELECT artist_name FROM lineup WHERE rave_id = ?', (rave_id,))
            return cursor.fetchall()
        except Exception as e:
            log_error("Failed to retrieve lineup from database", exc_info=True)
            return []
    
    @staticmethod
    def add_stage(name, rave_id):
        try:
            cursor.execute('''
                INSERT INTO stages (name, rave_id)
                VALUES (?, ?)
            ''', (name, rave_id))
            conn.commit()
        except Exception as e:
            log_error("Failed to add stage to database", exc_info=True, name=name, rave_id=rave_id)
    
    @staticmethod
    def get_stages(rave_id):
        try:
            cursor.execute('SELECT name FROM stages WHERE rave_id = ?', (rave_id,))
            return cursor.fetchall()
        except Exception as e:
            log_error("Failed to retrieve stages from database", exc_info=True)
            return []
    
    @staticmethod
    def add_donation(user_id, amount, element, rave_id):
        try:
            cursor.execute('''
                INSERT INTO donations (user_id, amount, element, rave_id)
                VALUES (?, ?, ?, ?)
            ''', (user_id, amount, element, rave_id))
            conn.commit()
        except Exception as e:
            log_error("Failed to add donation to database", exc_info=True, user_id=user_id, amount=amount, element=element, rave_id=rave_id)
    
    @staticmethod
    def get_donations(rave_id):
        try:
            cursor.execute('SELECT user_id, amount, element FROM donations WHERE rave_id = ?', (rave_id,))
            return cursor.fetchall()
        except Exception as e:
            log_error("Failed to retrieve donations from database", exc_info=True)
            return []
    