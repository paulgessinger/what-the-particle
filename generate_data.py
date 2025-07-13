#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "particle>=0.24.0",
# ]
# ///
"""
Generate static data files for the particle explorer SPA.

This script extracts particle data from the particle package and generates:
1. Individual JSON files for each particle (by PDG ID)
2. A name mapping file for search functionality
3. A popular particles file

Output structure:
- frontend/static/particles/{pdgid}.json - Individual particle data
- frontend/static/particles/name-mapping.json - Search mapping
- frontend/static/particles/popular.json - Popular particles list
"""

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

from particle import Particle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "frontend" / "static" / "particles"


def safe_float(value: Any) -> Optional[float]:
    """Convert value to float, handling special cases."""
    if value is None:
        return None
    try:
        result = float(value)
        if math.isnan(result):
            return None
        if math.isinf(result):
            return None
        return result
    except (ValueError, TypeError, OverflowError):
        return None


def get_descriptive_name(particle: Particle) -> str:
    """Get a more descriptive name for common particles."""
    pdgid = int(particle.pdgid)
    descriptive_names = {
        # Leptons
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
        
        # Gauge bosons
        22: "photon",
        23: "Z boson",
        24: "W+ boson",
        -24: "W- boson",
        25: "Higgs boson",
        
        # Baryons
        2212: "proton",
        -2212: "antiproton",
        2112: "neutron",
        -2112: "antineutron",
        
        # Mesons
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


def create_particle_data(particle: Particle) -> Dict[str, Any]:
    """Create particle data dictionary."""
    try:
        anti_particle = particle.invert()
        has_antiparticle = anti_particle != particle
    except Exception:
        has_antiparticle = False
        anti_particle = None
    
    return {
        "pdgid": int(particle.pdgid),
        "name": particle.name,
        "descriptive_name": get_descriptive_name(particle),
        "latex_name": getattr(particle, "latex_name", particle.name),
        "mass": safe_float(particle.mass),
        "mass_upper": safe_float(getattr(particle, "mass_upper", None)),
        "mass_lower": safe_float(getattr(particle, "mass_lower", None)),
        "width": safe_float(particle.width),
        "width_upper": safe_float(getattr(particle, "width_upper", None)),
        "width_lower": safe_float(getattr(particle, "width_lower", None)),
        "charge": safe_float(particle.charge),
        "three_charge": getattr(particle, "three_charge", None),
        "spin": safe_float(getattr(particle, "J", None)),
        "parity": getattr(particle, "P", None),
        "c_parity": getattr(particle, "C", None),
        "g_parity": getattr(particle, "G", None),
        "anti_particle_pdgid": int(anti_particle.pdgid) if has_antiparticle else None,
        "anti_particle_name": anti_particle.name if has_antiparticle else None,
        "status": str(particle.status) if hasattr(particle, "status") and particle.status is not None else None,
        "lifetime": safe_float(particle.lifetime / 1e9) if particle.lifetime is not None and particle.lifetime != 0 else safe_float(particle.lifetime),  # Convert ns to s
        "ctau": safe_float(getattr(particle, "ctau", None)),
    }


def build_name_mapping() -> Dict[str, List[int]]:
    """Build comprehensive name mapping for search functionality."""
    name_mapping = {}
    
    try:
        all_particles = Particle.all()
        logger.info(f"Processing {len(all_particles)} particles for name mapping")
        
        for particle in all_particles:
            try:
                pdgid = int(particle.pdgid)
                
                # Add particle name (exact)
                name = particle.name.lower()
                if name not in name_mapping:
                    name_mapping[name] = []
                if pdgid not in name_mapping[name]:
                    name_mapping[name].append(pdgid)
                
                # Add PDG name if different
                if hasattr(particle, 'pdg_name') and particle.pdg_name.lower() != name:
                    pdg_name = particle.pdg_name.lower()
                    if pdg_name not in name_mapping:
                        name_mapping[pdg_name] = []
                    if pdgid not in name_mapping[pdg_name]:
                        name_mapping[pdg_name].append(pdgid)
                
                # Add common aliases based on PDG ID
                aliases = []
                if pdgid == 11:
                    aliases = ['electron']
                elif pdgid == -11:
                    aliases = ['positron']
                elif pdgid == 13:
                    aliases = ['muon']
                elif pdgid == -13:
                    aliases = ['antimuon']
                elif pdgid == 2212:
                    aliases = ['proton']
                elif pdgid == -2212:
                    aliases = ['antiproton']
                elif pdgid == 2112:
                    aliases = ['neutron']
                elif pdgid == -2112:
                    aliases = ['antineutron']
                elif pdgid == 22:
                    aliases = ['photon']
                elif pdgid == 25:
                    aliases = ['higgs', 'higgs boson']
                elif pdgid == 15:
                    aliases = ['tau']
                elif pdgid == -15:
                    aliases = ['antitau']
                elif pdgid == 1:
                    aliases = ['down', 'down quark', 'd']
                elif pdgid == -1:
                    aliases = ['anti-down', 'antidown']
                elif pdgid == 2:
                    aliases = ['up', 'up quark', 'u']
                elif pdgid == -2:
                    aliases = ['anti-up', 'antiup']
                elif pdgid == 3:
                    aliases = ['strange', 'strange quark', 's']
                elif pdgid == -3:
                    aliases = ['anti-strange', 'antistrange']
                elif pdgid == 4:
                    aliases = ['charm', 'charm quark', 'c']
                elif pdgid == -4:
                    aliases = ['anti-charm', 'anticharm']
                elif pdgid == 5:
                    aliases = ['bottom', 'bottom quark', 'beauty', 'b']
                elif pdgid == -5:
                    aliases = ['anti-bottom', 'antibottom', 'anti-beauty']
                elif pdgid == 6:
                    aliases = ['top', 'top quark', 't']
                elif pdgid == -6:
                    aliases = ['anti-top', 'antitop']
                
                # Add aliases to mapping
                for alias in aliases:
                    alias_lower = alias.lower()
                    if alias_lower not in name_mapping:
                        name_mapping[alias_lower] = []
                    if pdgid not in name_mapping[alias_lower]:
                        name_mapping[alias_lower].append(pdgid)
                        
            except Exception as e:
                logger.warning(f"Failed to process particle {particle}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Failed to build name mapping: {e}")
        
    logger.info(f"Built name mapping with {len(name_mapping)} entries")
    return name_mapping


def generate_popular_particles() -> List[Dict[str, Any]]:
    """Generate popular particles list."""
    popular_pdgids = [
        11,    # electron
        -11,   # positron
        13,    # muon
        -13,   # anti-muon
        22,    # photon
        25,    # Higgs boson
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
            particle = Particle.from_pdgid(pdgid)
            particles.append({
                "pdgid": int(particle.pdgid),
                "name": particle.name,
                "descriptive_name": get_descriptive_name(particle),
                "latex_name": getattr(particle, "latex_name", particle.name),
                "mass": safe_float(particle.mass),
                "charge": safe_float(particle.charge),
                "three_charge": getattr(particle, "three_charge", None),
            })
        except Exception as e:
            logger.warning(f"Failed to process popular particle {pdgid}: {e}")
            continue
    
    return particles


def main():
    """Main function to generate all data files."""
    logger.info("Starting particle data generation...")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all particles
    try:
        all_particles = Particle.all()
        logger.info(f"Found {len(all_particles)} particles")
    except Exception as e:
        logger.error(f"Failed to load particles: {e}")
        return 1
    
    # Generate individual particle files
    logger.info("Generating individual particle files...")
    particle_count = 0
    for particle in all_particles:
        try:
            pdgid = int(particle.pdgid)
            particle_data = create_particle_data(particle)
            
            output_file = OUTPUT_DIR / f"{pdgid}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(particle_data, f, indent=2, ensure_ascii=False)
            
            particle_count += 1
        except Exception as e:
            logger.warning(f"Failed to generate file for particle {particle}: {e}")
            continue
    
    logger.info(f"Generated {particle_count} particle files")
    
    # Generate name mapping file
    logger.info("Generating name mapping file...")
    name_mapping = build_name_mapping()
    name_mapping_file = OUTPUT_DIR / "name-mapping.json"
    with open(name_mapping_file, 'w', encoding='utf-8') as f:
        json.dump(name_mapping, f, indent=2, ensure_ascii=False)
    
    # Generate popular particles file
    logger.info("Generating popular particles file...")
    popular_particles = generate_popular_particles()
    popular_file = OUTPUT_DIR / "popular.json"
    with open(popular_file, 'w', encoding='utf-8') as f:
        json.dump({"particles": popular_particles}, f, indent=2, ensure_ascii=False)
    
    logger.info("Data generation complete!")
    logger.info(f"Generated files in: {OUTPUT_DIR}")
    logger.info(f"- {particle_count} individual particle files")
    logger.info(f"- 1 name mapping file with {len(name_mapping)} entries")
    logger.info(f"- 1 popular particles file with {len(popular_particles)} particles")
    
    return 0


if __name__ == "__main__":
    exit(main())