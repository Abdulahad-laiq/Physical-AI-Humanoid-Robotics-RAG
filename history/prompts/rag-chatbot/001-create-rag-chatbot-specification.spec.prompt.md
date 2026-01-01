---
id: 001
title: Create RAG Chatbot Specification
stage: spec
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot
branch: main
user: binary
command: /sp.specify
labels: ["spec", "rag", "chatbot", "ai-native", "retrieval", "gemini"]
links:
  spec: specs/rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/rag-chatbot/spec.md
  - history/prompts/rag-chatbot/001-create-rag-chatbot-specification.spec.prompt.md
tests:
  - Specification completeness validation
  - Constitutional alignment verification
---

## Prompt

/sp.specify
Project: Integrated RAG Chatbot for Physical AI & Humanoid Robotics Textbook

Purpose:
Define the detailed technical and functional specifications for implementing a Retrieval-Augmented
Generation (RAG) chatbot embedded in a Docusaurus-based textbook. The chatbot must answer
questions based strictly on the book content or user-selected text.

Functional Requirements:
1. Question-Answering:
   - Respond to user queries using only book content or explicitly selected text.
   - If the answer is unavailable in the provided text, respond with:
     "Information not found in the book."

2. Selected-Text Mode:
   - When a user highlights text, retrieval and generation must be constrained to that scope.
   - Do not query global embeddings in this mode.

3. Agent:
   - Implement using OpenAI/ChatKit SDKs.
   - Agent instructions: "please answer the question to the best of your ability."
   - Must support synchronous and asynchronous execution.

4. Model:
   - Use Gemini-2.0-flash model through the AsyncOpenAI client.
   - All API keys and credentials must be loaded securely from environment variables.

5. API Endpoints:
   - Backend built with FastAPI
   - Stateless endpoints for:
     - Question submission
     - Selected-text submission
     - Retrieval metadata
   - Return answer along with source references (chapter, section, chunk ID)

6. Database & Vector Storage:
   - Neon Postgres for session & metadata storage
   - Qdrant Cloud Free Tier for vector embeddings
   - Chunking strategy: semantic + section-aware
   - Store all embeddings with source metadata (chapter, section, URL anchor)

Technical Specifications:
1. Agent Setup Example (Python):
   ```python
   from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
   import os
   from dotenv import load_dotenv

   load_dotenv()
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

   external_client = AsyncOpenAI(api_key=GEMINI_API_KEY,
                                 base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

   model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client)

   config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

   agent = Agent(name="Assistant", instructions="please answer the question to the best of your ability.")

   result = Runner.run_sync(agent, "What is the capital of France?", run_config=config)
   print(result.final_output)
   ```

## Response snapshot

Created comprehensive feature specification for RAG Chatbot system.

Key deliverables:
1. **User Stories (P1-P4)**:
   - P1: Core Q&A functionality with grounded responses and citations
   - P2: Selected-text mode for contextual, isolated queries
   - P3: Clickable source citations with navigation to textbook sections
   - P4: Streaming responses for improved UX

2. **Functional Requirements (FR-001 to FR-015)**:
   - Grounded retrieval with "Information not found" fallback
   - Selected-text isolation (no global embedding leakage)
   - Gemini-2.0-flash via AsyncOpenAI
   - Agent orchestration with OpenAI SDK/ChatKit
   - Stateless FastAPI endpoints
   - Qdrant + Neon storage with metadata
   - Secure credential management

3. **Non-Functional Requirements (NFR-001 to NFR-010)**:
   - p95 latency < 3 seconds
   - Free tier operation (Qdrant, Neon)
   - 50 concurrent users capacity
   - No PII storage
   - Rate limiting and observability

4. **Key Entities**:
   - TextChunk (embeddings + metadata)
   - Query (user questions, modes)
   - Response (answers + citations)
   - SelectedText (highlighted content)
   - Session (logging/debugging)

5. **Success Criteria (SC-001 to SC-010)**:
   - 95% accuracy on covered topics
   - Zero hallucinations (100% "not found" for out-of-scope)
   - 100% isolation in selected-text mode
   - All responses include valid citations
   - Performance and cost targets met

6. **Edge Cases Covered**:
   - Empty queries, non-English, very long selections
   - Concurrent requests, malformed API calls
   - Vector DB unavailability, rate limiting
   - Zero retrieval matches

7. **Technical Constraints**:
   - FastAPI + Gemini-2.0-flash + Qdrant + Neon
   - Semantic + section-aware chunking (512 tokens max)
   - Docker deployment to free-tier platforms
   - HTTPS, input validation, rate limiting

8. **Open Questions Documented**:
   - Chunking strategy details (hybrid recommended)
   - Embedding model choice (Sentence-Transformers recommended)
   - Citation format (inline links recommended)
   - Selected-text activation UX (auto-detection recommended)
   - Free tier limit handling (graceful degradation)

## Outcome

- ✅ Impact: Comprehensive, actionable specification created for RAG Chatbot feature aligned with constitutional principles
- 🧪 Tests: Specification completeness validated; constitutional alignment verified
- 📁 Files: specs/rag-chatbot/spec.md created (v1.0)
- 🔁 Next prompts: /sp.plan (architecture design), /sp.tasks (task breakdown), /sp.adr (architectural decisions)
- 🧠 Reflection: Spec balances technical precision with user-centric design; prioritized user stories enable incremental delivery; open questions captured for planning phase

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL):
  - Constitutional alignment: PASS (all Section VIII principles covered)
  - Template adherence: PASS (all mandatory sections present)
  - Testability: PASS (all user stories independently testable)
  - Clarity: PASS (requirements unambiguous, no placeholder text)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute /sp.plan to validate architectural feasibility of specified requirements
