import click
from src.lib.config import load_config
from src.services.sync import sync_albums, sync_artists, sync_tracks, sync_playlists

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
        sync_albums()
        sync_artists()
        sync_tracks()
        sync_playlists()
        click.echo("Synchronization complete.")
    else:
        if sync_albums:
            click.echo("Synchronizing albums...")
            sync_albums()
        if sync_artists:
            click.echo("Synchronizing artists...")
            sync_artists()
        if sync_tracks:
            click.echo("Synchronizing tracks...")
            sync_tracks()
        if sync_playlists:
            click.echo("Synchronizing playlists...")
            sync_playlists()
        click.echo("Selective synchronization complete.")

if __name__ == '__main__':
    cli()
