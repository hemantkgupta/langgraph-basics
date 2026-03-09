from my_agent.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.app_name == "langgraph-basics"
    assert settings.environment == "local"
    assert settings.default_question == "What is LangGraph?"
    assert settings.openai_model == "gpt-4.1-mini"
    assert settings.gemini_model == "gemini-2.5-flash"
    assert settings.openai_api_key is None
    assert settings.google_api_key is None
    assert settings.gemini_api_key is None


def test_settings_reads_environment(monkeypatch) -> None:
    monkeypatch.setenv("MY_AGENT_DEFAULT_QUESTION", "What is 2 + 2?")
    monkeypatch.setenv("MY_AGENT_OPENAI_MODEL", "gpt-4.1-mini")
    monkeypatch.setenv("MY_AGENT_GEMINI_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-test-key")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    settings = Settings()

    assert settings.default_question == "What is 2 + 2?"
    assert settings.openai_model == "gpt-4.1-mini"
    assert settings.gemini_model == "gemini-2.5-flash"
    assert settings.openai_api_key == "openai-test-key"
    assert settings.google_api_key == "google-test-key"
    assert settings.gemini_api_key == "test-key"
