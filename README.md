# LangGraph Basics

This repository is a small, teaching-first Python project for learning LangGraph concepts step by step.

## Project Layout

```text
langgraph-basics/
├─ .env.example
├─ .gitignore
├─ .python-version
├─ docs/
│  ├─ development.md
│  ├─ module-1.md
│  ├─ module-2.md
│  ├─ module-3.md
│  ├─ module-4.md
│  ├─ module-5.md
│  ├─ module-6.md
│  ├─ module-7.md
│  └─ project-spec.md
├─ pyproject.toml
├─ uv.lock
├─ README.md
├─ src/
│  └─ my_agent/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ settings.py
│     ├─ prompts/
│     │  └─ system.txt
│     ├─ tools/
│     │  ├─ agent_tools.py
│     │  ├─ __init__.py
│     │  └─ expense_db.py
│     ├─ workflows/
│     │  ├─ first_graph.py
│     │  ├─ gemini_chat_graph.py
│     │  ├─ loop_agent_graph.py
│     │  ├─ memory_graph.py
│     │  ├─ openai_chat_graph.py
│     │  ├─ planner.py
│     │  ├─ routing_graph.py
│     │  └─ tool_agent_graph.py
│     └─ models/
│        └─ schemas.py
├─ tests/
│  ├─ test_module_seven.py
│  ├─ test_module_six.py
│  ├─ test_module_five.py
│  ├─ test_module_four.py
│  ├─ test_module_one.py
│  ├─ test_module_three.py
│  ├─ test_module_two.py
│  └─ test_settings.py
└─ scripts/
   ├─ check.sh
   └─ dev.sh
   ├─ lint.sh
   └─ test.sh
```

## Quick Start

1. Install or sync dependencies:

```bash
uv sync --dev
```

2. Create a local env file:

```bash
cp .env.example .env
```

3. Run the demo:

```bash
./scripts/dev.sh --module 7 --provider openai --thread-id demo-thread "My name is Hemant."
./scripts/dev.sh --module 7 --provider gemini --thread-id demo-thread "My name is Hemant."
./scripts/dev.sh --module 6 --thread-id demo-thread "My name is Hemant"
./scripts/dev.sh --module 5 "What is 2 + 2?"
./scripts/dev.sh --module 4 "calculate 2 + 2"
./scripts/dev.sh --module 3 "solve math 2 + 2"
./scripts/dev.sh --module 2 "How to write Python code?"
./scripts/dev.sh --module 1 "What is 7 + 5?"
```

4. Run quality checks:

```bash
./scripts/check.sh
```

## Docs

- Development workflow: [docs/development.md](docs/development.md)
- Module 1 walkthrough: [docs/module-1.md](docs/module-1.md)
- Module 2 walkthrough: [docs/module-2.md](docs/module-2.md)
- Module 3 walkthrough: [docs/module-3.md](docs/module-3.md)
- Module 4 walkthrough: [docs/module-4.md](docs/module-4.md)
- Module 5 walkthrough: [docs/module-5.md](docs/module-5.md)
- Module 6 walkthrough: [docs/module-6.md](docs/module-6.md)
- Module 7 walkthrough: [docs/module-7.md](docs/module-7.md)
- Project conventions and specs: [docs/project-spec.md](docs/project-spec.md)

## Module 1: Core Concepts of LangGraph

This module teaches only three ideas:

1. `State`
2. `Node`
3. `Edge`

If these are clear, most of LangGraph stops feeling complicated.

### First Mental Model

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

### State

State is the shared notebook for the workflow.

Every node can:

- read from the state
- write updates back to the state

Example state from this repo:

```python
{
    "question": "What is 7 + 5?",
    "classification": "math",
    "result": "12",
    "answer": "Math route selected. Calculator result: 12."
}
```

In this project, the state schema lives in [src/my_agent/models/schemas.py](src/my_agent/models/schemas.py).

### Nodes

A node is just a function:

1. It receives the current state.
2. It does one job.
3. It returns only the fields it wants to update.

Examples in [src/my_agent/workflows/planner.py](src/my_agent/workflows/planner.py):

- `classify_question`
- `calculator`
- `search_docs`
- `llm_answer`
- `format_answer`

### Edges

Edges decide what runs next.

In this repo, `decide_next_step` is the routing edge:

- `math` -> `calculator`
- `coding` -> `search_docs`
- `general` -> `llm_answer`

That is the rule to remember:

- State = facts
- Nodes = actions
- Edges = decisions

## File Map

- [src/my_agent/main.py](src/my_agent/main.py) runs Modules 1, 2, 3, 4, 5, 6, or 7 from the CLI.
- [src/my_agent/workflows/first_graph.py](src/my_agent/workflows/first_graph.py) contains the real LangGraph example for Module 2.
- [src/my_agent/workflows/loop_agent_graph.py](src/my_agent/workflows/loop_agent_graph.py) contains the looping agent graph for Module 5.
- [src/my_agent/workflows/memory_graph.py](src/my_agent/workflows/memory_graph.py) contains the memory and persistence graph for Module 6.
- [src/my_agent/workflows/openai_chat_graph.py](src/my_agent/workflows/openai_chat_graph.py) contains the OpenAI-backed chatbot graph for Module 7.
- [src/my_agent/workflows/gemini_chat_graph.py](src/my_agent/workflows/gemini_chat_graph.py) contains the Gemini-backed chatbot graph for Module 7.
- [src/my_agent/workflows/routing_graph.py](src/my_agent/workflows/routing_graph.py) contains the conditional routing graph for Module 3.
- [src/my_agent/workflows/tool_agent_graph.py](src/my_agent/workflows/tool_agent_graph.py) contains the tool-using agent graph for Module 4.
- [src/my_agent/workflows/planner.py](src/my_agent/workflows/planner.py) contains the Module 1 manual workflow logic.
- [src/my_agent/tools/agent_tools.py](src/my_agent/tools/agent_tools.py) contains the calculator and search tools for Module 4.
- [src/my_agent/tools/expense_db.py](src/my_agent/tools/expense_db.py) is a simple local tool used by the `search_docs` node.
- [src/my_agent/settings.py](src/my_agent/settings.py) shows a clean settings pattern for later modules.

Module 1 intentionally uses plain Python orchestration so you can learn the concepts before adding `StateGraph`, `add_node`, `add_edge`, and `compile()`.

The full walkthrough lives in [docs/module-1.md](docs/module-1.md).

## Module 2: Your First LangGraph Program

Module 2 introduces the real LangGraph primitives:

- `StateGraph`
- `add_node()`
- `add_edge()`
- `compile()`

The Module 2 graph is:

```text
START -> classify -> answer -> END
```

Run it with:

```bash
./scripts/dev.sh --module 2 "How to write Python code?"
```

The final state looks like this:

```json
{
  "question": "How to write Python code?",
  "category": "coding",
  "answer": "This is a programming question."
}
```

The full walkthrough lives in [docs/module-2.md](docs/module-2.md).

## Module 3: Conditional Routing in LangGraph

Module 3 introduces `add_conditional_edges()` so the graph can branch dynamically.

The Module 3 graph is:

```text
                classify
              /    |     \
           math  coding  general
            |      |       |
        math_node coding_node general_node
            |      |       |
           END    END     END
```

Run it with:

```bash
./scripts/dev.sh --module 3 "solve math 2 + 2"
```

The final state looks like this:

```json
{
  "question": "solve math 2 + 2",
  "category": "math",
  "answer": "Use a calculator for this math question."
}
```

The full walkthrough lives in [docs/module-3.md](docs/module-3.md).

## Module 4: Building a Tool-Using Agent in LangGraph

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

The Module 4 graph is:

```text
START -> decide_tool -> [calculator | search | final_answer] -> END
```

Run it with:

```bash
./scripts/dev.sh --module 4 "calculate 2 + 2"
```

The final state looks like this:

```json
{
  "question": "calculate 2 + 2",
  "tool": "calculator",
  "tool_result": "Calculator result: 4",
  "answer": "Final answer based on tool result: Calculator result: 4"
}
```

The full walkthrough lives in [docs/module-4.md](docs/module-4.md).

## Module 5: Agent Loops in LangGraph

Module 5 introduces the classic agent loop:

```text
START -> agent -> [tools -> agent | END]
```

Run it with:

```bash
./scripts/dev.sh --module 5 "What is 2 + 2?"
```

The final state looks like this:

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

The full walkthrough lives in [docs/module-5.md](docs/module-5.md).

## Module 6: Memory and Persistence in LangGraph

Module 6 introduces thread-scoped memory using a checkpointer and `thread_id`.

The Module 6 graph is:

```text
START -> chatbot -> END
```

Run it with:

```bash
./scripts/dev.sh --module 6 --thread-id demo-thread "My name is Hemant"
```

The CLI runs two turns in one process so the memory behavior is visible:

1. your first message
2. a follow-up message, defaulting to `What did I tell you?`

The full walkthrough lives in [docs/module-6.md](docs/module-6.md).

## Module 7: Real LLM Chatbot with Memory

Module 7 combines:

- message state
- `add_messages`
- `InMemorySaver`
- a real provider-backed chat model
- `thread_id`-scoped memory

The Module 7 graph is:

```text
START -> chatbot -> END
```

Run it with:

```bash
./scripts/dev.sh --module 7 --provider openai --thread-id demo-thread "My name is Hemant."
./scripts/dev.sh --module 7 --provider gemini --thread-id demo-thread "My name is Hemant."
```

The CLI runs two turns in one process so you can see memory across turns with the same thread.

The full walkthrough lives in [docs/module-7.md](docs/module-7.md).

## Common Commands

- Run Module 7 with OpenAI: `./scripts/dev.sh --module 7 --provider openai --thread-id demo-thread "My name is Hemant."`
- Run Module 7 with Gemini: `./scripts/dev.sh --module 7 --provider gemini --thread-id demo-thread "My name is Hemant."`
- Run Module 6: `./scripts/dev.sh --module 6 --thread-id demo-thread "My name is Hemant"`
- Run Module 5: `./scripts/dev.sh --module 5 "What is 2 + 2?"`
- Run Module 4: `./scripts/dev.sh --module 4 "calculate 2 + 2"`
- Run Module 3: `./scripts/dev.sh --module 3 "solve math 2 + 2"`
- Run Module 2: `./scripts/dev.sh --module 2 "How to write Python code?"`
- Run Module 1: `./scripts/dev.sh --module 1 "What is 7 + 5?"`
- Run tests: `./scripts/test.sh`
- Run lint: `./scripts/lint.sh`
- Run lint + tests: `./scripts/check.sh`

## Mini Exercise

Try changing the classifier in [src/my_agent/workflows/planner.py](src/my_agent/workflows/planner.py):

- Add a new route like `finance`
- Create a new node for that route
- Update the edge function so the graph can branch to it

That is exactly how you think when designing a LangGraph workflow.

## Next Module

Module 8 should add real tool calling with an LLM plus memory:

```text
User
 ↓
model decides
 ↓
tool call
 ↓
model interprets result
 ↓
answer with memory
```

That is where LangGraph starts to feel like a complete agent platform.
