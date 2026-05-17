# 🐳 Docker Deployment Guide - IBM Bob Copilot

## Quick Start

### Prerequisites

1. **Install Docker Desktop**
   - Windows: https://www.docker.com/products/docker-desktop
   - Ensure Docker Desktop is running before proceeding

2. **Verify Installation**
   ```powershell
   docker --version
   docker compose version
   ```

---

## Deployment Methods

### Method 1: Automated Deployment (Recommended) ⭐

Simply run the deployment script:

```powershell
.\deploy.ps1 start
```

This will:
- ✅ Check Docker installation
- ✅ Create `.env` file from template
- ✅ Build Docker images
- ✅ Start all services
- ✅ Verify health status

**Access the application:**
- Frontend UI: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Method 2: Manual Docker Compose

```powershell
# Create environment file
Copy-Item .env.example .env

# Build and start services
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

---

## Deployment Script Commands

The `deploy.ps1` script supports multiple actions:

```powershell
# Start the application
.\deploy.ps1 start

# Stop the application
.\deploy.ps1 stop

# Restart the application
.\deploy.ps1 restart

# View live logs
.\deploy.ps1 logs

# Rebuild containers
.\deploy.ps1 build

# Check status
.\deploy.ps1 status

# Clean up everything (removes containers, volumes, images)
.\deploy.ps1 clean
```

---

## Configuration

### Environment Variables

Edit the `.env` file to configure the application:

```bash
# Basic Configuration
APP_NAME=IBM Bob Copilot
APP_ENV=development
DEBUG=true

# Server Ports
BACKEND_PORT=8000
FRONTEND_PORT=8501

# Optional: AI Provider Keys
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Custom Ports

To use different ports, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "9000:8000"  # Change 9000 to your desired port
  
  frontend:
    ports:
      - "9501:8501"  # Change 9501 to your desired port
```

---

## Architecture

The Docker deployment includes:

```
┌─────────────────────────────────────┐
│     Docker Compose Network          │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Frontend   │  │   Backend   │ │
│  │  (Streamlit) │  │  (FastAPI)  │ │
│  │  Port: 8501  │  │  Port: 8000 │ │
│  └──────┬───────┘  └──────┬──────┘ │
│         │                 │        │
│         └────────┬────────┘        │
│                  │                 │
│         ┌────────▼────────┐        │
│         │  Shared Volume  │        │
│         │   (app code)    │        │
│         └─────────────────┘        │
└─────────────────────────────────────┘
```

---

## Container Details

### Backend Container
- **Image**: Built from Dockerfile
- **Port**: 8000
- **Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **Health Check**: HTTP GET to `/`
- **Volumes**: 
  - `./app` → `/app/app` (live code reload)
  - `./bob_evidence` → `/app/bob_evidence`

### Frontend Container
- **Image**: Built from Dockerfile
- **Port**: 8501
- **Command**: `streamlit run frontend/streamlit_app.py`
- **Depends On**: Backend (waits for backend health check)
- **Volumes**: 
  - `./frontend` → `/app/frontend` (live code reload)

---

## Development Workflow

### Live Code Reloading

Both containers support live code reloading:

1. **Backend**: Edit files in `./app/` - changes auto-reload
2. **Frontend**: Edit files in `./frontend/` - Streamlit auto-reloads

### Viewing Logs

```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100
```

### Accessing Containers

```powershell
# Backend shell
docker compose exec backend bash

# Frontend shell
docker compose exec frontend bash

# Run commands in container
docker compose exec backend python -c "print('Hello from container')"
```

---

## Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:
```powershell
# Find process using the port
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change the port in docker-compose.yml
```

### Container Won't Start

**Check logs**:
```powershell
docker compose logs backend
docker compose logs frontend
```

**Common issues**:
1. Missing dependencies → Rebuild: `.\deploy.ps1 build`
2. Port conflicts → Change ports in `docker-compose.yml`
3. Permission issues → Run Docker Desktop as Administrator

### Backend Health Check Failing

```powershell
# Check backend status
docker compose ps

# View backend logs
docker compose logs backend

# Restart backend
docker compose restart backend
```

### Cannot Connect to Backend from Frontend

**Issue**: Frontend can't reach backend

**Solution**: Ensure `BACKEND_URL` in frontend uses the service name:
```bash
# In .env or docker-compose.yml
BACKEND_URL=http://backend:8000  # Use service name, not localhost
```

---

## Performance Optimization

### Resource Limits

Add resource limits to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Build Cache

Speed up builds by using cache:

```powershell
# Build with cache
docker compose build

# Build without cache (clean build)
docker compose build --no-cache
```

---

## Production Considerations

### Security

1. **Change default secrets** in `.env`:
   ```bash
   SECRET_KEY=<generate-strong-random-key>
   JWT_SECRET_KEY=<generate-strong-random-key>
   ```

2. **Disable debug mode**:
   ```bash
   DEBUG=false
   APP_ENV=production
   ```

3. **Use secrets management**:
   ```yaml
   services:
     backend:
       secrets:
         - openai_api_key
   
   secrets:
     openai_api_key:
       file: ./secrets/openai_key.txt
   ```

### Scaling

Scale services horizontally:

```powershell
# Scale backend to 3 instances
docker compose up -d --scale backend=3

# Add load balancer (nginx) in docker-compose.yml
```

### Monitoring

Add monitoring services:

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

---

## Backup and Recovery

### Backup Volumes

```powershell
# Backup volume data
docker run --rm -v bob-data:/data -v ${PWD}:/backup alpine tar czf /backup/bob-data-backup.tar.gz /data
```

### Restore Volumes

```powershell
# Restore volume data
docker run --rm -v bob-data:/data -v ${PWD}:/backup alpine tar xzf /backup/bob-data-backup.tar.gz -C /
```

---

## Cleanup

### Remove Containers and Volumes

```powershell
# Stop and remove containers
docker compose down

# Remove containers and volumes
docker compose down -v

# Remove containers, volumes, and images
docker compose down -v --rmi all

# Or use the deployment script
.\deploy.ps1 clean
```

### Free Up Disk Space

```powershell
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

---

## Advanced Configuration

### Multi-Stage Builds

The Dockerfile uses multi-stage builds for optimization:

```dockerfile
FROM python:3.11-slim as base
# Base dependencies

FROM base as builder
# Build dependencies

FROM base as production
# Production image
```

### Custom Networks

Create isolated networks:

```yaml
networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
    internal: true  # No external access
```

### Health Checks

Customize health checks:

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## Comparison: Docker vs Local

| Feature | Docker Deployment | Local Development |
|---------|------------------|-------------------|
| Setup Time | 5 minutes | 10-15 minutes |
| Dependencies | Isolated in containers | System-wide |
| Consistency | Same on all machines | May vary |
| Resource Usage | Higher (containers) | Lower |
| Debugging | Requires container access | Direct access |
| Best For | Production-like testing | Active development |

---

## Next Steps

1. ✅ Deploy with Docker: `.\deploy.ps1 start`
2. 📖 Read [API_SPECIFICATION.md](API_SPECIFICATION.md) for API details
3. 🏗️ Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
4. 🚀 Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for cloud deployment

---

## Support

**Issues?**
- Check logs: `.\deploy.ps1 logs`
- View status: `.\deploy.ps1 status`
- Rebuild: `.\deploy.ps1 build`
- Clean start: `.\deploy.ps1 clean` then `.\deploy.ps1 start`

**Need Help?**
- Review this guide
- Check Docker Desktop logs
- Verify Docker is running
- Ensure ports 8000 and 8501 are available