# Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the AI Engineering and Operations Copilot in various environments, from local development to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Database Setup](#database-setup)
7. [Monitoring & Observability](#monitoring--observability)
8. [Backup & Recovery](#backup--recovery)
9. [Scaling](#scaling)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Requirements**:
- CPU: 4 cores
- RAM: 8 GB
- Disk: 50 GB SSD
- OS: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2

**Recommended for Production**:
- CPU: 8+ cores
- RAM: 16+ GB
- Disk: 100+ GB SSD
- OS: Linux (Ubuntu 22.04 LTS)

### Software Dependencies

- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Python**: 3.11+
- **Node.js**: 18+
- **PostgreSQL**: 15+
- **Redis**: 7+

### External Services

- **LLM Providers**: OpenAI API key, Anthropic API key, or Ollama instance
- **Vector Database**: Qdrant (self-hosted or cloud)
- **Object Storage**: S3-compatible storage (AWS S3, MinIO, etc.)

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-ops-copilot.git
cd ai-ops-copilot
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Required Environment Variables**:

```bash
# Application
APP_NAME=AI Ops Copilot
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=postgresql://aiops:password@localhost:5432/aiops
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Providers (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_BASE_URL=http://localhost:11434

# Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# JWT
JWT_SECRET_KEY=your-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# CORS (for development)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 3. Start Dependencies with Docker Compose

```bash
# Start PostgreSQL, Redis, and Qdrant
docker-compose -f docker-compose.dev.yml up -d

# Verify services are running
docker-compose -f docker-compose.dev.yml ps
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run database migrations
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py

# Start backend server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

### 6. Create Admin User

```bash
cd backend
python scripts/create_admin.py
```

Follow the prompts to create an admin user.

## Docker Deployment

### Development Environment

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production-like Environment

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View service status
docker-compose -f docker-compose.prod.yml ps
```

## Production Deployment

### Architecture Overview

```
                    ┌─────────────┐
                    │   Load      │
                    │   Balancer  │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
       ┌────▼────┐    ┌───▼────┐    ┌───▼────┐
       │ Backend │    │Backend │    │Backend │
       │Instance1│    │Instance2│    │Instance3│
       └────┬────┘    └───┬────┘    └───┬────┘
            │             │              │
            └─────────────┼──────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
    │PostgreSQL│     │  Redis  │     │ Qdrant  │
    │ Primary  │     │ Cluster │     │ Cluster │
    └────┬────┘     └─────────┘     └─────────┘
         │
    ┌────▼────┐
    │PostgreSQL│
    │ Replica  │
    └─────────┘
```

### Option 1: Docker Swarm Deployment

#### 1. Initialize Swarm

```bash
# On manager node
docker swarm init --advertise-addr <MANAGER-IP>

# On worker nodes (use token from init output)
docker swarm join --token <TOKEN> <MANAGER-IP>:2377
```

#### 2. Create Docker Secrets

```bash
# Create secrets for sensitive data
echo "your-secret-key" | docker secret create app_secret_key -
echo "your-jwt-secret" | docker secret create jwt_secret_key -
echo "sk-..." | docker secret create openai_api_key -
echo "postgresql://..." | docker secret create database_url -
```

#### 3. Deploy Stack

```bash
# Deploy the stack
docker stack deploy -c docker-stack.yml aiops

# Check services
docker stack services aiops

# View logs
docker service logs aiops_backend
```

#### 4. Scale Services

```bash
# Scale backend service
docker service scale aiops_backend=5

# Scale frontend service
docker service scale aiops_frontend=3
```

### Option 2: Kubernetes Deployment

#### 1. Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

#### 2. Create Namespace

```bash
kubectl create namespace aiops-copilot
```

#### 3. Create Secrets

```bash
# Create secret for environment variables
kubectl create secret generic aiops-secrets \
  --from-literal=secret-key='your-secret-key' \
  --from-literal=jwt-secret='your-jwt-secret' \
  --from-literal=openai-api-key='sk-...' \
  --from-literal=database-url='postgresql://...' \
  -n aiops-copilot
```

#### 4. Deploy PostgreSQL

```bash
# Add Bitnami repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install PostgreSQL
helm install postgresql bitnami/postgresql \
  --namespace aiops-copilot \
  --set auth.username=aiops \
  --set auth.password=secure-password \
  --set auth.database=aiops \
  --set primary.persistence.size=50Gi \
  --set readReplicas.replicaCount=2
```

#### 5. Deploy Redis

```bash
# Install Redis
helm install redis bitnami/redis \
  --namespace aiops-copilot \
  --set auth.password=secure-password \
  --set master.persistence.size=10Gi \
  --set replica.replicaCount=2
```

#### 6. Deploy Application

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment status
kubectl get pods -n aiops-copilot
kubectl get services -n aiops-copilot
```

#### 7. Configure Ingress

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: aiops-ingress
  namespace: aiops-copilot
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - aiops.example.com
    secretName: aiops-tls
  rules:
  - host: aiops.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

### Option 3: Cloud Provider Deployment

#### AWS Deployment

**Using ECS (Elastic Container Service)**:

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure

# Create ECS cluster
aws ecs create-cluster --cluster-name aiops-copilot

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create service
aws ecs create-service \
  --cluster aiops-copilot \
  --service-name aiops-backend \
  --task-definition aiops-backend:1 \
  --desired-count 3 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

**Using EKS (Elastic Kubernetes Service)**:

```bash
# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Create EKS cluster
eksctl create cluster \
  --name aiops-copilot \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.large \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5 \
  --managed

# Deploy application (use Kubernetes deployment steps above)
```

#### Azure Deployment

**Using AKS (Azure Kubernetes Service)**:

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name aiops-copilot-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group aiops-copilot-rg \
  --name aiops-copilot-aks \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group aiops-copilot-rg --name aiops-copilot-aks

# Deploy application (use Kubernetes deployment steps above)
```

#### GCP Deployment

**Using GKE (Google Kubernetes Engine)**:

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize gcloud
gcloud init

# Create GKE cluster
gcloud container clusters create aiops-copilot \
  --num-nodes=3 \
  --machine-type=n1-standard-4 \
  --region=us-central1

# Get credentials
gcloud container clusters get-credentials aiops-copilot --region=us-central1

# Deploy application (use Kubernetes deployment steps above)
```

## Configuration

### Environment-Specific Configuration

#### Development
```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=*
```

#### Staging
```bash
APP_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=https://staging.example.com
```

#### Production
```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
CORS_ORIGINS=https://aiops.example.com
ENABLE_METRICS=true
ENABLE_TRACING=true
```

### Database Configuration

#### Connection Pooling

```python
# backend/app/config.py
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600
```

#### Read Replicas

```python
# Configure read replica for reporting queries
DATABASE_READ_REPLICA_URL=postgresql://user:pass@replica-host:5432/aiops
```

### Redis Configuration

```bash
# Cluster mode
REDIS_CLUSTER_NODES=redis-1:6379,redis-2:6379,redis-3:6379

# Sentinel mode
REDIS_SENTINEL_HOSTS=sentinel-1:26379,sentinel-2:26379,sentinel-3:26379
REDIS_SENTINEL_MASTER=mymaster
```

## Database Setup

### Initial Migration

```bash
cd backend

# Run migrations
alembic upgrade head

# Verify migration
alembic current
```

### Seed Data

```bash
# Seed initial data
python scripts/seed_data.py

# Create admin user
python scripts/create_admin.py
```

### Backup and Restore

```bash
# Backup database
pg_dump -h localhost -U aiops -d aiops -F c -f backup.dump

# Restore database
pg_restore -h localhost -U aiops -d aiops -c backup.dump
```

## Monitoring & Observability

### Prometheus Metrics

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aiops-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboards

```bash
# Import pre-built dashboards
curl -X POST http://grafana:3000/api/dashboards/import \
  -H "Content-Type: application/json" \
  -d @grafana-dashboard.json
```

### Log Aggregation

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

### Distributed Tracing

```python
# backend/app/main.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider

# Configure tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
```

## Backup & Recovery

### Automated Backups

```bash
# Cron job for daily backups
0 2 * * * /usr/local/bin/backup-database.sh

# backup-database.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U aiops -d aiops -F c -f /backups/aiops_$DATE.dump
aws s3 cp /backups/aiops_$DATE.dump s3://aiops-backups/
find /backups -name "*.dump" -mtime +30 -delete
```

### Disaster Recovery

```bash
# Restore from backup
aws s3 cp s3://aiops-backups/aiops_20240115_020000.dump /tmp/
pg_restore -h localhost -U aiops -d aiops -c /tmp/aiops_20240115_020000.dump

# Verify restoration
psql -h localhost -U aiops -d aiops -c "SELECT COUNT(*) FROM incidents;"
```

## Scaling

### Horizontal Scaling

#### Backend Services

```bash
# Docker Swarm
docker service scale aiops_backend=5

# Kubernetes
kubectl scale deployment backend --replicas=5 -n aiops-copilot
```

#### Database Read Replicas

```bash
# Add read replica
docker run -d \
  --name postgres-replica \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_REPLICATION_MODE=slave \
  -e POSTGRES_MASTER_HOST=postgres-primary \
  postgres:15
```

### Vertical Scaling

```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Auto-scaling

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

```bash
# Check database connectivity
psql -h localhost -U aiops -d aiops -c "SELECT 1;"

# Check connection pool
# In backend logs, look for: "connection pool exhausted"

# Solution: Increase pool size
DATABASE_POOL_SIZE=50
```

#### 2. High Memory Usage

```bash
# Check memory usage
docker stats

# Solution: Adjust resource limits
docker update --memory="4g" --memory-swap="4g" container_name
```

#### 3. Slow API Responses

```bash
# Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

# Solution: Add indexes or optimize queries
```

#### 4. WebSocket Connection Issues

```bash
# Check NGINX configuration
# Ensure WebSocket upgrade headers are set
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database health
pg_isready -h localhost -U aiops

# Redis health
redis-cli ping
```

### Logs

```bash
# View backend logs
docker logs -f aiops-backend

# View database logs
docker logs -f aiops-postgres

# Search logs
docker logs aiops-backend 2>&1 | grep ERROR
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Enable database encryption at rest
- [ ] Set up regular security updates
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Implement network segmentation
- [ ] Regular security audits

## Performance Optimization

### Database Optimization

```sql
-- Create indexes
CREATE INDEX CONCURRENTLY idx_incidents_severity_status 
ON incidents(severity, status);

-- Analyze tables
ANALYZE incidents;

-- Vacuum tables
VACUUM ANALYZE incidents;
```

### Caching Strategy

```python
# Redis caching
CACHE_TTL_SHORT=300  # 5 minutes
CACHE_TTL_MEDIUM=1800  # 30 minutes
CACHE_TTL_LONG=3600  # 1 hour
```

### CDN Configuration

```nginx
# NGINX caching
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Maintenance

### Regular Tasks

- **Daily**: Check logs for errors
- **Weekly**: Review performance metrics
- **Monthly**: Update dependencies
- **Quarterly**: Security audit
- **Annually**: Disaster recovery drill

### Update Procedure

```bash
# 1. Backup database
./scripts/backup-database.sh

# 2. Pull latest code
git pull origin main

# 3. Update dependencies
pip install -r requirements.txt --upgrade

# 4. Run migrations
alembic upgrade head

# 5. Restart services
docker-compose restart backend

# 6. Verify deployment
curl http://localhost:8000/health
```

## Support

For deployment support:
- Documentation: https://docs.aiops-copilot.com/deployment
- Email: devops@aiops-copilot.com
- Slack: #deployment-support