#!/usr/bin/env python3
"""migrate_to_opus.py - Re-encode all .m4a files to .ogg (Opus) and update content.toml."""

import argparse
import re
import subprocess
import sys
import toml
from pathlib import Path


def migrate_directory(music_dir: Path, dry_run: bool) -> None:
    m4a_files = sorted(f for f in music_dir.rglob("*.m4a") if f.is_file())

    if not m4a_files:
        print("No .m4a files found.")
        return

    print(f"Found {len(m4a_files)} .m4a file(s).\n")

    converted, failed = 0, 0

    for m4a_path in m4a_files:
        ogg_path = m4a_path.with_suffix(".ogg")

        if ogg_path.exists():
            print(f"  SKIP (exists): {m4a_path.name}")
            continue

        print(f"  Converting: {m4a_path.relative_to(music_dir)}")
        if dry_run:
            continue

        result = subprocess.run(
            ["ffmpeg", "-y", "-i", str(m4a_path), "-c:a", "libopus", "-b:a", "256k", str(ogg_path)],
            capture_output=True, timeout=600,
        )
        if result.returncode != 0:
            print(f"    FAILED: {result.stderr.decode().strip()}")
            failed += 1
            continue

        if not ogg_path.exists() or ogg_path.stat().st_size < 10_000:
            print(f"    FAILED: output file missing or too small")
            failed += 1
            continue

        print(f"    Done: {ogg_path.name}")
        m4a_path.unlink()
        converted += 1

    print(f"\nConverted: {converted}  Failed: {failed}")

    if dry_run and converted > 0:
        print("(Dry-run — no files were converted or deleted)")

    content_file = music_dir / "content.toml"
    if not content_file.exists():
        print("No content.toml found, skipping.")
        return

    content = content_file.read_text()
    updated = re.sub(r"\.m4a(?=[" r'"\']|\s|$)', ".ogg", content)

    if updated == content:
        print("content.toml: no .m4a paths found to update.")
        return

    print(f"\nUpdating content.toml...")
    if dry_run:
        print("(Dry-run — content.toml was not written)")
        return

    content_file.write_text(updated)
    print("content.toml updated.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-encode .m4a files to .ogg (Opus) and update content.toml.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(Path.home() / "Music"),
        help="Music directory (default: ~/Music)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be done without making changes",
    )
    args = parser.parse_args()

    music_dir = Path(args.directory).resolve()
    if not music_dir.is_dir():
        print(f"Error: '{music_dir}' is not a directory.")
        sys.exit(1)

    migrate_directory(music_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()