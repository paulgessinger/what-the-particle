"""Unit tests for the particle physics API endpoints."""

from fastapi import status


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint(self, client):
        """Test that the root endpoint returns correct information."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "Particle Information API"
        assert data["version"] == "1.0.0"


class TestParticleEndpoint:
    """Tests for the particle lookup endpoint."""

    def test_get_electron(self, client, sample_particle_data):
        """Test getting electron particle information."""
        electron = sample_particle_data["electron"]
        response = client.get(f"/particle/{electron['pdgid']}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Check required fields
        assert data["pdgid"] == electron["pdgid"]
        assert data["name"] == electron["expected_name"]
        assert abs(data["charge"] - electron["expected_charge"]) < 1e-10

        # Check mass (should be close to expected value)
        if data["mass"] is not None:
            assert abs(data["mass"] - electron["expected_mass"]) < 0.1

    def test_get_proton(self, client, sample_particle_data):
        """Test getting proton particle information."""
        proton = sample_particle_data["proton"]
        response = client.get(f"/particle/{proton['pdgid']}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["pdgid"] == proton["pdgid"]
        assert data["name"] == proton["expected_name"]
        assert abs(data["charge"] - proton["expected_charge"]) < 1e-10

        # Check mass (should be close to expected value)
        if data["mass"] is not None:
            assert abs(data["mass"] - proton["expected_mass"]) < 1.0

    def test_get_photon(self, client, sample_particle_data):
        """Test getting photon particle information."""
        photon = sample_particle_data["photon"]
        response = client.get(f"/particle/{photon['pdgid']}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["pdgid"] == photon["pdgid"]
        assert data["name"] == photon["expected_name"]
        assert abs(data["charge"] - photon["expected_charge"]) < 1e-10
        assert data["mass"] is None or data["mass"] == 0.0

    def test_get_invalid_particle(self, client, sample_particle_data):
        """Test getting information for a non-existent particle."""
        invalid = sample_particle_data["invalid"]
        response = client.get(f"/particle/{invalid['pdgid']}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert str(invalid["pdgid"]) in data["detail"]

    def test_particle_response_structure(self, client):
        """Test that particle response has correct structure."""
        response = client.get("/particle/11")  # electron
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        expected_fields = {
            "pdgid", "name", "latex_name", "mass", "mass_upper", "mass_lower",
            "width", "width_upper", "width_lower", "charge", "three_charge",
            "spin", "parity", "c_parity", "g_parity", "anti_particle_pdgid",
            "status", "lifetime", "ctau"
        }

        assert set(data.keys()) == expected_fields

        # Check that pdgid is an integer
        assert isinstance(data["pdgid"], int)
        assert data["pdgid"] == 11


class TestSearchEndpoint:
    """Tests for the particle search endpoint."""

    def test_search_electron(self, client):
        """Test searching for electron particles."""
        response = client.get("/search/electron")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "particles" in data
        assert "total" in data
        assert isinstance(data["particles"], list)
        assert isinstance(data["total"], int)
        assert data["total"] > 0

        # Check that electron is in results
        electron_found = False
        for particle in data["particles"]:
            if particle["pdgid"] == 11:
                electron_found = True
                assert particle["name"] == "e-"
                break
        assert electron_found

    def test_search_proton(self, client):
        """Test searching for proton particles."""
        response = client.get("/search/proton")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total"] > 0

        # Check for proton in results
        proton_found = False
        for particle in data["particles"]:
            if particle["pdgid"] == 2212:
                proton_found = True
                assert particle["name"] == "p"
                break
        assert proton_found

    def test_search_nonexistent(self, client):
        """Test searching for a non-existent particle."""
        response = client.get("/search/nonexistentparticle12345")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total"] == 0
        assert len(data["particles"]) == 0

    def test_search_with_limit(self, client):
        """Test search with limit parameter."""
        response = client.get("/search/pion?limit=3")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["particles"]) <= 3

    def test_search_particle_structure(self, client):
        """Test that search results have correct structure."""
        response = client.get("/search/electron")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        if data["particles"]:
            particle = data["particles"][0]
            expected_fields = {"pdgid", "name", "latex_name", "mass", "charge"}
            assert set(particle.keys()) == expected_fields


class TestPopularEndpoint:
    """Tests for the popular particles endpoint."""

    def test_get_popular_particles(self, client):
        """Test getting popular particles list."""
        response = client.get("/popular")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "particles" in data
        assert isinstance(data["particles"], list)
        assert len(data["particles"]) > 0

    def test_popular_particles_content(self, client, popular_particles_pdgids):
        """Test that popular particles contain expected particles."""
        response = client.get("/popular")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        particles = data["particles"]

        # Get PDG IDs from response
        response_pdgids = {p["pdgid"] for p in particles}

        # Check that common particles are included
        common_particles = {11, -11, 22, 2212, 2112}  # electron, positron, photon, proton, neutron
        assert common_particles.issubset(response_pdgids)

    def test_popular_particle_structure(self, client):
        """Test that popular particles have correct structure."""
        response = client.get("/popular")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        if data["particles"]:
            particle = data["particles"][0]
            expected_fields = {"pdgid", "name", "latex_name", "mass", "charge"}
            assert set(particle.keys()) == expected_fields


class TestCORSHeaders:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/")

        # Note: TestClient doesn't simulate browser CORS behavior exactly,
        # but we can test that the app doesn't crash with CORS middleware
        assert response.status_code == status.HTTP_200_OK


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_pdgid_type(self, client):
        """Test handling of invalid PDG ID types."""
        response = client.get("/particle/not_a_number")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_negative_search_limit(self, client):
        """Test search with negative limit."""
        response = client.get("/search/electron?limit=-1")
        assert response.status_code == status.HTTP_200_OK
        # The API should handle this gracefully
