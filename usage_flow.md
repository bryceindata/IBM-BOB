from fastapi import APIRouter
from app.bob_client import BobClient

router = APIRouter()
bob = BobClient()

@router.post("/analyze")
def analyze(log: str):
    return bob.query("incident", log)
