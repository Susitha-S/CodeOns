# Setup & Usage Guide

## Requirements

- **Python** 3.8 or later
- **pip** (comes with Python)

### Python Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | DataFrame loading, cleaning, and correlation computation |
| `numpy` | Numeric type checks and Z-score calculations |

> `json`, `sys`, and `pprint` are part of the Python standard library — no installation needed.

---

## Installation

### 1. Clone / obtain the project

```bash
git clone <repo-url>
cd project_x
```

### 2. (Recommended) Create a virtual environment

```bash
# Create
python -m venv .venv

# Activate — Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate — macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pandas numpy
```

---

## Running the Project

### Basic run (uses `data/input.csv` from `config.json`)

```bash
python run.py
```

### Run with a different CSV file

Pass the path as the first argument — it overrides the `p` key in `config.json`:

```bash
python run.py path/to/your/data.csv
```

### Dump the full correlation matrix

Add `--dump` to print the complete correlation matrix after the summary:

```bash
python run.py --dump
python run.py path/to/your/data.csv --dump
```

---

## Configuration

All settings live in [`config.json`](config.json). Edit it before running to change behaviour:

```json
{
  "p": "data/input.csv",   // input CSV path
  "t": 0.05,               // minimum |correlation| to report
  "m": "pearson",          // "pearson" or "spearman"
  "d": ",",                // CSV delimiter
  "x": true,               // drop rows still NaN after imputation
  "z": 2                   // Z-score outlier cutoff
}
```

---

## Expected Output

```
rows=10 | dropped=0 | usable=5
cols: ['a', 'b', 'c', 'd', 'e']
sig pairs:
  ('a', 'b') => 0.9857
  ('a', 'c') => -0.9227
  ...
```

- **rows** — total rows read from the CSV
- **dropped** — rows removed as outliers (Z-score > threshold)
- **usable** — rows remaining after outlier removal and imputation
- **sig pairs** — column pairs whose absolute Pearson/Spearman correlation exceeds `t`

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: pandas` | Dependencies not installed | Run `pip install pandas numpy` |
| `FileNotFoundError` | Wrong path in `config.json["p"]` | Check the `p` key points to a real file |
| `KeyError` on column `e` | CSV has no column named `e` | Remove or rename the categorical encoding line in `processor.py:14` |
| Pandas `ChainedAssignmentError` warnings | pandas ≥ 2.0 Copy-on-Write | See Known Issues in README.md |
| Empty `sig pairs` output | Threshold `t` too high, or too few clean rows | Lower `t` in `config.json` or reduce `z` |
