import math
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from particle import Particle
from pydantic import BaseModel
from thefuzz import fuzz, process
import logging


def safe_float(value: Any) -> float | None:
    """Convert value to float, return None if inf, -inf, or NaN"""
    if value is None:
        return None
    try:
        f = float(value)
        if math.isinf(f) or math.isnan(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


# Global variables for particle search
PARTICLE_NAME_MAP = {}
PARTICLE_SEARCH_LIST = []

app = FastAPI(
    title="Particle Information API",
    description="Get information about particles using PDG IDs",
    version="1.0.0",
)


@app.on_event("startup")
async def precompute_particle_data():
    """Precompute particle search data for better performance"""
    global PARTICLE_NAME_MAP, PARTICLE_SEARCH_LIST
    
    try:
        # Get all particles from the PDG database
        all_particles = Particle.all()
        
        # Build name mapping and search list
        for particle in all_particles:
            try:
                # Store particle by its name
                PARTICLE_NAME_MAP[particle.name.lower()] = particle
                
                # Also store by pdg_name if different
                if particle.pdg_name.lower() != particle.name.lower():
                    PARTICLE_NAME_MAP[particle.pdg_name.lower()] = particle
                    
                # Add to search list for fuzzy matching
                PARTICLE_SEARCH_LIST.append((particle.name, particle))
                if particle.pdg_name != particle.name:
                    PARTICLE_SEARCH_LIST.append((particle.pdg_name, particle))
                    
                # Add common aliases - use PDG ID to ensure we get the right particle
                name_lower = particle.name.lower()
                pdgid = particle.pdgid
                
                # Specific mappings based on PDG ID to avoid conflicts
                if pdgid == 11:  # electron
                    PARTICLE_NAME_MAP['electron'] = particle
                elif pdgid == -11:  # positron
                    PARTICLE_NAME_MAP['positron'] = particle
                elif pdgid == 13:  # muon
                    PARTICLE_NAME_MAP['muon'] = particle
                elif pdgid == -13:  # antimuon
                    PARTICLE_NAME_MAP['antimuon'] = particle
                elif pdgid == 2212:  # proton
                    PARTICLE_NAME_MAP['proton'] = particle
                elif pdgid == -2212:  # antiproton
                    PARTICLE_NAME_MAP['antiproton'] = particle
                elif pdgid == 2112:  # neutron
                    PARTICLE_NAME_MAP['neutron'] = particle
                elif pdgid == -2112:  # antineutron
                    PARTICLE_NAME_MAP['antineutron'] = particle
                elif pdgid == 22:  # photon
                    PARTICLE_NAME_MAP['photon'] = particle
                elif pdgid == 15:  # tau
                    PARTICLE_NAME_MAP['tau'] = particle
                elif pdgid == -15:  # antitau
                    PARTICLE_NAME_MAP['antitau'] = particle
                # Quarks
                elif pdgid == 1:  # down quark
                    PARTICLE_NAME_MAP['down'] = particle
                    PARTICLE_NAME_MAP['down quark'] = particle
                elif pdgid == -1:  # anti-down quark
                    PARTICLE_NAME_MAP['anti-down'] = particle
                    PARTICLE_NAME_MAP['antidown'] = particle
                elif pdgid == 2:  # up quark
                    PARTICLE_NAME_MAP['up'] = particle
                    PARTICLE_NAME_MAP['up quark'] = particle
                elif pdgid == -2:  # anti-up quark
                    PARTICLE_NAME_MAP['anti-up'] = particle
                    PARTICLE_NAME_MAP['antiup'] = particle
                elif pdgid == 3:  # strange quark
                    PARTICLE_NAME_MAP['strange'] = particle
                    PARTICLE_NAME_MAP['strange quark'] = particle
                elif pdgid == -3:  # anti-strange quark
                    PARTICLE_NAME_MAP['anti-strange'] = particle
                    PARTICLE_NAME_MAP['antistrange'] = particle
                elif pdgid == 4:  # charm quark
                    PARTICLE_NAME_MAP['charm'] = particle
                    PARTICLE_NAME_MAP['charm quark'] = particle
                elif pdgid == -4:  # anti-charm quark
                    PARTICLE_NAME_MAP['anti-charm'] = particle
                    PARTICLE_NAME_MAP['anticharm'] = particle
                elif pdgid == 5:  # bottom quark
                    PARTICLE_NAME_MAP['bottom'] = particle
                    PARTICLE_NAME_MAP['bottom quark'] = particle
                    PARTICLE_NAME_MAP['beauty'] = particle
                elif pdgid == -5:  # anti-bottom quark
                    PARTICLE_NAME_MAP['anti-bottom'] = particle
                    PARTICLE_NAME_MAP['antibottom'] = particle
                    PARTICLE_NAME_MAP['anti-beauty'] = particle
                elif pdgid == 6:  # top quark
                    PARTICLE_NAME_MAP['top'] = particle
                    PARTICLE_NAME_MAP['top quark'] = particle
                elif pdgid == -6:  # anti-top quark
                    PARTICLE_NAME_MAP['anti-top'] = particle
                    PARTICLE_NAME_MAP['antitop'] = particle
                elif 'pi' in name_lower:
                    PARTICLE_NAME_MAP[f'pion{name_lower.replace("pi", "")}'] = particle
                    
            except Exception:
                continue
                
        logging.info(f"Loaded {len(PARTICLE_NAME_MAP)} particle name mappings")
        logging.info(f"Built search list with {len(PARTICLE_SEARCH_LIST)} entries")
        
    except Exception as e:
        logging.error(f"Failed to precompute particle data: {e}")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ],  # Include FastAPI serving static files
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine the static files directory
# When running from Docker, the frontend build will be at /app/frontend/build
# When running locally, it might be at ../frontend/build
static_dir = None
possible_static_dirs = [
    Path("/app/frontend/build"),  # Docker path
    Path(__file__).parent.parent / "frontend" / "build",  # Local development path
    Path("frontend/build"),  # Alternative local path
]

for dir_path in possible_static_dirs:
    if dir_path.exists() and dir_path.is_dir():
        static_dir = dir_path
        break

if static_dir:
    # Mount static files (CSS, JS, images, etc.)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Serve SvelteKit app files
    if (static_dir / "_app").exists():
        app.mount(
            "/_app", StaticFiles(directory=static_dir / "_app"), name="svelte_app"
        )


class ParticleInfo(BaseModel):
    pdgid: int
    name: str
    descriptive_name: str
    latex_name: str
    mass: float | None
    mass_upper: float | None
    mass_lower: float | None
    width: float | None
    width_upper: float | None
    width_lower: float | None
    charge: float | None
    three_charge: int | None
    spin: float | None
    parity: int | None
    c_parity: int | None
    g_parity: int | None
    anti_particle_pdgid: int | None
    status: str | None
    lifetime: float | None
    ctau: float | None


class SearchResult(BaseModel):
    particles: list[dict[str, Any]]
    total: int




@app.get("/particle/{pdgid}", response_model=ParticleInfo)
async def get_particle_by_pdgid(pdgid: int) -> ParticleInfo:
    """Get detailed particle information by PDG ID"""
    try:
        p = Particle.from_pdgid(pdgid)

        return ParticleInfo(
            pdgid=int(p.pdgid),
            name=p.name,
            descriptive_name=get_descriptive_name(p),
            latex_name=getattr(p, "latex_name", p.name),
            mass=safe_float(p.mass),
            mass_upper=safe_float(getattr(p, "mass_upper", None)),
            mass_lower=safe_float(getattr(p, "mass_lower", None)),
            width=safe_float(p.width),
            width_upper=safe_float(getattr(p, "width_upper", None)),
            width_lower=safe_float(getattr(p, "width_lower", None)),
            charge=safe_float(p.charge),
            three_charge=getattr(p, "three_charge", None),
            spin=safe_float(getattr(p, "J", None)),
            parity=getattr(p, "P", None),
            c_parity=getattr(p, "C", None),
            g_parity=getattr(p, "G", None),
            anti_particle_pdgid=int(p.invert().pdgid) if p.invert() != p else None,
            status=str(p.status)
            if hasattr(p, "status") and p.status is not None
            else None,
            lifetime=safe_float(p.lifetime),
            ctau=safe_float(getattr(p, "ctau", None)),
        )
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Particle with PDG ID {pdgid} not found: {str(e)}"
        ) from e


@app.get("/search", response_model=SearchResult)
async def search_particles_empty(limit: int = 10) -> SearchResult:
    """Handle empty search query"""
    return SearchResult(particles=[], total=0)


def get_descriptive_name(particle: Particle) -> str:
    """Get a more descriptive name for common particles"""
    pdgid = int(particle.pdgid)
    descriptive_names = {
        11: "electron",
        -11: "positron", 
        13: "muon",
        -13: "antimuon",
        15: "tau lepton",
        -15: "tau antilepton",
        12: "electron neutrino",
        -12: "electron antineutrino",
        14: "muon neutrino", 
        -14: "muon antineutrino",
        16: "tau neutrino",
        -16: "tau antineutrino",
        22: "photon",
        23: "Z boson",
        24: "W+ boson",
        -24: "W- boson",
        25: "Higgs boson",
        2212: "proton",
        -2212: "antiproton",
        2112: "neutron",
        -2112: "antineutron",
        211: "charged pion",
        -211: "charged pion",
        111: "neutral pion",
        321: "charged kaon",
        -321: "charged kaon",
        311: "neutral kaon",
        130: "neutral kaon (long)",
        310: "neutral kaon (short)",
        # Quarks
        1: "down quark",
        -1: "anti-down quark",
        2: "up quark", 
        -2: "anti-up quark",
        3: "strange quark",
        -3: "anti-strange quark",
        4: "charm quark",
        -4: "anti-charm quark",
        5: "bottom quark",
        -5: "anti-bottom quark",
        6: "top quark",
        -6: "anti-top quark",
    }
    return descriptive_names.get(pdgid, particle.name)

def create_particle_dict(particle: Particle) -> dict[str, Any]:
    """Helper function to create a particle dictionary"""
    return {
        "pdgid": int(particle.pdgid),
        "name": particle.name,
        "descriptive_name": get_descriptive_name(particle),
        "latex_name": getattr(particle, "latex_name", particle.name),
        "mass": safe_float(particle.mass),
        "charge": safe_float(particle.charge),
    }


@app.get("/search/{query}", response_model=SearchResult)
async def search_particles(query: str, limit: int = 10) -> SearchResult:
    """Search for particles by name or PDG ID using fuzzy matching"""
    try:
        # Handle empty query
        if not query.strip():
            return SearchResult(particles=[], total=0)

        query_lower = query.strip().lower()
        matching_particles = []
        seen_pdgids = set()

        # Check if query is numeric (PDG ID search)
        try:
            pdg_id = int(query_lower)
            try:
                p = Particle.from_pdgid(pdg_id)
                particle_dict = create_particle_dict(p)
                return SearchResult(particles=[particle_dict], total=1)
            except Exception:
                pass
        except ValueError:
            pass

        # 1. Exact name matches first
        if query_lower in PARTICLE_NAME_MAP:
            particle = PARTICLE_NAME_MAP[query_lower]
            if particle.pdgid not in seen_pdgids:
                matching_particles.append(create_particle_dict(particle))
                seen_pdgids.add(particle.pdgid)

        # 2. Substring matches in our precomputed names
        for name, particle in PARTICLE_NAME_MAP.items():
            if query_lower in name and particle.pdgid not in seen_pdgids:
                matching_particles.append(create_particle_dict(particle))
                seen_pdgids.add(particle.pdgid)
                
                if len(matching_particles) >= limit:
                    break

        # 3. If we don't have enough matches, use fuzzy matching
        if len(matching_particles) < limit:
            # Extract just the names for fuzzy matching
            search_names = [name for name, _ in PARTICLE_SEARCH_LIST]
            
            # Get fuzzy matches
            fuzzy_matches = process.extract(
                query_lower, 
                search_names, 
                limit=limit * 2,  # Get more to account for duplicates
                scorer=fuzz.partial_ratio
            )
            
            # Add fuzzy matches that aren't already included
            for matched_name, score in fuzzy_matches:
                if score >= 60:  # Minimum similarity threshold
                    # Find the particle for this name
                    for name, particle in PARTICLE_SEARCH_LIST:
                        if name == matched_name and particle.pdgid not in seen_pdgids:
                            matching_particles.append(create_particle_dict(particle))
                            seen_pdgids.add(particle.pdgid)
                            break
                    
                    if len(matching_particles) >= limit:
                        break

        # 4. If still not enough, try the particle library's findall
        if len(matching_particles) < limit:
            try:
                particle_results = Particle.findall(query_lower)
                for particle in particle_results:
                    if particle.pdgid not in seen_pdgids:
                        matching_particles.append(create_particle_dict(particle))
                        seen_pdgids.add(particle.pdgid)
                        
                        if len(matching_particles) >= limit:
                            break
            except Exception:
                pass

        return SearchResult(
            particles=matching_particles[:limit], 
            total=len(matching_particles)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}") from e


@app.get("/popular")
async def get_popular_particles() -> dict[str, list[dict[str, Any]]]:
    """Get a list of commonly searched particles"""
    popular_pdgids = [
        11,  # electron
        -11,  # positron
        13,  # muon
        -13,  # anti-muon
        22,  # photon
        111,  # neutral pion
        211,  # charged pion
        -211,  # negative pion
        2212,  # proton
        -2212,  # anti-proton
        2112,  # neutron
        -2112,  # anti-neutron
        1,  # down quark
        2,  # up quark
        3,  # strange quark
        4,  # charm quark
        5,  # bottom quark
        6,  # top quark
    ]

    particles = []
    for pdgid in popular_pdgids:
        try:
            p = Particle.from_pdgid(pdgid)
            particles.append(
                {
                    "pdgid": int(p.pdgid),
                    "name": p.name,
                    "latex_name": getattr(p, "latex_name", p.name),
                    "mass": safe_float(p.mass),
                    "charge": safe_float(p.charge),
                }
            )
        except Exception:
            continue

    return {"particles": particles}


# Catch-all route to serve the frontend for SPA routing
@app.get("/{path:path}")
async def serve_frontend(path: str) -> Any:
    """Serve the frontend application for all unmatched routes"""
    # Don't serve frontend for API routes - let FastAPI return proper 404s
    api_prefixes = ["particle", "search", "popular", "docs", "openapi.json", "redoc"]
    if any(path.startswith(prefix) for prefix in api_prefixes):
        # Let FastAPI handle API routes with proper error responses
        raise HTTPException(status_code=404, detail="Not found")

    if static_dir:
        # Check if the requested file exists
        file_path = static_dir / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # For SPA routing, serve index.html for any path that doesn't exist
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)

    # If no static files are available
    logging.error("Frontend not built yet. Run 'npm run build' in the frontend directory.")
    raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)
