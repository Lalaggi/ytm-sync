# YTM-Sync

Sync your YouTube Music library to local Opus files.

**Source:** [gitlab.com/Lalaggi/ytm-sync](https://gitlab.com/Lalaggi/ytm-sync)

## Features

- **Sync** — Fetches all YTM library playlists, downloads missing tracks as Opus, embeds metadata and cover art
- **Auth** — Cookie-based authentication via browser export (DevTools), validated on each sync
- **Playlists** — Auto-generates `.m3u8` playlist files matching your YTM playlist structure
- **Cover Art** — Embeds album art from YouTube, with optional 1:1 crop for non-square images
- **Metadata** — Writes title, artist, album, genre (playlist name), and source URL; `fix-metadata` rewrites from local index
- **Scan** — Rebuilds your local track database from existing files by reading embedded YTM URLs
- **Get** — Search YTM interactively and download individual tracks
- **One-off Fixes** — Regen playlists, crop covers, or fix tags anytime

## Dependencies

- **Python 3.12+**
- System packages: `yt-dlp`, `ffmpeg`

## Installation

```bash
git clone https://gitlab.com/Lalaggi/ytm-sync.git
cd ytm-sync
pip install -r requirements.txt
# Optional: link to PATH
ln -s "$PWD/ytm-sync" ~/.local/bin/ytm-sync
```

## Quick Start

```bash
ytm-sync setup          # Paste cookies from browser, set download path
ytm-sync sync           # Fetch library and download everything
ytm-sync get "song name"  # Search and download a single track
```

## Usage

### `setup`

Interactive authentication. Paste JSON cookies from DevTools (`Application > Cookies > Export`) or raw request headers. Configures the download path and saves auth to `~/.local/share/ytm-sync/auth.txt`.

### `sync [playlist...]`

Fetch all YTM playlists, diff against the local index (`<music_dir>/content.toml`), and download missing tracks. Optionally filter to one or more playlists. Generated files are organized as `Artist/Album/Artist - Title.ogg`.

### `get <query>`

Search YTM for a track, select from results, and download it. Accepts ranges (e.g. `1-3,5`).

### `scan`

Scan existing `.ogg` files on disk and rebuild `content.toml` by matching embedded YouTube URLs against the YTM library.

### `dedupe`

YouTube Music occasionally repoints a playlist entry at a re-released version of a song (new `video_id` + album name). ytm-sync previously downloaded both into separate album folders. `dedupe` finds such collisions (same song identity across different album folders/files), keeps one canonical copy — preferring the version currently in your YTM library — and removes the rest, rewriting `content.toml` and playlists. Dry-run by default; pass `--apply` to actually delete redundant files.

> **Why songs get duplicated:** the file path is `Artist/Album/Artist - Title.ogg`. When YTM renames a release or swaps in a new upload of the same track, the path changes, so the existing file is no longer recognised and the track is re-downloaded. `sync` now keys on a stable song identity (`artist`/`title`, pinned to the album `browseId` when available) and skips re-downloading a song you already have.

### `list`

List all YTM playlists with track counts.

### `validate`

Check that the stored auth is still valid.

### `fix-playlists`

Regenerate all `.m3u8` playlist files from `content.toml`.

### `fix-covers`

Crop all embedded cover art to 1:1 (center crop) for files in the index.

### `fix-metadata`

Rewrite embedded tags (comment, purl) from `content.toml` into each file.

## File Layout

```
~/.config/ytm-sync/config.toml        # Download path
~/.local/share/ytm-sync/auth.txt      # Auth headers (JSON)
~/.local/share/ytm-sync/cookies.txt   # Netscape cookies for yt-dlp

<music_dir>/content.toml              # Track index (YTM ID → local path)
<music_dir>/Artist/Album/Artist - Title.ogg
<music_dir>/PlaylistName/PlaylistName.m3u8
```

## Reporting Issues

https://gitlab.com/Lalaggi/ytm-sync/-/issues
