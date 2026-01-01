# Implementation Plan: Integrated RAG Chatbot for Physical AI Textbook

**Branch**: `rag-chatbot` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/rag-chatbot/spec.md`

## Summary

Build an AI-native RAG chatbot embedded in the Docusaurus textbook that answers questions using strictly grounded retrieval from book content. The system uses Gemini-2.0-flash via AsyncOpenAI for generation, Qdrant for vector storage, Neon PostgreSQL for metadata, and FastAPI for the backend. Key features include selected-text mode (retrieval constrained to highlighted text), explicit citation of sources, and zero-hallucination guarantees through retrieval-first reasoning.

**Technical Approach**: Three-layer architecture (Frontend → Backend API → Agent + Vector Store) with modular, stateless design. Agent orchestration via OpenAI Assistants SDK/ChatKit. Deployment targets free-tier services (Qdrant Cloud, Neon, Gemini API free tier).

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: FastAPI, OpenAI SDK (agents), Qdrant Client, Psycopg3, Pydantic, python-dotenv, Sentence-Transformers (embedding model)
**Storage**: Qdrant Cloud Free Tier (vectors), Neon PostgreSQL Free Tier (metadata/sessions)
**Testing**: pytest (unit, integration), httpx (async API testing), pytest-asyncio
**Target Platform**: Linux server (Render/Railway/Fly.io free tier), embeddable in Docusaurus (web)
**Project Type**: Web application (backend API + frontend React component)
**Performance Goals**: p95 latency < 3 seconds, 50 concurrent users, 1000+ queries/day
**Constraints**: Free tier operation (Qdrant 1GB, Neon 500MB, Gemini 15 RPM), no PII storage, rate limiting 100 req/min per IP
**Scale/Scope**: Initial: 8-12 textbook chapters (~50k tokens), ~100-200 embedded chunks, 50-100 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Section VIII RAG Chatbot System Principles Compliance

| Principle | Requirement | Implementation Plan | Status |
|-----------|-------------|---------------------|--------|
| **Grounded Truthfulness** | All responses from indexed content or selected text; explicit "not found" message | Retrieval-first pipeline; threshold-based filtering; fallback message template | ✅ PASS |
| **Retrieval-First Reasoning** | Vector DB backing for all responses; semantic + section-aware chunking; deterministic retrieval | Qdrant retrieval before generation; metadata-rich chunks (chapter/section/URL); fixed similarity threshold | ✅ PASS |
| **Explainability** | Source traceability; debug mode; layer separation | Response includes chunk IDs + metadata; optional debug endpoint; modular architecture (retrieval/agent/API layers) | ✅ PASS |
| **Academic Clarity** | Consistent with textbook style; technically accurate; progressive concepts | Agent instructions tuned for technical audience; citation format aligns with textbook conventions | ✅ PASS |
| **AI-Native Architecture** | Agentic workflows; FastAPI; Qdrant; Neon; stateless endpoints | Agent class with retrieval tool; FastAPI REST API; Qdrant + Neon storage; no session state in API | ✅ PASS |
| **Security & Isolation** | Selected-text sandboxing; no PII; independent deployment | Selected-text mode uses temporary in-memory vector store; query logs anonymized; backend deployable separately | ✅ PASS |
| **Cost Constraints** | Free tier operation (Qdrant, Neon, Gemini) | Chunking optimized for <1M vectors; Neon <500MB; Gemini 15 RPM with retry logic | ✅ PASS |

**Result**: All constitutional requirements aligned. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (completed)
├── research.md          # Phase 0 research (embedding models, chunking strategies)
├── data-model.md        # Phase 1 data schemas (TextChunk, Query, Response, Session)
├── quickstart.md        # Phase 1 quickstart guide (local setup, env vars, testing)
├── contracts/           # Phase 1 API contracts (OpenAPI spec)
│   └── api-spec.yaml    # FastAPI endpoint schemas
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application: backend + frontend component

backend/
├── src/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Environment variables, settings
│   ├── models/
│   │   ├── schemas.py             # Pydantic models (Query, Response, TextChunk, etc.)
│   │   └── database.py            # Neon PostgreSQL connection, session models
│   ├── services/
│   │   ├── embeddings.py          # Sentence-Transformers embedding generation
│   │   ├── vector_store.py        # Qdrant client wrapper, retrieval logic
│   │   ├── chunking.py            # Semantic + section-aware chunking logic
│   │   ├── agent.py               # Agent orchestration (OpenAI SDK, Gemini-2.0-flash)
│   │   └── selected_text.py       # Selected-text mode isolation logic
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py            # POST /chat (global query)
│   │   │   ├── selected_text.py   # POST /chat/selected (selected-text query)
│   │   │   └── metadata.py        # GET /metadata (retrieval debug info)
│   │   └── middleware.py          # Rate limiting, logging, CORS
│   └── utils/
│       ├── logger.py              # Structured JSON logging
│       └── validators.py          # Input validation helpers
├── tests/
│   ├── unit/
│   │   ├── test_chunking.py
│   │   ├── test_embeddings.py
│   │   ├── test_vector_store.py
│   │   └── test_agent.py
│   ├── integration/
│   │   ├── test_chat_endpoint.py
│   │   └── test_selected_text_endpoint.py
│   └── fixtures/
│       └── sample_chunks.json     # Test data
├── scripts/
│   ├── ingest_textbook.py         # One-time script to chunk + embed textbook
│   └── setup_qdrant.py            # Initialize Qdrant collection
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md

frontend/
├── src/
│   ├── components/
│   │   ├── ChatWidget.tsx         # Main chat UI component
│   │   ├── ChatInput.tsx          # Query input field
│   │   ├── ChatMessage.tsx        # Message bubble with citations
│   │   └── SelectedTextButton.tsx # "Ask about this text" button
│   ├── services/
│   │   └── api.ts                 # Axios/Fetch wrapper for backend API
│   ├── hooks/
│   │   └── useTextSelection.ts    # Hook to detect text selection
│   └── styles/
│       └── chat.css
├── tests/
│   └── ChatWidget.test.tsx
├── package.json
└── README.md

shared/
└── types/                          # Shared TypeScript types (optional)
    └── api.ts
```

**Structure Decision**: Web application structure selected due to clear separation of backend (FastAPI) and frontend (React component for Docusaurus). Backend is independently deployable; frontend is embeddable via iframe or web component. This aligns with constitutional requirement for independent deployment and modular design.

## Complexity Tracking

> **No constitutional violations to justify.**

All complexity is warranted and minimal:
- **Agent Layer**: Required by constitution (AI-Native Architecture principle)
- **Selected-Text Mode**: Core functional requirement (FR-003) and constitutional principle (Security & Isolation)
- **Three-layer Architecture**: Simplest design meeting stateless, modular, and explainability requirements

## Scope & Dependencies

### In Scope

**Core Functionality** (aligned with P1-P2 user stories):
1. Global query mode: retrieve from entire textbook, cite sources
2. Selected-text query mode: retrieve only from highlighted text
3. Agent-based response generation with Gemini-2.0-flash
4. FastAPI backend with stateless endpoints
5. Qdrant vector storage with semantic + section-aware chunking
6. Neon PostgreSQL for session/query metadata logging
7. Rate limiting (100 req/min per IP)
8. Structured logging for debugging/evaluation

**Deferred to Future Iterations** (P3-P4 user stories):
- Clickable citation navigation (P3) - can be implemented after MVP
- Streaming responses (P4) - UX enhancement, not critical for functionality

### Out of Scope

- Multi-language support (English only per spec)
- User authentication/accounts
- Query history persistence across sessions
- Fine-tuning or custom model training
- External knowledge sources beyond textbook
- Voice input/output
- User feedback collection (thumbs up/down)

### External Dependencies

| Service/Library | Purpose | Free Tier Limits | Risk Mitigation |
|-----------------|---------|------------------|-----------------|
| **Qdrant Cloud** | Vector storage | 1GB, 1M vectors | Optimize chunking; monitor usage; fallback to local Qdrant if exceeded |
| **Neon PostgreSQL** | Metadata storage | 500MB | Store only essential logs; implement log rotation |
| **Gemini API** | LLM generation | 15 RPM, 1M TPM, 1500 RPD | Implement retry with exponential backoff; cache common queries; consider fallback to GPT-3.5-turbo |
| **OpenAI SDK** | Agent orchestration | N/A (used with external client) | Use AsyncOpenAI with Gemini endpoint |
| **Sentence-Transformers** | Embeddings | N/A (local) | No cost; CPU/GPU dependent; use all-MiniLM-L6-v2 for speed |

### System Dependencies

- **Python 3.9+**: Required for asyncio, type hints, modern features
- **Docker**: Optional for containerization and deployment
- **Node.js 18+**: For frontend build (Docusaurus compatibility)

## Key Decisions and Rationale

### Decision 1: Embedding Model Selection

**Options Considered**:
1. OpenAI text-embedding-3-small (paid, high quality, 1536 dimensions)
2. Sentence-Transformers all-MiniLM-L6-v2 (free, good quality, 384 dimensions, fast)
3. Sentence-Transformers all-mpnet-base-v2 (free, higher quality, 768 dimensions, slower)

**Trade-offs**:
- **OpenAI**: Best semantic quality, but costs ~$0.02/1M tokens; breaks free-tier constraint
- **all-MiniLM-L6-v2**: Fast inference, low dimension (good for free-tier Qdrant), sufficient quality for textbook QA
- **all-mpnet-base-v2**: Better quality but slower and higher dimension (more storage)

**Decision**: Use **Sentence-Transformers all-MiniLM-L6-v2**

**Rationale**:
- Meets free-tier constraint (no API costs)
- Fast inference for real-time query embedding
- 384 dimensions fit comfortably in Qdrant free tier (1M vectors × 384 dimensions × 4 bytes ≈ 1.4GB with metadata overhead; can fit ~200-300k chunks)
- Quality is sufficient for academic/technical content with section-aware chunking

**Reversibility**: High - can swap embedding models with re-ingestion (one-time cost)

**ADR Recommended**: YES - architecturally significant (affects cost, performance, retrieval quality)

---

### Decision 2: Chunking Strategy

**Options Considered**:
1. Fixed-size chunks (512 tokens, no section awareness)
2. Section-based chunks (variable size, respect Markdown headers)
3. Hybrid: Section-aware with max 512 token limit

**Trade-offs**:
- **Fixed-size**: Simple, predictable, but may split coherent concepts
- **Section-based**: Preserves semantic coherence but creates variable-size chunks (some may exceed 512 tokens)
- **Hybrid**: Best of both - preserves sections where possible, splits large sections at sentence boundaries

**Decision**: Use **Hybrid (section-aware with 512 token max)**

**Rationale**:
- Preserves semantic coherence for small/medium sections
- Prevents excessively large chunks that dilute retrieval accuracy
- Aligns with constitutional requirement: "Chunking strategy must preserve semantic and section-level coherence"
- Textbook sections are typically 200-800 tokens; hybrid handles both extremes

**Implementation**:
- Parse Docusaurus Markdown by headers (##, ###)
- If section < 512 tokens: chunk = section
- If section > 512 tokens: split at sentence boundaries (using spaCy or NLTK)
- Include metadata: chapter, section, subsection, url_anchor

**Reversibility**: Medium - re-ingestion required if strategy changes, but metadata schema supports multiple strategies

**ADR Recommended**: YES - architecturally significant (affects retrieval accuracy, user experience)

---

### Decision 3: Selected-Text Mode Implementation

**Options Considered**:
1. Temporary in-memory vector store (embed selected text on-demand)
2. Pre-embed all possible text selections (infeasible - combinatorial explosion)
3. String matching without embeddings (simple but inaccurate)

**Trade-offs**:
- **In-memory store**: Flexible, isolates selected text perfectly, but adds latency (embedding generation)
- **Pre-embedding**: Impossible due to combinatorial explosion
- **String matching**: Fast but doesn't support semantic queries

**Decision**: Use **Temporary in-memory vector store (embed selected text on-demand)**

**Rationale**:
- Perfect isolation: no global embeddings queried (meets constitutional requirement)
- Flexible: supports semantic queries on selected text
- Acceptable latency: Sentence-Transformers embedding for <1000 tokens takes ~100-200ms
- Stateless: no persistence needed (selected text is ephemeral)

**Implementation**:
- On POST /chat/selected, embed the selected text into 1-N chunks
- Store chunks in ephemeral in-memory Qdrant collection (or Python list for simplicity)
- Retrieve top-k from ephemeral store only
- Discard after response generation

**Reversibility**: High - isolated module, easy to replace

**ADR Recommended**: NO - straightforward implementation decision, not architecturally significant

---

### Decision 4: Agent Framework Selection

**Options Considered**:
1. OpenAI Assistants SDK with external client (Gemini via AsyncOpenAI)
2. LangGraph (more complex, supports multi-step reasoning)
3. ChatKit (lightweight, simpler than LangGraph)
4. Custom agent loop (most control, most implementation effort)

**Trade-offs**:
- **OpenAI SDK**: Mature, simple, supports Gemini via AsyncOpenAI; limited to single-step reasoning
- **LangGraph**: Powerful for multi-step workflows; overkill for simple RAG
- **ChatKit**: Lightweight, good for simple agents; less mature ecosystem
- **Custom loop**: Full control but reinvents the wheel

**Decision**: Use **OpenAI Assistants SDK (agents module) with AsyncOpenAI + Gemini endpoint**

**Rationale**:
- Simplest path to MVP (matches user-provided code example)
- Supports synchronous and asynchronous execution (FR-013)
- Gemini-2.0-flash compatible via AsyncOpenAI base_url override
- Agent instructions sufficient for RAG use case: "please answer the question to the best of your ability"
- Minimal abstraction overhead (constitutional principle: smallest viable change)

**Implementation**:
```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client)
config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)
agent = Agent(name="TextbookAssistant", instructions="Answer based on provided context only.")
```

**Reversibility**: Medium - agent framework is encapsulated in `services/agent.py`; can swap if needed

**ADR Recommended**: YES - architecturally significant (affects agent behavior, extensibility, dependencies)

---

### Decision 5: Citation Format

**Options Considered**:
1. Inline links: `[Chapter 3, Section 3.2](#ch3-s3.2)`
2. Footnote-style: `[1] Chapter 3, Section 3.2` with reference list at end
3. Structured JSON: `{"citations": [{"chapter": 3, "section": "3.2", "url": "..."}]}`

**Trade-offs**:
- **Inline links**: Immediate context, clickable, familiar to users
- **Footnote-style**: Cleaner prose but requires scrolling
- **Structured JSON**: Machine-readable but not user-friendly

**Decision**: Use **Inline links** in response text + structured JSON in API response

**Rationale**:
- Inline links provide immediate context (aligns with academic clarity principle)
- Structured JSON enables frontend to render citations flexibly (supports P3 user story: clickable navigation)
- Best of both worlds: human-readable response + machine-parseable metadata

**Implementation**:
- Response schema:
  ```json
  {
    "answer": "Inverse kinematics solves for joint angles given end-effector position [Chapter 3, Section 3.2].",
    "citations": [
      {
        "chunk_id": "ch3-s3.2-001",
        "chapter": 3,
        "section": "3.2",
        "url_anchor": "#inverse-kinematics",
        "relevance_score": 0.89
      }
    ]
  }
  ```

**Reversibility**: High - citation formatting is isolated in response generation logic

**ADR Recommended**: NO - straightforward implementation decision, not architecturally significant

---

### Decision 6: Rate Limiting Strategy

**Options Considered**:
1. IP-based rate limiting (100 req/min per IP)
2. Session-based rate limiting (requires authentication)
3. No rate limiting (rely on free-tier API limits)

**Trade-offs**:
- **IP-based**: Simple, no authentication required, prevents abuse
- **Session-based**: More accurate per-user limiting but requires auth (out of scope)
- **No limiting**: Simplest but risks exceeding Gemini free-tier limits (15 RPM)

**Decision**: Use **IP-based rate limiting (100 req/min per IP)**

**Rationale**:
- Meets NFR-009 requirement
- Prevents abuse without requiring authentication
- 100 req/min per IP >> 15 RPM Gemini limit (15 req/min global), so backend rate limiting is necessary
- Simple implementation via FastAPI middleware (e.g., slowapi library)

**Implementation**:
- Use `slowapi` library with Redis backend (or in-memory for MVP)
- Configure: 100 requests per minute per IP address
- Return 429 Too Many Requests with Retry-After header

**Reversibility**: High - middleware-based, easy to adjust limits

**ADR Recommended**: NO - standard operational practice, not architecturally significant

## Interfaces and API Contracts

### REST API Endpoints

#### 1. POST /chat (Global Query Mode)

**Purpose**: Submit a question to be answered using the entire textbook content.

**Request**:
```json
{
  "query": "What is inverse kinematics?",
  "session_id": "optional-uuid-for-logging",
  "debug": false
}
```

**Response** (200 OK):
```json
{
  "answer": "Inverse kinematics solves for joint angles given end-effector position [Chapter 3, Section 3.2].",
  "citations": [
    {
      "chunk_id": "ch3-s3.2-001",
      "chapter": 3,
      "section": "3.2",
      "url_anchor": "#inverse-kinematics",
      "relevance_score": 0.89,
      "text_preview": "Inverse kinematics (IK) is the process of determining the joint parameters..."
    }
  ],
  "query_id": "uuid",
  "generation_time_ms": 1234
}
```

**Response** (200 OK, no relevant content):
```json
{
  "answer": "Information not found in the book.",
  "citations": [],
  "query_id": "uuid",
  "generation_time_ms": 456
}
```

**Error Responses**:
- 400 Bad Request: Invalid input (empty query, malformed JSON)
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Backend failure
- 503 Service Unavailable: Qdrant/Gemini API unavailable

---

#### 2. POST /chat/selected (Selected-Text Query Mode)

**Purpose**: Submit a question constrained to user-highlighted text.

**Request**:
```json
{
  "query": "Explain this equation",
  "selected_text": "J = ∂f/∂q where J is the Jacobian matrix...",
  "session_id": "optional-uuid-for-logging",
  "debug": false
}
```

**Response** (200 OK):
```json
{
  "answer": "The Jacobian matrix J relates joint velocities to end-effector velocities...",
  "citations": [
    {
      "chunk_id": "selected-text-temp-001",
      "source": "selected_text",
      "relevance_score": 0.95,
      "text_preview": "J = ∂f/∂q where J is the Jacobian matrix..."
    }
  ],
  "query_id": "uuid",
  "generation_time_ms": 987
}
```

**Response** (200 OK, no relevant content in selected text):
```json
{
  "answer": "Information not found in the selected text.",
  "citations": [],
  "query_id": "uuid",
  "generation_time_ms": 321
}
```

---

#### 3. GET /metadata (Debug/Monitoring Endpoint)

**Purpose**: Retrieve retrieval metadata for debugging (optional, for admin use).

**Query Parameters**:
- `query_id`: UUID of a specific query

**Response** (200 OK):
```json
{
  "query_id": "uuid",
  "query_text": "What is inverse kinematics?",
  "mode": "global",
  "retrieved_chunks": [
    {
      "chunk_id": "ch3-s3.2-001",
      "relevance_score": 0.89,
      "chapter": 3,
      "section": "3.2"
    },
    {
      "chunk_id": "ch3-s3.1-005",
      "relevance_score": 0.76,
      "chapter": 3,
      "section": "3.1"
    }
  ],
  "model": "gemini-2.0-flash",
  "generation_time_ms": 1234
}
```

---

### Data Models (Pydantic Schemas)

#### TextChunk
```python
class TextChunk(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float]  # 384 dimensions for all-MiniLM-L6-v2
    chapter: int
    section: str
    subsection: Optional[str]
    url_anchor: str
    token_count: int
    chunk_index: int  # Position within section
```

#### QueryRequest
```python
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    debug: bool = False
```

#### SelectedTextQueryRequest
```python
class SelectedTextQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    selected_text: str = Field(..., min_length=10, max_length=5000)
    session_id: Optional[str] = None
    debug: bool = False
```

#### Citation
```python
class Citation(BaseModel):
    chunk_id: str
    chapter: Optional[int]
    section: Optional[str]
    url_anchor: Optional[str]
    relevance_score: float
    text_preview: str = Field(..., max_length=200)
    source: str = "textbook"  # or "selected_text"
```

#### ChatResponse
```python
class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    query_id: str
    generation_time_ms: int
```

---

### Versioning Strategy

- **API Version**: v1 (prefix: `/api/v1/chat`)
- **Backward Compatibility**: Maintain v1 schema for 6 months after v2 release (if needed)
- **Breaking Changes**: Introduce new version prefix (v2), deprecate old version with notice

---

### Error Taxonomy

| Status Code | Error Type | Description | Example |
|-------------|------------|-------------|---------|
| 400 | `INVALID_INPUT` | Malformed request, validation failure | Empty query, query >1000 chars |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests from IP | >100 req/min |
| 500 | `INTERNAL_ERROR` | Backend failure, uncaught exception | Database connection failure |
| 503 | `SERVICE_UNAVAILABLE` | External dependency unavailable | Qdrant down, Gemini API timeout |

**Error Response Schema**:
```json
{
  "error": {
    "type": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "details": "Limit: 100 requests per minute per IP",
    "retry_after_seconds": 30
  }
}
```

## Non-Functional Requirements (NFRs) and Budgets

### Performance

| Metric | Target | Measurement | Budget |
|--------|--------|-------------|--------|
| **p95 Query Latency** | <3 seconds | End-to-end (API request → response) | Retrieval: 500ms, Embedding: 200ms, Generation: 2000ms, Overhead: 300ms |
| **Throughput** | 50 concurrent users | Load testing (Locust, k6) | 50 users × 1 query/min = ~1 QPS sustained |
| **Embedding Speed** | <200ms for 512 tokens | Local benchmark (Sentence-Transformers) | all-MiniLM-L6-v2 on CPU: ~150ms for 512 tokens |
| **Retrieval Speed** | <500ms for top-10 | Qdrant query latency | Free tier: typically 100-300ms for 100k vectors |

### Reliability

| Metric | Target | Strategy |
|--------|--------|----------|
| **SLO (Availability)** | 99% uptime | Deploy to Render/Railway with health checks; Qdrant Cloud SLA: 99.9% |
| **Error Budget** | 1% error rate | Monitor 4xx/5xx rates; alert if >1% over 1-hour window |
| **Degradation Strategy** | Return cached responses or "Service temporarily unavailable" | Implement retry logic for Gemini API (3 retries with exponential backoff); fallback message if retries exhausted |
| **Retry Policy** | 3 retries with exponential backoff (1s, 2s, 4s) | Apply to Gemini API calls and Qdrant queries |

### Security

| Requirement | Implementation | Validation |
|-------------|----------------|------------|
| **AuthN/AuthZ** | None (public chatbot) | N/A (future: API key for rate limiting) |
| **Data Handling** | No PII storage; anonymize IP addresses in logs (hash) | Log audit; verify no raw IPs in database |
| **Secrets Management** | Environment variables (.env, platform secrets) | Never commit .env; use `.env.example` template |
| **Auditing** | Log all queries (anonymized), retrieval metadata, errors | Structured JSON logs with query_id, timestamp, session_id (hashed) |
| **Input Validation** | Pydantic schemas, max lengths, sanitization | Unit tests for injection attempts (SQL, XSS) |

### Cost

| Service | Free Tier Limit | Usage Estimate (1000 queries/day) | Unit Economics | Risk Mitigation |
|---------|-----------------|-----------------------------------|----------------|-----------------|
| **Qdrant Cloud** | 1GB storage, 1M vectors | ~200k chunks × 384 dim = ~300MB | Free | Monitor storage; optimize chunking if approaching limit |
| **Neon PostgreSQL** | 500MB storage | ~1000 queries/day × 1KB/log = ~30MB/month | Free | Implement log rotation (keep 30 days) |
| **Gemini API** | 15 RPM, 1M TPM, 1500 RPD | 1000 queries/day ÷ 24h ÷ 60m = 0.7 QPM (well below 15 RPM) | Free | Implement caching for common queries; retry logic for rate limit errors |
| **Sentence-Transformers** | N/A (local inference) | CPU cost only | Free (self-hosted) | Use lightweight model (all-MiniLM-L6-v2) |
| **Render/Railway** | Free tier: 512MB RAM, 0.1 CPU | Backend: ~200MB RAM | Free | Monitor memory usage; optimize if approaching limit |

**Total Monthly Cost**: $0 (within free tiers)

## Data Management and Migration

### Source of Truth

- **Textbook Content**: Docusaurus Markdown files in repository
- **Embeddings**: Qdrant Cloud (generated from textbook Markdown)
- **Metadata**: Neon PostgreSQL (query logs, session info)

### Schema Evolution

**TextChunk Schema** (Qdrant collection):
- **Version 1.0**: `{chunk_id, text, embedding, chapter, section, url_anchor, token_count, chunk_index}`
- **Migration Strategy**: If schema changes, create new Qdrant collection (e.g., `textbook_chunks_v2`), re-ingest, swap collection name in config
- **Backward Compatibility**: Not required (no user-facing schema changes)

**Query Log Schema** (Neon PostgreSQL):
- **Version 1.0**: `{query_id, query_text, timestamp, mode, session_id_hash, response_time_ms}`
- **Migration Strategy**: Use Alembic for schema migrations (PostgreSQL ALTER TABLE)
- **Data Retention**: 30 days (auto-delete via cron job or PostgreSQL trigger)

### Migration and Rollback

**Textbook Content Updates**:
1. Update Markdown files in repository
2. Run `scripts/ingest_textbook.py` to re-chunk and re-embed
3. Push new embeddings to Qdrant (replace collection or upsert chunks)
4. Zero downtime: Create new collection, swap in config, delete old collection

**Rollback**:
- Keep previous Qdrant collection for 7 days before deletion
- Config flag to switch between collections: `QDRANT_COLLECTION_NAME=textbook_chunks_v1`

**Database Migrations** (Neon PostgreSQL):
- Use Alembic for version control
- Test migrations in staging environment
- Rollback via Alembic downgrade

### Data Retention

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| **Query Logs** | 30 days | PostgreSQL cron job (delete WHERE timestamp < NOW() - INTERVAL '30 days') |
| **Session Metadata** | 7 days | Cascade delete with queries |
| **Embeddings** | Indefinite (until textbook updated) | Manual deletion after textbook re-ingestion |

## Operational Readiness

### Observability

**Logs**:
- Format: Structured JSON (one log per line)
- Fields: `timestamp`, `level`, `query_id`, `session_id_hash`, `endpoint`, `latency_ms`, `status_code`, `error_type`, `message`
- Destination: Stdout (captured by Render/Railway logging)
- Retention: 7 days (platform default)

**Metrics**:
- **Request Rate**: Queries per minute (QPM)
- **Latency Distribution**: p50, p95, p99 response times
- **Error Rate**: 4xx and 5xx responses per minute
- **Retrieval Accuracy**: Average relevance score of top-k chunks
- **Free Tier Usage**: Qdrant storage %, Neon storage %, Gemini RPM %

**Traces**:
- Disabled by default (`tracing_disabled=True` in RunConfig) for simplicity
- Enable in debug mode: Log retrieval → agent → response flow with query_id

### Alerting

| Condition | Threshold | Action | Owner |
|-----------|-----------|--------|-------|
| **Error Rate** | >5% over 5 minutes | Alert via email/Slack | DevOps |
| **p95 Latency** | >5 seconds over 10 minutes | Investigate Qdrant/Gemini API | DevOps |
| **Qdrant Storage** | >80% of 1GB | Optimize chunking or upgrade | DevOps |
| **Gemini Rate Limit** | >10 RPM sustained | Implement caching or reduce traffic | DevOps |
| **Service Down** | Health check fails 3× in 3 minutes | Restart service, investigate logs | DevOps |

### Runbooks

#### Runbook 1: Gemini API Rate Limit Exceeded

**Symptoms**: 429 errors from Gemini API, users see "Service temporarily unavailable"

**Steps**:
1. Check Gemini API dashboard for current RPM usage
2. If within free tier (15 RPM), implement retry with exponential backoff (already in code)
3. If sustained >15 RPM, implement query caching (cache common questions for 1 hour)
4. If still exceeded, consider upgrading to Gemini paid tier or switching to GPT-3.5-turbo

---

#### Runbook 2: Qdrant Storage Limit Approaching

**Symptoms**: Monitoring shows >80% of 1GB storage used

**Steps**:
1. Review chunking strategy: Are chunks too small (over-chunking)?
2. Analyze chunk distribution: Remove duplicate or low-quality chunks
3. If necessary, re-chunk with larger max size (512 → 768 tokens)
4. If still exceeded, upgrade to Qdrant paid tier or use local Qdrant instance

---

#### Runbook 3: High Latency (p95 >5 seconds)

**Symptoms**: Users report slow responses, logs show high latency

**Steps**:
1. Check Qdrant query latency (should be <500ms)
   - If high: Investigate Qdrant free tier performance, consider local Qdrant
2. Check Gemini API latency (should be <2 seconds)
   - If high: Implement caching, reduce prompt length
3. Check embedding generation latency (should be <200ms)
   - If high: Use GPU for Sentence-Transformers (if available)
4. Profile backend code for bottlenecks (use `cProfile` or `py-spy`)

### Deployment and Rollback

**Deployment Strategy**: Blue-Green Deployment

1. **Build**: Docker image built via CI/CD (GitHub Actions)
2. **Deploy to Green**: New version deployed to staging environment (green)
3. **Health Check**: Automated tests run against green (API smoke tests)
4. **Swap**: Route traffic to green (update DNS or load balancer)
5. **Monitor**: Watch metrics for 15 minutes; if errors spike, rollback to blue

**Rollback Strategy**:
- Keep previous Docker image tagged (`v1.0.0`, `v1.0.1`, etc.)
- Rollback command: `git revert` + re-deploy previous image
- Database rollback: Use Alembic downgrade (if schema changed)

**Deployment Frequency**: Weekly (or on-demand for critical fixes)

### Feature Flags

**Not implemented in MVP** (future consideration):
- Feature flags for experimental features (e.g., streaming responses, citation navigation)
- Use simple config flags in `.env` (e.g., `ENABLE_STREAMING=false`)

### Backward Compatibility

**API Compatibility**:
- Maintain v1 API schema for at least 6 months after v2 release
- Deprecation notice in response headers: `X-API-Deprecation: v1 will be deprecated on 2026-01-01`

**Database Compatibility**:
- Schema migrations via Alembic with rollback support
- No breaking changes to query log schema in v1.x releases

## Risk Analysis and Mitigation

### Top 3 Risks

| Risk | Probability | Impact | Blast Radius | Mitigation | Kill Switch |
|------|-------------|--------|--------------|------------|-------------|
| **1. Gemini API Free Tier Exhaustion** | Medium | High | All users (chatbot unavailable) | Implement caching (1-hour TTL for common queries); monitor RPM usage; fallback to "Service busy, try again later" message | Disable chatbot globally via `CHATBOT_ENABLED=false` in config |
| **2. Retrieval Quality Degradation** | Medium | Medium | Users get irrelevant answers | A/B test chunking strategies; log relevance scores; implement relevance threshold (>0.7); manual review of 100 random queries/week | Increase relevance threshold to reject low-quality retrievals |
| **3. Qdrant Free Tier Storage Limit** | Low | Medium | Cannot ingest new textbook chapters | Monitor storage usage weekly; optimize chunking (merge small chunks); implement chunk deduplication | Upgrade to Qdrant paid tier (~$25/month for 10GB) |

### Additional Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Hallucination (agent generates info not in context)** | Low | High | Strong agent instructions ("Answer only based on context"); log all responses for review; manual spot-checks |
| **Selected-Text Mode Context Leakage** | Low | High | Unit tests to verify no global embeddings queried; code review; isolated in-memory vector store |
| **Neon PostgreSQL Free Tier Exhaustion** | Low | Low | Implement log rotation (30-day retention); monitor storage usage; archive old logs to S3 if needed |
| **Malicious Input (injection attacks)** | Medium | Low | Input validation (Pydantic); sanitize user queries; no SQL/code execution in backend |

### Guardrails

1. **Relevance Threshold**: Reject retrievals with score <0.7 (tunable)
2. **Query Length Limit**: Max 1000 characters (prevent abuse)
3. **Selected-Text Length Limit**: Max 5000 characters (prevent memory overflow)
4. **Rate Limiting**: 100 req/min per IP (prevent DoS)
5. **Timeout**: 10-second timeout for agent generation (prevent hung requests)

## Evaluation and Validation

### Definition of Done

**Feature is complete when**:
1. ✅ All P1 and P2 user stories pass acceptance tests
2. ✅ Unit test coverage >80% for core modules (chunking, embeddings, retrieval, agent)
3. ✅ Integration tests pass for all API endpoints
4. ✅ Zero hallucinations observed in 100-query test set
5. ✅ p95 latency <3 seconds under 50 concurrent users (load test)
6. ✅ All constitutional principles validated (Section VIII compliance)
7. ✅ Backend deployed to staging and production environments
8. ✅ Frontend component embedded in Docusaurus and functional
9. ✅ Documentation complete (README, API spec, quickstart guide)
10. ✅ Security review passed (no PII leakage, input validation, secrets management)

### Output Validation

**Automated Tests**:
- **Unit Tests**: `pytest backend/tests/unit/` (mock Qdrant, Gemini API)
- **Integration Tests**: `pytest backend/tests/integration/` (real Qdrant, mock Gemini)
- **API Contract Tests**: Validate OpenAPI spec against actual endpoints
- **Load Tests**: `locust` or `k6` (50 concurrent users, 10-minute duration)

**Manual Validation**:
- **Retrieval Accuracy**: Manually review 100 random query-response pairs
- **Citation Correctness**: Verify citations link to correct textbook sections (10 random samples)
- **Selected-Text Isolation**: Test 10 selected-text queries, verify no global embeddings used

**Success Criteria Validation** (from spec.md):
- **SC-001**: 95% accuracy on covered topics → Test with 100 questions derived from textbook
- **SC-002**: Zero hallucinations → Manual review of 100 responses
- **SC-003**: 100% selected-text isolation → Unit tests + manual verification
- **SC-004**: All responses include citations → Automated test (assert `len(citations) > 0`)
- **SC-005**: p95 latency <3s → Load test with 50 concurrent users
- **SC-006**: Free tier operation → Monitor usage for 7 days
- **SC-007**: Zero PII leakage → Log audit + code review
- **SC-008**: 90% retrieval relevance → Log analysis (avg relevance score >0.8)
- **SC-009**: Frontend integration → Manual UI testing in Docusaurus
- **SC-010**: <5% error rate with 50 users → Load test

## Phase Breakdown

### Phase 0: Research and Exploration (1-2 days)

**Goal**: Validate technical assumptions and gather implementation details.

**Tasks**:
1. Research Sentence-Transformers models (benchmark all-MiniLM-L6-v2 vs. all-mpnet-base-v2)
2. Prototype chunking strategy (test on 1-2 textbook chapters)
3. Test Qdrant Cloud Free Tier (create collection, insert 1000 test vectors, query performance)
4. Test Gemini API with AsyncOpenAI (verify compatibility, measure latency)
5. Test OpenAI Assistants SDK with external client (proof of concept)
6. Document findings in `research.md`

**Deliverables**:
- `specs/rag-chatbot/research.md` with benchmarks and recommendations
- Prototype code (discardable) to validate key decisions

---

### Phase 1: Design and Setup (2-3 days)

**Goal**: Finalize architecture, define data models, and set up project scaffolding.

**Tasks**:
1. Define data models (Pydantic schemas for TextChunk, Query, Response, etc.)
2. Design API contracts (OpenAPI spec for FastAPI endpoints)
3. Set up project structure (backend/, frontend/, scripts/)
4. Set up development environment (Python venv, install dependencies)
5. Set up Qdrant Cloud account and create collection
6. Set up Neon PostgreSQL account and create database
7. Configure environment variables (.env.example, secrets management)
8. Write `data-model.md` (schemas, relationships, migration strategy)
9. Write `quickstart.md` (local setup instructions, running tests)
10. Write `contracts/api-spec.yaml` (OpenAPI specification)

**Deliverables**:
- `specs/rag-chatbot/data-model.md`
- `specs/rag-chatbot/quickstart.md`
- `specs/rag-chatbot/contracts/api-spec.yaml`
- Project scaffolding (directory structure, config files)

---

### Phase 2: Backend Core (4-5 days)

**Goal**: Implement chunking, embedding, vector storage, and retrieval.

**Tasks** (see `/sp.tasks` for detailed breakdown):
1. Implement chunking logic (`services/chunking.py`)
2. Implement embedding generation (`services/embeddings.py`)
3. Implement Qdrant client wrapper (`services/vector_store.py`)
4. Write ingestion script (`scripts/ingest_textbook.py`)
5. Ingest 1-2 sample chapters into Qdrant
6. Implement retrieval logic (global query mode)
7. Write unit tests for chunking, embeddings, retrieval
8. Validate retrieval accuracy manually (10 sample queries)

**Deliverables**:
- Functional chunking + embedding pipeline
- Qdrant collection populated with sample chapters
- Unit tests passing (`tests/unit/test_chunking.py`, etc.)

---

### Phase 3: Agent and API (3-4 days)

**Goal**: Implement agent orchestration, FastAPI endpoints, and selected-text mode.

**Tasks**:
1. Implement agent orchestration (`services/agent.py`)
2. Integrate retrieval with agent (retrieval-first pipeline)
3. Implement FastAPI app (`main.py`, `api/routes/chat.py`)
4. Implement POST /chat endpoint (global query mode)
5. Implement POST /chat/selected endpoint (selected-text mode)
6. Implement GET /metadata endpoint (debug)
7. Implement rate limiting middleware
8. Write integration tests for all endpoints
9. Test end-to-end flow (query → retrieval → agent → response)

**Deliverables**:
- Functional FastAPI backend with all endpoints
- Integration tests passing (`tests/integration/test_chat_endpoint.py`)
- Manual testing report (10 queries tested)

---

### Phase 4: Frontend Integration (2-3 days)

**Goal**: Build React chat component and embed in Docusaurus.

**Tasks**:
1. Design chat UI (mockup in Figma or wireframe)
2. Implement ChatWidget component (`frontend/src/components/ChatWidget.tsx`)
3. Implement API client (`frontend/src/services/api.ts`)
4. Implement text selection hook (`frontend/src/hooks/useTextSelection.ts`)
5. Integrate chat widget into Docusaurus (iframe or web component)
6. Test chat widget in Docusaurus environment
7. Style chat widget (responsive, accessible)

**Deliverables**:
- Functional chat widget embedded in Docusaurus
- Frontend tests passing (`frontend/tests/ChatWidget.test.tsx`)
- Manual UI testing report (10 user flows tested)

---

### Phase 5: Testing and Validation (2-3 days)

**Goal**: Comprehensive testing, performance validation, and security review.

**Tasks**:
1. Run unit tests (all modules, >80% coverage)
2. Run integration tests (all endpoints)
3. Run load tests (50 concurrent users, 10 minutes)
4. Validate success criteria (SC-001 to SC-010)
5. Manual retrieval accuracy review (100 queries)
6. Security review (input validation, PII leakage, secrets)
7. Log audit (verify no raw IPs, sensitive data in logs)
8. Fix any issues identified during testing

**Deliverables**:
- All tests passing
- Load test report (p95 latency, error rate)
- Security review report
- Bug fixes (if any)

---

### Phase 6: Deployment and Documentation (1-2 days)

**Goal**: Deploy to production, finalize documentation, and hand off.

**Tasks**:
1. Containerize backend (Dockerfile, docker-compose.yml)
2. Deploy backend to Render/Railway/Fly.io
3. Configure environment variables in production
4. Set up health checks and monitoring
5. Deploy frontend (integrate into Docusaurus build)
6. Write deployment documentation (README, deployment guide)
7. Write user guide (how to use chatbot)
8. Conduct final smoke tests in production
9. Hand off to stakeholders

**Deliverables**:
- Backend deployed to production
- Frontend deployed and functional
- Documentation complete (README.md, deployment guide, user guide)
- Handoff checklist completed

## Architectural Decision Records (ADR) Suggestions

📋 **Architectural decisions detected**. Based on the three-part ADR significance test (Impact + Alternatives + Scope), the following decisions should be documented:

### Recommended ADRs:

1. **ADR-001: Embedding Model Selection (Sentence-Transformers all-MiniLM-L6-v2)**
   - **Impact**: Affects retrieval quality, cost, performance, and free-tier viability (long-term)
   - **Alternatives**: OpenAI embeddings, all-mpnet-base-v2, other models
   - **Scope**: Cross-cutting (affects ingestion, retrieval, storage)
   - **Suggest**: `/sp.adr embedding-model-selection`

2. **ADR-002: Chunking Strategy (Hybrid Section-Aware with 512 Token Max)**
   - **Impact**: Affects retrieval accuracy, user experience, and semantic coherence (long-term)
   - **Alternatives**: Fixed-size, pure section-based, sentence-based
   - **Scope**: Cross-cutting (affects ingestion, retrieval, citations)
   - **Suggest**: `/sp.adr chunking-strategy`

3. **ADR-003: Agent Framework Selection (OpenAI Assistants SDK with AsyncOpenAI + Gemini)**
   - **Impact**: Affects extensibility, agent behavior, and dependencies (long-term)
   - **Alternatives**: LangGraph, ChatKit, custom agent loop
   - **Scope**: Cross-cutting (affects generation, error handling, future multi-step reasoning)
   - **Suggest**: `/sp.adr agent-framework-selection`

**Note**: Other decisions (citation format, rate limiting strategy, selected-text implementation) are straightforward and do not meet the ADR significance criteria.

## Next Steps

1. **Review and Approve Plan**: Stakeholder review of this document
2. **Create ADRs**: Run `/sp.adr embedding-model-selection`, `/sp.adr chunking-strategy`, `/sp.adr agent-framework-selection`
3. **Generate Tasks**: Run `/sp.tasks` to create dependency-ordered, testable tasks
4. **Begin Phase 0**: Start research and validation (embedding benchmark, Qdrant test, Gemini test)
5. **Iterate**: Adjust plan based on Phase 0 findings (document in `research.md`)

## Appendix: Technology Stack Summary

| Layer | Technology | Purpose | Justification |
|-------|------------|---------|---------------|
| **Frontend** | React (TypeScript) | Chat UI component | Docusaurus uses React; seamless integration |
| **Backend** | FastAPI (Python 3.9+) | REST API | Fast, async, type-safe, easy OpenAPI generation |
| **Agent** | OpenAI Assistants SDK + AsyncOpenAI | Agent orchestration | Simple, mature, supports Gemini via external client |
| **LLM** | Gemini-2.0-flash | Response generation | Free tier (15 RPM), good quality, cost-effective |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) | Text → vector | Free, fast, sufficient quality for textbook QA |
| **Vector DB** | Qdrant Cloud Free Tier | Embedding storage + retrieval | Free tier (1GB), fast, good Python SDK |
| **SQL DB** | Neon PostgreSQL Free Tier | Metadata + session logs | Free tier (500MB), serverless, easy setup |
| **Deployment** | Render/Railway/Fly.io | Backend hosting | Free tier, Docker support, easy CI/CD |
| **Testing** | pytest, httpx, pytest-asyncio | Unit + integration tests | Standard Python testing stack |
| **Logging** | Python logging (JSON format) | Observability | Structured logs, easy to parse |

---

**Plan Version**: 1.0
**Last Updated**: 2025-12-25
**Status**: Draft (awaiting approval)
