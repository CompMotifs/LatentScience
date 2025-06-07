

import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel


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


# Luna's code
tokenizer = AutoTokenizer.from_pretrained("allenai/specter")
encoder = TFAutoModel.from_pretrained("allenai/specter")

doi_to_vector = {}
def encode_papers(doi_to_title_abs, doi_to_vector):
    papers = [doi_to_title_abs[paper][0] + tokenizer.sep_token + doi_to_title_abs[paper][1] for paper in doi_to_title_abs]
    inputs = tokenizer(papers, padding="max_length", truncation=True, max_length=512, return_tensors="tf")
    results = encoder(**inputs)
    last = results.last_hidden_state[:, 0, :]
    embeds = tf.nn.l2_normalize(last, axis=1) # this is the raw EagerTensor output
    embeds = tf.keras.backend.get_value(embeds)

    counter = 0 # initialise at element 0 of embeds, adds one after processing each paper
    for paper in doi_to_title_abs:
    doi_to_vector[paper] = embeds[counter]
    counter +=1

    return doi_to_vector