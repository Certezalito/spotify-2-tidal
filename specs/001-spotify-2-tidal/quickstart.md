# Quickstart: spotify-2-tidal

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
spotify-2-tidal
```

### Selective Synchronization
You can also synchronize specific types of your music data:

- **Albums**: `spotify-2-tidal --sync-albums`
- **Artists**: `spotify-2-tidal --sync-artists`
- **Tracks**: `spotify-2-tidal --sync-tracks`
- **Playlists**: `spotify-2-tidal --sync-playlists`

### Help
To view the help message, run:
```
spotify-2-tidal --help
```
