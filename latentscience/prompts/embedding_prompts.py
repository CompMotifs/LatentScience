class EmbeddingPrompts:
    def get_rephrasing_prompt(self, paper_text: str, research_question: str) -> str:
        """Task 2: Prompt for rephrasing paper and research question"""
        return f"""
You are a research assistant helping to optimize text for semantic similarity search.
Your task is to rephrase and combine the given paper content and research question 
to create a more focused, searchable text that will work better for embedding generation.

Paper Content:
{paper_text}

Research Question:
{research_question}

Please create a concise, well-structured text that:
1. Combines the key concepts from both the paper and research question
2. Emphasizes the main research themes and methodologies
3. Includes important domain-specific terminology
4. Maintains the semantic meaning while improving searchability

Output a single paragraph of 150-300 words that would be optimal for finding related papers.
"""

    def get_context_enhancement_prompt(self, paper_title: str, abstract: str) -> str:
        """Enhance paper context for better embedding"""
        return f"""
Enhance this research paper's context for better semantic search matching:

Title: {paper_title}
Abstract: {abstract}

Please expand this into a comprehensive research summary that includes:
- Key research domains and methodologies
- Potential applications and implications
- Related fields and interdisciplinary connections
- Technical approaches and innovations

Keep it focused and under 400 words.
"""
