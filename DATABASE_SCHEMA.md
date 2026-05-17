from fastapi import APIRouter
from app.bob_client import BobClient

router = APIRouter()
bob = BobClient()

@router.post("/ask")
def ask_repo(question: str):
    return bob.query("repo", question)
