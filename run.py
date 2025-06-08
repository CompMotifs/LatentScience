# We can rename / move this
from LatentScience.services import SimilarityService


def find_comparison(abstract, research_question):
    
    # Simplify abstract text
    prompter = EmbeddingPrompts()
    abstract_layman = prompter.get_rephrasing_prompt(
        paper_text=abstract, research_question=research_question)
    
    # Generate embedding for abstract
    embedder = PaperEmbedder(model_name="all-MiniLM-L6-v2")
    embeddings_abstract = embedder.get_embedding(abstract_layman)
    
    # Generate embeddings for database papers
    # embeddings_database = 
    
    # Compare embedding with database embeddings
    big_number = 0
    similarifier = SimilarityService(top_choices=big_number, dim=-1)
    
    top_picks, top_picks_idx = similarifier(embeddings_abstract, embeddings_database)

    # Return the top picks
    return top_picks, top_picks_idx
    

def main(prompt):
    
    # Find top similar paper
    find_comparison(
        abstract="This is a sample abstract text for testing purposes.",
        research_question="What are the main findings of this paper?"
    )
    
    # Run comparison prompt
    
    # Reformat as nice output
    
    
    # entry 7 & 8
    
