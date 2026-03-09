from __future__ import annotations

import operator
import re

from langchain_core.tools import BaseTool, tool

from my_agent.tools.expense_db import search_expense_docs

_MATH_EXPRESSION = re.compile(r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)")
_SEARCH_INDEX = {
    "langgraph": "LangGraph is a framework for building stateful, multi-step AI agents.",
    "ada lovelace": "Ada Lovelace is widely regarded as an early computing pioneer.",
    "openai": "OpenAI builds AI models, APIs, and agent tooling.",
}


def run_calculator_tool(question: str) -> str:
    match = _MATH_EXPRESSION.search(question)
    if not match:
        return "Calculator result: I could not parse a numeric expression."

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
        return "Calculator result: Division by zero is not allowed."

    if raw_result.is_integer():
        return f"Calculator result: {int(raw_result)}"

    return f"Calculator result: {raw_result}"


def run_search_tool(question: str) -> str:
    lowered_question = question.lower()

    for term, result in _SEARCH_INDEX.items():
        if term in lowered_question:
            return f"Search result: {result}"

    if "expense" in lowered_question or "python" in lowered_question:
        documents = search_expense_docs(question, limit=1)
        return f"Search result: {documents[0]}"

    return "Search result: No matching result found in the demo search index."


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def get_module_eight_tools() -> list[BaseTool]:
    return [multiply]
