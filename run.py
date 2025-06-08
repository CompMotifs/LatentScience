# We can rename / move this
from LatentScience.prompts import EmbeddingPrompts, PaperEmbedder
from LatentScience.services import SimilarityService
import anthropic

anthropic_client = anthropic.Anthropic(api_key="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")

def get_claude_layman(paper_text, query_prompt, layman_prompt):
    message = anthropic_client.messages.create(
        model=os.getenv("CLAUDE_MODEL"),
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": f"{layman_prompt}\n{query_prompt}\n\nPaper:\n{paper_text}"}],
        )
    return message.content[0].text.strip()
    
    

def find_comparison(abstract, research_question):
    
    # Simplify abstract text
    prompter = EmbeddingPrompts()
    prompt_abstract = prompter.get_rephrasing_prompt(
        paper_text=abstract, research_question=research_question)
    abstract_layman = get_layman_abstract(call_claude(prompt_abstract))

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
    
