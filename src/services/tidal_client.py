from src.services.tidal_auth import get_tidal_client
import tidalapi
from tidalapi import artist

def find_track(session, title, artist, album, duration_ms, isrc=None):
    """
    Finds a track on Tidal using its ISRC only.
    """
    if isrc:
        tracks = session.get_tracks_by_isrc(isrc)
        if tracks:
            return tracks[0]
    return None

def find_album(session, title, artist):
    """
    Finds an album on Tidal using its metadata.
    """
    results = session.search(query=f"{title} {artist}", models=[tidalapi.media.Album])
    if results['albums']:
        return results['albums'][0]
    return None

def find_artist(session, name):
    """
    Finds an artist on Tidal using their name.
    """
    results = session.search(query=name, models=[tidalapi.artist.Artist])
    if results['artists']:
        return results['artists'][0]
    return None
