# Python for Data Science & AI — Practice Track

A test-driven practice curriculum. Every module is a folder with two files:

- `exercises.py` — function stubs with docstrings and `TODO`. **You write the code here.**
- `test_exercises.py` — the grader. **Don't edit this.** It defines what "correct" means.

## How to work

```bash
cd practice

# Run one module
pytest 00_python_basics -v

# Run one exercise while you work on it
pytest 00_python_basics -v -k evens

# Stop at the first failure (best default while grinding)
pytest 00_python_basics -x

# Run everything you've done so far
pytest -v
```

Green means done. Read the failure output — it's written to tell you *what* was expected,
not just that something broke.

## Rules of the game

1. Do them in order. Each exercise builds on the previous one.
2. Don't look up the answer first. Get it wrong, read the traceback, fix it. That's the rep.
3. When you're stuck for more than ~10 minutes, ask me — I'll explain the concept, not just
   hand you the line.
4. When a module goes green, ask me to review it. Passing tests ≠ idiomatic code, and the gap
   between those two is most of what separates a junior from a senior.

## Curriculum

| # | Module | Focus | Status |
|---|--------|-------|--------|
| 00 | `00_python_basics` | Comprehensions, dicts, exceptions, files, generators, classes | ▶️ start here |
| 01 | `01_pandas` | Loading, cleaning, groupby, joins, reshaping, time series | 🔒 |
| 02 | `02_numpy_stats` | Vectorization, broadcasting, distributions, hypothesis testing | 🔒 |
| 03 | `03_ml_sklearn` | Pipelines, CV, feature engineering, evaluation, leakage | 🔒 |
| 04 | `04_llm_ai` | Prompting, tool-use agents, RAG, evaluation | 🔒 |

Modules unlock as you finish the one before. Ask and I'll write the next one.

## Setup

```bash
pip install -r requirements.txt
```
