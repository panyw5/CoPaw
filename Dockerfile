# CoPaw Dockerfile for ModelScope Studio
# Simplified version optimized for ModelScope deployment

# -----------------------------------------------------------------------------
# Stage 1: Build console frontend
# -----------------------------------------------------------------------------
FROM node:20-slim AS console-builder

WORKDIR /app
COPY console /app/console

RUN cd /app/console && \
    npm ci --include=dev && \
    npm run build

# -----------------------------------------------------------------------------
# Stage 2: Runtime image
# -----------------------------------------------------------------------------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    COPAW_WORKING_DIR=/app/working \
    COPAW_SECRET_DIR=/app/working.secret \
    COPAW_PORT=7860 \
    COPAW_DISABLE_DESKTOP=1 \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy project files
COPY pyproject.toml setup.py README.md ./
COPY src ./src

# Copy pre-built console from stage 1
COPY --from=console-builder /app/console/dist/ ./src/copaw/console/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Initialize CoPaw with defaults
RUN copaw init --defaults --accept-security

# Expose port (ModelScope uses 7860 by default)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Start CoPaw using copaw app command (handles port configuration)
CMD ["copaw", "app", "--host", "0.0.0.0", "--port", "7860"]
