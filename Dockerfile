# syntax=docker/dockerfile:1.4

# Base Stage - Common base for builder and runtime
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="/app:$PYTHONPATH"

WORKDIR /app

# Builder Stage - Install dependencies and prepare application
FROM base AS builder

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       build-essential \
       python3-dev \
       curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency installation
RUN pip install uv

# Copy dependency files and README (needed for build)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv pip install --system .

# Copy application code
COPY latentscience/ ./latentscience/
COPY scripts/ ./scripts/

# Development Stage - Includes development tools
FROM builder AS development

# Install development dependencies
RUN uv pip install --system ".[dev]"

# Runtime Stage - Clean production image
FROM base AS runtime

# Create and use non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app/latentscience /app/latentscience
COPY --from=builder /app/scripts /app/scripts

# Make scripts executable
RUN chmod +x /app/scripts/*.sh

# Change ownership of the application directory to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["./scripts/start.sh"]

# # Health check
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8000/api/health || exit 1
