# We can rename / move this
from LatentScience.prompts import EmbeddingPrompts, PaperEmbedder
from LatentScience.services import SimilarityService
import anthropic
import os

csv_path = 'abstract.csv'

anthropic_client = anthropic.Anthropic(api_key="")


def database_prompts(csv_path, prompter):
    with open(csv_path, mode="r", encoding="utf-8", newline="") as files:
        reader = csv.reader(files)
        next(reader)
        for row in reader:
            abstract = row[1]
            prompt_abstract = prompter.get_rephrasing_prompt(paper_text=abstract, research_question=research_question)

            list_of_prompts.append(prompt_abstract)
    return list_of_prompts

def get_claude_layman(content_prompt):
    message = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": content_prompt}],
        )
    return message.content[0].text.strip()

def find_comparison(abstract, research_question):
    
    # Simplify abstract text
    prompter = EmbeddingPrompts()
    prompt_abstract = prompter.get_rephrasing_prompt(
        paper_text=abstract, research_question=research_question)
    abstract_layman = get_claude_layman(prompt_abstract)

    # Simplify Database text
    list_of_db_prompts = database_prompts(csv_path, prompter)
    list_of_db_layman = []
    for prompt in list_of_db_prompts:
        layman = get_claude_layman(prompt)
        list_of_db_layman.append(layman)
    
    # Generate embedding for abstract
    embedder = PaperEmbedder(model_name="all-MiniLM-L6-v2")
    embeddings_abstract = embedder.get_embedding(abstract_layman)

    # Generate embedding for database
    embeddings_database = embedder.get_embedding(list_of_db_layman)
    
    # Compare embedding with database embeddings
    big_number = 0
    similarifier = SimilarityService(top_choices=big_number, dim=-1)
    
    top_picks, top_picks_idx = similarifier(embeddings_abstract, embeddings_database)

    # Return the top picks
    return top_picks, top_picks_idx


def main(abstract, research_question):
    
    # Find top similar paper
    top_picks, top_picks_idx = find_comparison(
        abstract=abstract,
        research_question=research_question
    )
    
    # Run comparison prompt
    
    
    # entry 7 & 8
    
