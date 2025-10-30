import click
from ..lib.config import load_config
from ..services.sync import sync_albums as _sync_albums, sync_artists as _sync_artists, sync_tracks as _sync_tracks, sync_playlists as _sync_playlists
from ..lib.logger import logger
from ..services.tidal_auth import get_tidal_client
import time

@click.group()
def cli():
    """
    A command-line tool to synchronize your Spotify music library to your Tidal account.
    """
    load_config()

@cli.command()
@click.option('--sync-albums', is_flag=True, help='Synchronize saved albums only.')
@click.option('--sync-artists', is_flag=True, help='Synchronize followed artists only.')
@click.option('--sync-tracks', is_flag=True, help='Synchronize liked songs only.')
@click.option('--sync-playlists', is_flag=True, help='Synchronize playlists only.')
def sync(sync_albums, sync_artists, sync_tracks, sync_playlists):
    """
    Synchronize your Spotify music library to your Tidal account.

    By default, this command will synchronize all music data. You can use the flags to synchronize specific types of data.
    """
    start_time = time.time()
    tidal_session = get_tidal_client()
    if not tidal_session:
        logger.error("Failed to authenticate with Tidal. Aborting.")
        return

    if not any([sync_albums, sync_artists, sync_tracks, sync_playlists]):
        logger.info("Synchronizing all music data...")
        _sync_albums(tidal_session)
        _sync_artists(tidal_session)
        _sync_tracks(tidal_session)
        _sync_playlists(tidal_session)
        logger.info("Synchronization complete.")
    else:
        if sync_albums:
            logger.info("Synchronizing albums...")
            _sync_albums(tidal_session)
        if sync_artists:
            logger.info("Synchronizing artists...")
            _sync_artists(tidal_session)
        if sync_tracks:
            logger.info("Synchronizing tracks...")
            _sync_tracks(tidal_session)
        if sync_playlists:
            logger.info("Synchronizing playlists...")
            _sync_playlists(tidal_session)
        logger.info("Selective synchronization complete.")
    
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"Total API communication time: {duration:.2f} seconds.")

if __name__ == '__main__':
    cli()
