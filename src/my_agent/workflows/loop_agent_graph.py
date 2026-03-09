from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleFiveState, ModuleFiveToolRequest
from my_agent.tools import run_calculator_tool, run_search_tool

_MATH_EXPRESSION = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)")
_MAX_AGENT_STEPS = 5


def _normalize_tool_result(result: str, prefix: str) -> str:
    if result.startswith(prefix):
        return result.removeprefix(prefix).strip()
    return result


def agent_node(state: ModuleFiveState) -> ModuleFiveState:
    question = state["question"]
    lowered_question = question.lower()
    messages = list(state.get("messages", []))
    tool_result = state.get("tool_result", "")
    steps = state.get("steps", 0) + 1

    if steps > _MAX_AGENT_STEPS:
        return {
            "steps": steps,
            "tool_request": "",
            "final_answer": "Stopping because max steps reached.",
            "messages": messages + ["Max steps reached, stopping"],
        }

    if tool_result:
        return {
            "steps": steps,
            "tool_request": "",
            "final_answer": f"The answer is based on tool result: {tool_result}",
            "messages": messages + ["Tool result received, finishing"],
        }

    if "2 + 2" in question or "calculate" in lowered_question or "math" in lowered_question:
        tool_request: ModuleFiveToolRequest = "calculator"
        thought = "Need calculator"
    elif (
        "search" in lowered_question
        or "who is" in lowered_question
        or "what is" in lowered_question
    ):
        tool_request = "search"
        thought = "Need search"
    elif _MATH_EXPRESSION.search(question):
        tool_request = "calculator"
        thought = "Need calculator"
    else:
        return {
            "steps": steps,
            "tool_request": "",
            "final_answer": "I can answer directly.",
            "messages": messages + ["No tool needed"],
        }

    return {
        "steps": steps,
        "tool_request": tool_request,
        "messages": messages + [thought],
    }


def tool_node(state: ModuleFiveState) -> ModuleFiveState:
    question = state["question"]
    messages = list(state.get("messages", []))
    tool_request = state.get("tool_request", "")

    if tool_request == "calculator":
        tool_result = _normalize_tool_result(run_calculator_tool(question), "Calculator result:")
        return {
            "tool_result": tool_result,
            "messages": messages + [f"Calculator returned {tool_result}"],
        }

    if tool_request == "search":
        tool_result = _normalize_tool_result(run_search_tool(question), "Search result:")
        return {
            "tool_result": tool_result,
            "messages": messages + ["Search returned a result"],
        }

    return {
        "tool_result": "unknown tool",
        "messages": messages + ["Unknown tool"],
    }


def route_after_agent(state: ModuleFiveState) -> str:
    if state.get("final_answer"):
        return "end"
    if state.get("tool_request"):
        return "tools"
    return "end"


def build_module_five_graph() -> StateGraph:
    graph = StateGraph(ModuleFiveState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "end": END,
        },
    )
    graph.add_edge("tools", "agent")
    return graph


@lru_cache(maxsize=2)
def get_module_five_app(use_checkpointer: bool = False) -> Any:
    graph = build_module_five_graph()
    if use_checkpointer:
        return graph.compile(checkpointer=InMemorySaver())
    return graph.compile()


def invoke_module_five_workflow(
    question: str,
    *,
    use_checkpointer: bool = False,
    thread_id: str = "module-five-demo",
    steps: int = 0,
) -> ModuleFiveState:
    app = get_module_five_app(use_checkpointer)
    input_state: ModuleFiveState = {
        "question": question,
        "messages": [],
        "tool_request": "",
        "tool_result": "",
        "final_answer": "",
        "steps": steps,
    }

    if use_checkpointer:
        return app.invoke(input_state, config={"configurable": {"thread_id": thread_id}})

    return app.invoke(input_state)
