# 🐍 Python Automation Portfolio

A collection of clean, production-ready Python automation tools — the kind of
scripts small businesses and freelancers need every day. Each project is
self-contained, documented, and runnable out of the box.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Style](https://img.shields.io/badge/CLI-argparse-blue)

---

## 📦 Projects

### 1. [CSV → Excel Report Generator](./csv-to-excel-report)
Turns a raw CSV into a polished, multi-sheet Excel report with a cleaned data
sheet, an aggregated summary, and an auto-generated bar chart.
**Stack:** `pandas`, `openpyxl`

### 2. [Bulk Image Processor](./image-batch-processor)
Batch-resizes, watermarks, converts and web-optimizes whole folders of images
in one command — a common e-commerce / content task.
**Stack:** `Pillow`

### 3. [Smart File Organizer](./file-organizer)
Automatically sorts a messy folder (Downloads, Desktop…) into tidy
category subfolders by file type — pure standard library, zero dependencies.
**Stack:** Python stdlib only

---

## 🚀 Quick start

Each project has its own `README.md` and (where needed) `requirements.txt`:

```bash
cd csv-to-excel-report
pip install -r requirements.txt
python report.py --help
```

---

## 🧰 What these projects demonstrate
- Clean, documented, modular Python
- Proper CLI design with `argparse` (help, sensible defaults, dry-runs)
- Robust error handling and per-file fault tolerance
- Real-world data / file / image processing
- No secrets or external services required to run the demos

## 📄 License
MIT
