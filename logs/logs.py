import logging
import os
from openai import OpenAI

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s at line %(lineno)d: %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()  # Also log to console
    ]
)

# Root logger for general logging
logger = logging.getLogger(__name__)

# Separate logger for errors
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)

# Add formatter to include detailed information
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s at line %(lineno)d: %(message)s')
error_handler.setFormatter(formatter)
error_logger.addHandler(error_handler)

def log_error(message, exc_info=True, **kwargs):
    extra = {key: value for key, value in kwargs.items()}
    error_logger.error(message, exc_info=exc_info, extra=extra)

# Initialize OpenAI client
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_logs(log_file_path):
    with open(log_file_path, 'r') as file:
        logs = file.read()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an AI assistant tasked with analyzing error logs and suggesting fixes."},
            {"role": "user", "content": f"Analyze the following logs and provide suggestions to fix the errors:\n\n{logs}"}
        ]
    )

    analysis = response.choices[0].message.content
    print("AI Analysis and Suggestions:")
    print(analysis)

# Example usage:
analyze_logs("logs/error.log")
