from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.models.paper import PaperSearchRequest, Paper
from app.models.embedding import EmbeddingRequest
from app.models.similarity import SimilarityBatch
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def create_api_app() -> FastAPI:
    api = FastAPI(title="Paper Links API", version="1.0.0")

    # Add CORS middleware
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.post("/api/search-papers", response_model=List[Dict])
    async def search_similar_papers(request: PaperSearchRequest):
        """Main endpoint for finding similar papers"""
        try:
            # This would integrate with your Modal services
            # For now, returning a mock response
            return [
                {
                    "paper_id": "paper_123",
                    "title": "Related Research Paper",
                    "similarity": 0.85,
                    "explanation": "This paper shares similar methodologies and research focus.",
                }
            ]
        except Exception as e:
            logger.error(f"Error in search_similar_papers: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @api.post("/api/generate-embedding")
    async def generate_embedding(request: EmbeddingRequest):
        """Generate embedding for given text"""
        try:
            # Integration with Modal EmbeddingService
            return {"embedding": [0.1] * 1536, "model": request.model}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @api.get("/api/health")
    async def health_check():
        return {"status": "healthy", "service": "paper-links-api"}

    return api
