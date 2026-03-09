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
│     │  ├─ __init__.py
│     │  └─ expense_db.py
│     ├─ workflows/
│     │  ├─ first_graph.py
│     │  └─ planner.py
│     └─ models/
│        └─ schemas.py
├─ tests/
│  ├─ test_module_one.py
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

- [src/my_agent/main.py](src/my_agent/main.py) runs either Module 1 or Module 2 from the CLI.
- [src/my_agent/workflows/first_graph.py](src/my_agent/workflows/first_graph.py) contains the real LangGraph example for Module 2.
- [src/my_agent/workflows/planner.py](src/my_agent/workflows/planner.py) contains the Module 1 manual workflow logic.
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

## Common Commands

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

Module 3 should add conditional routing:

```text
         classify
        /   |   \
     math coding general
      |      |      |
 calculator search   llm
```

That is where LangGraph starts to feel like a real agent workflow.
