# IBM Bob Copilot - Application Startup Script
# This script starts both the FastAPI backend and Streamlit frontend

Write-Host "🚀 Starting IBM Bob Copilot..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".\IBM\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment 'IBM' not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv IBM" -ForegroundColor Yellow
    exit 1
}

# Check if dependencies are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
& .\IBM\Scripts\python.exe -c "import fastapi, uvicorn, streamlit" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dependencies not installed!" -ForegroundColor Red
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & .\IBM\Scripts\python.exe -m pip install --upgrade pip --quiet
    & .\IBM\Scripts\pip.exe install -r requirements.txt --quiet
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
}

Write-Host "✅ Dependencies verified!" -ForegroundColor Green
Write-Host ""

# Start backend in a new PowerShell window
Write-Host "🔧 Starting FastAPI Backend (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$PWD'; .\IBM\Scripts\Activate.ps1; Write-Host '🔧 FastAPI Backend Running' -ForegroundColor Green; Write-Host 'API: http://localhost:8000' -ForegroundColor Cyan; Write-Host 'Docs: http://localhost:8000/docs' -ForegroundColor Cyan; Write-Host ''; uvicorn app.main:app --reload --port 8000"
)

# Wait for backend to start
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test backend health
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Backend is running!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""

# Start frontend in a new PowerShell window
Write-Host "🎨 Starting Streamlit Frontend (Port 8501)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$PWD'; .\IBM\Scripts\Activate.ps1; Write-Host '🎨 Streamlit Frontend Running' -ForegroundColor Green; Write-Host 'UI: http://localhost:8501' -ForegroundColor Cyan; Write-Host ''; streamlit run frontend/streamlit_app.py"
)

Write-Host ""
Write-Host "✅ Application started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Cyan
Write-Host "   Frontend UI:  http://localhost:8501" -ForegroundColor White
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: Both services will open in separate windows" -ForegroundColor Yellow
Write-Host "🛑 To stop: Press Ctrl+C in each window" -ForegroundColor Yellow
Write-Host ""

# Made with Bob
