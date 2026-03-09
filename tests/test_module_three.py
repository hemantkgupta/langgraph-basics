from my_agent.workflows.routing_graph import invoke_module_three_workflow


def test_module_three_routes_math_questions() -> None:
    result = invoke_module_three_workflow("solve math 2 + 2")

    assert result["question"] == "solve math 2 + 2"
    assert result["category"] == "math"
    assert result["answer"] == "Use a calculator for this math question."


def test_module_three_routes_coding_questions() -> None:
    result = invoke_module_three_workflow("How do I write Python code?")

    assert result["category"] == "coding"
    assert result["answer"] == "Search documentation for the coding solution."


def test_module_three_routes_general_questions() -> None:
    result = invoke_module_three_workflow("What is LangGraph?")

    assert result["category"] == "general"
    assert result["answer"] == "General LLM answer."
