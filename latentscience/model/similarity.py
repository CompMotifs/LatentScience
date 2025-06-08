from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class SimilarityMethod(str, Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"
    MANHATTAN = "manhattan"


class SimilarityResult(BaseModel):
    paper_a_id: str
    paper_b_id: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    method: SimilarityMethod
    explanation: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SimilarityBatch(BaseModel):
    query_paper_id: str
    results: List[SimilarityResult]
    method: SimilarityMethod
    threshold: float
    total_comparisons: int
    execution_time: Optional[float] = None


class LinkExplanation(BaseModel):
    paper_a_id: str
    paper_b_id: str
    similarity_score: float
    explanation: str = Field(..., min_length=50)
    key_connections: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
