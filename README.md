# ytm-sync

Sync your YouTube Music library to local Opus files, with embedded metadata and playlists.

**Source:** [gitlab.com/Lalaggi/ytm-sync](https://gitlab.com/Lalaggi/ytm-sync)

## Features

- **Sync** — fetches all YTM playlists, downloads missing tracks as Opus, embeds metadata and cover art
- **Auth** — cookie-based authentication via browser export (DevTools), validated on each sync
- **Playlists** — auto-generates `.m3u8` files matching your YTM structure
- **Cover art** — embeds album art, with optional 1:1 crop for non-square images
- **Metadata** — writes title, artist, album, genre (playlist name), and source URL; `fix-metadata` rewrites from the local index
- **Scan** — rebuilds the local track database from existing files by reading embedded YTM URLs
- **Get** — search YTM interactively and download individual tracks

## Dependencies

- **Python 3.12+**
- **System:** `yt-dlp`, `ffmpeg`

## Installation

```bash
git clone https://gitlab.com/Lalaggi/ytm-sync.git
cd ytm-sync
pip install -r requirements.txt
# Optional: add to PATH
ln -s "$PWD/ytm-sync" ~/.local/bin/ytm-sync
```

## Quick Start

```bash
ytm-sync setup              # paste cookies, set download path
ytm-sync sync               # fetch library and download everything
ytm-sync get "song name"    # search and download a single track
```

## Usage

### `setup`

Interactive auth — paste JSON cookies from DevTools (`Application → Cookies → Export`) or raw headers. Saves to `~/.local/share/ytm-sync/auth.txt` and sets the download path in `~/.config/ytm-sync/config.toml`.

### `sync [playlist...]`

Diffs YTM playlists against the local index (`<music_dir>/content.toml`) and downloads missing tracks as `Artist/Album/Artist - Title.ogg`. Optionally filter to specific playlists.

### `get <query>`

Search YTM, pick from results, and download. Accepts ranges like `1-3,5`.

### `scan`

Rebuild `content.toml` from existing `.ogg` files by matching embedded YouTube URLs.

### `dedupe`

Safety-net cleanup for duplicate files that may have been created by older versions. Finds stale copies of a song (same `artist`/`title` in different files, e.g. single vs album version) and removes the redundant one; index duplicates (same path, split across `playlists`) are merged. Dry-run by default; `--apply` to delete.

> **New:** `sync` now handles re-releases in-place — when YTM swaps a track for a re-released version (new `video_id`/`album`), the local file's **ID and embedded metadata are updated** and its playlist memberships merged. Sync never re-downloads the same song in its entirety and a song in multiple playlists is stored as **one file with a `playlists = [...]` list**.

### Other commands

| Command | Description |
|---------|-------------|
| `list` | List all YTM playlists with track counts |
| `validate` | Check that stored auth is still valid |
| `fix-playlists` | Regenerate `.m3u8` playlists from `content.toml` |
| `fix-covers` | Crop embedded covers to 1:1 (center crop) |
| `fix-metadata` | Rewrite embedded tags from `content.toml` |

## File Layout

```
~/.config/ytm-sync/config.toml        # download path
~/.local/share/ytm-sync/auth.txt      # auth headers (JSON)
~/.local/share/ytm-sync/cookies.txt   # Netscape cookies for yt-dlp

<music_dir>/content.toml              # track index (YTM ID → local path)
<music_dir>/Artist/Album/Artist - Title.ogg
<music_dir>/PlaylistName/PlaylistName.m3u8
```

## Reporting Issues

https://gitlab.com/Lalaggi/ytm-sync/-/issues

## License

GPL-3.0 — see [LICENSE](LICENSE).
