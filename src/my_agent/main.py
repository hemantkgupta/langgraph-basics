from __future__ import annotations

import argparse
import json

from my_agent.settings import get_settings
from my_agent.workflows.planner import run_module_one_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Module 1 LangGraph basics demo.",
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Optional question to send through the workflow.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    question = args.question or settings.default_question
    run = run_module_one_workflow(question)

    print("Module 1: State, Nodes, Edges")
    print(f"Question: {question}")
    print()

    for snapshot in run.snapshots:
        print(f"Node: {snapshot.node}")
        print("Updates:")
        print(json.dumps(snapshot.updates, indent=2))
        print("State after:")
        print(json.dumps(snapshot.state_after, indent=2))
        print()

    print("Route taken:")
    print(" -> ".join(run.route))
    print()
    print("Final answer:")
    print(run.final_state["answer"])


if __name__ == "__main__":
    main()
