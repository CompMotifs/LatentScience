from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.paper import PaperSearchRequest
from services.embedding_service import EmbeddingService
from services.database_service import DatabaseService
from services.explanation_service import ExplanationService
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def create_api_app() -> FastAPI:
    api = FastAPI(title="LatentScience API", version="1.0.0")

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
            # Mock papers related to the research question
            # TODO: Replace with actual database search logic
            mock_papers = [
                {
                    "title": "Machine Learning Applications in Genomics",
                    "abstract": "This paper explores the application of deep learning techniques to genomic data analysis, focusing on pattern recognition in DNA sequences and protein structure prediction.",
                    "similarity": 0.85,
                    "explanation": "Shares similar AI/ML methodologies with your research focus.",
                },
                {
                    "title": "Neural Networks for Scientific Discovery",
                    "abstract": "A comprehensive review of how artificial neural networks are accelerating scientific breakthroughs across multiple disciplines including physics, chemistry, and biology.",
                    "similarity": 0.78,
                    "explanation": "Related through computational approaches to scientific problems.",
                },
                {
                    "title": "Computational Methods in Modern Research",
                    "abstract": "This work presents novel computational frameworks for analyzing complex scientific data, with applications in climate modeling, drug discovery, and materials science.",
                    "similarity": 0.72,
                    "explanation": "Connected through computational and analytical methodologies.",
                },
            ]

            # 1. Generate embedding for the input paper/query
            embedding_service = EmbeddingService()
            query_embedding = await embedding_service.generate_embedding.remote(
                request.paper.abstract + " " + request.research_question.question
            )

            # 2. Search for similar papers in your database
            db_service = DatabaseService()
            similar_papers = await db_service.search_similar_papers.remote(
                query_embedding, request.similarity_threshold
            )

            # 3. Generate explanations for the connections
            explanation_service = ExplanationService()
            explanations = await explanation_service.batch_explain_connections.remote(
                request.paper.dict(), similar_papers
            )

            # TODO: Return actual papers insetad of mock data
            return mock_papers

        except Exception as e:
            logger.error(f"Error in search_similar_papers: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @api.get("/api/health")
    async def health_check():
        return {"status": "healthy", "service": "paper-links-api"}

    return api
