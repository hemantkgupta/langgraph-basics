#!/usr/bin/env bash
set -euo pipefail

QUESTION="${1:-}"

if [[ -n "${QUESTION}" ]]; then
  PYTHONPATH=src ./.venv/bin/python -m my_agent.main "${QUESTION}"
else
  PYTHONPATH=src ./.venv/bin/python -m my_agent.main
fi
