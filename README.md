# CodeOns — Automated Codebase Onboarding Agent
### IBM Bob 2.0 Hackathon Submission

**Team:** Susitha Sambath, Aravina D  
**Track:** Developer Workflow Improvement  
**Tool:** IBM Bob 2.0 (Agent Mode + Custom Skill)

---

## The Problem

Every developer has inherited a project like this:

- No README
- Cryptic variable names (`f1`, `f2`, `pp`, `zz`, `rr`)
- No setup instructions
- No comments
- Hidden bugs
- No idea what inputs it expects or what it produces

This is not an edge case. It is the norm in real teams — when developers leave, projects get handed off, or someone returns to code they wrote months ago.

**The cost is real:**
- 2–3 hours minimum to understand an unfamiliar codebase
- Bugs never caught because no one understood the code well enough
- New team members blocked for days before they can contribute

---

## The Solution — CodeOns

CodeOns is a **reusable IBM Bob 2.0 custom skill** that turns any undocumented, messy codebase into a fully documented, bug-fixed, ready-to-use project — in under 5 minutes.

### How it works

A developer opens any project in Bob IDE and says:

> *"I've inherited this codebase, help me understand it"*

Bob **automatically activates the `code-ons` skill** and runs a structured 9-step autonomous workflow:

```
Step 1 — Scan full repo structure (entry points, configs, data files)
Step 2 — Launch 4 parallel analysis tracks:
           ├── End-to-end flow mapping
           ├── Dependency detection
           ├── Input/output mapping
           └── Bug and code quality analysis
Step 3 — Generate README.md
Step 4 — Generate SETUP.md
Step 5 — Add inline comments to all source files
Step 6 — Fix every identified bug
Step 7 — Generate CHANGES.md (before/after for every fix)
Step 8 — Generate requirements.txt
Step 9 — Print final onboarding summary
```

### The Skill File

The CodeOns skill lives at `.bob/skills/code-ons/SKILL.md` in this repo.

Any developer can copy this skill into their own Bob workspace and get the same workflow on any codebase — in any language.

**To invoke it:**
- Natural language: *"I've inherited this codebase, help me understand it"*
- Direct command: `/code-ons`

---

## Demos

### Demo 1 — `project_x/` (synthetic messy repo)

A deliberately undocumented Python data analysis project built to show the before/after contrast clearly.

**Before CodeOns:**
```
project_x/
├── config.json      ← cryptic single-letter keys (p, t, n, m, d, x, z, q, r, k)
├── run.py           ← entry point, zero comments
├── processor.py     ← go(), smry(), cryptic variable names (pp, tt, mm, zz, rr)
├── helper.py        ← f1(), f2(), f3(), f4(), no docstrings
└── data/
    └── input.csv    ← 10 rows, no column descriptions
```

**After CodeOns (generated in one session):**

| Output | Description |
|--------|-------------|
| `README.md` | Full project overview, pipeline description, config key table, function reference |
| `SETUP.md` | Python version requirements, venv setup, install and run instructions |
| `CHANGES.md` | Every bug found and fixed with before/after code |
| Inline comments | Added to all `.py` files |
| `requirements.txt` | Auto-generated from codebase analysis |

**Bugs found and fixed automatically:**

| Bug | Location | Impact |
|-----|----------|--------|
| `inplace=True` on DataFrame slice — imputation silently failed | `helper.py:27` | Critical — halved usable dataset |
| Unused `import json` | `processor.py:2` | Low |
| No error handling for missing config/CSV | `run.py` | Medium |

---

### Demo 2 — `Python/` (real public repo)

CodeOns applied to a real public GitHub repository: [joeyajames/Python](https://github.com/joeyajames/Python) — 50+ standalone scripts with no documentation.

**One sentence triggered the full workflow:**
> *"I've inherited the codebase in the Python/ folder, help me understand it"*

**Result — 24/24 tasks completed autonomously:**
- Explored 24 files in 22 seconds
- Generated README, SETUP, CHANGES, requirements.txt
- Found and fixed 5 real bugs with exact line numbers
- Added inline comments to all key source files
- Ran validation on fixed scripts to confirm they pass

**Real bugs found:**

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `Sorting Algorithms/quick_sort.py:8` | `threshold` used but never defined → NameError | Added `threshold = 4` |
| 2 | `Sorting Algorithms/insertion_sort.py:17` | Bounds check too late → silent `A[-1]` access | Swapped condition order |
| 3 | `LinkedLists/DoublyLinkedList1.py:56` | Head never unlinked on remove | Fixed root assignment |
| 4 | `HashMap.py:52` | `keys()` returned wrong type, dropped chained entries | Rewrote with inner loop |
| 5 | `BinaryToDecimal.py:26` | Wrong base in modulo → all conversions wrong | Fixed `% toBase` → `% fromBase` |

---

## IBM Bob 2.0 Features Used

| Feature | How it was used |
|---------|----------------|
| **Custom Skill (`code-ons`)** | Reusable 9-step onboarding workflow, auto-activates on natural language trigger |
| **Agent mode** | Autonomous multi-step execution across entire workflow |
| **Parallel tasks** | 4-track analysis running simultaneously; docs generated in parallel |
| **Subagents** | Separate focused steps for scan, analyze, document, fix, validate |
| **Document understanding** | Read and reasoned across all project files in context |
| **Code execution** | Ran fixed scripts to validate bug fixes |

---

## Impact

| Metric | Manual | CodeOns |
|--------|--------|---------|
| Time to understand codebase | 2–3 hours | ~2 minutes |
| Time to write README + SETUP | 1–2 hours | ~1 minute |
| Bugs caught before running | 0 (hidden) | 5 (auto-detected + fixed) |
| Files changed per session | — | 22 files |
| Works on any language/repo | No (manual effort) | Yes (reusable skill) |

---

## Repository Structure

```
CodeOns/
├── .bob/
│   └── skills/
│       └── code-ons/
│           └── SKILL.md          ← the reusable CodeOns skill
├── project_x/                    ← Demo 1: synthetic messy repo
│   ├── config.json
│   ├── run.py
│   ├── processor.py
│   ├── helper.py
│   ├── data/input.csv
│   ├── README.md                 ← generated by CodeOns
│   ├── SETUP.md                  ← generated by CodeOns
│   └── CHANGES.md                ← generated by CodeOns
├── Python/                       ← Demo 2: real public repo
│   ├── README.md                 ← generated by CodeOns
│   ├── SETUP.md                  ← generated by CodeOns
│   ├── CHANGES.md                ← generated by CodeOns
│   └── requirements.txt          ← generated by CodeOns
├── bob_sessions/                 ← mandatory Bob session screenshots
│   ├── task01_project_x_creation.png
│   └── task02_python_repo_onboarding.png
└── README.md                     ← this file
```

---

*Built with IBM Bob 2.0 — IBM Bob 2.0 Hackathon, September 2026.*
