# CHANGES.md

All changes were made as targeted bug fixes following a code-quality audit of the original codebase. No behaviour was changed beyond what is explicitly described below.

---

## Fix 1 — `helper.py`: Replace `fillna(inplace=True)` with direct column assignment

**File:** `helper.py`, function `f1`, line 27  
**Type:** Bug fix

### What was wrong

```python
# Before
x[c].fillna(x[c].median(), inplace=True)
```

This is a chained assignment: `x[c]` returns a temporary copy of the column, and calling `.fillna(inplace=True)` mutates that temporary copy — not the original DataFrame `x`. In pandas ≥ 2.0 (Copy-on-Write mode), this raises a `ChainedAssignmentError` on every numeric column and the imputation silently does nothing. As a result, all rows with any remaining NaN were subsequently dropped by the `dropna()` call, reducing the usable dataset from 10 rows down to 5.

### What was changed

```python
# After
x[c] = x[c].fillna(x[c].median())
```

Direct assignment to `x[c]` writes the imputed series back into the DataFrame correctly, regardless of pandas version. The `inplace=True` argument is removed entirely.

### Impact

- Eliminates all `ChainedAssignmentError` warnings at runtime.
- Imputation now works correctly: rows with NaN in numeric columns are filled with the column median and retained. In the sample dataset this restores 5 previously-dropped rows, raising `usable` from 5 → 10.

---

## Fix 2 — `processor.py`: Remove unused `import json`

**File:** `processor.py`, line 2  
**Type:** Code quality / cleanup

### What was wrong

```python
# Before
import json  # NOTE: imported but not used — can be removed
```

`json` was imported in `processor.py` but never referenced anywhere in the module. The JSON loading is performed in `run.py`, which already imports `json` correctly.

### What was changed

The `import json` line was removed entirely.

### Impact

- No functional change.
- Eliminates a spurious import that could mislead a reader into thinking `processor.py` reads or writes JSON itself.

---

## Fix 3 — `run.py`: Add basic error handling for startup failures

**File:** `run.py`  
**Type:** Robustness / error handling

### What was wrong

The original `run.py` had no error handling at startup. Three failure modes produced confusing Python tracebacks instead of actionable messages:

1. **Missing `config.json`** — `FileNotFoundError` with a raw Python traceback.
2. **Malformed `config.json`** — `json.JSONDecodeError` with a raw traceback.
3. **Missing required config keys** — `KeyError` inside `processor.go()`, far from the real cause.
4. **Missing CSV file** — `FileNotFoundError` raised deep inside pandas, with no hint about which config key to fix.
5. **`--dump` passed as the first positional arg** — previously would have incorrectly overwritten `cfg["p"]` with the string `"--dump"`.

### What was changed

```python
# After — run.py startup sequence
import os

# 1. Check config file exists before opening
if not os.path.exists(CONFIG_PATH):
    print(f"Error: configuration file '{CONFIG_PATH}' not found.")
    sys.exit(1)

# 2. Catch malformed JSON
with open(CONFIG_PATH) as f:
    try:
        cfg = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: could not parse '{CONFIG_PATH}': {e}")
        sys.exit(1)

# 3. Validate all required keys are present
REQUIRED_KEYS = ["p", "t", "m", "z", "x", "d"]
missing = [k for k in REQUIRED_KEYS if k not in cfg]
if missing:
    print(f"Error: config.json is missing required key(s): {missing}")
    sys.exit(1)

# 4. Guard CLI override against flag arguments (e.g. --dump)
if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    cfg["p"] = sys.argv[1]

# 5. Check CSV file exists before running the pipeline
if not os.path.exists(cfg["p"]):
    print(f"Error: input file '{cfg['p']}' not found. Check the 'p' key in config.json.")
    sys.exit(1)
```

### Impact

- All four failure modes now print a clear, actionable error message and exit with code 1 instead of dumping a traceback.
- The `--dump` flag is no longer accidentally treated as a file path when passed as `sys.argv[1]`.
- No change to normal execution behaviour.
