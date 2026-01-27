# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - DOCKERFILE
# =============================================================================
# Multi-stage Dockerfile for the Python Authentication Service.
# =============================================================================

# =============================================================================
# STAGE 1: BUILDER
# =============================================================================
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# =============================================================================
# STAGE 2: PRODUCTION
# =============================================================================
FROM python:3.11-slim as production

# Labels
LABEL org.opencontainers.image.title="Nexus Platform Authentication Service"
LABEL org.opencontainers.image.description="Authentication and authorization service for Nexus Platform"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="Nexus Platform"

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8081/health || exit 1

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8081"]


# =============================================================================
# STAGE 3: DEVELOPMENT
# =============================================================================
FROM python:3.11-slim as development

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    pytest-cov \
    httpx \
    black \
    isort \
    mypy \
    ruff

# Copy application code
COPY . .

EXPOSE 8081

# Run with auto-reload for development
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
