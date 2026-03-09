# Module 6: Memory and Persistence in LangGraph

Module 6 introduces one of LangGraph's most practical production features: thread-scoped memory through a checkpointer.

The key mental model is:

- graph state = current working memory
- checkpointer = storage for that memory
- thread ID = the conversation key

Same graph + same `thread_id` + checkpointer = memory across turns.

## State

Module 6 uses message-oriented state with a reducer in [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleSixState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    reply: str
```

The important detail is `add_messages`.

That reducer appends new messages to existing history instead of replacing the full list.

## Graph

The workflow lives in [src/my_agent/workflows/memory_graph.py](../src/my_agent/workflows/memory_graph.py).

It is intentionally small:

```text
START -> chatbot -> END
```

The memory behavior comes from how the graph is compiled:

```python
app = build_module_six_graph().compile(checkpointer=InMemorySaver())
```

## Thread IDs

Each conversation uses a thread ID:

```python
config = {"configurable": {"thread_id": "user-1"}}
```

If two invokes use the same thread ID, LangGraph reloads the prior checkpointed state for that thread.

## Run It

Command line:

```bash
./scripts/dev.sh --module 6 --thread-id demo-thread "My name is Hemant"
```

By default, the CLI runs two turns in one process:

1. your first message
2. a follow-up message, defaulting to `What did I tell you?`

You can override the second turn:

```bash
./scripts/dev.sh --module 6 --thread-id demo-thread --follow-up "Repeat what I said" "My name is Hemant"
```

## What Happens

Turn 1:

- user message is added to `messages`
- graph runs
- assistant reply is appended
- checkpoint is saved for the thread

Turn 2 with the same `thread_id`:

- prior messages are restored
- the new user message is appended
- the bot can reference earlier thread history

## Example

Turn 1 input:

```text
My name is Hemant
```

Turn 2 input:

```text
What did I tell you?
```

Turn 2 reply:

```text
You told me: My name is Hemant
```

## Development vs Production

Module 6 uses `InMemorySaver`, which is good for local development and tests.

It is not durable across process restarts.

Production systems should use a persistent backend instead of in-memory storage.

## Why This Matters

This is not chat-history magic. It is persisted workflow state.

That makes LangGraph memory feel closer to:

- workflow checkpointing
- resumable state machines
- thread-scoped state persistence

## Next Module

Module 7 combines real LLM calls, memory, multi-turn chat state, and thread-scoped conversations with either OpenAI or Gemini.
