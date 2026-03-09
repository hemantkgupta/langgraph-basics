# Module 7: Real LLM Chatbot with Memory

Module 7 is the first graph in this repo that calls a real model.

It combines:

- provider-backed chat models
- message state with `add_messages`
- `InMemorySaver`
- `thread_id`-scoped memory

## Graph

The graph is intentionally minimal:

```text
START -> chatbot -> END
```

The power comes from persisted state, not graph complexity.

## State

Module 7 uses message-oriented state in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleSevenState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
```

`add_messages` is what makes new conversation turns append instead of overwrite.

## Providers

Module 7 supports both providers with the same graph shape:

- OpenAI in [src/my_agent/workflows/openai_chat_graph.py](../src/my_agent/workflows/openai_chat_graph.py)
- Gemini in [src/my_agent/workflows/gemini_chat_graph.py](../src/my_agent/workflows/gemini_chat_graph.py)

Provider settings:

- `MY_AGENT_OPENAI_MODEL`, default `gpt-4.1-mini`
- `MY_AGENT_GEMINI_MODEL`, default `gemini-2.5-flash`

Provider API keys:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`

## Build The Graph

```python
graph = StateGraph(ModuleSevenState)
graph.add_node("chatbot", chatbot_node)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
app = graph.compile(checkpointer=InMemorySaver())
```

## Why Memory Works

The rule is:

Same graph + same `thread_id` + checkpointer = memory across turns.

The CLI demonstrates that by running two turns with the same thread:

1. your first user message
2. a follow-up message

## Run It

First make sure the API key for the provider you want is available.

```bash
export OPENAI_API_KEY="your_api_key_here"
export GEMINI_API_KEY="your_api_key_here"
```

Then run:

```bash
./scripts/dev.sh --module 7 --provider openai --thread-id demo-thread "My name is Hemant."
./scripts/dev.sh --module 7 --provider gemini --thread-id demo-thread "My name is Hemant."
```

By default, the follow-up turn is:

```text
What is my name?
```

You can override it:

```bash
./scripts/dev.sh --module 7 --provider gemini --thread-id demo-thread --follow-up "Summarize what I told you." "My name is Hemant."
```

If you do not pass `--provider`, the CLI prefers OpenAI when `OPENAI_API_KEY` is configured. Otherwise it falls back to Gemini when `GOOGLE_API_KEY` or `GEMINI_API_KEY` is configured.

## What Happens

Turn 1:

- your message is added to `messages`
- the model responds
- the checkpointer saves the updated thread state

Turn 2 with the same `thread_id`:

- LangGraph reloads the saved thread state
- the new message is appended
- the model sees the earlier context and can answer from memory

## Development vs Production

Module 7 uses `InMemorySaver`, which is good for local learning.

It is not durable across process restarts.

Production systems should use a persistent checkpointer backend.

## Testing

The test suite does not call either provider API.

[tests/test_module_seven.py](../tests/test_module_seven.py) uses a stub chat model so memory behavior can be tested offline and deterministically for both OpenAI and Gemini graph variants.

## Next Module

Module 8 adds real tool calling with a provider-backed model plus memory.
