from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleFourState, ModuleFourTool
from my_agent.tools import run_calculator_tool, run_search_tool

_MATH_EXPRESSION = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)")


def decide_tool(state: ModuleFourState) -> ModuleFourState:
    question = state["question"].lower()

    if "calculate" in question or "math" in question or _MATH_EXPRESSION.search(question):
        tool: ModuleFourTool = "calculator"
    elif "search" in question or "who is" in question or "what is" in question:
        tool = "search"
    else:
        tool = "none"

    return {"tool": tool}


def route_tool(state: ModuleFourState) -> ModuleFourTool:
    return state["tool"]


def calculator(state: ModuleFourState) -> ModuleFourState:
    return {"tool_result": run_calculator_tool(state["question"])}


def search(state: ModuleFourState) -> ModuleFourState:
    return {"tool_result": run_search_tool(state["question"])}


def final_answer(state: ModuleFourState) -> ModuleFourState:
    tool_result = state.get("tool_result")

    if tool_result:
        answer = f"Final answer based on tool result: {tool_result}"
    else:
        answer = "Final answer without a tool: respond directly."

    return {"answer": answer}


def build_module_four_graph() -> StateGraph:
    graph = StateGraph(ModuleFourState)
    graph.add_node("decide_tool", decide_tool)
    graph.add_node("calculator", calculator)
    graph.add_node("search", search)
    graph.add_node("final_answer", final_answer)
    graph.add_edge(START, "decide_tool")
    graph.add_conditional_edges(
        "decide_tool",
        route_tool,
        {
            "calculator": "calculator",
            "search": "search",
            "none": "final_answer",
        },
    )
    graph.add_edge("calculator", "final_answer")
    graph.add_edge("search", "final_answer")
    graph.add_edge("final_answer", END)
    return graph


@lru_cache(maxsize=1)
def get_module_four_app() -> Any:
    return build_module_four_graph().compile()


def invoke_module_four_workflow(question: str) -> ModuleFourState:
    app = get_module_four_app()
    return app.invoke({"question": question})
