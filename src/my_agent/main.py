from __future__ import annotations

import argparse
import json

from my_agent.settings import get_settings
from my_agent.workflows.first_graph import invoke_module_two_workflow
from my_agent.workflows.gemini_chat_graph import (
    run_module_seven_demo as run_module_seven_gemini_demo,
    serialize_module_seven_state as serialize_module_seven_gemini_state,
)
from my_agent.workflows.gemini_tool_call_graph import (
    get_module_eight_app as get_module_eight_gemini_app,
)
from my_agent.workflows.loop_agent_graph import invoke_module_five_workflow
from my_agent.workflows.memory_graph import run_module_six_demo, serialize_module_six_state
from my_agent.workflows.openai_chat_graph import (
    run_module_seven_demo as run_module_seven_openai_demo,
    serialize_module_seven_state as serialize_module_seven_openai_state,
)
from my_agent.workflows.openai_tool_call_graph import (
    get_module_eight_app as get_module_eight_openai_app,
)
from my_agent.workflows.routing_graph import invoke_module_three_workflow
from my_agent.workflows.planner import run_module_one_workflow
from my_agent.workflows.tool_calling_graph import (
    run_module_eight_demo,
    serialize_module_eight_state,
)
from my_agent.workflows.tool_agent_graph import invoke_module_four_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a LangGraph basics module demo.",
    )
    parser.add_argument(
        "--module",
        choices=("1", "2", "3", "4", "5", "6", "7", "8"),
        default="8",
        help="Which learning module to run.",
    )
    parser.add_argument(
        "--thread-id",
        default="langgraph-basics-demo-thread",
        help="Thread ID used for memory-enabled module demos.",
    )
    parser.add_argument(
        "--follow-up",
        default="",
        help="Optional second message for memory-enabled module demos.",
    )
    parser.add_argument(
        "--provider",
        choices=("openai", "gemini"),
        default="",
        help="Model provider used for Modules 7 and 8.",
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

    if args.module == "5":
        result = invoke_module_five_workflow(question)
        print("Module 5: Agent Loops in LangGraph")
        print(f"Question: {question}")
        print()
        print("Graph:")
        print("START -> agent -> [tools -> agent | END]")
        print()
        print("Final state:")
        print(json.dumps(result, indent=2))
        return

    if args.module == "6":
        first_message = args.question or "My name is Hemant"
        follow_up = args.follow_up or "What did I tell you?"
        turn_one, turn_two = run_module_six_demo(
            first_message,
            follow_up,
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
        return

    if args.module == "7":
        first_message = args.question or "My name is Hemant."
        follow_up = args.follow_up or "What is my name?"
        provider = args.provider or _default_model_provider(settings)
        if provider == "openai":
            turn_one, turn_two = run_module_seven_openai_demo(
                first_message,
                follow_up,
                thread_id=args.thread_id,
            )
            serializer = serialize_module_seven_openai_state
        else:
            turn_one, turn_two = run_module_seven_gemini_demo(
                first_message,
                follow_up,
                thread_id=args.thread_id,
            )
            serializer = serialize_module_seven_gemini_state

        print("Module 7: Real LLM Chatbot with Memory")
        print(f"Provider: {provider}")
        print(f"Thread ID: {args.thread_id}")
        print()
        print("Turn 1:")
        print(json.dumps(serializer(turn_one), indent=2))
        print()
        print("Turn 2:")
        print(json.dumps(serializer(turn_two), indent=2))
        return

    first_message = args.question or "What is 7 multiplied by 8?"
    follow_up = args.follow_up or "Now multiply that by 2."
    provider = args.provider or _default_model_provider(settings)
    if provider == "openai":
        app = get_module_eight_openai_app()
    else:
        app = get_module_eight_gemini_app()

    turn_one, turn_two = run_module_eight_demo(
        first_message,
        follow_up,
        thread_id=args.thread_id,
        app=app,
    )

    print("Module 8: Tool Calling with a Real LLM + Memory")
    print(f"Provider: {provider}")
    print(f"Thread ID: {args.thread_id}")
    print()
    print("Turn 1:")
    print(json.dumps(serialize_module_eight_state(turn_one), indent=2))
    print()
    print("Turn 2:")
    print(json.dumps(serialize_module_eight_state(turn_two), indent=2))


def _default_model_provider(settings) -> str:
    if settings.openai_api_key:
        return "openai"
    if settings.google_api_key or settings.gemini_api_key:
        return "gemini"
    return "openai"


if __name__ == "__main__":
    main()
