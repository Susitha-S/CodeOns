# project_x — Correlation Analysis Tool

A lightweight Python pipeline that reads a CSV dataset, cleans it, removes outliers, and computes pairwise variable correlations. Significant correlation pairs are printed to stdout.

---

## What It Does

1. **Loads** a CSV file specified in `config.json`
2. **Encodes** any string/categorical column (`e`) to integer codes so it can be included in numeric analysis
3. **Removes outliers** using Z-score filtering (rows whose numeric values exceed a configurable Z-score threshold are dropped)
4. **Imputes missing values** in numeric columns with each column's median; optionally drops any remaining rows that still have NaN values
5. **Computes a correlation matrix** across all numeric columns using either Pearson or Spearman method
6. **Filters** the matrix to only return column pairs whose absolute correlation exceeds the configured significance threshold
7. **Prints** a summary: row counts, column names, and all significant correlation pairs with their coefficients

---

## Project Structure

```
project_x/
├── config.json       # Runtime configuration (all settings live here)
├── run.py            # Entry point — load config, run pipeline, print results
├── processor.py      # Pipeline orchestration (go) and console summary (smry)
├── helper.py         # Core data-processing functions
└── data/
    └── input.csv     # Sample input dataset (10 rows, 5 columns)
```

---

## Configuration (`config.json`)

| Key | Type | Description |
|-----|------|-------------|
| `p` | string | Path to the input CSV file |
| `t` | float | Correlation significance threshold (e.g. `0.05` keeps pairs with \|r\| ≥ 0.05) |
| `n` | int | Expected number of rows (informational, not enforced) |
| `m` | string | Correlation method: `"pearson"` or `"spearman"` |
| `d` | string | CSV delimiter character (e.g. `","`) |
| `x` | bool | If `true`, drop rows that still have NaN after median imputation |
| `z` | int/float | Z-score threshold for outlier removal (e.g. `2` removes rows > 2 std devs) |
| `q` | array | Quantile bounds (defined but not currently used in the pipeline) |
| `r` | int | Random seed (defined but not currently used in the pipeline) |
| `k` | int | Cluster count (defined but not currently used in the pipeline) |

---

## Input / Output

### Input
- **CSV file** at the path specified by `config.json["p"]`
- Must have a header row
- Numeric columns can contain missing values (imputed with median)
- One categorical/string column named `e` is supported and auto-encoded to integers

### Output (stdout)
```
rows=<total> | dropped=<outliers> | usable=<clean rows>
cols: [<column names>]
sig pairs:
  ('<col1>', '<col2>') => <correlation coefficient>
  ...
```
- If `--dump` is passed as a CLI argument, the full correlation matrix is also pretty-printed.

---

## Function Reference

### `helper.py`

| Function | Signature | Purpose |
|----------|-----------|---------|
| `f1` | `f1(df, s)` | Impute missing numeric values with column medians; optionally drop remaining NaN rows |
| `f2` | `f2(df, m)` | Compute correlation matrix using the specified method (`pearson`/`spearman`) |
| `f3` | `f3(r, t)` | Extract column pairs from the correlation matrix that exceed threshold `t` |
| `f4` | `f4(df, z)` | Remove rows whose numeric values exceed Z-score `z`; returns `(clean_df, outlier_df)` |

### `processor.py`

| Function | Purpose |
|----------|---------|
| `go(cfg)` | Full pipeline: load CSV → encode → outlier removal → imputation → correlation → filter |
| `smry(res)` | Print a human-readable summary of the pipeline result dict |

---

## Known Issues & Code Quality Notes

- **`ChainedAssignmentError` (helper.py line 9):** `x[c].fillna(..., inplace=True)` triggers a pandas Copy-on-Write warning in pandas ≥ 2.0. The imputation may silently fail on some pandas versions. Fix: replace with `x[c] = x[c].fillna(x[c].median())`.
- **Variable shadowing (processor.py line 9):** `mm` is used for both the correlation method string and later `mm2` for the column count — confusing but harmless.
- **Unused config keys:** `q` (quantiles), `r` (random seed), and `k` (cluster count) are loaded from config but never referenced in the pipeline.
- **Hardcoded column name `"e"`:** The categorical encoding in `processor.py` line 14 only handles a column literally named `"e"`. Any other string column will cause `corr()` to fail.
- **No error handling:** Missing file, malformed CSV, or wrong config keys all produce unhandled exceptions.
- **`import json` unused in processor.py:** Imported but never called.
