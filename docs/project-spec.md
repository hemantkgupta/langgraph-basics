# Project Spec

## Purpose

This repository teaches LangGraph fundamentals in small modules. Module 1 is intentionally simple and focuses on the core mental model:

- State = facts
- Nodes = actions
- Edges = decisions

## Scope

This project is not yet a production agent. It is a learning scaffold that should stay easy to read, test, and extend.

## Repository Conventions

- Application code lives under `src/my_agent/`
- Tests live under `tests/`
- Reusable shell entrypoints live under `scripts/`
- Environment configuration belongs in [src/my_agent/settings.py](../src/my_agent/settings.py)
- Prompt text belongs in `src/my_agent/prompts/`
- Workflow orchestration belongs in `src/my_agent/workflows/`
- Tool integrations belong in `src/my_agent/tools/`

## State Spec

The state contract for Module 1 is defined in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py).

Current fields:

- `question`
- `classification`
- `documents`
- `result`
- `answer`

Rules:

- State holds shared workflow facts
- Nodes should read state and return partial updates
- Nodes should avoid mutating the state directly
- New state fields should be added to the schema first

## Node Spec

Nodes live in [src/my_agent/workflows/planner.py](../src/my_agent/workflows/planner.py).

Rules:

- Each node should have one clear responsibility
- Node names should describe the action they perform
- Node output should be deterministic unless randomness is required for the lesson
- Nodes should return only the keys they update

Current nodes:

- `classify_question`
- `calculator`
- `search_docs`
- `llm_answer`
- `format_answer`

## Edge Spec

Routing is handled by `decide_next_step`.

Rules:

- Edges should be explicit and easy to trace
- Every route returned by an edge must map to a valid next node
- When adding a new route, update both routing logic and tests

Current routes:

- `math`
- `coding`
- `general`

## Testing Spec

Minimum expectations for workflow changes:

- Keep settings coverage in [tests/test_settings.py](../tests/test_settings.py)
- Keep route coverage in [tests/test_smoke.py](../tests/test_smoke.py)
- Add or update tests for every new route or state field

Canonical commands:

```bash
./scripts/test.sh
./scripts/lint.sh
./scripts/check.sh
```

## Module Boundary

Module 1 does not require the real `langgraph` package yet. That is deliberate.

Module 2 should introduce:

- `StateGraph`
- `add_node`
- `add_edge`
- `compile()`
