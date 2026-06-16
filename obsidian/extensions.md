# Original Extensions

## Dynamic Hot Context

The `hot.md` page is designed as the small context packet an agent should read first. It mirrors the assignment idea of generating a dynamic hot path from graph evidence.

## Centrality-Based Suspect Ranking

`graph_builder.py` adds a simple degree centrality score to each node in `artifacts/graph.json`. This supports ranking investigation targets before spending tokens on raw code.

## Impact Report

Changing `parse_plan` affects task construction and scheduler inputs but not the scheduler algorithm. That impact boundary is documented in `BUG_ANALYSIS.md` and covered by regression tests.
