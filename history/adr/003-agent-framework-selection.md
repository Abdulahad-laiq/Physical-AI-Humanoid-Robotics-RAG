# ADR-003: Agent Framework and LLM Integration Stack

> **Scope**: Document decision cluster for agent orchestration framework, LLM integration, and execution model (sync/async).

- **Status:** Accepted
- **Date:** 2025-12-25
- **Feature:** rag-chatbot
- **Context:** The RAG chatbot requires an agent framework to orchestrate retrieval and generation workflows. The agent must integrate with Gemini-2.0-flash (via AsyncOpenAI compatibility layer), support both synchronous and asynchronous execution (FR-013), and align with AI-native architecture principles (constitution Section VIII). The choice affects system extensibility, error handling, and future multi-step reasoning capabilities.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects agent behavior, extensibility to multi-step workflows, dependency management, and integration patterns for the lifetime of the product
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - OpenAI SDK, LangGraph, ChatKit, custom agent loop
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts generation layer, error handling, future tool integration, and agent instruction patterns
-->

## Decision

**Use OpenAI Assistants SDK (agents module) with AsyncOpenAI + Gemini-2.0-flash**

- **Agent Framework**: OpenAI Assistants SDK (`agents` module from OpenAI Python library)
- **LLM Integration**: AsyncOpenAI client with external endpoint override
  - Model: `gemini-2.0-flash`
  - Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`
  - API Key: `GEMINI_API_KEY` (from environment variables)
- **Execution Modes**:
  - Synchronous: `Runner.run_sync(agent, query, run_config)`
  - Asynchronous: `Runner.run_async(agent, query, run_config)` (for concurrent requests)
- **Agent Instructions**: "Answer the question to the best of your ability based on the provided context. If the answer is not found in the context, respond with 'Information not found in the book.'"
- **Configuration**:
  ```python
  from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
  import os

  external_client = AsyncOpenAI(
      api_key=os.getenv("GEMINI_API_KEY"),
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )

  model = OpenAIChatCompletionsModel(
      model="gemini-2.0-flash",
      openai_client=external_client
  )

  config = RunConfig(
      model=model,
      model_provider=external_client,
      tracing_disabled=True  # Simplify for MVP
  )

  agent = Agent(
      name="TextbookAssistant",
      instructions="Answer based on provided context only. If not found, say 'Information not found in the book.'"
  )
  ```

## Consequences

### Positive

- **Simplicity**: Minimal abstraction layer; straightforward integration matching user-provided code example
- **Gemini Compatibility**: AsyncOpenAI base_url override enables seamless Gemini-2.0-flash integration (OpenAI-compatible API)
- **Sync/Async Support**: Native support for both execution modes (FR-013) via `run_sync` and `run_async` methods
- **Mature Ecosystem**: OpenAI SDK is well-documented, widely used, and actively maintained (reduces risk of breaking changes)
- **Future Extensibility**: If multi-step reasoning is needed (e.g., tool use for citation validation), OpenAI SDK supports function calling and tool integration
- **Minimal Dependencies**: Single library (`openai`) for agent orchestration; no additional frameworks required
- **Clear Error Handling**: SDK provides structured error types (APIError, RateLimitError, etc.) for robust error handling

### Negative

- **Limited to Single-Step Reasoning**: OpenAI Assistants SDK is optimized for simple request-response; not ideal for complex multi-step workflows (acceptable for MVP, but may require migration to LangGraph if future requirements include multi-step reasoning)
- **OpenAI SDK Coupling**: Tight coupling to OpenAI SDK patterns; switching to different frameworks (LangGraph, ChatKit) requires refactoring `services/agent.py`
- **Gemini API Limitations**: Gemini free tier (15 RPM, 1M TPM, 1500 RPD) may require caching or rate limiting (mitigated in plan with retry logic and caching strategy)
- **AsyncOpenAI Overhead**: Using AsyncOpenAI for Gemini adds indirection (OpenAI client → Gemini API); direct Gemini SDK might be simpler, but loses OpenAI compatibility
- **Tracing Disabled**: `tracing_disabled=True` for simplicity; loses observability into agent execution (can enable in debug mode)

## Alternatives Considered

### Alternative A: LangGraph (LangChain Framework)

**Configuration**:
- Framework: LangGraph (part of LangChain ecosystem)
- LLM: Gemini-2.0-flash via LangChain's ChatGoogleGenerativeAI
- Execution: Define graph with nodes (retrieval, generation, citation) and edges (control flow)
- Features: Multi-step reasoning, state management, conditional branching

**Why Rejected**:
- **Overkill for Simple RAG**: LangGraph excels at complex workflows (e.g., multi-agent systems, iterative refinement), but RAG chatbot is linear: retrieve → generate → cite
- **Complexity**: Requires defining graphs, nodes, edges, and state schemas; adds cognitive overhead for simple use case
- **Larger Dependency**: LangChain is a large framework (~50+ dependencies); violates "smallest viable change" constitutional principle
- **Learning Curve**: Team must learn LangGraph concepts (graphs, state management); OpenAI SDK is more familiar

**When to Revisit**: If future requirements include multi-step reasoning (e.g., "retrieve → validate → refine → cite" workflows), or if agent needs to use tools (e.g., code execution, external APIs)

---

### Alternative B: ChatKit (Lightweight Agent Framework)

**Configuration**:
- Framework: ChatKit (lightweight, simple agent framework)
- LLM: Gemini-2.0-flash via direct API calls
- Execution: Define agents with simple message handling
- Features: Simpler than LangGraph, more flexible than OpenAI SDK

**Why Rejected**:
- **Less Mature**: ChatKit has smaller ecosystem and community compared to OpenAI SDK (higher risk of breaking changes, limited documentation)
- **Manual LLM Integration**: Requires custom integration with Gemini API (no pre-built connectors); more implementation effort than AsyncOpenAI
- **No Clear Advantage**: For simple RAG use case, ChatKit offers no significant benefits over OpenAI SDK (similar simplicity, but less mature)

**When to Revisit**: If OpenAI SDK proves too rigid or if Gemini API changes break AsyncOpenAI compatibility

---

### Alternative C: Custom Agent Loop

**Configuration**:
- Framework: None (custom implementation)
- LLM: Direct Gemini API calls via `google-generativeai` Python SDK
- Execution: Manual loop: retrieve chunks → format prompt → call Gemini → parse response → format citations
- Features: Full control over prompt engineering, error handling, retries

**Why Rejected**:
- **Reinvents the Wheel**: Replicates functionality already provided by OpenAI SDK (message handling, retry logic, error types)
- **Higher Maintenance**: Custom code requires ongoing maintenance for edge cases (timeouts, rate limits, malformed responses)
- **No Async Support**: Would need to implement async execution manually (using `asyncio`); OpenAI SDK provides this out-of-box
- **Violates Constitutional Principle**: "Smallest viable change" principle favors using existing, battle-tested frameworks

**When to Revisit**: If OpenAI SDK and all alternatives prove inadequate (unlikely for simple RAG use case)

## Implementation Details

### Agent Initialization (services/agent.py)

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize AsyncOpenAI client with Gemini endpoint
external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Configure model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure runner
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,  # Enable in debug mode
    max_retries=3,
    timeout=10.0  # 10-second timeout
)

# Define agent
textbook_agent = Agent(
    name="TextbookAssistant",
    instructions=(
        "You are a helpful assistant for a Physical AI and Humanoid Robotics textbook. "
        "Answer questions based strictly on the provided context. "
        "If the answer is not found in the context, respond with: 'Information not found in the book.' "
        "Always cite sources using [Chapter X, Section Y.Z] format."
    )
)
```

### Synchronous Execution (for API endpoints)

```python
def answer_question(query: str, retrieved_chunks: List[str]) -> str:
    """
    Answer user query using agent with retrieved context.

    Args:
        query: User question
        retrieved_chunks: List of relevant text chunks from Qdrant

    Returns:
        Agent response (answer with citations)
    """
    context = "\n\n".join([
        f"[Chunk {i+1}]: {chunk}"
        for i, chunk in enumerate(retrieved_chunks)
    ])

    prompt = f"""Context from textbook:
{context}

Question: {query}

Answer:"""

    result = Runner.run_sync(textbook_agent, prompt, run_config=config)
    return result.final_output
```

### Asynchronous Execution (for concurrent requests)

```python
async def answer_question_async(query: str, retrieved_chunks: List[str]) -> str:
    """Async version of answer_question for concurrent processing."""
    context = "\n\n".join([
        f"[Chunk {i+1}]: {chunk}"
        for i, chunk in enumerate(retrieved_chunks)
    ])

    prompt = f"""Context from textbook:
{context}

Question: {query}

Answer:"""

    result = await Runner.run_async(textbook_agent, prompt, run_config=config)
    return result.final_output
```

## Migration Path to LangGraph (if needed in future)

If future requirements necessitate multi-step reasoning, migration path:

1. **Encapsulate in `services/agent.py`**: All agent logic is isolated; swapping framework requires only modifying this module
2. **Define LangGraph Workflow**:
   ```python
   from langgraph.graph import StateGraph, END

   workflow = StateGraph()
   workflow.add_node("retrieve", retrieval_node)
   workflow.add_node("generate", generation_node)
   workflow.add_node("cite", citation_node)
   workflow.add_edge("retrieve", "generate")
   workflow.add_edge("generate", "cite")
   workflow.add_edge("cite", END)
   ```
3. **Maintain Same Interface**: `answer_question(query, chunks)` function signature unchanged; internal implementation switches from OpenAI SDK to LangGraph
4. **Estimated Effort**: 1-2 days for migration (low risk due to isolation)

## References

- Feature Spec: [specs/rag-chatbot/spec.md](../../specs/rag-chatbot/spec.md) (FR-006: Agent orchestration; FR-013: Sync/async execution)
- Implementation Plan: [specs/rag-chatbot/plan.md](../../specs/rag-chatbot/plan.md#decision-4-agent-framework-selection) (Decision 4, lines 274-313)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Section VIII: AI-Native Architecture principle)
- Related ADRs:
  - ADR-001 (Embedding Model Selection - agent consumes embeddings for retrieval context)
  - ADR-002 (Chunking Strategy - agent receives chunked context)
- OpenAI SDK Documentation: [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- Gemini API Documentation: [Gemini OpenAI Compatibility](https://ai.google.dev/gemini-api/docs/openai)
- Evaluator Evidence: To be added after Phase 3 (agent integration testing)

---

**Approval**: Accepted on 2025-12-25
**Reviewers**: N/A (initial planning phase)
**Supersedes**: None
**Superseded By**: None
