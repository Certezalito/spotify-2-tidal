# spotify-2-tidal

A command-line tool to synchronize your Spotify music library to your Tidal account.  This project was built with https://github.com/github/spec-kit version 0.0.57.   More details in [how was this project built](build.md) 

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/Certezalito/spotify-2-tidal-spec-kit.git
   cd spotify-2-tidal-spec-kit
   ```

2. **Create and activate a virtual environment**:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` file** in the root of the project.

2. **Add your API credentials** to the `.env` file:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   TIDAL_CLIENT_ID=your_tidal_client_id
   TIDAL_CLIENT_SECRET=your_tidal_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   TIDAL_REDIRECT_URI=http://localhost:8888/callback
   TIDAL_PLAYLIST_FOLDER=synced_from_spotify
   TIDAL_SESSION_FILE=tidal_session.json
   ```

## Usage

### Full Synchronization
To synchronize your entire Spotify music library to your Tidal account, run the following command:
```
python3 -m src.cli.main sync
```

### Selective Synchronization
You can also synchronize specific types of your music data:

- **Albums**: `python3 -m src.cli.main sync --sync-albums`
- **Artists**: `python3 -m src.cli.main sync --sync-artists`
- **Tracks**: `python3 -m src.cli.main sync --sync-tracks`
- **Playlists**: `python3 -m src.cli.main sync --sync-playlists`

### Help
To view the help message, run:
```
python3 -m src.cli.main sync --help
```

## Viewing the Log File

The application logs all track synchronization failures to a SQLite database file named `synced.db`. You can inspect this file to see which tracks failed to sync and why.

You can use any SQLite database viewer to open and explore the `synced.db` file. Here are a few common methods:

### Using the `sqlite3` Command-Line Tool

If you have `sqlite3` installed, you can use it to query the database directly from your terminal:

```bash
sqlite3 synced.db
```

Once you're in the SQLite shell, you can run queries. For example, to see all the logs:

```sql
SELECT * FROM logs;
```

To see only the failed tracks:

```sql
SELECT * FROM logs WHERE status = 'failure';
```

### Using a GUI Tool

If you prefer a graphical interface, you can use a tool like [DB Browser for SQLite](https://sqlitebrowser.org/). Simply open the `synced.db` file with the application to browse the data.
