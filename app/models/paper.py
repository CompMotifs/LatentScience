from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class PaperStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


class Paper(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=500)
    abstract: str = Field(..., min_length=10)
    authors: List[str] = Field(default_factory=list)
    publication_date: Optional[datetime] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    status: PaperStatus = PaperStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class ResearchQuestion(BaseModel):
    question: str = Field(..., min_length=10, max_length=1000)
    context: Optional[str] = None
    focus_areas: List[str] = Field(default_factory=list)


class PaperSearchRequest(BaseModel):
    paper: Paper
    research_question: ResearchQuestion
    max_results: int = Field(default=10, ge=1, le=50)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
