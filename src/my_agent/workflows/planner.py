from __future__ import annotations

import operator
import re
from copy import deepcopy
from typing import Callable

from my_agent.models.schemas import AgentState, NodeName, Route, StepSnapshot, WorkflowRun
from my_agent.tools import search_expense_docs

_MATH_EXPRESSION = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)")
_CODING_KEYWORDS = (
    "code",
    "python",
    "bug",
    "api",
    "database",
    "sql",
    "function",
    "expense",
    "store",
)


def classify_question(state: AgentState) -> AgentState:
    question = state["question"].lower()

    if _MATH_EXPRESSION.search(question):
        classification: Route = "math"
    elif any(keyword in question for keyword in _CODING_KEYWORDS):
        classification = "coding"
    else:
        classification = "general"

    return {"classification": classification}


def calculator(state: AgentState) -> AgentState:
    match = _MATH_EXPRESSION.search(state["question"])
    if not match:
        return {"result": "I can only calculate simple expressions like 7 + 5."}

    left, operator_symbol, right = match.groups()
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    try:
        raw_result = operations[operator_symbol](float(left), float(right))
    except ZeroDivisionError:
        return {"result": "Division by zero is not allowed."}

    if raw_result.is_integer():
        return {"result": str(int(raw_result))}

    return {"result": str(raw_result)}


def search_docs(state: AgentState) -> AgentState:
    documents = search_expense_docs(state["question"])
    return {"documents": documents}


def llm_answer(state: AgentState) -> AgentState:
    question = state["question"]
    return {
        "result": (
            "This is the general route. In a real LangGraph app, an LLM node would "
            f"answer the question directly: {question}"
        )
    }


def format_answer(state: AgentState) -> AgentState:
    classification = state["classification"]

    if classification == "math":
        result = state.get("result", "No result was produced.")
        answer = f"Math route selected. Calculator result: {result}."
    elif classification == "coding":
        documents = state.get("documents", [])
        answer = "Coding route selected. Relevant docs:\n- " + "\n- ".join(documents)
    else:
        answer = state.get("result", "No answer was produced.")

    return {"answer": answer}


def decide_next_step(state: AgentState) -> Route:
    return state["classification"]


def run_module_one_workflow(question: str) -> WorkflowRun:
    state: AgentState = {"question": question}
    route_taken: list[NodeName] = []
    snapshots: list[StepSnapshot] = []

    def apply_node(node_name: NodeName, node: Callable[[AgentState], AgentState]) -> None:
        updates = node(state)
        state.update(updates)
        route_taken.append(node_name)
        snapshots.append(
            StepSnapshot(
                node=node_name,
                updates=deepcopy(dict(updates)),
                state_after=deepcopy(state),
            )
        )

    apply_node("classify_question", classify_question)

    next_step = decide_next_step(state)
    if next_step == "math":
        apply_node("calculator", calculator)
    elif next_step == "coding":
        apply_node("search_docs", search_docs)
    else:
        apply_node("llm_answer", llm_answer)

    apply_node("format_answer", format_answer)

    return WorkflowRun(
        final_state=deepcopy(state),
        route=route_taken,
        snapshots=snapshots,
    )
