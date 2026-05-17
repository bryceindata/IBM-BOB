from fastapi import FastAPI
from app.routes.repo_brain import router as repo_router
from app.routes.incident import router as incident_router
from app.routes.workflow import router as workflow_router

app = FastAPI(title="IBM Bob Intelligent Copilot v2")

app.include_router(repo_router, prefix="/repo")
app.include_router(incident_router, prefix="/incident")
app.include_router(workflow_router, prefix="/workflow")

@app.get("/")
def root():
    return {"status": "IBM Bob Copilot v2 running"}
