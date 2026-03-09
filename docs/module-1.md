# Module 1: Core Concepts of LangGraph

Module 1 teaches the three concepts that explain most LangGraph workflows:

1. `State`
2. `Node`
3. `Edge`

## First Mental Model

Think of a workflow like this:

```text
User question -> classify -> route -> answer
```

Graph view:

```text
[START]
   |
   v
classify_question
   |
   v
 decide_next_step
   |-----------|-----------|
   v           v           v
calculator  search_docs  llm_answer
   \           |           /
    \          |          /
     v         v         v
       format_answer
            |
            v
          [END]
```

## State

State is the shared notebook for the workflow.

Each node can:

- read from the state
- write updates back to the state

Module 1 state is defined in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class AgentState(TypedDict, total=False):
    question: str
    classification: Route
    documents: list[str]
    result: str
    answer: str
```

Example evolved state:

```python
{
    "question": "What is 7 + 5?",
    "classification": "math",
    "result": "12",
    "answer": "Math route selected. Calculator result: 12."
}
```

## Nodes

Nodes are just functions.

Each node:

1. receives the current state
2. does one job
3. returns partial state updates

Module 1 nodes live in [src/my_agent/workflows/planner.py](../src/my_agent/workflows/planner.py):

- `classify_question`
- `calculator`
- `search_docs`
- `llm_answer`
- `format_answer`

## Edges

Edges decide what runs next.

Module 1 uses `decide_next_step` to route between:

- `math` -> `calculator`
- `coding` -> `search_docs`
- `general` -> `llm_answer`

That is the key rule to remember:

- State = facts
- Nodes = actions
- Edges = decisions

## Run Module 1

```bash
./scripts/dev.sh --module 1 "What is 7 + 5?"
./scripts/dev.sh --module 1 "How should I store expense records in Python?"
```

## Testing

Module 1 behavior is covered in [tests/test_module_one.py](../tests/test_module_one.py).

Run it with:

```bash
./scripts/test.sh
```

## Why Module 1 Exists

Module 1 does not use the real `langgraph` package.

That is intentional. It teaches the mental model first, so Module 2 can focus on `StateGraph`, `add_node()`, `add_edge()`, and `compile()`.
