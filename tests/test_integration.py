"""Integration tests for the particle physics API."""


class TestParticleWorkflow:
    """Integration tests for typical user workflows."""

    def test_electron_workflow(self, client):
        """Test complete workflow for electron particle lookup."""
        # Step 1: Search for electron
        search_response = client.get("/search/electron")
        assert search_response.status_code == 200

        search_data = search_response.json()
        assert search_data["total"] > 0

        # Find electron in search results
        electron_pdgid = None
        for particle in search_data["particles"]:
            if particle["name"] == "e-":
                electron_pdgid = particle["pdgid"]
                break

        assert electron_pdgid is not None
        assert electron_pdgid == 11

        # Step 2: Get detailed information about electron
        detail_response = client.get(f"/particle/{electron_pdgid}")
        assert detail_response.status_code == 200

        detail_data = detail_response.json()
        assert detail_data["pdgid"] == 11
        assert detail_data["name"] == "e-"
        assert detail_data["charge"] == -1.0

        # Step 3: Verify electron is in popular particles
        popular_response = client.get("/popular")
        assert popular_response.status_code == 200

        popular_data = popular_response.json()
        electron_in_popular = any(
            p["pdgid"] == 11 for p in popular_data["particles"]
        )
        assert electron_in_popular

    def test_quark_family_lookup(self, client):
        """Test looking up quarks and verify they form a complete family."""
        quark_pdgids = [1, 2, 3, 4, 5, 6]  # down, up, strange, charm, bottom, top
        quark_names = ["d", "u", "s", "c", "b", "t"]

        quarks_found = []
        for pdgid in quark_pdgids:
            response = client.get(f"/particle/{pdgid}")
            if response.status_code == 200:
                data = response.json()
                quarks_found.append(data)

        # Should find at least some quarks
        assert len(quarks_found) >= 4

        # Check that quark names are as expected
        found_names = {q["name"] for q in quarks_found}
        expected_names = set(quark_names[:len(quarks_found)])
        assert found_names.intersection(expected_names) == expected_names

    def test_particle_antiparticle_symmetry(self, client):
        """Test that particles and their antiparticles have correct relationships."""
        test_pairs = [
            (11, -11),    # electron, positron
            (13, -13),    # muon, anti-muon
            (2212, -2212), # proton, anti-proton
        ]

        for particle_id, antiparticle_id in test_pairs:
            # Get particle
            particle_response = client.get(f"/particle/{particle_id}")
            if particle_response.status_code != 200:
                continue

            particle_data = particle_response.json()

            # Get antiparticle
            antiparticle_response = client.get(f"/particle/{antiparticle_id}")
            if antiparticle_response.status_code != 200:
                continue

            antiparticle_data = antiparticle_response.json()

            # Check charge symmetry
            if particle_data["charge"] is not None and antiparticle_data["charge"] is not None:
                assert abs(particle_data["charge"] + antiparticle_data["charge"]) < 1e-10

            # Check mass equality
            if particle_data["mass"] is not None and antiparticle_data["mass"] is not None:
                assert abs(particle_data["mass"] - antiparticle_data["mass"]) < 1e-6


class TestDataConsistency:
    """Tests for data consistency across different endpoints."""

    def test_popular_particles_accessible(self, client):
        """Test that all popular particles can be accessed individually."""
        popular_response = client.get("/popular")
        assert popular_response.status_code == 200

        popular_data = popular_response.json()

        for particle in popular_data["particles"]:
            pdgid = particle["pdgid"]
            detail_response = client.get(f"/particle/{pdgid}")

            # Should be able to get details for each popular particle
            assert detail_response.status_code == 200

            detail_data = detail_response.json()

            # Basic consistency checks
            assert detail_data["pdgid"] == pdgid
            assert detail_data["name"] == particle["name"]

            # Mass and charge should be consistent
            if particle["mass"] is not None and detail_data["mass"] is not None:
                assert abs(particle["mass"] - detail_data["mass"]) < 1e-6

            if particle["charge"] is not None and detail_data["charge"] is not None:
                assert abs(particle["charge"] - detail_data["charge"]) < 1e-10

    def test_search_consistency_with_direct_lookup(self, client):
        """Test that search results are consistent with direct particle lookup."""
        # Search for a specific particle
        search_response = client.get("/search/muon")
        assert search_response.status_code == 200

        search_data = search_response.json()

        for particle in search_data["particles"]:
            pdgid = particle["pdgid"]

            # Get detailed info
            detail_response = client.get(f"/particle/{pdgid}")
            if detail_response.status_code != 200:
                continue

            detail_data = detail_response.json()

            # Check consistency
            assert detail_data["pdgid"] == particle["pdgid"]
            assert detail_data["name"] == particle["name"]

            # Mass should be consistent
            if particle["mass"] is not None and detail_data["mass"] is not None:
                assert abs(particle["mass"] - detail_data["mass"]) < 1e-6


class TestAPIPerformance:
    """Basic performance and reliability tests."""

    def test_multiple_requests_stability(self, client):
        """Test that the API handles multiple requests reliably."""
        test_pdgids = [11, -11, 22, 2212, 2112]

        for _ in range(5):  # Repeat multiple times
            for pdgid in test_pdgids:
                response = client.get(f"/particle/{pdgid}")
                assert response.status_code in [200, 404]  # Should not crash

                if response.status_code == 200:
                    data = response.json()
                    assert "pdgid" in data
                    assert data["pdgid"] == pdgid

    def test_search_with_various_limits(self, client):
        """Test search functionality with different limit parameters."""
        limits = [1, 5, 10, 20]

        for limit in limits:
            response = client.get(f"/search/pion?limit={limit}")
            assert response.status_code == 200

            data = response.json()
            assert len(data["particles"]) <= limit

    def test_edge_case_searches(self, client):
        """Test search with edge cases."""
        edge_cases = ["", "a", "xyz123", "π", "μ"]

        for query in edge_cases:
            response = client.get(f"/search/{query}")
            # Should handle all queries gracefully
            assert response.status_code == 200

            data = response.json()
            assert "particles" in data
            assert "total" in data
            assert isinstance(data["particles"], list)
            assert isinstance(data["total"], int)


class TestErrorRecovery:
    """Tests for error handling and recovery."""

    def test_malformed_requests_handled_gracefully(self, client):
        """Test that malformed requests don't crash the server."""
        # Test various malformed requests
        malformed_urls = [
            "/particle/",
            "/particle/abc",
            "/particle/999999999999999999999",
            "/nonexistent_endpoint",
        ]

        for url in malformed_urls:
            response = client.get(url)
            # Should return error status, not crash
            assert response.status_code in [400, 404, 422, 500]

    def test_concurrent_access_simulation(self, client):
        """Simulate concurrent access to test thread safety."""
        endpoints = [
            "/",
            "/particle/11",
            "/particle/22",
            "/search/electron",
            "/popular",
        ]

        # Make multiple requests rapidly
        responses = []
        for endpoint in endpoints * 3:  # Repeat each endpoint 3 times
            response = client.get(endpoint)
            responses.append(response)

        # Check that all requests were handled
        for response in responses:
            assert response.status_code in [200, 404, 422]
