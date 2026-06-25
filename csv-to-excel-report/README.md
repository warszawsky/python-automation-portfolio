# 📊 CSV → Excel Report Generator

Turn a raw CSV export into a clean, presentation-ready Excel report in one
command. The script cleans the data, builds an aggregated summary, and embeds
an auto-generated bar chart.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?logo=pandas&logoColor=white)

## What it produces
- **Data** sheet — cleaned dataset, styled header, frozen top row, auto-sized columns
- **Summary** sheet — totals of a numeric column grouped by a category, sorted high→low
- An embedded **bar chart** visualising the summary

## Usage
```bash
pip install -r requirements.txt

# Auto-detect category & numeric columns
python report.py sample_data/sales.csv

# Or be explicit
python report.py sample_data/sales.csv -o sales_report.xlsx --group-by Region --value Revenue
```

## Features
- Auto-detects a category column and numeric column when not specified
- Cleans column names, drops empty rows/columns, trims whitespace
- Friendly errors (missing file, bad column names, empty data)
- Works with any CSV — not hard-coded to the sample

## Example
Running on `sample_data/sales.csv` groups revenue by region and charts it:

```
✅ Report written to: sample_data/sales_report.xlsx
   Rows processed : 16
   Grouped by     : Region
   Summed         : Revenue
   Categories     : 4
```
