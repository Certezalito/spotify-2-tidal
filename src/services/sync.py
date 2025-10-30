from src.services.spotify_client import get_saved_albums, get_followed_artists, get_liked_songs, get_playlists
from src.services.tidal_client import find_track, find_album, find_artist
from src.lib.logger import logger
from src.lib.config import load_config
import time
import re
import tidalapi

def clean_html(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def sync_albums(tidal_session):
    """
    Synchronizes the user's saved albums from Spotify to Tidal.
    """
    albums = get_saved_albums()
    for album in albums:
        logger.info(f"Syncing album: {album['name']} by {album['artists'][0]['name']}...")
        try:
            tidal_album = find_album(tidal_session, album['name'], album['artists'][0]['name'])
            if tidal_album:
                try:
                    tidal_session.user.favorites.add_album(tidal_album.id)
                    logger.info(f"Successfully synced album: {album['name']}")
                except Exception as e:
                    logger.error(f"Failed to sync album: {album['name']}. Reason: {e}")
            else:
                logger.error(f"Failed to sync album: {album['name']}. Reason: Not found on Tidal")
        except Exception as e:
            if '429' in str(e):
                logger.error(f"Tidal API rate limit reached while syncing album: {album['name']}")
            else:
                logger.error(f"An error occurred while syncing album: {album['name']}. Reason: {e}")

def sync_artists(tidal_session):
    """
    Synchronizes the user's followed artists from Spotify to Tidal.
    """
    artists = get_followed_artists()
    for artist in artists:
        logger.info(f"Syncing artist: {artist['name']}...")
        try:
            tidal_artist = find_artist(tidal_session, artist['name'])
            if tidal_artist:
                try:
                    tidal_session.user.favorites.add_artist(tidal_artist.id)
                    logger.info(f"Successfully synced artist: {artist['name']}")
                except Exception as e:
                    logger.error(f"Failed to sync artist: {artist['name']}. Reason: {e}")
            else:
                logger.error(f"Failed to sync artist: {artist['name']}. Reason: Not found on Tidal")
        except Exception as e:
            if '429' in str(e):
                logger.error(f"Tidal API rate limit reached while syncing artist: {artist['name']}")
            else:
                logger.error(f"An error occurred while syncing artist: {artist['name']}. Reason: {e}")

def sync_tracks(tidal_session):
    """
    Synchronizes the user's liked songs from Spotify to Tidal.
    """
    tracks = get_liked_songs()
    for track in tracks:
        logger.info(f"Syncing track: {track['name']} by {track['artists'][0]['name']}...")
        isrc = track.get('external_ids', {}).get('isrc')
        try:
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
                    if not tidal_track.available:
                        logger.warning(f"Track '{track['name']}' (ISRC: {isrc}) is not available on Tidal, but has been added to your library.")
                    
                    logger.info(f"Successfully synced track: {track['name']} (ISRC: {isrc})")
                except Exception as e:
                    logger.error(f"Failed to sync track: {track['name']} (ISRC: {isrc}). Reason: {e}")
            else:
                logger.error(f"Failed to sync track: {track['name']} (ISRC: {isrc}). Reason: Not found on Tidal by ISRC")
        except Exception as e:
            if '429' in str(e):
                logger.error(f"Tidal API rate limit reached while syncing track: {track['name']}")
            else:
                logger.error(f"An error occurred while syncing track: {track['name']}. Reason: {e}")

def sync_playlists(tidal_session):
    """
    Synchronizes the user's playlists from Spotify to Tidal.
    """
    config = load_config()
    playlist_folder_name = config.get("TIDAL_PLAYLIST_FOLDER")
    
    folder = None
    if playlist_folder_name:
        try:
            # Check if the folder already exists
            user_folder = tidal_session.user.folder
            if user_folder and user_folder.name == playlist_folder_name:
                folder = user_folder
            else:
                # Create the folder if it doesn't exist
                folder = tidal_session.user.create_folder(playlist_folder_name)
                logger.info(f"Created Tidal playlist folder: {playlist_folder_name}")
        except Exception as e:
            if '429' in str(e):
                logger.error(f"Tidal API rate limit reached while creating playlist folder.")
            else:
                logger.error(f"An error occurred while creating playlist folder. Reason: {e}")

    playlists = get_playlists()
    for playlist in playlists:
        logger.info(f"Syncing playlist: {playlist['name']}...")
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
                    isrc = track.get('external_ids', {}).get('isrc')
                    logger.info(f"  ({i+1}/{len(items)}) Searching for track: {track['name']} by {track['artists'][0]['name']} (ISRC: {isrc})...")
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
                            logger.warning(f"Track '{track['name']}' (ISRC: {isrc}) is not available on Tidal, but has been added to the playlist.")
                    else:
                        logger.error(f"Failed to find track '{track['name']}' (ISRC: {isrc}) on Tidal by ISRC.")
                except Exception as exc:
                    if '429' in str(exc):
                        logger.error(f"Tidal API rate limit reached while searching for track: {track['name']}")
                    else:
                        logger.error(f"  Error searching for track: {track['name']} (ISRC: {isrc}). Reason: {repr(exc)}")
                time.sleep(0.5)

            if track_ids:
                logger.info(f"Adding {len(track_ids)} tracks to playlist: {playlist['name']}...")
                new_playlist.add(track_ids)
            
            logger.info(f"Successfully synced playlist: {playlist['name']}")
        except Exception as e:
            if '429' in str(e):
                logger.error(f"Tidal API rate limit reached while syncing playlist: {playlist['name']}")
            else:
                logger.error(f"Failed to sync playlist: {playlist['name']}. Reason: {e}")
