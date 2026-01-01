"""
Hybrid section-aware text chunking service.

Implements intelligent chunking that respects Markdown section boundaries
while enforcing a maximum token limit. Uses spaCy for sentence-level splitting
when sections exceed the token limit.
"""

import re
import uuid
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import spacy
from transformers import AutoTokenizer
import logging

logger = logging.getLogger(__name__)

# Load spaCy model for sentence splitting
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# Load tokenizer for token counting (matches all-MiniLM-L6-v2)
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


# ============================================================================
# Configuration
# ============================================================================

MAX_CHUNK_TOKENS = 512
MIN_CHUNK_TOKENS = 50  # Avoid overly small chunks
OVERLAP_TOKENS = 50  # Token overlap between consecutive chunks for context


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class ChunkMetadata:
    """
    Metadata for a text chunk.

    Attributes:
        chunk_id: Unique identifier (format: ch{chapter}-s{section}-{index})
        text: The chunk text content
        chapter: Chapter number
        section: Section identifier (e.g., "3.2")
        subsection: Optional subsection identifier (e.g., "3.2.1")
        url_anchor: URL fragment for citation linking
        token_count: Number of tokens in the chunk
        chunk_index: Sequential index within the section (0-based)
        source_file: Original source file path
    """
    chunk_id: str
    text: str
    chapter: int
    section: str
    subsection: Optional[str]
    url_anchor: str
    token_count: int
    chunk_index: int
    source_file: str


@dataclass
class Section:
    """
    Represents a section extracted from a Markdown document.

    Attributes:
        title: Section title (from Markdown header)
        level: Header level (1-6)
        content: Section text content
        chapter: Chapter number
        section_id: Section identifier (e.g., "3.2")
        subsection_id: Optional subsection identifier (e.g., "3.2.1")
        url_anchor: URL anchor generated from title
    """
    title: str
    level: int
    content: str
    chapter: int
    section_id: str
    subsection_id: Optional[str]
    url_anchor: str


# ============================================================================
# Utility Functions
# ============================================================================

def count_tokens(text: str) -> int:
    """
    Count tokens in text using the embedding model's tokenizer.

    Args:
        text: Input text

    Returns:
        int: Number of tokens
    """
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)


def create_url_anchor(title: str) -> str:
    """
    Generate URL anchor from section title.

    Converts title to lowercase, replaces spaces with hyphens,
    removes special characters.

    Args:
        title: Section title

    Returns:
        str: URL anchor (e.g., "inverse-kinematics")
    """
    # Convert to lowercase and replace spaces with hyphens
    anchor = title.lower().strip()
    anchor = re.sub(r'[^\w\s-]', '', anchor)  # Remove special chars
    anchor = re.sub(r'[\s_]+', '-', anchor)  # Replace spaces/underscores with hyphens
    anchor = re.sub(r'-+', '-', anchor)  # Collapse multiple hyphens
    return anchor.strip('-')


def extract_chapter_number(file_path: str) -> int:
    """
    Extract chapter number from file path.

    Supports patterns like:
    - chapter-3.md, chapter3.md, ch3-basics.md
    - 03-kinematics.md (leading digits)
    - intro.md, preface.md, glossary.md, index.md (returns 0)

    Args:
        file_path: Path to chapter file

    Returns:
        int: Chapter number (0 for intro/preface/appendix)

    Raises:
        ValueError: If chapter number cannot be extracted
    """
    # Try pattern: chapter-N.md or chN.md
    match = re.search(r'ch(?:apter)?-?(\d+)', file_path, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try pattern: NN-title.md (leading digits)
    match = re.search(r'(\d+)-', file_path)
    if match:
        return int(match.group(1))

    # Handle intro, preface, appendix, glossary, bibliography files (return 0)
    if re.search(r'intro|preface|appendix|foreword|prologue|glossary|index|references|bibliography', file_path, re.IGNORECASE):
        return 0

    raise ValueError(f"Cannot extract chapter number from file path: {file_path}")


# ============================================================================
# Section Parsing
# ============================================================================

def parse_markdown_sections(markdown_text: str, chapter: int, source_file: str) -> List[Section]:
    """
    Parse Markdown text into sections based on headers.

    Extracts sections delimited by Markdown headers (# through ######),
    generating metadata for each section.

    Args:
        markdown_text: Markdown document text
        chapter: Chapter number
        source_file: Source file path

    Returns:
        List[Section]: Parsed sections with metadata
    """
    sections = []
    lines = markdown_text.split('\n')

    current_section = None
    current_content = []
    section_counters = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    for line in lines:
        # Check if line is a Markdown header
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if header_match:
            # Save previous section if exists
            if current_section:
                current_section.content = '\n'.join(current_content).strip()
                if current_section.content:  # Only add non-empty sections
                    sections.append(current_section)

            # Parse new section header
            level = len(header_match.group(1))
            title = header_match.group(2).strip()

            # Update section counters
            section_counters[level] += 1
            # Reset counters for deeper levels
            for deeper_level in range(level + 1, 7):
                section_counters[deeper_level] = 0

            # Generate section ID (e.g., "3.2" for level 2 in chapter 3)
            if level == 1:
                section_id = str(chapter)
                subsection_id = None
            elif level == 2:
                section_id = f"{chapter}.{section_counters[2]}"
                subsection_id = None
            else:
                # For level 3+, create subsection ID
                section_id = f"{chapter}.{section_counters[2]}"
                subsection_parts = [str(section_counters[i]) for i in range(2, level + 1)]
                subsection_id = f"{chapter}.{'.'.join(subsection_parts)}"

            # Create new section
            current_section = Section(
                title=title,
                level=level,
                content="",
                chapter=chapter,
                section_id=section_id,
                subsection_id=subsection_id,
                url_anchor=create_url_anchor(title)
            )
            current_content = []
        else:
            # Add line to current section content
            if current_section:
                current_content.append(line)

    # Add final section
    if current_section:
        current_section.content = '\n'.join(current_content).strip()
        if current_section.content:
            sections.append(current_section)

    logger.info(f"Parsed {len(sections)} sections from {source_file}")
    return sections


# ============================================================================
# Chunking Logic
# ============================================================================

def split_text_by_sentences(text: str, max_tokens: int = MAX_CHUNK_TOKENS) -> List[str]:
    """
    Split text into chunks at sentence boundaries using spaCy.

    Args:
        text: Input text to split
        max_tokens: Maximum tokens per chunk

    Returns:
        List[str]: List of text chunks
    """
    if nlp is None:
        # Fallback: simple splitting by periods if spaCy unavailable
        logger.warning("spaCy not available, using simple sentence splitting")
        sentences = re.split(r'(?<=[.!?])\s+', text)
    else:
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)

        # If single sentence exceeds max, split it forcefully
        if sentence_tokens > max_tokens:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_tokens = 0

            # Split long sentence by words
            words = sentence.split()
            temp_chunk = []
            temp_tokens = 0

            for word in words:
                word_tokens = count_tokens(word)
                if temp_tokens + word_tokens > max_tokens:
                    if temp_chunk:
                        chunks.append(' '.join(temp_chunk))
                    temp_chunk = [word]
                    temp_tokens = word_tokens
                else:
                    temp_chunk.append(word)
                    temp_tokens += word_tokens

            if temp_chunk:
                chunks.append(' '.join(temp_chunk))

        # Check if adding sentence would exceed limit
        elif current_tokens + sentence_tokens > max_tokens:
            # Save current chunk and start new one
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_tokens = sentence_tokens
        else:
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    # Add final chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def chunk_section(section: Section, source_file: str) -> List[ChunkMetadata]:
    """
    Chunk a section into smaller pieces if needed.

    If section fits within MAX_CHUNK_TOKENS, return as single chunk.
    Otherwise, split at sentence boundaries.

    Args:
        section: Section to chunk
        source_file: Original source file path

    Returns:
        List[ChunkMetadata]: List of chunks with metadata
    """
    section_tokens = count_tokens(section.content)

    # If section fits in one chunk, keep it intact
    if section_tokens <= MAX_CHUNK_TOKENS:
        chunk_id = str(uuid.uuid4())
        return [ChunkMetadata(
            chunk_id=chunk_id,
            text=section.content,
            chapter=section.chapter,
            section=section.section_id,
            subsection=section.subsection_id,
            url_anchor=section.url_anchor,
            token_count=section_tokens,
            chunk_index=0,
            source_file=source_file
        )]

    # Section too large - split by sentences
    chunk_texts = split_text_by_sentences(section.content, max_tokens=MAX_CHUNK_TOKENS)
    chunks = []

    for idx, chunk_text in enumerate(chunk_texts):
        # Skip overly small chunks (likely artifacts)
        token_count = count_tokens(chunk_text)
        if token_count < MIN_CHUNK_TOKENS and idx > 0:
            # Merge with previous chunk if possible
            if chunks:
                prev_chunk = chunks[-1]
                merged_text = prev_chunk.text + ' ' + chunk_text
                merged_tokens = count_tokens(merged_text)
                if merged_tokens <= MAX_CHUNK_TOKENS:
                    prev_chunk.text = merged_text
                    prev_chunk.token_count = merged_tokens
                    continue

        chunk_id = str(uuid.uuid4())
        chunks.append(ChunkMetadata(
            chunk_id=chunk_id,
            text=chunk_text,
            chapter=section.chapter,
            section=section.section_id,
            subsection=section.subsection_id,
            url_anchor=section.url_anchor,
            token_count=token_count,
            chunk_index=idx,
            source_file=source_file
        ))

    logger.info(f"Section '{section.title}' split into {len(chunks)} chunks")
    return chunks


# ============================================================================
# Main Chunking Pipeline
# ============================================================================

def chunk_textbook_chapter(
    markdown_text: str,
    source_file: str,
    chapter: int = None
) -> List[ChunkMetadata]:
    """
    Chunk a complete textbook chapter into searchable pieces.

    Main entry point for the chunking pipeline. Parses Markdown into sections,
    then chunks each section while respecting token limits.

    Args:
        markdown_text: Markdown chapter content
        source_file: Source file path
        chapter: Chapter number (auto-detected if None)

    Returns:
        List[ChunkMetadata]: All chunks with complete metadata

    Raises:
        ValueError: If chapter number cannot be determined
    """
    # Extract chapter number if not provided
    if chapter is None:
        chapter = extract_chapter_number(source_file)

    # Parse into sections
    sections = parse_markdown_sections(markdown_text, chapter, source_file)

    # Chunk each section
    all_chunks = []
    for section in sections:
        section_chunks = chunk_section(section, source_file)
        all_chunks.extend(section_chunks)

    logger.info(
        f"Chunked chapter {chapter} into {len(all_chunks)} chunks "
        f"from {len(sections)} sections (file: {source_file})"
    )

    return all_chunks


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and testing of chunking service.
    """
    # Example Markdown content
    sample_markdown = """
# Chapter 3: Robot Kinematics

This chapter covers the fundamentals of robot kinematics.

## 3.1 Forward Kinematics

Forward kinematics (FK) is the process of computing the position and orientation
of the robot's end-effector from the joint angles. This is a straightforward
computation using the Denavit-Hartenberg (DH) convention.

The DH convention uses four parameters to describe each link: a, α, d, θ.

## 3.2 Inverse Kinematics

Inverse kinematics (IK) is the process of determining joint angles that achieve
a desired end-effector position. This is more challenging than forward kinematics
because multiple solutions may exist, or no solution may exist if the target is
outside the robot's workspace.

### 3.2.1 Analytical Solutions

Analytical IK solutions exist for robots with specific geometric configurations,
such as those with spherical wrists. These solutions are preferred when available
because they are fast and deterministic.

### 3.2.2 Numerical Solutions

When analytical solutions are not available, numerical methods like the Jacobian
transpose method or gradient descent can be used. These methods are iterative
and may converge to local minima.
"""

    # Chunk the sample
    chunks = chunk_textbook_chapter(
        markdown_text=sample_markdown,
        source_file="chapter-3.md",
        chapter=3
    )

    # Display results
    print(f"\nGenerated {len(chunks)} chunks:\n")
    for chunk in chunks:
        print(f"Chunk ID: {chunk.chunk_id}")
        print(f"  Section: {chunk.section} (subsection: {chunk.subsection})")
        print(f"  Tokens: {chunk.token_count}")
        print(f"  URL Anchor: {chunk.url_anchor}")
        print(f"  Text preview: {chunk.text[:100]}...")
        print()
