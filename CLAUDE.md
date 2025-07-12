# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Particle Explorer is a full-stack web application for exploring particle physics data using PDG IDs. It consists of:

- **Backend**: FastAPI application (`backend/main.py`) serving particle data from the PDG database via the `particle` Python library
- **Frontend**: SvelteKit application with TypeScript and Tailwind CSS for the user interface

## Development Commands

### Backend (Python)
- **Run backend**: `uv run python -m backend.main`
- **Run tests**: `uv run pytest` or `just test`
- **Run linting**: `uv run ruff check .`
- **Run type checking**: `uv run mypy backend/`
- **Run tests with coverage**: `uv run pytest tests/test_api.py -v --cov=backend --cov-report=xml`

### Frontend (Node.js)
- **Install dependencies**: `cd frontend && npm ci`
- **Run dev server**: `cd frontend && npm run dev` (serves on http://localhost:5173)
- **Build for production**: `cd frontend && npm run build`
- **Type checking**: `cd frontend && npm run check`

### Full Application
- **Development mode**: `./run.sh` (runs both frontend and backend separately)
- **Production mode**: Build frontend first, then run backend (serves static files + API on port 8000)
- **Docker**: `docker build -t particle-explorer . && docker run -p 8000:8000 particle-explorer`

## Architecture

### Backend Architecture (`backend/main.py`)
- **FastAPI application** with automatic OpenAPI documentation at `/docs`
- **Particle data endpoints**:
  - `GET /particle/{pdgid}` - Get detailed particle info by PDG ID
  - `GET /search/{query}` - Search particles by name  
  - `GET /popular` - Get list of commonly searched particles
- **Static file serving**: Automatically detects and serves built frontend from multiple possible paths
- **SPA routing support**: Catch-all route serves `index.html` for client-side routing
- **CORS configuration**: Allows requests from localhost development servers

### Frontend Architecture
- **SvelteKit** with static adapter for production builds
- **Component structure**:
  - `ParticleCard.svelte` - Displays detailed particle information
  - `SearchBar.svelte` - Handles PDG ID search input
  - `PopularParticles.svelte` - Shows list of commonly searched particles
- **API integration**: Uses axios to communicate with backend API
- **Responsive design**: Tailwind CSS with dark mode support

### Deployment Modes
1. **Development**: Frontend (port 5173) + Backend (port 8000) running separately
2. **Production**: Single FastAPI server (port 8000) serving both static files and API
3. **Docker**: Multi-stage build that builds frontend and runs everything in single container

## Testing

- **Backend tests**: Located in `tests/` directory using pytest
- **Integration tests**: Full stack tests in `test_integration.py`
- **CI pipeline**: Tests Python 3.10, 3.11, 3.12 with comprehensive linting, type checking, and Docker builds

## Key Dependencies

- **Backend**: FastAPI, uvicorn, particle (PDG database), pydantic
- **Frontend**: SvelteKit, TypeScript, Tailwind CSS, axios, KaTeX (for LaTeX rendering)
- **Development**: uv for Python dependency management, pytest for testing, ruff for linting

## Development Notes

- Uses `uv` for fast Python dependency management
- Frontend must be built before production backend serving
- API endpoints are protected from serving frontend files via prefix checking
- Static file paths are auto-detected for different deployment environments
- All particle data comes from the official PDG database via the `particle` library