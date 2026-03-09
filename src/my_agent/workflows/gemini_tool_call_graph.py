from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from my_agent.settings import get_settings
from my_agent.tools import get_module_eight_tools
from my_agent.workflows.tool_calling_graph import (
    build_module_eight_graph,
    invoke_module_eight_turn,
    run_module_eight_demo,
    serialize_module_eight_state,
)


def build_gemini_tool_call_model() -> Any:
    settings = get_settings()
    api_key = settings.google_api_key or settings.gemini_api_key
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY or GOOGLE_API_KEY is not configured. Set one in the environment "
            "or .env before running Module 8 with Gemini."
        )

    model = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0,
        google_api_key=api_key,
    )
    return model.bind_tools(get_module_eight_tools())


@lru_cache(maxsize=1)
def get_module_eight_app() -> Any:
    model = build_gemini_tool_call_model()
    return build_module_eight_graph(model).compile(checkpointer=InMemorySaver())


__all__ = [
    "build_gemini_tool_call_model",
    "build_module_eight_graph",
    "get_module_eight_app",
    "invoke_module_eight_turn",
    "run_module_eight_demo",
    "serialize_module_eight_state",
]
