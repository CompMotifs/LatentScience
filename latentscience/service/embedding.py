import numpy as np
from scipy.spatial.distance import cosine, euclidean, cityblock
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import logging

from latentscience.model.similarity import SimilarityMethod

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model)
        self.methods = {
            SimilarityMethod.COSINE: self._cosine_similarity,
            SimilarityMethod.EUCLIDEAN: self._euclidean_similarity,
            SimilarityMethod.DOT_PRODUCT: self._dot_product_similarity,
            SimilarityMethod.MANHATTAN: self._manhattan_similarity,
        }

    def calculate_similarity(
        self, embedding1: List[float], embedding2: List[float], method: str = "cosine"
    ) -> float:
        """Task 3: Calculate semantic similarity between embeddings"""
        method_enum = SimilarityMethod(method)
        similarity_func = self.methods[method_enum]
        return similarity_func(embedding1, embedding2)

    def batch_similarity(
        self,
        query_embedding: List[float],
        embeddings: List[List[float]],
        method: str = "cosine",
    ) -> List[float]:
        """Calculate similarity between query and multiple embeddings"""
        query_array = np.array(query_embedding)
        embeddings_array = np.array(embeddings)

        if method == "cosine":
            similarities = cosine_similarity([query_array], embeddings_array)[0]
            return similarities.tolist()

        similarities = []
        for embedding in embeddings:
            sim = self.calculate_similarity(query_embedding, embedding, method)
            similarities.append(sim)
        return similarities

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for given text"""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def batch_generate_embeddings(
        self, texts: List[str], model: str = "text-embedding-ada-002"
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        return 1 - cosine(v1, v2)

    def _euclidean_similarity(self, v1: List[float], v2: List[float]) -> float:
        dist = euclidean(v1, v2)
        return 1 / (1 + dist)  # Convert distance to similarity

    def _dot_product_similarity(self, v1: List[float], v2: List[float]) -> float:
        return np.dot(v1, v2)

    def _manhattan_similarity(self, v1: List[float], v2: List[float]) -> float:
        dist = cityblock(v1, v2)
        return 1 / (1 + dist)
