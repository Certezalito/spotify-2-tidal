# Data Model: Spotify to Tidal Music Library Synchronization

## Entities

### User
- **Description**: Represents the individual using the tool.
- **Attributes**:
  - `spotify_credentials`: OAuth 2.0 tokens for the Spotify API.
  - `tidal_credentials`: OAuth 2.0 tokens for the Tidal API.

### Track
- **Description**: A single song.
- **Attributes**:
  - `title`: The title of the track.
  - `artist`: The primary artist of the track.
  - `album`: The album the track belongs to.
  - `isrc`: The International Standard Recording Code.
  - `spotify_id`: The ID of the track on Spotify.
  - `tidal_id`: The ID of the track on Tidal.

### Album
- **Description**: A collection of tracks.
- **Attributes**:
  - `title`: The title of the album.
  - `artist`: The primary artist of the album.
  - `spotify_id`: The ID of the album on Spotify.
  - `tidal_id`: The ID of the album on Tidal.

### Artist
- **Description**: A musical artist.
- **Attributes**:
  - `name`: The name of the artist.
  - `spotify_id`: The ID of the artist on Spotify.
  - `tidal_id`: The ID of the artist on Tidal.

### Playlist
- **Description**: A user-curated list of tracks.
- **Attributes**:
  - `name`: The name of the playlist.
  - `description`: The description of the playlist.
  - `is_public`: A boolean indicating whether the playlist is public or private.
  - `spotify_id`: The ID of the playlist on Spotify.
  - `tidal_id`: The ID of the playlist on Tidal.

### Log
- **Description**: A record of a synchronization attempt.
- **Attributes**:
  - `item_type`: The type of item being synced (e.g., "track", "album").
  - `item_name`: The name of the item.
  - `artist_name`: The name of the artist.
  - `album_name`: The name of the album.
  - `status`: The status of the sync attempt ("success" or "failure").
  - `reason`: The reason for a failure, if applicable.
  - `timestamp`: The date and time of the sync attempt.
