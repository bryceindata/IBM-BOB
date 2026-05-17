# IBM Bob Copilot - Docker Deployment Script
# This script deploys the application using Docker Compose

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "restart", "logs", "build", "status", "clean")]
    [string]$Action = "start"
)

$ErrorActionPreference = "Stop"

Write-Host "🐳 IBM Bob Copilot - Docker Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
function Test-Docker {
    try {
        $dockerVersion = docker --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Docker is not installed or not running!" -ForegroundColor Red
        Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        return $false
    }
    return $false
}

# Check if Docker Compose is available
function Test-DockerCompose {
    try {
        $composeVersion = docker compose version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ Docker Compose is not available!" -ForegroundColor Red
        return $false
    }
    return $false
}

# Create .env file if it doesn't exist
function Initialize-Environment {
    if (-not (Test-Path ".env")) {
        Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env file created. Please update it with your configuration." -ForegroundColor Green
        Write-Host "⚠️  You may need to edit .env before starting the application." -ForegroundColor Yellow
    } else {
        Write-Host "✅ .env file exists" -ForegroundColor Green
    }
}

# Start the application
function Start-Application {
    Write-Host "🚀 Starting IBM Bob Copilot..." -ForegroundColor Cyan
    Write-Host ""
    
    Initialize-Environment
    
    Write-Host "📦 Building and starting containers..." -ForegroundColor Yellow
    docker compose up -d --build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Application started successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Access Points:" -ForegroundColor Cyan
        Write-Host "   Frontend UI:  http://localhost:8501" -ForegroundColor White
        Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 Tips:" -ForegroundColor Yellow
        Write-Host "   - View logs: .\deploy.ps1 logs" -ForegroundColor White
        Write-Host "   - Stop app:  .\deploy.ps1 stop" -ForegroundColor White
        Write-Host "   - Restart:   .\deploy.ps1 restart" -ForegroundColor White
        Write-Host ""
        
        # Wait a moment and check health
        Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5 -UseBasicParsing
            Write-Host "✅ Backend is healthy and responding!" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Backend may still be starting. Check logs with: .\deploy.ps1 logs" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Failed to start application!" -ForegroundColor Red
        Write-Host "Check logs with: docker compose logs" -ForegroundColor Yellow
    }
}

# Stop the application
function Stop-Application {
    Write-Host "🛑 Stopping IBM Bob Copilot..." -ForegroundColor Yellow
    docker compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Application stopped successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to stop application!" -ForegroundColor Red
    }
}

# Restart the application
function Restart-Application {
    Write-Host "🔄 Restarting IBM Bob Copilot..." -ForegroundColor Cyan
    Stop-Application
    Start-Sleep -Seconds 2
    Start-Application
}

# Show logs
function Show-Logs {
    Write-Host "📋 Showing application logs (Ctrl+C to exit)..." -ForegroundColor Cyan
    Write-Host ""
    docker compose logs -f
}

# Build containers
function Build-Containers {
    Write-Host "🔨 Building Docker containers..." -ForegroundColor Cyan
    docker compose build --no-cache
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Containers built successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to build containers!" -ForegroundColor Red
    }
}

# Show status
function Show-Status {
    Write-Host "📊 Application Status:" -ForegroundColor Cyan
    Write-Host ""
    docker compose ps
    Write-Host ""
    
    # Check if services are running
    $backendRunning = docker compose ps backend --format json 2>$null | ConvertFrom-Json | Where-Object { $_.State -eq "running" }
    $frontendRunning = docker compose ps frontend --format json 2>$null | ConvertFrom-Json | Where-Object { $_.State -eq "running" }
    
    if ($backendRunning) {
        Write-Host "✅ Backend:  Running" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend:  Not Running" -ForegroundColor Red
    }
    
    if ($frontendRunning) {
        Write-Host "✅ Frontend: Running" -ForegroundColor Green
    } else {
        Write-Host "❌ Frontend: Not Running" -ForegroundColor Red
    }
}

# Clean up everything
function Clean-Application {
    Write-Host "🧹 Cleaning up Docker resources..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  This will remove:" -ForegroundColor Yellow
    Write-Host "   - All containers" -ForegroundColor White
    Write-Host "   - All volumes" -ForegroundColor White
    Write-Host "   - All images" -ForegroundColor White
    Write-Host ""
    
    $confirm = Read-Host "Are you sure? (yes/no)"
    if ($confirm -eq "yes") {
        docker compose down -v --rmi all
        Write-Host "✅ Cleanup complete!" -ForegroundColor Green
    } else {
        Write-Host "❌ Cleanup cancelled" -ForegroundColor Yellow
    }
}

# Main execution
if (-not (Test-Docker)) {
    exit 1
}

if (-not (Test-DockerCompose)) {
    exit 1
}

Write-Host ""

switch ($Action) {
    "start" { Start-Application }
    "stop" { Stop-Application }
    "restart" { Restart-Application }
    "logs" { Show-Logs }
    "build" { Build-Containers }
    "status" { Show-Status }
    "clean" { Clean-Application }
    default { 
        Write-Host "❌ Unknown action: $Action" -ForegroundColor Red
        Write-Host "Valid actions: start, stop, restart, logs, build, status, clean" -ForegroundColor Yellow
    }
}

Write-Host ""

# Made with Bob
