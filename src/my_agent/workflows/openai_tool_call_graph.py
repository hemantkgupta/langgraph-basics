from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from my_agent.settings import get_settings
from my_agent.tools import get_module_eight_tools
from my_agent.workflows.tool_calling_graph import (
    build_module_eight_graph,
    invoke_module_eight_turn,
    run_module_eight_demo,
    serialize_module_eight_state,
)


def build_openai_tool_call_model() -> Any:
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Set it in the environment or .env before "
            "running Module 8 with OpenAI."
        )

    model = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
    )
    return model.bind_tools(get_module_eight_tools())


@lru_cache(maxsize=1)
def get_module_eight_app() -> Any:
    model = build_openai_tool_call_model()
    return build_module_eight_graph(model).compile(checkpointer=InMemorySaver())


__all__ = [
    "build_module_eight_graph",
    "build_openai_tool_call_model",
    "get_module_eight_app",
    "invoke_module_eight_turn",
    "run_module_eight_demo",
    "serialize_module_eight_state",
]
