from src.services.tidal_auth import get_tidal_client
import tidalapi
from tidalapi import artist
from thefuzz import fuzz

def find_track(session, title, artist, album, duration_ms, isrc=None):
    """
    Finds a track on Tidal using its ISRC or metadata, with improved fallback searching and fuzzy matching.
    """
    # 1. Prioritize searching by ISRC if available
    if isrc:
        try:
            results = session.search(query=f"isrc:{isrc}", models=[tidalapi.media.Track])
            if results.get('tracks'):
                return results['tracks'][0]
        except Exception:
            pass  # Ignore ISRC search errors and proceed to metadata search

    # 2. Fallback to searching by metadata with a sequence of queries
    search_queries = [
        f'{title} {artist}',
        f'{title} {album}',
        title,
    ]
    
    best_match = None
    highest_score = 0

    for query in search_queries:
        try:
            results = session.search(query=query, models=[tidalapi.media.Track])
            if results.get('tracks'):
                for tidal_track in results['tracks']:
                    # Calculate a similarity score using a more robust fuzzy matching algorithm
                    title_ratio = fuzz.token_set_ratio(title.lower(), tidal_track.name.lower())
                    artist_ratio = fuzz.token_set_ratio(artist.lower(), tidal_track.artist.name.lower())
                    
                    # Factor in the duration difference
                    duration_diff = abs(duration_ms - (tidal_track.duration * 1000))
                    duration_score = max(0, 100 - (duration_diff / 1000)) # Penalize large duration differences
                    
                    # Weighted score with duration
                    score = (title_ratio * 0.5) + (artist_ratio * 0.3) + (duration_score * 0.2)

                    if score > highest_score:
                        highest_score = score
                        best_match = tidal_track
        except Exception:
            pass # Ignore search errors for a query and try the next one
    
    # 3. Return the best match if it meets a certain threshold
    if highest_score > 85: # Threshold can be adjusted
        return best_match
    
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
