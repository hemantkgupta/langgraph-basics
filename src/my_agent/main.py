from __future__ import annotations

import argparse
import json

from my_agent.settings import get_settings
from my_agent.workflows.first_graph import invoke_module_two_workflow
from my_agent.workflows.routing_graph import invoke_module_three_workflow
from my_agent.workflows.planner import run_module_one_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a LangGraph basics module demo.",
    )
    parser.add_argument(
        "--module",
        choices=("1", "2", "3"),
        default="3",
        help="Which learning module to run.",
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

    if args.module == "1":
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
        return

    if args.module == "2":
        result = invoke_module_two_workflow(question)
        print("Module 2: Your First LangGraph Program")
        print(f"Question: {question}")
        print()
        print("Graph:")
        print("START -> classify -> answer -> END")
        print()
        print("Final state:")
        print(json.dumps(result, indent=2))
        return

    result = invoke_module_three_workflow(question)
    print("Module 3: Conditional Routing in LangGraph")
    print(f"Question: {question}")
    print()
    print("Graph:")
    print("START -> classify -> [math_node | coding_node | general_node] -> END")
    print()
    print("Final state:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
