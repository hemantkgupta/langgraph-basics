from my_agent.workflows.planner import run_module_one_workflow


def test_math_question_routes_to_calculator() -> None:
    run = run_module_one_workflow("What is 7 + 5?")

    assert run.final_state["classification"] == "math"
    assert run.final_state["result"] == "12"
    assert run.route == ["classify_question", "calculator", "format_answer"]
    assert "Calculator result: 12" in run.final_state["answer"]


def test_coding_question_routes_to_search_docs() -> None:
    run = run_module_one_workflow("How should I store expense records in Python?")

    assert run.final_state["classification"] == "coding"
    assert run.route == ["classify_question", "search_docs", "format_answer"]
    assert run.final_state["documents"]
    assert "Coding route selected." in run.final_state["answer"]
