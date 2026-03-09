from my_agent.workflows.tool_agent_graph import invoke_module_four_workflow


def test_module_four_routes_to_calculator_tool() -> None:
    result = invoke_module_four_workflow("calculate 2 + 2")

    assert result["tool"] == "calculator"
    assert result["tool_result"] == "Calculator result: 4"
    assert result["answer"] == "Final answer based on tool result: Calculator result: 4"


def test_module_four_routes_to_search_tool() -> None:
    result = invoke_module_four_workflow("What is LangGraph?")

    assert result["tool"] == "search"
    assert result["tool_result"] == (
        "Search result: LangGraph is a framework for building stateful, multi-step AI agents."
    )
    assert result["answer"].startswith("Final answer based on tool result:")


def test_module_four_can_skip_tools() -> None:
    result = invoke_module_four_workflow("Say hello to the team.")

    assert result["tool"] == "none"
    assert "tool_result" not in result
    assert result["answer"] == "Final answer without a tool: respond directly."
