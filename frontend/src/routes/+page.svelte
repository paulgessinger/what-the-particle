<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  import ParticleCard from '../lib/components/ParticleCard.svelte';
  import SearchBar from '../lib/components/SearchBar.svelte';
  import PopularParticles from '../lib/components/PopularParticles.svelte';

  // Use the same origin as the current page when served by FastAPI
  const API_BASE = typeof window !== 'undefined' 
    ? window.location.origin
    : 'http://localhost:8765';

  let searchQuery = '';
  let currentParticle = null;
  let loading = false;
  let error = null;
  let popularParticles = [];

  onMount(async () => {
    // Load popular particles on mount
    try {
      const response = await axios.get(`${API_BASE}/popular`);
      popularParticles = response.data.particles;
    } catch (err) {
      console.error('Failed to load popular particles:', err);
    }

    // Check URL parameters for deep linking
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const particleId = urlParams.get('particle');
      
      if (particleId) {
        const pdgId = parseInt(particleId);
        if (!isNaN(pdgId)) {
          searchQuery = particleId;
          await searchParticle(pdgId);
        }
      }
    }
  });

  async function searchParticle(pdgId) {
    if (!pdgId) return;

    loading = true;
    error = null;

    try {
      const response = await axios.get(`${API_BASE}/particle/${pdgId}`);
      currentParticle = response.data;
      
      // Update URL with the particle ID
      if (typeof window !== 'undefined') {
        const url = new URL(window.location);
        url.searchParams.set('particle', pdgId);
        window.history.pushState({}, '', url);
      }
    } catch (err) {
      error = err.response?.data?.detail || 'Failed to fetch particle data';
      currentParticle = null;
    } finally {
      loading = false;
    }
  }

  async function searchParticleByText(query) {
    if (!query) return;

    loading = true;
    error = null;

    try {
      const response = await axios.get(`${API_BASE}/search/${encodeURIComponent(query)}`);
      const results = response.data.particles;
      
      if (results.length > 0) {
        // If we get results, show the first one
        await searchParticle(results[0].pdgid);
      } else {
        error = `No particles found matching "${query}"`;
        currentParticle = null;
      }
    } catch (err) {
      error = err.response?.data?.detail || 'Failed to search particles';
      currentParticle = null;
    } finally {
      loading = false;
    }
  }

  function handleSearch(event) {
    if (event.detail.pdgId) {
      searchParticle(event.detail.pdgId);
    } else if (event.detail.textQuery) {
      searchParticleByText(event.detail.textQuery);
    }
  }

  function handlePopularParticleClick(particle) {
    searchQuery = particle.pdgid.toString();
    searchParticle(particle.pdgid);
  }
</script>

<svelte:head>
  <title>Particle Explorer - Discover Fundamental Particles</title>
  <meta name="description" content="Explore the world of particle physics. Search for particles by PDG ID and discover their properties, masses, charges, and more." />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
  <!-- Hero Section -->
  <div class="relative overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
      <div class="text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 animate-fade-in">
          Explore the <span class="bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">Quantum Universe</span>
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto animate-fade-in">
          Discover fundamental particles using PDG IDs. Search through the complete database of quarks, leptons, bosons, and more with detailed physics properties.
        </p>

        <!-- Search Interface -->
        <div class="max-w-2xl mx-auto mb-16 animate-slide-up">
          <SearchBar bind:searchQuery on:search={handleSearch} {loading} />
        </div>
      </div>
    </div>

    <!-- Floating particles background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-primary-400 rounded-full animate-pulse-subtle"></div>
      <div class="absolute top-1/3 right-1/3 w-3 h-3 bg-purple-400 rounded-full animate-pulse-subtle" style="animation-delay: 0.5s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-1 h-1 bg-blue-400 rounded-full animate-pulse-subtle" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-1/3 right-1/4 w-2 h-2 bg-green-400 rounded-full animate-pulse-subtle" style="animation-delay: 1.5s;"></div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Popular Particles Sidebar -->
      <div class="lg:col-span-1">
        <PopularParticles
          particles={popularParticles}
          on:particleClick={(e) => handlePopularParticleClick(e.detail)}
        />
      </div>

      <!-- Main Content Area -->
      <div class="lg:col-span-2">
        {#if loading}
          <div class="card text-center py-12">
            <div class="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p class="text-gray-600 dark:text-gray-400">Searching particle database...</p>
          </div>
        {:else if error}
          <div class="card border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0">
                <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-medium text-red-800 dark:text-red-200">Particle Not Found</h3>
                <p class="text-red-600 dark:text-red-300">{error}</p>
              </div>
            </div>
          </div>
        {:else if currentParticle}
          <ParticleCard particle={currentParticle} on:antiparticleClick={(e) => searchParticle(e.detail.pdgid)} />
        {:else}
          <div class="card text-center py-12">
            <div class="text-6xl mb-4">🔍</div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Search for a Particle</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">Enter a PDG ID above to discover detailed particle information</p>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-500 dark:text-gray-400">
              <div>
                <span class="font-medium">Examples:</span>
              </div>
              <div>11 (electron)</div>
              <div>2212 (proton)</div>
              <div>22 (photon)</div>
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>
