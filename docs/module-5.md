# Module 5: Agent Loops in LangGraph

Module 5 introduces the core agent loop pattern:

```text
START
  ↓
agent
  ↓
┌───────────────┐
│ tool needed?  │
└──────┬────────┘
       │ yes
       ↓
     tools
       ↓
     agent
       │
       no
       ↓
      END
```

This is the basic ReAct-style workflow:

- think
- use a tool
- observe the result
- think again
- finish when ready

## State

Module 5 uses this state in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleFiveState(TypedDict, total=False):
    question: str
    messages: list[str]
    tool_request: ModuleFiveToolRequest
    tool_result: str
    final_answer: str
    steps: int
```

The important additions are:

- `messages` to record the running trace
- `steps` to prevent infinite loops

## Nodes

The workflow lives in [src/my_agent/workflows/loop_agent_graph.py](../src/my_agent/workflows/loop_agent_graph.py).

Nodes:

- `agent`
- `tools`

Router:

- `route_after_agent`

The `agent` node decides whether to:

- request a tool
- answer directly
- stop because the max step count was reached
- finish after seeing a tool result

## Build The Graph

```python
graph = StateGraph(ModuleFiveState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        "end": END,
    },
)
graph.add_edge("tools", "agent")
app = graph.compile()
```

The key loop edge is:

```python
graph.add_edge("tools", "agent")
```

That is what makes the workflow iterative.

## Run It

Command line:

```bash
./scripts/dev.sh --module 5 "What is 2 + 2?"
./scripts/dev.sh --module 5 "Who is Ada Lovelace?"
```

Direct Python:

```bash
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 5 "What is 2 + 2?"
```

## Example Output

```json
{
  "question": "What is 2 + 2?",
  "messages": [
    "Need calculator",
    "Calculator returned 4",
    "Tool result received, finishing"
  ],
  "tool_request": "",
  "tool_result": "4",
  "final_answer": "The answer is based on tool result: 4",
  "steps": 2
}
```

## Stop Condition

Module 5 includes a max step guard.

If the agent exceeds the limit, it returns:

```text
Stopping because max steps reached.
```

This is the minimal protection every looping agent should have.

## Checkpointer Preview

Module 5 also includes an optional `InMemorySaver` hook:

```python
from langgraph.checkpoint.memory import InMemorySaver

app = build_module_five_graph().compile(checkpointer=InMemorySaver())
```

In this repo, `get_module_five_app(use_checkpointer=True)` enables that mode.

This is only a preview. Module 6 should go deeper into:

- thread memory
- checkpointing
- resumability
- multi-turn execution

## Why This Matters

This is the core LangGraph agent pattern:

- agent node = think
- tool node = act
- updated state = observe
- loop edge = think again

That is the foundation for ReAct agents, coding assistants, research agents, and tool-augmented copilots.
