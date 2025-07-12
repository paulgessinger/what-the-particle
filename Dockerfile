# Multi-stage Dockerfile for particle physics web application
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
COPY frontend/svelte.config.js ./
COPY frontend/vite.config.js ./
COPY frontend/tsconfig.json ./
COPY frontend/tailwind.config.js ./
COPY frontend/postcss.config.js ./

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/src ./src
COPY frontend/static ./static

# Install the static adapter for building a static site
RUN npm install --save-dev @sveltejs/adapter-static

# Update svelte.config.js to use static adapter for Docker builds
RUN sed -i "s/adapter-auto/adapter-static/g" svelte.config.js && \
    sed -i "s/adapter()/adapter({ fallback: 'index.html' })/g" svelte.config.js

# Build the frontend
RUN npm run build

# Stage 2: Python application
FROM python:3.11-slim AS python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set working directory
WORKDIR /app

# Copy Python configuration files
COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# Copy backend source code
COPY backend ./backend

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Expose only port 8000 (FastAPI will serve everything)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command - run FastAPI server which serves both API and static files
CMD ["uv", "run", "python", "-m", "backend.main"]

# Alternative commands for development
# To run tests: docker run <image> uv run pytest
# To run with custom host/port: docker run -p 8000:8000 <image> uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000