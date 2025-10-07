import os
import tidalapi

def get_tidal_client():
    """
    Returns a Tidal API client object.
    """
    session = tidalapi.Session()
    session.login_oauth_simple(
        client_id=os.getenv("TIDAL_CLIENT_ID"),
        client_secret=os.getenv("TIDAL_CLIENT_SECRET"),
    )
    return session
