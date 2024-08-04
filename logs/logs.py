import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s at line %(lineno)d: %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.FileHandler("logs/error.log")
    ]
)

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
