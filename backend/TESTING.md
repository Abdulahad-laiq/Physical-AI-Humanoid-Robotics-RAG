# Backend Testing Guide

Complete guide for testing the RAG Chatbot backend (Phase 3).

## Prerequisites

- Python 3.9 or higher installed
- Access to terminal/command prompt
- Credentials configured in `.env` file

## Step 1: Environment Setup

### Create Virtual Environment

```bash
# Navigate to backend directory
cd D:\PIAIC\Quarter4\Physical-AI-Humanoid-Robotics\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Verify .env Configuration

Ensure `backend/.env` file exists with all required credentials:

```bash
# Check if .env exists
# If not, copy from .env.example:
copy .env.example .env  # Windows
# OR
cp .env.example .env    # macOS/Linux
```

Required environment variables:
- `GEMINI_API_KEY` - Your Gemini API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `QDRANT_COLLECTION_NAME` - Collection name (default: textbook_chunks_v1)
- `NEON_DATABASE_URL` - Neon PostgreSQL connection string

---

## Step 2: Initialize Qdrant Collection

Create the vector database collection with correct configuration:

```bash
# Run Qdrant setup script
python scripts/setup_qdrant.py --show-config

# If collection already exists and you want to recreate:
python scripts/setup_qdrant.py --recreate
```

**Expected Output:**
```
✓ Qdrant connection successful
✓ Collection created successfully
Collection Name: textbook_chunks_v1
Embedding Dimension: 384
Distance Metric: Cosine
Current Chunk Count: 0
```

**Troubleshooting:**
- If connection fails, verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check Qdrant Cloud dashboard to confirm cluster is running

---

## Step 3: Run Database Migrations

Initialize the PostgreSQL database schema:

```bash
# Run Alembic migrations
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema with query_logs table
```

**Troubleshooting:**
- If connection fails, verify `NEON_DATABASE_URL` in `.env`
- Ensure Neon database is active (not suspended)
- Check connection string format: `postgresql://user:pass@host/dbname?sslmode=require`

---

## Step 4: (Optional) Ingest Sample Data

If you have textbook chapters to test with:

```bash
# Ingest all chapters from a directory
python scripts/ingest_textbook.py --chapters-dir ../docs

# OR ingest a single file
python scripts/ingest_textbook.py --single-file ../docs/chapter-1.md
```

**Expected Output:**
```
Processing chapter: chapter-1.md
Chunking chapter...
Generated 45 chunks
Generating embeddings...
Uploading 45 chunks to Qdrant...
✓ Upload complete
```

**Note:** If you don't have textbook chapters yet, you can still test the API with empty results or manually insert test data.

---

## Step 5: Start the API Server

Run the FastAPI server:

```bash
# Development server with auto-reload
uvicorn src.main:app --reload --port 8000

# OR use the main.py script directly
python src/main.py
```

**Expected Output:**
```
INFO:     Starting RAG Chatbot Backend...
INFO:     ✓ Configuration validated
INFO:     ✓ Qdrant connection successful
INFO:     ✓ Neon PostgreSQL connection successful
INFO:     ✓ Embedding service loaded
INFO:     ✓ Agent service initialized
INFO:     RAG Chatbot Backend is ready to accept requests
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Troubleshooting:**
- **Port 8000 already in use:** Use `--port 8001` to run on different port
- **Import errors:** Ensure all dependencies installed and virtual environment activated
- **Configuration errors:** Check `.env` file for missing/invalid values

---

## Step 6: Test API Endpoints

### Test 1: Root Endpoint

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "name": "RAG Chatbot API",
  "version": "1.0.0",
  "description": "Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics textbook",
  "docs": "/docs",
  "health": "/health"
}
```

### Test 2: Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "neon_connected": true,
  "timestamp": "2025-12-25T10:30:00.000000Z"
}
```

**If degraded:**
- `qdrant_connected: false` → Check Qdrant credentials and network
- `neon_connected: false` → Check Neon database status

### Test 3: Chat Endpoint (Basic Query)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is inverse kinematics?"
  }'
```

**Expected Response (with data):**
```json
{
  "answer": "Inverse kinematics solves for joint angles... [Chapter 3, Section 3.2]",
  "citations": [
    {
      "chunk_id": "ch3-s3.2-001",
      "chapter": 3,
      "section": "3.2",
      "url_anchor": "#inverse-kinematics",
      "relevance_score": 0.89,
      "text_preview": "Inverse kinematics (IK) is the process...",
      "source": "Chapter 3, Section 3.2"
    }
  ],
  "query_id": "550e8400-e29b-41d4-a716-446655440000",
  "generation_time_ms": 1234
}
```

**Expected Response (no data ingested):**
```json
{
  "answer": "Information not found in the book. Please try rephrasing your question or ask about a different topic covered in the textbook.",
  "citations": [],
  "query_id": "...",
  "generation_time_ms": 123
}
```

### Test 4: Chat Endpoint (Debug Mode)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain forward kinematics",
    "debug": true
  }'
```

**Expected Response:**
```json
{
  "answer": "...",
  "citations": [...],
  "query_id": "...",
  "generation_time_ms": 1234,
  "debug_metadata": {
    "retrieval": {
      "chunks_retrieved": 5,
      "top_scores": [0.89, 0.85, 0.81],
      "search_time_ms": 1234
    },
    "chunks": [
      {
        "chunk_id": "ch3-s3.1-001",
        "score": 0.89,
        "chapter": 3,
        "section": "3.1",
        "text_preview": "Forward kinematics (FK) computes..."
      }
    ]
  }
}
```

### Test 5: Chat Endpoint (with Session ID)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is a Jacobian matrix?",
    "session_id": "test-session-123"
  }'
```

Session ID will be hashed and stored in the database for analytics.

---

## Step 7: Test Error Handling

### Test 7a: Empty Query (400 Error)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": ""
  }'
```

**Expected Response:**
```json
{
  "detail": "Query cannot be empty or only whitespace"
}
```

### Test 7b: Query Too Long (400 Error)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"$(python -c 'print(\"a\" * 1001)')\"
  }"
```

**Expected Response:**
```json
{
  "detail": "Query must not exceed 1000 characters"
}
```

### Test 7c: Rate Limiting (429 Error)

Send 101 requests within 1 minute:

```bash
# Send 101 requests rapidly
for i in {1..101}; do
  curl -X POST http://localhost:8000/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "test"}' &
done
wait
```

**Expected Response (after 100 requests):**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "retry_after": "60 seconds"
}
```

---

## Step 8: Verify Database Logging

Check that queries are being logged to Neon PostgreSQL:

```python
# Run this Python script to check logs
import os
from src.models.database import get_database_manager

db_manager = get_database_manager()

with db_manager.get_session() as session:
    from src.models.database import QueryLogModel

    recent_queries = session.query(QueryLogModel).order_by(
        QueryLogModel.timestamp.desc()
    ).limit(10).all()

    print(f"Recent queries ({len(recent_queries)}):")
    for q in recent_queries:
        print(f"  [{q.timestamp}] {q.query_text[:50]}... ({q.mode}, {q.response_time_ms}ms)")
```

---

## Step 9: Interactive API Documentation

FastAPI provides automatic interactive documentation:

1. **Swagger UI:** http://localhost:8000/docs
2. **ReDoc:** http://localhost:8000/redoc

You can test all endpoints directly from the browser using the Swagger UI.

---

## Step 10: Performance Validation

Check that performance meets requirements:

- **p95 latency < 3 seconds** for typical queries
- **Embedding generation < 200ms** (check logs)
- **Qdrant query < 500ms** (check logs)
- **Gemini API response < 2 seconds** (check logs)

Monitor logs during testing:

```bash
# Server logs show performance timings
INFO:src.services.embeddings:embedding_generation completed in 150.23ms
INFO:src.services.vector_store:vector_search completed in 234.56ms
INFO:src.services.agent:agent_generation completed in 1567.89ms
INFO:src.api.routes.chat:Chat request completed successfully (time=2156ms, chunks=5)
```

---

## Common Issues & Solutions

### Issue: "Module not found" errors

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: Qdrant connection timeout

**Solution:**
- Check Qdrant Cloud cluster status
- Verify API key hasn't expired
- Check firewall/network settings

### Issue: Gemini API 429 errors

**Solution:**
- You're hitting rate limits (15 RPM for free tier)
- Add delay between requests
- Check API key quota in Google AI Studio

### Issue: Database migration fails

**Solution:**
```bash
# Drop all tables and recreate
alembic downgrade base
alembic upgrade head
```

### Issue: "No module named 'src'"

**Solution:**
```bash
# Run commands from backend/ directory, not backend/src/
cd D:\PIAIC\Quarter4\Physical-AI-Humanoid-Robotics\backend
```

---

## Success Criteria

Phase 3 testing is complete when:

- ✅ Qdrant collection created (384 dimensions, cosine distance)
- ✅ Database migrations applied successfully
- ✅ FastAPI server starts without errors
- ✅ /health returns "healthy" status
- ✅ /api/v1/chat accepts queries and returns responses
- ✅ Citations appear in responses (if data ingested)
- ✅ Query logging works (check Neon database)
- ✅ Rate limiting activates after 100 req/min
- ✅ Error handling works for invalid inputs
- ✅ p95 latency < 3 seconds

---

## Next Steps After Testing

Once Phase 3 testing passes:

1. **Phase 4:** Implement selected-text query mode
2. **Phase 5:** Build frontend React components
3. **Deployment:** Deploy to Render/Railway/Fly.io

---

## Support

If you encounter issues:

1. Check logs for detailed error messages
2. Verify all `.env` variables are set correctly
3. Ensure all services (Qdrant, Neon, Gemini) are accessible
4. Review configuration with: `python scripts/setup_qdrant.py --show-config`
