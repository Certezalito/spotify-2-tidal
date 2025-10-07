from src.models.log import get_db_session, Log

def log_sync(item_type, item_name, artist_name, album_name, status, reason=None):
    """
    Logs a synchronization attempt to the database.
    """
    session = get_db_session()
    log = Log(
        item_type=item_type,
        item_name=item_name,
        artist_name=artist_name,
        album_name=album_name,
        status=status,
        reason=reason,
    )
    session.add(log)
    session.commit()
