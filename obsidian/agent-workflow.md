# Agent Workflow

## Stages

1. `load_graph_context` reads only `index.md`, `hot.md`, and `GRAPH_REPORT.md`.
2. `choose_suspects` selects parser and parser tests from graph evidence.
3. `inspect_suspects` reads focused source files.
4. `explain_fix` records root cause and fix summary.

## LangGraph Compatibility

`agent_workflow.py` includes `build_langgraph_workflow()`. If `langgraph` is installed, the same stages can be compiled into a real `StateGraph`. Without that optional dependency, the deterministic local runner keeps the project executable in a clean Python environment.

## Context Reduction Mechanism

The workflow does not read raw source until graph and Obsidian pages identify the hot path.
