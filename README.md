# Particle Explorer 🚀⚛️

A modern web application for exploring particle physics data using PDG IDs. Built with FastAPI backend and SvelteKit frontend.

## Features

- 🔍 **Search by PDG ID**: Look up any particle using its Particle Data Group identifier
- 📊 **Detailed Information**: View mass, charge, spin, lifetime, and quantum numbers
- 🎨 **Modern UI**: Beautiful, responsive interface with dark mode support
- ⚡ **Fast & Responsive**: Built with SvelteKit for optimal performance
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- 🌟 **Popular Particles**: Quick access to commonly searched particles

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: SvelteKit + TypeScript
- **Styling**: Tailwind CSS
- **Data Source**: `particle` Python library (PDG database)
- **Math Rendering**: KaTeX for LaTeX formulas

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn
- Docker (optional, for containerized deployment)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd what-the-particle
   ```

2. **Backend Setup**

   **Option A: Using uv (recommended)**
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies and run
   uv sync
   uv run python -m backend.main
   ```

   **Option B: Using pip with virtual environment**
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies and run
   uv sync
   uv run python -m backend.main
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Development Mode (Separate Frontend/Backend)

This runs frontend and backend on separate ports for development:

**Option A: Using the convenience script**
```bash
chmod +x run.sh
./run.sh
```

**Option B: Manual startup**

Terminal 1 (Backend):
```bash
# Using uv (recommended)
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Mode (Single Server)

For production, the backend serves both the API and the built frontend from a single port:

1. **Build the Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Run the Backend (which now serves static files)**
   ```bash
   # The backend will automatically serve the built frontend
   uv run python -m backend.main
   ```

3. **Access the Application**
   - Complete Application: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Deployment

The Docker setup builds the frontend and serves everything through FastAPI in a single container:

1. **Build the Docker Image**
   ```bash
   docker build -t particle-explorer .
   ```

2. **Run the Container**
   ```bash
   docker run -p 8000:8000 particle-explorer
   ```

3. **Access the Application**
   - Complete Application: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

**Alternative Docker Commands:**
```bash
# Run tests
docker run particle-explorer uv run pytest

# Run with custom uvicorn settings
docker run -p 8000:8000 particle-explorer uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Build Process Details

### Frontend Build

The frontend uses SvelteKit with a static adapter for production builds:

```bash
cd frontend
npm install
npm run build
```

This creates a `build/` directory containing:
- `index.html` - Main HTML file
- `_app/` - SvelteKit application assets (JS, CSS)
- Static assets and other files

### Backend Static File Serving

The FastAPI backend automatically detects and serves frontend build files:

- **API Routes**: `/particle/*`, `/search/*`, `/popular` - API endpoints
- **Static Files**: `/_app/*` - SvelteKit application assets
- **SPA Fallback**: All other routes serve `index.html` for client-side routing

## Usage

### Search for Particles

Enter a PDG ID in the search bar to get detailed particle information:

- **11**: Electron
- **-11**: Positron
- **13**: Muon
- **22**: Photon
- **2212**: Proton
- **2112**: Neutron
- **211**: Charged pion
- **111**: Neutral pion

### Example Searches

- **Quarks**: 1 (down), 2 (up), 3 (strange), 4 (charm), 5 (bottom), 6 (top)
- **Leptons**: 11 (electron), 13 (muon), 15 (tau), 12 (electron neutrino)
- **Bosons**: 22 (photon), 23 (Z boson), 24 (W boson), 25 (Higgs)
- **Hadrons**: 2212 (proton), 2112 (neutron), 211 (π⁺), -211 (π⁻)

## API Endpoints

### GET `/particle/{pdgid}`
Get detailed information for a particle by PDG ID.

**Example**: `/particle/11` returns electron data

### GET `/popular`
Get a list of commonly searched particles.

### GET `/search/{query}`
Search for particles by name (partial matching).

**Example**: `/search/electron` finds electron-related particles

## Continuous Integration

The project includes a comprehensive CI pipeline with the following jobs:

### CI Jobs

1. **Python Tests** - Tests the backend code across Python 3.10, 3.11, and 3.12
   - Runs linting with `ruff`
   - Runs type checking with `mypy`
   - Runs all tests with `pytest` and coverage reporting

2. **Docker Build Test** - Verifies the Docker image builds and runs correctly
   - Builds the multi-stage Docker image
   - Tests that the application responds on expected endpoints

3. **Frontend Build Test** - Verifies the frontend builds correctly
   - Installs Node.js dependencies
   - Builds the SvelteKit application
   - Verifies build output structure

4. **Integration Test** - Tests the full application stack
   - Builds both frontend and backend
   - Starts the backend server
   - Runs integration tests against the running application

All CI jobs use `uv` for Python dependency management, ensuring fast and reliable builds.

## Development

### Project Structure

```
particle-explorer/
├── backend/
│   ├── main.py              # FastAPI application
│   └── __init__.py
├── frontend/
│   ├── src/                 # SvelteKit source code
│   ├── build/              # Built static files (after npm run build)
│   ├── package.json        # Node dependencies and scripts
│   └── svelte.config.js    # SvelteKit configuration
├── Dockerfile              # Multi-stage Docker build
├── pyproject.toml          # Python project configuration (uv)
├── run.sh                  # Development startup script
└── README.md
```

### Backend Development

The backend uses FastAPI with automatic OpenAPI documentation. Key files:
- `backend/main.py`: Main application and API routes
- Static file serving is automatically configured for production builds

### Frontend Development

The frontend is built with SvelteKit and Tailwind CSS. Key files:
- `frontend/src/routes/+page.svelte`: Main page
- `frontend/src/lib/components/`: Reusable components
- `frontend/src/app.css`: Global styles and Tailwind configuration

For development, use `npm run dev` which starts a development server with hot reload.
For production, use `npm run build` which creates optimized static files.

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new components in `src/lib/components/`
3. **Styling**: Use Tailwind classes or extend the configuration

## Testing

### Frontend Build Test
```bash
cd frontend
npm install
npm run build
# Should create a build/ directory with index.html and _app/ folder
ls -la build/
```

### Backend Static Serving Test
```bash
# After building the frontend
cd backend
python main.py
# Visit http://localhost:8000 - should serve the complete application
# Visit http://localhost:8000/docs - should show API documentation
```

### Docker Build Test
```bash
docker build -t particle-explorer .
docker run -p 8000:8000 particle-explorer
# Visit http://localhost:8000 - should serve the complete application
```

## Deployment Options

### 1. Docker (Recommended)
- Single container with both frontend and backend
- Production-ready with optimized builds
- Easy scaling and deployment

### 2. Separate Services
- Deploy frontend as static files (Netlify, Vercel, etc.)
- Deploy backend as API service (Heroku, Railway, etc.)
- Configure CORS for cross-origin requests

### 3. Traditional Server
- Build frontend: `npm run build`
- Copy built files to web server
- Run backend with static file serving

## Data Source

Particle data comes from the official Particle Data Group (PDG) database via the `particle` Python library. This ensures accurate, up-to-date information about fundamental particles.

## Browser Support

- Chrome/Chromium 88+
- Firefox 85+
- Safari 14+
- Edge 88+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Credits

- Data from the [Particle Data Group](https://pdg.lbl.gov/)
- Built with [FastAPI](https://fastapi.tiangolo.com/) and [SvelteKit](https://kit.svelte.dev/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
