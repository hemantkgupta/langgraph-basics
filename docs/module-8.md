# Module 8: Tool Calling with a Real LLM + Memory

Module 8 is the first agent loop in this repo that uses a real model, real tool calls, and persisted thread memory together.

It combines:

- provider-backed chat models
- message state with `add_messages`
- a real structured tool
- a graph-controlled loop
- `InMemorySaver`
- `thread_id`-scoped memory

## Graph

The Module 8 graph is:

```text
START -> agent -> [tools -> agent | END]
```

This is the standard tool-calling loop:

1. the model decides whether it needs a tool
2. the tool node executes requested tools
3. the graph routes back to the model
4. the loop stops when the model returns a final answer

## State

Module 8 uses [src/my_agent/models/schemas.py](../src/my_agent/models/schemas.py):

```python
class ModuleEightState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    steps: int
```

`messages` stores the conversation, tool calls, and tool results.

`steps` is a simple loop counter so the graph can stop safely instead of running forever.

## Tool

The structured tool lives in [src/my_agent/tools/agent_tools.py](../src/my_agent/tools/agent_tools.py):

```python
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b
```

The model gets tool-calling capability through `bind_tools(...)`.

## Providers

Module 8 supports both providers with the same graph shape:

- OpenAI in [src/my_agent/workflows/openai_tool_call_graph.py](../src/my_agent/workflows/openai_tool_call_graph.py)
- Gemini in [src/my_agent/workflows/gemini_tool_call_graph.py](../src/my_agent/workflows/gemini_tool_call_graph.py)

Provider settings:

- `MY_AGENT_OPENAI_MODEL`, default `gpt-4.1-mini`
- `MY_AGENT_GEMINI_MODEL`, default `gemini-2.5-flash`

Provider API keys:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `GOOGLE_API_KEY`

## Shared Graph Logic

The provider-independent loop is in [src/my_agent/workflows/tool_calling_graph.py](../src/my_agent/workflows/tool_calling_graph.py).

Key pieces:

- `agent_node_factory(model)` calls the model and increments the step counter
- `route_after_agent(...)` checks whether the latest AI message contains `tool_calls`
- `tool_node(...)` executes each tool call and returns `ToolMessage` objects
- `serialize_module_eight_state(...)` makes CLI output and tests readable

## Run It

First make sure the API key for the provider you want is available.

```bash
export OPENAI_API_KEY="your_api_key_here"
export GEMINI_API_KEY="your_api_key_here"
```

Then run:

```bash
./scripts/dev.sh --module 8 --provider openai --thread-id demo-thread "What is 7 multiplied by 8?"
./scripts/dev.sh --module 8 --provider gemini --thread-id demo-thread "What is 7 multiplied by 8?"
```

By default, the follow-up turn is:

```text
Now multiply that by 2.
```

You can override it:

```bash
./scripts/dev.sh --module 8 --provider gemini --thread-id demo-thread --follow-up "Multiply the previous result by 3." "What is 7 multiplied by 8?"
```

If you do not pass `--provider`, the CLI prefers OpenAI when `OPENAI_API_KEY` is configured. Otherwise it falls back to Gemini when `GOOGLE_API_KEY` or `GEMINI_API_KEY` is configured.

## What Happens

Turn 1:

- the user message is appended to `messages`
- the model emits a structured tool call for `multiply`
- the tool node runs and returns a `ToolMessage`
- the model sees the tool result and writes the final answer

Turn 2 with the same `thread_id`:

- the earlier thread state is restored
- the new user message is appended
- the model can use prior context from the same conversation
- the graph loops again if another tool call is needed

## Safety

Module 8 includes a max-step guard in the agent node.

If the model keeps requesting tools forever, the graph returns:

```text
Stopping because max tool steps reached.
```

That keeps the demo predictable and reflects the production rule that agent loops should always have a stop condition.

## Testing

The test suite does not call either provider API.

[tests/test_module_eight.py](../tests/test_module_eight.py) uses stub models to verify:

- tool calls and final answers
- memory across turns in the same thread
- serialized tool-call history
- max-step stopping behavior

## Next Module

Module 9 should turn these building blocks into a real project.
