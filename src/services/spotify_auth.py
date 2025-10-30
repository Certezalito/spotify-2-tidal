import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.lib.config import load_config

def get_spotify_client():
    """
    Returns a Spotipy client object.
    """
    config = load_config()
    scope = "user-library-read playlist-read-private user-follow-read"
    auth_manager = SpotifyOAuth(
        client_id=config.get("SPOTIFY_CLIENT_ID"),
        client_secret=config.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=config.get("SPOTIFY_REDIRECT_URI"),
        scope=scope,
    )
    return spotipy.Spotify(
        auth_manager=auth_manager,
        requests_timeout=config.get("API_TIMEOUT", 30)
    )
