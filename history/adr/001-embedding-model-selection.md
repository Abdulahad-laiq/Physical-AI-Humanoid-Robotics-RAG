# ADR-001: Embedding Model Selection for RAG Retrieval

> **Scope**: Document decision cluster for text embedding strategy, including model choice, dimensionality, and deployment approach.

- **Status:** Accepted
- **Date:** 2025-12-25
- **Feature:** rag-chatbot
- **Context:** The RAG chatbot requires converting textbook content and user queries into vector embeddings for semantic retrieval. The choice of embedding model affects retrieval quality, cost, performance (latency), and free-tier viability. The system must operate within Qdrant Cloud Free Tier limits (1GB storage, 1M vectors) and provide real-time query embedding (<200ms).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects cost model, retrieval quality, storage constraints, and system performance for the lifetime of the product
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - OpenAI embeddings, all-MiniLM-L6-v2, all-mpnet-base-v2
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts ingestion pipeline, retrieval service, storage sizing, query latency
-->

## Decision

**Use Sentence-Transformers all-MiniLM-L6-v2 for all text embeddings** (textbook content and user queries).

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Deployment**: Local inference (self-hosted, no API calls)
- **Hardware**: CPU-based (no GPU required for inference)
- **Library**: HuggingFace Transformers + Sentence-Transformers Python library
- **Use Cases**:
  - Textbook content chunking and embedding (one-time ingestion)
  - Real-time user query embedding (per-request)
  - Selected-text mode embedding (ephemeral, per-request)

## Consequences

### Positive

- **Zero API Costs**: Self-hosted model eliminates per-request embedding costs (critical for free-tier operation)
- **Fast Inference**: ~150ms for 512 tokens on CPU; <100ms on GPU (meets <200ms latency requirement)
- **Low Dimensionality**: 384 dimensions → smaller storage footprint in Qdrant (1M vectors × 384 × 4 bytes ≈ 1.5GB including metadata; fits comfortably in 1GB free tier with ~200-300k chunks)
- **Good Quality**: Sufficient semantic accuracy for academic/technical content, especially when combined with section-aware chunking
- **No External Dependencies**: No reliance on third-party embedding APIs (OpenAI, Cohere); reduces failure modes and latency variance
- **Easy Swapping**: Model is a configuration change; can upgrade to larger model (all-mpnet-base-v2) or switch to API-based embeddings (OpenAI) by re-ingesting content

### Negative

- **Lower Quality than OpenAI**: Semantic accuracy lower than OpenAI text-embedding-3-small (384d vs 1536d; weaker on nuanced queries)
- **CPU Inference Required**: Backend must have CPU capacity for real-time embedding (adds ~150ms per query)
- **Re-ingestion Cost**: Changing embedding models requires re-chunking and re-embedding all textbook content (one-time effort, ~1-2 hours for 8-12 chapters)
- **Limited Fine-tuning**: Pre-trained on general text; not optimized for robotics/AI domain-specific terminology (acceptable tradeoff given section-aware chunking provides domain context)

## Alternatives Considered

### Alternative A: OpenAI text-embedding-3-small

**Configuration**:
- Model: `text-embedding-3-small`
- Dimensions: 1536 (or configurable down to 512)
- Deployment: API-based (pay per token)
- Cost: ~$0.02 per 1M tokens

**Why Rejected**:
- **Breaks Free-Tier Constraint**: API costs incompatible with $0/month budget (even at low volume, 1000 queries/day × 100 tokens/query × 30 days ≈ 3M tokens/month ≈ $0.06/month, plus ingestion costs)
- **External Dependency**: Adds failure mode (OpenAI API downtime) and latency variance (network calls)
- **Overkill for Use Case**: Higher dimensionality (1536d) provides marginal retrieval improvement for academic content but consumes 4× storage (exceeds Qdrant free tier)

**When to Revisit**: If free-tier constraints are lifted, or if retrieval quality testing shows <85% accuracy with all-MiniLM-L6-v2

---

### Alternative B: Sentence-Transformers all-mpnet-base-v2

**Configuration**:
- Model: `sentence-transformers/all-mpnet-base-v2`
- Dimensions: 768
- Deployment: Local inference (self-hosted)
- Performance: ~300-400ms for 512 tokens on CPU

**Why Rejected**:
- **Slower Inference**: 2-3× slower than all-MiniLM-L6-v2 (300-400ms vs 150ms); risks exceeding 3-second p95 latency budget
- **Higher Storage**: 768 dimensions = 2× storage vs all-MiniLM-L6-v2; reduces max chunks from 300k to 150k (may require chunking optimization)
- **Marginal Quality Gain**: Retrieval accuracy improvement (~5-10% on benchmarks) not worth latency and storage tradeoffs for MVP

**When to Revisit**: If retrieval quality testing shows <85% accuracy with all-MiniLM-L6-v2, and latency/storage budgets can be increased

---

### Alternative C: Custom Fine-tuned Model

**Configuration**:
- Base: all-MiniLM-L6-v2 or similar
- Fine-tuning: Train on robotics/AI textbook corpus
- Deployment: Local inference

**Why Rejected**:
- **Out of Scope**: Fine-tuning requires labeled dataset (question-chunk pairs), training infrastructure, and evaluation framework (not in MVP scope per spec.md)
- **Complexity**: Adds training pipeline, versioning, and model registry (violates "smallest viable change" constitutional principle)
- **Uncertain ROI**: Pre-trained model + section-aware chunking likely sufficient for textbook QA

**When to Revisit**: If retrieval accuracy testing shows <80% accuracy after optimizing chunking strategy

## References

- Feature Spec: [specs/rag-chatbot/spec.md](../../specs/rag-chatbot/spec.md) (NFR-002: Free tier operation; SC-008: 90% retrieval accuracy)
- Implementation Plan: [specs/rag-chatbot/plan.md](../../specs/rag-chatbot/plan.md#decision-1-embedding-model-selection) (Decision 1, lines 184-207)
- Related ADRs: ADR-002 (Chunking Strategy - works synergistically with embedding choice)
- Model Documentation: [HuggingFace Model Card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- Evaluator Evidence: To be added after Phase 0 research (benchmark results)

---

**Approval**: Accepted on 2025-12-25
**Reviewers**: N/A (initial planning phase)
**Supersedes**: None
**Superseded By**: None
