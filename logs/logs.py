import logging
import os
import traceback
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
    if exc_info:
        analyze_code(traceback.extract_tb(exc_info[2]))

def log_info(message, **kwargs):
    extra = {key: value for key, value in kwargs.items()}
    logger.info(message, extra=extra)

# Initialize OpenAI client
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_code_context(filename, lineno):
    # Read the file and get the code context around the error line
    with open(filename, 'r') as file:
        lines = file.readlines()
    start = max(lineno - 3, 0)
    end = min(lineno + 2, len(lines))
    code_context = ''.join(lines[start:end])

    return code_context

def analyze_code(traceback_stack):
    for tb in traceback_stack:
        filename = tb.filename
        lineno = tb.lineno
        code_context = get_code_context(filename, lineno)
        response = client.chat_completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI assistant tasked with analyzing code and suggesting fixes."},
                {"role": "user", "content": f"Analyze the following code and provide suggestions to fix the errors:\n\nFile: {filename}\nLine: {lineno}\nCode:\n{code_context}"}
            ]
        )

        analysis = response.choices[0].message.content
        print("AI Code Analysis and Suggestions:")
        print(analysis)
        # Optionally, you can log the analysis to a separate file or the console
        with open("logs/code_analysis.log", "a") as analysis_file:
            analysis_file.write(analysis + "\n")

# Example usage:
# try:
#     # code that might raise an exception
# except Exception as e:
#     log_error("An unexpected error occurred", exc_info=True)
