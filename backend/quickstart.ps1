# Quick Start Script for RAG Chatbot Backend
# Run this script to set up and test the backend

Write-Host "======================================================================"
Write-Host "RAG Chatbot Backend - Quick Start"
Write-Host "======================================================================"
Write-Host ""

# Check if running in backend directory
$currentDir = Get-Location
if ($currentDir.Path -notlike "*backend*") {
    Write-Host "ERROR: Please run this script from the backend directory" -ForegroundColor Red
    Write-Host "Example: cd D:\PIAIC\Quarter4\Physical-AI-Humanoid-Robotics\backend" -ForegroundColor Yellow
    Write-Host "         .\quickstart.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/7] Checking Python installation..." -ForegroundColor Cyan

# Check Python
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python 3\.[9-9]|Python 3\.1[0-9]") {
            $pythonCmd = $cmd
            Write-Host "  ✓ Found: $version" -ForegroundColor Green
            break
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "  ✗ Python 3.9+ not found" -ForegroundColor Red
    Write-Host "  Please install Python 3.9 or higher from python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[2/7] Creating virtual environment..." -ForegroundColor Cyan

if (Test-Path "venv") {
    Write-Host "  ✓ Virtual environment already exists" -ForegroundColor Green
} else {
    & $pythonCmd -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Cyan

# Activate venv
$activateScript = "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "  ✗ Activation script not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/7] Installing dependencies..." -ForegroundColor Cyan

& pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[5/7] Downloading spaCy model..." -ForegroundColor Cyan

& python -m spacy download en_core_web_sm --quiet
Write-Host "  ✓ spaCy model downloaded" -ForegroundColor Green

Write-Host ""
Write-Host "[6/7] Checking configuration..." -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    Write-Host "  ! Creating .env from .env.example" -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "  ✓ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "  IMPORTANT: Edit .env file and add your credentials:" -ForegroundColor Yellow
    Write-Host "    - GEMINI_API_KEY" -ForegroundColor Yellow
    Write-Host "    - QDRANT_URL" -ForegroundColor Yellow
    Write-Host "    - QDRANT_API_KEY" -ForegroundColor Yellow
    Write-Host "    - NEON_DATABASE_URL" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "  Press Enter when .env is configured (or Ctrl+C to exit)"
}

Write-Host ""
Write-Host "[7/7] Setting up Qdrant collection..." -ForegroundColor Cyan

& python scripts/setup_qdrant.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Qdrant collection ready" -ForegroundColor Green
} else {
    Write-Host "  ✗ Qdrant setup failed - check credentials in .env" -ForegroundColor Red
    Write-Host "  You can run this manually later: python scripts/setup_qdrant.py" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================"
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================================================"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. (Optional) Ingest textbook chapters:" -ForegroundColor White
Write-Host "     python scripts/ingest_textbook.py --chapters-dir ../docs" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Start the API server:" -ForegroundColor White
Write-Host "     uvicorn src.main:app --reload --port 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Test the API:" -ForegroundColor White
Write-Host "     http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. See TESTING.md for detailed testing instructions" -ForegroundColor White
Write-Host ""

# Ask if user wants to start server
$startServer = Read-Host "Would you like to start the API server now? (y/N)"
if ($startServer -eq "y" -or $startServer -eq "Y") {
    Write-Host ""
    Write-Host "Starting FastAPI server..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    & uvicorn src.main:app --reload --port 8000
}
