from dotenv import load_dotenv
import os

def load_config():
    """
    Loads environment variables from a .env file.
    """
    load_dotenv()
    return {
        "TIDAL_PLAYLIST_FOLDER": os.getenv("TIDAL_PLAYLIST_FOLDER"),
    }
