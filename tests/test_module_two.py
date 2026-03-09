from my_agent.workflows.first_graph import invoke_module_two_workflow


def test_module_two_coding_question() -> None:
    result = invoke_module_two_workflow("How to write Python code?")

    assert result["question"] == "How to write Python code?"
    assert result["category"] == "coding"
    assert result["answer"] == "This is a programming question."


def test_module_two_math_question() -> None:
    result = invoke_module_two_workflow("This is a math problem.")

    assert result["category"] == "math"
    assert result["answer"] == "This is a math question."


def test_module_two_general_question() -> None:
    result = invoke_module_two_workflow("What is LangGraph?")

    assert result["category"] == "general"
    assert result["answer"] == "This is a general question."
