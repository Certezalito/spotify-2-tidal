import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    """
    Returns a Spotipy client object.
    """
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=scope,
    )
    return spotipy.Spotify(auth_manager=auth_manager)
