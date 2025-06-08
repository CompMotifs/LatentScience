from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Database
    pg_host: str = "localhost"
    pg_database: str = "latentscience"
    pg_user: str = "postgres"
    pg_password: str = "password"
    pg_port: int = 5432

    # Application
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
