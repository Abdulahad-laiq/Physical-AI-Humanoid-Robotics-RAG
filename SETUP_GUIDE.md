# RAG Chatbot Setup Guide

Complete guide to set up and run the RAG Chatbot for the Physical AI & Humanoid Robotics textbook.

## Overview

The RAG Chatbot system consists of:
- **Backend**: FastAPI server with RAG pipeline (Python)
- **Frontend**: React components integrated into Docusaurus
- **External Services**: Qdrant (vector database), Neon PostgreSQL (query logging), Google Gemini API (LLM)

---

## Prerequisites

### Required
- Python 3.10+ with pip
- Node.js 18+ with npm
- Git

### External Services (Free Tier)
1. **Qdrant Cloud** (https://cloud.qdrant.io) - Vector database
2. **Neon PostgreSQL** (https://neon.tech) - Serverless PostgreSQL
3. **Google AI Studio** (https://aistudio.google.com) - Gemini API key

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Abdulahad-laiq/Physical-AI-Humanoid-Robotics.git
cd Physical-AI-Humanoid-Robotics
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

#### Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=textbook_chunks_v1

# Neon PostgreSQL
NEON_DATABASE_URL=postgresql://user:password@host/database

# CORS (for local development, use localhost:3000)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Debug mode
DEBUG=true
```

#### Initialize Services

**Step 1: Set up Qdrant collection**

```bash
python backend/scripts/setup_qdrant.py
```

This creates the vector collection with:
- Dimension: 384 (all-MiniLM-L6-v2 embeddings)
- Distance metric: Cosine similarity
- Collection name: `textbook_chunks_v1`

**Step 2: Initialize database schema**

```bash
cd backend
alembic upgrade head
```

This creates the `queries` table for logging.

**Step 3: Ingest textbook chapters**

```bash
# Ingest all markdown files in docs/
python backend/scripts/ingest_textbook.py --input ../docs --recursive

# Or ingest specific files
python backend/scripts/ingest_textbook.py --input ../docs/ch01-introduction.md
```

This:
- Chunks textbook content (512 token max, section-aware)
- Generates embeddings
- Uploads to Qdrant with metadata (chapter, section, URL anchors)

#### Run Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

**Test endpoints:**
- Health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### 3. Frontend/Docusaurus Setup

The chat widget is already integrated into Docusaurus!

#### Install Dependencies

```bash
# From project root
npm install
```

#### Configure API URL

Create `.env` in project root:

```bash
REACT_APP_API_URL=http://localhost:8000
```

For production deployment, set to your deployed backend URL.

#### Run Docusaurus

```bash
npm start
```

Docusaurus will start at: http://localhost:3000

**The chat widget should appear in the bottom-right corner!**

---

## External Service Setup

### 1. Qdrant Cloud Setup

1. Go to https://cloud.qdrant.io
2. Sign up for free account
3. Create a new cluster:
   - Name: `rag-textbook` (or any name)
   - Region: Choose closest to you
   - Tier: **Free** (1GB storage, 1GB RAM)
4. Get credentials:
   - **Cluster URL**: Copy from dashboard (e.g., `https://abc123.us-east.qdrant.io:6333`)
   - **API Key**: Generate in "Data Access Control" section
5. Add to `backend/.env`:
   ```bash
   QDRANT_URL=https://your-cluster.qdrant.io:6333
   QDRANT_API_KEY=your_api_key_here
   ```

### 2. Neon PostgreSQL Setup

1. Go to https://neon.tech
2. Sign up for free account
3. Create a new project:
   - Name: `rag-chatbot` (or any name)
   - Region: Choose closest to you
   - Postgres version: Latest (16+)
4. Get connection string:
   - Go to "Connection Details"
   - Copy **Connection String** (starts with `postgresql://`)
5. Add to `backend/.env`:
   ```bash
   NEON_DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   ```

**Note:** Neon free tier includes:
- 0.5 GB storage
- 1 GB data transfer/month
- Auto-pause after 5 minutes inactivity (perfect for development!)

### 3. Google Gemini API Setup

1. Go to https://aistudio.google.com
2. Sign in with Google account
3. Click "Get API Key"
4. Create new API key or use existing
5. Copy API key
6. Add to `backend/.env`:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

**Free tier includes:**
- 60 requests/minute
- 1500 requests/day
- Perfect for development and testing!

---

## Testing

### Backend API Testing

The backend includes comprehensive test scripts.

**Run all tests:**

```bash
cd backend
python test_api.py
```

This tests:
- Health endpoint
- Global query mode
- Selected-text query mode
- Error handling
- Rate limiting

**Manual testing with curl:**

```bash
# Health check
curl http://localhost:8000/health

# Global query
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is inverse kinematics?"}'

# Selected-text query
curl -X POST http://localhost:8000/api/v1/chat/selected \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this term",
    "selected_text": "Inverse kinematics is the process of determining joint angles..."
  }'
```

### Frontend Testing

1. **Start services:**
   ```bash
   # Terminal 1: Backend
   cd backend && uvicorn src.main:app --reload

   # Terminal 2: Docusaurus
   npm start
   ```

2. **Test chat widget:**
   - Open http://localhost:3000
   - Click chat icon (bottom-right)
   - Type: "What is humanoid robotics?"
   - Verify response with citations

3. **Test selected-text mode:**
   - Highlight text on any page (10+ characters)
   - Click "Ask about this text" button
   - Type question about selected text
   - Verify answer uses only selected content

4. **Test citations:**
   - Click citation link (e.g., "[Chapter 1, Section 1.2]")
   - Verify page navigates to correct section

---

## Deployment

### Backend Deployment (Render/Railway/Fly.io)

See `backend/README.md` for detailed deployment instructions.

**Quick steps:**

1. Push code to GitHub
2. Connect repository to Render/Railway
3. Set environment variables in platform dashboard
4. Deploy!

### Frontend Deployment (GitHub Pages/Vercel/Netlify)

**GitHub Pages:**

```bash
# Set organization/user name in docusaurus.config.js
# Then build and deploy:
npm run deploy
```

**Vercel/Netlify:**

1. Connect GitHub repository
2. Build command: `npm run build`
3. Output directory: `build`
4. Set environment variable: `REACT_APP_API_URL=https://your-backend.com`

---

## Troubleshooting

### Backend Issues

**Problem: "ModuleNotFoundError: No module named 'X'"**

Solution:
```bash
cd backend
.venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

**Problem: "Qdrant connection failed"**

Solution:
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check Qdrant cluster is running (cloud.qdrant.io dashboard)
- Test: `python backend/scripts/setup_qdrant.py --show-config`

**Problem: "Database connection failed"**

Solution:
- Verify `NEON_DATABASE_URL` in `.env`
- Check Neon project is active (neon.tech dashboard)
- Run: `alembic upgrade head` to initialize schema

**Problem: "Gemini API rate limit"**

Solution:
- Free tier: 60 requests/minute
- Wait 1 minute or upgrade to paid tier
- Check quota: https://aistudio.google.com/app/apikey

### Frontend Issues

**Problem: Chat widget not appearing**

Solution:
- Check browser console for errors
- Verify `src/theme/Root.js` exists
- Clear cache: `npm run clear && npm run build`

**Problem: "CORS error"**

Solution:
- Add Docusaurus URL to `CORS_ORIGINS` in backend `.env`:
  ```bash
  CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
  ```
- Restart backend server

**Problem: TypeScript errors**

Solution:
```bash
# Type check
cd frontend
npm run type-check

# Or in project root for Docusaurus
npm run type-check
```

---

## File Structure

```
Physical-AI-Humanoid-Robotics/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/               # API routes
│   │   ├── models/            # Data models
│   │   ├── services/          # Core services (RAG, embeddings, agent)
│   │   └── utils/             # Utilities
│   ├── scripts/               # Setup and ingestion scripts
│   ├── .env                   # Environment variables (create from .env.example)
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Standalone React frontend (for reference)
│   └── src/
│       ├── components/        # React components
│       ├── hooks/             # Custom hooks
│       ├── services/          # API client
│       └── types/             # TypeScript types
├── src/                       # Docusaurus integration
│   ├── components/
│   │   ├── chat/             # Chat components (copied from frontend/)
│   │   └── ChatbotWidget.tsx # Docusaurus wrapper
│   ├── theme/
│   │   └── Root.js           # Theme swizzle for global chat widget
│   ├── hooks/                # Text selection hook
│   ├── services/             # API client
│   └── types/                # TypeScript types
├── docs/                      # Textbook markdown files
├── specs/                     # Feature specifications
│   └── rag-chatbot/
│       ├── spec.md           # Requirements
│       ├── plan.md           # Architecture
│       └── tasks.md          # Implementation tasks
└── docusaurus.config.js      # Docusaurus configuration
```

---

## Development Workflow

### Adding New Textbook Content

1. Add markdown files to `docs/`
2. Ingest into vector database:
   ```bash
   python backend/scripts/ingest_textbook.py --input docs/new-chapter.md
   ```
3. Test queries against new content

### Updating Chat Widget

1. Edit files in `src/components/chat/`
2. Restart Docusaurus: `npm start`
3. Test changes at http://localhost:3000

### Database Migrations

```bash
cd backend

# Create migration
alembic revision -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Performance Tips

### Backend Optimization

1. **Enable query caching** (future enhancement in `src/services/agent.py`)
2. **Monitor Qdrant storage:**
   ```python
   python -c "from src.services.vector_store import get_vector_store; vs = get_vector_store(); print(f'Chunks: {vs.count_chunks()}')"
   ```
3. **Check query logs:**
   ```sql
   -- Connect to Neon database
   SELECT COUNT(*) FROM queries WHERE mode = 'global';
   ```

### Frontend Optimization

1. **Lazy load chat widget:**
   ```tsx
   const ChatWidget = React.lazy(() => import('./components/ChatbotWidget'));
   ```

2. **Only show on specific pages:**
   ```tsx
   // In src/theme/Root.js
   import {useLocation} from '@docusaurus/router';

   const location = useLocation();
   const showChat = location.pathname.startsWith('/docs');
   ```

---

## Next Steps

After setup:

1. ✅ Test both query modes (global + selected-text)
2. ✅ Ingest remaining textbook chapters
3. ✅ Customize chat widget styling (`src/css/chat.css`)
4. ✅ Deploy backend to cloud platform
5. ✅ Deploy Docusaurus to GitHub Pages/Vercel
6. ✅ Monitor usage and performance

---

## Support

- **Backend issues**: See `backend/README.md` and `backend/TESTING.md`
- **Frontend integration**: See `frontend/DOCUSAURUS_INTEGRATION.md`
- **Architecture**: See `specs/rag-chatbot/plan.md`
- **Tasks**: See `specs/rag-chatbot/tasks.md`

---

## Success Criteria

From `specs/rag-chatbot/spec.md`, verify:

- ✅ **SC-001**: Answers grounded in textbook content
- ✅ **SC-002**: Zero hallucinations ("Information not found" for out-of-scope)
- ✅ **SC-003**: Selected-text mode isolated (no global embeddings)
- ✅ **SC-004**: Citations include chapter/section references
- ✅ **SC-005**: p95 latency < 3 seconds
- ✅ **SC-006**: Free tier operation (Qdrant, Neon, Gemini)
- ✅ **SC-007**: Chat widget embedded in Docusaurus
- ✅ **SC-008**: Citation navigation works
- ✅ **SC-009**: Error handling (rate limits, timeouts, validation)
- ✅ **SC-010**: Query logging to PostgreSQL

---

## License

MIT License - See LICENSE file for details
