version: '3.8'

services:
  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: bob-backend
    ports:
      - "8000:8000"
    environment:
      - APP_NAME=IBM Bob Copilot
      - APP_ENV=development
      - DEBUG=true
      - BACKEND_URL=http://localhost:8000
    volumes:
      - ./app:/app/app
      - ./bob_evidence:/app/bob_evidence
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - bob-network
    restart: unless-stopped

  # Streamlit Frontend
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: bob-frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    volumes:
      - ./frontend:/app/frontend
    command: streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - bob-network
    restart: unless-stopped

networks:
  bob-network:
    driver: bridge

volumes:
  bob-data:
    driver: local

# Made with Bob
