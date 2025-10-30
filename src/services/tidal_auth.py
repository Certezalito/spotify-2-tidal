import tidalapi
import os
from src.lib.config import load_config
import json
import click
import threading
import webbrowser

_auth_lock = threading.Lock()

def get_tidal_client():
    """
    Returns an authenticated Tidal client using the Authorization Code Flow.
    """
    with _auth_lock:
        config = load_config()
        session_file = config.get("TIDAL_SESSION_FILE", "tidal_session.json")

        session = tidalapi.Session()
        session.client_id = config.get("TIDAL_CLIENT_ID")
        session.client_secret = config.get("TIDAL_CLIENT_SECRET")

        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    session.load_oauth_session(
                        session_id=session_data['session_id'],
                        token_type=session_data['token_type'],
                        access_token=session_data['access_token'],
                        refresh_token=session_data['refresh_token']
                    )
            except Exception as e:
                click.echo(f"Could not load session from file: {e}. Re-authenticating.")
                os.remove(session_file)

        if not session.check_login():
            click.echo("Tidal authentication required. A browser window will open for you to log in.")

            # login_oauth returns a LinkLogin and a Future which completes when the login is done
            link_login, future = session.login_oauth()

            # Open the verification URL in the user's browser. Use the complete URL if available.
            try:
                verification = getattr(link_login, 'verification_uri_complete', None) or getattr(link_login, 'verification_uri', None)
                if verification:
                    # verification may already include https://
                    if not verification.startswith('http'):
                        verification = f"https://{verification}"
                    webbrowser.open(verification)
                else:
                    click.echo(f"Open this URL to continue login: {link_login}")
            except Exception:
                click.echo("Please open the link provided by Tidal to authenticate:")
                click.echo(str(link_login))

            # Wait for the login future to complete (this will return when the device/link flow is finished)
            try:
                future.result()
            except Exception as e:
                click.echo(f"Tidal login failed: {e}")
                return None

            # After successful login, save the session
            if session.check_login():
                try:
                    with open(session_file, 'w') as f:
                        json.dump({
                            'session_id': session.session_id,
                            'token_type': session.token_type,
                            'access_token': session.access_token,
                            'refresh_token': session.refresh_token,
                        }, f)
                    click.echo("Tidal session saved.")
                except Exception as e:
                    click.echo(f"Could not save Tidal session: {e}")
            else:
                click.echo("Failed to log in to Tidal.")
                return None

        return session
