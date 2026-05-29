#!/usr/bin/env python3
"""Fix metadata in ogg/opus files from content.toml."""

import sys
from pathlib import Path

try:
    import toml
except ImportError:
    print("Error: toml required. Install with: pip install toml")
    sys.exit(1)

try:
    from mutagen.oggopus import OggOpus
except ImportError:
    print("Error: mutagen required. Install with: pip install mutagen")
    sys.exit(1)


def expand_path(p: str, music_dir: Path) -> Path:
    if p.startswith("~/"):
        return Path(p.replace("~", str(Path.home())))
    if p.startswith("/"):
        return Path(p)
    return (music_dir / p).resolve()


def main():
    music_dir = Path.home() / "Music"
    content_file = music_dir / "content.toml"

    if not content_file.exists():
        print(f"Error: {content_file} not found")
        sys.exit(1)

    with open(content_file) as f:
        data = toml.load(f)

    tracks = data.get("tracks", [])
    print(f"Processing {len(tracks)} tracks...")

    updated = skipped = errors = 0

    for track in tracks:
        path = track.get("path", "")
        if not path:
            continue

        fp = expand_path(path, music_dir)
        if not fp.exists():
            skipped += 1
            continue

        youtube_id = track.get("youtube_id", "")
        if not youtube_id:
            skipped += 1
            continue

        url = f"https://music.youtube.com/watch?v={youtube_id}"

        try:
            from mutagen.oggopus import OggOpus
            audio = OggOpus(str(fp))

            audio["comment"] = url
            audio["purl"] = url
            audio.save()
            updated += 1
            print(f"  Updated: {fp.name}")
        except Exception as e:
            errors += 1
            print(f"  Error: {fp.name}: {e}")

    print(f"\nUpdated: {updated}  Skipped: {skipped}  Errors: {errors}")


if __name__ == "__main__":
    main()