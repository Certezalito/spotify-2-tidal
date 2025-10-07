from src.services.spotify_client import get_saved_albums, get_followed_artists, get_liked_songs, get_playlists
from src.services.tidal_client import find_track, find_album, find_artist
from src.models.log import get_db_session, Log
from src.services.tidal_auth import get_tidal_client

def sync_albums():
    """
    Synchronizes the user's saved albums from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    albums = get_saved_albums()
    for album in albums:
        tidal_album = find_album(album['name'], album['artists'][0]['name'])
        if tidal_album:
            try:
                tidal_session.user.library.add_album(tidal_album.id)
                log = Log(item_type='album', item_name=album['name'], artist_name=album['artists'][0]['name'], status='success')
                session.add(log)
                session.commit()
            except Exception as e:
                log = Log(item_type='album', item_name=album['name'], artist_name=album['artists'][0]['name'], status='failure', reason=str(e))
                session.add(log)
                session.commit()
        else:
            log = Log(item_type='album', item_name=album['name'], artist_name=album['artists'][0]['name'], status='failure', reason='Not found on Tidal')
            session.add(log)
            session.commit()

def sync_artists():
    """
    Synchronizes the user's followed artists from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    artists = get_followed_artists()
    for artist in artists:
        tidal_artist = find_artist(artist['name'])
        if tidal_artist:
            try:
                tidal_session.user.library.add_artist(tidal_artist.id)
                log = Log(item_type='artist', item_name=artist['name'], status='success')
                session.add(log)
                session.commit()
            except Exception as e:
                log = Log(item_type='artist', item_name=artist['name'], status='failure', reason=str(e))
                session.add(log)
                session.commit()
        else:
            log = Log(item_type='artist', item_name=artist['name'], status='failure', reason='Not found on Tidal')
            session.add(log)
            session.commit()

def sync_tracks():
    """
    Synchronizes the user's liked songs from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    tracks = get_liked_songs()
    for track in tracks:
        tidal_track = find_track(track['name'], track['artists'][0]['name'], track['album']['name'])
        if tidal_track:
            try:
                tidal_session.user.library.add_track(tidal_track.id)
                log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='success')
                session.add(log)
                session.commit()
            except Exception as e:
                log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='failure', reason=str(e))
                session.add(log)
                session.commit()
        else:
            log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='failure', reason='Not found on Tidal')
            session.add(log)
            session.commit()

def sync_playlists():
    """
    Synchronizes the user's playlists from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    playlists = get_playlists()
    for playlist in playlists:
        try:
            new_playlist = tidal_session.user.create_playlist(playlist['name'], playlist['description'])
            track_ids = []
            for item in playlist['tracks']['items']:
                track = item['track']
                tidal_track = find_track(track['name'], track['artists'][0]['name'], track['album']['name'])
                if tidal_track:
                    track_ids.append(tidal_track.id)
            new_playlist.add(track_ids)
            log = Log(item_type='playlist', item_name=playlist['name'], status='success')
            session.add(log)
            session.commit()
        except Exception as e:
            log = Log(item_type='playlist', item_name=playlist['name'], status='failure', reason=str(e))
            session.add(log)
            session.commit()
