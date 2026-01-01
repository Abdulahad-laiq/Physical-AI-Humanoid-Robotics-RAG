---
id: 002
title: RAG Chatbot Constitution Definition
stage: constitution
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "rag", "chatbot", "architecture", "ai-native"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/002-rag-chatbot-constitution.constitution.prompt.md
tests:
  - N/A (constitutional definition)
---

## Prompt

/sp.constitution
Project: Integrated RAG Chatbot for a Physical AI & Humanoid Robotics Textbook

Purpose:
Define the constitutional principles, standards, and constraints for designing and implementing
an AI-native Retrieval-Augmented Generation (RAG) chatbot embedded within a Docusaurus-based
textbook. The chatbot must answer questions grounded strictly in the book's content and support
context-aware responses based on user-selected text.

Core Principles:
- Grounded Truthfulness: All chatbot responses must be derived strictly from indexed book content
  or explicitly selected user text. No hallucinated or external knowledge is allowed unless cited
  as supplemental.
- Retrieval-First Reasoning: Every response must be backed by retrieved passages from the vector
  database before generation.
- Explainability: The system must be able to surface which document chunks or text selections
  were used to generate an answer.
- Academic & Technical Clarity: Responses must be clear, concise, and suitable for a computer
  science and robotics audience.
- AI-Native Design: The system should be architected around agentic workflows, tool use, and
  retrieval pipelines rather than monolithic request-response logic.
- Security & Isolation: User-selected text queries must be sandboxed and must not leak or mix
  context with global embeddings unless explicitly allowed.

Key Standards:
- Architecture:
  - Backend API implemented using FastAPI/LangGraph
  - Agent orchestration using LangGraph or ChatKit
  - Vector storage using Qdrant (Cloud Free Tier)
  - Metadata and session storage using Neon PostgreSQL
- Retrieval:
  - Chunking strategy must preserve semantic and section-level coherence
  - Each chunk must include source metadata (chapter, section, URL anchor)
- Generation:
  - Answers must cite retrieved chunks
  - If relevant context is missing, the chatbot must explicitly say "Information not found in the book"
- Selected Text Mode:
  - When the user selects text, retrieval must be limited strictly to that text scope
  - Global embeddings must not be queried in this mode
- API Design:
  - Stateless inference endpoints
  - Deterministic retrieval parameters for reproducibility

Constraints:
- Deployment:
  - Backend must be deployable independently from the Docusaurus frontend
  - Frontend integration must be embeddable inside the book UI
- Cost:
  - Must operate fully within free tiers where specified (Qdrant Cloud, Neon)
- Documentation:
  - All architectural decisions must be documented with rationale and tradeoffs
- Ethics & Safety:
  - No training on user data
  - No storage of personally identifiable information (PII)

Quality & Validation Requirements:
- Every chatbot answer must be traceable to retrieved source chunks
- Retrieval accuracy must be verifiable via logs or debug mode
- No hallucinated responses allowed
- System must gracefully handle empty or irrelevant queries
- Code must be modular, testable, and spec-compliant

Success Criteria:
- Chatbot correctly answers questions about the book content
- Chatbot correctly answers questions using only user-selected text
- Zero hallucinations observed during evaluation
- Clear separation of retrieval, reasoning, and generation layers
- Architecture aligns with AI-native, agent-based best practices

## Response snapshot

Analyzing the RAG Chatbot constitutional request and integrating it into the project constitution.

Key actions:
1. Created PHR for constitutional definition (ID: 002)
2. Updating main constitution.md to add RAG Chatbot principles as Section VIII
3. Maintaining separation between textbook content principles and chatbot system principles
4. Ensuring alignment with existing AI-native development standards

The constitution will now include:
- Core textbook principles (I-VII): unchanged
- New Section VIII: RAG Chatbot System Principles
- Updated content requirements to include chatbot integration
- New technical standards for RAG architecture
- Expanded success criteria for chatbot functionality

## Outcome

- ✅ Impact: Established constitutional foundation for RAG Chatbot feature development
- 🧪 Tests: Constitution validation (structure, completeness, non-contradiction)
- 📁 Files: constitution.md updated with Section VIII
- 🔁 Next prompts: /sp.specify for RAG Chatbot feature spec, /sp.plan for architecture design
- 🧠 Reflection: Clear separation maintained between textbook content standards and chatbot system standards; both are now constitutionally governed

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute /sp.specify to create detailed RAG Chatbot feature specification
