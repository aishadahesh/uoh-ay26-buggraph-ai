# PLAN / PRD - EX04 Graph-Guided Reverse Engineering

## Product Goal

Create a professional Python submission that demonstrates how graph-guided reverse engineering helps understand unfamiliar code, locate a bug, fix it, document the architecture, and prove token-efficiency compared with naive raw-code reading.

## Scope

The project investigates a compact Python task scheduler based on the selected allowed repository option, `martinpeck/broken-python`. The selected scope is intentionally bounded so every required EX04 artifact can be completed: runnable code, tests, graph output, Obsidian vault, bug report, diagrams, token report, and an agent workflow.

## User Stories

- As a reviewer, I can run the tests and see the bug is fixed.
- As a reviewer, I can open the Obsidian vault and navigate from `index.md` to `hot.md`, architecture, bug analysis, and token evidence.
- As a reviewer, I can inspect `artifacts/graph.json` and understand which nodes are central.
- As a student team, we can explain why graph-guided navigation reduced context and token usage.

## Functional Requirements

1. Parse pipe-delimited task plans into domain objects.
2. Accept valid forward dependency references.
3. Reject missing dependencies with clear errors.
4. Detect cycles during scheduling.
5. Generate an AST-based graph artifact.
6. Run a graph-guided agent workflow that reads documentation first and source second.
7. Produce token-efficiency evidence for naive and graph-guided modes.

## Non-Functional Requirements

- Keep source files below the 150-code-line guideline.
- Use a clear modular structure: `src`, `tests`, `docs`, `reports`, `obsidian`, `artifacts`, `data`.
- Make the project runnable with only the Python standard library.
- Keep optional LangGraph support isolated so missing optional dependencies do not break basic execution.

## Acceptance Criteria

- `python -m unittest discover -s tests` passes.
- `python -m gaphify_re graph --repo .` writes `artifacts/graph.json`.
- `python -m gaphify_re agent --repo .` prints root cause and fix summary.
- `python -m gaphify_re tokens --repo .` prints both token modes.
- README explains what was implemented, what was found, and what changed.
