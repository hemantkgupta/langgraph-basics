from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleThreeCategory, ModuleThreeState

_MATH_EXPRESSION = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)")


def classify(state: ModuleThreeState) -> ModuleThreeState:
    question = state["question"].lower()

    if "math" in question or _MATH_EXPRESSION.search(question):
        category: ModuleThreeCategory = "math"
    elif "code" in question or "python" in question:
        category = "coding"
    else:
        category = "general"

    return {"category": category}


def route_question(state: ModuleThreeState) -> ModuleThreeCategory:
    return state["category"]


def math_node(state: ModuleThreeState) -> ModuleThreeState:
    return {"answer": "Use a calculator for this math question."}


def coding_node(state: ModuleThreeState) -> ModuleThreeState:
    return {"answer": "Search documentation for the coding solution."}


def general_node(state: ModuleThreeState) -> ModuleThreeState:
    return {"answer": "General LLM answer."}


def build_module_three_graph() -> StateGraph:
    graph = StateGraph(ModuleThreeState)
    graph.add_node("classify", classify)
    graph.add_node("math_node", math_node)
    graph.add_node("coding_node", coding_node)
    graph.add_node("general_node", general_node)
    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_question,
        {
            "math": "math_node",
            "coding": "coding_node",
            "general": "general_node",
        },
    )
    graph.add_edge("math_node", END)
    graph.add_edge("coding_node", END)
    graph.add_edge("general_node", END)
    return graph


@lru_cache(maxsize=1)
def get_module_three_app() -> Any:
    return build_module_three_graph().compile()


def invoke_module_three_workflow(question: str) -> ModuleThreeState:
    app = get_module_three_app()
    return app.invoke({"question": question})
