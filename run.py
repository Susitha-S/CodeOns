import json
import sys
import os
from processor import go, smry

# --- Load configuration ---
# config.json holds all runtime settings (file path, thresholds, method, etc.)
CONFIG_PATH = "config.json"

if not os.path.exists(CONFIG_PATH):
    print(f"Error: configuration file '{CONFIG_PATH}' not found.")
    sys.exit(1)

with open(CONFIG_PATH) as f:
    try:
        cfg = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: could not parse '{CONFIG_PATH}': {e}")
        sys.exit(1)

# Ensure all required keys are present before running anything
REQUIRED_KEYS = ["p", "t", "m", "z", "x", "d"]
missing = [k for k in REQUIRED_KEYS if k not in cfg]
if missing:
    print(f"Error: config.json is missing required key(s): {missing}")
    sys.exit(1)

# --- Optional CLI override for the input file path ---
# If a positional argument is provided (e.g. python run.py mydata.csv),
# it overrides the "p" (path) key from config.json.
if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    cfg["p"] = sys.argv[1]

# Verify the CSV file actually exists before handing off to the pipeline
if not os.path.exists(cfg["p"]):
    print(f"Error: input file '{cfg['p']}' not found. Check the 'p' key in config.json.")
    sys.exit(1)

# --- Run the analysis pipeline ---
# go() returns a result dict with row counts, column names, and correlation pairs
r = go(cfg)

# --- Print the summary to stdout ---
smry(r)

# --- Optional: dump the full correlation matrix ---
# Pass --dump as any CLI argument to pretty-print the complete matrix.
# Example: python run.py --dump
#          python run.py mydata.csv --dump
if "--dump" in sys.argv:
    import pprint
    pprint.pprint(r["mx"])
