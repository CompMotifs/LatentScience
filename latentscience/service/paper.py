import logging
from openai import OpenAI
from latentscience.database.paper import PaperRepository
from latentscience.model.paper import Paper, SimilarPaper
from latentscience.prompts.embedding_prompts import EmbeddingPrompts
from latentscience.service.embedding import EmbeddingService

logger = logging.getLogger(__name__)


class PaperService:
    """Paper Service"""

    def __init__(
        self,
        paper_repo: PaperRepository,
        embedding_service: EmbeddingService,
        openai: OpenAI,
    ):
        self.paper_repo = paper_repo
        self.embedding_service = embedding_service
        self.openai = openai
        self.prompts = EmbeddingPrompts()

    async def find_similar_papers(
        self, query: str, abstract: str
    ) -> list[SimilarPaper]:
        """Find similar papers based on the given paper ID."""
        search_query = f"{query}\n\nAbstract: {abstract}"
        embedding = self.embedding_service.generate_embedding(search_query)
        similar_papers = await self.paper_repo.find_similar_papers(embedding)
        return similar_papers

    def rephrase_for_embedding(self, paper_text: str, research_question: str) -> str:
        """Task 2: Rephrase input paper and research question for better embeddings"""
        prompt = self.prompts.get_rephrasing_prompt(paper_text, research_question)

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
            )
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("No valid rewponse from the LLM API")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error rephrasing text: {e}")
            return f"{paper_text}\n\nResearch focus: {research_question}"

    def generate_embedding(
        self, text: str, model: str = "text-embedding-ada-002"
    ) -> list[float]:
        """Generate embedding for given text"""
        try:
            response = self.openai.embeddings.create(model=model, input=text)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def batch_generate_embeddings(
        self, texts: list[str], model: str = "text-embedding-ada-002"
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text, model)
            embeddings.append(embedding)
        return embeddings
