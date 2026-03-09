from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypedDict

Route = Literal["math", "coding", "general"]
ModuleTwoCategory = Literal["math", "coding", "general"]
ModuleThreeCategory = Literal["math", "coding", "general"]
ModuleFourTool = Literal["calculator", "search", "none"]
NodeName = Literal[
    "classify_question",
    "calculator",
    "search_docs",
    "llm_answer",
    "format_answer",
]


class AgentState(TypedDict, total=False):
    question: str
    classification: Route
    documents: list[str]
    result: str
    answer: str


class ModuleTwoState(TypedDict, total=False):
    question: str
    category: ModuleTwoCategory
    answer: str


class ModuleThreeState(TypedDict, total=False):
    question: str
    category: ModuleThreeCategory
    answer: str


class ModuleFourState(TypedDict, total=False):
    question: str
    tool: ModuleFourTool
    tool_result: str
    answer: str


@dataclass(slots=True)
class StepSnapshot:
    node: NodeName
    updates: dict[str, Any]
    state_after: AgentState


@dataclass(slots=True)
class WorkflowRun:
    final_state: AgentState
    route: list[NodeName]
    snapshots: list[StepSnapshot]
