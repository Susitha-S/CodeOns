---
name: code-ons
description: Use when the user has inherited, is onboarding onto, or wants to fully understand an unfamiliar codebase — scans structure, analyzes flow, fixes bugs, and generates README, SETUP, inline comments, CHANGES, and requirements.txt.
---

# codeOns — Unfamiliar Codebase Onboarding Skill

Follow these steps **in order** every time this skill is activated. Use `update_todo_list` to track progress. Never skip a step.

---

## Step 1 — Announce and scaffold the todo list

Tell the user you are beginning a full codebase onboarding pass. Create an initial todo list with all steps below marked pending.

```
[ ] Step 1 — Scan repository structure
[ ] Step 2 — Parallel analysis (flow, deps, I/O, quality)
[ ] Step 3 — Generate README.md
[ ] Step 4 — Generate SETUP.md
[ ] Step 5 — Add inline comments to all source files
[ ] Step 6 — Fix identified bugs
[ ] Step 7 — Generate CHANGES.md
[ ] Step 8 — Generate requirements.txt
[ ] Step 9 — Print onboarding summary
```

---

## Step 2 — Scan repository structure

Use `list_files` (recursive: true) on the workspace root to get the full file tree.

Identify:
- The **entry point(s)** — files named `main.*`, `run.*`, `app.*`, `index.*`, `__main__.py`, or similar
- All **source files** by extension (`.py`, `.js`, `.ts`, `.go`, `.java`, `.rb`, `.rs`, `.cs`, etc.)
- **Configuration files** — `config.*`, `.env`, `*.json`, `*.yaml`, `*.toml`, `*.ini`
- **Dependency manifests** — `requirements.txt`, `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `Pipfile`, `pyproject.toml`, etc.
- **Existing documentation** — `README*`, `SETUP*`, `CHANGES*`, `CHANGELOG*`, `docs/`
- **Data files** — `*.csv`, `*.json`, `*.parquet`, `*.db`, etc.

Mark Step 1 complete, start Step 2.

---

## Step 3 — Parallel analysis (four tracks)

Read all source and configuration files. Launch all four analyses **in the same turn** where possible using parallel tool calls.

### Track A — End-to-end flow
- Trace execution from the entry point through every module
- Map the call chain: which function calls which, in what order
- Identify the data transformation pipeline (load → process → output)
- Note any branching logic or CLI argument handling

### Track B — Dependencies
- From manifests or import statements, list every external library/package used
- Note the **actual version** installed if detectable (e.g. from a lock file or `pip show`)
- Flag any import that is declared but never used

### Track C — Inputs and outputs
- **Inputs:** files read, environment variables, CLI arguments, config keys, stdin, APIs called
- **Outputs:** files written, stdout/stderr, return values of public functions, side effects
- For each config key: record its name, type, default value, and what it controls

### Track D — Code quality and bugs
- Look for: silent failures, wrong-direction mutations (e.g. `inplace=True` on a slice), unused imports, unused variables, shadowed names, hardcoded paths, missing error handling, type mismatches
- Classify each finding as **Bug** (incorrect behaviour) or **Quality** (smell/warning)
- Record the file name, line number, and a one-line description for every finding

Mark Step 2 complete, start Step 3.

---

## Step 4 — Generate README.md

Write `README.md` to the workspace root. Include all of the following sections:

```markdown
# <Project Name> — <one-line description>

## What It Does
<Paragraph describing the end-to-end pipeline in plain English>

## Project Structure
<Directory tree with one-line explanation per file>

## Configuration
<Table: key | type | default | description — for every config key found>

## Input / Output
### Input
<List every input: files, CLI args, env vars, config keys>
### Output (stdout/stderr/files)
<Sample output block + description of each field>

## Function Reference
<Table: function name | signature | what it does — for every public function>

## Known Issues & Code Quality Notes
<Bullet list of every finding from Track D, with file:line references>
```

Mark Step 3 complete, start Step 4.

---

## Step 5 — Generate SETUP.md

Write `SETUP.md` to the workspace root. Include:

```markdown
# Setup & Usage Guide

## Requirements
<Language version, runtime version>

### Dependencies
<Table: package | purpose>

## Installation
### 1. Clone / obtain the project
### 2. Create a virtual environment (if applicable)
### 3. Install dependencies
<Exact shell commands for the detected language/ecosystem>

## Running the Project
### Basic run
### Run with a different input file (if applicable)
### Optional flags / modes

## Configuration
<Annotated copy of the config file with inline explanations>

## Expected Output
<Sample output block>

## Troubleshooting
<Table: problem | likely cause | fix — for every known failure mode>
```

Mark Step 4 complete, start Step 5.

---

## Step 6 — Add inline comments to all source files

For **every source file** identified in Step 2:

1. Read the current file contents.
2. Add a **docstring** (or equivalent for the language) to every function/method/class that lacks one. The docstring must describe: what it does, its parameters, and its return value.
3. Add **inline comments** to non-obvious logic — algorithm steps, magic values, side-effect warnings, workarounds.
4. Do **not** remove existing code. Do **not** reformat unrelated lines. Surgical edits only.
5. Use `apply_diff` or `search_and_replace` for targeted additions; use `write_file` only if the changes are too pervasive for diffs.

Process files one at a time (not in parallel) to avoid conflicts.

Mark Step 5 complete, start Step 6.

---

## Step 7 — Fix identified bugs

For each **Bug** finding from Track D (not Quality smells):

1. State the bug: file, line, what is wrong, and why.
2. Apply the minimal correct fix using `apply_diff` or `search_and_replace`.
3. Update the inline comment in the fixed line to explain the fix.
4. Do **not** fix Quality items here — those go into CHANGES.md as notes only.
5. After all fixes, run the project's entry point with `execute_command` to verify no new errors were introduced. If a test command is present (`pytest`, `npm test`, etc.), run that instead.

Mark Step 6 complete, start Step 7.

---

## Step 8 — Generate CHANGES.md

Write `CHANGES.md` to the workspace root. Document **every change made in Steps 6 and 7**:

```markdown
# CHANGES.md

## Fix N — <short title>
**File:** `path/to/file.ext`, line N  
**Type:** Bug fix | Code quality | Comment added

### What was wrong
<Code block showing the before state>

### What was changed
<Code block showing the after state>

### Impact
<One paragraph: what breaks without this fix, what improves with it>
```

Include one entry per fix. Do not include changes that were comments-only unless there is something noteworthy to explain.

Mark Step 7 complete, start Step 8.

---

## Step 9 — Generate requirements.txt (Python projects)

**If the project is Python:**

1. Collect every unique third-party import found across all `.py` files (ignore stdlib modules).
2. Check if exact versions are already pinned in an existing `requirements.txt`, `Pipfile.lock`, or `pyproject.toml`.
3. If exact versions are available, use `==`. Otherwise use `>=<minimum_safe_version>` based on the API features used.
4. Write the file — one package per line, alphabetically sorted.

**If the project is not Python**, generate the appropriate equivalent:
- Node.js → confirm `package.json` `dependencies` block is correct
- Go → confirm `go.mod` is present
- Other → list detected dependencies in a plain `dependencies.txt` with a note

Mark Step 8 complete, start Step 9.

---

## Step 10 — Print onboarding summary

Print a final summary to the chat with these sections:

### ✅ Files Generated
List every file created or modified, with a one-line description.

### 🔍 What This Project Does
Two or three sentences describing the project in plain English.

### ⚠️ Bugs Fixed
Bullet list: file:line — what was wrong — what was done.

### 📋 Quality Notes (not fixed)
Bullet list of remaining smells/warnings that were documented but not auto-fixed.

### 🚀 To Run It
The single shell command needed to run the project, copy-pasteable.

Mark Step 9 complete. The onboarding pass is complete.
