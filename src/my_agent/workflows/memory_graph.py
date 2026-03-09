from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleSixState


def chatbot_node(state: ModuleSixState) -> ModuleSixState:
    messages = state.get("messages", [])
    human_messages = [message.content for message in messages if isinstance(message, HumanMessage)]
    latest_human_message = human_messages[-1] if human_messages else ""

    if latest_human_message.lower().strip(" ?") == "what did i tell you":
        if len(human_messages) >= 2:
            reply = f"You told me: {human_messages[-2]}"
        else:
            reply = "I do not have anything earlier in this thread yet."
    else:
        reply = f"I remember you said: {latest_human_message}"

    return {
        "reply": reply,
        "messages": [AIMessage(content=reply)],
    }


def build_module_six_graph() -> StateGraph:
    graph = StateGraph(ModuleSixState)
    graph.add_node("chatbot", chatbot_node)
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", END)
    return graph


@lru_cache(maxsize=1)
def get_module_six_app() -> Any:
    return build_module_six_graph().compile(checkpointer=InMemorySaver())


def invoke_module_six_turn(user_message: str, *, thread_id: str) -> ModuleSixState:
    app = get_module_six_app()
    return app.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config={"configurable": {"thread_id": thread_id}},
    )


def run_module_six_demo(
    first_message: str,
    second_message: str,
    *,
    thread_id: str,
) -> tuple[ModuleSixState, ModuleSixState]:
    first_turn = invoke_module_six_turn(first_message, thread_id=thread_id)
    second_turn = invoke_module_six_turn(second_message, thread_id=thread_id)
    return first_turn, second_turn


def serialize_module_six_state(state: ModuleSixState) -> dict[str, Any]:
    messages = [
        {
            "role": _message_role(message),
            "content": message.content,
        }
        for message in state.get("messages", [])
    ]
    return {
        "messages": messages,
        "reply": state.get("reply", ""),
    }


def _message_role(message: BaseMessage) -> str:
    if isinstance(message, HumanMessage):
        return "user"
    if isinstance(message, AIMessage):
        return "assistant"
    return message.type
