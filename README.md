# YTM-Sync

Sync your YouTube Music library to local Opus files.

**Source:** [codeberg.org/el1lovescomputers/ytm-sync](https://codeberg.org/el1lovescomputers/ytm-sync)

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

```bash
pip install toml ytmusicapi yt-dlp-ejs Pillow mutagen
```

System packages: `yt-dlp`, `ffmpeg`, `python3`

## Installation

```bash
git clone https://codeberg.org/el1lovescomputers/ytm-sync
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

https://codeberg.org/el1lovescomputers/ytm-sync/issues
