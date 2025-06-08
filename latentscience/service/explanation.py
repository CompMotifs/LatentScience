import openai
import os
from typing import Dict, List
from latentscience.model.paper import Paper, PaperSearchRequest, SimilarPaper
from prompts.explanation_prompts import ExplanationPrompts
import logging

logger = logging.getLogger(__name__)


class ExplanationService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompts = ExplanationPrompts()

    async def explain_connection(
        self, request: PaperSearchRequest, paper: SimilarPaper
    ) -> str:
        """Task 4: Generate explanation for link between papers"""
        prompt = self.prompts.get_explanation_prompt(
            request, paper.paper, paper.similarity_score
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("No valid rewponse from the LLM API")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Papers are connected with {paper.similarity_score:.2f} similarity based on semantic analysis."

    def batch_explain_connections(
        self, query_paper: Dict, similar_papers: List[Dict]
    ) -> List[Dict]:
        """Generate explanations for multiple paper connections"""
        explanations = []
        for paper_data in similar_papers:
            explanation = self.explain_connection(
                query_paper, paper_data["paper_data"], paper_data["similarity"]
            )
            explanations.append(
                {
                    "paper_id": paper_data["paper_id"],
                    "similarity": paper_data["similarity"],
                    "explanation": explanation,
                    "paper_data": paper_data["paper_data"],
                }
            )
        return explanations
