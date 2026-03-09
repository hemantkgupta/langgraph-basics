from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

Route = Literal["math", "coding", "general"]
ModuleTwoCategory = Literal["math", "coding", "general"]
ModuleThreeCategory = Literal["math", "coding", "general"]
ModuleFourTool = Literal["calculator", "search", "none"]
ModuleFiveToolRequest = Literal["", "calculator", "search"]
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


class ModuleFiveState(TypedDict, total=False):
    question: str
    messages: list[str]
    tool_request: ModuleFiveToolRequest
    tool_result: str
    final_answer: str
    steps: int


class ModuleSixState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    reply: str


class ModuleSevenState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]


class ModuleEightState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    steps: int


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
