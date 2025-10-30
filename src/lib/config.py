from dotenv import load_dotenv
import os

def load_config():
    """
    Loads environment variables from a .env file.
    """
    load_dotenv()
    return {
        "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
        "SPOTIFY_CLIENT_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "SPOTIFY_REDIRECT_URI": os.getenv("SPOTIFY_REDIRECT_URI"),
        "TIDAL_CLIENT_ID": os.getenv("TIDAL_CLIENT_ID"),
        "TIDAL_CLIENT_SECRET": os.getenv("TIDAL_CLIENT_SECRET"),
        "TIDAL_PLAYLIST_FOLDER": os.getenv("TIDAL_PLAYLIST_FOLDER"),
        "TIDAL_SESSION_FILE": os.getenv("TIDAL_SESSION_FILE"),
        "LOG_FILE": os.getenv("LOG_FILE"),
        "API_TIMEOUT": int(os.getenv("API_TIMEOUT", 30)),
    }
