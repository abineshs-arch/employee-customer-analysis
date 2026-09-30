# Employee Data Analysis & Insights Platform

Modular Python pipeline: ingest, clean, analyze (NumPy/Pandas), merge, enrich via REST API, visualize (Matplotlib), report.

## Setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env

## Run
python -m src.main

## Data
- data/raw/employees.csv: IBM Employee Dataset (Kaggle)
- data/raw/departments.csv: illustrative placeholder budgets (not real figures)

## Notes
- Left join keeps every employee even if a department is missing from the budget file.
- The join-trend chart uses an approximate join year (2026 minus years at company) because the source has no joining date.