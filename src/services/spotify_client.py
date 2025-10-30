from src.services.spotify_auth import get_spotify_client
import click
import time

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
            time.sleep(0.5)
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
            time.sleep(0.5)
        else:
            results = None
    return artists

def get_liked_songs():
    """
    Returns a list of the user's liked songs.
    """
    sp = get_spotify_client()
    
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return [item['track'] for item in tracks]

def get_playlists():
    """
    Returns a list of the user's playlists.
    """
    sp = get_spotify_client()
    playlists = []
    results = sp.current_user_playlists()
    while results:
        for playlist_summary in results['items']:
            # Fetch the full playlist details, but not the tracks yet
            playlist = sp.playlist(playlist_summary['id'], fields="id,name,description,owner.display_name")

            # Fetch the tracks separately using manual offset-based pagination for robustness
            all_track_items = []
            limit = 50  # Using a smaller limit can sometimes be more reliable
            offset = 0
            while True:
                try:
                    tracks_results = sp.playlist_tracks(
                        playlist['id'],
                        fields="items(track(name,artists,album(name),external_ids,duration_ms,is_playable)),next",
                        limit=limit,
                        offset=offset
                    )
                    
                    if not tracks_results or not tracks_results.get('items'):
                        break  # No more tracks

                    all_track_items.extend(tracks_results['items'])
                    
                    if tracks_results.get('next'):
                        offset += limit
                        time.sleep(0.5)
                    else:
                        break  # No more pages
                except Exception as e:
                    click.echo(f"Error fetching page of tracks for playlist {playlist['name']} at offset {offset}: {e}")
                    break
            
            playlist['tracks'] = {'items': all_track_items}
            playlists.append(playlist)

        if results['next']:
            results = sp.next(results)
            time.sleep(0.5)
        else:
            results = None
    return playlists
