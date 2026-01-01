# RAG Chatbot Backend

AI-native Retrieval-Augmented Generation (RAG) chatbot for the Physical AI & Humanoid Robotics textbook.

## Architecture

Three-layer architecture:
- **API Layer**: FastAPI REST endpoints
- **Service Layer**: Agent orchestration, retrieval, embeddings, chunking
- **Storage Layer**: Qdrant (vectors), Neon PostgreSQL (metadata)

## Technology Stack

- **Framework**: FastAPI (Python 3.9+)
- **LLM**: Gemini-2.0-flash via AsyncOpenAI
- **Agent**: OpenAI Assistants SDK
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2, 384 dimensions)
- **Vector DB**: Qdrant Cloud Free Tier
- **SQL DB**: Neon PostgreSQL Free Tier
- **Chunking**: Hybrid section-aware (512 token max, spaCy sentence splitting)

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Qdrant Cloud account (free tier)
- Neon PostgreSQL account (free tier)
- Gemini API key

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Initialize Qdrant collection**:
   ```bash
   python scripts/setup_qdrant.py
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Ingest textbook chapters**:
   ```bash
   python scripts/ingest_textbook.py --chapters-dir ../docs
   ```

### Running the Server

**Development**:
```bash
uvicorn src.main:app --reload --port 8000
```

**Production**:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

```bash
docker build -t rag-chatbot-backend .
docker run -p 8000:8000 --env-file .env rag-chatbot-backend
```

## API Endpoints

### POST /api/v1/chat
Ask a question about the textbook (global query mode).

**Request**:
```json
{
  "query": "What is inverse kinematics?",
  "session_id": "optional-uuid",
  "debug": false
}
```

**Response**:
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
      "text_preview": "Inverse kinematics (IK) is the process..."
    }
  ],
  "query_id": "uuid",
  "generation_time_ms": 1234
}
```

### POST /api/v1/chat/selected
Ask a question about user-selected text (selected-text mode).

**Request**:
```json
{
  "query": "Explain this equation",
  "selected_text": "J = ∂f/∂q where J is the Jacobian matrix...",
  "session_id": "optional-uuid",
  "debug": false
}
```

### GET /api/v1/metadata
Retrieve retrieval metadata for debugging (query by query_id).

## Project Structure

```
backend/
├── src/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment configuration
│   ├── models/
│   │   ├── schemas.py           # Pydantic models
│   │   └── database.py          # Database connection
│   ├── services/
│   │   ├── agent.py             # Agent orchestration
│   │   ├── embeddings.py        # Embedding generation
│   │   ├── vector_store.py      # Qdrant client wrapper
│   │   ├── chunking.py          # Text chunking logic
│   │   └── selected_text.py     # Selected-text mode
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py          # Global query endpoint
│   │   │   ├── selected_text.py # Selected-text endpoint
│   │   │   └── metadata.py      # Debug endpoint
│   │   └── middleware.py        # Rate limiting, CORS
│   └── utils/
│       ├── logger.py            # Structured logging
│       └── validators.py        # Input validation
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── ingest_textbook.py       # Textbook ingestion
│   └── setup_qdrant.py          # Qdrant initialization
├── alembic/                     # Database migrations
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Development

### Running Tests

```bash
pytest tests/ -v
pytest tests/integration/ -v --asyncio-mode=auto
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
pylint src/ tests/

# Type checking
mypy src/
```

## Deployment

### Recommended Platforms (Free Tier)

- **Render**: Supports Docker, auto-deploy from git
- **Railway**: Easy environment variable management
- **Fly.io**: Global edge deployment

### Environment Variables (Production)

Ensure all variables in `.env.example` are set in your deployment platform's environment configuration.

### Health Check

The `/health` endpoint returns server status and can be used for monitoring.

## Monitoring

- **Logs**: Structured JSON logs with query_id tracking
- **Metrics**: Query rate (QPM), latency (p50, p95), error rate
- **Free Tier Usage**: Qdrant storage %, Neon storage %, Gemini RPM %

## Troubleshooting

### Gemini API Rate Limit Exceeded

- Implement query caching (1-hour TTL)
- Monitor Gemini RPM usage
- Add retry logic with exponential backoff

### Qdrant Storage Limit

- Optimize chunking (larger chunks = fewer vectors)
- Monitor storage usage weekly
- Consider upgrading to paid tier (~$25/month for 10GB)

### High Latency (p95 >3 seconds)

- Check Qdrant query latency (<500ms expected)
- Check Gemini API latency (<2 seconds expected)
- Profile embedding generation (<200ms expected)
- Consider GPU for Sentence-Transformers

## License

See LICENSE file in repository root.
