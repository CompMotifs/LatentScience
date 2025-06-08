# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Linting and Formatting
- `just fix` - Auto-format and fix linting issues for latentscience directory
- `just lint` - Run linting and type checking on latentscience directory
- `just lint-file <file>` - Lint specific file
- `uv run ruff format latentscience` - Format code
- `uv run ruff check --fix latentscience` - Fix linting issues
- `uv run pyright latentscience` - Type checking

### Testing
- `uv run pytest` - Run all tests
- `uv run pytest tests/test_<module>.py` - Run specific test file
- `uv run pytest --cov=latentscience tests/` - Run tests with coverage

### Modal Development
- `modal serve latentscience/main.py` - Run Modal app locally
- `modal deploy latentscience/main.py` - Deploy to Modal
- `modal logs paper-links` - View Modal app logs
- `modal secret create openai-secret OPENAI_API_KEY=<key>` - Create OpenAI secret

### Local Development (Docker)
- `just local-up` - Start local development environment with Docker
- `just local-down` - Stop local environment
- `just local-logs` - View logs from all services
- `just local-shell` - Open shell in API container
- `just local-refresh` - Wipe and restart entire environment

## Architecture Overview

This is a research paper similarity search application with a dual architecture:

### 1. Frontend (Next.js)
- Located in `app/` directory
- React-based web interface for paper search
- Uses modern Next.js patterns with app router

### 2. Backend (Python/Modal)
- Core logic in `latentscience/` directory
- Service-oriented architecture with Modal.com for serverless deployment
- FastAPI-based web API

### Key Components

**Modal Services** (`latentscience/main.py`):
- `EmbeddingServiceModal` - Generate embeddings using OpenAI or local models
- `SimilarityServiceModal` - Calculate semantic similarity between papers
- `ExplanationServiceModal` - Generate AI explanations for paper connections
- `DatabaseServiceModal` - Manage paper storage and retrieval

**API Layer** (`latentscience/api/api.py`):
- FastAPI application with CORS support
- `/api/search-papers` - Main search endpoint
- `/api/generate-embedding` - Direct embedding generation
- Currently returns mock data - real Modal service integration is TODO

**Data Models** (`latentscience/models/`):
- Pydantic models for request/response validation
- `Paper`, `Embedding`, `Similarity` model definitions

**Services** (`latentscience/services/`):
- Business logic implementations
- `EmbeddingService` - Text-to-vector conversion
- `SimilarityService` - Vector similarity calculations
- `ExplanationService` - AI-powered connection explanations
- `DatabaseService` - Data persistence layer

### Current State

The codebase is in active development with a hybrid structure:
- Skeleton services are implemented but contain placeholder logic
- Modal integration framework is complete but not fully connected
- Frontend exists but may need updates to match backend API
- Real embedding generation and database operations are TODO items

### Development Workflow

1. Use `uv` for Python dependency management
2. Modal.com for serverless backend deployment
3. Docker for local development environment
4. Services are designed to be independently testable and deployable

### Configuration

- `modal.toml` - Modal deployment configuration
- `pyproject.toml` - Python project dependencies and metadata
- Docker compose setup in `infra/` for local development
- Environment variables managed through Modal secrets

When implementing features, follow the service-oriented pattern and ensure Modal decorators are properly configured for resource requirements (GPU, memory, secrets).