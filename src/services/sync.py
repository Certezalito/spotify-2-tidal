from src.services.spotify_client import get_saved_albums, get_followed_artists, get_liked_songs, get_playlists
from src.services.tidal_client import find_track, find_album, find_artist
from src.models.log import get_db_session, Log
from src.services.tidal_auth import get_tidal_client
from src.lib.config import load_config
import click
import time
import re
import tidalapi

def clean_html(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def sync_albums():
    """
    Synchronizes the user's saved albums from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    albums = get_saved_albums()
    for album in albums:
        click.echo(f"Syncing album: {album['name']} by {album['artists'][0]['name']}...")
        tidal_album = find_album(tidal_session, album['name'], album['artists'][0]['name'])
        if tidal_album:
            try:
                tidal_session.user.favorites.add_album(tidal_album.id)
                log = Log(item_type='album', item_name=album['name'], artist_name=album['artists'][0]['name'], status='success')
                session.add(log)
                session.commit()
                click.echo(f"Successfully synced album: {album['name']}")
            except Exception as e:
                log = Log(item_type='album', item_name=album['name'], artist_name=album['artists'][0]['name'], status='failure', reason=str(e))
                session.add(log)
                session.commit()
                click.echo(f"Failed to sync album: {album['name']}. Reason: {e}")
        else:
            session.add(log)
            session.commit()
            click.echo(f"Failed to sync album: {album['name']}. Reason: Not found on Tidal")

def sync_artists():
    """
    Synchronizes the user's followed artists from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    artists = get_followed_artists()
    for artist in artists:
        click.echo(f"Syncing artist: {artist['name']}...")
        tidal_artist = find_artist(tidal_session, artist['name'])
        if tidal_artist:
            try:
                tidal_session.user.favorites.add_artist(tidal_artist.id)
                log = Log(item_type='artist', item_name=artist['name'], status='success')
                session.add(log)
                session.commit()
                click.echo(f"Successfully synced artist: {artist['name']}")
            except Exception as e:
                log = Log(item_type='artist', item_name=artist['name'], status='failure', reason=str(e))
                session.add(log)
                session.commit()
                click.echo(f"Failed to sync artist: {artist['name']}. Reason: {e}")
        else:
            log = Log(item_type='artist', item_name=artist['name'], status='failure', reason='Not found on Tidal')
            session.add(log)
            session.commit()
            click.echo(f"Failed to sync artist: {artist['name']}. Reason: Not found on Tidal")

def sync_tracks():
    """
    Synchronizes the user's liked songs from Spotify to Tidal.
    """
    session = get_db_session()
    tidal_session = get_tidal_client()
    tracks = get_liked_songs()
    for track in tracks:
        click.echo(f"Syncing track: {track['name']} by {track['artists'][0]['name']}...")
        isrc = track.get('external_ids', {}).get('isrc')
        tidal_track = find_track(
            tidal_session,
            track['name'],
            track['artists'][0]['name'],
            track['album']['name'],
            track['duration_ms'],
            isrc=isrc
        )
        if tidal_track:
            try:
                # Always add the track if it's found
                tidal_session.user.favorites.add_track(tidal_track.id)
                
                # Log if the track is unavailable
                status = 'success'
                reason = ''
                if not tidal_track.available:
                    status = 'unavailable'
                    reason = 'Track is not available on Tidal'
                
                log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status=status, reason=reason)
                session.add(log)
                session.commit()
                click.echo(f"Successfully synced track: {track['name']}")
            except Exception as e:
                log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='failure', reason=str(e))
                session.add(log)
                session.commit()
                click.echo(f"Failed to sync track: {track['name']}. Reason: {e}")
        else:
            log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='failure', reason='Not found on Tidal by ISRC')
            session.add(log)
            session.commit()
            click.echo(f"Failed to sync track: {track['name']}. Reason: Not found on Tidal by ISRC")

def sync_playlists():
    """
    Synchronizes the user's playlists from Spotify to Tidal.
    """
    config = load_config()
    playlist_folder_name = config.get("TIDAL_PLAYLIST_FOLDER")
    session = get_db_session()
    tidal_session = get_tidal_client()
    
    folder = None
    if playlist_folder_name:
        # Check if the folder already exists
        user_folder = tidal_session.user.folder
        if user_folder and user_folder.name == playlist_folder_name:
            folder = user_folder
        else:
            # Create the folder if it doesn't exist
            folder = tidal_session.user.create_folder(playlist_folder_name)
            click.echo(f"Created Tidal playlist folder: {playlist_folder_name}")

    playlists = get_playlists()
    for playlist in playlists:
        click.echo(f"Syncing playlist: {playlist['name']}...")
        try:
            description = playlist['description'] or ''
            cleaned_description = clean_html(description)
            cleaned_description += f"\\n\\nSynced from Spotify from user {playlist['owner']['display_name']}."
            folder_id = folder.id if folder else None
            new_playlist = tidal_session.user.create_playlist(playlist['name'], cleaned_description, folder_id)
            
            # Revert to per-track ISRC search
            track_ids = []
            items = playlist['tracks']['items']
            for i, item in enumerate(items):
                track = item['track']
                if not track:
                    continue
                try:
                    click.echo(f"  ({i+1}/{len(items)}) Searching for track: {track['name']} by {track['artists'][0]['name']}...")
                    isrc = track.get('external_ids', {}).get('isrc')
                    tidal_track = find_track(
                        tidal_session,
                        track['name'],
                        track['artists'][0]['name'],
                        track['album']['name'],
                        track['duration_ms'],
                        isrc=isrc
                    )
                    if tidal_track:
                        track_ids.append(tidal_track.id)
                        if not tidal_track.available:
                            log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='unavailable', reason='Track is not available on Tidal')
                            session.add(log)
                            session.commit()
                    else:
                        log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='failure', reason='Not found on Tidal by ISRC')
                        session.add(log)
                        session.commit()
                except Exception as exc:
                    click.echo(f"  Error searching for track: {track['name']}. Reason: {repr(exc)}")
                    log = Log(item_type='track', item_name=track['name'], artist_name=track['artists'][0]['name'], album_name=track['album']['name'], status='failure', reason=str(exc))
                    session.add(log)
                    session.commit()
                time.sleep(0.5)

            if track_ids:
                click.echo(f"Adding {len(track_ids)} tracks to playlist: {playlist['name']}...")
                new_playlist.add(track_ids)
            
            log = Log(item_type='playlist', item_name=playlist['name'], status='success')
            session.add(log)
            session.commit()
            click.echo(f"Successfully synced playlist: {playlist['name']}")
        except Exception as e:
            log = Log(item_type='playlist', item_name=playlist['name'], status='failure', reason=str(e))
            session.add(log)
            session.commit()
            click.echo(f"Failed to sync playlist: {playlist['name']}. Reason: {e}")
