from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    openai_api_key: Optional[str] = (
        "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"
    )
    anthropic_api_key: Optional[str] = None

    # Database
    pg_host: str = "localhost"
    pg_database: str = "latentscience"
    pg_user: str = "postgres"
    pg_password: str = "password"
    pg_port: int = 5432

    # Application
    api_prefix: str = "/api/v1"
    debug: bool = False
    log_level: str = "INFO"
    max_papers_per_search: int = 50
    default_similarity_threshold: float = 0.7
    max_embedding_batch_size: int = 100

    # Models
    default_embedding_model: str = "text-embedding-ada-002"
    default_chat_model: str = "gpt-4"
    embedding_dimensions: int = 1536

    # Rate Limiting
    requests_per_minute: int = 60
    openai_requests_per_minute: int = 50

    class Config:
        env_file = ".env.local"
        case_sensitive = False


def get_settings() -> Settings:
    """Returns the application settings."""
    return Settings()
