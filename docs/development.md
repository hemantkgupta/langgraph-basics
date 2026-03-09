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
./scripts/dev.sh
./scripts/dev.sh "What is 7 + 5?"
./scripts/dev.sh "How should I store expense records in Python?"
```

Direct module execution also works:

```bash
PYTHONPATH=src ./.venv/bin/python -m my_agent.main
PYTHONPATH=src ./.venv/bin/python -m my_agent.main "What is LangGraph?"
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
- `OPENAI_API_KEY`

The env contract is defined in [src/my_agent/settings.py](../src/my_agent/settings.py).

## Current Quality Bar

Before committing changes:

1. Run `./scripts/lint.sh`
2. Run `./scripts/test.sh`
3. If you changed the workflow, run `./scripts/dev.sh` with at least one sample question
