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
COPY README.md ./

# Copy backend source code
COPY backend ./backend

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Create a simple static file server script for the frontend
RUN echo '#!/bin/bash\n\
echo "Starting particle physics application..."\n\
echo "Backend API will be available at http://localhost:8000"\n\
echo "Frontend will be available at http://localhost:3000"\n\
\n\
# Start backend API server\n\
cd /app && uv run python -m backend.main &\n\
BACKEND_PID=$!\n\
\n\
# Start simple HTTP server for frontend\n\
cd /app/frontend/build && python -m http.server 3000 &\n\
FRONTEND_PID=$!\n\
\n\
# Wait for both processes\n\
wait $BACKEND_PID $FRONTEND_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["/app/start.sh"]

# Alternative commands for development
# To run only backend: docker run -p 8000:8000 <image> uv run python -m backend.main
# To run tests: docker run <image> uv run pytest
