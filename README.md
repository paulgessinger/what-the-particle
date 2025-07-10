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

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd what-the-particle
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the Application**
   
   **Option A: Using the convenience script**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   
   **Option B: Manual startup**
   
   Terminal 1 (Backend):
   ```bash
   cd backend
   python main.py
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

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

## Development

### Backend Development

The backend uses FastAPI with automatic OpenAPI documentation. Key files:
- `backend/main.py`: Main application and API routes
- `backend/requirements.txt`: Python dependencies

### Frontend Development

The frontend is built with SvelteKit and Tailwind CSS. Key files:
- `frontend/src/routes/+page.svelte`: Main page
- `frontend/src/lib/components/`: Reusable components
- `frontend/src/app.css`: Global styles and Tailwind configuration

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new components in `src/lib/components/`
3. **Styling**: Use Tailwind classes or extend the configuration

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
