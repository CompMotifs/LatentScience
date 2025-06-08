# We can rename / move this

from LatentScience.services import SimilarityService


def find_comparison(abstract, research_question):
    
    # Simplify abstract text
    prompter = EmbeddingPrompts()
    prompt_rephrase = prompter.get_rephrasing_prompt(
        paper_text=abstract, research_question=research_question)
    
    # Generate embedding for abstract
    embedder = PaperEmbedder(model_name="all-MiniLM-L6-v2")
    embedding_just_abstract = embedder.get_embedding(abstract)
    embedding_simp_abstract = embedder.get_embedding(prompt_rephrase)
    
    # Combine the embeddings of the raw and rephrased abstracts
    embedding_mixed = embedding_just_abstract + embedding_simp_abstract
    
    # Compare embedding with database embeddings
    big_number = int(1e6)
    similarifier = SimilarityService(top_choices=big_number, dim=-1)
    
    if use_mixed:
        top_picks, top_picks_idx = similarifier(embedding_mixed, database)
    else:
        top_picks, top_picks_idx = similarifier(embedding_simp_abstract, database)

    # Return the top picks
    return top_picks, top_picks_idx
    
def main():
    
    # Find top similar paper
    find_comparison(
        abstract="This is a sample abstract text for testing purposes.",
        research_question="What are the main findings of this paper?"
    )
    
    # Run comparison prompt
    
    # Reformat as nice output
    
    
    # entry 7 & 8
    