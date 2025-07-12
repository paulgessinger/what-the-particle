"""Pytest configuration and fixtures for particle physics API tests."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_particle_data():
    """Sample particle data for testing."""
    return {
        "electron": {
            "pdgid": 11,
            "expected_name": "e-",
            "expected_charge": -1.0,
            "expected_mass": 0.5109989461,  # MeV
        },
        "proton": {
            "pdgid": 2212,
            "expected_name": "p",
            "expected_charge": 1.0,
            "expected_mass": 938.2720813,  # MeV
        },
        "photon": {
            "pdgid": 22,
            "expected_name": "gamma",
            "expected_charge": 0.0,
            "expected_mass": None,  # massless
        },
        "invalid": {
            "pdgid": 99999999,  # Non-existent particle
        }
    }


@pytest.fixture
def popular_particles_pdgids():
    """PDG IDs of particles that should be in the popular list."""
    return [11, -11, 13, -13, 22, 111, 211, -211, 2212, -2212, 2112, -2112, 1, 2, 3, 4, 5, 6]
