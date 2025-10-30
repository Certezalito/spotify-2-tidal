import logging
from src.lib.config import load_config

class SpotifyRateLimitFilter(logging.Filter):
    """A logging filter to clarify Spotify rate limit warnings."""
    def filter(self, record):
        if 'Your application has reached a rate/request limit' in record.getMessage():
            record.msg = f"Spotify API rate limit reached. {record.msg}"
        return True

def setup_logger():
    """
    Sets up the root logger to output to both the console and a file,
    and to filter for Spotify rate limit messages.
    """
    config = load_config()
    log_file = config.get("LOG_FILE", "sync.log")

    # Get the root logger to capture logs from all libraries
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear any existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create handlers for file and console
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    # Create a formatter and apply it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Add our custom filter to clarify Spotify messages
    logger.addFilter(SpotifyRateLimitFilter())

    return logger

logger = setup_logger()
