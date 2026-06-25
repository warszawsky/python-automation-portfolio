"""
Smart File Organizer
====================

Tidies a messy folder (Downloads, Desktop, …) by moving files into category
subfolders based on their type — Images, Documents, Audio, Video, Archives,
Code, and Other.

Safe by design:
  • --dry-run shows exactly what would happen, changing nothing
  • never overwrites: name clashes get an automatic " (1)", " (2)" suffix
  • only touches files in the top level (its own category folders are skipped)

No third-party dependencies — pure Python standard library.

Usage
-----
    python organize.py ~/Downloads --dry-run
    python organize.py ~/Downloads
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Ensure emoji / Unicode print correctly on Windows consoles (cp1251 etc.)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                  ".txt", ".rtf", ".odt", ".csv", ".md"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".sh",
             ".java", ".c", ".cpp", ".go", ".rs", ".rb", ".php"},
}
OTHER = "Other"


def category_for(suffix: str) -> str:
    suffix = suffix.lower()
    for name, exts in CATEGORIES.items():
        if suffix in exts:
            return name
    return OTHER


def unique_destination(dest: Path) -> Path:
    """Avoid overwriting: foo.txt → foo (1).txt → foo (2).txt …"""
    if not dest.exists():
        return dest
    i = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({i}){dest.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def organize(folder: Path, dry_run: bool) -> dict[str, int]:
    managed = set(CATEGORIES) | {OTHER}
    counts: dict[str, int] = {}

    files = [p for p in folder.iterdir() if p.is_file()]
    for path in files:
        category = category_for(path.suffix)
        target_dir = folder / category
        dest = unique_destination(target_dir / path.name)

        action = "[dry-run] would move" if dry_run else "moved"
        print(f"  {action}: {path.name}  →  {category}/{dest.name}")

        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(path), str(dest))

        counts[category] = counts.get(category, 0) + 1

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sort a folder's files into category subfolders."
    )
    parser.add_argument("folder", type=Path, help="Folder to organize")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without moving anything"
    )
    args = parser.parse_args()

    if not args.folder.is_dir():
        sys.exit(f"❌ Not a folder: {args.folder}")

    print(f"📂 Organizing: {args.folder.resolve()}")
    counts = organize(args.folder, args.dry_run)

    if not counts:
        print("Nothing to organize — no files found.")
        return

    print("\nSummary:")
    for category, n in sorted(counts.items()):
        print(f"  {category:<10} {n} file(s)")
    total = sum(counts.values())
    verb = "Would move" if args.dry_run else "Moved"
    print(f"\n✅ {verb} {total} file(s).")


if __name__ == "__main__":
    main()
