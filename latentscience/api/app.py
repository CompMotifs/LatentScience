from fastapi import FastAPI
from latentscience.api.routes import paper
from latentscience.config import get_settings
from latentscience.di import lifespan, setup_di


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="LatentScience API",
        description="API for LatentScience, a platform for scientific research and paper discovery.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Register routes
    app.include_router(
        paper.router, prefix=f"{settings.api_prefix}/paper", tags=["paper"]
    )

    # Set up dependency injection
    setup_di(app)

    return app
