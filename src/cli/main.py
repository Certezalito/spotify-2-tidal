import click
from ..lib.config import load_config
from ..services.sync import sync_albums as _sync_albums, sync_artists as _sync_artists, sync_tracks as _sync_tracks, sync_playlists as _sync_playlists
import logging

class SpotifyRateLimitFilter(logging.Filter):
    def filter(self, record):
        if 'Your application has reached a rate/request limit' in record.getMessage():
            record.msg = f"Spotify API rate limit reached. {record.msg}"
        return True

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(name)s:%(message)s')
logging.getLogger().addFilter(SpotifyRateLimitFilter())

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
    if not any([sync_albums, sync_artists, sync_tracks, sync_playlists]):
        click.echo("Synchronizing all music data...")
        _sync_albums()
        _sync_artists()
        _sync_tracks()
        _sync_playlists()
        click.echo("Synchronization complete.")
    else:
        if sync_albums:
            click.echo("Synchronizing albums...")
            _sync_albums()
        if sync_artists:
            click.echo("Synchronizing artists...")
            _sync_artists()
        if sync_tracks:
            click.echo("Synchronizing tracks...")
            _sync_tracks()
        if sync_playlists:
            click.echo("Synchronizing playlists...")
            _sync_playlists()
        click.echo("Selective synchronization complete.")

if __name__ == '__main__':
    cli()
