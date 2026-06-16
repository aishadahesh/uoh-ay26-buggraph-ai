# Worklog

## Step 1 - Assignment Interpretation

The assignment requires more than fixing a bug. It asks for a complete investigation workflow: reverse engineering, graph representation, Obsidian documentation, agentic debugging, token-efficiency comparison, and before/after proof.

## Step 2 - Scope Selection

A compact scheduler bug was selected because it is small enough to fully document but still contains meaningful architecture: parsing, domain objects, dependency validation, topological ordering, and schedule calculation.

## Step 3 - Reverse Engineering

The upstream snapshot mixed parsing, dependency validation, and insertion in a single loop. Graph navigation made `parse_plan` the central hot node because scheduler correctness depended on parser output.

## Step 4 - Bug Reproduction

The failure case was a forward dependency. A valid task plan failed only because row order placed the dependency after the dependent task.

## Step 5 - Fix and Enhancement

The parser was redesigned into a two-pass flow: parse all tasks, validate dependencies, then build the plan. This is both a bug fix and a design improvement because validation no longer depends on input ordering.

## Step 6 - Evidence

Unit tests, graph output, Obsidian pages, and reports were added to make the reasoning auditable.
