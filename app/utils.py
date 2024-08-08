import os
import json
from logs.logs import log_error

def load_env_vars():
    """
    Load environment variables from Replit secrets.
    """
    required_vars = ["TELEGRAM_BOT_TOKEN", "GROUP_CHAT_ID", "VERIFICATION_CHAT_ID", "OPENAI_API_KEY", "WEBHOOK_URL"]
    missing_vars = [var for var in required_vars if var not in os.environ]

    if missing_vars:
        log_error(f"Missing required environment variables: {', '.join(missing_vars)}")
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    print("Loaded environment variables from Replit secrets")

def read_json(file_path):
    """
    Read and return data from a JSON file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        log_error(f"File {file_path} not found.")
        raise FileNotFoundError(f"File {file_path} not found.")

def write_json(file_path, data):
    """
    Write data to a JSON file.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        log_error(f"Failed to write data to {file_path}", exc_info=True)
        raise e

def validate_date(date_str):
    """
    Validate date format (example: YYYY-MM-DD).
    """
    import re
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(date_pattern, date_str):
        return True
    else:
        return False

def validate_bpm(bpm):
    """
    Validate that BPM is a positive integer.
    """
    if isinstance(bpm, int) and bpm > 0:
        return True
    else:
        return False

def validate_soundsystem(soundsystem):
    """
    Validate that soundsystem is a non-empty list.
    """
    if isinstance(soundsystem, list) and len(soundsystem) > 0:
        return True
    else:
        return False

def validate_lineup(lineup):
    """
    Validate that lineup is a non-empty list.
    """
    if isinstance(lineup, list) and len(lineup) > 0:
        return True
    else:
        return False

def validate_participants(participants):
    """
    Validate that participants is a non-empty list.
    """
    if isinstance(participants, list) and len(participants) > 0:
        return True
    else:
        return False
