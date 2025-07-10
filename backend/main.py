from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import particle
from particle import Particle
import math

def safe_float(value):
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

app = FastAPI(
    title="Particle Information API",
    description="Get information about particles using PDG IDs",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParticleInfo(BaseModel):
    pdgid: int
    name: str
    latex_name: str
    mass: Optional[float]
    mass_upper: Optional[float]
    mass_lower: Optional[float]
    width: Optional[float]
    width_upper: Optional[float]
    width_lower: Optional[float]
    charge: Optional[float]
    three_charge: Optional[int]
    spin: Optional[float]
    parity: Optional[int]
    c_parity: Optional[int]
    g_parity: Optional[int]
    anti_particle_pdgid: Optional[int]
    status: Optional[str]
    lifetime: Optional[float]
    ctau: Optional[float]

class SearchResult(BaseModel):
    particles: List[Dict[str, Any]]
    total: int

@app.get("/")
async def root():
    return {"message": "Particle Information API", "version": "1.0.0"}

@app.get("/particle/{pdgid}", response_model=ParticleInfo)
async def get_particle_by_pdgid(pdgid: int):
    """Get detailed particle information by PDG ID"""
    try:
        p = Particle.from_pdgid(pdgid)
        
        return ParticleInfo(
            pdgid=int(p.pdgid),
            name=p.name,
            latex_name=getattr(p, 'latex_name', p.name),
            mass=safe_float(p.mass),
            mass_upper=safe_float(getattr(p, 'mass_upper', None)),
            mass_lower=safe_float(getattr(p, 'mass_lower', None)),
            width=safe_float(p.width),
            width_upper=safe_float(getattr(p, 'width_upper', None)),
            width_lower=safe_float(getattr(p, 'width_lower', None)),
            charge=safe_float(p.charge),
            three_charge=getattr(p, 'three_charge', None),
            spin=safe_float(getattr(p, 'J', None)),
            parity=getattr(p, 'P', None),
            c_parity=getattr(p, 'C', None),
            g_parity=getattr(p, 'G', None),
            anti_particle_pdgid=int(p.invert().pdgid) if p.invert() != p else None,
            status=str(p.status) if hasattr(p, 'status') and p.status is not None else None,
            lifetime=safe_float(p.lifetime),
            ctau=safe_float(getattr(p, 'ctau', None))
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Particle with PDG ID {pdgid} not found: {str(e)}")

@app.get("/search", response_model=SearchResult)
async def search_particles_empty(limit: int = 10):
    """Handle empty search query"""
    return SearchResult(particles=[], total=0)

@app.get("/search/{query}", response_model=SearchResult)
async def search_particles(query: str, limit: int = 10):
    """Search for particles by name"""
    try:
        matching_particles = []
        
        # Handle empty query
        if not query.strip():
            return SearchResult(particles=[], total=0)
        
        # Use a simple approach: test common particles first for the query
        common_pdgids = [
            11, -11, 13, -13, 22, 111, 211, -211, 321, -321,
            2212, -2212, 2112, -2112, 3122, -3122, 3112, -3112,
            1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6,
            15, -15, 12, -12, 14, -14, 16, -16,
            130, 310, 311, -311, 313, -313, 323, -323,
        ]
        
        query_lower = query.lower()
        
        for pdgid in common_pdgids:
            try:
                p = Particle.from_pdgid(pdgid)
                name_lower = p.name.lower()
                latex_name_lower = getattr(p, 'latex_name', p.name).lower()
                
                # Check if query matches name or common name patterns
                matches = (
                    query_lower in name_lower or
                    query_lower in latex_name_lower or
                    (query_lower == "electron" and name_lower in ["e-", "e+"]) or
                    (query_lower == "muon" and name_lower.startswith("mu")) or
                    (query_lower == "proton" and name_lower == "p") or
                    (query_lower == "neutron" and name_lower == "n") or
                    (query_lower == "photon" and name_lower == "gamma") or
                    (query_lower == "pion" and "pi" in name_lower)
                )
                
                if matches:
                    particle_dict = {
                        "pdgid": int(p.pdgid),
                        "name": p.name,
                        "latex_name": getattr(p, 'latex_name', p.name),
                        "mass": safe_float(p.mass),
                        "charge": safe_float(p.charge),
                    }
                    matching_particles.append(particle_dict)
                    
                    if len(matching_particles) >= limit:
                        break
            except:
                # Skip particles that can't be loaded
                continue
        
        return SearchResult(particles=matching_particles, total=len(matching_particles))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/popular")
async def get_popular_particles():
    """Get a list of commonly searched particles"""
    popular_pdgids = [
        11,    # electron
        -11,   # positron
        13,    # muon
        -13,   # anti-muon
        22,    # photon
        111,   # neutral pion
        211,   # charged pion
        -211,  # negative pion
        2212,  # proton
        -2212, # anti-proton
        2112,  # neutron
        -2112, # anti-neutron
        1,     # down quark
        2,     # up quark
        3,     # strange quark
        4,     # charm quark
        5,     # bottom quark
        6,     # top quark
    ]
    
    particles = []
    for pdgid in popular_pdgids:
        try:
            p = Particle.from_pdgid(pdgid)
            particles.append({
                "pdgid": int(p.pdgid),
                "name": p.name,
                "latex_name": getattr(p, 'latex_name', p.name),
                "mass": safe_float(p.mass),
                "charge": safe_float(p.charge),
            })
        except:
            continue
    
    return {"particles": particles}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)