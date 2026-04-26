from fastapi import APIRouter
from services.rag_service import search_resumes

router = APIRouter()

@router.get("/search")
def search(query: str):
    results = search_resumes(query)
    return {
        "query": query,
        "results": results
    }