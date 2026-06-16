# Optimization and Enhancement Report

## Why Optimization Was Needed

The upstream `broken-python` files are teaching examples, so the assignment should not stop at making them compile. The goal is to debug them, reverse-engineer the design problems, and make the fixed copy easier to test and maintain.

## Improvements Performed

| Area | Before | After |
|---|---|---|
| Quiz questions | Repeated procedural blocks | Shared `Question` model and `run_quiz` function |
| User input | Hardwired `input()` everywhere | Injectable `input_fn` for tests |
| Output | Hardwired `print()` everywhere | Injectable `print_fn` for tests |
| Score reporting | Reads global `score` | Uses explicit function parameters |
| Polygon formulas | Hard-coded triangle/square fallback | General formula for any `sides >= 3` |
| Drawing | Always draws six sides | Draws `polygon.sides` sides |
| Script behavior | Runs prompts on import | Interactive code guarded by `__main__` |

## Result

The repaired copy is still recognizable as the original educational scripts, but the logic is testable, reusable, and documented. This supports the EX04 goal of improving code after understanding it through reverse engineering.
