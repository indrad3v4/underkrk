import sqlite3
import os
from openai import OpenAI
from logs.logs import log_error, log_info

# Connect to SQLite database (create if not exists)
conn = sqlite3.connect('raves.db')
cursor = conn.cursor()

# Initialize OpenAI client
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Create table for participants if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    verification_link TEXT
)
''')
conn.commit()

def analyze_data_and_optimize():
    try:
        cursor.execute('SELECT * FROM raves')
        raves = cursor.fetchall()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI assistant that analyzes rave data and provides optimization suggestions."},
                {"role": "user", "content": f"Analyze the following rave data and provide suggestions for optimization:\n\n{raves}"}
            ]
        )
        analysis = response.choices[0].message.content
        log_info("AI Analysis and Suggestions:")
        log_info(analysis)
        # Implement suggested optimizations (this part would depend on the specific suggestions provided by AI)
    except Exception as e:
        log_error("Failed to analyze and optimize rave data", exc_info=True)

def add_rave(insight, name, location, date, style, bpm, soundsystem=None, lineup=None, participants=None, stages=None, donations=None):
    try:
        cursor.execute('''
            INSERT INTO raves (insight, name, location, date, style, bpm, soundsystem, lineup, participants, stages, donations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            insight, name, location, date, style, bpm,
            json.dumps(soundsystem) if soundsystem else json.dumps([]),
            json.dumps(lineup) if lineup else json.dumps([]),
            json.dumps(participants) if participants else json.dumps([]),
            json.dumps(stages) if stages else json.dumps(["Main Stage"]),
            json.dumps(donations) if donations else json.dumps([])
        ))
        conn.commit()
        analyze_data_and_optimize()
    except Exception as e:
        log_error("Failed to add rave to database", exc_info=True, insight=insight, name=name, location=location, date=date, style=style, bpm=bpm)

def add_participant(user_id, role, verification_link):
    try:
        cursor.execute('''
            INSERT INTO participants (user_id, role, verification_link)
            VALUES (?, ?, ?)
        ''', (user_id, role, verification_link))
        conn.commit()
        analyze_data_and_optimize()
    except Exception as e:
        log_error("Failed to add participant to database", exc_info=True, user_id=user_id, role=role, verification_link=verification_link)

def update_participant(user_id, role=None, verification_link=None):
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
        conn.commit()
        analyze_data_and_optimize()
    except Exception as e:
        log_error("Failed to update participant in database", exc_info=True, user_id=user_id, role=role, verification_link=verification_link)

def get_participants():
    try:
        cursor.execute('SELECT * FROM participants')
        return cursor.fetchall()
    except Exception as e:
        log_error("Failed to retrieve participants from database", exc_info=True)
        return []

def load_rave(rave_id):
    try:
        cursor.execute('SELECT * FROM raves WHERE id = ?', (rave_id,))
        row = cursor.fetchone()
        if row:
            return {
                "insight": row[1], "name": row[2], "location": row[3], "date": row[4],
                "style": row[5], "bpm": row[6], "soundsystem": json.loads(row[7]),
                "lineup": json.loads(row[8]), "participants": json.loads(row[9]),
                "stages": json.loads(row[10]), "donations": json.loads(row[11])
            }
    except Exception as e:
        log_error("Failed to load rave from database", exc_info=True, rave_id=rave_id)
    return None

def load_all_raves():
    try:
        cursor.execute('SELECT * FROM raves')
        rows = cursor.fetchall()
        return [
            {
                "insight": row[1], "name": row[2], "location": row[3], "date": row[4],
                "style": row[5], "bpm": row[6], "soundsystem": json.loads(row[7]),
                "lineup": json.loads(row[8]), "participants": json.loads(row[9]),
                "stages": json.loads(row[10]), "donations": json.loads(row[11])
            } for row in rows
        ]
    except Exception as e:
        log_error("Failed to load raves from database", exc_info=True)
        return []
