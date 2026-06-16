# Architecture

## Block Diagram

```mermaid
flowchart LR
    Input[Task text] --> Parser[parser.py]
    Parser --> Domain[Task and ProjectPlan]
    Domain --> Scheduler[scheduler.py]
    Scheduler --> Finish[Finish times]
    Source[src package] --> Graph[graph_builder.py]
    Graph --> Json[artifacts/graph.json]
    Json --> Vault[Obsidian vault]
    Vault --> Agent[agent_workflow.py]
```

## OOP Diagram

```mermaid
classDiagram
    class Task {
        +str task_id
        +str title
        +int duration_hours
        +tuple depends_on
        +finish_time(starts_at, dependency_finishes)
    }
    class ProjectPlan {
        +dict tasks
        +add(task)
        +roots()
    }
    ProjectPlan "1" o-- "many" Task
    Parser ..> Task
    Parser ..> ProjectPlan
    Scheduler ..> ProjectPlan
```

## Extracted Insight

The original bug is architectural, not syntactic. Validation belongs after parsing has established the complete task-id universe.
