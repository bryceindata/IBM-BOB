# IBM Bob Copilot - Environment Configuration Template
# Copy this file to .env and update with your actual values

# ============================================
# Application Settings
# ============================================
APP_NAME=IBM Bob Copilot
APP_ENV=development
DEBUG=true
SECRET_KEY=change-this-to-a-secure-random-string-in-production

# ============================================
# Server Configuration
# ============================================
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501

# Backend Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Server
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8501

# ============================================
# AI Provider Configuration (Optional)
# ============================================
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Ollama Configuration (for local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# ============================================
# Database Configuration (Optional - for future use)
# ============================================
DATABASE_URL=postgresql://bobuser:password@localhost:5432/bobdb
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# ============================================
# Redis Configuration (Optional - for caching)
# ============================================
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# ============================================
# Vector Database (Optional - for RAG)
# ============================================
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# ============================================
# Security Settings
# ============================================
JWT_SECRET_KEY=change-this-jwt-secret-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8501

# ============================================
# Logging Configuration
# ============================================
LOG_LEVEL=INFO
LOG_FORMAT=json

# ============================================
# Feature Flags
# ============================================
ENABLE_METRICS=false
ENABLE_TRACING=false
ENABLE_RATE_LIMITING=false

# ============================================
# Docker-specific Settings
# ============================================
# Use these when running in Docker
# BACKEND_URL=http://backend:8000
# REDIS_URL=redis://redis:6379/0
# DATABASE_URL=postgresql://bobuser:password@postgres:5432/bobdb