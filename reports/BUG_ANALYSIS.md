# Bug Analysis Report

## Selected Repository

The selected allowed repository is [`martinpeck/broken-python`](https://github.com/martinpeck/broken-python). It was chosen because it contains small, intentionally broken Python scripts that can be fully reverse-engineered, fixed, tested, and documented within the EX04 scope.

Local upstream copy: `data/upstream_broken_python/`

Fixed copy: `fixed/broken-python/`

## Bugs Identified

| File | Bug type | Root cause |
|---|---|---|
| `mathsquiz/mathsquiz.py` | Syntax and logic | Mixed Python 2/3 syntax, assignment in conditionals, invalid branching, wrong answers, missing score updates. |
| `mathsquiz/mathsquiz-step2.py` | State coupling | `print_final_scores(final_score)` ignores its parameter and reads global `score`. |
| `mathsquiz/mathsquiz-step3.py` | State coupling and testability | Final score function reads global `score`; random quiz behavior is not isolated for tests. |
| `polygons/polygons.py` | Syntax and algorithm | Invalid `new Polygon(...)`, undefined `Object`, hard-coded formulas, fixed six-side drawing loop. |

## Root Cause Themes

The common problem is not just syntax. The upstream examples mix interactive IO, computation, global state, and script execution. That makes them fragile and difficult to test.

## Fix Summary

The fixed copy separates pure logic from interaction, adds `__main__` guards, removes global-score coupling, implements correct formulas, and adds tests proving both the upstream failures and the repaired behavior.

See `reports/BROKEN_PYTHON_REPAIR_MATRIX.md` for file-by-file evidence.
