# Module 3: Conditional Routing in LangGraph

Module 3 introduces the most important LangGraph feature for real agents: conditional edges.

The graph is no longer linear:

```text
                classify
              /    |     \
           math  coding  general
            |      |       |
        math_node coding_node general_node
            |      |       |
           END    END     END
```

## Why Routing Exists

Agents need to decide what to do next.

Examples:

- math question -> calculator path
- coding question -> documentation search path
- general question -> direct LLM path

That choice is what conditional routing models.

## Key API

LangGraph routing uses `add_conditional_edges()`:

```python
graph.add_conditional_edges(
    "classify",
    route_question,
    {
        "math": "math_node",
        "coding": "coding_node",
        "general": "general_node",
    },
)
```

The router function returns a string, and that string selects the next node.

## State

Module 3 uses a small `TypedDict` state in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleThreeState(TypedDict, total=False):
    question: str
    category: ModuleThreeCategory
    answer: str
```

## Nodes

Module 3 lives in [src/my_agent/workflows/routing_graph.py](../src/my_agent/workflows/routing_graph.py).

Nodes:

- `classify`
- `math_node`
- `coding_node`
- `general_node`

Router:

- `route_question`

The important split is:

- the node updates state
- the router decides the next edge

## Build The Graph

```python
graph = StateGraph(ModuleThreeState)
graph.add_node("classify", classify)
graph.add_node("math_node", math_node)
graph.add_node("coding_node", coding_node)
graph.add_node("general_node", general_node)
graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_question,
    {
        "math": "math_node",
        "coding": "coding_node",
        "general": "general_node",
    },
)
graph.add_edge("math_node", END)
graph.add_edge("coding_node", END)
graph.add_edge("general_node", END)
app = graph.compile()
```

## Run It

Command line:

```bash
./scripts/dev.sh --module 3 "solve math 2 + 2"
```

Direct Python:

```bash
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 3 "solve math 2 + 2"
```

## Example Output

```json
{
  "question": "solve math 2 + 2",
  "category": "math",
  "answer": "Use a calculator for this math question."
}
```

## Key Insight

Good LangGraph design is:

- LLM decides
- graph routes
- tools execute

This keeps the system controllable, debuggable, and deterministic.

## Next Module

Module 4 turns those routed branches into a real tool-using agent graph with explicit tool nodes and a final answer step.
