# 🗂 Smart File Organizer

Instantly tidy a cluttered folder (Downloads, Desktop, a shared drive…) by
sorting files into category subfolders — **Images, Documents, Audio, Video,
Archives, Code, Other**.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-success)

## Why it's safe
- **`--dry-run`** previews every move and changes nothing
- **Never overwrites** — name clashes get an automatic ` (1)`, ` (2)` suffix
- Only touches top-level files; its own category folders are left alone
- **Zero dependencies** — pure Python standard library

## Usage
```bash
# Preview first (recommended)
python organize.py "C:/Users/you/Downloads" --dry-run

# Actually organize
python organize.py "C:/Users/you/Downloads"
```

## Example output
```
📂 Organizing: C:/Users/you/Downloads
  moved: invoice.pdf      →  Documents/invoice.pdf
  moved: logo.png         →  Images/logo.png
  moved: setup.zip        →  Archives/setup.zip

Summary:
  Archives   1 file(s)
  Documents  1 file(s)
  Images     1 file(s)

✅ Moved 3 file(s).
```

## Customizing
Edit the `CATEGORIES` dictionary in `organize.py` to add extensions or new
categories — it's a single, readable mapping.
