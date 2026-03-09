from __future__ import annotations

from functools import lru_cache
from typing import Any, Protocol

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from my_agent.models.schemas import ModuleSevenState
from my_agent.settings import get_settings


class ChatModel(Protocol):
    def invoke(self, messages: list[BaseMessage]) -> BaseMessage:
        ...


def build_gemini_chat_model() -> ChatGoogleGenerativeAI:
    settings = get_settings()
    api_key = settings.google_api_key or settings.gemini_api_key
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY or GOOGLE_API_KEY is not configured. Set one in the environment "
            "or .env before running Module 7."
        )

    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0,
        google_api_key=api_key,
    )


def chatbot_node_factory(model: ChatModel):
    def chatbot_node(state: ModuleSevenState) -> ModuleSevenState:
        system_prompt = SystemMessage(
            content="You are a helpful assistant. Answer clearly and briefly.",
        )
        response = model.invoke([system_prompt] + state["messages"])
        return {"messages": [response]}

    return chatbot_node


def build_module_seven_graph(model: ChatModel) -> StateGraph:
    graph = StateGraph(ModuleSevenState)
    graph.add_node("chatbot", chatbot_node_factory(model))
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", END)
    return graph


@lru_cache(maxsize=1)
def get_module_seven_app() -> Any:
    model = build_gemini_chat_model()
    return build_module_seven_graph(model).compile(checkpointer=InMemorySaver())


def invoke_module_seven_turn(user_message: str, *, thread_id: str, app: Any | None = None) -> ModuleSevenState:
    compiled_app = app or get_module_seven_app()
    return compiled_app.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config={"configurable": {"thread_id": thread_id}},
    )


def run_module_seven_demo(
    first_message: str,
    second_message: str,
    *,
    thread_id: str,
    app: Any | None = None,
) -> tuple[ModuleSevenState, ModuleSevenState]:
    compiled_app = app or get_module_seven_app()
    first_turn = invoke_module_seven_turn(first_message, thread_id=thread_id, app=compiled_app)
    second_turn = invoke_module_seven_turn(second_message, thread_id=thread_id, app=compiled_app)
    return first_turn, second_turn


def serialize_module_seven_state(state: ModuleSevenState) -> dict[str, Any]:
    return {
        "messages": [
            {
                "role": _message_role(message),
                "content": message.content,
            }
            for message in state.get("messages", [])
        ]
    }


def _message_role(message: BaseMessage) -> str:
    if isinstance(message, HumanMessage):
        return "user"
    if isinstance(message, AIMessage):
        return "assistant"
    return message.type
