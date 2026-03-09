from __future__ import annotations

import argparse
import json

from my_agent.settings import get_settings
from my_agent.workflows.first_graph import invoke_module_two_workflow
from my_agent.workflows.loop_agent_graph import invoke_module_five_workflow
from my_agent.workflows.memory_graph import run_module_six_demo, serialize_module_six_state
from my_agent.workflows.routing_graph import invoke_module_three_workflow
from my_agent.workflows.planner import run_module_one_workflow
from my_agent.workflows.tool_agent_graph import invoke_module_four_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a LangGraph basics module demo.",
    )
    parser.add_argument(
        "--module",
        choices=("1", "2", "3", "4", "5", "6"),
        default="6",
        help="Which learning module to run.",
    )
    parser.add_argument(
        "--thread-id",
        default="module-6-demo-thread",
        help="Thread ID used for memory-enabled module demos.",
    )
    parser.add_argument(
        "--follow-up",
        default="What did I tell you?",
        help="Optional second message for the Module 6 memory demo.",
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

    if args.module == "3":
        result = invoke_module_three_workflow(question)
        print("Module 3: Conditional Routing in LangGraph")
        print(f"Question: {question}")
        print()
        print("Graph:")
        print("START -> classify -> [math_node | coding_node | general_node] -> END")
        print()
        print("Final state:")
        print(json.dumps(result, indent=2))
        return

    if args.module == "4":
        result = invoke_module_four_workflow(question)
        print("Module 4: Building a Tool-Using Agent in LangGraph")
        print(f"Question: {question}")
        print()
        print("Graph:")
        print("START -> decide_tool -> [calculator | search | final_answer] -> END")
        print()
        print("Final state:")
        print(json.dumps(result, indent=2))
        return

    result = invoke_module_five_workflow(question)
    if args.module == "5":
        print("Module 5: Agent Loops in LangGraph")
        print(f"Question: {question}")
        print()
        print("Graph:")
        print("START -> agent -> [tools -> agent | END]")
        print()
        print("Final state:")
        print(json.dumps(result, indent=2))
        return

    first_message = args.question or "My name is Hemant"
    turn_one, turn_two = run_module_six_demo(
        first_message,
        args.follow_up,
        thread_id=args.thread_id,
    )
    print("Module 6: Memory and Persistence in LangGraph")
    print(f"Thread ID: {args.thread_id}")
    print()
    print("Turn 1:")
    print(json.dumps(serialize_module_six_state(turn_one), indent=2))
    print()
    print("Turn 2:")
    print(json.dumps(serialize_module_six_state(turn_two), indent=2))


if __name__ == "__main__":
    main()
