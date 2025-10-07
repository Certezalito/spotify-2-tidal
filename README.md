# spotify-2-tidal

A command-line tool to synchronize your Spotify music library to your Tidal account.

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/Certezalito/spotify-2-tidal-spec-kit.git
   cd spotify-2-tidal-spec-kit
   ```

2. **Install dependencies**:
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
   ```

## Usage

### Full Synchronization
To synchronize your entire Spotify music library to your Tidal account, run the following command:
```
python src/cli/main.py sync
```

### Selective Synchronization
You can also synchronize specific types of your music data:

- **Albums**: `python src/cli/main.py sync --sync-albums`
- **Artists**: `python src/cli/main.py sync --sync-artists`
- **Tracks**: `python src/cli/main.py sync --sync-tracks`
- **Playlists**: `python src/cli/main.py sync --sync-playlists`

### Help
To view the help message, run:
```
python src/cli/main.py sync --help
```
