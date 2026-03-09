from my_agent.workflows.memory_graph import (
    invoke_module_six_turn,
    run_module_six_demo,
    serialize_module_six_state,
)


def test_module_six_remembers_prior_turn_in_same_thread() -> None:
    _, second_turn = run_module_six_demo(
        "My name is Hemant",
        "What did I tell you?",
        thread_id="module-six-memory-thread",
    )

    assert second_turn["reply"] == "You told me: My name is Hemant"


def test_module_six_keeps_threads_isolated() -> None:
    invoke_module_six_turn("My name is Hemant", thread_id="module-six-thread-a")
    second_thread_result = invoke_module_six_turn(
        "What did I tell you?",
        thread_id="module-six-thread-b",
    )

    assert second_thread_result["reply"] == "I do not have anything earlier in this thread yet."


def test_module_six_appends_messages_with_reducer() -> None:
    _, second_turn = run_module_six_demo(
        "I am learning LangGraph",
        "What did I tell you?",
        thread_id="module-six-reducer-thread",
    )

    serialized = serialize_module_six_state(second_turn)

    assert len(serialized["messages"]) == 4
    assert serialized["messages"][0] == {"role": "user", "content": "I am learning LangGraph"}
    assert serialized["messages"][-1]["role"] == "assistant"
