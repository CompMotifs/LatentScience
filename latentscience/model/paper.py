from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PaperStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


class Paper(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=500)
    abstract: str = Field(..., min_length=10)
    field: str = Field(..., min_length=1, max_length=100)
    embedding: list[float] = Field(...)


class SimilarPaper(BaseModel):
    paper: Paper
    similarity_score: float = Field(..., ge=0.0, le=1.0)


class PaperSearchRequest(BaseModel):
    query: str
    abstract: str
    max_results: int = Field(default=10, ge=1, le=50)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class PaperSearchResponse(BaseModel):
    papers: list[SimilarPaper] = Field(..., min_length=1)
    top_paper_comparison: str
