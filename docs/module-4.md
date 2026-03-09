# Module 4: Building a Tool-Using Agent in LangGraph

Module 4 introduces the classic tool-using agent pattern:

```text
User Question
      ↓
LLM decides what tool to use
      ↓
Execute tool
      ↓
LLM produces final answer
```

In this repo, the LLM decision is still simulated so the graph stays easy to inspect.

## Agent Graph

```text
             decide_tool
                  |
      ┌───────────┼───────────┐
      |           |           |
 calculator    search     final_answer
      |           |           |
      └───────────┴───────────┘
                  |
                 END
```

`decide_tool` routes to:

- `calculator`
- `search`
- `final_answer` when no tool is needed

## State

Module 4 uses this state in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleFourState(TypedDict, total=False):
    question: str
    tool: ModuleFourTool
    tool_result: str
    answer: str
```

## Nodes

The Module 4 workflow lives in [src/my_agent/workflows/tool_agent_graph.py](../src/my_agent/workflows/tool_agent_graph.py).

Nodes:

- `decide_tool`
- `calculator`
- `search`
- `final_answer`

Router:

- `route_tool`

The actual tool functions live in [src/my_agent/tools/agent_tools.py](../src/my_agent/tools/agent_tools.py).

## Build The Graph

```python
graph = StateGraph(ModuleFourState)
graph.add_node("decide_tool", decide_tool)
graph.add_node("calculator", calculator)
graph.add_node("search", search)
graph.add_node("final_answer", final_answer)
graph.add_edge(START, "decide_tool")
graph.add_conditional_edges(
    "decide_tool",
    route_tool,
    {
        "calculator": "calculator",
        "search": "search",
        "none": "final_answer",
    },
)
graph.add_edge("calculator", "final_answer")
graph.add_edge("search", "final_answer")
graph.add_edge("final_answer", END)
app = graph.compile()
```

## Run It

Command line:

```bash
./scripts/dev.sh --module 4 "calculate 2 + 2"
./scripts/dev.sh --module 4 "What is LangGraph?"
```

Direct Python:

```bash
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 4 "calculate 2 + 2"
```

## Example Output

```json
{
  "question": "calculate 2 + 2",
  "tool": "calculator",
  "tool_result": "Calculator result: 4",
  "answer": "Final answer based on tool result: Calculator result: 4"
}
```

## Why This Matters

This is the first module that looks like a real AI agent:

- a decision node chooses the next action
- tool nodes execute deterministic work
- a final answer node turns tool output into a user-facing response

That is the core pattern behind coding assistants, research agents, and workflow agents.

## Next Module

Module 5 should add loops so the agent can think, use a tool, observe the result, and decide again.
