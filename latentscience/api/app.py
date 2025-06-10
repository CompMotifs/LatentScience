from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

    # Add CORS middleware - allow all connections
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Register routes
    app.include_router(
        paper.router, prefix=f"{settings.api_prefix}/paper", tags=["paper"]
    )

    # Set up dependency injection
    setup_di(app)

    return app
