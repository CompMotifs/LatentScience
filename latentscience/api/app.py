from fastapi import FastAPI
from latentscience.config import get_settings
from latentscience.di import lifespan


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
        webhooks, prefix=f"{settings.api_prefix}/webhooks", tags=["webhooks"]
    )
    app.include_router(health, prefix=f"{settings.api_prefix}/health", tags=["health"])

    # Set up dependency injection
    setup_di(app)

    logfire.instrument_fastapi(app)

    return app
