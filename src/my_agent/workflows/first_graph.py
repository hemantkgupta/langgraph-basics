from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleTwoState

_MATH_EXPRESSION = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)")


def classify(state: ModuleTwoState) -> ModuleTwoState:
    question = state["question"].lower()

    if "code" in question or "python" in question:
        category = "coding"
    elif "math" in question or _MATH_EXPRESSION.search(question):
        category = "math"
    else:
        category = "general"

    return {"category": category}


def answer(state: ModuleTwoState) -> ModuleTwoState:
    category = state["category"]

    if category == "math":
        result = "This is a math question."
    elif category == "coding":
        result = "This is a programming question."
    else:
        result = "This is a general question."

    return {"answer": result}


def build_module_two_graph() -> StateGraph:
    graph = StateGraph(ModuleTwoState)
    graph.add_node("classify", classify)
    graph.add_node("answer", answer)
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "answer")
    graph.add_edge("answer", END)
    return graph


@lru_cache(maxsize=1)
def get_module_two_app() -> Any:
    return build_module_two_graph().compile()


def invoke_module_two_workflow(question: str) -> ModuleTwoState:
    app = get_module_two_app()
    return app.invoke({"question": question})
