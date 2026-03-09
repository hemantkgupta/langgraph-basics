# Development Guide

## Prerequisites

- Python `3.12.2`
- `uv`

Check installed versions:

```bash
python --version
uv --version
```

## Setup

1. Sync dependencies into `.venv`:

```bash
uv sync --dev
```

2. Create a local env file:

```bash
cp .env.example .env
```

3. Optional: update `.env` values if you want a different default question.

## Run The Demo

Use the helper script:

```bash
./scripts/dev.sh --module 7 --provider openai --thread-id demo-thread "My name is Hemant."
./scripts/dev.sh --module 7 --provider gemini --thread-id demo-thread "My name is Hemant."
./scripts/dev.sh --module 6 --thread-id demo-thread "My name is Hemant"
./scripts/dev.sh --module 5 "What is 2 + 2?"
./scripts/dev.sh --module 4 "calculate 2 + 2"
./scripts/dev.sh --module 3 "solve math 2 + 2"
./scripts/dev.sh --module 2 "How to write Python code?"
./scripts/dev.sh --module 1 "What is 7 + 5?"
./scripts/dev.sh --module 1 "How should I store expense records in Python?"
```

Direct module execution also works:

```bash
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 7 --provider openai --thread-id demo-thread "My name is Hemant."
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 7 --provider gemini --thread-id demo-thread "My name is Hemant."
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 6 --thread-id demo-thread "My name is Hemant"
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 5 "What is 2 + 2?"
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 4 "calculate 2 + 2"
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 3 "solve math 2 + 2"
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 2 "How to write Python code?"
PYTHONPATH=src ./.venv/bin/python -m my_agent.main --module 1 "What is LangGraph?"
```

## Run Tests

Canonical command:

```bash
./scripts/test.sh
```

Direct command:

```bash
PYTHONPATH=src ./.venv/bin/python -m pytest
```

## Run Lint

Canonical command:

```bash
./scripts/lint.sh
```

Direct command:

```bash
./.venv/bin/python -m ruff check src tests
```

## Run All Checks

```bash
./scripts/check.sh
```

## Environment Variables

The project currently uses a small settings surface:

- `MY_AGENT_APP_NAME`
- `MY_AGENT_ENVIRONMENT`
- `MY_AGENT_DEFAULT_QUESTION`
- `MY_AGENT_OPENAI_MODEL`
- `MY_AGENT_GEMINI_MODEL`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`

The env contract is defined in [src/my_agent/settings.py](../src/my_agent/settings.py).

## LangGraph Dependencies

Modules 2, 3, 4, 5, 6, and 7 now depend on:

- `langgraph`
- `langchain`
- `langchain-openai`
- `langchain-google-genai`

They are declared in [pyproject.toml](../pyproject.toml), so `uv sync --dev` installs them.

## Current Quality Bar

Before committing changes:

1. Run `./scripts/lint.sh`
2. Run `./scripts/test.sh`
3. If you changed the workflow, run `./scripts/dev.sh` with at least one sample question
