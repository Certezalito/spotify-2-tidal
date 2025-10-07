# CLI Contracts: spotify-2-tidal

## `spotify-2-tidal`

### Description
The main command for the tool. Running this command without any arguments will synchronize the user's entire Spotify music library to their Tidal account.

### Usage
```
spotify-2-tidal [OPTIONS]
```

### Options
- `--sync-albums`: Synchronize saved albums only.
- `--sync-artists`: Synchronize followed artists only.
- `--sync-tracks`: Synchronize liked songs only.
- `--sync-playlists`: Synchronize playlists only.
- `--help`: Show the help message and exit.

### Behavior
- If no options are provided, the tool will perform a full synchronization of all data types.
- If one or more sync options are provided, the tool will only synchronize the specified data types.
- The tool will authenticate with both Spotify and Tidal before performing any synchronization.
- The tool will display real-time feedback to the user during the synchronization process.
- The tool will log all successful and failed synchronization attempts to `synced.log` and `errors.log` respectively.
