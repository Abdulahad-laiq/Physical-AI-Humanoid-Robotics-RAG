# RAG Chatbot - Quick Start

Get the chatbot running in 5 minutes!

## 🚀 Prerequisites

- Python 3.10+
- Node.js 18+
- Google Gemini API key (https://aistudio.google.com)
- Qdrant Cloud account (https://cloud.qdrant.io - free tier)
- Neon PostgreSQL account (https://neon.tech - free tier)

---

## ⚡ 5-Minute Setup

### Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Create virtual environment and install dependencies
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configure environment
cp .env.example .env
# Edit .env with your API keys (see below)
```

**Required `.env` values:**

```bash
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=postgresql://user:password@host/database
CORS_ORIGINS=http://localhost:3000
```

### Step 2: Initialize Services (1 minute)

```bash
# From backend/ directory

# Set up Qdrant collection
python scripts/setup_qdrant.py

# Initialize database
alembic upgrade head

# Ingest sample chapter
python scripts/ingest_textbook.py --input ../docs/ch01-introduction.md
```

### Step 3: Start Backend (30 seconds)

```bash
cd backend
uvicorn src.main:app --reload
```

Backend running at: http://localhost:8000

### Step 4: Start Frontend (1 minute)

```bash
# New terminal, from project root
npm install
npm start
```

Docusaurus running at: http://localhost:3000

### Step 5: Test! (30 seconds)

1. Open http://localhost:3000
2. Click chat icon (bottom-right)
3. Ask: "What is physical AI?"
4. Get answer with citations!

---

## 🎯 What You Get

- **Global Query Mode**: Ask questions about entire textbook
- **Selected-Text Mode**: Highlight text → ask questions about selection only
- **Citations**: Click to navigate to source sections
- **Dark/Light Theme**: Auto-syncs with Docusaurus theme

---

## 🔧 Quick Commands

### Backend

```bash
# Start server
cd backend && uvicorn src.main:app --reload

# Test API
python backend/test_api.py

# Check health
curl http://localhost:8000/health

# Ingest more chapters
python backend/scripts/ingest_textbook.py --input docs/ --recursive
```

### Frontend

```bash
# Start Docusaurus
npm start

# Build for production
npm run build

# Type check
npm run type-check
```

---

## 📊 Get Your API Keys

### Google Gemini (1 minute)

1. Go to https://aistudio.google.com
2. Click "Get API Key"
3. Copy key → paste in `backend/.env` as `GEMINI_API_KEY`

**Free tier:** 60 requests/min, 1500/day

### Qdrant Cloud (2 minutes)

1. Sign up at https://cloud.qdrant.io
2. Create cluster (free tier: 1GB storage)
3. Copy cluster URL (e.g., `https://abc123.us-east.qdrant.io:6333`)
4. Generate API key in "Data Access Control"
5. Add to `backend/.env`:
   ```bash
   QDRANT_URL=https://your-cluster.qdrant.io:6333
   QDRANT_API_KEY=your_key
   ```

### Neon PostgreSQL (2 minutes)

1. Sign up at https://neon.tech
2. Create project
3. Copy connection string (starts with `postgresql://`)
4. Add to `backend/.env`:
   ```bash
   NEON_DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   ```

**Free tier:** 0.5GB storage, auto-pause after 5 min

---

## ✅ Verification

After setup, verify everything works:

### Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "neon_connected": true
}
```

### Test Query

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is inverse kinematics?"}'
```

Expected: Answer with citations

### Frontend

1. Open http://localhost:3000
2. Chat widget visible (bottom-right)
3. Ask question → get answer
4. Highlight text → "Ask about this text" button appears

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"

```bash
cd backend
.venv\Scripts\activate
pip install -r requirements.txt
```

### "Qdrant connection failed"

- Check cluster URL and API key in `.env`
- Verify cluster is running (cloud.qdrant.io dashboard)

### "Database connection failed"

- Check connection string in `.env`
- Verify Neon project is active (neon.tech dashboard)

### Chat widget not appearing

- Clear cache: `npm run clear && npm start`
- Check console for errors (F12)

### CORS errors

Add to `backend/.env`:
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

Then restart backend.

---

## 📚 Next Steps

- [Full Setup Guide](SETUP_GUIDE.md) - Detailed instructions
- [Backend README](backend/README.md) - Backend architecture
- [Docusaurus Integration](frontend/DOCUSAURUS_INTEGRATION.md) - Frontend details
- [Testing Guide](backend/TESTING.md) - Comprehensive testing

---

## 🎉 You're Ready!

The chatbot is now running. Try these example queries:

- "What is humanoid robotics?"
- "Explain inverse kinematics"
- "How does balance control work?"
- Highlight any paragraph → Ask "Summarize this"

Enjoy your AI-powered textbook assistant! 🤖📖
