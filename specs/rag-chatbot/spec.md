# Feature Specification: Integrated RAG Chatbot for Physical AI Textbook

**Feature Branch**: `rag-chatbot`
**Created**: 2025-12-25
**Status**: Draft
**Input**: User description: "Integrated RAG Chatbot for Physical AI & Humanoid Robotics Textbook - AI-native chatbot with grounded retrieval, selected-text mode, and strict citation requirements"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions About Book Content (Priority: P1)

A student reading the textbook encounters an unfamiliar concept and wants immediate clarification without leaving the page. They type a question into the embedded chatbot and receive an answer grounded strictly in the textbook content with clear source citations.

**Why this priority**: This is the core value proposition - providing instant, reliable answers based on book content. Without this, the chatbot has no purpose.

**Independent Test**: Can be fully tested by asking a question about any chapter content (e.g., "What is inverse kinematics?") and verifying the response includes correct information with source citations (chapter/section references).

**Acceptance Scenarios**:

1. **Given** a student is reading Chapter 3 on Kinematics, **When** they ask "What is the Denavit-Hartenberg convention?", **Then** the chatbot responds with an accurate explanation derived from the book with citations showing Chapter 3, Section 3.2
2. **Given** a student asks "What is forward kinematics?", **When** relevant content exists in the book, **Then** the response includes the definition, key concepts, and references to specific sections
3. **Given** a student asks "How do I implement a Kalman filter?", **When** this topic is not covered in the book, **Then** the chatbot responds: "Information not found in the book."
4. **Given** a student asks a vague question like "Tell me about robots", **When** the query is too broad, **Then** the chatbot retrieves the most relevant chunks and provides a focused answer with citations

---

### User Story 2 - Query Selected Text for Contextual Clarification (Priority: P2)

A student highlights a complex paragraph or equation in the textbook and wants clarification or expansion without the chatbot retrieving irrelevant content from other chapters. The chatbot constrains its retrieval and generation to only the selected text.

**Why this priority**: This prevents context pollution and enables precise, focused answers. It's a key differentiator from generic chatbots and aligns with grounded truthfulness principles.

**Independent Test**: Can be tested independently by selecting a specific paragraph (e.g., a derivation in Chapter 4), asking "Explain this step-by-step", and verifying the response uses ONLY the selected text, not global embeddings.

**Acceptance Scenarios**:

1. **Given** a student selects a paragraph about PID control, **When** they ask "Explain the derivative term", **Then** the chatbot responds using only information from the selected text, not from other chapters
2. **Given** a student highlights an equation for Jacobian computation, **When** they ask "What does this equation mean?", **Then** the response explains the equation using context strictly from the selected text
3. **Given** a student selects text that doesn't contain the answer to their question, **When** they ask something not covered in the selection, **Then** the chatbot responds: "Information not found in the selected text."
4. **Given** a student switches from selected-text mode back to normal mode, **When** they ask a new question, **Then** the chatbot correctly queries global embeddings again

---

### User Story 3 - View Source Citations and Navigate to Original Content (Priority: P3)

A student receives an answer from the chatbot and wants to verify the source or read more context. The chatbot provides clickable citations that link directly to the relevant section in the textbook.

**Why this priority**: Builds trust, supports academic integrity, and enables deeper learning. Critical for educational contexts but can be implemented after core Q&A works.

**Independent Test**: Can be tested by asking any question, receiving a response, and clicking on the citation link to verify it navigates to the correct chapter/section in the Docusaurus textbook.

**Acceptance Scenarios**:

1. **Given** a student receives an answer about "humanoid balance control", **When** the response includes a citation like "[Chapter 6, Section 6.3]", **Then** clicking the citation navigates to that exact section in the Docusaurus site
2. **Given** an answer is derived from multiple chunks, **When** the chatbot cites multiple sources, **Then** all citations are displayed clearly with distinct links
3. **Given** a student wants to see which text chunks were retrieved, **When** they enable debug mode, **Then** the chatbot displays all retrieved chunks with similarity scores and metadata

---

### User Story 4 - Asynchronous and Streaming Responses (Priority: P4)

A student asks a complex question requiring substantial retrieval and generation. Instead of waiting for a complete response, they see the answer stream token-by-token in real-time, improving perceived responsiveness.

**Why this priority**: Enhances UX and reduces perceived latency. Not critical for MVP but important for production polish.

**Independent Test**: Can be tested by asking a question that generates a long response and observing that tokens appear progressively rather than all at once.

**Acceptance Scenarios**:

1. **Given** a student asks a complex question, **When** the response is being generated, **Then** text appears incrementally in the chat interface
2. **Given** the backend is processing retrieval, **When** chunks are being retrieved, **Then** the frontend shows a loading indicator before streaming begins
3. **Given** an error occurs during generation, **When** streaming is interrupted, **Then** the partial response is preserved and an error message is displayed

---

### Edge Cases

- **Empty Query**: What happens when a user submits an empty or whitespace-only question?
  - **Expected**: System returns a prompt like "Please enter a question."

- **Non-English Queries**: What happens if the user asks a question in a language other than English?
  - **Expected**: System responds: "I can only answer questions in English based on the textbook content."

- **Very Long Selected Text**: What happens when a user selects an entire chapter (thousands of words)?
  - **Expected**: System chunks the selected text and retrieves the most relevant portions, or warns if the selection is too large.

- **Concurrent Requests**: What happens when a user submits multiple questions rapidly?
  - **Expected**: Each request is handled independently; responses may arrive out of order but are correctly associated with their questions.

- **Malformed API Requests**: What happens if the frontend sends invalid JSON or missing required fields?
  - **Expected**: Backend returns a 400 error with a clear error message indicating the validation failure.

- **Vector DB Unavailable**: What happens if Qdrant is down or unreachable?
  - **Expected**: System returns an error: "Chatbot temporarily unavailable. Please try again later."

- **Rate Limiting**: What happens if a user exceeds API rate limits (e.g., 100 requests/minute)?
  - **Expected**: Backend returns 429 Too Many Requests with a Retry-After header.

- **No Retrieved Chunks**: What happens when the retrieval system finds zero relevant chunks (similarity score too low)?
  - **Expected**: System responds: "Information not found in the book."

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST respond to user questions using only content from the indexed textbook or user-selected text
- **FR-002**: System MUST return "Information not found in the book." when no relevant content is retrieved or similarity scores are below the threshold
- **FR-003**: System MUST support selected-text mode where retrieval is constrained strictly to the highlighted text (no global embeddings queried)
- **FR-004**: System MUST cite the source of all answers with chapter, section, and chunk metadata
- **FR-005**: System MUST use the Gemini-2.0-flash model via the AsyncOpenAI client for response generation
- **FR-006**: System MUST implement an AI agent using OpenAI Assistants SDK or ChatKit with the instruction: "Please answer the question to the best of your ability based on the provided context."
- **FR-007**: System MUST chunk textbook content using a semantic + section-aware strategy preserving chapter/section boundaries
- **FR-008**: System MUST store all vector embeddings in Qdrant Cloud Free Tier with metadata (chapter, section, URL anchor)
- **FR-009**: System MUST store session metadata and user interaction logs in Neon PostgreSQL
- **FR-010**: System MUST load all API keys and credentials securely from environment variables (GEMINI_API_KEY, QDRANT_API_KEY, NEON_DATABASE_URL)
- **FR-011**: System MUST expose stateless FastAPI endpoints for question submission, selected-text submission, and retrieval metadata
- **FR-012**: System MUST return answers along with source references in a structured JSON format
- **FR-013**: System MUST support both synchronous and asynchronous execution modes
- **FR-014**: System MUST implement streaming responses for real-time token delivery (Priority P4)
- **FR-015**: System MUST validate all incoming requests and return clear error messages for invalid inputs

### Non-Functional Requirements

- **NFR-001**: System MUST respond to queries within 3 seconds (p95 latency) under normal load
- **NFR-002**: System MUST operate within Qdrant Cloud Free Tier limits (1GB storage, 1M vectors)
- **NFR-003**: System MUST operate within Neon PostgreSQL Free Tier limits (500MB storage)
- **NFR-004**: System MUST handle at least 50 concurrent users without degradation
- **NFR-005**: System MUST log all retrieval and generation events for debugging and evaluation
- **NFR-006**: System MUST NOT store personally identifiable information (PII) from user queries
- **NFR-007**: System MUST be deployable independently from the Docusaurus frontend
- **NFR-008**: System MUST use HTTPS for all external API communication
- **NFR-009**: System MUST implement rate limiting (100 requests/minute per IP address)
- **NFR-010**: System MUST provide observability via structured logging (JSON logs with trace IDs)

### Key Entities

- **TextChunk**: Represents a semantically coherent segment of textbook content
  - Attributes: chunk_id, text, embedding_vector, chapter, section, url_anchor, token_count
  - Relationships: Belongs to a Chapter and Section

- **Query**: Represents a user question submitted to the chatbot
  - Attributes: query_id, query_text, timestamp, mode (global | selected-text), session_id
  - Relationships: Produces one Response, retrieves multiple TextChunks

- **Response**: Represents the chatbot's answer to a Query
  - Attributes: response_id, response_text, query_id, model, generation_time, citations
  - Relationships: Belongs to one Query, cites multiple TextChunks

- **SelectedText**: Represents text explicitly highlighted by the user
  - Attributes: selection_id, selected_text, timestamp, session_id
  - Relationships: Used to constrain retrieval for selected-text mode queries

- **Session**: Represents a user's interaction session (for logging and debugging)
  - Attributes: session_id, created_at, user_agent, ip_address (hashed for privacy)
  - Relationships: Contains multiple Queries

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chatbot correctly answers 95% of questions about content explicitly covered in the textbook (measured via test question set)
- **SC-002**: Chatbot returns "Information not found in the book" for 100% of questions about topics not covered in the textbook (zero hallucinations)
- **SC-003**: Selected-text mode queries retrieve zero chunks from outside the selected text scope (100% isolation)
- **SC-004**: All chatbot responses include valid source citations (chapter, section, chunk ID) traceable to the original textbook
- **SC-005**: 95% of queries receive responses within 3 seconds (p95 latency)
- **SC-006**: System operates successfully within Qdrant and Neon free tier limits for 1000+ queries/day
- **SC-007**: Zero PII leakage incidents (verified via log audits)
- **SC-008**: Retrieval accuracy: 90% of retrieved chunks are semantically relevant to the query (measured via manual evaluation)
- **SC-009**: Frontend integration: chatbot UI is seamlessly embedded in Docusaurus with zero layout breaks
- **SC-010**: System handles 50 concurrent users with <5% error rate

## Out of Scope

The following are explicitly OUT OF SCOPE for this feature:

- **Multi-language Support**: Chatbot will only support English queries and English textbook content
- **User Accounts and Authentication**: No user login or personalization features
- **Query History Persistence**: Users cannot view past conversations across sessions
- **Fine-tuning or Model Training**: No custom model training; only pre-trained Gemini-2.0-flash is used
- **Textbook Content Editing**: Chatbot cannot modify or suggest edits to the textbook itself
- **External Knowledge Sources**: Chatbot will not retrieve or use information from sources outside the textbook
- **Voice Input/Output**: No speech-to-text or text-to-speech capabilities
- **Feedback Collection**: No thumbs-up/down or explicit user feedback mechanisms (may be added in future iterations)
- **Advanced Agent Behaviors**: No multi-step reasoning, tool use, or autonomous task execution beyond simple retrieval and generation

## Technical Constraints

### Architecture Constraints

- **Backend**: MUST use FastAPI (Python 3.9+)
- **Agent Framework**: MUST use OpenAI Assistants SDK or ChatKit
- **LLM**: MUST use Gemini-2.0-flash via AsyncOpenAI client with base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
- **Vector Database**: MUST use Qdrant Cloud Free Tier
- **Relational Database**: MUST use Neon PostgreSQL Free Tier
- **Frontend Integration**: MUST be embeddable in Docusaurus via iframe or web component
- **Deployment**: Backend MUST be containerized (Docker) and deployable to free-tier platforms (Render, Railway, or Fly.io)

### Data Constraints

- **Chunking Strategy**: Semantic + section-aware chunking with max chunk size of 512 tokens
- **Embedding Model**: MUST use a model compatible with Qdrant and optimized for semantic search (e.g., text-embedding-3-small or equivalent open-source model)
- **Metadata Schema**: Each chunk MUST include: chapter, section, subsection, url_anchor, token_count, chunk_index

### Security Constraints

- **API Keys**: MUST be loaded from environment variables (never hardcoded)
- **Input Validation**: All user inputs MUST be sanitized to prevent injection attacks
- **Rate Limiting**: MUST enforce 100 requests/minute per IP address
- **HTTPS Only**: All external API calls MUST use HTTPS
- **No PII Storage**: User queries may be logged for debugging but MUST NOT include PII

## Dependencies

### External Services

- **Qdrant Cloud**: Free Tier (1GB storage, 1M vectors)
- **Neon PostgreSQL**: Free Tier (500MB storage)
- **Gemini API**: Requires GEMINI_API_KEY (free tier: 15 RPM, 1M TPM, 1500 RPD)

### Python Libraries

- **FastAPI**: Web framework for API endpoints
- **Uvicorn**: ASGI server for FastAPI
- **OpenAI SDK**: For AsyncOpenAI client and agent orchestration
- **Qdrant Client**: Python client for Qdrant vector database
- **Psycopg3**: PostgreSQL adapter for Python
- **python-dotenv**: Environment variable management
- **Pydantic**: Data validation and serialization
- **LangChain or ChatKit**: Agent orchestration (if not using OpenAI Assistants SDK directly)

### Frontend Dependencies

- **Docusaurus**: Textbook platform (existing)
- **React**: For chat UI component
- **Axios or Fetch API**: For backend communication

## Open Questions

1. **Chunking Strategy**: Should we use fixed-size chunks (512 tokens) or variable-size chunks based on section boundaries?
   - **Recommendation**: Hybrid approach - prefer section boundaries but enforce max 512 tokens

2. **Embedding Model**: Which embedding model should we use? Options:
   - OpenAI text-embedding-3-small (paid, high quality)
   - Sentence-Transformers all-MiniLM-L6-v2 (free, good quality)
   - **Recommendation**: Start with Sentence-Transformers for cost efficiency; evaluate quality

3. **Citation Format**: How should citations be displayed in the chat UI?
   - Option A: Inline links like "[Chapter 3, Section 3.2]"
   - Option B: Footnote-style references like "[1] Chapter 3, Section 3.2"
   - **Recommendation**: Option A for simplicity and immediate context

4. **Selected-Text Mode Activation**: How does the user activate selected-text mode?
   - Option A: Right-click context menu "Ask about this text"
   - Option B: Automatic detection when text is highlighted and chat is focused
   - **Recommendation**: Option B for smoother UX

5. **Error Handling for Free Tier Limits**: What happens if Qdrant or Neon free tier limits are exceeded?
   - **Recommendation**: Implement graceful degradation with clear error messages and consider caching strategies

## Next Steps

After specification approval:

1. Run `/sp.plan` to create the architectural design and implementation plan
2. Run `/sp.tasks` to generate actionable, dependency-ordered tasks
3. Identify architecturally significant decisions and document them via `/sp.adr`
4. Begin implementation starting with P1 user story (core Q&A functionality)

## Revision History

| Version | Date       | Author | Changes                              |
|---------|------------|--------|--------------------------------------|
| 1.0     | 2025-12-25 | Agent  | Initial specification draft created  |
