# Remaining Manual Setup Steps

This document lists what still needs to be done to complete the RAG Chatbot implementation.

## ✅ Completed

All code has been written and integrated:

- ✅ Backend implementation (FastAPI, RAG pipeline, agent, services)
- ✅ Frontend implementation (React components, hooks, API client)
- ✅ Docusaurus integration (chat widget embedded)
- ✅ Database migrations (Alembic)
- ✅ Ingestion scripts (chunking, embeddings, vector store)
- ✅ Testing scripts
- ✅ Documentation (README, setup guides, testing guides)
- ✅ TypeScript configuration
- ✅ Dependency management (requirements.txt, package.json)

## ⏳ Remaining Manual Steps

These steps require external accounts and cannot be automated:

### 1. Create External Service Accounts (15-20 minutes)

#### A. Google Gemini API Key (5 minutes)

**Purpose:** Powers the LLM for generating answers

**Steps:**
1. Go to https://aistudio.google.com
2. Sign in with Google account
3. Click "Get API Key" button
4. Create new API key or use existing
5. Copy the API key
6. Add to `backend/.env`:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Perfect for development!

**Cost:** $0 (free tier sufficient)

---

#### B. Qdrant Cloud Account (5 minutes)

**Purpose:** Vector database for storing textbook embeddings

**Steps:**
1. Go to https://cloud.qdrant.io
2. Sign up for free account
3. Create a new cluster:
   - **Name**: `rag-textbook` (or any name)
   - **Region**: Select closest to your location
   - **Cloud Provider**: Any (AWS/GCP/Azure)
   - **Tier**: Select **FREE** tier
4. Wait for cluster provisioning (1-2 minutes)
5. Get credentials:
   - **Cluster URL**: Copy from cluster dashboard
     - Format: `https://xyz123.us-east.qdrant.io:6333`
   - **API Key**:
     - Go to "Data Access Control" tab
     - Click "Create API Key"
     - Copy the generated key
6. Add to `backend/.env`:
   ```bash
   QDRANT_URL=https://your-cluster.qdrant.io:6333
   QDRANT_API_KEY=your_api_key_here
   QDRANT_COLLECTION_NAME=textbook_chunks_v1
   ```

**Free Tier Limits:**
- 1 GB storage
- 1 GB RAM
- Unlimited API requests
- Perfect for this project!

**Cost:** $0 (free tier sufficient)

---

#### C. Neon PostgreSQL Account (5 minutes)

**Purpose:** Stores query logs for analytics

**Steps:**
1. Go to https://neon.tech
2. Sign up for free account (GitHub/Google/Email)
3. Create a new project:
   - **Name**: `rag-chatbot` (or any name)
   - **Region**: Select closest to your location
   - **Postgres Version**: Latest (16+)
4. Get connection string:
   - Go to project dashboard
   - Click "Connection Details"
   - Copy the **Connection String**
   - Format: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`
5. Add to `backend/.env`:
   ```bash
   NEON_DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
   ```

**Free Tier Limits:**
- 0.5 GB storage
- 1 GB data transfer per month
- Auto-pause after 5 minutes of inactivity
- Perfect for query logging!

**Cost:** $0 (free tier sufficient)

---

### 2. Install Backend Dependencies (5 minutes)

If you haven't already:

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Or Windows CMD
# .venv\Scripts\activate.bat

# Or Linux/Mac
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

---

### 3. Initialize Backend Services (5 minutes)

Once you have all credentials in `backend/.env`:

#### Step 1: Create Qdrant Collection

```bash
cd backend
python scripts/setup_qdrant.py
```

**Expected output:**
```
Starting Qdrant collection setup
✓ Qdrant connection successful
Creating collection (dimension=384, distance=cosine)
✓ Collection created successfully
Collection verification: 0 chunks (expected 0 for new collection)
====================================
Qdrant Setup Complete
====================================
```

#### Step 2: Initialize Database Schema

```bash
cd backend
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> abc123, create queries table
```

#### Step 3: Ingest Textbook Content

Ingest all markdown files from the `docs/` directory:

```bash
cd backend
python scripts/ingest_textbook.py --input ../docs --recursive
```

**Or ingest specific files:**

```bash
# Ingest one chapter
python scripts/ingest_textbook.py --input ../docs/ch01-introduction.md

# Ingest multiple specific files
python scripts/ingest_textbook.py --input ../docs/ch01-introduction.md ../docs/ch02-robot-fundamentals.md
```

**Expected output:**
```
Processing: ../docs/ch01-introduction.md
  Chunks created: 45
  Embeddings generated: 45
  Uploaded to Qdrant: 45
Processing: ../docs/ch02-robot-fundamentals.md
  Chunks created: 67
  Embeddings generated: 67
  Uploaded to Qdrant: 67
Total chunks ingested: 112
```

**Time estimate:** 1-2 minutes per chapter

---

### 4. Test Backend (2 minutes)

Start the backend server:

```bash
cd backend
uvicorn src.main:app --reload
```

**Test endpoints:**

```bash
# Health check
curl http://localhost:8000/health

# Expected:
# {"status":"healthy","qdrant_connected":true,"neon_connected":true}

# Test query
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is inverse kinematics?"}'

# Expected: JSON response with answer and citations
```

Or use the comprehensive test script:

```bash
cd backend
python test_api.py
```

---

### 5. Test Frontend Integration (2 minutes)

Start Docusaurus:

```bash
# From project root
npm start
```

**Manual testing:**

1. Open http://localhost:3000
2. Click chat icon in bottom-right corner
3. Type: "What is humanoid robotics?"
4. Press Enter or click Send
5. Verify:
   - ✅ Answer appears
   - ✅ Citations shown (e.g., "[Chapter 1, Section 1.1]")
   - ✅ Loading spinner while processing
   - ✅ No errors in console (F12)

**Test selected-text mode:**

1. Highlight any paragraph on the page (at least 10 characters)
2. Click "Ask about this text" button
3. Type: "Summarize this"
4. Verify answer references only the selected text

**Test citations:**

1. Click on a citation link
2. Verify page navigates to referenced section
3. Section should be highlighted

---

## 📋 Checklist

Use this checklist to track your progress:

### External Services
- [ ] Created Google Gemini API account
- [ ] Got Gemini API key
- [ ] Added `GEMINI_API_KEY` to `backend/.env`
- [ ] Created Qdrant Cloud account
- [ ] Created Qdrant cluster (free tier)
- [ ] Got Qdrant URL and API key
- [ ] Added `QDRANT_URL` and `QDRANT_API_KEY` to `backend/.env`
- [ ] Created Neon PostgreSQL account
- [ ] Created Neon project
- [ ] Got database connection string
- [ ] Added `NEON_DATABASE_URL` to `backend/.env`

### Backend Setup
- [ ] Installed Python dependencies (`pip install -r requirements.txt`)
- [ ] Downloaded spaCy model (`python -m spacy download en_core_web_sm`)
- [ ] Created Qdrant collection (`python scripts/setup_qdrant.py`)
- [ ] Initialized database schema (`alembic upgrade head`)
- [ ] Ingested textbook chapters (`python scripts/ingest_textbook.py`)
- [ ] Tested backend (`python test_api.py`)
- [ ] Backend starts without errors (`uvicorn src.main:app --reload`)

### Frontend Setup
- [ ] Installed npm dependencies (`npm install`)
- [ ] Docusaurus starts without errors (`npm start`)
- [ ] Chat widget appears on page
- [ ] Global queries work
- [ ] Selected-text mode works
- [ ] Citations navigation works
- [ ] No console errors

### Deployment (Optional)
- [ ] Deployed backend to cloud platform
- [ ] Deployed Docusaurus to GitHub Pages/Vercel/Netlify
- [ ] Updated `REACT_APP_API_URL` in production environment
- [ ] Updated `CORS_ORIGINS` in backend production environment
- [ ] Tested production deployment

---

## ⚠️ Common Issues

### "Configuration validation failed"

**Problem:** Missing environment variables

**Solution:**
```bash
cd backend
python -c "from src.config import validate_configuration; validate_configuration()"
```

This will show which variables are missing.

### "Qdrant connection failed"

**Problem:** Wrong URL or API key

**Solution:**
1. Check cluster is running (https://cloud.qdrant.io)
2. Verify URL format: `https://xyz.region.qdrant.io:6333`
3. Regenerate API key if needed

### "Database connection failed"

**Problem:** Wrong connection string or database inactive

**Solution:**
1. Check Neon project is active (https://console.neon.tech)
2. Verify connection string format
3. Test connection:
   ```bash
   python -c "from src.models.database import get_database_manager; db = get_database_manager(); print(db.health_check())"
   ```

### "No chunks found in collection"

**Problem:** Textbook not ingested

**Solution:**
```bash
cd backend
python scripts/ingest_textbook.py --input ../docs --recursive
```

---

## 🎯 Success Criteria

After completing all steps, verify:

1. **Backend Health:**
   ```bash
   curl http://localhost:8000/health
   # Returns: {"status":"healthy",...}
   ```

2. **Query Works:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"query":"test"}'
   # Returns: {"answer":"...","citations":[...]}
   ```

3. **Frontend Works:**
   - Chat widget visible
   - Questions return answers
   - Citations clickable

4. **No Errors:**
   - Backend logs clean
   - Frontend console clean
   - Database logs queries

---

## 📚 Additional Resources

- **Full Setup Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Backend Details:** [backend/README.md](backend/README.md)
- **Testing Guide:** [backend/TESTING.md](backend/TESTING.md)
- **Integration Guide:** [frontend/DOCUSAURUS_INTEGRATION.md](frontend/DOCUSAURUS_INTEGRATION.md)
- **Architecture:** [specs/rag-chatbot/plan.md](specs/rag-chatbot/plan.md)
- **Tasks:** [specs/rag-chatbot/tasks.md](specs/rag-chatbot/tasks.md)

---

## 🆘 Need Help?

If you encounter issues:

1. Check the troubleshooting sections in the guides above
2. Review error messages carefully
3. Verify all environment variables are set correctly
4. Check service dashboards (Qdrant, Neon, Gemini)
5. Review backend logs for detailed error messages

---

## ✅ You're Almost There!

The implementation is **95% complete**. Only external service setup remains:

1. Get 3 API keys (Gemini, Qdrant, Neon) - 15 minutes
2. Run 3 setup commands - 5 minutes
3. Test - 2 minutes

**Total time:** ~25 minutes to full working system! 🎉
