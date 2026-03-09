from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from my_agent.workflows.gemini_tool_call_graph import (
    build_module_eight_graph as build_gemini_module_eight_graph,
    run_module_eight_demo as run_module_eight_gemini_demo,
    serialize_module_eight_state as serialize_module_eight_gemini_state,
)
from my_agent.workflows.openai_tool_call_graph import (
    build_module_eight_graph as build_openai_module_eight_graph,
    run_module_eight_demo as run_module_eight_openai_demo,
    serialize_module_eight_state as serialize_module_eight_openai_state,
)


class StubToolCallingModel:
    def invoke(self, messages: list[BaseMessage]) -> BaseMessage:
        last_message = messages[-1]
        human_messages = [message for message in messages if isinstance(message, HumanMessage)]
        tool_messages = [message for message in messages if isinstance(message, ToolMessage)]
        latest_user_message = human_messages[-1].content if human_messages else ""

        if isinstance(last_message, ToolMessage):
            return AIMessage(content=f"The final answer is {last_message.content}.")

        if latest_user_message == "What is 7 multiplied by 8?":
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "call_multiply_1",
                        "name": "multiply",
                        "args": {"a": 7, "b": 8},
                    }
                ],
            )

        if latest_user_message == "Now multiply that by 2.":
            prior_result = int(tool_messages[-1].content) if tool_messages else 0
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "call_multiply_2",
                        "name": "multiply",
                        "args": {"a": prior_result, "b": 2},
                    }
                ],
            )

        return AIMessage(content="I can answer directly.")


class LoopingToolCallingModel:
    def invoke(self, messages: list[BaseMessage]) -> BaseMessage:
        return AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "loop_call",
                    "name": "multiply",
                    "args": {"a": 3, "b": 3},
                }
            ],
        )


def test_module_eight_openai_uses_tools_and_memory() -> None:
    app = build_openai_module_eight_graph(StubToolCallingModel()).compile(
        checkpointer=InMemorySaver()
    )

    _, second_turn = run_module_eight_openai_demo(
        "What is 7 multiplied by 8?",
        "Now multiply that by 2.",
        thread_id="module-eight-openai-thread",
        app=app,
    )

    serialized = serialize_module_eight_openai_state(second_turn)

    assert serialized["messages"][-1] == {
        "role": "assistant",
        "content": "The final answer is 112.",
    }


def test_module_eight_gemini_uses_tools_and_memory() -> None:
    app = build_gemini_module_eight_graph(StubToolCallingModel()).compile(
        checkpointer=InMemorySaver()
    )

    _, second_turn = run_module_eight_gemini_demo(
        "What is 7 multiplied by 8?",
        "Now multiply that by 2.",
        thread_id="module-eight-gemini-thread",
        app=app,
    )

    serialized = serialize_module_eight_gemini_state(second_turn)

    assert serialized["messages"][-1] == {
        "role": "assistant",
        "content": "The final answer is 112.",
    }


def test_module_eight_serializes_tool_calls_and_tool_messages() -> None:
    app = build_gemini_module_eight_graph(StubToolCallingModel()).compile(
        checkpointer=InMemorySaver()
    )

    first_turn, _ = run_module_eight_gemini_demo(
        "What is 7 multiplied by 8?",
        "Now multiply that by 2.",
        thread_id="module-eight-serialize-thread",
        app=app,
    )

    serialized = serialize_module_eight_gemini_state(first_turn)

    assert serialized["steps"] == 2
    assert serialized["messages"][0] == {
        "role": "user",
        "content": "What is 7 multiplied by 8?",
    }
    assert serialized["messages"][1]["tool_calls"] == [
        {
            "id": "call_multiply_1",
            "name": "multiply",
            "args": {"a": 7, "b": 8},
        }
    ]
    assert serialized["messages"][2] == {
        "role": "tool",
        "content": "56",
        "tool_call_id": "call_multiply_1",
    }


def test_module_eight_stops_after_max_steps() -> None:
    app = build_openai_module_eight_graph(LoopingToolCallingModel()).compile(
        checkpointer=InMemorySaver()
    )

    result, _ = run_module_eight_openai_demo(
        "Keep multiplying forever.",
        "Keep going.",
        thread_id="module-eight-stop-thread",
        app=app,
    )

    serialized = serialize_module_eight_openai_state(result)

    assert serialized["messages"][-1] == {
        "role": "assistant",
        "content": "Stopping because max tool steps reached.",
    }
    assert serialized["steps"] == 6
