import numpy as np
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any


class EmbeddingRequest(BaseModel):
    text: str = Field(..., min_length=1)
    model: str = Field(default="text-embedding-ada-002")
    paper_id: Optional[str] = None
    embedding_type: str = Field(default="semantic")  # semantic, syntactic, hybrid


class EmbeddingResponse(BaseModel):
    embedding: List[float] = Field(..., min_items=1)
    model: str
    dimensions: int
    paper_id: Optional[str] = None
    embedding_type: str

    @validator("dimensions")
    def validate_dimensions(cls, v, values):
        if "embedding" in values and len(values["embedding"]) != v:
            raise ValueError("Dimensions must match embedding length")
        return v


class StoredEmbedding(BaseModel):
    id: str
    paper_id: str
    embedding: List[float]
    model: str
    dimensions: int
    embedding_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
