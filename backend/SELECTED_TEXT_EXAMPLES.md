# Selected-Text Mode Examples

Complete examples for testing the selected-text query endpoint.

## Overview

Selected-text mode allows users to highlight specific text and ask questions about it. The system creates an **ephemeral in-memory vector store** from the selected text only, ensuring complete isolation from the global database.

**Key Features:**
- ✅ Complete isolation - no global database access
- ✅ Ephemeral vector store (exists only for single query)
- ✅ Automatic chunking for long selections
- ✅ Context-specific answers

---

## Endpoint

```
POST /api/v1/chat/selected
```

---

## Request Format

```json
{
  "query": "User's question about the selected text",
  "selected_text": "Text highlighted by the user...",
  "session_id": "optional-session-id",
  "debug": false
}
```

**Field Limits:**
- `query`: 1-1000 characters
- `selected_text`: 10-5000 characters
- `session_id`: Optional, alphanumeric
- `debug`: Boolean, default false

---

## Example 1: Simple Question About Equation

### Request

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does the Jacobian matrix do?",
    "selected_text": "The Jacobian matrix J relates joint velocities to end-effector velocities: v = J(q) * q_dot, where v is the end-effector velocity and q_dot is the joint velocity vector. The inverse Jacobian can be used to compute joint velocities needed to achieve a desired end-effector velocity."
  }'
```

### Expected Response

```json
{
  "answer": "The Jacobian matrix J relates joint velocities (q_dot) to end-effector velocities (v) through the equation v = J(q) * q_dot. The inverse Jacobian can compute the joint velocities needed to achieve a desired end-effector velocity.",
  "citations": [
    {
      "chunk_id": "selected-000",
      "chapter": 0,
      "section": "selected",
      "url_anchor": "",
      "relevance_score": 0.95,
      "text_preview": "The Jacobian matrix J relates joint velocities to end-effector velocities...",
      "source": "Selected Text"
    }
  ],
  "query_id": "uuid",
  "generation_time_ms": 567
}
```

---

## Example 2: Clarify Complex Paragraph

### Request

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this in simpler terms",
    "selected_text": "Inverse kinematics (IK) is the process of determining joint angles that achieve a desired end-effector position and orientation. Unlike forward kinematics, which has a unique solution, inverse kinematics may have multiple solutions, no solution, or an infinite number of solutions depending on the robot'\''s configuration and the target pose."
  }'
```

### Expected Response

```json
{
  "answer": "Inverse kinematics is about figuring out what angles the robot joints need to be at to put the robot's hand (end-effector) in a specific position. While forward kinematics always gives one answer, inverse kinematics can give multiple answers, no answer, or infinite answers depending on the robot's design and where you want it to reach.",
  "citations": [...],
  "query_id": "uuid",
  "generation_time_ms": 623
}
```

---

## Example 3: Long Selected Text (Auto-Chunking)

When selected text exceeds 512 tokens, it's automatically chunked:

### Request

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d @long_selection.json
```

**long_selection.json:**
```json
{
  "query": "Summarize the main points",
  "selected_text": "... very long text (e.g., 2000 characters) ...",
  "debug": true
}
```

### Expected Response (with debug)

```json
{
  "answer": "The main points are: ...",
  "citations": [...],
  "query_id": "uuid",
  "generation_time_ms": 1234,
  "debug_metadata": {
    "mode": "selected-text",
    "selected_text_length": 2000,
    "chunks_created": 4,
    "isolation": "ephemeral_store_only",
    "global_db_accessed": false
  }
}
```

---

## Example 4: With Session Tracking

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this about?",
    "selected_text": "Forward kinematics computes the end-effector position from joint angles using the Denavit-Hartenberg convention.",
    "session_id": "user-session-789"
  }'
```

Session ID will be hashed and stored for analytics (privacy-preserving).

---

## Example 5: Error - Text Too Short

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this?",
    "selected_text": "Too short"
  }'
```

### Expected Response (400 Error)

```json
{
  "detail": "Selected text must be at least 10 characters"
}
```

---

## Example 6: Error - Text Too Long

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Summarize this",
    "selected_text": "... text over 5000 characters ..."
  }'
```

### Expected Response (400 Error)

```json
{
  "detail": "Selected text must not exceed 5000 characters"
}
```

---

## Example 7: Python Test Script

```python
import httpx
import asyncio

async def test_selected_text():
    url = "http://localhost:8000/api/v1/chat/selected"

    payload = {
        "query": "Explain the DH convention",
        "selected_text": """
        The Denavit-Hartenberg (DH) convention uses four parameters
        to describe each link: a (link length), α (link twist),
        d (link offset), and θ (joint angle). These parameters
        allow systematic computation of forward kinematics.
        """,
        "debug": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data['answer']}")
            print(f"Citations: {len(data['citations'])}")
            print(f"Time: {data['generation_time_ms']}ms")

            if data.get('debug_metadata'):
                print(f"Chunks created: {data['debug_metadata']['chunks_created']}")
                print(f"Isolation: {data['debug_metadata']['isolation']}")
        else:
            print(f"Error {response.status_code}: {response.text}")

asyncio.run(test_selected_text())
```

---

## Example 8: Health Check

```bash
curl http://localhost:8000/api/v1/chat/selected/health
```

### Expected Response

```json
{
  "status": "healthy",
  "components": {
    "embedding_service": "healthy",
    "agent": "healthy"
  },
  "isolation": "ephemeral_store_only",
  "global_db_access": false
}
```

---

## Example 9: Info Endpoint

```bash
curl http://localhost:8000/api/v1/chat/selected/info
```

### Expected Response

```json
{
  "mode": "selected-text",
  "description": "Answer questions about user-highlighted text",
  "isolation": {
    "type": "ephemeral_in_memory_store",
    "global_db_accessed": false,
    "explanation": "Creates temporary vector store from selected text only"
  },
  "limits": {
    "min_text_length": 10,
    "max_text_length": 5000,
    "max_chunks": "dynamic (based on text length)",
    "chunking_strategy": "sentence-aware, 512 token max"
  },
  "security": {
    "pii_handling": "Selected text not stored in database",
    "session_tracking": "Session ID hashed (SHA-256) for privacy",
    "isolation_guarantee": "No global embeddings accessed"
  },
  "use_cases": [
    "Explain specific equations or code snippets",
    "Clarify complex paragraphs",
    "Answer questions about selected sections",
    "Deep dive into specific topics"
  ]
}
```

---

## Testing Isolation

To verify isolation (no global database leakage):

### Test 1: Query About Global Content

```bash
# Select text about inverse kinematics
# Ask about DIFFERENT topic (forward kinematics)
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is forward kinematics?",
    "selected_text": "Inverse kinematics (IK) determines joint angles from end-effector pose. It may have multiple solutions."
  }'
```

**Expected:** "Information not found in the selected text." (even if forward kinematics is in global DB)

### Test 2: Check Citations

All citations should have:
- `chunk_id` starting with "selected-"
- `section` = "selected"
- `chapter` = 0

No citations from global database (ch1-*, ch2-*, etc.) should appear.

---

## Use Cases

### 1. Equation Explanation
User highlights: `E = mc²`
Query: "What does each variable represent?"

### 2. Code Snippet Analysis
User highlights code block
Query: "Explain what this code does line by line"

### 3. Dense Paragraph Simplification
User highlights complex paragraph
Query: "Explain this in simpler terms"

### 4. Definition Lookup
User highlights technical term
Query: "Define this term"

### 5. Comparison
User highlights two concepts
Query: "What's the difference between these two?"

---

## Performance Expectations

- **Embedding generation:** < 200ms (depends on text length)
- **Total response time:** < 3 seconds for typical selections
- **Max concurrent requests:** 100/minute per IP (rate limited)

---

## Security & Privacy

1. **Isolation Guarantee:**
   - No global Qdrant database access
   - Ephemeral vector store created per request
   - Store destroyed after response

2. **Privacy:**
   - Selected text NOT stored in database
   - Only query text and metadata logged
   - Session IDs hashed (SHA-256)

3. **Validation:**
   - XSS detection on query and selected text
   - SQL injection prevention
   - HTML entity escaping

---

## Debugging

Enable debug mode to see internal processing:

```bash
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this",
    "selected_text": "...",
    "debug": true
  }'
```

Debug metadata includes:
- `selected_text_length`: Original text length
- `chunks_created`: Number of chunks generated
- `isolation`: "ephemeral_store_only"
- `global_db_accessed`: false

---

## Comparison: Global vs Selected-Text Mode

| Feature | Global Mode | Selected-Text Mode |
|---------|-------------|-------------------|
| **Endpoint** | `/api/v1/chat` | `/api/v1/chat/selected` |
| **Data Source** | Qdrant database | Ephemeral in-memory store |
| **Context** | Entire textbook | User-selected text only |
| **Isolation** | Shared database | Complete isolation |
| **Use Case** | General questions | Context-specific questions |
| **Citations** | Chapter/Section refs | Selected text chunks |

---

## Next Steps

After testing selected-text mode:

1. **Verify isolation** - Check no global DB citations appear
2. **Test edge cases** - Very short, very long, special characters
3. **Performance test** - Measure response times
4. **Frontend integration** - Build text selection UI
