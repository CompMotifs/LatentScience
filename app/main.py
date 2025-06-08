import modal
from services.embedding_service import EmbeddingService
from services.similarity_service import SimilarityService
from services.explanation_service import ExplanationService
from services.database_service import DatabaseService

# Create Modal app
app = modal.App("LatentScience")

# Define the image with all dependencies
image = (
    modal.Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
    .run_commands("python -m spacy download en_core_web_sm")
)

# Shared volumes for database and model caching
database_volume = modal.Volume.from_name("paper-links-db", create_if_missing=True)
model_cache_volume = modal.Volume.from_name("model-cache", create_if_missing=True)


# Database service
@app.cls(
    image=image,
    volumes={"/data": database_volume},
    # secrets=[modal.Secret.from_name("database-secrets")],
)
class DatabaseServiceModal:
    def __init__(self):
        self.service = DatabaseService()

    @modal.method()
    def store_paper(self, paper_data: dict):
        return self.service.store_paper(paper_data)

    @modal.method()
    def store_embedding(self, embedding_data: dict):
        return self.service.store_embedding(embedding_data)

    @modal.method()
    def get_all_embeddings(self):
        return self.service.get_all_embeddings()

    @modal.method()
    def search_similar_papers(self, query_embedding: list, threshold: float = 0.7):
        return self.service.search_similar_papers(query_embedding, threshold)


# Embedding service
@app.cls(
    image=image,
    volumes={"/cache": model_cache_volume},
    secrets=[modal.Secret.from_name("openai-secret")],
    gpu="T4",  # Optional GPU for local models
)
class EmbeddingServiceModal:
    def __init__(self):
        self.service = EmbeddingService()

    @modal.method()
    def generate_embedding(self, text: str, model: str = "text-embedding-ada-002"):
        return self.service.generate_embedding(text, model)

    @modal.method()
    def rephrase_for_embedding(self, paper_text: str, research_question: str):
        return self.service.rephrase_for_embedding(paper_text, research_question)

    @modal.method()
    def batch_generate_embeddings(
        self, texts: list, model: str = "text-embedding-ada-002"
    ):
        return self.service.batch_generate_embeddings(texts, model)


# Similarity service
@app.cls(image=image)
class SimilarityServiceModal:
    def __init__(self):
        self.service = SimilarityService()

    @modal.method()
    def calculate_similarity(
        self, embedding1: list, embedding2: list, method: str = "cosine"
    ):
        return self.service.calculate_similarity(embedding1, embedding2, method)

    @modal.method()
    def batch_similarity(
        self, query_embedding: list, embeddings: list, method: str = "cosine"
    ):
        return self.service.batch_similarity(query_embedding, embeddings, method)

    @modal.method()
    def find_most_similar(
        self, query_embedding: list, embeddings: list, top_k: int = 10
    ):
        return self.service.find_most_similar(query_embedding, embeddings, top_k)


# Explanation service
@app.cls(image=image, secrets=[modal.Secret.from_name("openai-secret")])
class ExplanationServiceModal:
    def __init__(self):
        self.service = ExplanationService()

    @modal.method()
    def explain_connection(
        self, paper1_data: dict, paper2_data: dict, similarity_score: float
    ):
        return self.service.explain_connection(
            paper1_data, paper2_data, similarity_score
        )

    @modal.method()
    def batch_explain_connections(self, query_paper: dict, similar_papers: list):
        return self.service.batch_explain_connections(query_paper, similar_papers)


# Web interface
@app.function(image=image, secrets=[modal.Secret.from_name("openai-secret")])
@modal.web_endpoint(method="GET")
def web_app():
    """Serve the web interface"""
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    web_app = FastAPI()

    # Mount static files
    web_app.mount("/static", StaticFiles(directory="web/static"), name="static")

    @web_app.get("/")
    async def read_index():
        return FileResponse("web/static/index.html")

    return web_app


# API endpoints
@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("openai-secret"),
        # modal.Secret.from_name("database-secrets"),
    ],
)
@modal.web_endpoint(method="POST", label="api")
def api_endpoint():
    """Main API endpoint for the paper linking service"""
    from web.api import create_api_app

    return create_api_app()


if __name__ == "__main__":
    # For local development
    app.serve()
