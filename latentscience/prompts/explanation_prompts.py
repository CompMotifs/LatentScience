from latentscience.model.paper import Paper, PaperSearchRequest


class ExplanationPrompts:
    def get_explanation_prompt(
        self, request: PaperSearchRequest, paper: Paper, similarity_score: float
    ) -> str:
        """Task 4: Prompt for explaining connections between papers"""
        return f"""
You are a research analyst explaining connections between academic papers.
Analyze the relationship between these two papers and provide a clear explanation.

Paper 1:
Abstract: {request.abstract}

Paper 2:
Abstract: {paper.abstract}

Similarity Score: {similarity_score:.3f}

Please provide a detailed explanation that covers:
1. The main conceptual connections between these papers
2. Shared methodologies, theories, or approaches
3. How one paper might inform or build upon the other
4. Potential areas for cross-pollination of ideas
5. Why a researcher interested in Paper 1 should care about Paper 2

Write a clear, informative explanation in 2-3 paragraphs.
"""

    def get_batch_explanation_prompt(
        self, query_paper: dict, similar_papers: list
    ) -> str:
        """Generate explanations for multiple paper connections"""
        papers_text = ""
        for i, paper in enumerate(similar_papers, 1):
            papers_text += f"""
Paper {i} (Similarity: {paper["similarity"]:.3f}):
Title: {paper["paper_data"].get("title", "Unknown")}
Abstract: {paper["paper_data"].get("abstract", "Not available")[:200]}...
"""

        return f"""
You are a research analyst explaining how multiple papers relate to a query paper.

Query Paper:
Title: {query_paper.get("title", "Unknown")}
Abstract: {query_paper.get("abstract", "Not available")}

Related Papers:
{papers_text}

For each related paper, provide a brief but insightful explanation of:
1. The key connection to the query paper
2. What makes this paper relevant
3. How it could inform future research

Keep each explanation to 1-2 sentences, focusing on the most important connections.
"""
