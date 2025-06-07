import numpy as np
from typing import List, Dict, Tuple
from scipy.spatial.distance import cosine, euclidean, cityblock
from sklearn.metrics.pairwise import cosine_similarity
from app.models.similarity import SimilarityResult, SimilarityMethod, SimilarityBatch
import logging

logger = logging.getLogger(__name__)

class SimilarityService(nn.CosineSimilarity):
    def __init__(self, top_choices=0, dim=1, eps=1e-6):
        super(SimilarityService, self).__init__(dim=dim, eps=eps)
        self.top_choices = top_choices
    
    def forward(self, query, database):
        similarity = F.cosine_similarity(query, database, self.dim, self.eps)
        descending_idx = torch.argsort(similarity, descending=True)

        if self.top_choices:
            top_picks_idx = descending_idx[:self.top_choices]
            top_picks = database_emb[top_picks_idx]
            return top_picks, top_picks_idx
        else:
            return database_emb[descending_idx], descending_idx

class SimilarityService:
    def __init__(self):
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

    def find_most_similar(
        self, query_embedding: List[float], embeddings: List[Dict], top_k: int = 10
    ) -> List[Dict]:
        """Find top-k most similar papers"""
        embedding_vectors = [item["embedding"] for item in embeddings]
        similarities = self.batch_similarity(query_embedding, embedding_vectors)

        # Combine similarities with paper data
        results = []
        for i, (similarity, paper_data) in enumerate(zip(similarities, embeddings)):
            results.append(
                {
                    "paper_id": paper_data["paper_id"],
                    "similarity": similarity,
                    "paper_data": paper_data,
                }
            )

        # Sort by similarity and return top-k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

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
