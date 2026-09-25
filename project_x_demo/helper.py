import pandas as pd
import numpy as np


def f1(df, s):
    """
    Impute missing values and optionally drop incomplete rows.

    For every numeric column (float64 or int64), fills NaN entries with that
    column's median value.  If `s` is True, any rows that still contain NaN
    after imputation (e.g. in non-numeric columns) are dropped entirely.

    Args:
        df (pd.DataFrame): Input dataframe, may contain NaN values.
        s  (bool):         If True, drop rows that still have NaN after imputation.

    Returns:
        pd.DataFrame: Cleaned copy of the input dataframe.
    """
    x = df.copy()  # work on a copy so the original is never mutated

    for c in x.columns:
        if x[c].dtype in [np.float64, np.int64]:
            # Replace NaN with the column median — robust to skewed distributions.
            # Direct assignment avoids the pandas >=2.0 ChainedAssignmentError that
            # was triggered by calling .fillna(inplace=True) on a DataFrame slice.
            x[c] = x[c].fillna(x[c].median())

    if s:
        # Drop any row that still has at least one NaN (e.g. non-numeric columns)
        x = x.dropna()

    return x


def f2(df, m):
    """
    Compute a pairwise correlation matrix for all numeric columns.

    Args:
        df (pd.DataFrame): Input dataframe (numeric + non-numeric columns allowed).
        m  (str):          Correlation method — "pearson" (linear) or "spearman" (rank-based).

    Returns:
        pd.DataFrame: Square correlation matrix of shape (n_numeric_cols, n_numeric_cols).
    """
    # Select only numeric columns so string/categorical columns don't cause errors
    nc = df.select_dtypes(include=[np.number]).columns.tolist()

    if m == "pearson":
        return df[nc].corr(method="pearson")   # standard linear correlation
    elif m == "spearman":
        return df[nc].corr(method="spearman")  # rank-based, handles non-linear relationships
    else:
        return df[nc].corr()                   # pandas default (pearson)


def f3(r, t):
    """
    Filter a correlation matrix to significant column pairs.

    Iterates the upper triangle of the correlation matrix (excluding the diagonal)
    and keeps only those pairs whose absolute correlation value is >= threshold `t`.

    Args:
        r (pd.DataFrame): Square correlation matrix (output of f2).
        t (float):        Minimum absolute correlation to include (e.g. 0.05).

    Returns:
        dict: Mapping of (col_a, col_b) tuple → rounded correlation coefficient.
              Only pairs with |correlation| >= t are included.
    """
    out = {}
    cols = r.columns.tolist()

    # Walk the upper triangle to avoid duplicate pairs (a,b) and (b,a)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            v = r.iloc[i, j]
            if abs(v) >= t:
                out[(cols[i], cols[j])] = round(v, 4)

    return out


def f4(df, z):
    """
    Remove outlier rows using Z-score filtering.

    Computes the Z-score for every numeric column.  Any row where at least one
    numeric value exceeds the absolute Z-score threshold `z` is considered an
    outlier and separated from the clean data.

    Args:
        df (pd.DataFrame): Input dataframe.
        z  (float):        Z-score cutoff (e.g. 2 removes rows > 2 std devs from mean).

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (clean_df, outlier_df)
            - clean_df   : rows where all numeric Z-scores are within threshold
            - outlier_df : rows that were flagged as outliers
    """
    nc = df.select_dtypes(include=[np.number]).columns  # only numeric columns considered
    tmp = df[nc].copy()

    # Z-score = (value - column_mean) / column_std for each cell
    zs = (tmp - tmp.mean()) / tmp.std()

    # Flag rows where ANY numeric column exceeds the Z-score threshold
    mask = (zs.abs() > z).any(axis=1)

    return df[~mask], df[mask]  # (clean rows, outlier rows)
