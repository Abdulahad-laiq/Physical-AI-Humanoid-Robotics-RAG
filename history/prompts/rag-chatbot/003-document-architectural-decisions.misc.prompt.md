---
id: 003
title: Document Architectural Decisions for RAG Chatbot
stage: misc
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot
branch: main
user: binary
command: /sp.adr
labels: ["adr", "architecture", "decisions", "embedding", "chunking", "agent"]
links:
  spec: specs/rag-chatbot/spec.md
  ticket: null
  adr: history/adr/001-embedding-model-selection.md, history/adr/002-chunking-strategy.md, history/adr/003-agent-framework-selection.md
  pr: null
files:
  - history/adr/001-embedding-model-selection.md
  - history/adr/002-chunking-strategy.md
  - history/adr/003-agent-framework-selection.md
  - history/prompts/rag-chatbot/003-document-architectural-decisions.misc.prompt.md
tests:
  - ADR significance test (Impact + Alternatives + Scope): PASS (3/3 ADRs)
  - Constitutional alignment: PASS (all decisions support Section VIII principles)
  - Completeness check: PASS (all placeholders filled, references linked)
---

## Prompt

/sp.adr embedding-model-selection

User request: "ADR first"

Context: After creating the comprehensive architectural plan (plan.md), the user requested to document the architecturally significant decisions as ADRs before proceeding to task generation. The plan identified three key decisions requiring ADR documentation:
1. Embedding Model Selection
2. Chunking Strategy
3. Agent Framework Selection

## Response snapshot

Executed ADR workflow to document the three architecturally significant decisions from the plan.

**Step 1: Load Planning Context**
- Feature directory: `specs/rag-chatbot/`
- Available artifacts: `plan.md`, `spec.md`
- ADR directory: Created `history/adr/` (did not exist)

**Step 2: Extract Architectural Decisions**
Identified three decision clusters from plan.md:
1. **Embedding Model Selection** (lines 184-207): Sentence-Transformers all-MiniLM-L6-v2 vs OpenAI vs all-mpnet-base-v2
2. **Chunking Strategy** (lines 210-239): Hybrid section-aware with 512 token max
3. **Agent Framework Selection** (lines 274-313): OpenAI SDK + AsyncOpenAI + Gemini-2.0-flash

**Step 3: Check Existing ADRs**
- No existing ADRs found (new feature)
- All three decisions qualified as ADR candidates

**Step 4: Apply Significance Test**
All three decisions passed the significance test:
- ✅ Impact: Long-term consequences (cost, quality, extensibility)
- ✅ Alternatives: Multiple viable options with documented tradeoffs
- ✅ Scope: Cross-cutting concerns affecting multiple components

**Step 5: Create ADRs**
Created three ADRs using the ADR template:

1. **ADR-001: Embedding Model Selection for RAG Retrieval**
   - Decision: Sentence-Transformers all-MiniLM-L6-v2 (384 dimensions, local inference)
   - Rationale: Zero API costs, fast inference (~150ms), fits free-tier constraints
   - Alternatives: OpenAI text-embedding-3-small (rejected: breaks free tier), all-mpnet-base-v2 (rejected: slower, higher storage)
   - Consequences: +Zero cost, +Fast, +Low storage | -Lower quality than OpenAI, -CPU required, -Re-ingestion cost for model changes

2. **ADR-002: Hybrid Section-Aware Chunking Strategy**
   - Decision: Respect Markdown section boundaries (##, ###) with 512 token max; split at sentences if exceeded
   - Rationale: Preserves semantic coherence, accurate citations, constitutional compliance
   - Alternatives: Fixed-size chunking (rejected: breaks coherence), pure section-based (rejected: too large), sentence-based (rejected: no section awareness)
   - Consequences: +Semantic coherence, +Accurate citations, +Flexible | -Variable sizes, -Sentence splitting complexity, -Large section handling

3. **ADR-003: Agent Framework and LLM Integration Stack**
   - Decision: OpenAI Assistants SDK with AsyncOpenAI + Gemini-2.0-flash
   - Rationale: Simple, mature, Gemini-compatible, sync/async support, minimal dependencies
   - Alternatives: LangGraph (rejected: overkill for simple RAG), ChatKit (rejected: less mature), custom loop (rejected: reinvents wheel)
   - Consequences: +Simplicity, +Gemini compatibility, +Mature ecosystem, +Future extensible | -Single-step only, -OpenAI coupling, -AsyncOpenAI overhead

**Step 6: Report Completion**
All ADRs created successfully with full context, alternatives, consequences, and references.

## Outcome

- ✅ Impact: Three architecturally significant decisions documented with full rationale, alternatives, and tradeoffs
- 🧪 Tests:
  - Significance test: 3/3 PASS (Impact + Alternatives + Scope criteria met)
  - Template adherence: PASS (all placeholders filled, structured correctly)
  - Constitutional alignment: PASS (decisions support Section VIII principles)
  - References: PASS (all ADRs link back to spec.md and plan.md)
- 📁 Files: 3 ADRs created in `history/adr/` directory
- 🔁 Next prompts: /sp.tasks (generate dependency-ordered implementation tasks)
- 🧠 Reflection: ADRs capture critical long-term decisions before implementation begins; clustered decisions appropriately (not over-granular); alternatives documented with clear rejection rationale; consequences include both positive and negative outcomes

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL):
  - Over-granular ADR check: PASS (decisions clustered appropriately: embedding strategy, chunking strategy, agent stack)
  - Missing alternatives check: PASS (each ADR documents 2-3 alternatives with rationale)
  - Completeness check: PASS (all sections filled: context, decision, consequences, alternatives, references)
  - Conciseness vs. detail balance: PASS (ADRs detailed enough for future reference but not verbose)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute /sp.tasks to generate implementation tasks based on plan and ADRs
