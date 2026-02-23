from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dishka import AsyncContainer, Provider, make_async_container, Scope, provide
from dishka.integrations.fastapi import DishkaRoute, setup_dishka
from fastapi import FastAPI
from psycopg2.extensions import connection

from latentscience.config import Settings
from latentscience.database.paper import PaperRepository
from latentscience.service.paper import PaperService
from latentscience.service.embedding import EmbeddingService
from latentscience.service.explanation import ExplanationService


class Core(Provider):
    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        """Provides the core settings for the application."""
        return Settings()

    @provide(scope=Scope.REQUEST)
    def provide_connection(self, settings: Settings) -> connection:
        """Provides a database connection using the provided settings."""
        import psycopg2

        conn = psycopg2.connect(
            host=settings.pg_host,
            dbname=settings.pg_database,
            user=settings.pg_user,
            password=settings.pg_password,
            port=settings.pg_port,
        )
        conn.autocommit = True
        return conn


class Repository(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_paper(self, conn: connection) -> PaperRepository:
        """Provides the PaperRepository instance."""
        return PaperRepository(conn)


class Service(Provider):
    """Provides the core services for the application."""

    @provide(scope=Scope.APP)
    def provide_embedding(self) -> EmbeddingService:
        """Provides the EmbeddingService instance."""
        return EmbeddingService()

    @provide(scope=Scope.APP)
    def provide_explanation(self) -> ExplanationService:
        """Provides the ExplanationService instance."""
        return ExplanationService()

    @provide(scope=Scope.REQUEST)
    def provide_paper(
        self, paper_repo: PaperRepository, embedding_service: EmbeddingService
    ) -> PaperService:
        """Provides the PaperService instance."""
        return PaperService(paper_repo, embedding_service)


def build_container() -> AsyncContainer:
    """Builds the dependency injection container for the application."""
    providers = [Core(), Repository(), Service()]
    return make_async_container(*providers)


container = build_container()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan event to manage container lifecycle."""
    yield
    await app.state.dishka_container.close()


def setup_di(app: FastAPI, container_instance: AsyncContainer | None = None) -> None:
    """Set up the dependency injection container for the FastAPI app."""
    # Set DishkaRoute for automatic dependency injection
    app.router.route_class = DishkaRoute

    # Use provided container or default
    container_to_use = container_instance or container

    # Setup dishka integration with the FastAPI app
    setup_dishka(container=container_to_use, app=app)
