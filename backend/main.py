from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import particle
from particle import Particle

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
            pdgid=p.pdgid,
            name=p.name,
            latex_name=p.latex_name if hasattr(p, 'latex_name') else p.name,
            mass=float(p.mass) if p.mass is not None else None,
            mass_upper=float(p.mass_upper) if hasattr(p, 'mass_upper') and p.mass_upper is not None else None,
            mass_lower=float(p.mass_lower) if hasattr(p, 'mass_lower') and p.mass_lower is not None else None,
            width=float(p.width) if p.width is not None else None,
            width_upper=float(p.width_upper) if hasattr(p, 'width_upper') and p.width_upper is not None else None,
            width_lower=float(p.width_lower) if hasattr(p, 'width_lower') and p.width_lower is not None else None,
            charge=float(p.charge) if p.charge is not None else None,
            three_charge=p.three_charge if hasattr(p, 'three_charge') else None,
            spin=float(p.spin) if p.spin is not None else None,
            parity=p.parity if hasattr(p, 'parity') else None,
            c_parity=p.c_parity if hasattr(p, 'c_parity') else None,
            g_parity=p.g_parity if hasattr(p, 'g_parity') else None,
            anti_particle_pdgid=p.anti_particle.pdgid if p.anti_particle is not None else None,
            status=str(p.status) if hasattr(p, 'status') else None,
            lifetime=float(p.lifetime) if p.lifetime is not None else None,
            ctau=float(p.ctau) if hasattr(p, 'ctau') and p.ctau is not None else None
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Particle with PDG ID {pdgid} not found: {str(e)}")

@app.get("/search/{query}", response_model=SearchResult)
async def search_particles(query: str, limit: int = 10):
    """Search for particles by name"""
    try:
        # Get all particles and filter by name
        all_particles = particle.data_table.load_table("particle2022.csv")
        matching_particles = []
        
        query_lower = query.lower()
        for p in all_particles:
            if query_lower in p.name.lower() or (hasattr(p, 'latex_name') and query_lower in p.latex_name.lower()):
                particle_dict = {
                    "pdgid": p.pdgid,
                    "name": p.name,
                    "latex_name": p.latex_name if hasattr(p, 'latex_name') else p.name,
                    "mass": float(p.mass) if p.mass is not None else None,
                    "charge": float(p.charge) if p.charge is not None else None,
                }
                matching_particles.append(particle_dict)
                
                if len(matching_particles) >= limit:
                    break
        
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
                "pdgid": p.pdgid,
                "name": p.name,
                "latex_name": p.latex_name if hasattr(p, 'latex_name') else p.name,
                "mass": float(p.mass) if p.mass is not None else None,
                "charge": float(p.charge) if p.charge is not None else None,
            })
        except:
            continue
    
    return {"particles": particles}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)