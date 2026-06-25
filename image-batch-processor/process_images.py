"""
Bulk Image Processor
====================

Batch-process a whole folder of images in one command:

  • Resize (by max width/height, keeping aspect ratio)
  • Add a text watermark (bottom-right, semi-transparent)
  • Convert format (jpg / png / webp)
  • Web-optimize (quality + strip metadata)

Each file is handled independently — one broken image won't stop the batch.

Usage
-----
    python process_images.py ./input ./output --max-size 1280 --format webp
    python process_images.py ./input ./output --watermark "© My Brand" --quality 80
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Ensure emoji / Unicode print correctly on Windows consoles (cp1251 etc.)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif"}
FORMAT_MAP = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}


def find_images(folder: Path) -> list[Path]:
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED)


def resize(img: Image.Image, max_size: int | None) -> Image.Image:
    if not max_size:
        return img
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    return img


def add_watermark(img: Image.Image, text: str) -> Image.Image:
    """Draw a semi-transparent watermark in the bottom-right corner."""
    base = img.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(14, base.size[0] // 25)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    margin = max(8, font_size // 2)
    x, y = base.size[0] - tw - margin, base.size[1] - th - margin * 2

    # subtle shadow + text for readability on any background
    draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0, 160))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 200))

    return Image.alpha_composite(base, overlay)


def save(img: Image.Image, dest: Path, fmt: str, quality: int) -> None:
    pillow_fmt = FORMAT_MAP[fmt]
    if pillow_fmt in {"JPEG"} and img.mode in {"RGBA", "P"}:
        img = img.convert("RGB")  # JPEG has no alpha channel
    params: dict = {}
    if pillow_fmt in {"JPEG", "WEBP"}:
        params.update(quality=quality, optimize=True)
    img.save(dest, format=pillow_fmt, **params)


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch resize / watermark / convert images.")
    parser.add_argument("input", type=Path, help="Input folder")
    parser.add_argument("output", type=Path, help="Output folder (created if missing)")
    parser.add_argument("--max-size", type=int, help="Max width/height in px (keeps aspect ratio)")
    parser.add_argument("--watermark", help="Watermark text (bottom-right)")
    parser.add_argument(
        "--format", choices=["jpg", "png", "webp"], help="Convert to this format"
    )
    parser.add_argument("--quality", type=int, default=85, help="JPEG/WebP quality 1-95 (default 85)")
    args = parser.parse_args()

    if not args.input.is_dir():
        sys.exit(f"❌ Input folder not found: {args.input}")

    images = find_images(args.input)
    if not images:
        sys.exit(f"❌ No supported images in {args.input}")

    args.output.mkdir(parents=True, exist_ok=True)

    ok, failed = 0, 0
    for path in images:
        try:
            with Image.open(path) as img:
                img.load()
                img = resize(img, args.max_size)
                if args.watermark:
                    img = add_watermark(img, args.watermark)

                fmt = args.format or path.suffix.lstrip(".").lower()
                fmt = "jpg" if fmt == "jpeg" else fmt
                if fmt not in FORMAT_MAP:
                    fmt = "png"
                dest = args.output / f"{path.stem}.{fmt}"
                save(img, dest, fmt, args.quality)
            print(f"  ✓ {path.name}  →  {dest.name}")
            ok += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ {path.name}: {exc}")
            failed += 1

    print(f"\n✅ Done. Processed {ok} image(s), {failed} failed → {args.output}")


if __name__ == "__main__":
    main()
