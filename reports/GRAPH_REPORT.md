# Graph Report

## Central Nodes

| Node | Why it matters |
|---|---|
| `parser.py::parse_plan` | Converts raw task text into the domain object and contains the fixed validation logic. |
| `scheduler.py::topological_order` | Proves whether the parsed dependency graph is usable. |
| `agent_workflow.py::run_workflow` | Orchestrates graph-first investigation. |
| `graph_builder.py::build_graph` | Produces `artifacts/graph.json` from AST structure. |

## Communities

| Community | Files | Responsibility |
|---|---|---|
| Domain and scheduling | `domain.py`, `parser.py`, `scheduler.py` | Business rules of the investigated system. |
| Knowledge graph | `graph_builder.py`, `artifacts/graph.json` | Static extraction and navigation. |
| Agent and evidence | `agent_workflow.py`, `token_meter.py`, `reports/`, `obsidian/` | Context reduction and debugging narrative. |

## God Nodes and Risk

No severe God Node remains. The highest-risk area is `parse_plan` because it bridges raw input, domain construction, and validation. The mitigation is focused tests around valid forward references, missing dependencies, and cycles.
