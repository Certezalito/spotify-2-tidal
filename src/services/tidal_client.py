from src.services.tidal_auth import get_tidal_client
import tidalapi

def find_track(title, artist, album):
    """
    Finds a track on Tidal using its metadata.
    """
    session = get_tidal_client()
    results = session.search(query=f"{title} {artist} {album}", models=[tidalapi.media.Track])
    if results['tracks']:
        return results['tracks'][0]
    return None

def find_album(title, artist):
    """
    Finds an album on Tidal using its metadata.
    """
    session = get_tidal_client()
    results = session.search(query=f"{title} {artist}", models=[tidalapi.media.Album])
    if results['albums']:
        return results['albums'][0]
    return None

def find_artist(name):
    """
    Finds an artist on Tidal using their name.
    """
    session = get_tidal_client()
    results = session.search(query=name, models=[tidalapi.media.Artist])
    if results['artists']:
        return results['artists'][0]
    return None
