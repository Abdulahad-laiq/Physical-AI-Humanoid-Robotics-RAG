# Tasks: Integrated RAG Chatbot for Physical AI Textbook

**Input**: Design documents from `/specs/rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Focus is on implementation and manual validation per success criteria.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/src/`, `frontend/src/` (per plan.md)
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per plan.md (backend/, frontend/, scripts/, specs/, history/)
- [X] T002 [P] Initialize Python virtual environment and install backend dependencies in backend/requirements.txt (FastAPI, openai, qdrant-client, psycopg[binary], pydantic, python-dotenv, sentence-transformers, uvicorn, httpx, pytest, pytest-asyncio)
- [X] T003 [P] Create .env.example with required environment variables (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, NEON_DATABASE_URL, QDRANT_COLLECTION_NAME)
- [X] T004 [P] Initialize frontend React project in frontend/ with TypeScript, Axios, and React hooks
- [X] T005 [P] Create .gitignore for Python, Node.js, and environment files
- [ ] T006 Set up Qdrant Cloud Free Tier account and create collection (textbook_chunks_v1, 384 dimensions) - **MANUAL SETUP REQUIRED**
- [ ] T007 Set up Neon PostgreSQL Free Tier account and create database (rag_chatbot_db) - **MANUAL SETUP REQUIRED**
- [X] T008 [P] Create backend/Dockerfile for containerization
- [X] T009 [P] Write backend/README.md with setup instructions and architecture overview

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 [P] Create Pydantic data models in backend/src/models/schemas.py (TextChunk, QueryRequest, SelectedTextQueryRequest, Citation, ChatResponse)
- [X] T011 [P] Create database session management in backend/src/models/database.py (Neon PostgreSQL connection, Session schema for query logging)
- [X] T012 [P] Implement chunking logic in backend/src/services/chunking.py (hybrid section-aware strategy, 512 token max, spaCy sentence splitting)
- [X] T013 [P] Implement embedding generation in backend/src/services/embeddings.py (Sentence-Transformers all-MiniLM-L6-v2, 384 dimensions)
- [X] T014 Implement Qdrant client wrapper in backend/src/services/vector_store.py (collection management, upsert, query with metadata filtering)
- [X] T015 [P] Implement configuration management in backend/src/config.py (load environment variables, validate required settings)
- [X] T016 [P] Implement structured logging in backend/src/utils/logger.py (JSON format, query_id tracking, log levels)
- [X] T017 [P] Implement input validation helpers in backend/src/utils/validators.py (sanitize user queries, validate request payloads)
- [X] T018 Create textbook ingestion script in backend/scripts/ingest_textbook.py (chunk Markdown files, generate embeddings, upsert to Qdrant with metadata)
- [X] T019 Create Qdrant collection initialization script in backend/scripts/setup_qdrant.py (create collection with correct dimension and distance metric)
- [X] T020 Initialize Neon PostgreSQL schema with Alembic migrations in backend/alembic/ (queries table: query_id, query_text, timestamp, mode, session_id_hash, response_time_ms)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Ask Questions About Book Content (Priority: P1) 🎯 MVP

**Goal**: Students can ask questions about textbook content and receive accurate, grounded answers with source citations.

**Independent Test**: Ask "What is inverse kinematics?" and verify response includes correct information with citations (e.g., "[Chapter 3, Section 3.2]"). Ask "How do I implement a Kalman filter?" (not in book) and verify response is "Information not found in the book."

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement agent orchestration in backend/src/services/agent.py (AsyncOpenAI client, Gemini-2.0-flash model, Agent class with grounded instructions, sync/async execution)
- [X] T022 [P] [US1] Implement retrieval-agent integration in backend/src/services/agent.py (format retrieved chunks as context, call agent with query + context, parse response with citations)
- [X] T023 [P] [US1] Create FastAPI app structure in backend/src/main.py (app initialization, CORS middleware, error handlers, startup/shutdown events)
- [X] T024 [P] [US1] Implement rate limiting middleware in backend/src/api/middleware.py (IP-based, 100 req/min, 429 error with Retry-After header)
- [X] T025 [US1] Implement POST /api/v1/chat endpoint in backend/src/api/routes/chat.py (validate QueryRequest, retrieve chunks from Qdrant, call agent, format ChatResponse with citations, log query metadata)
- [X] T026 [US1] Implement error handling for POST /chat in backend/src/api/routes/chat.py (empty query → 400, Qdrant unavailable → 503, Gemini timeout → 500, no chunks found → "Information not found")
- [X] T027 [US1] Add query logging to Neon PostgreSQL in backend/src/api/routes/chat.py (anonymize IP, store query_id, query_text, mode=global, response_time_ms)
- [ ] T028 [US1] Ingest 2 sample textbook chapters using backend/scripts/ingest_textbook.py (test chunking, embeddings, Qdrant upsert) - **REQUIRES T006/T007 SETUP**
- [ ] T029 [US1] Manual validation: Test 10 questions from ingested chapters (verify citations, accuracy, "not found" for out-of-scope) - **MANUAL TESTING**
- [ ] T030 [US1] Validate p95 latency <3 seconds with 10 concurrent requests using manual testing or simple load script - **MANUAL TESTING**

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently via API calls (e.g., curl, Postman)

---

## Phase 4: User Story 2 - Query Selected Text for Contextual Clarification (Priority: P2)

**Goal**: Students can highlight text in the textbook and ask questions constrained strictly to that selection, preventing context pollution from other chapters.

**Independent Test**: Select a paragraph about "PID control", ask "Explain the derivative term", and verify response uses ONLY selected text (no global embeddings). Verify switching back to global mode works correctly.

### Implementation for User Story 2

- [X] T031 [P] [US2] Implement selected-text mode logic in backend/src/services/selected_text.py (chunk selected text, embed on-demand, create ephemeral in-memory vector store, retrieve top-k from ephemeral store only)
- [X] T032 [US2] Implement POST /api/v1/chat/selected endpoint in backend/src/api/routes/selected_text.py (validate SelectedTextQueryRequest, call selected_text service, call agent with ephemeral context, return ChatResponse with source=selected_text)
- [X] T033 [US2] Implement error handling for POST /chat/selected in backend/src/api/routes/selected_text.py (selected_text >5000 chars → 400, selected_text <10 chars → 400, no relevant chunks in selection → "Information not found in the selected text")
- [X] T034 [US2] Add query logging for selected-text mode in backend/src/api/routes/selected_text.py (mode=selected-text, anonymize selected_text in logs)
- [ ] T035 [US2] Manual validation: Test 5 selected-text queries (verify isolation, no global embeddings queried, accurate responses) - **MANUAL TESTING**
- [ ] T036 [US2] Validate mode switching: Test global query → selected-text query → global query sequence - **MANUAL TESTING**

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently via API

---

## Phase 5: Frontend Integration for User Stories 1 and 2

**Goal**: Embed chatbot UI in Docusaurus textbook with support for global queries and selected-text queries.

**Independent Test**: Open Docusaurus textbook, type a question in chat widget, receive answer. Highlight text, click "Ask about this text", ask question, receive answer constrained to selection.

### Implementation for Frontend

- [X] T037 [P] [US1] Create ChatWidget component in frontend/src/components/ChatWidget.tsx (message list, input field, send button, loading state, error display)
- [X] T038 [P] [US1] Create ChatMessage component in frontend/src/components/ChatMessage.tsx (render answer text, display citations as inline links, show timestamps)
- [X] T039 [P] [US1] Create ChatInput component in frontend/src/components/ChatInput.tsx (textarea with validation, character counter, submit on Enter)
- [X] T040 [P] [US1] Implement API client in frontend/src/services/api.ts (POST /chat with error handling, retry logic for 429, timeout handling)
- [X] T041 [US1] Integrate ChatWidget with API client in frontend/src/components/ChatWidget.tsx (handle submit, call API, display response, handle errors)
- [X] T042 [P] [US2] Implement text selection hook in frontend/src/hooks/useTextSelection.ts (detect highlighted text, expose selection state, handle deselection)
- [X] T043 [P] [US2] Create SelectedTextButton component in frontend/src/components/SelectedTextButton.tsx ("Ask about this text" button, appears on text selection, triggers selected-text mode)
- [X] T044 [US2] Implement POST /chat/selected integration in frontend/src/services/api.ts (send selected_text + query, handle selected-text errors)
- [X] T045 [US2] Integrate selected-text mode in frontend/src/components/ChatWidget.tsx (toggle mode on button click, clear selection after submit, visual indicator for selected-text mode)
- [X] T046 [P] Style chat widget in frontend/src/styles/chat.css (responsive design, Docusaurus theme integration, mobile-friendly, accessibility)
- [X] T047 Embed ChatWidget in Docusaurus via iframe or web component (update Docusaurus config, test embedding)
- [ ] T048 Manual UI validation: Test chat widget in Docusaurus (10 queries, 5 selected-text queries, verify layout, errors, mobile responsiveness) - **MANUAL TESTING**

**Checkpoint**: Frontend fully integrated; User Stories 1 and 2 testable end-to-end in Docusaurus

---

## Phase 6: User Story 3 - View Source Citations and Navigate to Original Content (Priority: P3)

**Goal**: Students can click citations to navigate directly to the source section in the textbook, building trust and enabling deeper learning.

**Independent Test**: Ask "What is humanoid balance control?", receive answer with citation "[Chapter 6, Section 6.3]", click citation, verify navigation to Chapter 6, Section 6.3 in Docusaurus.

### Implementation for User Story 3

- [ ] T049 [P] [US3] Implement GET /api/v1/metadata endpoint in backend/src/api/routes/metadata.py (retrieve query metadata by query_id, return retrieved chunks with similarity scores and metadata for debug mode)
- [ ] T050 [US3] Enhance citation format in backend/src/services/agent.py (include url_anchor in citation metadata, format as clickable links)
- [ ] T051 [P] [US3] Implement citation click handler in frontend/src/components/ChatMessage.tsx (parse citations, convert to clickable links with href=#url_anchor, handle navigation)
- [ ] T052 [US3] Add debug mode toggle in frontend/src/components/ChatWidget.tsx (fetch and display retrieved chunks from GET /metadata, show similarity scores)
- [ ] T053 [US3] Manual validation: Test citation navigation (5 questions, verify all citations link correctly, test multi-chunk answers)

**Checkpoint**: All user stories (P1, P2, P3) are independently functional and integrated

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T054 [P] Ingest remaining textbook chapters (6-10 chapters) using backend/scripts/ingest_textbook.py
- [ ] T055 [P] Write backend deployment documentation in backend/README.md (Docker setup, environment variables, deployment to Render/Railway/Fly.io)
- [ ] T056 [P] Write frontend deployment documentation in frontend/README.md (build process, embedding in Docusaurus, configuration)
- [ ] T057 [P] Create quickstart guide in specs/rag-chatbot/quickstart.md (local development setup, running backend, running frontend, testing end-to-end)
- [ ] T058 [P] Optimize chunking strategy based on retrieval accuracy manual review (adjust token limits, evaluate edge cases like long equations)
- [ ] T059 [P] Implement query caching for common questions in backend/src/services/agent.py (1-hour TTL, reduce Gemini API calls)
- [ ] T060 [P] Add monitoring and alerting setup documentation (Qdrant storage monitoring, Gemini RPM tracking, p95 latency logging)
- [ ] T061 Code cleanup and refactoring (remove debug print statements, standardize error messages, improve code comments)
- [ ] T062 Security hardening review (verify no PII in logs, validate all inputs sanitized, confirm secrets in environment variables)
- [ ] T063 Perform final success criteria validation per spec.md (SC-001 to SC-010: accuracy, zero hallucinations, isolation, citations, latency, free tier operation)
- [ ] T064 [P] Update ADRs with evaluation evidence from Phase 0 research and implementation learnings (add benchmarks to ADR-001, chunking quality to ADR-002, agent performance to ADR-003)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T009) completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T010-T020) completion
- **User Story 2 (Phase 4)**: Depends on Foundational (T010-T020) completion - Can run in parallel with US1 backend tasks
- **Frontend (Phase 5)**: Depends on User Story 1 backend (T021-T030) AND User Story 2 backend (T031-T036) completion
- **User Story 3 (Phase 6)**: Depends on Frontend (T037-T048) completion
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Backend tasks (T031-T036) can run in parallel with US1 backend; frontend tasks (T042-T045) depend on US1 frontend (T037-T041) completion
- **User Story 3 (P3)**: Depends on US1 and US2 frontend completion - Builds on existing chat widget

### Within Each User Story

- **User Story 1**:
  - T021 (agent) and T022 (retrieval-agent) and T023 (FastAPI app) and T024 (rate limiting) can run in parallel [P]
  - T025 (POST /chat endpoint) depends on T021, T022, T023, T024
  - T026 (error handling) and T027 (logging) depend on T025
  - T028 (ingest chapters) can run in parallel with T021-T027 [P]
  - T029 (manual validation) depends on T025, T026, T027, T028
  - T030 (latency validation) depends on T029

- **User Story 2**:
  - T031 (selected-text logic) can run in parallel with US1 backend tasks
  - T032 (POST /chat/selected endpoint) depends on T031 and T021 (agent from US1)
  - T033 (error handling) and T034 (logging) depend on T032
  - T035 (manual validation) and T036 (mode switching) depend on T032, T033, T034

- **Frontend** (serves US1 and US2):
  - T037 (ChatWidget), T038 (ChatMessage), T039 (ChatInput), T040 (API client) can run in parallel [P]
  - T041 (integrate ChatWidget) depends on T037, T038, T039, T040
  - T042 (text selection hook), T043 (SelectedTextButton) can run in parallel [P]
  - T044 (selected-text API integration) can run in parallel with T042, T043 [P]
  - T045 (integrate selected-text mode) depends on T041, T042, T043, T044
  - T046 (styling) can run in parallel [P]
  - T047 (embed in Docusaurus) depends on T041, T045, T046
  - T048 (manual UI validation) depends on T047

- **User Story 3**:
  - T049 (GET /metadata endpoint), T050 (enhance citations), T051 (citation click handler) can run in parallel [P]
  - T052 (debug mode toggle) depends on T049, T051
  - T053 (manual validation) depends on T050, T051, T052

### Parallel Opportunities

- **Setup**: T002, T003, T004, T005, T008, T009 can run in parallel (different files)
- **Foundational**: T010, T011, T012, T013, T015, T016, T017 can run in parallel (different files)
- **User Story 1**: T021, T022, T023, T024, T028 can run in parallel
- **User Story 2 Backend**: T031 can run in parallel with US1 backend tasks (T021-T027)
- **Frontend**: T037, T038, T039, T040, T042, T043, T044, T046 can run in parallel (different files/components)
- **User Story 3**: T049, T050, T051 can run in parallel
- **Polish**: T054, T055, T056, T057, T058, T059, T060, T064 can run in parallel (different files)

---

## Parallel Example: Foundational Phase

```bash
# Launch all parallel foundational tasks together:
Task T010: "Create Pydantic data models in backend/src/models/schemas.py"
Task T011: "Create database session management in backend/src/models/database.py"
Task T012: "Implement chunking logic in backend/src/services/chunking.py"
Task T013: "Implement embedding generation in backend/src/services/embeddings.py"
Task T015: "Implement configuration management in backend/src/config.py"
Task T016: "Implement structured logging in backend/src/utils/logger.py"
Task T017: "Implement input validation helpers in backend/src/utils/validators.py"
```

## Parallel Example: User Story 1 Backend

```bash
# Launch all parallel User Story 1 backend tasks together:
Task T021: "Implement agent orchestration in backend/src/services/agent.py"
Task T022: "Implement retrieval-agent integration in backend/src/services/agent.py"
Task T023: "Create FastAPI app structure in backend/src/main.py"
Task T024: "Implement rate limiting middleware in backend/src/api/middleware.py"
Task T028: "Ingest 2 sample textbook chapters using backend/scripts/ingest_textbook.py"
```

## Parallel Example: Frontend Components

```bash
# Launch all parallel frontend component tasks together:
Task T037: "Create ChatWidget component in frontend/src/components/ChatWidget.tsx"
Task T038: "Create ChatMessage component in frontend/src/components/ChatMessage.tsx"
Task T039: "Create ChatInput component in frontend/src/components/ChatInput.tsx"
Task T040: "Implement API client in frontend/src/services/api.ts"
Task T042: "Implement text selection hook in frontend/src/hooks/useTextSelection.ts"
Task T043: "Create SelectedTextButton component in frontend/src/components/SelectedTextButton.tsx"
Task T044: "Implement POST /chat/selected integration in frontend/src/services/api.ts"
Task T046: "Style chat widget in frontend/src/styles/chat.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T020) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 Backend (T021-T030)
4. Complete Phase 5: Frontend for User Story 1 (T037-T041, T046-T048)
5. **STOP and VALIDATE**: Test User Story 1 independently end-to-end
6. Deploy/demo if ready

**Estimated MVP Scope**: 39 tasks (T001-T009, T010-T020, T021-T030, T037-T041, T046-T048)

### Incremental Delivery

1. Complete Setup + Foundational (T001-T020) → Foundation ready
2. Add User Story 1 Backend (T021-T030) → Test API independently
3. Add Frontend for User Story 1 (T037-T041, T046-T048) → Test UI independently → **Deploy/Demo (MVP!)**
4. Add User Story 2 Backend (T031-T036) → Test API independently
5. Add Frontend for User Story 2 (T042-T045) → Test UI independently → **Deploy/Demo (Enhanced!)**
6. Add User Story 3 (T049-T053) → Test independently → **Deploy/Demo (Citations!)**
7. Polish (T054-T064) → **Production Ready**

Each increment adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T020)
2. Once Foundational is done:
   - **Developer A**: User Story 1 Backend (T021-T030)
   - **Developer B**: User Story 2 Backend (T031-T036) *in parallel*
   - **Developer C**: Frontend components (T037-T040, T042-T044, T046) *in parallel*
3. Integration:
   - Developer A or C: Integrate US1 frontend (T041, T047-T048)
   - Developer B or C: Integrate US2 frontend (T045)
4. User Story 3 can start once US1+US2 frontend complete (T049-T053)

---

## Summary

- **Total Tasks**: 64 tasks
- **Setup**: 9 tasks (T001-T009)
- **Foundational**: 11 tasks (T010-T020)
- **User Story 1 (P1)**: 10 tasks (T021-T030) - **MVP Core**
- **User Story 2 (P2)**: 6 tasks (T031-T036)
- **Frontend (US1+US2)**: 12 tasks (T037-T048)
- **User Story 3 (P3)**: 5 tasks (T049-T053)
- **Polish**: 11 tasks (T054-T064)

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phases

**Independent Test Criteria**:
- **US1**: Ask question → receive answer with citations OR "Information not found in the book"
- **US2**: Select text → ask question → receive answer using ONLY selected text
- **US3**: Click citation → navigate to source section in Docusaurus

**Suggested MVP Scope**: User Story 1 only (Setup + Foundational + US1 Backend + US1 Frontend = 39 tasks)

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label (US1, US2, US3) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included (not requested in spec); manual validation used instead
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ All task IDs sequential (T001-T064)
✅ All [P] markers indicate parallelizable tasks (different files, no dependencies)
✅ All [Story] labels map to user stories (US1, US2, US3)
✅ All descriptions include exact file paths
✅ Organization by user story enables independent implementation and testing
