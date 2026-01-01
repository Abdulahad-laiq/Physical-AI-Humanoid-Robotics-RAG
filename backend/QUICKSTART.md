# Quick Start Guide

Get the RAG Chatbot backend running in 5 minutes.

## Option 1: Automated Setup (Windows)

```powershell
# Run the quick start script
cd D:\PIAIC\Quarter4\Physical-AI-Humanoid-Robotics\backend
.\quickstart.ps1
```

The script will:
1. Check Python installation
2. Create virtual environment
3. Install dependencies
4. Download spaCy model
5. Setup Qdrant collection
6. Optionally start the server

## Option 2: Manual Setup

### 1. Setup Environment

```bash
cd D:\PIAIC\Quarter4\Physical-AI-Humanoid-Robotics\backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure Credentials

Ensure `backend/.env` exists with your credentials:

```bash
# If not exists, copy from example
copy .env.example .env
```

Required variables:
- `GEMINI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `NEON_DATABASE_URL`

### 3. Initialize Services

```bash
# Create Qdrant collection
python scripts/setup_qdrant.py

# Run database migrations
alembic upgrade head
```

### 4. Start Server

```bash
uvicorn src.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs

## Quick Test Commands

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is inverse kinematics?"}'
```

## Automated Testing

```bash
# Run all API tests
python test_api.py
```

## Optional: Ingest Data

```bash
# Ingest textbook chapters
python scripts/ingest_textbook.py --chapters-dir ../docs
```

## Troubleshooting

**Server won't start?**
- Check `.env` file has all credentials
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Qdrant connection fails?**
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check Qdrant Cloud dashboard

**Neon connection fails?**
- Verify `NEON_DATABASE_URL` format
- Ensure database is not suspended

**Import errors?**
- Run from `backend/` directory (not `backend/src/`)
- Ensure virtual environment is activated

## Full Documentation

See [TESTING.md](./TESTING.md) for comprehensive testing guide.

## Next Steps

1. ✅ Setup complete
2. ✅ Server running
3. **Test API** → Run `python test_api.py`
4. **Ingest data** → Add textbook chapters
5. **Phase 4** → Implement selected-text mode
