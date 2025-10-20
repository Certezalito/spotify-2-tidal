import tidalapi
import os
from src.lib.config import load_config
import json
import click
import threading

_auth_lock = threading.Lock()

def get_tidal_client():
    """
    Returns an authenticated Tidal client.
    """
    with _auth_lock:
        config = load_config()
        session_file = config.get("TIDAL_SESSION_FILE", "tidal_session.json")

        # Correctly configure the tidalapi session
        tidal_config = tidalapi.Config()
        tidal_config.api_token = config.get("TIDAL_CLIENT_ID")
        tidal_config.api_secret = config.get("TIDAL_CLIENT_SECRET")
        
        session = tidalapi.Session(config=tidal_config)

        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    session.load_oauth_session(session_data['session_id'], session_data['token_type'], session_data['access_token'], session_data['refresh_token'])
            except Exception as e:
                if '401' in str(e):
                    click.echo("Invalid Tidal session file. Re-authentication is required.")
                    os.remove(session_file)
                    # Re-initialize the session with the correct config
                    session = tidalapi.Session(config=tidal_config)
                else:
                    raise e

        if not session.check_login():
            click.echo("Tidal authentication required. The sync process will pause.")
            click.echo("Please follow the instructions to log in...")
            session.login_oauth_simple()
            if session.check_login():
                # Manually save the session
                with open(session_file, 'w') as f:
                    json.dump({
                        'session_id': session.session_id,
                        'token_type': session.token_type,
                        'access_token': session.access_token,
                        'refresh_token': session.refresh_token,
                    }, f)
                click.echo("Tidal session saved.")
            else:
                click.echo("Failed to log in to Tidal.")
                return None

        return session
