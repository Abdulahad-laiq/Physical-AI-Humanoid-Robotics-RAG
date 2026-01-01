# ADR-002: Hybrid Section-Aware Chunking Strategy

> **Scope**: Document decision cluster for textbook content chunking approach, including segmentation logic, size constraints, and metadata schema.

- **Status:** Accepted
- **Date:** 2025-12-25
- **Feature:** rag-chatbot
- **Context:** The RAG chatbot must chunk the Docusaurus textbook content into semantically coherent segments for vector embedding and retrieval. Chunking strategy directly impacts retrieval accuracy (semantic relevance), citation quality (source traceability), and user experience (answer precision). The constitution requires "chunking strategy must preserve semantic and section-level coherence" while maintaining retrieval effectiveness.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects retrieval accuracy, user experience, and answer quality for the lifetime of the product; difficult to change without full re-ingestion
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Fixed-size chunking, pure section-based chunking, hybrid approach
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts ingestion pipeline, retrieval logic, citation generation, and answer quality
-->

## Decision

**Use Hybrid Section-Aware Chunking with 512 Token Maximum**

- **Primary Strategy**: Respect Markdown section boundaries (##, ###, ####) as natural chunk boundaries
- **Size Constraint**: Max 512 tokens per chunk (hard limit)
- **Overflow Handling**: If section exceeds 512 tokens, split at sentence boundaries using spaCy or NLTK
- **Metadata Schema**: Each chunk includes:
  - `chunk_id`: Unique identifier (e.g., `ch3-s3.2-001`)
  - `chapter`: Chapter number (integer)
  - `section`: Section identifier (e.g., "3.2")
  - `subsection`: Subsection identifier (e.g., "3.2.1", optional)
  - `url_anchor`: Docusaurus URL fragment (e.g., `#inverse-kinematics`)
  - `token_count`: Actual tokens in chunk
  - `chunk_index`: Position within section (for multi-chunk sections)
- **Special Cases**:
  - **Code blocks**: Preserve as single chunk if <512 tokens; split by function/class if larger
  - **Equations**: Keep with surrounding explanatory text
  - **Lists**: Keep entire list together if <512 tokens; split at list item boundaries if larger

## Consequences

### Positive

- **Semantic Coherence**: Preserves natural topic boundaries from textbook structure (sections correspond to coherent concepts)
- **Accurate Citations**: Citations directly map to textbook sections (e.g., "Chapter 3, Section 3.2"), making answers verifiable
- **Flexible Size**: Handles both short sections (200 tokens) and long sections (1500+ tokens) gracefully
- **Constitutional Compliance**: Aligns with requirement to "preserve semantic and section-level coherence"
- **Better Context**: Retrieved chunks include full context of a concept (not truncated mid-sentence or mid-paragraph)
- **Easy Re-ingestion**: Changing chunk size (e.g., 512 → 768 tokens) only requires re-running ingestion script; metadata schema is unchanged

### Negative

- **Variable Chunk Sizes**: Creates chunks ranging from 50 to 512 tokens (averaging ~300 tokens); may affect retrieval consistency (very short chunks have less context, very long chunks may dilute signal)
- **Sentence Splitting Complexity**: Requires NLP library (spaCy or NLTK) for sentence boundary detection; adds dependency and potential errors (e.g., splitting on abbreviations like "Dr.")
- **Large Section Handling**: Sections >512 tokens are split into multiple chunks, potentially breaking conceptual unity (e.g., a 1000-token derivation split into 2 chunks may lose coherence)
- **Overlap Consideration**: No overlap between chunks (simplicity); may miss queries that span chunk boundaries (acceptable tradeoff for MVP; can add 50-token overlap in future iterations)

## Alternatives Considered

### Alternative A: Fixed-Size Chunking (512 Tokens, No Section Awareness)

**Configuration**:
- Fixed 512 tokens per chunk
- Sliding window with 50-token overlap (optional)
- No respect for Markdown section boundaries

**Why Rejected**:
- **Breaks Semantic Coherence**: May split sentences, paragraphs, or concepts mid-thought (e.g., equation explanation split from the equation itself)
- **Poor Citations**: Citations reference arbitrary character ranges rather than meaningful sections (e.g., "Chapter 3, Characters 1500-2500" instead of "Section 3.2")
- **Constitutional Violation**: Does not "preserve semantic and section-level coherence" as required

**When to Revisit**: If retrieval testing shows section-aware chunking creates too many very short chunks (<100 tokens), consider fixed-size as fallback

---

### Alternative B: Pure Section-Based Chunking (Variable Size, No Limit)

**Configuration**:
- One chunk per section (##, ###, ####)
- No size limit (chunks may be 50-5000+ tokens)
- Perfect alignment with textbook structure

**Why Rejected**:
- **Excessively Large Chunks**: Some textbook sections are 2000-5000 tokens (e.g., long derivations, case studies); large chunks dilute retrieval accuracy (too much irrelevant context mixed with relevant content)
- **Inefficient Retrieval**: Retrieving a 3000-token chunk when only 200 tokens are relevant wastes context window and confuses the agent
- **Poor Scalability**: all-MiniLM-L6-v2 has max sequence length of 512 tokens; chunks >512 tokens would be truncated during embedding (losing information)

**When to Revisit**: If embedding model is upgraded to support longer sequences (e.g., Longformer-based embeddings with 4096 token max), AND retrieval testing shows large chunks improve accuracy

---

### Alternative C: Sentence-Based Chunking (Natural Sentence Boundaries)

**Configuration**:
- Chunk by sentences, targeting ~300-500 tokens per chunk
- Respect sentence boundaries only (not sections)
- Use spaCy for sentence segmentation

**Why Rejected**:
- **No Section Awareness**: Loses alignment with textbook structure; citations become less meaningful ("Chapter 3, Sentences 45-52" instead of "Section 3.2")
- **Fragmentation**: Conceptually related sentences (e.g., definition + example) may be split into separate chunks if they happen to cross chunk boundary
- **Constitutional Violation**: Does not preserve "section-level coherence"

**When to Revisit**: Not recommended; hybrid approach provides sentence-level granularity within sections

## Implementation Details

### Chunking Algorithm

```python
def chunk_section(section_text: str, section_metadata: dict) -> List[Chunk]:
    """
    Chunk a single Markdown section using hybrid strategy.

    Args:
        section_text: Full text of the section (including subsections)
        section_metadata: {chapter, section, url_anchor}

    Returns:
        List of Chunk objects with text and metadata
    """
    MAX_TOKENS = 512
    chunks = []

    # Tokenize section
    tokens = tokenizer.encode(section_text)

    if len(tokens) <= MAX_TOKENS:
        # Section fits in one chunk - preserve as-is
        chunks.append(Chunk(
            text=section_text,
            tokens=tokens,
            metadata={**section_metadata, "chunk_index": 0}
        ))
    else:
        # Section exceeds limit - split at sentence boundaries
        sentences = nlp(section_text).sents  # spaCy sentence segmentation
        current_chunk = []
        current_tokens = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_tokens = tokenizer.encode(sentence.text)

            if current_tokens + len(sentence_tokens) <= MAX_TOKENS:
                current_chunk.append(sentence.text)
                current_tokens += len(sentence_tokens)
            else:
                # Save current chunk
                chunks.append(Chunk(
                    text=" ".join(current_chunk),
                    tokens=current_tokens,
                    metadata={**section_metadata, "chunk_index": chunk_index}
                ))

                # Start new chunk
                current_chunk = [sentence.text]
                current_tokens = len(sentence_tokens)
                chunk_index += 1

        # Save final chunk
        if current_chunk:
            chunks.append(Chunk(
                text=" ".join(current_chunk),
                tokens=current_tokens,
                metadata={**section_metadata, "chunk_index": chunk_index}
            ))

    return chunks
```

### Metadata Schema (Qdrant Payload)

```json
{
  "chunk_id": "ch3-s3.2-001",
  "chapter": 3,
  "section": "3.2",
  "subsection": null,
  "url_anchor": "#inverse-kinematics",
  "token_count": 487,
  "chunk_index": 0,
  "source_file": "docs/chapter-03-kinematics.md"
}
```

## References

- Feature Spec: [specs/rag-chatbot/spec.md](../../specs/rag-chatbot/spec.md) (FR-007: Section-aware chunking; SC-008: 90% retrieval accuracy)
- Implementation Plan: [specs/rag-chatbot/plan.md](../../specs/rag-chatbot/plan.md#decision-2-chunking-strategy) (Decision 2, lines 210-239)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Section VIII: Retrieval-First Reasoning principle)
- Related ADRs:
  - ADR-001 (Embedding Model Selection - 512 token max aligns with all-MiniLM-L6-v2 sequence limit)
  - ADR-003 (Agent Framework Selection - chunking affects context provided to agent)
- Evaluator Evidence: To be added after Phase 0 research (chunking quality evaluation on sample chapters)

---

**Approval**: Accepted on 2025-12-25
**Reviewers**: N/A (initial planning phase)
**Supersedes**: None
**Superseded By**: None
