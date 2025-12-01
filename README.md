# Spotify 2 Tidal Music Library Sync

A command-line tool to synchronize your Spotify music library—including saved albums, artists, tracks, and playlists—to your Tidal account.

## Features

- **Full and Selective Sync**: Synchronize your entire library or choose specific types of content (albums, artists, tracks, playlists).
- **ISRC Matching**: Uses ISRC codes for accurate track matching.
- **Session Caching**: Caches your Tidal session to avoid re-authenticating on every run.
- **Logging**: Provides real-time feedback in the console and saves a detailed log to a file.

## Installation

This project uses `uv` for fast environment and dependency management. You can install it with:
```bash
pip install uv
```

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Certezalito/spotify-2-tidal.git
    cd spotify-2-tidal
    ```

2.  **Create and activate a virtual environment with `uv`**:
    ```bash
    uv venv
    ```

3.  **Install dependencies with `uv`**:
    ```bash
    uv pip install -r requirements.txt
    ```


## Configuration

Before you can use the tool, you need to configure your API credentials and settings in a `.env` file.

1.  **Create a `.env` file** in the root of the project.

2.  **Add your configuration** to the `.env` file. Below is an explanation of each variable:

    ```
    # Spotify API Credentials
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback

    # Tidal API Credentials
    TIDAL_CLIENT_ID=your_tidal_client_id
    TIDAL_CLIENT_SECRET=your_tidal_client_secret

    # Application Settings
    TIDAL_PLAYLIST_FOLDER=synced_from_spotify
    TIDAL_SESSION_FILE=tidal_session.json
    LOG_FILE=sync.log
    API_TIMEOUT=30
    ```

### Configuration Details

-   **`SPOTIFY_CLIENT_ID`** & **`SPOTIFY_CLIENT_SECRET`**: Your Spotify application's credentials. These are required to access the Spotify API.
-   **`SPOTIFY_REDIRECT_URI`**: The callback URL for Spotify's authentication. This must match the one you set in your Spotify Developer Dashboard.

-   **`TIDAL_CLIENT_ID`** & **`TIDAL_CLIENT_SECRET`**: Your Tidal application's credentials. These are required to access the Tidal API.

-   **`TIDAL_PLAYLIST_FOLDER`**: The name of the folder that will be created in your Tidal account to store the synced playlists.
-   **`TIDAL_SESSION_FILE`**: The name of the file used to cache your Tidal login session. This prevents you from having to re-authenticate every time you run the tool.
-   **`LOG_FILE`**: The name of the file where all synchronization activity will be logged.
-   **`API_TIMEOUT`**: The number of seconds the application will wait for a response from the Spotify or Tidal APIs before timing out.

### How to Obtain API Credentials

-   **Spotify**:
    1.  Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    2.  Create a new application.
    3.  Copy the `Client ID` and `Client Secret`.
    4.  In the application settings, add `http://127.0.0.1:8888/callback` as a "Redirect URI".

-   **Tidal**:
    1.  Go to the [Tidal Developer Portal](https://developer.tidal.com/).
    2.  Create a new application.
    3.  Copy the `Client ID` and `Client Secret` into your `.env` file.

## Usage

Make sure your virtual environment is activated before running any commands.

### Full Synchronization

To synchronize your entire Spotify music library to your Tidal account, run the following command:

```bash
uv run python3 -m src.cli.main sync
```

### Selective Synchronization

You can also synchronize specific types of your music data:

-   **Albums**: `uv run python3 -m src.cli.main sync --sync-albums`
-   **Artists**: `uv run python3 -m src.cli.main sync --sync-artists`
-   **Tracks**: `uv run python3 -m src.cli.main sync --sync-tracks`
-   **Playlists**: `uv run python3 -m src.cli.main sync --sync-playlists`

### Help

To view the help message, run:

```bash
uv run python3 -m src.cli.main sync --help
```

## Viewing the Log File

The application logs all synchronization activity to the file specified by the `LOG_FILE` variable in your `.env` file (default is `sync.log`). You can review this file to see which items were synced successfully and which failed.

## Switching Accounts / Troubleshooting

The application caches your login sessions to make it easier to run multiple times. If you want to switch to a different Spotify or Tidal account, you will need to delete the cached session files.

-   **To switch Spotify accounts**: Delete the `.cache` file in the root of the project directory.
-   **To switch Tidal accounts**: Delete the file specified by `TIDAL_SESSION_FILE` in your `.env` file (the default is `tidal_session.json`).

## How This Project Was Built

This project was built using [spec-kit](https://github.com/github/spec-kit), VSCode using Copilot with a Gemini 2.5 Pro agent. For more details on the development process, see [howthisprojectwasbuilt.md](howthisprojectwasbuilt.md).

## Acknowledgements

This project was inspired by the work of the [spotify2tidal/spotify_to_tidal](https://github.com/spotify2tidal/spotify_to_tidal) project.

