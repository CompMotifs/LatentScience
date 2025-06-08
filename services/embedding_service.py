import openai
import os
from typing import List
from prompts.embedding_prompts import EmbeddingPrompts
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompts = EmbeddingPrompts()

    def rephrase_for_embedding(self, paper_text: str, research_question: str) -> str:
        """Task 2: Rephrase input paper and research question for better embeddings"""
        prompt = self.prompts.get_rephrasing_prompt(paper_text, research_question)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error rephrasing text: {e}")
            return f"{paper_text}\n\nResearch focus: {research_question}"

    def generate_embedding(
        self, text: str, model: str = "text-embedding-ada-002"
    ) -> List[float]:
        """Generate embedding for given text"""
        try:
            response = self.client.embeddings.create(model=model, input=text)
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def batch_generate_embeddings(
        self, texts: List[str], model: str = "text-embedding-ada-002"
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text, model)
            embeddings.append(embedding)
        return embeddings
