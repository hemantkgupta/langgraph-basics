from my_agent.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.app_name == "langgraph-basics"
    assert settings.environment == "local"
    assert settings.default_question == "What is LangGraph?"
    assert settings.openai_api_key is None


def test_settings_reads_environment(monkeypatch) -> None:
    monkeypatch.setenv("MY_AGENT_DEFAULT_QUESTION", "What is 2 + 2?")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    settings = Settings()

    assert settings.default_question == "What is 2 + 2?"
    assert settings.openai_api_key == "test-key"
