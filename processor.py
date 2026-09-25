import pandas as pd
from helper import f1, f2, f3, f4


def go(cfg):
    """
    Run the full data analysis pipeline.

    Steps:
        1. Load the CSV file specified in config.
        2. Encode the categorical column 'e' (if present) to integer codes so it
           can participate in numeric correlation analysis.
        3. Remove outlier rows using Z-score filtering (helper f4).
        4. Impute remaining missing values with column medians (helper f1).
        5. Compute the pairwise correlation matrix (helper f2).
        6. Extract only the statistically significant pairs (helper f3).
        7. Return a result dict with counts, column names, and correlations.

    Args:
        cfg (dict): Configuration dict loaded from config.json. Expected keys:
                    "p" (str)   — CSV file path
                    "t" (float) — correlation significance threshold
                    "m" (str)   — correlation method ("pearson" or "spearman")
                    "z" (float) — Z-score outlier cutoff
                    "x" (bool)  — drop rows with remaining NaN after imputation
                    "d" (str)   — CSV delimiter

    Returns:
        dict: {
            "n_in"  : total rows read from CSV,
            "n_out" : rows removed as outliers,
            "n_clean": rows remaining after cleaning,
            "cols"  : list of all column names,
            "corr"  : dict of significant (col_a, col_b) → correlation coefficient,
            "mx"    : full correlation matrix as a nested dict
        }
    """
    # Unpack config keys into readable local names
    pp = cfg["p"]   # input CSV path
    tt = cfg["t"]   # significance threshold for filtering correlation pairs
    mm = cfg["m"]   # correlation method string ("pearson" / "spearman")
    zz = cfg["z"]   # Z-score threshold for outlier removal
    sx = cfg["x"]   # whether to drop rows still containing NaN after imputation

    # --- Step 1: Load raw data ---
    raw = pd.read_csv(pp, sep=cfg["d"])

    # --- Step 2: Encode categorical column 'e' ---
    # Converts string labels (e.g. "low", "medium", "high") to integer codes (0, 1, 2)
    # so the column can be included in the numeric correlation matrix.
    # WARNING: only handles a column literally named "e" — any other string column
    # will cause corr() to fail later.
    raw["e"] = raw["e"].astype("category").cat.codes if "e" in raw.columns else raw

    nn, mm2 = raw.shape   # nn = total row count, mm2 = column count (mm2 shadows config var mm)
    cl = list(raw.columns)  # store original column names before any filtering

    # --- Step 3: Outlier removal ---
    cln, outs = f4(raw, zz)   # cln = clean rows, outs = flagged outlier rows

    # --- Step 4: Impute missing values ---
    fx = f1(cln, sx)           # fills NaN with medians; drops remaining NaN rows if sx=True

    # --- Step 5 & 6: Correlation matrix + significance filter ---
    rr = f2(fx, mm)            # compute full correlation matrix
    sig = f3(rr, tt)           # keep only pairs with |correlation| >= tt

    # --- Step 7: Package results ---
    res = {
        "n_in":   nn,                                        # original row count
        "n_out":  len(outs),                                 # outlier rows dropped
        "n_clean": len(fx),                                  # usable rows after all cleaning
        "cols":   cl,                                        # all column names
        "corr":   {str(k): v for k, v in sig.items()},      # significant pairs (keys as strings)
        "mx":     rr.to_dict()                               # full matrix for optional --dump output
    }
    return res


def smry(res):
    """
    Print a human-readable summary of the pipeline result to stdout.

    Args:
        res (dict): Result dict returned by go().
    """
    # Row count summary line
    print(f"rows={res['n_in']} | dropped={res['n_out']} | usable={res['n_clean']}")
    print(f"cols: {res['cols']}")

    if res["corr"]:
        print("sig pairs:")
        for k, v in res["corr"].items():
            # Each key is a stringified tuple e.g. "('a', 'b')", value is the coefficient
            print(f"  {k} => {v}")
    else:
        print("no sig corr found")
