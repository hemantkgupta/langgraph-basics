from __future__ import annotations

from typing import Any, Protocol

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleEightState
from my_agent.tools import get_module_eight_tools

_MAX_AGENT_STEPS = 5
_SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are a helpful assistant. Use the multiply tool for arithmetic requests. "
        "After you receive tool results, answer clearly and briefly."
    )
)
_TOOLS = get_module_eight_tools()
_TOOLS_BY_NAME = {tool.name: tool for tool in _TOOLS}


class ChatModel(Protocol):
    def invoke(self, messages: list[BaseMessage]) -> BaseMessage:
        ...


def agent_node_factory(model: ChatModel):
    def agent_node(state: ModuleEightState) -> ModuleEightState:
        next_step = state.get("steps", 0) + 1
        if next_step > _MAX_AGENT_STEPS:
            return {
                "steps": next_step,
                "messages": [AIMessage(content="Stopping because max tool steps reached.")],
            }

        response = model.invoke([_SYSTEM_PROMPT] + state.get("messages", []))
        return {
            "steps": next_step,
            "messages": [response],
        }

    return agent_node


def route_after_agent(state: ModuleEightState) -> str:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return "end"


def tool_node(state: ModuleEightState) -> ModuleEightState:
    last_message = state["messages"][-1]
    tool_messages: list[ToolMessage] = []

    for tool_call in getattr(last_message, "tool_calls", []):
        tool_name = tool_call["name"]
        tool_args = tool_call.get("args", {})
        tool_impl = _TOOLS_BY_NAME.get(tool_name)

        if tool_impl is None:
            result = f"Unknown tool: {tool_name}"
        else:
            try:
                result = tool_impl.invoke(tool_args)
            except Exception as exc:  # pragma: no cover - defensive path
                result = f"Tool error: {exc}"

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
                name=tool_name,
            )
        )

    return {"messages": tool_messages}


def build_module_eight_graph(model: ChatModel) -> StateGraph:
    graph = StateGraph(ModuleEightState)
    graph.add_node("agent", agent_node_factory(model))
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


def invoke_module_eight_turn(
    user_message: str,
    *,
    thread_id: str,
    app: Any,
) -> ModuleEightState:
    return app.invoke(
        {
            "messages": [HumanMessage(content=user_message)],
            "steps": 0,
        },
        config={"configurable": {"thread_id": thread_id}},
    )


def run_module_eight_demo(
    first_message: str,
    second_message: str,
    *,
    thread_id: str,
    app: Any,
) -> tuple[ModuleEightState, ModuleEightState]:
    first_turn = invoke_module_eight_turn(first_message, thread_id=thread_id, app=app)
    second_turn = invoke_module_eight_turn(second_message, thread_id=thread_id, app=app)
    return first_turn, second_turn


def serialize_module_eight_state(state: ModuleEightState) -> dict[str, Any]:
    return {
        "steps": state.get("steps", 0),
        "messages": [_serialize_message(message) for message in state.get("messages", [])],
    }


def _serialize_message(message: BaseMessage) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "role": _message_role(message),
        "content": message.content,
    }

    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        payload["tool_calls"] = [
            {
                "id": tool_call["id"],
                "name": tool_call["name"],
                "args": tool_call.get("args", {}),
            }
            for tool_call in tool_calls
        ]

    if isinstance(message, ToolMessage):
        payload["tool_call_id"] = message.tool_call_id

    return payload


def _message_role(message: BaseMessage) -> str:
    if isinstance(message, HumanMessage):
        return "user"
    if isinstance(message, ToolMessage):
        return "tool"
    if isinstance(message, AIMessage):
        return "assistant"
    return message.type
