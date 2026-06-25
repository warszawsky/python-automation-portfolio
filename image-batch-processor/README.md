# 🖼 Bulk Image Processor

Process an entire folder of images in one command — resize, watermark, convert
and web-optimize. Built for e-commerce catalogs, blogs and content pipelines.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-11.0-orange)

## Features
- **Resize** by max width/height while keeping aspect ratio
- **Watermark** — semi-transparent text in the bottom-right corner
- **Convert** between `jpg` / `png` / `webp`
- **Web-optimize** — quality control + metadata stripping
- Fault-tolerant: a corrupt file is skipped, the batch keeps going

## Usage
```bash
pip install -r requirements.txt

# Resize everything to max 1280px and convert to WebP
python process_images.py ./input ./output --max-size 1280 --format webp

# Add a watermark and compress
python process_images.py ./input ./output --watermark "© My Brand" --quality 80
```

## Options
| Option | Description |
|---|---|
| `--max-size N` | Max width/height in px (aspect ratio preserved) |
| `--watermark "text"` | Adds a semi-transparent watermark, bottom-right |
| `--format {jpg,png,webp}` | Convert output format |
| `--quality 1-95` | JPEG/WebP quality (default 85) |

Supported inputs: `jpg, jpeg, png, webp, bmp, tiff, gif`.
