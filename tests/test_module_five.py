from my_agent.workflows.loop_agent_graph import invoke_module_five_workflow


def test_module_five_loops_through_tool_and_finishes() -> None:
    result = invoke_module_five_workflow("What is 2 + 2?")

    assert result["tool_request"] == ""
    assert result["tool_result"] == "4"
    assert result["steps"] == 2
    assert result["messages"] == [
        "Need calculator",
        "Calculator returned 4",
        "Tool result received, finishing",
    ]
    assert result["final_answer"] == "The answer is based on tool result: 4"


def test_module_five_can_answer_directly() -> None:
    result = invoke_module_five_workflow("Say hello to the team.")

    assert result["tool_request"] == ""
    assert result["steps"] == 1
    assert result["messages"] == ["No tool needed"]
    assert result["final_answer"] == "I can answer directly."


def test_module_five_stops_at_max_steps() -> None:
    result = invoke_module_five_workflow("What is 2 + 2?", steps=5)

    assert result["steps"] == 6
    assert result["final_answer"] == "Stopping because max steps reached."
    assert result["messages"] == ["Max steps reached, stopping"]


def test_module_five_supports_in_memory_checkpointer() -> None:
    result = invoke_module_five_workflow(
        "Who is Ada Lovelace?",
        use_checkpointer=True,
        thread_id="test-module-five-thread",
    )

    assert result["tool_result"] == "Ada Lovelace is widely regarded as an early computing pioneer."
    assert result["final_answer"].startswith("The answer is based on tool result:")
