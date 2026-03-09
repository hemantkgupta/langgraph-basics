# Module 2: Your First LangGraph Program

Module 2 turns the manual workflow from Module 1 into a real LangGraph app.

The graph is intentionally small:

```text
START -> classify -> answer -> END
```

## Core Objects

These are the four LangGraph objects to know first:

- `StateGraph`: creates the workflow graph
- `add_node()`: adds a step
- `add_edge()`: connects steps
- `compile()`: builds the runnable graph

## State

Module 2 uses a small `TypedDict` state in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleTwoState(TypedDict, total=False):
    question: str
    category: ModuleTwoCategory
    answer: str
```

## Nodes

The two nodes live in [src/my_agent/workflows/first_graph.py](../src/my_agent/workflows/first_graph.py):

- `classify`
- `answer`

`classify` reads `question` and writes `category`.

`answer` reads `category` and writes `answer`.

## Build The Graph

The graph builder is:

```python
graph = StateGraph(ModuleTwoState)
graph.add_node("classify", classify)
graph.add_node("answer", answer)
graph.add_edge(START, "classify")
graph.add_edge("classify", "answer")
graph.add_edge("answer", END)
app = graph.compile()
```

## Run It

Command line:

```bash
./scripts/dev.sh --module 2 "How to write Python code?"
```

Direct Python:

```bash
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 2 "How to write Python code?"
```

## Example Output

```json
{
  "question": "How to write Python code?",
  "category": "coding",
  "answer": "This is a programming question."
}
```

## What Changed From Module 1

- Module 1 used plain Python orchestration
- Module 2 uses a real compiled `StateGraph`
- LangGraph now merges state automatically as nodes run

## Why `langchain` And Provider Packages Are Installed

This module does not need an LLM yet.

The dependencies are installed now because the later modules move from fixed answers to real model-backed nodes.
