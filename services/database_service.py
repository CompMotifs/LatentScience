import os
import json
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, String, Text, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class PaperRecord(Base):
    __tablename__ = "papers"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=False)
    authors = Column(ARRAY(String))
    publication_date = Column(DateTime)
    journal = Column(String)
    doi = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmbeddingRecord(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True)
    paper_id = Column(String, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    model = Column(String, nullable=False)
    dimensions = Column(Integer, nullable=False)
    embedding_type = Column(String, default="semantic")
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseService:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///papers.db")
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(bind=self.engine)
        self.session = SessionLocal()

    def store_paper(self, paper_data: Dict) -> str:
        """Task 5: Store paper in database"""
        paper = PaperRecord(**paper_data)
        self.session.add(paper)
        self.session.commit()
        return paper.id

    def store_embedding(self, embedding_data: Dict) -> str:
        """Store embedding in database"""
        embedding = EmbeddingRecord(**embedding_data)
        self.session.add(embedding)
        self.session.commit()
        return embedding.id

    def get_all_embeddings(self) -> List[Dict]:
        """Get all stored embeddings"""
        embeddings = self.session.query(EmbeddingRecord).all()
        return [
            {
                "paper_id": e.paper_id,
                "embedding": e.embedding,
                "model": e.model,
                "dimensions": e.dimensions,
            }
            for e in embeddings
        ]

    def search_similar_papers(
        self, query_embedding: List[float], threshold: float = 0.7
    ) -> List[Dict]:
        """Search for similar papers based on embedding similarity"""
        # This is a simplified version - in production, use vector databases like Pinecone/Weaviate
        all_embeddings = self.get_all_embeddings()
        # Would implement actual similarity search here
        return all_embeddings[:10]  # Placeholder
