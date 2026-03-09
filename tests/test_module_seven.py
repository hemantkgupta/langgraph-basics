from types import SimpleNamespace

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from my_agent.main import _default_module_seven_provider
from my_agent.workflows.gemini_chat_graph import (
    build_module_seven_graph as build_gemini_module_seven_graph,
    run_module_seven_demo as run_module_seven_gemini_demo,
    serialize_module_seven_state as serialize_module_seven_gemini_state,
)
from my_agent.workflows.openai_chat_graph import (
    build_module_seven_graph as build_openai_module_seven_graph,
    run_module_seven_demo as run_module_seven_openai_demo,
    serialize_module_seven_state as serialize_module_seven_openai_state,
)


class StubChatModel:
    def invoke(self, messages: list[BaseMessage]) -> BaseMessage:
        latest_user_message = ""
        human_messages = [message for message in messages if isinstance(message, HumanMessage)]
        if human_messages:
            latest_user_message = human_messages[-1].content

        if latest_user_message == "What is my name?":
            prior_name = next(
                (
                    message.content.rstrip(".")
                    for message in human_messages
                    if message.content.lower().startswith("my name is ")
                ),
                "I do not know your name.",
            )
            if prior_name.startswith("My name is "):
                name = prior_name.removeprefix("My name is ")
                return AIMessage(content=f"Your name is {name}.")
            return AIMessage(content="I do not know your name.")

        return AIMessage(content=f"Echo: {latest_user_message}")


def test_module_seven_openai_uses_memory_with_same_thread() -> None:
    app = build_openai_module_seven_graph(StubChatModel()).compile(checkpointer=InMemorySaver())

    _, second_turn = run_module_seven_openai_demo(
        "My name is Hemant.",
        "What is my name?",
        thread_id="module-seven-memory-thread",
        app=app,
    )

    serialized = serialize_module_seven_openai_state(second_turn)

    assert serialized["messages"][-1] == {"role": "assistant", "content": "Your name is Hemant."}


def test_module_seven_gemini_uses_memory_with_same_thread() -> None:
    app = build_gemini_module_seven_graph(StubChatModel()).compile(checkpointer=InMemorySaver())

    _, second_turn = run_module_seven_gemini_demo(
        "My name is Hemant.",
        "What is my name?",
        thread_id="module-seven-gemini-memory-thread",
        app=app,
    )

    serialized = serialize_module_seven_gemini_state(second_turn)

    assert serialized["messages"][-1] == {"role": "assistant", "content": "Your name is Hemant."}


def test_module_seven_serializes_message_history() -> None:
    app = build_gemini_module_seven_graph(StubChatModel()).compile(checkpointer=InMemorySaver())

    first_turn, _ = run_module_seven_gemini_demo(
        "I am learning LangGraph.",
        "What is my name?",
        thread_id="module-seven-serialize-thread",
        app=app,
    )

    serialized = serialize_module_seven_gemini_state(first_turn)

    assert serialized["messages"] == [
        {"role": "user", "content": "I am learning LangGraph."},
        {"role": "assistant", "content": "Echo: I am learning LangGraph."},
    ]


def test_module_seven_provider_defaults_to_openai_when_available() -> None:
    provider = _default_module_seven_provider(
        SimpleNamespace(
            openai_api_key="openai-key",
            google_api_key="google-key",
            gemini_api_key="gemini-key",
        )
    )

    assert provider == "openai"


def test_module_seven_provider_falls_back_to_gemini() -> None:
    provider = _default_module_seven_provider(
        SimpleNamespace(
            openai_api_key=None,
            google_api_key="google-key",
            gemini_api_key=None,
        )
    )

    assert provider == "gemini"
