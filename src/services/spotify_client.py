from src.services.spotify_auth import get_spotify_client

def get_saved_albums():
    """
    Returns a list of the user's saved albums.
    """
    sp = get_spotify_client()
    results = sp.current_user_saved_albums()
    albums = []
    while results:
        for item in results['items']:
            albums.append(item['album'])
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return albums

def get_followed_artists():
    """
    Returns a list of the user's followed artists.
    """
    sp = get_spotify_client()
    results = sp.current_user_followed_artists()
    artists = []
    while results:
        for item in results['artists']['items']:
            artists.append(item)
        if results['artists']['next']:
            results = sp.next(results['artists'])
        else:
            results = None
    return artists

def get_liked_songs():
    """
    Returns a list of the user's liked songs.
    """
    sp = get_spotify_client()
    results = sp.current_user_saved_tracks()
    tracks = []
    while results:
        for item in results['items']:
            tracks.append(item['track'])
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return tracks

def get_playlists():
    """
    Returns a list of the user's playlists.
    """
    sp = get_spotify_client()
    results = sp.current_user_playlists()
    playlists = []
    while results:
        for item in results['items']:
            playlists.append(item)
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return playlists
