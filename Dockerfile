# Multi-stage Dockerfile for Project Chimera
# Uses uv for fast, reproducible Python dependency management

# Stage 1: Builder - install dependencies and prepare environment
FROM python:3.12-slim AS builder

# Install system dependencies needed for uv and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv from official container image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set uv environment variables for optimal caching and linking
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Set working directory
WORKDIR /app

# Copy dependency files first (for better layer caching)
COPY pyproject.toml uv.lock* ./

# Install production dependencies only (no dev deps)
# Use cache mount for uv's cache directory
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy application code
COPY . .

# Sync project (install the project itself in editable mode)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Stage 2: Runtime - minimal image with only runtime dependencies
FROM python:3.12-slim AS runtime

# Install minimal runtime dependencies (if any are needed)
# Most Python packages are self-contained after uv sync

# Copy uv binary (needed for uv run commands)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . /app

# Set working directory
WORKDIR /app

# Set uv environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Default command: run tests (can be overridden)
# For production, this would be: CMD ["uv", "run", "python", "-m", "chimera"]
CMD ["uv", "run", "pytest", "tests/", "-v"]
