

# First, ensure you have the necessary library installed:
# pip install sentence-transformers numpy

import numpy as np
from sentence_transformers import SentenceTransformer
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel
from prompts.claude_llm import get_claude_layman

class Simplify():
    def __init__(self, layman_prompt):
        self.layman_prompt = layman_prompt

    def get_query_layman(self, abstract, query):
        return get_claude_layman(abstract, query, self.layman_prompt)

    def get_database_layman(self, csv_path, query):
        """
        Convert all the abstracts in the database into Layman Terms.

        Args:
            csv_path: The path to the csv file containing all the papers
            query: The user input query

        Returns:
            List of Raw Responses from the LLM service
        """
        list_of_laymans = []
        
        with open(csv_path, mode="r", encoding="utf-8", newline="") as files:
            reader = csv.reader(files)
            next(reader)
            for row in reader:
                abstract = row[1]
                layman = get_claude_layman(abstract, query, self.layman_prompt)
                list_of_laymans.append(layman)

class EmbeddingPrompts:
    def get_rephrasing_prompt(self, paper_text: str, research_question: str) -> str:
        """Task 1: Prompt for rephrasing paper and research question"""
        return f"""
    You are a research assistant helping to optimize text for semantic similarity search.
    Your task is to rephrase and combine the given paper content and research question 
    to create a more focused, searchable text that will work better for embedding generation.

    Please create a concise, well-structured text that:
    1. Combines the key concepts from both the paper and research question
    2. Emphasizes the main research themes and methodologies
    3. Includes important domain-specific terminology
    4. Maintains the semantic meaning while improving searchability

    Output a single paragraph of 150-300 words that would be optimal for finding related papers.
    
    Paper Content:
    {paper_text}

    Research Question:
    {research_question}
    """

    def get_context_enhancement_prompt(self, paper_title: str, abstract: str) -> str:
        """Task 2: Enhance paper context for better embedding"""
        return f"""
    Enhance this research paper's context for better semantic search matching:

    Please expand this into a comprehensive research summary that includes:
    - Key research domains and methodologies
    - Potential applications and implications
    - Related fields and interdisciplinary connections
    - Technical approaches and innovations

    Keep it focused and under 400 words.
    
    Title: {paper_title}
    Abstract: {abstract}
    """
    
    def get_challenges_summary_prompt(self, paper_title: str, abstract: str) -> str:
        """Task 3: Summarize key challenges of the paper for embedding"""
        return f"""I'm providing you with a scientific paper. 
    Please identify every challenge encountered in the paper. 
    For each item you identify, provide a detailed but simple explanation 
    focusing on how it works and the goal of its use. 
    Make the explanation as simple as possible and use the most general term for every word.
    
    Title: {paper_title}
    Abstract: {abstract}
    """
    
    def get_comparison_prompt(self, paper):
        return f"""Take the descriptions of challenges in two 
    different papers and highlight similarities between them. 
    The goal is to find common areas in disparate research fields 
    that have the same goals or use the methodologies or concepts, 
    but where this is not obvious. 
    
    Output your analysis as a json 
    file. The fields should be "cross_disciplinary_commonalities", 
    "research_fields", and "meta_analysis". Within the cross_disciplinary_commonalities 
    field, list your similarities as sub-fields named as the commonalities, 
    with each commonality subdivided as “description” (state the link), 
    "source" (theme in the first input), "target" (theme in the second input), 
    “common_insight” (explain the link). Within "research_fields" state the 
    "source_field" and "target_field" research fields. Within "meta_analysis", 
    analyse in terms of "cross_disciplinary_potential”, "methodological_overlap”, 
    "universal_principles”, “structural_analogies”, “Cross_cutting_themes”, 
    and “shared_concepts”, where applicable.
    """


    
class Paper:
    """
    A class to represent a scientific paper with its title, abstract, and DOI.
    
    Attributes:
        title (str): The title of the paper.
        abstract (str): The abstract of the paper.
        doi (str): The Digital Object Identifier of the paper.
    """

    def __init__(self, title: str, abstract: str, doi: str = None):
        self.title = title
        self.abstract = abstract
        self.doi = doi


class PaperEmbedder:
    """
    A class to generate LLM embeddings for scientific paper titles and abstracts.

    It uses a pre-trained Sentence Transformer model to convert text into
    dense vector representations.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the PaperEmbedder with a specified Sentence Transformer model.

        Args:
            model_name (str): The name of the pre-trained model to load from
                              Hugging Face Model Hub.
                              Examples: 'all-MiniLM-L6-v2', 'multi-qa-MiniLM-L6-cos-v1',
                              'malteos/scincl'
                              or domain-specific models like 'allenai/specter' (if compatible
                              and available via Sentence Transformers).
        """
        try:
            # Load the pre-trained Sentence Transformer model.
            # This model converts sentences/paragraphs into a 384-dimensional dense vector space.
            self.model = SentenceTransformer(model_name)
            print(f"Model '{model_name}' loaded successfully.")
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            print("Please ensure the model name is correct and you have an internet connection.")
            raise

    def get_embedding(self, texts: Union[str, List[str]]):
        """
        Compute embeddings for a single string or a list of strings.

        Args:
          texts: Either one string or a list of strings.
        
        Returns:
          A 2D numpy array of shape (n_texts, embedding_dim).
          If a single string is passed, you'll still get shape (1, dim).
        """
        if isinstance(texts, str):
          texts = [texts]        
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        if self.normalize:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / np.clip(norms, a_min=1e-9, a_max=None)
        embeddings = torch.from_numpy(embeddings)
        return embeddings
    
    
def run(simp_abstract, prompt):
    """
    Function to run the embedding process on a given abstract.
    
    Args:
        abstract (str): The (simplified) abstract of the paper to be embedded.
        
    Returns:
        numpy.ndarray: The embedding of the provided abstract.
    """
    embedder = PaperEmbedder(model_name='all-MiniLM-L6-v2')
    return embedder.get_embedding(simp_abstract)
    


# Example Usage:
if __name__ == "__main__":
    # --- Step 1: Initialize the PaperEmbedder ---
    # You can specify a different model if needed, e.g., 'allenai/specter'
    # but make sure it's compatible and available via sentence_transformers.
    # The default 'all-MiniLM-L6-v2' is a good general choice.
    try:
        embedder = PaperEmbedder(model_name='all-MiniLM-L6-v2')

        # --- Step 2: Define Sample Paper Data ---
        p1 = Paper(title="Large Language Models Are Few-Shot Learners",
                   abstract=(
            "We show that large language models (LMs) are surprisingly good "
            "few-shot learners—that is, they can adapt to a new task with "
            "only a few examples—by simply conditioning them on a task "
            "description and a few examples, then querying for the answer. "
            "For example, a GPT-3 instance with 175 billion parameters "
            "achieves strong performance on a wide range of NLP datasets."
        )) 
        
        p2 = Paper(title="Attention Is All You Need",
                   abstract=(
            "The dominant sequence transduction models are based on complex "
            "recurrent or convolutional neural networks that include an "
            "encoder-decoder structure. The best performing models also "
            "connect the encoder and decoder with an attention mechanism. "
            "We propose a new simple network architecture, the Transformer, "
            "based solely on attention mechanisms."
        )) 

        # A paper from a different domain for comparison
        p3 = Paper(title="CRISPR-Cas9: A Revolutionary Gene-Editing Tool",
                   abstract=(
            "CRISPR-Cas9 systems have emerged as powerful tools for genome "
            "editing, enabling precise modifications to DNA in a wide range "
            "of organisms. This review summarizes the mechanisms, applications, "
            "and challenges of this groundbreaking technology."
        )) 


        # --- Step 3: Generate Embeddings ---
        print("\nGenerating embeddings...")
        embedding1 = embedder.get_embedding(p1.abstract)
        embedding2 = embedder.get_embedding(p2.abstract)
        embedding3 = embedder.get_embedding(p3.abstract)


        # --- Step 4: Display Results ---
        print(f"\nEmbedding for Paper 1 (Title: '{sample_paper_title[:50]}...')")
        print(f"  Shape: {embedding1.shape}")
        print(f"  First 10 dimensions: {embedding1[:10]}")

        print(f"\nEmbedding for Paper 2 (Title: '{another_paper_title[:50]}...')")
        print(f"  Shape: {embedding2.shape}")
        print(f"  First 10 dimensions: {embedding2[:10]}")

        print(f"\nEmbedding for Paper 3 (Title: '{biology_paper_title[:50]}...')")
        print(f"  Shape: {embedding3.shape}")
        print(f"  First 10 dimensions: {embedding3[:10]}")

        # --- Optional: Calculate Cosine Similarity to demonstrate usefulness ---
        # Cosine similarity measures the cosine of the angle between two vectors.
        # A higher value (closer to 1) indicates greater similarity.
        from sklearn.metrics.pairwise import cosine_similarity

        print("\nCalculating Cosine Similarities:")
        # Similarity between two NLP papers (expected to be high)
        sim_nlp_nlp = cosine_similarity(embedding1.reshape(1, -1), embedding2.reshape(1, -1))[0][0]
        print(f"Similarity between Paper 1 and Paper 2 (both NLP): {sim_nlp_nlp:.4f}")

        # Similarity between an NLP paper and a Biology paper (expected to be lower)
        sim_nlp_bio1 = cosine_similarity(embedding1.reshape(1, -1), embedding3.reshape(1, -1))[0][0]
        print(f"Similarity between Paper 1 (NLP) and Paper 3 (Biology): {sim_nlp_bio1:.4f}")

        sim_nlp_bio2 = cosine_similarity(embedding2.reshape(1, -1), embedding3.reshape(1, -1))[0][0]
        print(f"Similarity between Paper 2 (NLP) and Paper 3 (Biology): {sim_nlp_bio2:.4f}")

    except ImportError:
        print("\nError: 'sentence-transformers' or 'numpy' not found.")
        print("Please install them using: pip install sentence-transformers numpy scikit-learn")
    except Exception as e:
        print(f"\nAn unexpected error occurred during execution: {e}")


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
"""
