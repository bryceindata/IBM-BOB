# API Specification

## Overview

The AI Engineering and Operations Copilot exposes a RESTful API with WebSocket support for real-time updates. This document provides comprehensive API specifications including endpoints, request/response formats, authentication, and error handling.

## Base URL

```
Development: http://localhost:8000
Production: https://api.aiops-copilot.com
```

## API Versioning

All API endpoints are versioned using URL path versioning:

```
/api/v1/*
```

## Authentication

### JWT Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Obtaining a Token

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Refreshing a Token

**Endpoint**: `POST /api/v1/auth/refresh`

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Common Response Formats

### Success Response

```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* additional error details */ }
  }
}
```

### Paginated Response

```json
{
  "success": true,
  "data": [ /* array of items */ ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Authentication required or token invalid |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## Rate Limiting

- **Default**: 100 requests per minute per user
- **Burst**: 200 requests per minute
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests per window
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Unix timestamp when the limit resets

## API Endpoints

### 1. Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
```

**Request**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Get Current User
```http
GET /api/v1/auth/me
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "roles": ["engineer"],
    "is_active": true,
    "last_login_at": "2024-01-15T10:30:00Z"
  }
}
```

### 2. Incident Endpoints

#### List Incidents
```http
GET /api/v1/incidents
```

**Query Parameters**:
- `page` (integer, default: 1): Page number
- `page_size` (integer, default: 20): Items per page
- `severity` (string): Filter by severity (critical, high, medium, low)
- `status` (string): Filter by status (open, investigating, resolved, closed)
- `assigned_to` (uuid): Filter by assigned user
- `from_date` (ISO 8601): Filter incidents after this date
- `to_date` (ISO 8601): Filter incidents before this date
- `search` (string): Search in title and description

**Response**: `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "High latency in payment service",
      "description": "Users reporting slow payment processing",
      "severity": "high",
      "status": "investigating",
      "source": "prometheus",
      "detected_at": "2024-01-15T10:00:00Z",
      "assigned_to": {
        "id": "uuid",
        "username": "johndoe",
        "full_name": "John Doe"
      },
      "affected_systems": [
        {
          "id": "uuid",
          "name": "payment-service",
          "type": "service"
        }
      ],
      "tags": ["payment", "latency"],
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 45,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Incident Details
```http
GET /api/v1/incidents/{incident_id}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "High latency in payment service",
    "description": "Users reporting slow payment processing",
    "severity": "high",
    "status": "investigating",
    "source": "prometheus",
    "detected_at": "2024-01-15T10:00:00Z",
    "acknowledged_at": "2024-01-15T10:05:00Z",
    "resolved_at": null,
    "root_cause": "Database connection pool exhaustion",
    "root_cause_confidence": 0.87,
    "remediation_steps": [
      {
        "step": 1,
        "action": "Scale payment service to 5 replicas",
        "status": "completed"
      },
      {
        "step": 2,
        "action": "Increase DB connection pool size",
        "status": "pending"
      }
    ],
    "assigned_to": {
      "id": "uuid",
      "username": "johndoe",
      "full_name": "John Doe"
    },
    "affected_systems": [
      {
        "id": "uuid",
        "name": "payment-service",
        "type": "service",
        "environment": "production"
      }
    ],
    "metadata": {
      "alert_id": "alert-123",
      "runbook_url": "https://wiki.example.com/runbooks/payment-latency"
    },
    "tags": ["payment", "latency"],
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Create Incident
```http
POST /api/v1/incidents
```

**Request**:
```json
{
  "title": "High latency in payment service",
  "description": "Users reporting slow payment processing",
  "severity": "high",
  "source": "manual",
  "detected_at": "2024-01-15T10:00:00Z",
  "affected_system_ids": ["uuid1", "uuid2"],
  "tags": ["payment", "latency"],
  "metadata": {
    "reporter": "customer-support"
  }
}
```

**Response**: `201 Created`

#### Update Incident
```http
PUT /api/v1/incidents/{incident_id}
```

**Request**:
```json
{
  "status": "resolved",
  "root_cause": "Database connection pool exhaustion",
  "resolved_at": "2024-01-15T11:00:00Z"
}
```

**Response**: `200 OK`

#### Analyze Incident (Root Cause Analysis)
```http
POST /api/v1/incidents/{incident_id}/analyze
```

**Request**:
```json
{
  "include_historical": true,
  "time_window_hours": 24
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "root_cause": "Database connection pool exhaustion due to increased traffic",
    "confidence": 0.87,
    "reasoning": "Analysis of metrics shows...",
    "similar_incidents": [
      {
        "id": "uuid",
        "title": "Payment service latency",
        "similarity_score": 0.92,
        "resolution": "Scaled service and increased connection pool"
      }
    ],
    "remediation_suggestions": [
      {
        "action": "Scale payment service to 5 replicas",
        "priority": "high",
        "estimated_impact": "Immediate relief"
      },
      {
        "action": "Increase DB connection pool from 20 to 50",
        "priority": "high",
        "estimated_impact": "Prevent future occurrences"
      }
    ],
    "analysis_metadata": {
      "model_used": "gpt-4",
      "analysis_duration_ms": 2340,
      "data_sources": ["prometheus", "logs", "historical_incidents"]
    }
  }
}
```

#### Get Incident Timeline
```http
GET /api/v1/incidents/{incident_id}/timeline
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "event_type": "created",
      "event_data": {
        "severity": "high"
      },
      "actor": {
        "id": "uuid",
        "username": "system",
        "type": "system"
      },
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "id": "uuid",
      "event_type": "status_changed",
      "event_data": {
        "from": "open",
        "to": "investigating"
      },
      "actor": {
        "id": "uuid",
        "username": "johndoe",
        "type": "user"
      },
      "timestamp": "2024-01-15T10:05:00Z"
    }
  ]
}
```

### 3. System Endpoints

#### List Systems
```http
GET /api/v1/systems
```

**Query Parameters**:
- `page`, `page_size`: Pagination
- `type`: Filter by type (service, database, queue, etc.)
- `environment`: Filter by environment (production, staging, etc.)
- `health_status`: Filter by health status
- `search`: Search in name and description

**Response**: `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "payment-service",
      "type": "service",
      "environment": "production",
      "description": "Handles payment processing",
      "health_status": "healthy",
      "last_health_check": "2024-01-15T10:30:00Z",
      "tags": ["payment", "critical"],
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": { /* ... */ }
}
```

#### Get System Details
```http
GET /api/v1/systems/{system_id}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "payment-service",
    "type": "service",
    "environment": "production",
    "description": "Handles payment processing",
    "repository_url": "https://github.com/org/payment-service",
    "documentation_url": "https://docs.example.com/payment-service",
    "health_status": "healthy",
    "health_check_url": "https://payment-service.example.com/health",
    "last_health_check": "2024-01-15T10:30:00Z",
    "configuration": {
      "replicas": 3,
      "cpu_limit": "2000m",
      "memory_limit": "4Gi"
    },
    "metadata": {
      "team": "payments",
      "on_call": "payments-oncall@example.com"
    },
    "tags": ["payment", "critical"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

#### Get System Dependencies
```http
GET /api/v1/systems/{system_id}/dependencies
```

**Query Parameters**:
- `direction`: "upstream" or "downstream" (default: both)
- `depth`: Maximum depth to traverse (default: 3)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "system": {
      "id": "uuid",
      "name": "payment-service"
    },
    "dependencies": {
      "upstream": [
        {
          "id": "uuid",
          "name": "api-gateway",
          "type": "service",
          "dependency_type": "api",
          "is_critical": true
        }
      ],
      "downstream": [
        {
          "id": "uuid",
          "name": "payment-db",
          "type": "database",
          "dependency_type": "data",
          "is_critical": true
        },
        {
          "id": "uuid",
          "name": "notification-service",
          "type": "service",
          "dependency_type": "async",
          "is_critical": false
        }
      ]
    },
    "graph": {
      "nodes": [ /* graph nodes */ ],
      "edges": [ /* graph edges */ ]
    }
  }
}
```

#### Query Systems (Natural Language)
```http
POST /api/v1/systems/query
```

**Request**:
```json
{
  "query": "What services depend on the payment database?",
  "include_context": true
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "answer": "The payment database has 3 direct dependencies: payment-service, billing-service, and analytics-service. The payment-service is the most critical dependency as it handles real-time payment processing.",
    "systems": [
      {
        "id": "uuid",
        "name": "payment-service",
        "relevance_score": 0.95
      }
    ],
    "context": {
      "query_type": "dependency_analysis",
      "confidence": 0.92
    }
  }
}
```

#### Get System Health
```http
GET /api/v1/systems/{system_id}/health
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "checks": [
      {
        "name": "http_endpoint",
        "status": "passing",
        "last_check": "2024-01-15T10:30:00Z"
      },
      {
        "name": "database_connection",
        "status": "passing",
        "last_check": "2024-01-15T10:30:00Z"
      }
    ],
    "metrics": {
      "cpu_usage": 45.2,
      "memory_usage": 62.8,
      "request_rate": 1250.5,
      "error_rate": 0.02
    }
  }
}
```

### 4. Workflow Endpoints

#### List Workflows
```http
GET /api/v1/workflows
```

**Query Parameters**:
- `page`, `page_size`: Pagination
- `trigger_type`: Filter by trigger type
- `is_active`: Filter by active status
- `search`: Search in name and description

**Response**: `200 OK`

#### Get Workflow Details
```http
GET /api/v1/workflows/{workflow_id}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Auto-scale on high latency",
    "description": "Automatically scale services when latency exceeds threshold",
    "trigger_type": "event",
    "trigger_config": {
      "event_type": "metric_threshold",
      "metric": "http_request_duration_p95",
      "threshold": 1000,
      "duration_minutes": 5
    },
    "is_active": true,
    "requires_approval": false,
    "steps": [
      {
        "id": "uuid",
        "step_order": 1,
        "name": "Check current replica count",
        "action_type": "kubernetes.get_replicas",
        "action_config": {
          "service": "payment-service"
        }
      },
      {
        "id": "uuid",
        "step_order": 2,
        "name": "Scale service",
        "action_type": "kubernetes.scale",
        "action_config": {
          "service": "payment-service",
          "replicas": 5
        }
      }
    ],
    "created_by": {
      "id": "uuid",
      "username": "johndoe"
    },
    "tags": ["auto-scaling", "performance"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
}
```

#### Create Workflow
```http
POST /api/v1/workflows
```

**Request**:
```json
{
  "name": "Auto-scale on high latency",
  "description": "Automatically scale services when latency exceeds threshold",
  "trigger_type": "event",
  "trigger_config": {
    "event_type": "metric_threshold",
    "metric": "http_request_duration_p95",
    "threshold": 1000
  },
  "requires_approval": false,
  "steps": [
    {
      "step_order": 1,
      "name": "Scale service",
      "action_type": "kubernetes.scale",
      "action_config": {
        "service": "payment-service",
        "replicas": 5
      }
    }
  ],
  "tags": ["auto-scaling"]
}
```

**Response**: `201 Created`

#### Execute Workflow
```http
POST /api/v1/workflows/{workflow_id}/execute
```

**Request**:
```json
{
  "trigger_data": {
    "incident_id": "uuid",
    "reason": "Manual execution for testing"
  }
}
```

**Response**: `202 Accepted`
```json
{
  "success": true,
  "data": {
    "execution_id": "uuid",
    "workflow_id": "uuid",
    "status": "running",
    "started_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Get Workflow Executions
```http
GET /api/v1/workflows/{workflow_id}/executions
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "workflow_id": "uuid",
      "status": "completed",
      "triggered_by": {
        "id": "uuid",
        "username": "johndoe"
      },
      "started_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:32:15Z",
      "result": {
        "steps_completed": 2,
        "steps_failed": 0
      }
    }
  ],
  "pagination": { /* ... */ }
}
```

### 5. Chat Endpoints

#### Send Chat Message
```http
POST /api/v1/chat/message
```

**Request**:
```json
{
  "session_id": "uuid",
  "message": "What's causing the high latency in the payment service?",
  "context": {
    "incident_id": "uuid"
  }
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "message_id": "uuid",
    "response": "Based on the analysis, the high latency is caused by database connection pool exhaustion. The payment service is experiencing 300% more traffic than usual, and the connection pool is at 95% utilization.",
    "suggestions": [
      "Scale payment service to 5 replicas",
      "Increase DB connection pool size",
      "Enable query caching"
    ],
    "context": {
      "systems_analyzed": ["payment-service", "payment-db"],
      "confidence": 0.87
    }
  }
}
```

#### Get Chat History
```http
GET /api/v1/chat/history
```

**Query Parameters**:
- `session_id`: Filter by session
- `limit`: Number of messages to return (default: 50)

**Response**: `200 OK`

### 6. Integration Endpoints

#### List Integrations
```http
GET /api/v1/integrations
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "Production Prometheus",
      "type": "prometheus",
      "category": "observability",
      "is_enabled": true,
      "last_sync_at": "2024-01-15T10:30:00Z",
      "last_sync_status": "success",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Configure Integration
```http
POST /api/v1/integrations/{type}/configure
```

**Request** (Prometheus example):
```json
{
  "name": "Production Prometheus",
  "configuration": {
    "url": "https://prometheus.example.com",
    "api_key": "encrypted_key"
  }
}
```

**Response**: `201 Created`

#### Test Integration
```http
POST /api/v1/integrations/{type}/test
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "status": "success",
    "message": "Successfully connected to Prometheus",
    "details": {
      "version": "2.45.0",
      "metrics_available": 1250
    }
  }
}
```

## WebSocket Endpoints

### Real-time Incident Updates
```
WS /ws/incidents
```

**Subscribe Message**:
```json
{
  "action": "subscribe",
  "filters": {
    "severity": ["critical", "high"],
    "status": ["open", "investigating"]
  }
}
```

**Event Message**:
```json
{
  "event": "incident.created",
  "data": {
    "id": "uuid",
    "title": "High latency in payment service",
    "severity": "high",
    "status": "open"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Real-time Chat
```
WS /ws/chat/{session_id}
```

**Message Format**:
```json
{
  "type": "message",
  "content": "What's the status of incident INC-123?",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Webhooks

### Webhook Configuration

Configure webhooks to receive notifications for specific events.

**Endpoint**: `POST /api/v1/webhooks`

**Request**:
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["incident.created", "incident.resolved"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload

```json
{
  "event": "incident.created",
  "data": {
    "id": "uuid",
    "title": "High latency in payment service",
    "severity": "high"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "signature": "sha256=..."
}
```

## SDK Examples

### Python SDK

```python
from aiops_copilot import Client

client = Client(
    base_url="https://api.aiops-copilot.com",
    api_key="your_api_key"
)

# List incidents
incidents = client.incidents.list(
    severity="high",
    status="open"
)

# Analyze incident
analysis = client.incidents.analyze(
    incident_id="uuid",
    include_historical=True
)

# Execute workflow
execution = client.workflows.execute(
    workflow_id="uuid",
    trigger_data={"reason": "Manual execution"}
)
```

### JavaScript/TypeScript SDK

```typescript
import { AIOpsClient } from '@aiops-copilot/sdk';

const client = new AIOpsClient({
  baseUrl: 'https://api.aiops-copilot.com',
  apiKey: 'your_api_key'
});

// List incidents
const incidents = await client.incidents.list({
  severity: 'high',
  status: 'open'
});

// Analyze incident
const analysis = await client.incidents.analyze('uuid', {
  includeHistorical: true
});

// Execute workflow
const execution = await client.workflows.execute('uuid', {
  triggerData: { reason: 'Manual execution' }
});
```

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```python
try:
    incident = client.incidents.get(incident_id)
except NotFoundError:
    print("Incident not found")
except RateLimitError:
    print("Rate limit exceeded, retry after delay")
except APIError as e:
    print(f"API error: {e.message}")
```

### 2. Pagination

Use pagination for large result sets:

```python
page = 1
while True:
    incidents = client.incidents.list(page=page, page_size=100)
    process_incidents(incidents.data)
    
    if not incidents.pagination.has_next:
        break
    page += 1
```

### 3. Webhooks Security

Verify webhook signatures:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

### 4. Rate Limiting

Implement exponential backoff:

```python
import time

def make_request_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

## Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- Core endpoints for incidents, systems, workflows
- WebSocket support for real-time updates
- JWT authentication

## Support

For API support:
- Documentation: https://docs.aiops-copilot.com
- Email: api-support@aiops-copilot.com
- GitHub Issues: https://github.com/org/aiops-copilot/issues